"""Clauset, Shalizi & Newman (2009) discrete power-law fit: MLE alpha, KS-chosen xmin, bootstrap GOF p,
and Vuong likelihood-ratio test vs a discretised lognormal. Applied to type frequencies (counts per
sub-sequence type): a Zipf rank-frequency law with exponent s implies P(f) ~ f^-(1+1/s)."""
import numpy as np
from scipy.optimize import minimize, minimize_scalar
from scipy.special import erfc, log_ndtr, zeta

MIN_TAIL = 10  # CSN set no minimum tail size, but fits on fewer than 10 points are meaningless


def _alpha(x, xmin):
    n, slx = len(x), np.log(x).sum()
    r = minimize_scalar(lambda a: a * slx / n + np.log(zeta(a, xmin)), bounds=(1.0001, 8), method="bounded")
    return r.x


def _ks(x, xmin, a):
    v, c = np.unique(x, return_counts=True)
    emp = np.cumsum(c) / len(x)
    theo = 1 - zeta(a, v + 1) / zeta(a, xmin)
    return float(np.abs(emp - theo).max())


def fit(x):
    """x: positive integer sample. Scan xmin over unique values keeping >= MIN_TAIL tail points."""
    x = np.asarray(x, float)
    best = None
    for xmin in np.unique(x):
        t = x[x >= xmin]
        if len(t) < MIN_TAIL:
            break
        a = _alpha(t, xmin)
        d = _ks(t, xmin, a)
        if best is None or d < best["D"]:
            best = {"alpha": float(a), "xmin": float(xmin), "D": d, "ntail": int(len(t)), "n": int(len(x))}
    return best


def _sample_pl(a, xmin, size, rng):
    grid = np.arange(xmin, xmin + 100000)
    sf = zeta(a, grid) / zeta(a, xmin)            # P(X >= grid)
    u = rng.random(size)
    i = np.searchsorted(-sf, -u, side="right") - 1  # largest grid with sf >= u
    out = grid[np.clip(i, 0, len(grid) - 1)].astype(float)
    far = u < sf[-1]                               # beyond table: continuous approximation (CSN eq. D.6)
    out[far] = np.floor((xmin - 0.5) * (1 - rng.random(far.sum())) ** (-1 / (a - 1)) + 0.5)
    return out


def gof_p(x, f, nsim, rng):
    """Semi-parametric bootstrap p (CSN sec. 4.1). p > 0.1 -> power law plausible."""
    x = np.asarray(x, float)
    body = x[x < f["xmin"]]
    hits = 0
    for _ in range(nsim):
        k = rng.binomial(len(x), f["ntail"] / len(x))
        syn = np.concatenate((_sample_pl(f["alpha"], f["xmin"], k, rng), rng.choice(body, len(x) - k) if len(body) else []))
        fs = fit(syn)
        hits += fs is not None and fs["D"] >= f["D"]
    return hits / nsim


def _lognorm_ll(t, xmin, mu, s):
    """log P(X = t | X >= xmin) for a lognormal discretised on [t-0.5, t+0.5)."""
    a, b = (np.log(t - 0.5) - mu) / s, (np.log(t + 0.5) - mu) / s
    up = a > 0  # use the upper tail where it is the smaller side, for precision
    hi, lo = log_ndtr(np.where(up, -a, b)), log_ndtr(np.where(up, -b, a))
    logp = hi + np.log1p(-np.exp(np.minimum(lo - hi, -1e-300)))
    return logp - log_ndtr(-(np.log(xmin - 0.5) - mu) / s)


def lr_vs_lognormal(x, f):
    """Vuong test on the tail. R > 0 favours power law; p = significance of the sign.
    Works on unique values with weights (count data has few distinct values)."""
    x = np.asarray(x, float)
    t, w = np.unique(x[x >= f["xmin"]], return_counts=True)
    n = w.sum()
    xmin = f["xmin"]  # >= 1 for counts, so ln(xmin - 0.5) is defined
    lt = np.log(t)
    m0 = (w * lt).sum() / n
    s0 = np.sqrt((w * (lt - m0) ** 2).sum() / n) + 0.1
    # mu is floored at -50: as the lognormal approaches a power law, mu runs off to -inf, and the LR is ~0 there anyway
    nll = lambda p: -(w * _lognorm_ll(t, xmin, max(p[0], -50), np.exp(np.clip(p[1], -3, 3)))).sum()
    res = minimize(nll, [m0, np.log(s0)], method="Nelder-Mead", options={"maxiter": 4000, "xatol": 1e-6, "fatol": 1e-9})
    mu, sg = max(res.x[0], -50), float(np.exp(np.clip(res.x[1], -3, 3)))
    d = -f["alpha"] * lt - np.log(zeta(f["alpha"], xmin)) - _lognorm_ll(t, xmin, mu, sg)
    R = float((w * d).sum())
    sd = np.sqrt((w * (d - R / n) ** 2).sum() / n)
    p = float(erfc(abs(R) / (np.sqrt(2 * n) * sd))) if sd > 0 else 1.0
    return {"R": R, "p": p, "mu": float(mu), "sigma": sg}


def analyse(x, nsim=0, rng=None):
    f = fit(x)
    if f is None:
        return None
    f.update({"lr_" + k: v for k, v in lr_vs_lognormal(x, f).items()})
    if nsim:
        f["gof_p"] = gof_p(x, f, nsim, rng)
    return f


if __name__ == "__main__":
    rng = np.random.default_rng(1)
    x = _sample_pl(2.0, 1, 3000, rng)
    f = analyse(x, nsim=50, rng=rng)
    assert abs(f["alpha"] - 2.0) < 0.1 and f["gof_p"] > 0.05, f
    y = np.floor(np.exp(rng.normal(2, 0.6, 3000))) + 1  # lognormal, narrow: should not favour power law
    g = analyse(y)
    assert g["lr_R"] < 0, g
    print("powerlaw selfcheck ok", round(f["alpha"], 3), f["gof_p"], round(g["lr_R"], 1))
