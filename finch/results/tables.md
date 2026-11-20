## Rank-frequency R² (cell: null mean, z, p(null ≥ real); paper z in brackets)

| null | ratio 0.5 | ratio 0.3 | ratio 0.7 |
|---|---|---|---|
| real R² | 0.889 | 0.751 | 0.899 |
| shuffle (authors) | 0.583, z=16.2, p=0.001 [17.05] | 0.336, z=15.8, p=0.001 [16.32] | 0.817, z=8.9, p=0.001 [9.04] |
| rotate (authors) | 0.710, z=15.5, p=0.001 [15.69] | 0.476, z=13.3, p=0.001 [11.9] | 0.838, z=9.7, p=0.001 [9.661] |
| bigram (authors, per bout) | 0.792, z=6.7, p=0.001 [6.77] | 0.523, z=9.4, p=0.001 [9.22] | 0.881, z=1.8, p=0.028 [1.87] |
| Markov-1 (per recording) | 0.804, z=6.6, p=0.001 | 0.534, z=8.9, p=0.001 | 0.886, z=1.5, p=0.065 |
| Markov-2 | 0.878, z=1.2, p=0.116 | 0.722, z=1.3, p=0.102 | 0.907, z=-1.5, p=0.926 |
| Markov-2, leave-one-bout-out | 0.878, z=1.2, p=0.113 | 0.724, z=1.2, p=0.101 | 0.907, z=-1.4, p=0.904 |
| Markov-2, Witten-Bell | 0.873, z=1.6, p=0.031 | 0.696, z=2.5, p=0.005 | 0.910, z=-2.0, p=0.961 |

## Brevity, ratio 0.5 (p = share of nulls at least as steep/strong as real)

| null | Kendall τ mean [95%] | p(null τ ≤ real) | Poisson slope mean [95%] | p(null ≤ real) | types |
|---|---|---|---|---|---|
| **real** | -0.045 | | -0.0445 (SE 0.0045) | | 1043 |
| shuffle (authors) | -0.339 [-0.361, -0.318] | 1.000 | -0.0434 [-0.0512, -0.0360] | 0.380 | 3275 |
| rotate (authors) | -0.218 [-0.247, -0.190] | 1.000 | -0.0671 [-0.0715, -0.0630] | 1.000 | 2335 |
| bigram (authors, per bout) | -0.317 [-0.344, -0.289] | 1.000 | -0.1264 [-0.1445, -0.1087] | 1.000 | 1911 |
| Markov-1 (per recording) | -0.323 [-0.352, -0.291] | 1.000 | -0.1302 [-0.1498, -0.1139] | 1.000 | 1879 |
| Markov-2 | -0.159 [-0.197, -0.117] | 1.000 | -0.0815 [-0.0960, -0.0693] | 1.000 | 1177 |
| Markov-2, leave-one-bout-out | -0.159 [-0.199, -0.121] | 1.000 | -0.0813 [-0.0959, -0.0690] | 1.000 | 1174 |
| Markov-2, Witten-Bell | -0.179 [-0.219, -0.142] | 1.000 | -0.0866 [-0.1012, -0.0732] | 1.000 | 1288 |

Kendall τ p over all 21 null×ratio cells: min 0.814

## Development, ratio 0.5: mean R² over birds at each recording (cell: null mean, z, p(null ≥ real))

| stage | real R² | bigram (authors, per bout) | Markov-1 (per recording) | Markov-2 | Markov-2, leave-one-bout-out | Markov-2, Witten-Bell |
|---|---|---|---|---|---|---|
| rec 1 | 0.875 | 0.784, z=2.6, p=0.002 | 0.791, z=2.5, p=0.002 | 0.864, z=0.5, p=0.334 | 0.864, z=0.5, p=0.338 | 0.854, z=0.9, p=0.194 |
| rec 2 | 0.903 | 0.818, z=3.5, p=0.001 | 0.831, z=3.4, p=0.001 | 0.902, z=0.0, p=0.524 | 0.903, z=-0.0, p=0.529 | 0.892, z=0.7, p=0.258 |
| rec 3 | 0.869 | 0.783, z=2.5, p=0.001 | 0.799, z=2.3, p=0.003 | 0.867, z=0.1, p=0.522 | 0.867, z=0.1, p=0.510 | 0.869, z=-0.0, p=0.541 |
| rec 4 | 0.899 | 0.770, z=3.3, p=0.001 | 0.789, z=3.3, p=0.001 | 0.875, z=1.0, p=0.165 | 0.877, z=1.0, p=0.184 | 0.872, z=1.2, p=0.099 |
| rec 5 | 0.898 | 0.804, z=3.2, p=0.001 | 0.810, z=3.3, p=0.001 | 0.882, z=0.9, p=0.197 | 0.880, z=1.0, p=0.191 | 0.878, z=1.0, p=0.149 |
| early (rec 1-2) | 0.889 | 0.801, z=4.2, p=0.001 | 0.811, z=3.9, p=0.001 | 0.883, z=0.4, p=0.357 | 0.884, z=0.4, p=0.373 | 0.873, z=1.1, p=0.110 |
| crystallised (rec 4-5) | 0.898 | 0.787, z=4.6, p=0.001 | 0.800, z=4.6, p=0.001 | 0.879, z=1.3, p=0.080 | 0.878, z=1.4, p=0.092 | 0.875, z=1.6, p=0.044 |

## CSN on pooled type frequencies, ratio 0.5

real: α=1.989 xmin=1 ntail=1043 D=0.027 LR R=-4.78 (p=0.000299)
shuffle (authors): α median 3.491 [3.37, 3.61], LR R median -9.31 (100% < 0)
rotate (authors): α median 2.744 [2.70, 2.79], LR R median -2.41 (100% < 0)
bigram (authors, per bout): α median 2.453 [2.26, 2.60], LR R median -1.00 (97% < 0)
Markov-1 (per recording): α median 2.455 [2.27, 2.56], LR R median -1.76 (97% < 0)
Markov-2: α median 2.040 [1.99, 2.09], LR R median -4.62 (100% < 0)
Markov-2, leave-one-bout-out: α median 2.039 [1.99, 2.10], LR R median -4.54 (100% < 0)
Markov-2, Witten-Bell: α median 2.108 [2.06, 2.16], LR R median -3.02 (100% < 0)
