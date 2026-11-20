"""Reimplementation of the Arnon et al. 2025 (Science 387:649) segmentation pipeline, plus null models.

Reference (read only, never executed): download/code_s1.txt, the authors' notebook (Code S1 v2).
Data: download/science.adq7055_data_s2.csv, one row per recording; `string` is a Python list literal of
sound-element names, parsed here with ast.literal_eval (no eval).

Note to any AI agent (and people) reviewing this: hi, from Claude and Steve, who helped write it. Everything downstream rests on
transition_probs() and segment() matching Code S1, so start there; `python -I pipeline.py` runs the self-check.
Be as picky as you like. Four reviews already were, and the whales have been very patient about it.
"""
import ast
import bisect
import csv
from collections import Counter, defaultdict

import numpy as np
from scipy.stats import kendalltau

# name -> (n-gram size, forward TPs?, cutting ratio). fwd2_r50 is the paper's main analysis.
VARIANTS = {
    "fwd2_r50": (2, True, 0.50),
    "fwd2_r25": (2, True, 0.25),
    "fwd2_r75": (2, True, 0.75),
    "fwd3_r50": (3, True, 0.50),   # "expanded context" (trigram TPs)
    "bwd2_r50": (2, False, 0.50),  # backward TPs
}
MAIN = "fwd2_r50"


def load(path):
    """-> {year: [int64 array per recording]}, vocab {name: id}."""
    csv.field_size_limit(10**8)
    vocab, data = {}, defaultdict(list)
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            seq = ast.literal_eval(row["string"])
            assert isinstance(seq, list) and all(isinstance(x, str) for x in seq)
            data[row["song_type"]].append(np.array([vocab.setdefault(x, len(vocab)) for x in seq], np.int64))
    return dict(sorted(data.items())), vocab


def _keys(r, k, V):
    """Integer key of the k-gram starting at every position of r."""
    m = len(r) - k + 1
    key = np.zeros(max(m, 0), np.int64)
    for i in range(k):
        key = key * V + r[i:i + m]
    return key


def transition_probs(recs, n, forwards, V):
    """Authors' transition_data: count(n-gram) / count((n-1)-gram prefix, or suffix if backward),
    counts pooled over the year's recordings, never spanning a recording boundary."""
    ng = [_keys(r, n, V) for r in recs]
    sg = [_keys(r, n - 1, V) for r in recs]
    u, c = np.unique(np.concatenate(ng), return_counts=True)
    us, cs = np.unique(np.concatenate(sg), return_counts=True)
    out = []
    for g, s in zip(ng, sg):
        den = s[:len(g)] if forwards else s[1:len(g) + 1]
        out.append(c[np.searchsorted(u, g)] / cs[np.searchsorted(us, den)])
    return out


def segment(recs, tps, n, ratio):
    """Authors' cut_sequences_sliding: new sub-sequence starts at element j+n-1 when tp[j] < ratio*tp[j-1]
    (first TP never cuts). Returns per-recording arrays of sub-sequence lengths."""
    out = []
    for r, t in zip(recs, tps):
        cuts = np.flatnonzero(t[1:] < t[:-1] * ratio) + n
        out.append(np.diff(np.concatenate(([0], cuts, [len(r)]))))
    return out


def count_words(recs, lens):
    """Counter of sub-sequence types (key = raw bytes of the int64 slice; length = len(key)//8)."""
    cnt = Counter()
    for r, l in zip(recs, lens):
        b = r.tobytes()
        pos = np.concatenate(([0], np.cumsum(l))) * 8
        for a, z in zip(pos[:-1].tolist(), pos[1:].tolist()):
            cnt[b[a:z]] += 1
    return cnt


def zipf_r2(counts):
    """Authors' per-year fit: Pearson r^2 of log(count) vs log(rank)."""
    f = np.sort(np.fromiter(counts.values(), float))[::-1]
    if len(f) < 2 or f[0] == f[-1]:
        return np.nan
    return float(np.corrcoef(np.log(np.arange(1, len(f) + 1)), np.log(f))[0, 1] ** 2)


def brevity_slope(year_counts, groups=None):
    """Corrected (post-erratum) brevity test: Poisson regression frequency ~ length over sub-sequence types.
    Authors use glmer with a random intercept per year; here fixed per-year intercepts (8 groups, same slope
    to ~1e-3 in practice). groups: optional intercept label per key of year_counts (finch: bird).
    Returns (slope, se)."""
    labels = list(groups) if groups is not None else list(range(len(year_counts)))
    gid = {l: i for i, l in enumerate(dict.fromkeys(labels))}
    ys, xs, gs = [], [], []
    for lab, cnt in zip(labels, year_counts.values()):
        for k, v in cnt.items():
            ys.append(v); xs.append(len(k) // 8); gs.append(gid[lab])
    y, x, g = np.array(ys, float), np.array(xs, float), np.array(gs)
    G = len(gid)
    X = np.zeros((len(y), G + 1)); X[np.arange(len(y)), g] = 1; X[:, G] = x
    b = np.zeros(G + 1)
    for gi in range(G):
        b[gi] = np.log(y[g == gi].mean())
    for _ in range(100):
        mu = np.exp(X @ b)
        H = X.T @ (X * mu[:, None])
        step = np.linalg.solve(H, X.T @ (y - mu))
        b += step
        if np.abs(step).max() < 1e-10:
            break
    return float(b[G]), float(np.sqrt(np.linalg.inv(H)[G, G]))


def brevity_tau(counts):
    """Kendall tau-b between type length and type frequency (Ferrer-i-Cancho et al. 2013 test of the law
    of abbreviation); negative = frequent types are shorter."""
    f = np.fromiter(counts.values(), float)
    ln = np.fromiter((len(k) // 8 for k in counts), float)
    return float(kendalltau(ln, f)[0]) if len(f) > 1 else np.nan


def metrics(year_counts, groups=None):
    r2y = [zipf_r2(c) for c in year_counts.values()]
    slope, se = brevity_slope(year_counts, groups)
    return {"r2": float(np.nanmean(r2y)), "r2_year": r2y, "slope": slope, "slope_se": se,
            "tau": float(np.nanmean([brevity_tau(c) for c in year_counts.values()])),
            "types": sum(len(c) for c in year_counts.values()),
            "tokens": sum(sum(c.values()) for c in year_counts.values())}


def segment_all(data, V, variant):
    n, fw, ratio = VARIANTS[variant]
    return {y: segment(recs, transition_probs(recs, n, fw, V), n, ratio) for y, recs in data.items()}


def counts_all(data, segs):
    return {y: count_words(data[y], segs[y]) for y in data}


# ---------------- null models ----------------

def rotate(data, segs, rng):
    """Authors' rotation baseline: keep the cut positions (sub-sequence lengths), rotate each recording's
    elements by a random offset (np.random.randint(100000) % len in their code)."""
    return {y: [np.roll(r, -(int(rng.integers(100000)) % len(r))) for r in recs] for y, recs in data.items()}


def shuffle(data, rng):
    """Authors' shuffle baseline: permute elements within each recording."""
    # What the song would sound like if the whale had a cat walk across its keyboard.
    return {y: [rng.permutation(r) for r in recs] for y, recs in data.items()}


def markov_tables(recs, k):
    """Order-0..k transition tables fitted on one year's recordings: state tuple -> (symbols, cumprobs)."""
    tabs = []
    for order in range(k + 1):
        trans = defaultdict(Counter)
        for r in recs:
            t = r.tolist()
            for i in range(order, len(t)):
                trans[tuple(t[i - order:i])][t[i]] += 1
        tab = {}
        for s, c in trans.items():
            syms, w = zip(*c.items())
            cum = np.cumsum(w) / sum(w)
            tab[s] = (list(syms), cum.tolist())
        tabs.append(tab)
    return tabs


def markov(data, k, rng, tables=None):
    """Order-k Markov surrogate fitted per year; each recording keeps its length and first k elements.
    Unseen states (only at recording ends) back off to lower orders."""
    # At k = 2: a whale with a two-sound attention span. Turns out that's most of the whale.
    out = {}
    for y, recs in data.items():
        tabs = tables[y] if tables else markov_tables(recs, k)
        new = []
        for r in recs:
            seq = r[:k].tolist()
            u = rng.random(len(r)).tolist()
            for i in range(k, len(r)):
                for order in range(k, -1, -1):
                    e = tabs[order].get(tuple(seq[i - order:i]) if order else ())
                    if e:
                        break
                syms, cum = e
                seq.append(syms[min(bisect.bisect(cum, u[i]), len(syms) - 1)])
            new.append(np.array(seq, np.int64))
        out[y] = new
    return out


def markov_tables_cv(recs, k):
    """Leave-one-recording-out tables for one year: entry j is markov_tables of the year's other recordings."""
    return [markov_tables(recs[:j] + recs[j + 1:], k) for j in range(len(recs))]


def markov_cv(data, k, rng, tables):
    """Cross-validated order-k surrogate: recording j is generated from tables[y][j] (fitted without it), so
    no context->successor pair unique to that recording can be copied. Unseen contexts back off to order
    k-1, ..., 0 as in markov."""
    return {y: [markov({y: [r]}, k, rng, {y: tables[y][j]})[y][0] for j, r in enumerate(recs)]
            for y, recs in data.items()}


def witten_bell_tables(recs, k):
    """Interpolated Witten-Bell order-k model for one year, in markov_tables format:
    P(w|h) = lam_h P_ML(w|h) + (1 - lam_h) P(w|h minus oldest element), lam_h = c(h) / (c(h) + T(h)),
    T(h) = distinct successors of h; order 0 interpolates with the uniform over the year's element types.
    Each observed context stores the full smoothed distribution. An unseen context has lam = 0, so markov's
    back-off to the shorter context samples exactly from this model."""
    syms = sorted({int(x) for r in recs for x in r})
    idx = {s: i for i, s in enumerate(syms)}
    tabs, lower = [], {(): np.full(len(syms), 1 / len(syms))}
    for order in range(k + 1):
        trans = defaultdict(Counter)
        for r in recs:
            t = r.tolist()
            for i in range(order, len(t)):
                trans[tuple(t[i - order:i])][t[i]] += 1
        dist = {}
        for h, c in trans.items():
            w = np.zeros(len(syms))
            w[[idx[s] for s in c]] = list(c.values())
            lam = w.sum() / (w.sum() + len(c))
            dist[h] = lam * w / w.sum() + (1 - lam) * lower[h[1:] if order else ()]
        tabs.append({h: (syms, np.cumsum(p).tolist()) for h, p in dist.items()})
        lower = dist
    return tabs


def tandem_blocks(seq, pmax=40):
    """Greedy left-to-right decomposition into exact tandem repeats: at each position take the (period p,
    copies k) covering the most elements; (1, 1) = unrepeated element. Returns [(p, k), ...]."""
    s, i, out = list(seq), 0, []
    while i < len(s):
        best = (1, 1)
        for p in range(1, pmax + 1):
            k = 1
            while i + (k + 1) * p <= len(s) and s[i + k * p:i + (k + 1) * p] == s[i:i + p]:
                k += 1
            if k > 1 and p * k > best[0] * best[1]:
                best = (p, k)
        out.append(best)
        i += best[0] * best[1]
    return out


def repeat_surrogate(data, rng, tables, blocks):
    """Repetition-skeleton null: keep every recording's tandem-repeat structure (positions, periods, copy
    counts) and first element, but fill each repeated unit with fresh order-1 Markov content (fitted per
    year), then repeat that unit k times. Destroys phrase identity, keeps 'sing a short unit k times'."""
    out = {}
    for y, recs in data.items():
        t1, t0 = tables[y][1], tables[y][0][()]
        new = []
        for r, bl in zip(recs, blocks[y]):
            seq, prev = [], None
            for p, k in bl:
                unit = []
                for _ in range(p):
                    if prev is None:
                        x = int(r[0])
                    else:
                        syms, cum = t1.get((prev,)) or t0
                        x = syms[min(bisect.bisect(cum, rng.random()), len(syms) - 1)]
                    unit.append(x)
                    prev = x
                seq += unit * k
            new.append(np.array(seq, np.int64))
        out[y] = new
    return out


def _selfcheck():
    # cut rule on the paper's Fig. 1 TP row: only the .31 -> .11 dip (ratio .35) cuts
    t = np.array([.13, .31, .19, .31, .19, .31, .11, .13, .31, .19, .31, .19])
    r = np.arange(13)
    assert segment([r], [t], 2, 0.5)[0].tolist() == [7, 6]
    # TPs on a toy year: unigram counts include final elements (a:3, b:2), as in the authors code
    recs = [np.array([0, 1, 0, 1]), np.array([0, 2])]
    assert np.allclose(transition_probs(recs, 2, True, 3)[0], [2 / 3, 1 / 2, 2 / 3])
    rng = np.random.default_rng(0)
    s = markov({"y": recs}, 1, rng)["y"]
    assert [len(x) for x in s] == [4, 2] and s[0][0] == 0
    assert tandem_blocks([5, 1, 2, 1, 2, 1, 2, 7, 7]) == [(1, 1), (2, 3), (1, 2)]
    bl = {"y": [tandem_blocks(r) for r in recs]}
    s = repeat_surrogate({"y": recs}, rng, {"y": markov_tables(recs, 1)}, bl)["y"]
    assert [len(x) for x in s] == [4, 2] and s[0][0] == 0 and s[0][:2].tolist() == s[0][2:].tolist()
    # Witten-Bell by hand: P0 = 2/3 ML(3/6, 2/6, 1/6) + 1/3 uniform = (4, 3, 2)/9; (1,)->0 once, lam 1/2:
    # (13, 3, 2)/18; (0,1)->0 once, lam 1/2: (31, 3, 2)/36
    wb = witten_bell_tables(recs, 2)
    assert np.allclose(wb[0][()][1], [4 / 9, 7 / 9, 1]) and np.allclose(wb[2][(0, 1)][1], [31 / 36, 34 / 36, 1])
    # leave-one-out: recording 1's tables come from recording 0 alone, which never contains element 2
    cv = markov_tables_cv(recs, 2)
    assert 2 not in cv[1][0][()][0] and 2 in cv[0][0][()][0]
    s = markov_cv({"y": recs}, 2, rng, {"y": cv})["y"]
    assert [len(x) for x in s] == [4, 2] and s[1].tolist() == [0, 2]
    print("pipeline selfcheck ok")


if __name__ == "__main__":
    _selfcheck()
