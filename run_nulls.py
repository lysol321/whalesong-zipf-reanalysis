"""Run N surrogate datasets of one null model through the identical pipeline (all variants) + CSN on the
main variant. Checkpoints to results/null_<name>.json every 25 samples; rerun resumes.
Usage: python -I run_nulls.py <data_s2.csv> <shuffle|rotate|markov1|markov2|repeat|markov2cv|markov2wb> [N=1000]"""
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
NULLS = ["shuffle", "rotate", "markov1", "markov2", "repeat", "markov2cv", "markov2wb"]  # index seeds the rng


def save(path, recs):
    tmp = path + ".tmp"
    with open(tmp, "w") as fh:
        json.dump(recs, fh)
    os.replace(tmp, path)


def main(path, null, N, res=None):
    """res: results directory (default whalesong/results; the speech control writes elsewhere)."""
    print("priority class: 0x%x" % (set_idle() or 0), flush=True)
    data, vocab = P.load(path)
    V = len(vocab)
    out = os.path.join(res or os.path.join(HERE, "results"), f"null_{null}.json")
    recs = json.load(open(out)) if os.path.exists(out) else []
    done = {r["i"] for r in recs}
    real_segs = {v: P.segment_all(data, V, v) for v in P.VARIANTS} if null == "rotate" else None
    k = {"markov1": 1, "markov2": 2, "repeat": 1, "markov2cv": 2, "markov2wb": 2}.get(null)
    fit = {"markov2cv": P.markov_tables_cv, "markov2wb": P.witten_bell_tables}.get(null, P.markov_tables)
    tables = {y: fit(r, k) for y, r in data.items()} if k else None
    blocks = {y: [P.tandem_blocks(r) for r in rs] for y, rs in data.items()} if null == "repeat" else None
    t0 = time.time()
    for i in range(N):
        if i in done:
            continue
        rng = np.random.default_rng([NULLS.index(null), i])
        rec = {"i": i}
        if null == "shuffle":
            sur = P.shuffle(data, rng)
        elif null == "repeat":
            sur = P.repeat_surrogate(data, rng, tables, blocks)
        elif null == "markov2cv":
            sur = P.markov_cv(data, k, rng, tables)
        elif k:
            sur = P.markov(data, k, rng, tables)
        for v in P.VARIANTS:
            if null == "rotate":
                segs = real_segs[v]
                cnt = P.counts_all(P.rotate(data, segs, rng), segs)
            else:
                cnt = P.counts_all(sur, P.segment_all(sur, V, v))
            m = P.metrics(cnt)
            rec[v] = {k: m[k] for k in ("r2", "slope", "tau", "types")}
            if v == P.MAIN:
                rec[v]["r2_year"] = m["r2_year"]
                rec["csn"] = {y: PL.analyse(list(c.values())) for y, c in cnt.items()}
                rec["csn"]["pooled"] = PL.analyse([f for c in cnt.values() for f in c.values()])
        recs.append(rec)
        if len(recs) % 25 == 0:
            save(out, recs)
            print(f"{null} {len(recs)}/{N} {time.time() - t0:.0f}s", flush=True)
    save(out, sorted(recs, key=lambda r: r["i"]))
    print(f"{null} done {len(recs)} in {time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 1000)
