"""Human positive control: the Simon-game colour sequences of Arnon & Kirby 2024 (Sci. Rep. 14:5255, the whale
paper's ref. 19; data github.com/smkirby/cultural_evolution_of_statistical_structure, simon_game_data.csv)
through the whale nulls and calibration. A set (chain x generation, 60 sequences) plays the role of a whale year,
a sequence the role of a recording. Their pipeline: trigram TPs per set, sliding cut at a ratio set from the
random generation-0 sets, per-set log-log R^2 (generations 1-10).

Usage (from whalesong/human; the CSV is untrusted: parsed as text, validated, never executed):
  python -I run_human.py                                          self-check
  python -I run_human.py download/simon_game_data.csv real         reproduction + thresholds -> results/real.json
  python -I run_human.py download/simon_game_data.csv null <shuffle|markov1|markov2|markov2cv> [N=1000]
  python -I run_human.py download/simon_game_data.csv ncv <1|2|3> [N=1000] [D=20]
  python -I run_human.py download/simon_game_data.csv report      -> results/tables.md
"""
import csv
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))  # whalesong/: pipeline, smalldata, run_nulls, lowprio
import numpy as np

import pipeline as P
import smalldata as S
from lowprio import set_idle
from run_nulls import save

RES = os.path.join(HERE, "results")
N_TP = 3  # their TPs condition on the previous two colours
NULLS = ["shuffle", "markov1", "markov2", "markov2cv"]  # index seeds the rng: [500 + index, i]
SEED_OFF = 600  # calibration truths use [600 + k, d]; whale 0, finch 300
GROUPS = {"early": range(1, 4), "late": range(8, 11), "all": range(1, 11)}


def load(path):
    """-> {set key 'A03': [int arrays in file order]}, in key order. Validates every row."""
    data = {}
    with open(path, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            c, g, s = row["chain"], int(row["generation"]), row["string"]
            assert c in "ABCDEF" and len(c) == 1 and 0 <= g <= 10 and s and set(s) <= set("RGBY"), row
            data.setdefault(f"{c}{g:02d}", []).append(np.array(["RGBY".index(x) for x in s], np.int64))
    assert all(len(v) == 60 for v in data.values()) and len(data) == 66
    return dict(sorted(data.items()))


def gen_keys(data, g):
    return [k for k in data if int(k[1:]) == g]


def thresholds(data):
    """Generation-0 TP ratios, 5th percentile as their percentile() (sorted[int(n * 0.05)]). Theirs: each TP over
    the sequence's first TP (last_tp never updated in get_distribution_of_pairs_of_TPs). Consecutive: each TP over
    the previous one, which is what the cut rule compares."""
    first, consec = [], []
    for k in gen_keys(data, 0):
        for t in P.transition_probs(data[k], N_TP, True, 4):
            first += list(t[1:] / t[0])
            consec += list(t[1:] / t[:-1])
    pick = lambda r: float(sorted(r)[int(len(r) * 0.05)])
    return {"theirs_first_tp": pick(first), "consecutive": pick(consec), "n_ratios": len(first)}


def scorer(cut):
    """dataset -> mean per-set R^2 for each generation 'g00'..'g10' and each group in GROUPS."""
    def score(data):
        r2 = {k: P.zipf_r2(P.count_words(v, P.segment(v, P.transition_probs(v, N_TP, True, 4), N_TP, cut)))
              for k, v in data.items()}
        out = {f"g{g:02d}": float(np.nanmean([r2[k] for k in gen_keys(data, g)])) for g in range(11)}
        for name, gs in GROUPS.items():
            out[name] = float(np.nanmean([out[f"g{g:02d}"] for g in gs]))
        return out
    return score


def cutoff():
    return json.load(open(os.path.join(RES, "real.json")))["thresholds"]["theirs_first_tp"]


def real(path):
    data = load(path)
    th = thresholds(data)
    out = {"thresholds": th}
    os.makedirs(RES, exist_ok=True)
    out["r2"] = scorer(th["theirs_first_tp"])(data)
    out["r2_consecutive_cut"] = scorer(th["consecutive"])(data)
    json.dump(out, open(os.path.join(RES, "real.json"), "w"), indent=1)
    print(json.dumps(out, indent=1))


def null(path, name, N):
    print("priority class: 0x%x" % (set_idle() or 0), flush=True)
    data, score = load(path), scorer(cutoff())
    out = os.path.join(RES, f"null_{name}.json")
    recs = json.load(open(out)) if os.path.exists(out) else []
    done = {r["i"] for r in recs}
    k = {"markov1": 1, "markov2": 2, "markov2cv": 2}.get(name)
    tabs = ({s: P.markov_tables_cv(v, 2) for s, v in data.items()} if name == "markov2cv" else
            {s: P.markov_tables(v, k) for s, v in data.items()} if k else None)
    t0 = time.time()
    for i in range(N):
        if i in done:
            continue
        rng = np.random.default_rng([500 + NULLS.index(name), i])
        sur = (P.shuffle(data, rng) if name == "shuffle" else
               P.markov_cv(data, 2, rng, tabs) if name == "markov2cv" else P.markov(data, k, rng, tabs))
        recs.append({"i": i, **score(sur)})
        if len(recs) % 100 == 0:
            save(out, recs)
            print(f"{name} {len(recs)}/{N} {time.time() - t0:.0f}s", flush=True)
    save(out, sorted(recs, key=lambda r: r["i"]))
    print(f"{name} done {len(recs)} in {time.time() - t0:.0f}s", flush=True)


def report():
    real_ = json.load(open(os.path.join(RES, "real.json")))
    r = real_["r2"]
    cols = [f"g{g:02d}" for g in range(11)] + list(GROUPS)
    L = [f"Cut ratio {real_['thresholds']['theirs_first_tp']:.4f} (theirs; consecutive-ratio version "
         f"{real_['thresholds']['consecutive']:.4f}).", "",
         "## Nulls: mean per-set R² (cell: null mean, z, p(null ≥ real))", "",
         "| | " + " | ".join(cols) + " |", "|---|" + "---|" * len(cols),
         "| real | " + " | ".join(f"{r[c]:.3f}" for c in cols) + " |"]
    for n in NULLS:
        p = os.path.join(RES, f"null_{n}.json")
        if not os.path.exists(p):
            continue
        recs = json.load(open(p))
        cells = []
        for c in cols:
            v = [x[c] for x in recs if x[c] == x[c]]  # drop surrogates whose R^2 is undefined (all chunks unique)
            z, pv = S.zp(r[c], v)
            cells.append(f"{np.mean(v):.3f}, z {z:+.1f}, p {pv:.3f}" + (f" (n={len(v)})" if len(v) < len(recs) else ""))
        L.append(f"| {n} (N={len(recs)}) | " + " | ".join(cells) + " |")
    ncv = {t: json.load(open(p)) for t in (1, 2, 3) if os.path.exists(p := os.path.join(RES, f"smalldata_ncv{t}.json"))}
    if ncv:
        fake = {"real": {c: {"r2": r[c]} for c in cols}, "nulls": {}}
        for k in (1, 2):
            p = os.path.join(RES, f"null_markov{k}.json")
            recs = json.load(open(p))
            fake["nulls"][f"markov{k}"] = {}
            for c in cols:
                z, pv = S.zp(r[c], [x[c] for x in recs])
                fake["nulls"][f"markov{k}"][c] = {"r2": {"n": len(recs), "mean": float(np.mean([x[c] for x in recs])),
                                                          "z": z, "p": pv}}
        for c in ("all", "early", "late"):
            S._nc_table(L, ncv, lambda x, c=c: (x["r2"][c], x["markov1"][c], x["markov2"][c]), fake, c,
                        f"## Calibration, generations {c} ({list(GROUPS[c])[0]}-{list(GROUPS[c])[-1]})")
    md = "\n".join(L) + "\n"
    open(os.path.join(RES, "tables.md"), "w", encoding="utf-8").write(md)
    sys.stdout.reconfigure(encoding="utf-8")
    print(md)


def _selfcheck():
    rng = np.random.default_rng(0)
    pats = [rng.integers(0, 4, 4) for _ in range(6)]  # a few recurring motifs, so chunk counts vary
    toy = {f"{c}{g:02d}": [np.concatenate([pats[j] for j in rng.integers(0, 6, 3)]) for _ in range(60)]
           for c in "AB" for g in range(11)}
    th = thresholds(toy)
    assert 0 < th["theirs_first_tp"] < 1.5 and 0 < th["consecutive"] < 1.5 and th["n_ratios"] == 2 * 60 * 9
    s = scorer(0.425)(toy)
    assert set(s) == {f"g{g:02d}" for g in range(11)} | set(GROUPS) and all(0 <= v <= 1 for v in s.values())
    # their cut on a hand case: TPs [.5, .5, .1] -> ratio .2 < .425 cuts before element j + n - 1 = 4
    assert P.segment([np.arange(6)], [np.array([.5, .5, .1, .5])], 3, .425)[0].tolist() == [4, 2]
    r = S.negative_control_all(toy, 4, 1, 0, 3, score=scorer(0.425), seed_off=SEED_OFF)
    assert len(r["markov2"]["all"]["null"]) == 3
    print("run_human selfcheck ok")


if __name__ == "__main__":
    a = sys.argv
    if len(a) < 3:
        _selfcheck()
    elif a[2] == "real":
        real(a[1])
    elif a[2] == "null":
        assert a[3] in NULLS
        null(a[1], a[3], int(a[4]) if len(a) > 4 else 1000)
    elif a[2] == "ncv":
        assert a[3] in ("1", "2", "3")
        print("priority class: 0x%x" % (set_idle() or 0), flush=True)
        S.run_nc(load(a[1]), 4, a[3], int(a[4]) if len(a) > 4 else 1000, int(a[5]) if len(a) > 5 else 20,
                 allv=True, res=RES, score=scorer(cutoff()), seed_off=SEED_OFF)
    elif a[2] == "report":
        report()
