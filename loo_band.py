"""Leave-one-out band coverage: is each synthetic dataset inside the min-max band of the other 19 of its truth?"""
import json, sys
P = ["fwd2_r50", "fwd2_r25", "fwd2_r75", "fwd3_r50", "bwd2_r50"]
for t in ["1", "2", "3", "4", "rec2", "rec3"]:
    D = json.load(open(f"{sys.argv[1]}/results/smalldata_ncv{t}.json"))
    z = [{p: (d["markov1"][p]["z"], d["markov2"][p]["z"]) for p in P} for d in D]
    allp, single = 0, []
    for i, zi in enumerate(z):
        rest = z[:i] + z[i + 1:]
        ok = {p: all(min(r[p][k] for r in rest) <= zi[p][k] <= max(r[p][k] for r in rest) for k in (0, 1)) for p in P}
        allp += all(ok.values())
        single.append(sum(ok.values()))
    per_p = [sum(1 for i in range(len(z)) if all(min(r[p][k] for r in z[:i] + z[i + 1:]) <= z[i][p][k] <= max(r[p][k] for r in z[:i] + z[i + 1:]) for k in (0, 1))) for p in P]
    print(t, len(z), "all5:", allp, "per pipeline:", per_p)
