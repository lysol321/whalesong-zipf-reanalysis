"""Real-data metrics for every pipeline variant + CSN power-law check on the main variant.
Usage: python -I reproduce.py <data_s2.csv> [nsim]   -> results/real.json"""
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np

import pipeline as P
import powerlaw as PL
from lowprio import set_idle

HERE = os.path.dirname(os.path.abspath(__file__))


def main(path, nsim):
    print("priority class: 0x%x" % (set_idle() or 0))
    data, vocab = P.load(path)
    V = len(vocab)
    out = {"years": list(data), "elements": {y: int(sum(len(r) for r in recs)) for y, recs in data.items()},
           "recordings": {y: len(recs) for y, recs in data.items()}, "vocab": V}
    # sound elements themselves (paper Fig. 2B: R^2 = 0.87)
    unig = {y: P.count_words(recs, [np.ones(len(r), int) for r in recs]) for y, recs in data.items()}
    out["sound_elements_r2"] = float(np.nanmean([P.zipf_r2(c) for c in unig.values()]))
    for v in P.VARIANTS:
        segs = P.segment_all(data, V, v)
        cnt = P.counts_all(data, segs)
        out[v] = P.metrics(cnt)
        out[v]["cuts_per_year"] = float(np.mean([sum(len(l) - 1 for l in segs[y]) for y in data]))
        print(v, {k: out[v][k] for k in ("r2", "slope", "slope_se", "tau", "types", "cuts_per_year")}, flush=True)
        if v == P.MAIN:
            rng = np.random.default_rng(2025)
            t0 = time.time()
            out["csn"] = {y: PL.analyse(list(c.values()), nsim, rng) for y, c in cnt.items()}
            out["csn"]["pooled"] = PL.analyse([f for c in cnt.values() for f in c.values()], nsim, rng)
            print("csn", round(time.time() - t0, 1), "s", flush=True)
            for y, f in out["csn"].items():
                print(" ", y, f and {k: round(f[k], 3) for k in ("alpha", "xmin", "ntail", "D", "lr_R", "lr_p", "gof_p") if k in f})
    with open(os.path.join(HERE, "results", "real.json"), "w") as fh:
        json.dump(out, fh, indent=1)


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 0)
