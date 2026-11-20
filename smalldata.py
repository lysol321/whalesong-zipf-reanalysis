"""Small-data check: does the unsmoothed order-2 null match real
song only because trigram tables are sparse at 1-14k elements per year?

1. Held-out order selection. Per year, interpolated Witten-Bell chains of order 0-4 (the rule of
   pipeline.witten_bell_tables, scored instead of sampled, extended to any order) are fitted
   leave-one-recording-out and scored on the held-out recording: cross-entropy in bits per element,
   token-weighted over recordings; plus the share of held-out order-k contexts unseen in the other
   recordings. The base distribution is uniform over all 239 element types, so every held-out element has
   finite cost and no order is favoured.
2. Synthetic negative control. An order-1 (then order-2, order-3) chain fitted to the real year generates one
   synthetic dataset with the real recording count, lengths and start elements. It is treated as "real":
   main-pipeline R^2, then N plain Markov-1 and N plain Markov-2 surrogates from chains fitted to the
   synthetic data (pipeline.markov with back-off, exactly as run_nulls.py), z and one-sided p as in
   summarize.py. D independent synthetic datasets per truth. `ncv` regenerates the same datasets and
   surrogates from the same seeds and scores each surrogate on all five pipelines (pipeline.VARIANTS), so
   the main-pipeline numbers are identical to `nc` and the other four pipelines get the same calibration.

Usage (from whalesong/; checkpoints in results/, reruns resume):
  python -I smalldata.py                                       self-check
  python -I smalldata.py <data_s2.csv> ce                      -> results/smalldata_ce.json (seconds)
  python -I smalldata.py <data_s2.csv> nc <1|2|3> [N=1000] [D=20] -> results/smalldata_nc<truth>.json (~40 min)
  python -I smalldata.py <data_s2.csv> ncv <1|2|3|4|rec2|rec3> [N=1000] [D=20] -> results/smalldata_ncv<truth>.json
                                                               (all pipelines, ~2x nc; truth_spec explains rec2/rec3)
  python -I smalldata.py <data_s2.csv> het [D=20]              -> results/smalldata_het.json (between-recording differences)
  python -I smalldata.py <data_s2.csv> copy [D=20]             -> results/smalldata_copy.json (8-grams copied from source recording)
  python -I smalldata.py <data_s2.csv> report                  -> results/smalldata.json, smalldata_tables.md
"""
import json
import math
import os
import sys
import time
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np

import pipeline as P
from lowprio import set_idle
from run_nulls import save

RES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
ORDERS = (0, 1, 2, 3, 4)


# ---------------- 1. held-out cross-entropy ----------------

def wb_fit(recs, k):
    """Witten-Bell tables for orders 0..k: order -> {context: (Counter, lam, n)}, lam = n / (n + distinct
    successors). Contexts counted exactly as pipeline.markov_tables (order o from position o on)."""
    cnt = [defaultdict(Counter) for _ in range(k + 1)]
    for r in recs:
        t = r.tolist()
        for i in range(len(t)):
            for o in range(min(i, k) + 1):
                cnt[o][tuple(t[i - o:i])][t[i]] += 1
    return [{h: (c, sum(c.values()) / (sum(c.values()) + len(c)), sum(c.values())) for h, c in tab.items()}
            for tab in cnt]


def wb_prob(tabs, V, h, w):
    """P(w | h) under interpolated Witten-Bell: start from the uniform over V element types and climb the
    suffixes of h; an unseen context has lam = 0 (same rule as pipeline.witten_bell_tables)."""
    p = 1.0 / V
    for o in range(len(h) + 1):
        e = tabs[o].get(h[len(h) - o:])
        if e:
            c, lam, n = e
            p = lam * c.get(w, 0) / n + (1 - lam) * p
    return p


def heldout(recs, k, V):
    """Leave-one-recording-out at order k. Returns raw sums over the year's recordings:
    (bits, elements, unseen order-k contexts, order-k contexts). Positions before k use the shorter
    available context, so every order scores every element."""
    bits = n = unseen = ctx = 0
    for j, r in enumerate(recs):
        tabs = wb_fit(recs[:j] + recs[j + 1:], k)
        t = r.tolist()
        for i, w in enumerate(t):
            h = tuple(t[max(0, i - k):i])
            bits -= math.log2(wb_prob(tabs, V, h, w))
            if k and i >= k:
                ctx += 1
                unseen += h not in tabs[k]
        n += len(t)
    return bits, n, unseen, ctx


def cross_entropy(data, V):
    raw = {y: {o: heldout(recs, o, V) for o in ORDERS} for y, recs in data.items()}
    ce = {y: {o: b / n for o, (b, n, _, _) in d.items()} for y, d in raw.items()}
    unseen = {y: {o: u / c for o, (_, _, u, c) in d.items() if o} for y, d in raw.items()}
    return {"orders": list(ORDERS), "ce": ce, "unseen": unseen,
            "ce_pooled": {o: sum(raw[y][o][0] for y in raw) / sum(raw[y][o][1] for y in raw) for o in ORDERS},
            "unseen_pooled": {o: sum(raw[y][o][2] for y in raw) / sum(raw[y][o][3] for y in raw) for o in ORDERS if o},
            "best_order": {y: min(d, key=d.get) for y, d in ce.items()},
            "recordings": {y: len(r) for y, r in data.items()},
            "elements": {y: int(sum(len(x) for x in r)) for y, r in data.items()}}


# ---------------- 2. synthetic negative control ----------------

VLABEL = {"fwd2_r50": "forward TPs, ratio 0.5 (main)", "fwd2_r25": "forward TPs, ratio 0.25",
          "fwd2_r75": "forward TPs, ratio 0.75", "fwd3_r50": "trigram TPs, ratio 0.5", "bwd2_r50": "backward TPs, ratio 0.5"}


def r2_variant(sur, V, variant):
    """Rank-frequency R^2 of one pipeline variant, as pipeline.metrics computes it."""
    cnt = P.counts_all(sur, P.segment_all(sur, V, variant))
    return float(np.nanmean([P.zipf_r2(c) for c in cnt.values()]))


def r2_main(sur, V):
    """Main-pipeline rank-frequency R^2 (forward TPs, ratio 0.5)."""
    return r2_variant(sur, V, P.MAIN)


def zp(real, null):
    """z = (real - null mean) / null SD, one-sided p = (1 + #null >= real) / (N + 1), as summarize.py."""
    null = np.asarray(null, float)
    return float((real - null.mean()) / null.std()), float((1 + (null >= real).sum()) / (len(null) + 1))


def fit_all(data, k):
    return {y: P.markov_tables(r, k) for y, r in data.items()}


def truth_spec(truth):
    """'1'..'4' -> order-k chain fitted per year, pooled over its recordings (stationary within a year);
    'rec2', 'rec3' -> every recording generated from an order-k chain fitted on that recording alone, so the
    real between-recording differences within a year are kept. -> (kind, k, seed code). Plain orders keep
    seed code k, so truths 1-3 regenerate the section 8.2 datasets exactly."""
    t = str(truth)
    if t.startswith("rec"):
        return "rec", int(t[3:]), 200 + int(t[3:])
    return "pooled", int(t), int(t)


def tlabel(truth):
    kind, k, _ = truth_spec(truth)
    return f"order-{k} chain" + (" per recording" if kind == "rec" else "")


def synth(data, truth, d, seed_off=0):
    """Synthetic dataset d of a ground truth (truth_spec): real recording count, lengths, first k elements."""
    kind, k, code = truth_spec(truth)
    rng = np.random.default_rng([code + seed_off, d])
    if kind == "pooled":
        return P.markov(data, k, rng, fit_all(data, k))
    return {y: [P.markov({y: [r]}, k, rng, {y: P.markov_tables([r], k)})[y][0] for r in recs]
            for y, recs in data.items()}


def negative_control_all(data, V, truth, d, N, variants=tuple(P.VARIANTS), score=None, seed_off=0):
    """One synthetic dataset (seed d) of ground truth `truth` (truth_spec), scored as if it were the real
    data: R^2 on each pipeline in `variants`, then N Markov-1 and N Markov-2 surrogates generated from chains
    fitted to the synthetic data (pipeline.markov, back-off at unseen contexts as run_nulls), every surrogate
    scored on every pipeline. score(dataset) -> {variant: R^2} replaces the whale pipelines (finch). The rng
    sequence does not depend on `variants` or `score`, so the main-pipeline entries are identical whatever
    else is scored.
    -> {"d", "N", "r2": {variant: R^2}, "markov1": {variant: {z, p, mean, sd, null}}, "markov2": {...}}"""
    score = score or (lambda s: {v: r2_variant(s, V, v) for v in variants})
    syn = synth(data, truth, d, seed_off)
    out = {"d": d, "N": N, "r2": score(syn)}
    variants = list(out["r2"])
    for k in (1, 2):
        tabs, rng = fit_all(syn, k), np.random.default_rng([truth_spec(truth)[2] + seed_off, d, k])
        null = {v: [] for v in variants}
        for _ in range(N):
            s = score(P.markov(syn, k, rng, tabs))
            for v in variants:
                null[v].append(s[v])
        out[f"markov{k}"] = {}
        for v in variants:
            z, p = zp(out["r2"][v], null[v])
            out[f"markov{k}"][v] = {"z": z, "p": p, "mean": float(np.mean(null[v])), "sd": float(np.std(null[v])),
                                    "null": null[v]}
    return out


def negative_control(data, V, truth, d, N):
    """Main pipeline only, in the flat format of results/smalldata_nc<truth>.json."""
    r = negative_control_all(data, V, truth, d, N, (P.MAIN,))
    return {"d": d, "N": N, "r2": r["r2"][P.MAIN], "markov1": r["markov1"][P.MAIN], "markov2": r["markov2"][P.MAIN]}


def run_nc(data, V, truth, N, D, allv=False, res=RES, score=None, seed_off=0):
    """Datasets 0..D-1, checkpointed one per dataset; allv = all pipelines -> smalldata_ncv<truth>.json."""
    path = os.path.join(res, f"smalldata_nc{'v' if allv else ''}{truth}.json")
    recs = [r for r in (json.load(open(path)) if os.path.exists(path) else []) if r["N"] == N]
    done, t0 = {r["d"] for r in recs}, time.time()
    for d in range(D):
        if d in done:
            continue
        r = (negative_control_all(data, V, truth, d, N, score=score, seed_off=seed_off) if allv
             else negative_control(data, V, truth, d, N))
        recs.append(r)
        save(path, sorted(recs, key=lambda x: x["d"]))
        if allv:
            print(f"truth {truth} dataset {d}: " + "  ".join(
                f"{v} M1 {r['markov1'][v]['z']:+.1f} M2 {r['markov2'][v]['z']:+.1f}" for v in r["r2"]) +
                f"  {time.time() - t0:.0f}s", flush=True)
        else:
            print(f"truth {truth} dataset {d}: r2 {r['r2']:.4f}  M1 z {r['markov1']['z']:+.1f} p {r['markov1']['p']:.3f}"
                  f"  M2 z {r['markov2']['z']:+.1f} p {r['markov2']['p']:.3f}  {time.time() - t0:.0f}s", flush=True)


HET_TRUTHS = ("1", "2", "3", "4", "rec2", "rec3")


def heterogeneity(data, V, D, truths=HET_TRUTHS, res=RES, seed_off=0):
    """How much do recordings within a year differ? For the real song (section 8.1) and every synthetic
    dataset of every truth: leave-one-recording-out order-2 Witten-Bell cross-entropy (bits per element) and
    the share of held-out order-2 contexts unseen in the other recordings, pooled over years. A stationary
    per-year chain makes recordings more alike than real ones are; a per-recording chain keeps the
    differences. Checkpointed per truth -> results/smalldata_het.json."""
    path = os.path.join(res, "smalldata_het.json")
    out = json.load(open(path)) if os.path.exists(path) else {}
    for t in truths:
        if len(out.get(t, [])) == D:
            continue
        rows, t0 = [], time.time()
        for d in range(D):
            raw = [heldout(recs, 2, V) for recs in synth(data, t, d, seed_off).values()]
            rows.append({"d": d, "ce2": sum(r[0] for r in raw) / sum(r[1] for r in raw),
                         "unseen2": sum(r[2] for r in raw) / sum(r[3] for r in raw)})
        out[t] = rows
        save(path, out)
        print(f"het {t}: ce2 {np.mean([r['ce2'] for r in rows]):.3f}  unseen2 "
              f"{100 * np.mean([r['unseen2'] for r in rows]):.1f}%  {time.time() - t0:.0f}s", flush=True)
    return out


def copying(data, D, n=8, truths=("2", "3", "rec2", "rec3"), res=RES, seed_off=0):
    """Share of each synthetic recording's n-grams that occur verbatim in the real recording it was generated
    for (same index), pooled over years, per dataset -> <res>/smalldata_copy.json."""
    out = {}
    for t in truths:
        out[t] = []
        for d in range(D):
            hit = tot = 0
            for y, syn in synth(data, t, d, seed_off).items():
                for r, s in zip(data[y], syn):
                    src = {r[i:i + n].tobytes() for i in range(len(r) - n + 1)}
                    g = [s[i:i + n].tobytes() for i in range(len(s) - n + 1)]
                    hit += sum(x in src for x in g)
                    tot += len(g)
            out[t].append(hit / tot)
        print(f"copy {t}: {100 * np.mean(out[t]):.1f}% [{100 * min(out[t]):.1f}, {100 * max(out[t]):.1f}]", flush=True)
    save(os.path.join(res, "smalldata_copy.json"), out)
    return out


# ---------------- report ----------------

def _nc_table(L, nc, pick, real, variant, title):
    """Append one negative-control table to L (a row per truth x null, then real song from summary.json for
    `variant`) and return its summary dict. pick(record) -> (synthetic R^2, Markov-1 stats, Markov-2 stats)."""
    L += ["", title, "",
          "| ground truth | null | datasets x N | synthetic 'real' R^2 mean | null R^2 mean | z mean (sd) | z median [min, max] | p median | datasets p <= 0.05 | datasets p >= 0.95 |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    summ = {}
    for truth, recs in nc.items():
        rows = [pick(r) for r in recs]
        for k in (1, 2):
            z = np.array([m[k]["z"] for m in rows])
            p = np.array([m[k]["p"] for m in rows])
            s = {"datasets": len(recs), "N": recs[0]["N"], "r2_mean": float(np.mean([m[0] for m in rows])),
                 "null_mean": float(np.mean([m[k]["mean"] for m in rows])),
                 "z_mean": float(z.mean()), "z_sd": float(z.std()), "z_median": float(np.median(z)),
                 "z_min": float(z.min()), "z_max": float(z.max()), "p_median": float(np.median(p)),
                 "n_p_le_05": int((p <= 0.05).sum()), "n_p_ge_95": int((p >= 0.95).sum()),
                 "z": z.tolist(), "p": p.tolist()}
            summ.setdefault(str(truth), {})[f"markov{k}"] = s
            L.append(f"| {tlabel(truth)} | Markov-{k} | {s['datasets']} x {s['N']} | {s['r2_mean']:.3f} | "
                     f"{s['null_mean']:.3f} | {s['z_mean']:+.1f} ({s['z_sd']:.1f}) | {s['z_median']:+.1f} "
                     f"[{s['z_min']:+.1f}, {s['z_max']:+.1f}] | {s['p_median']:.3f} | {s['n_p_le_05']}/{s['datasets']} "
                     f"| {s['n_p_ge_95']}/{s['datasets']} |")
    for k in (1, 2):
        r = real["nulls"][f"markov{k}"][variant]["r2"]
        L.append(f"| **real song** (README section 4) | Markov-{k} | 1 x {r['n']} | {real['real'][variant]['r2']:.3f} | "
                 f"{r['mean']:.3f} | {r['z']:+.1f} | | {r['p']:.3f} | | |")
    return summ


def report():
    ce = json.load(open(os.path.join(RES, "smalldata_ce.json")))
    real = json.load(open(os.path.join(RES, "summary.json")))
    nc, ncv = {}, {}
    for truth in (1, 2, 3):
        for store, tag in ((nc, ""), (ncv, "v")):
            p = os.path.join(RES, f"smalldata_nc{tag}{truth}.json")
            if os.path.exists(p):
                store[truth] = json.load(open(p))
    # gate: the all-pipeline run must reproduce the main-pipeline numbers of the nc run exactly
    for truth, recs in ncv.items():
        byd = {r["d"]: r for r in nc.get(truth, [])}
        for r in recs:
            o = byd.get(r["d"])
            assert o is None or (o["r2"] == r["r2"][P.MAIN] and all(
                o[m]["null"] == r[m][P.MAIN]["null"] for m in ("markov1", "markov2"))), (truth, r["d"])
    orders = [str(o) for o in ce["orders"]]
    L = ["## Table 1. Held-out cross-entropy, bits per element (interpolated Witten-Bell, leave-one-recording-out)",
         "", "| year | recordings | elements | " + " | ".join(f"order {o}" for o in orders) +
         " | best | unseen order-2 contexts |", "|---|---|---|" + "---|" * len(orders) + "---|---|"]
    for y in ce["ce"]:
        c = ce["ce"][y]
        L.append(f"| {y} | {ce['recordings'][y]} | {ce['elements'][y]} | " +
                 " | ".join(f"**{c[o]:.3f}**" if o == str(ce["best_order"][y]) else f"{c[o]:.3f}" for o in orders) +
                 f" | {ce['best_order'][y]} | {100 * ce['unseen'][y]['2']:.1f}% |")
    cp, bp = ce["ce_pooled"], str(min(ce["ce_pooled"], key=ce["ce_pooled"].get))
    L.append(f"| **pooled** | {sum(ce['recordings'].values())} | {sum(ce['elements'].values())} | " +
             " | ".join(f"**{cp[o]:.3f}**" if o == bp else f"{cp[o]:.3f}" for o in orders) +
             f" | {bp} | {100 * ce['unseen_pooled']['2']:.1f}% |")
    L.append("")
    L.append("Unseen held-out contexts, pooled, by order: " +
             ", ".join(f"order {o}: {100 * v:.1f}%" for o, v in ce["unseen_pooled"].items()))
    summ = _nc_table(L, nc, lambda r: (r["r2"], r["markov1"], r["markov2"]), real, P.MAIN,
                     "## Table 2. Synthetic negative control (main pipeline; z and one-sided p as for real song)")
    summv = {}
    for i, v in enumerate(x for x in P.VARIANTS if x != P.MAIN):
        summv[v] = _nc_table(L, ncv, lambda r, v=v: (r["r2"][v], r["markov1"][v], r["markov2"][v]), real, v,
                             f"## Table 3{'abcd'[i]}. Synthetic negative control, {VLABEL[v]} "
                             "(same synthetic datasets and surrogates as Table 2)")
    ncx = {}
    for t in HET_TRUTHS[3:]:
        p = os.path.join(RES, f"smalldata_ncv{t}.json")
        if os.path.exists(p):
            ncx[t] = json.load(open(p))
    summx = {}
    if ncx:
        allt = {str(t): r for t, r in ncv.items()} | ncx
        for i, v in enumerate(P.VARIANTS):
            summx[v] = _nc_table(L, allt, lambda r, v=v: (r["r2"][v], r["markov1"][v], r["markov2"][v]), real, v,
                                 f"## Table 4{'abcde'[i]}. All ground truths, {VLABEL[v]} "
                                 "(adds an order-4 chain and per-recording order-2/3 chains)")
    hp = os.path.join(RES, "smalldata_het.json")
    het = json.load(open(hp)) if os.path.exists(hp) else {}
    if het:
        L += ["", "## Table 5. Between-recording differences: leave-one-recording-out order-2 cross-entropy "
              "(bits per element) and share of held-out order-2 contexts unseen in the other recordings, pooled over years",
              "", "| data | datasets | cross-entropy mean [min, max] | unseen contexts mean [min, max] |", "|---|---|---|---|",
              f"| **real song** (Table 1) | 1 | {ce['ce_pooled']['2']:.3f} | {100 * ce['unseen_pooled']['2']:.1f}% |"]
        for t, rows in het.items():
            c, u = [r["ce2"] for r in rows], [100 * r["unseen2"] for r in rows]
            L.append(f"| {tlabel(t)} | {len(rows)} | {np.mean(c):.3f} [{min(c):.3f}, {max(c):.3f}] | "
                     f"{np.mean(u):.1f}% [{min(u):.1f}, {max(u):.1f}] |")
    md = "\n".join(L) + "\n"
    with open(os.path.join(RES, "smalldata_tables.md"), "w", encoding="utf-8") as fh:
        fh.write(md)
    out = {"cross_entropy": ce, "negative_control": summ,
           "negative_control_datasets": {t: [{k: v for k, v in r.items() if k not in ("markov1", "markov2")} |
                                             {f"markov{k}": {a: b for a, b in r[f"markov{k}"].items() if a != "null"}
                                              for k in (1, 2)} for r in recs] for t, recs in nc.items()},
           "negative_control_variants": summv, "negative_control_extra": summx, "heterogeneity": het}
    with open(os.path.join(RES, "smalldata.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    sys.stdout.reconfigure(encoding="utf-8")
    print(md)


# ---------------- self-check ----------------

def _selfcheck():
    # Witten-Bell by hand, same toy year as pipeline's self-check, uniform over its 3 element types:
    # P(0 | ()) = 4/9, P(0 | (0,1)) = 31/36; unseen context (2,1) backs off to (1,): 13/18
    recs = [np.array([0, 1, 0, 1]), np.array([0, 2])]
    tabs = wb_fit(recs, 2)
    assert math.isclose(wb_prob(tabs, 3, (), 0), 4 / 9) and math.isclose(wb_prob(tabs, 3, (0, 1), 0), 31 / 36)
    assert math.isclose(wb_prob(tabs, 3, (2, 1), 0), 13 / 18)
    assert math.isclose(P.witten_bell_tables(recs, 2)[2][(0, 1)][1][0], wb_prob(tabs, 3, (0, 1), 0))
    # held-out on a deterministic cycle: exactly log2(3) bits at order 0, near 0 at order 1, no unseen contexts
    cyc = [np.array([0, 1, 2] * 50)] * 2
    b0, n0, _, _ = heldout(cyc, 0, 3)
    b1, n1, u1, c1 = heldout(cyc, 1, 3)
    assert math.isclose(b0 / n0, math.log2(3)) and b1 / n1 < 0.05 and (u1, c1) == (0, 2 * 149)
    # unseen contexts: every order-1 context of each recording is absent from the other -> 4 of 4
    assert heldout([np.array([0, 1, 0, 1]), np.array([2, 2])], 1, 3)[2:] == (4, 4)
    # z / p convention
    assert zp(0.9, [0.8, 0.9, 1.0]) == (0.0, 0.75)
    # negative control on a toy song: synthetic data keeps recording count, lengths and first elements,
    # differs from the toy, is reproducible from its seed, and p agrees with the stored null list
    rng = np.random.default_rng(1)

    def chain(L):  # skewed cycle over 4 symbols (uniform noise never cuts: all TPs equal)
        s = [int(rng.integers(4))]
        for _ in range(L - 1):
            s.append((s[-1] + 1) % 4 if rng.random() < .7 else int(rng.integers(4)))
        return np.array(s, np.int64)
    toy = {"a": [chain(120) for _ in range(3)], "b": [chain(160) for _ in range(2)]}
    nc = negative_control(toy, 4, 1, 0, 7)
    syn = P.markov(toy, 1, np.random.default_rng([1, 0]), fit_all(toy, 1))
    assert [len(r) for r in syn["a"]] == [120] * 3 and all(s[0] == r[0] for s, r in zip(syn["a"], toy["a"]))
    assert any(s.tolist() != r.tolist() for s, r in zip(syn["a"], toy["a"]))
    assert nc["r2"] == r2_main(syn, 4) and not math.isnan(nc["r2"])
    for k in (1, 2):
        m = nc[f"markov{k}"]
        assert len(m["null"]) == 7 and m["p"] == (1 + sum(x >= nc["r2"] for x in m["null"])) / 8
        assert math.isclose(m["z"], (nc["r2"] - m["mean"]) / m["sd"])
    assert negative_control(toy, 4, 2, 0, 3)["markov2"]["p"] <= 1
    # all-pipeline scoring of the same surrogates: main-pipeline entries identical to the flat record, every
    # other pipeline scored on the same N surrogates with finite R^2 (toy long enough that ratio 0.25 always cuts)
    ncv = negative_control_all(toy, 4, 1, 0, 7)
    assert ncv["r2"][P.MAIN] == nc["r2"] and all(ncv[m][P.MAIN] == nc[m] for m in ("markov1", "markov2"))
    assert set(ncv["r2"]) == set(P.VARIANTS) and all(
        len(ncv[m][v]["null"]) == 7 and not np.isnan([ncv["r2"][v]] + ncv[m][v]["null"]).any()
        and 0 < ncv[m][v]["p"] <= 1
        for v in P.VARIANTS for m in ("markov1", "markov2"))
    # table helper: header (5 lines) + one row per truth x null + two real-song rows, stats pulled through pick
    L = []
    real = {"real": {P.MAIN: {"r2": .93}}, "nulls": {f"markov{k}": {P.MAIN: {"r2": {"n": 1, "mean": .9, "z": z, "p": p}}}
                                                      for k, z, p in ((1, 6., .001), (2, -2., .97))}}
    s = _nc_table(L, {1: [nc, nc]}, lambda r: (r["r2"], r["markov1"], r["markov2"]), real, P.MAIN, "t")
    assert len(L) == 5 + 2 + 2 and s["1"]["markov2"]["z_min"] == nc["markov2"]["z"] and s["1"]["markov1"]["datasets"] == 2
    assert L[-1].endswith("| -2.0 | | 0.970 | | |") and L[5].startswith("| order-1 chain | Markov-1 | 2 x 7 |")
    # truths: plain orders regenerate the old seeds; a per-recording truth only uses its own recording's
    # transitions (recording 1 never contains 0 or 1, so its synthetic copy cannot either; a pooled chain can)
    assert all(a.tolist() == b.tolist() for a, b in zip(synth(toy, "1", 0)["a"], syn["a"]))
    assert truth_spec(2) == ("pooled", 2, 2) and truth_spec("rec3") == ("rec", 3, 203) and tlabel("rec2") == "order-2 chain per recording"
    het = {"y": [np.array([0, 1, 2, 0, 1, 2, 0, 1, 2]), np.array([2, 3, 2, 3, 2, 2, 3, 3, 2])]}
    for d in range(5):
        s = synth(het, "rec1", d)["y"]
        assert [len(x) for x in s] == [9, 9] and s[1][0] == 2 and set(s[1].tolist()) <= {2, 3} and set(s[0].tolist()) <= {0, 1, 2}
    assert any(not set(synth(het, "1", d)["y"][1].tolist()) <= {2, 3} for d in range(20))
    r = negative_control_all(toy, 4, "rec2", 0, 3, (P.MAIN,))
    assert len(r["markov2"][P.MAIN]["null"]) == 3 and 0 < r["markov1"][P.MAIN]["p"] <= 1
    print("smalldata selfcheck ok")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        _selfcheck()
        sys.exit()
    print("priority class: 0x%x" % (set_idle() or 0), flush=True)
    data, vocab = P.load(sys.argv[1])
    V, mode = len(vocab), sys.argv[2]
    if mode == "ce":
        t0 = time.time()
        res = cross_entropy(data, V)
        with open(os.path.join(RES, "smalldata_ce.json"), "w") as fh:
            json.dump(res, fh, indent=1)
        for y, c in res["ce"].items():
            print(y, {o: round(v, 3) for o, v in c.items()}, "unseen2 %.1f%%" % (100 * res["unseen"][y][2]))
        print("pooled", {o: round(v, 3) for o, v in res["ce_pooled"].items()},
              "unseen2 %.1f%%" % (100 * res["unseen_pooled"][2]), f"{time.time() - t0:.0f}s")
    elif mode in ("nc", "ncv"):
        assert sys.argv[3] in HET_TRUTHS and (mode == "ncv" or sys.argv[3] in "123"), sys.argv[3]
        run_nc(data, V, sys.argv[3], int(sys.argv[4]) if len(sys.argv) > 4 else 1000,
               int(sys.argv[5]) if len(sys.argv) > 5 else 20, allv=mode == "ncv")
    elif mode == "het":
        heterogeneity(data, V, int(sys.argv[3]) if len(sys.argv) > 3 else 20)
    elif mode == "copy":
        copying(data, int(sys.argv[3]) if len(sys.argv) > 3 else 20)
    elif mode == "report":
        report()
