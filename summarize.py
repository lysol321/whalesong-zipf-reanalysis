"""Tables (markdown, stdout + results/summary.json) and figures from results/real.json + results/null_*.json.
Usage: python -I summarize.py <data_s2.csv>"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import pipeline as P
from run_nulls import NULLS

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "results")
LABEL = {"shuffle": "shuffle (authors)", "rotate": "rotate (authors)", "markov1": "Markov-1",
         "markov2": "Markov-2", "repeat": "repeat skeleton + Markov-1",
         "markov2cv": "Markov-2, leave-one-recording-out", "markov2wb": "Markov-2, Witten-Bell"}
PAPER_Z = {("shuffle", "fwd2_r50"): 23.09, ("shuffle", "fwd3_r50"): 26, ("shuffle", "bwd2_r50"): 24.67,
           ("shuffle", "fwd2_r25"): 19.14, ("shuffle", "fwd2_r75"): 20.04,  # last two: Code S1 printout
           ("rotate", "fwd2_r50"): 14.43, ("rotate", "fwd3_r50"): 17.55, ("rotate", "bwd2_r50"): 17.32}
INK, MUTED, GRID, ACCENT = "#0b0b0b", "#52514e", "#e4e3df", "#eb6834"
SERIES = ["#2a78d6", "#1baf7a", "#eda100", "#e87ba4", "#6250d6"]  # one colour per null series


def stat(real, null, upper):
    """z and one-sided empirical p. upper=True: H1 real > null (R^2). upper=False: H1 real < null (steeper
    brevity), p = (1 + #null at least as extreme) / (N + 1)."""
    null = np.asarray([x for x in null if x == x])
    z = (real - null.mean()) / null.std()
    k = (null >= real).sum() if upper else (null <= real).sum()
    return {"mean": float(null.mean()), "sd": float(null.std()), "z": float(z),
            "p": float((1 + k) / (len(null) + 1)), "n": int(len(null)),
            "q025": float(np.quantile(null, .025)), "q975": float(np.quantile(null, .975))}


def main(path):
    sys.stdout.reconfigure(encoding="utf-8")
    real = json.load(open(os.path.join(RES, "real.json")))
    nulls = {n: json.load(open(os.path.join(RES, f"null_{n}.json"))) for n in NULLS
             if os.path.exists(os.path.join(RES, f"null_{n}.json"))}
    S = {"real": {v: {k: real[v][k] for k in ("r2", "slope", "tau", "types")} for v in P.VARIANTS}, "nulls": {}}
    print("## Null results (one-sided empirical p; z = (real - mean)/sd)\n")
    print("| null | pipeline | N | R² null mean [95%] | z R² | p(null R² ≥ real) | Poisson slope null mean | z slope | p(null slope ≤ real) | Kendall τ null mean | z τ | p(null τ ≤ real) | paper z R² |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for n, recs in nulls.items():
        S["nulls"][n] = {}
        for v in P.VARIANTS:
            r2 = stat(real[v]["r2"], [r[v]["r2"] for r in recs], True)
            sl = stat(real[v]["slope"], [r[v]["slope"] for r in recs], False)
            tau = stat(real[v]["tau"], [r[v]["tau"] for r in recs], False)
            S["nulls"][n][v] = {"r2": r2, "slope": sl, "tau": tau,
                                "types_mean": float(np.mean([r[v]["types"] for r in recs]))}
            pz = PAPER_Z.get((n, v), "")
            print(f"| {LABEL[n]} | {v} | {r2['n']} | {r2['mean']:.3f} [{r2['q025']:.3f}, {r2['q975']:.3f}] | {r2['z']:.1f} | "
                  f"{r2['p']:.4f} | {sl['mean']:.3f} | {sl['z']:.1f} | {sl['p']:.4f} | {tau['mean']:.3f} | {tau['z']:.1f} | {tau['p']:.4f} | {pz} |")
    print("\nReal:", {v: {k: round(x, 4) for k, x in S["real"][v].items()} for v in P.VARIANTS})

    # CSN power-law check, main pipeline
    print("\n## CSN power-law fit to type frequencies (main pipeline)\n")
    print("| data | α (pooled) | xmin | KS D | LR vs lognormal R (pooled) | years with R<0 | per-year α range | GOF p (pooled) |")
    print("|---|---|---|---|---|---|---|---|")
    c = real["csn"]
    yrs = [y for y in c if y != "pooled"]
    S["csn_real"] = c
    print(f"| real | {c['pooled']['alpha']:.3f} | {c['pooled']['xmin']:.0f} | {c['pooled']['D']:.3f} | {c['pooled']['lr_R']:.2f} (p={c['pooled']['lr_p']:.1e}) | "
          f"{sum(c[y]['lr_R'] < 0 for y in yrs)}/8 | {min(c[y]['alpha'] for y in yrs):.2f}–{max(c[y]['alpha'] for y in yrs):.2f} | {c['pooled'].get('gof_p', 'n/a')} |")
    S["csn_nulls"] = {}
    for n, recs in nulls.items():
        a = np.array([r["csn"]["pooled"]["alpha"] for r in recs])
        d = np.array([r["csn"]["pooled"]["D"] for r in recs])
        R = np.array([r["csn"]["pooled"]["lr_R"] for r in recs])
        xm = np.array([r["csn"]["pooled"]["xmin"] for r in recs])
        neg = np.mean([sum(r["csn"][y]["lr_R"] < 0 for y in yrs) for r in recs])
        S["csn_nulls"][n] = {"alpha_med": float(np.median(a)), "alpha_q": [float(np.quantile(a, .025)), float(np.quantile(a, .975))],
                             "D_med": float(np.median(d)), "R_med": float(np.median(R)), "frac_R_neg": float(np.mean(R < 0)),
                             "xmin_med": float(np.median(xm)), "years_R_neg_mean": float(neg)}
        print(f"| {LABEL[n]} (median of {len(recs)}) | {np.median(a):.3f} [{np.quantile(a, .025):.2f}, {np.quantile(a, .975):.2f}] | {np.median(xm):.0f} | "
              f"{np.median(d):.3f} | {np.median(R):.2f} ({100 * np.mean(R < 0):.0f}% < 0) | {neg:.1f}/8 | | |")
    print("\nPer-year real CSN:")
    for y in yrs:
        f = c[y]
        print(f"  {y}: α={f['alpha']:.3f} xmin={f['xmin']:.0f} ntail={f['ntail']} D={f['D']:.3f} R={f['lr_R']:.2f} p_LR={f['lr_p']:.3f} GOF p={f.get('gof_p', 'n/a')}")
    json.dump(S, open(os.path.join(RES, "summary.json"), "w"), indent=1)
    figures(path, real, nulls)


def figures(path, real, nulls):
    plt.rcParams.update({"font.size": 9, "axes.edgecolor": MUTED, "axes.labelcolor": INK, "xtick.color": MUTED,
                         "ytick.color": MUTED, "axes.spines.top": False, "axes.spines.right": False})
    names = [n for n in NULLS if n in nulls]
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.8), sharey=True)
    for ax, (key, title) in zip(axes, [("r2", "Zipf fit R² (higher = more Zipfian)"),
                                      ("slope", "Brevity: Poisson slope (lower = steeper)"),
                                      ("tau", "Brevity: Kendall τ (lower = stronger)")]):
        for i, n in enumerate(names):
            x = np.array([r[P.MAIN][key] for r in nulls[n]])
            lo, q1, md, q3, hi = np.quantile(x, [.025, .25, .5, .75, .975])
            ax.plot([lo, hi], [i, i], color=MUTED, lw=1.5, solid_capstyle="round")
            ax.plot([q1, q3], [i, i], color=MUTED, lw=6, solid_capstyle="round", alpha=.55)
            ax.plot(md, i, "o", ms=6, color=INK, mec="white", mew=1.5)
        ax.axvline(real[P.MAIN][key], color=ACCENT, lw=2)
        ax.text(real[P.MAIN][key], len(names) - .45, " real", color=INK, va="bottom", ha="left", fontsize=8)
        ax.set_title(title, fontsize=9, color=INK, loc="left")
        ax.grid(axis="x", color=GRID, lw=.8)
        ax.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(5))
        ax.set_axisbelow(True)
    axes[0].set_yticks(range(len(names)), [LABEL[n] for n in names])
    axes[0].set_ylim(-.6, len(names) - .1)
    fig.suptitle("Main pipeline (forward TPs, ratio 0.5): 1000 surrogates per null — median, IQR, 95% range; orange = real song",
                 fontsize=9, color=MUTED, x=.01, ha="left")
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "fig_nulls.png"), dpi=150)

    # rank-frequency: real vs the i=0 surrogate of each null, mean count per rank over years (as paper Fig. 2A)
    data, vocab = P.load(path)
    V = len(vocab)

    def curve(d, segs=None):
        segs = segs or P.segment_all(d, V, P.MAIN)
        fs = [np.sort(list(c.values()))[::-1] for c in P.counts_all(d, segs).values()]
        m = max(map(len, fs))
        return np.array([np.mean([f[i] for f in fs if len(f) > i]) for i in range(m)])

    fig, ax = plt.subplots(figsize=(5.5, 4))
    tables1 = {y: P.markov_tables(r, 1) for y, r in data.items()}
    tables2 = {y: P.markov_tables(r, 2) for y, r in data.items()}
    blocks = {y: [P.tandem_blocks(r) for r in rs] for y, rs in data.items()}
    sur = {"shuffle": lambda g: P.shuffle(data, g), "markov1": lambda g: P.markov(data, 1, g, tables1),
           "markov2": lambda g: P.markov(data, 2, g, tables2), "repeat": lambda g: P.repeat_surrogate(data, g, tables1, blocks)}
    for i, n in enumerate(["shuffle", "markov1", "markov2", "repeat"]):
        y = curve(sur[n](np.random.default_rng([NULLS.index(n), 0])))
        ax.loglog(np.arange(1, len(y) + 1), y, color=SERIES[i], lw=1.5, label=LABEL[n])
    y = curve(data)
    ax.loglog(np.arange(1, len(y) + 1), y, color=INK, lw=2.2, label="real song")
    ax.set_xlabel("rank")
    ax.set_ylabel("mean count over 8 years")
    ax.grid(color=GRID, lw=.8)
    ax.legend(frameon=False, fontsize=8)
    ax.set_title("Sub-sequence rank–frequency, main pipeline (one surrogate each)", fontsize=9, loc="left")
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "fig_rankfreq.png"), dpi=150)


if __name__ == "__main__":
    main(sys.argv[1])
