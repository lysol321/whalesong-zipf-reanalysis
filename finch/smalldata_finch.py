"""Small-data calibration of the whale analysis (../README.md section 8) applied to the Bengalese finch.

Unit as in run_finch.py: recording = bird x day, bouts within it play the role of the whale's recordings within a
year. 1. Held-out order selection: Witten-Bell chains of order 0-4, leave-one-bout-out within each recording
(smalldata.cross_entropy). 2. Synthetic known-order truths: an order-1/2/3 chain fitted per recording generates
D datasets with the real bout count, lengths and start syllables; each is scored at the paper's three ratios and
against N plain Markov-1 and Markov-2 surrogates fitted per recording to the synthetic data, as run_finch.py
does for real song (smalldata.negative_control_all with a finch scorer).

Usage (from whalesong/finch; checkpoints in results/, reruns resume):
  python -I smalldata_finch.py                                    self-check
  python -I smalldata_finch.py finch_bouts.tsv ce                 -> results/smalldata_ce.json
  python -I smalldata_finch.py finch_bouts.tsv ncv <1|2|3> [N=1000] [D=20] -> results/smalldata_ncv<truth>.json
  python -I smalldata_finch.py finch_bouts.tsv report             -> results/smalldata.json, smalldata_tables.md
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))  # whalesong/: pipeline, smalldata, lowprio
sys.path.insert(0, HERE)
import numpy as np

import pipeline as P
import run_finch as F
import smalldata as S
from lowprio import set_idle

RES = os.path.join(HERE, "results")
SEED_OFF = 300  # finch null seeds are [100-106, i]; truths use [300 + k, d]
RLABEL = {"r50": "ratio 0.5 (main)", "r30": "ratio 0.3", "r70": "ratio 0.7"}


def scorer(V):
    """dataset -> {ratio: mean per-recording rank-frequency R^2}, exactly run_finch.analyse's r2."""
    def score(data):
        out = {}
        for v, ratio in F.RATIOS.items():
            sg = F.seg_all(data, V, ratio)
            out[v] = float(np.nanmean([P.zipf_r2(P.count_words(data[k], sg[k])) for k in data]))
        return out
    return score


def report():
    ce = json.load(open(os.path.join(RES, "smalldata_ce.json")))
    real = json.load(open(os.path.join(RES, "summary.json")))
    ncv = {t: json.load(open(p)) for t in (1, 2, 3)
           if os.path.exists(p := os.path.join(RES, f"smalldata_ncv{t}.json"))}
    orders = [str(o) for o in ce["orders"]]
    cp = ce["ce_pooled"]
    best = [str(b) for b in ce["best_order"].values()]
    L = ["## Table F1. Held-out cross-entropy, bits per syllable (interpolated Witten-Bell, leave-one-bout-out "
         "within each of the 30 recordings), pooled", "",
         "| | " + " | ".join(f"order {o}" for o in orders) + " |", "|---|" + "---|" * len(orders),
         "| pooled | " + " | ".join(f"{cp[o]:.3f}" for o in orders) + " |",
         "| recordings where this order is best | " + " | ".join(str(best.count(o)) for o in orders) + " |", "",
         "Unseen held-out contexts, pooled, by order: " +
         ", ".join(f"order {o}: {100 * v:.1f}%" for o, v in ce["unseen_pooled"].items())]
    summ = {}
    for i, v in enumerate(F.RATIOS):
        summ[v] = S._nc_table(L, ncv, lambda r, v=v: (r["r2"][v], r["markov1"][v], r["markov2"][v]), real, v,
                              f"## Table F2{'abc'[i]}. Synthetic negative control, {RLABEL[v]}")
    md = "\n".join(L) + "\n"
    with open(os.path.join(RES, "smalldata_tables.md"), "w", encoding="utf-8") as fh:
        fh.write(md)
    with open(os.path.join(RES, "smalldata.json"), "w") as fh:
        json.dump({"cross_entropy": ce, "negative_control": summ}, fh, indent=1)
    sys.stdout.reconfigure(encoding="utf-8")
    print(md)


def _selfcheck():
    # scorer on a toy recording set equals run_finch.analyse's R^2 at every ratio
    rng = np.random.default_rng(3)
    toy = {k: [np.array([(i + int(rng.random() < .2)) % 4 for i in range(int(n))]) for n in rng.integers(30, 60, 6)]
           for k in ("b1", "b2")}
    s = scorer(4)(toy)
    a = F.analyse(toy, 4, {"b1": "b", "b2": "b"})
    assert all(np.isclose(s[v], a[v]["r2"]) for v in F.RATIOS), (s, {v: a[v]["r2"] for v in F.RATIOS})
    r = S.negative_control_all(toy, 4, 1, 0, 3, score=scorer(4), seed_off=SEED_OFF)
    assert set(r["r2"]) == set(F.RATIOS) and all(len(r[m][v]["null"]) == 3 for m in ("markov1", "markov2") for v in F.RATIOS)
    print("smalldata_finch selfcheck ok")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        _selfcheck()
        sys.exit()
    mode = sys.argv[2]
    if mode == "report":
        report()
        sys.exit()
    print("priority class: 0x%x" % (set_idle() or 0), flush=True)
    data, bird, recno, printed, V = F.load(sys.argv[1])
    real_r2 = {v: json.load(open(os.path.join(RES, "real.json")))[v]["r2"] for v in F.RATIOS}
    assert all(np.isclose(scorer(V)(data)[v], real_r2[v], rtol=0, atol=1e-12) for v in F.RATIOS), "scorer != real.json"
    if mode == "ce":
        res = S.cross_entropy(data, V)
        with open(os.path.join(RES, "smalldata_ce.json"), "w") as fh:
            json.dump(res, fh, indent=1)
        print("pooled", {o: round(v, 3) for o, v in res["ce_pooled"].items()})
    elif mode == "het":  # held-out order-2 cost of every synthetic dataset, as whale Table 5 (bouts within recordings)
        S.heterogeneity(data, V, 20, ("1", "2", "3"), RES, SEED_OFF)
    elif mode == "ncv":
        assert sys.argv[3] in ("1", "2", "3")
        S.run_nc(data, V, sys.argv[3], int(sys.argv[4]) if len(sys.argv) > 4 else 1000,
                 int(sys.argv[5]) if len(sys.argv) > 5 else 20, allv=True, res=RES, score=scorer(V), seed_off=SEED_OFF)
