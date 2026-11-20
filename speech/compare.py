"""Whale song vs speech samples A and B on the same scale: for each pipeline, the distance of real data's z from
each fake-song truth (in that truth's SD units, Markov-1 / Markov-2) and whether it falls inside the band.
Usage (from whalesong/speech): python -I compare.py   -> results/compare.md"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import numpy as np

import pipeline as P

WHALE = os.path.join(os.path.dirname(HERE), "results")
LABEL = {"fwd2_r50": "ratio 0.5 (main)", "fwd2_r25": "ratio 0.25", "fwd2_r75": "ratio 0.75",
         "fwd3_r50": "trigram TPs", "bwd2_r50": "backward TPs"}
TRUTHS = {"2": "two-back per year", "3": "three-back per year", "rec2": "two-back per recording"}


def real_z(src):
    """-> {variant: (Markov-1 z, Markov-2 z)} for whale (summary.json) or a speech sample (null files)."""
    if src == "whale":
        s = json.load(open(os.path.join(WHALE, "summary.json")))
        return {v: tuple(s["nulls"][f"markov{k}"][v]["r2"]["z"] for k in (1, 2)) for v in P.VARIANTS}
    res = os.path.join(HERE, "results", src)
    real_ = json.load(open(os.path.join(res, "real.json")))
    out = {}
    for v in P.VARIANTS:
        zs = []
        for k in (1, 2):
            null = np.array([r[v]["r2"] for r in json.load(open(os.path.join(res, f"null_markov{k}.json")))])
            zs.append((real_[v]["r2"] - null.mean()) / null.std())
        out[v] = tuple(zs)
    return out


def bands(src, t):
    d = WHALE if src == "whale" else os.path.join(HERE, "results", src)
    recs = json.load(open(os.path.join(d, f"smalldata_ncv{t}.json")))
    return {v: [np.array([r[f"markov{k}"][v]["z"] for r in recs]) for k in (1, 2)] for v in P.VARIANTS}


def main():
    srcs = ["whale", "A", "B", "SA", "SB"]
    rz = {s: real_z(s) for s in srcs}
    bd = {s: {t: bands(s, t) for t in TRUTHS} for s in srcs}
    L = ["# Whale song vs child-directed speech (phonemes A, B; syllables SA, SB) under the same calibration", "",
         "Samples A, B are phonemes; SA, SB syllables. Cell: real z's distance from the truth's mean z in that truth's SD, Markov-1 / Markov-2; * = inside the "
         "[min, max] band on both nulls.", ""]
    for t, name in TRUTHS.items():
        L += [f"## {name}", "", "| pipeline | whale | phonemes A | phonemes B | syllables SA | syllables SB |", "|---|---|---|---|---|---|"]
        for v in P.VARIANTS:
            cells = []
            for s in srcs:
                b = bd[s][t][v]
                d = [(rz[s][v][k] - b[k].mean()) / b[k].std() for k in (0, 1)]
                inside = all(b[k].min() <= rz[s][v][k] <= b[k].max() for k in (0, 1))
                cells.append(f"{d[0]:+.1f} / {d[1]:+.1f}" + (" *" if inside else ""))
            L.append(f"| {LABEL[v]} | " + " | ".join(cells) + " |")
        L.append("")
    L += ["## Real z (Markov-1 / Markov-2)", "", "| pipeline | whale | phonemes A | phonemes B | syllables SA | syllables SB |", "|---|---|---|---|---|---|"]
    for v in P.VARIANTS:
        L.append(f"| {LABEL[v]} | " + " | ".join(f"{rz[s][v][0]:+.1f} / {rz[s][v][1]:+.1f}" for s in srcs) + " |")
    md = "\n".join(L) + "\n"
    open(os.path.join(HERE, "results", "compare.md"), "w", encoding="utf-8").write(md)
    sys.stdout.reconfigure(encoding="utf-8")
    print(md)


if __name__ == "__main__":
    main()
