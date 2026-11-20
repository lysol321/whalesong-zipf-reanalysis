"""Natural-speech control: whale-matched phoneme samples from CHILDES Brent-Ratner (make_speech.py) through the
identical whale code. Sample A = first 45,749 phonemes, B = the next 45,749 (replication). Results go to
results/<A|B>/; the whale results are not touched.

Usage (from whalesong/speech):
  python -I run_speech.py                              self-check
  python -I run_speech.py <A|B|SA|SB> real                   real-data metrics on all five pipelines
  python -I run_speech.py <A|B|SA|SB> null <name> [N=1000]   name as run_nulls.NULLS (checkpointed, resumable)
  python -I run_speech.py <A|B|SA|SB> ce | het | copy        held-out order choice, recording differences, copying
  python -I run_speech.py <A|B|SA|SB> ncv <1|2|3|4|rec2|rec3> [N=1000] [D=20]
  python -I run_speech.py <A|B|SA|SB> words                  TP cuts vs true word boundaries
  python -I run_speech.py <A|B|SA|SB> report                 -> results/<A|B>/tables.md
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))  # whalesong/
import numpy as np

import pipeline as P
import run_nulls as RN
import smalldata as S
from lowprio import set_idle

SEED_OFF = 700  # calibration truths [700 + k, d]; whale 0, finch 300, Simon game 600
V_LABEL = {"fwd2_r50": "ratio 0.5 (main)", "fwd2_r25": "ratio 0.25", "fwd2_r75": "ratio 0.75",
           "fwd3_r50": "trigram TPs", "bwd2_r50": "backward TPs"}
TRUTHS = ("1", "2", "3", "4", "rec2", "rec3")


def paths(tag):
    res = os.path.join(HERE, "results", tag)
    os.makedirs(res, exist_ok=True)
    return os.path.join(HERE, "data", f"speech_{tag}.csv"), os.path.join(HERE, "data", f"words_{tag}.json"), res


def real(tag):
    csv_, _, res = paths(tag)
    data, voc = P.load(csv_)
    out = {"V": len(voc)}
    for v in P.VARIANTS:
        m = P.metrics(P.counts_all(data, P.segment_all(data, len(voc), v)))
        out[v] = {k: m[k] for k in ("r2", "slope", "tau", "types", "tokens")}
    json.dump(out, open(os.path.join(res, "real.json"), "w"), indent=1)
    print(json.dumps(out, indent=1))


def align(data, words, V, variant, segs=None):
    """Precision / recall of TP cuts against true word starts (a recording's first position is never a cut) and
    the chance precision, the share of cuttable positions that are word starts."""
    hits = cuts = starts = cuttable = 0
    for y, ys in (segs or P.segment_all(data, V, variant)).items():
        for lens, ws in zip(ys, words[y]):
            c = set(np.cumsum(lens)[:-1].tolist())
            w = set(ws) - {0}
            hits += len(c & w)
            cuts += len(c)
            starts += len(w)
            cuttable += int(lens.sum()) - 1
    return {"precision": hits / cuts if cuts else float("nan"), "recall": hits / starts,
            "chance_precision": starts / cuttable, "cuts": cuts}


def words_mode(tag):
    csv_, wj, res = paths(tag)
    data, voc = P.load(csv_)
    words = json.load(open(wj))
    out = {v: align(data, words, len(voc), v) for v in P.VARIANTS}
    json.dump(out, open(os.path.join(res, "words.json"), "w"), indent=1)
    print(json.dumps(out, indent=1))


def _zp_low(real_, null):
    """One-sided p for brevity: share of nulls at least as negative (strong) as real, as summarize.py."""
    null = np.asarray(null, float)
    return float((real_ - null.mean()) / null.std()), float((1 + (null <= real_).sum()) / (len(null) + 1))


def report(tag):
    _, _, res = paths(tag)
    real_ = json.load(open(os.path.join(res, "real.json")))
    V = list(P.VARIANTS)
    corpus, unit = ("UCI_Brent_Syl", "syllable") if tag.startswith("S") else ("Brent-Ratner", "phoneme")
    L = [f"# Speech sample {tag}: CHILDES {corpus} {unit}s in the whale layout ({real_['V']} {unit} types)", "",
         "## Nulls: R² (null mean, z, p(null ≥ real))", "",
         "| null | " + " | ".join(V_LABEL[v] for v in V) + " |", "|---|" + "---|" * len(V),
         "| real | " + " | ".join(f"{real_[v]['r2']:.3f}" for v in V) + " |"]
    nz = {}
    for n in RN.NULLS:
        p = os.path.join(res, f"null_{n}.json")
        if not os.path.exists(p):
            continue
        recs = json.load(open(p))
        nz[n] = {}
        cells = []
        for v in V:
            z, pv = S.zp(real_[v]["r2"], [r[v]["r2"] for r in recs])
            nz[n][v] = {"r2": {"n": len(recs), "mean": float(np.mean([r[v]["r2"] for r in recs])), "z": z, "p": pv}}
            cells.append(f"{nz[n][v]['r2']['mean']:.3f}, z {z:+.1f}, p {pv:.3f}")
        L.append(f"| {n} (N={len(recs)}) | " + " | ".join(cells) + " |")
    L += ["", "## Brevity, main pipeline (z and p(null at least as strong as real))", "",
          "| null | Kendall τ null mean | z | p | Poisson slope null mean | z | p |", "|---|---|---|---|---|---|---|",
          f"| real | {real_['fwd2_r50']['tau']:.3f} | | | {real_['fwd2_r50']['slope']:.3f} | | |"]
    for n in nz:
        recs = json.load(open(os.path.join(res, f"null_{n}.json")))
        t, s = [r["fwd2_r50"]["tau"] for r in recs], [r["fwd2_r50"]["slope"] for r in recs]
        zt, pt = _zp_low(real_["fwd2_r50"]["tau"], t)
        zs, ps = _zp_low(real_["fwd2_r50"]["slope"], s)
        L.append(f"| {n} | {np.mean(t):.3f} | {zt:+.1f} | {pt:.3f} | {np.mean(s):.3f} | {zs:+.1f} | {ps:.3f} |")
    ncv = {t: json.load(open(p)) for t in TRUTHS if os.path.exists(p := os.path.join(res, f"smalldata_ncv{t}.json"))}
    if ncv and "markov1" in nz and "markov2" in nz:
        fake = {"real": {v: {"r2": real_[v]["r2"]} for v in V},
                "nulls": {f"markov{k}": {v: nz[f"markov{k}"][v] for v in V} for k in (1, 2)}}
        L += ["", "## Calibration bands (Markov-1 / Markov-2 z, [min, max] over fake datasets)", "",
              "| pipeline | real | " + " | ".join(S.tlabel(t) for t in ncv) + " |", "|---|---|" + "---|" * len(ncv)]
        for v in V:
            band = lambda t, m: [r[m][v]["z"] for r in ncv[t]]
            cells = [f"[{min(band(t, 'markov1')):+.1f}, {max(band(t, 'markov1')):+.1f}] / "
                     f"[{min(band(t, 'markov2')):+.1f}, {max(band(t, 'markov2')):+.1f}]" for t in ncv]
            L.append(f"| {V_LABEL[v]} | {nz['markov1'][v]['r2']['z']:+.1f} / {nz['markov2'][v]['r2']['z']:+.1f} | "
                     + " | ".join(cells) + " |")
        L += ["", "SD distance of real song's z from each truth's mean z (Markov-1 / Markov-2):", "",
              "| pipeline | " + " | ".join(S.tlabel(t) for t in ncv) + " |", "|---|" + "---|" * len(ncv)]
        for v in V:
            cells = []
            for t in ncv:
                ds = []
                for k in (1, 2):
                    z = np.array([r[f"markov{k}"][v]["z"] for r in ncv[t]])
                    ds.append((nz[f"markov{k}"][v]["r2"]["z"] - z.mean()) / z.std())
                cells.append(f"{ds[0]:+.1f} / {ds[1]:+.1f}")
            L.append(f"| {V_LABEL[v]} | " + " | ".join(cells) + " |")
        for v in V:
            S._nc_table(L, ncv, lambda r, v=v: (r["r2"][v], r["markov1"][v], r["markov2"][v]), fake, v,
                        f"### Calibration detail, {V_LABEL[v]}")
    for name, title in (("smalldata_ce.json", "Held-out order choice"), ("smalldata_het.json", "Recording differences"),
                        ("smalldata_copy.json", "Copying"), ("words.json", "TP cuts vs word boundaries")):
        p = os.path.join(res, name)
        if not os.path.exists(p):
            continue
        d = json.load(open(p))
        L += ["", f"## {title}", ""]
        if name == "smalldata_ce.json":
            L.append("pooled bits per element by order: " + ", ".join(f"{o}: {x:.3f}" for o, x in d["ce_pooled"].items())
                     + f"; best order per group: {list(d['best_order'].values())}; unseen order-2 contexts "
                     f"{100 * d['unseen_pooled']['2']:.1f}%")
        elif name == "smalldata_het.json":
            for t, rows in d.items():
                c, u = [x["ce2"] for x in rows], [100 * x["unseen2"] for x in rows]
                L.append(f"- {S.tlabel(t)}: {min(c):.3f}–{max(c):.3f} bits, {min(u):.1f}–{max(u):.1f}% unseen")
        elif name == "smalldata_copy.json":
            L.append(", ".join(f"{S.tlabel(t)} {100 * np.mean(x):.1f}%" for t, x in d.items()))
        else:
            for v, a in d.items():
                L.append(f"- {V_LABEL[v]}: precision {a['precision']:.3f} (chance {a['chance_precision']:.3f}), "
                         f"recall {a['recall']:.3f}, cuts {a['cuts']}")
    md = "\n".join(L) + "\n"
    open(os.path.join(res, "tables.md"), "w", encoding="utf-8").write(md)
    sys.stdout.reconfigure(encoding="utf-8")
    print(md)


def _selfcheck():
    data = {"y": [np.array([0, 1, 2, 0, 1, 2, 3, 3]), np.array([2, 1, 0, 2, 1, 0])]}
    words = {"y": [[0, 3, 6], [0, 3]]}
    # by hand: cuts at 3 and 6 in recording 0 (both word starts), none in recording 1; 3 word starts after
    # position 0 out of 7 + 5 = 12 cuttable positions
    a = align(data, words, 4, "fwd2_r50", {"y": [np.array([3, 3, 2]), np.array([6])]})
    assert a == {"precision": 1.0, "recall": 2 / 3, "chance_precision": 3 / 12, "cuts": 2}, a
    b = align(data, words, 4, "fwd2_r50")  # real segmentation path runs and stays in range
    assert b["cuts"] == 0 or 0 <= b["precision"] <= 1
    print("run_speech selfcheck ok")


if __name__ == "__main__":
    a = sys.argv
    if len(a) < 3:
        _selfcheck()
        sys.exit()
    tag, mode = a[1], a[2]
    assert tag in ("A", "B", "SA", "SB"), tag
    csv_, wj, res = paths(tag)
    if mode == "real":
        real(tag)
    elif mode == "null":
        assert a[3] in RN.NULLS
        RN.main(csv_, a[3], int(a[4]) if len(a) > 4 else 1000, res=res)
    elif mode == "words":
        words_mode(tag)
    elif mode == "report":
        report(tag)
    else:
        print("priority class: 0x%x" % (set_idle() or 0), flush=True)
        data, voc = P.load(csv_)
        if mode == "ce":
            json.dump(S.cross_entropy(data, len(voc)), open(os.path.join(res, "smalldata_ce.json"), "w"), indent=1)
        elif mode == "het":
            S.heterogeneity(data, len(voc), 20, S.HET_TRUTHS, res, SEED_OFF)
        elif mode == "copy":
            S.copying(data, 20, res=res, seed_off=SEED_OFF)
        elif mode == "ncv":
            assert a[3] in TRUTHS
            S.run_nc(data, len(voc), a[3], int(a[4]) if len(a) > 4 else 1000, int(a[5]) if len(a) > 5 else 20,
                     allv=True, res=res, seed_off=SEED_OFF)
