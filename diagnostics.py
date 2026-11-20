"""How much of the real song do the Markov surrogates copy? Conditional entropies of the fitted chains, and
novelty of surrogate n-grams / sub-sequence types relative to the real year. -> results/diagnostics.json
Usage: python -I diagnostics.py <data_s2.csv> [n_surrogates=50]"""
import json
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np

import pipeline as P
from lowprio import set_idle
from run_nulls import NULLS

HERE = os.path.dirname(os.path.abspath(__file__))


def cond_entropy(recs, k):
    """Plug-in H(X_t | previous k elements) in bits, and share of contexts (token-weighted) with one successor."""
    trans = {}
    for r in recs:
        t = r.tolist()
        for i in range(k, len(t)):
            trans.setdefault(tuple(t[i - k:i]), Counter())[t[i]] += 1
    n = sum(sum(c.values()) for c in trans.values())
    h = det = 0.0
    for c in trans.values():
        w = np.array(list(c.values()), float)
        h -= (w * np.log2(w / w.sum())).sum()
        det += w.sum() * (len(w) == 1)
    return h / n, det / n


def ngrams(recs, n):
    return {tuple(r[i:i + n].tolist()) for r in recs for i in range(len(r) - n + 1)}


def main(path, N):
    set_idle()
    data, vocab = P.load(path)
    V = len(vocab)
    tot = sum(len(r) for rs in data.values() for r in rs)
    out = {"entropy_bits": {}, "deterministic_share": {}}
    for k in (0, 1, 2, 3):
        hs = [(cond_entropy(rs, k), sum(len(r) for r in rs)) for rs in data.values()]
        out["entropy_bits"][k] = sum(h * w for (h, _), w in hs) / tot
        out["deterministic_share"][k] = sum(d * w for (_, d), w in hs) / tot
    real_ng = {n: {y: ngrams(rs, n) for y, rs in data.items()} for n in (4, 6, 8)}
    real_types = {y: set(c) for y, c in P.counts_all(data, P.segment_all(data, V, P.MAIN)).items()}
    t1 = {y: P.markov_tables(r, 1) for y, r in data.items()}
    t2 = {y: P.markov_tables(r, 2) for y, r in data.items()}
    tcv = {y: P.markov_tables_cv(r, 2) for y, r in data.items()}
    twb = {y: P.witten_bell_tables(r, 2) for y, r in data.items()}
    blocks = {y: [P.tandem_blocks(r) for r in rs] for y, rs in data.items()}
    gen = {"markov1": lambda g: P.markov(data, 1, g, t1), "markov2": lambda g: P.markov(data, 2, g, t2),
           "repeat": lambda g: P.repeat_surrogate(data, g, t1, blocks), "shuffle": lambda g: P.shuffle(data, g),
           "markov2cv": lambda g: P.markov_cv(data, 2, g, tcv), "markov2wb": lambda g: P.markov(data, 2, g, twb)}
    out["novel_ngram_share"], out["chunk_tokens_seen_in_real"] = {}, {}
    for name, f in gen.items():
        nov = {n: [] for n in (4, 6, 8)}
        seen = []
        for i in range(N):
            s = f(np.random.default_rng([NULLS.index(name), i]))
            for n in nov:
                tot_n = new_n = 0
                for y, rs in s.items():
                    for r in rs:
                        g = [tuple(r[j:j + n].tolist()) for j in range(len(r) - n + 1)]
                        tot_n += len(g)
                        new_n += sum(x not in real_ng[n][y] for x in g)
                nov[n].append(new_n / tot_n)
            cnt = P.counts_all(s, P.segment_all(s, V, P.MAIN))
            seen.append(sum(v for y, c in cnt.items() for k, v in c.items() if k in real_types[y]) /
                        sum(sum(c.values()) for c in cnt.values()))
        out["novel_ngram_share"][name] = {n: float(np.mean(v)) for n, v in nov.items()}
        out["chunk_tokens_seen_in_real"][name] = float(np.mean(seen))
        print(name, out["novel_ngram_share"][name], round(out["chunk_tokens_seen_in_real"][name], 3), flush=True)
    print("H bits by order", {k: round(v, 3) for k, v in out["entropy_bits"].items()},
          "deterministic share", {k: round(v, 3) for k, v in out["deterministic_share"].items()})
    json.dump(out, open(os.path.join(HERE, "results", "diagnostics.json"), "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 50)
