"""Bengalese finch (Kirby et al. 2026, Sci. Adv. 12:eaea3015) through the whale pipeline and nulls.
Unit: recording = bird x day (30); TPs per recording from bigrams within bouts; segmentation per bout.

Usage (from whalesong/finch, data = finch_bouts.tsv made by extract_dataset.py):
  python -I run_finch.py finch_bouts.tsv real
  python -I run_finch.py finch_bouts.tsv null <name> [N=1000]    name in NULLS; checkpoints, resumable
  python -I run_finch.py finch_bouts.tsv summary                 -> results/tables.md, summary.json, fig
"""
import json
import os
import random
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))  # whalesong/: pipeline, powerlaw, lowprio
import numpy as np

import pipeline as P
import powerlaw as PL
from lowprio import set_idle

RATIOS = {"r50": 0.5, "r30": 0.3, "r70": 0.7}  # the paper's three cutting ratios; r50 main
MAIN = "r50"
NULLS = ["shuffle", "rotate", "bigram_authors", "markov1", "markov2", "markov2cv", "markov2wb"]
RES = os.path.join(HERE, "results")


def load(path):
    """-> data {rec: [bout int arrays]}, bird {rec: bird}, recno {rec: 1..5 by day within bird},
    printed {rec: [unit-length arrays]} (the authors' published ratio-0.5 segmentation), vocab size."""
    vocab, data, bird, printed, days = {}, {}, {}, {}, {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            b, d, s = line.rstrip("\n").split("\t")
            d = int(d.replace(" ", ""))
            key = f"{b}{d}"
            units = s.replace("/", " ").split()  # line wraps fall on unit boundaries (checked: cuts/bout exact)
            assert all(c.isalpha() and c.islower() for u in units for c in u)
            seq = "".join(units)
            data.setdefault(key, []).append(np.array([vocab.setdefault(c, len(vocab)) for c in seq], np.int64))
            printed.setdefault(key, []).append(np.array([len(u) for u in units]))
            bird[key] = b
            days.setdefault(b, set()).add(d)
    recno = {k: sorted(days[bird[k]]).index(int(k[len(bird[k]):])) + 1 for k in data}
    return data, bird, recno, printed, len(vocab)


def seg_all(data, V, ratio):
    return {k: P.segment(bs, P.transition_probs(bs, 2, True, V), 2, ratio) for k, bs in data.items()}


def bigram_authors(data, rng):
    """Authors' 'bigram baseline' (Code S1 shuffled_data_bigram_based): per bout, successors drawn from that
    bout's own bigram list; start = random element of the bout; dead end -> random element of the bout."""
    r = random.Random(int(rng.integers(2**63)))
    out = {}
    for k, bs in data.items():
        new = []
        for seq in bs:
            seq = seq.tolist()
            nxt = {}
            for a, b in zip(seq[:-1], seq[1:]):
                nxt.setdefault(a, []).append(b)
            s = [r.choice(seq)]
            for _ in range(len(seq) - 1):
                s.append(r.choice(nxt[s[-1]]) if s[-1] in nxt else r.choice(seq))
            new.append(np.array(s, np.int64))
        out[k] = new
    return out


def analyse(data, V, bird, segs=None, src=None):
    """All ratios: metrics with bird intercepts for brevity (authors: glmer (1|bird)). segs/src: rotation."""
    keys = list(data)
    out = {}
    for v, ratio in RATIOS.items():
        sg = segs[v] if segs else seg_all(data, V, ratio)
        cnt = {k: P.count_words((src or data)[k] if not segs else src[v][k], sg[k]) for k in keys}
        m = P.metrics(cnt, [bird[k] for k in keys])
        out[v] = {"r2": m["r2"], "r2_rec": m["r2_year"], "slope": m["slope"], "slope_se": m["slope_se"],
                  "tau": m["tau"], "tau_rec": [P.brevity_tau(cnt[k]) for k in keys], "types": m["types"],
                  "cuts_per_bout": float(np.mean([len(l) - 1 for k in keys for l in sg[k]]))}
        if v == MAIN:
            out["csn"] = PL.analyse([f for c in cnt.values() for f in c.values()])
    return out


def real(path):
    print("priority class: 0x%x" % (set_idle() or 0))
    data, bird, recno, printed, V = load(path)
    res = analyse(data, V, bird)
    segs = seg_all(data, V, 0.5)
    same = sum(np.array_equal(segs[k][i], printed[k][i]) for k in data for i in range(len(data[k])))
    res["printed_segmentation_match"] = f"{same}/{sum(len(b) for b in data.values())} bouts identical"
    res["recs"] = list(data)
    res["bird"] = [bird[k] for k in data]
    res["recno"] = [recno[k] for k in data]
    res["sound_elements_r2"] = float(np.nanmean([P.zipf_r2(P.count_words(bs, [np.ones(len(b), int) for b in bs]))
                                                  for bs in data.values()]))
    for v in RATIOS:
        print(v, {k: (round(x, 4) if isinstance(x, float) else x) for k, x in res[v].items() if not k.endswith("_rec")})
    print(res["printed_segmentation_match"], "| syllable R2", round(res["sound_elements_r2"], 3))
    os.makedirs(RES, exist_ok=True)
    json.dump(res, open(os.path.join(RES, "real.json"), "w"), indent=1)


def null(path, name, N):
    print("priority class: 0x%x" % (set_idle() or 0), flush=True)
    data, bird, recno, printed, V = load(path)
    out = os.path.join(RES, f"null_{name}.json")
    recs = json.load(open(out)) if os.path.exists(out) else []
    done = {r["i"] for r in recs}
    tabs = None
    if name in ("markov1", "markov2"):
        tabs = {k: P.markov_tables(bs, int(name[-1])) for k, bs in data.items()}
    elif name == "markov2cv":  # leave-one-bout-out within the recording
        tabs = {k: P.markov_tables_cv(bs, 2) for k, bs in data.items()}
    elif name == "markov2wb":
        tabs = {k: P.witten_bell_tables(bs, 2) for k, bs in data.items()}
    real_segs = {v: seg_all(data, V, r) for v, r in RATIOS.items()} if name == "rotate" else None
    t0 = time.time()
    for i in range(N):
        if i in done:
            continue
        rng = np.random.default_rng([100 + NULLS.index(name), i])
        if name == "rotate":
            src = {v: P.rotate(data, real_segs[v], rng) for v in RATIOS}
            rec = analyse(data, V, bird, real_segs, src)
        else:
            sur = {"shuffle": lambda: P.shuffle(data, rng), "bigram_authors": lambda: bigram_authors(data, rng),
                   "markov1": lambda: P.markov(data, 1, rng, tabs), "markov2": lambda: P.markov(data, 2, rng, tabs),
                   "markov2cv": lambda: P.markov_cv(data, 2, rng, tabs),
                   "markov2wb": lambda: P.markov(data, 2, rng, tabs)}[name]()
            rec = analyse(sur, V, bird)
        rec["i"] = i
        recs.append(rec)
        if len(recs) % 25 == 0:
            tmp = out + ".tmp"
            json.dump(recs, open(tmp, "w"))
            os.replace(tmp, out)
            print(f"{name} {len(recs)}/{N} {time.time() - t0:.0f}s", flush=True)
    json.dump(sorted(recs, key=lambda r: r["i"]), open(out + ".tmp", "w"))
    os.replace(out + ".tmp", out)
    print(f"{name} done {len(recs)} in {time.time() - t0:.0f}s", flush=True)


LABEL = {"shuffle": "shuffle (authors)", "rotate": "rotate (authors)", "bigram_authors": "bigram (authors, per bout)",
         "markov1": "Markov-1 (per recording)", "markov2": "Markov-2", "markov2cv": "Markov-2, leave-one-bout-out",
         "markov2wb": "Markov-2, Witten-Bell"}
PAPER_Z = {("shuffle", "r50"): 17.05, ("shuffle", "r30"): 16.32, ("shuffle", "r70"): 9.04,
           ("bigram_authors", "r50"): 6.77, ("bigram_authors", "r30"): 9.22, ("bigram_authors", "r70"): 1.87,
           ("rotate", "r50"): 15.69, ("rotate", "r30"): 11.9, ("rotate", "r70"): 9.661}


def summary(path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from summarize import stat, INK, MUTED, GRID, ACCENT
    sys.stdout.reconfigure(encoding="utf-8")
    real = json.load(open(os.path.join(RES, "real.json")))
    nulls = {n: json.load(open(os.path.join(RES, f"null_{n}.json"))) for n in NULLS
             if os.path.exists(os.path.join(RES, f"null_{n}.json"))}
    S = {"real": {v: {k: real[v][k] for k in ("r2", "slope", "slope_se", "tau", "types", "cuts_per_bout")} for v in RATIOS},
         "nulls": {}, "development": {}}
    print("## Rank-frequency R² (cell: null mean, z, p(null ≥ real); paper z in brackets)\n")
    print("| null | " + " | ".join(f"ratio {RATIOS[v]}" for v in RATIOS) + " |\n|---|---|---|---|")
    print("| real R² | " + " | ".join(f"{real[v]['r2']:.3f}" for v in RATIOS) + " |")
    for n, recs in nulls.items():
        S["nulls"][n] = {}
        cells = []
        for v in RATIOS:
            st = {"r2": stat(real[v]["r2"], [r[v]["r2"] for r in recs], True),
                  "tau": stat(real[v]["tau"], [r[v]["tau"] for r in recs], False),
                  "slope": stat(real[v]["slope"], [r[v]["slope"] for r in recs], False)}
            S["nulls"][n][v] = st
            pz = PAPER_Z.get((n, v))
            cells.append(f"{st['r2']['mean']:.3f}, z={st['r2']['z']:.1f}, p={st['r2']['p']:.3f}" + (f" [{pz}]" if pz else ""))
        print(f"| {LABEL[n]} | " + " | ".join(cells) + " |")
    print("\n## Brevity, ratio 0.5 (p = share of nulls at least as steep/strong as real)\n")
    print("| null | Kendall τ mean [95%] | p(null τ ≤ real) | Poisson slope mean [95%] | p(null ≤ real) | types |\n|---|---|---|---|---|---|")
    print(f"| **real** | {real[MAIN]['tau']:.3f} | | {real[MAIN]['slope']:.4f} (SE {real[MAIN]['slope_se']:.4f}) | | {real[MAIN]['types']} |")
    for n, recs in nulls.items():
        t, s = S["nulls"][n][MAIN]["tau"], S["nulls"][n][MAIN]["slope"]
        print(f"| {LABEL[n]} | {t['mean']:.3f} [{t['q025']:.3f}, {t['q975']:.3f}] | {t['p']:.3f} | {s['mean']:.4f} [{s['q025']:.4f}, {s['q975']:.4f}] | {s['p']:.3f} | {np.mean([r[MAIN]['types'] for r in recs]):.0f} |")
    tau_all = [S["nulls"][n][v]["tau"]["p"] for n in nulls for v in RATIOS]
    print(f"\nKendall τ p over all {len(tau_all)} null×ratio cells: min {min(tau_all):.3f}")

    # development: mean R² over the 6 birds at each recording number (1 = ~day 60-70, 5 = crystallised ~day 120+)
    recno = np.array(real["recno"])
    stages = {f"rec {k}": recno == k for k in range(1, 6)}
    stages["early (rec 1-2)"] = recno <= 2
    stages["crystallised (rec 4-5)"] = recno >= 4
    print("\n## Development, ratio 0.5: mean R² over birds at each recording (cell: null mean, z, p(null ≥ real))\n")
    show = [n for n in ("bigram_authors", "markov1", "markov2", "markov2cv", "markov2wb") if n in nulls]
    print("| stage | real R² | " + " | ".join(LABEL[n] for n in show) + " |")
    print("|---" * (len(show) + 2) + "|")
    for st, msk in stages.items():
        rv = float(np.nanmean(np.array(real[MAIN]["r2_rec"])[msk]))
        S["development"][st] = {"real": rv}
        cells = []
        for n in show:
            nv = [float(np.nanmean(np.array(r[MAIN]["r2_rec"], float)[msk])) for r in nulls[n]]
            s = stat(rv, nv, True)
            S["development"][st][n] = s
            cells.append(f"{s['mean']:.3f}, z={s['z']:.1f}, p={s['p']:.3f}")
        print(f"| {st} | {rv:.3f} | " + " | ".join(cells) + " |")
    print("\n## CSN on pooled type frequencies, ratio 0.5\n")
    c = real["csn"]
    print(f"real: α={c['alpha']:.3f} xmin={c['xmin']:.0f} ntail={c['ntail']} D={c['D']:.3f} LR R={c['lr_R']:.2f} (p={c['lr_p']:.3g})")
    S["csn_real"] = c
    S["csn_nulls"] = {}
    for n, recs in nulls.items():
        a = np.array([r["csn"]["alpha"] for r in recs if r["csn"]])
        R = np.array([r["csn"]["lr_R"] for r in recs if r["csn"]])
        S["csn_nulls"][n] = {"alpha_med": float(np.median(a)), "alpha_q": [float(np.quantile(a, .025)), float(np.quantile(a, .975))],
                             "R_med": float(np.median(R)), "frac_R_neg": float(np.mean(R < 0))}
        print(f"{LABEL[n]}: α median {np.median(a):.3f} [{np.quantile(a, .025):.2f}, {np.quantile(a, .975):.2f}], LR R median {np.median(R):.2f} ({100 * np.mean(R < 0):.0f}% < 0)")
    json.dump(S, open(os.path.join(RES, "summary.json"), "w"), indent=1)

    # figure: nulls on the main ratio + development
    plt.rcParams.update({"font.size": 9, "axes.edgecolor": MUTED, "axes.labelcolor": INK, "xtick.color": MUTED,
                         "ytick.color": MUTED, "axes.spines.top": False, "axes.spines.right": False})
    names = [n for n in NULLS if n in nulls]
    fig, axes = plt.subplots(1, 3, figsize=(11.5, 3.4), gridspec_kw={"width_ratios": [1, 1, 1.15]})
    for ax, (key, title) in zip(axes[:2], [("r2", "Zipf fit R² (higher = more Zipfian)"), ("tau", "Brevity: Kendall τ (lower = stronger)")]):
        for i, n in enumerate(names):
            x = np.array([r[MAIN][key] for r in nulls[n]])
            lo, q1, md, q3, hi = np.quantile(x, [.025, .25, .5, .75, .975])
            ax.plot([lo, hi], [i, i], color=MUTED, lw=1.5, solid_capstyle="round")
            ax.plot([q1, q3], [i, i], color=MUTED, lw=6, solid_capstyle="round", alpha=.55)
            ax.plot(md, i, "o", ms=6, color=INK, mec="white", mew=1.5)
        ax.axvline(real[MAIN][key], color=ACCENT, lw=2)
        ax.text(real[MAIN][key], len(names) - .45, " real", color=INK, va="bottom", fontsize=8)
        ax.set_title(title, fontsize=9, color=INK, loc="left")
        ax.grid(axis="x", color=GRID, lw=.8)
        ax.set_axisbelow(True)
        ax.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(5))
        ax.set_ylim(-.6, len(names) - .1)
    axes[0].set_yticks(range(len(names)), [LABEL[n] for n in names])
    axes[1].set_yticks(range(len(names)), [])
    ax = axes[2]
    xs = np.arange(1, 6)
    for n, col in (("markov2", "#2a78d6"), ("markov2cv", "#1baf7a"), ("bigram_authors", "#eda100")):
        if n not in nulls:
            continue
        m = [S["development"][f"rec {k}"][n] for k in xs]
        ax.fill_between(xs, [s["q025"] for s in m], [s["q975"] for s in m], color=col, alpha=.18, lw=0)
        ax.plot(xs, [s["mean"] for s in m], color=col, lw=1.5, label=LABEL[n])
    ax.plot(xs, [S["development"][f"rec {k}"]["real"] for k in xs], color=INK, lw=2.2, marker="o", ms=5, label="real song")
    ax.set_xticks(xs, ["1\n~day 65", "2", "3", "4", "5\n~day 120"])
    ax.set_xlabel("recording (development)")
    ax.set_title("R² by recording, mean of 6 birds", fontsize=9, color=INK, loc="left")
    ax.grid(color=GRID, lw=.8)
    ax.legend(frameon=False, fontsize=7, loc="lower right")
    fig.suptitle("Bengalese finch, ratio 0.5: 1000 surrogates per null — median, IQR, 95% range; orange = real song",
                 fontsize=9, color=MUTED, x=.01, ha="left")
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "fig_finch.png"), dpi=150)


if __name__ == "__main__":
    a = sys.argv
    if a[2] == "real":
        real(a[1])
    elif a[2] == "null":
        null(a[1], a[3], int(a[4]) if len(a) > 4 else 1000)
    elif a[2] == "summary":
        summary(a[1])
