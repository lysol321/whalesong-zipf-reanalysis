# Speech sample SB: CHILDES UCI_Brent_Syl syllables in the whale layout (1595 syllable types)

## Nulls: R² (null mean, z, p(null ≥ real))

| null | ratio 0.5 (main) | ratio 0.25 | ratio 0.75 | trigram TPs | backward TPs |
|---|---|---|---|---|---|
| real | 0.822 | 0.732 | 0.864 | 0.755 | 0.817 |
| shuffle (N=1000) | 0.421, z +39.8, p 0.001 | 0.236, z +32.5, p 0.001 | 0.523, z +47.2, p 0.001 | 0.170, z +30.0, p 0.001 | 0.444, z +28.9, p 0.001 |
| rotate (N=1000) | 0.661, z +19.9, p 0.001 | 0.478, z +17.0, p 0.001 | 0.750, z +21.3, p 0.001 | 0.410, z +17.5, p 0.001 | 0.636, z +21.9, p 0.001 |
| markov1 (N=1000) | 0.867, z -10.4, p 1.000 | 0.718, z +1.2, p 0.108 | 0.918, z -24.3, p 1.000 | 0.742, z +1.4, p 0.057 | 0.833, z -2.9, p 0.996 |
| markov2 (N=1000) | 0.929, z -57.1, p 1.000 | 0.865, z -19.2, p 1.000 | 0.944, z -51.9, p 1.000 | 0.861, z -14.2, p 1.000 | 0.914, z -38.7, p 1.000 |
| repeat (N=1000) | 0.862, z -8.2, p 1.000 | 0.717, z +1.2, p 0.107 | 0.913, z -19.6, p 1.000 | 0.741, z +1.5, p 0.063 | 0.832, z -2.5, p 0.993 |
| markov2cv (N=1000) | 0.930, z -53.5, p 1.000 | 0.866, z -19.2, p 1.000 | 0.944, z -49.7, p 1.000 | 0.863, z -15.2, p 1.000 | 0.915, z -38.8, p 1.000 |
| markov2wb (N=1000) | 0.816, z +0.9, p 0.202 | 0.681, z +4.4, p 0.001 | 0.872, z -1.8, p 0.960 | 0.700, z +4.8, p 0.001 | 0.797, z +2.7, p 0.001 |

## Brevity, main pipeline (z and p(null at least as strong as real))

| null | Kendall τ null mean | z | p | Poisson slope null mean | z | p |
|---|---|---|---|---|---|---|
| real | -0.291 | | | -0.365 | | |
| shuffle | -0.253 | -7.5 | 0.001 | -0.162 | -47.3 | 0.001 |
| rotate | -0.260 | -4.7 | 0.001 | -0.156 | -83.2 | 0.001 |
| markov1 | -0.355 | +7.9 | 1.000 | -0.397 | +3.9 | 1.000 |
| markov2 | -0.254 | -3.4 | 0.001 | -0.296 | -2.0 | 0.001 |
| repeat | -0.354 | +8.3 | 1.000 | -0.354 | -1.2 | 0.122 |
| markov2cv | -0.251 | -3.6 | 0.001 | -0.291 | -2.1 | 0.001 |
| markov2wb | -0.315 | +3.1 | 1.000 | -0.346 | -2.2 | 0.014 |

## Calibration bands (Markov-1 / Markov-2 z, [min, max] over fake datasets)

| pipeline | real | order-1 chain | order-2 chain | order-3 chain | order-4 chain | order-2 chain per recording | order-3 chain per recording |
|---|---|---|---|---|---|---|---|
| ratio 0.5 (main) | -10.4 / -57.1 | [-10.2, -3.9] / [-28.9, -16.7] | [+7.6, +10.7] / [-0.9, +1.7] | [+8.0, +10.2] / [-0.6, +1.3] | [+7.0, +10.9] / [-3.0, +0.8] | [+8.0, +11.1] / [-0.7, +1.8] | [+8.7, +10.2] / [-1.0, +0.6] |
| ratio 0.25 | +1.2 / -19.2 | [-3.8, -0.0] / [-14.2, -6.8] | [+9.3, +11.6] / [-4.6, -2.4] | [+10.8, +13.6] / [-0.3, +1.5] | [+11.4, +13.6] / [-0.0, +2.0] | [+10.3, +13.2] / [-2.4, +0.3] | [+10.4, +13.4] / [-1.0, +1.6] |
| ratio 0.75 | -24.3 / -51.9 | [-14.3, -7.5] / [-19.6, -11.2] | [+3.3, +7.7] / [+2.4, +4.1] | [+3.1, +6.0] / [+1.7, +3.3] | [+2.1, +6.7] / [+0.3, +3.1] | [+3.6, +6.7] / [+2.2, +4.0] | [+2.9, +6.9] / [+0.3, +2.4] |
| trigram TPs | +1.4 / -14.2 | [-7.3, -3.4] / [-10.7, -5.7] | [+6.7, +9.7] / [-6.7, -3.2] | [+11.3, +13.8] / [-0.2, +3.4] | [+11.7, +14.7] / [+0.4, +3.2] | [+10.3, +12.6] / [-1.1, +1.2] | [+11.3, +14.0] / [+1.2, +3.0] |
| backward TPs | -2.9 / -38.7 | [-7.4, -4.3] / [-26.5, -18.6] | [+9.5, +11.8] / [-2.0, +0.3] | [+9.7, +11.9] / [-2.0, +0.3] | [+8.8, +11.9] / [-3.6, -0.0] | [+10.1, +11.9] / [-1.0, +0.8] | [+9.1, +12.4] / [-3.1, -0.3] |

SD distance of real song's z from each truth's mean z (Markov-1 / Markov-2):

| pipeline | order-1 chain | order-2 chain | order-3 chain | order-4 chain | order-2 chain per recording | order-3 chain per recording |
|---|---|---|---|---|---|---|
| ratio 0.5 (main) | -1.6 / -11.4 | -24.6 / -89.8 | -29.8 / -112.0 | -21.5 / -53.1 | -29.7 / -103.6 | -45.1 / -122.1 |
| ratio 0.25 | +3.2 / -6.1 | -15.6 / -28.1 | -16.2 / -41.6 | -17.9 / -38.0 | -14.5 / -30.5 | -16.9 / -34.5 |
| ratio 0.75 | -6.6 / -17.3 | -32.0 / -132.1 | -34.7 / -128.5 | -21.0 / -68.9 | -35.9 / -117.5 | -28.0 / -108.8 |
| trigram TPs | +8.2 / -4.9 | -8.0 / -10.3 | -16.6 / -20.7 | -15.2 / -21.3 | -16.7 / -26.3 | -13.1 / -31.1 |
| backward TPs | +3.2 / -8.2 | -25.9 / -58.1 | -21.6 / -52.2 | -17.2 / -47.7 | -27.3 / -81.1 | -16.8 / -59.8 |

### Calibration detail, ratio 0.5 (main)

| ground truth | null | datasets x N | synthetic 'real' R^2 mean | null R^2 mean | z mean (sd) | z median [min, max] | p median | datasets p <= 0.05 | datasets p >= 0.95 |
|---|---|---|---|---|---|---|---|---|---|
| order-1 chain | Markov-1 | 20 x 1000 | 0.866 | 0.895 | -8.0 (1.5) | -8.4 [-10.2, -3.9] | 1.000 | 0/20 | 20/20 |
| order-1 chain | Markov-2 | 20 x 1000 | 0.866 | 0.924 | -24.7 (2.8) | -24.7 [-28.9, -16.7] | 1.000 | 0/20 | 20/20 |
| order-2 chain | Markov-1 | 20 x 1000 | 0.930 | 0.896 | +9.3 (0.8) | +9.4 [+7.6, +10.7] | 0.001 | 20/20 | 0/20 |
| order-2 chain | Markov-2 | 20 x 1000 | 0.930 | 0.928 | +0.5 (0.6) | +0.5 [-0.9, +1.7] | 0.325 | 1/20 | 0/20 |
| order-3 chain | Markov-1 | 20 x 1000 | 0.930 | 0.896 | +9.2 (0.7) | +9.0 [+8.0, +10.2] | 0.001 | 20/20 | 0/20 |
| order-3 chain | Markov-2 | 20 x 1000 | 0.930 | 0.929 | +0.4 (0.5) | +0.2 [-0.6, +1.3] | 0.431 | 0/20 | 0/20 |
| order-4 chain | Markov-1 | 20 x 1000 | 0.929 | 0.895 | +9.0 (0.9) | +9.0 [+7.0, +10.9] | 0.001 | 20/20 | 0/20 |
| order-4 chain | Markov-2 | 20 x 1000 | 0.929 | 0.930 | -0.5 (1.1) | -0.1 [-3.0, +0.8] | 0.557 | 0/20 | 2/20 |
| order-2 chain per recording | Markov-1 | 20 x 1000 | 0.932 | 0.897 | +9.5 (0.7) | +9.7 [+8.0, +11.1] | 0.001 | 20/20 | 0/20 |
| order-2 chain per recording | Markov-2 | 20 x 1000 | 0.932 | 0.929 | +0.9 (0.6) | +1.0 [-0.7, +1.8] | 0.148 | 3/20 | 0/20 |
| order-3 chain per recording | Markov-1 | 20 x 1000 | 0.930 | 0.894 | +9.5 (0.4) | +9.4 [+8.7, +10.2] | 0.001 | 20/20 | 0/20 |
| order-3 chain per recording | Markov-2 | 20 x 1000 | 0.930 | 0.931 | -0.2 (0.5) | -0.2 [-1.0, +0.6] | 0.584 | 0/20 | 0/20 |
| **real song** (README section 4) | Markov-1 | 1 x 1000 | 0.822 | 0.867 | -10.4 | | 1.000 | | |
| **real song** (README section 4) | Markov-2 | 1 x 1000 | 0.822 | 0.929 | -57.1 | | 1.000 | | |

### Calibration detail, ratio 0.25

| ground truth | null | datasets x N | synthetic 'real' R^2 mean | null R^2 mean | z mean (sd) | z median [min, max] | p median | datasets p <= 0.05 | datasets p >= 0.95 |
|---|---|---|---|---|---|---|---|---|---|
| order-1 chain | Markov-1 | 20 x 1000 | 0.720 | 0.739 | -1.6 (0.9) | -1.2 [-3.8, -0.0] | 0.893 | 0/20 | 7/20 |
| order-1 chain | Markov-2 | 20 x 1000 | 0.720 | 0.818 | -9.9 (1.5) | -9.8 [-14.2, -6.8] | 1.000 | 0/20 | 20/20 |
| order-2 chain | Markov-1 | 20 x 1000 | 0.868 | 0.742 | +10.4 (0.6) | +10.5 [+9.3, +11.6] | 0.001 | 20/20 | 0/20 |
| order-2 chain | Markov-2 | 20 x 1000 | 0.868 | 0.890 | -3.5 (0.6) | -3.6 [-4.6, -2.4] | 0.996 | 0/20 | 20/20 |
| order-3 chain | Markov-1 | 20 x 1000 | 0.893 | 0.739 | +12.5 (0.7) | +12.4 [+10.8, +13.6] | 0.001 | 20/20 | 0/20 |
| order-3 chain | Markov-2 | 20 x 1000 | 0.893 | 0.888 | +0.7 (0.5) | +0.6 [-0.3, +1.5] | 0.286 | 1/20 | 0/20 |
| order-4 chain | Markov-1 | 20 x 1000 | 0.892 | 0.739 | +12.4 (0.6) | +12.3 [+11.4, +13.6] | 0.001 | 20/20 | 0/20 |
| order-4 chain | Markov-2 | 20 x 1000 | 0.892 | 0.887 | +0.7 (0.5) | +0.8 [-0.0, +2.0] | 0.219 | 1/20 | 0/20 |
| order-2 chain per recording | Markov-1 | 20 x 1000 | 0.883 | 0.740 | +11.5 (0.7) | +11.6 [+10.3, +13.2] | 0.001 | 20/20 | 0/20 |
| order-2 chain per recording | Markov-2 | 20 x 1000 | 0.883 | 0.888 | -0.6 (0.6) | -0.6 [-2.4, +0.3] | 0.741 | 0/20 | 1/20 |
| order-3 chain per recording | Markov-1 | 20 x 1000 | 0.891 | 0.735 | +12.3 (0.7) | +12.3 [+10.4, +13.4] | 0.001 | 20/20 | 0/20 |
| order-3 chain per recording | Markov-2 | 20 x 1000 | 0.891 | 0.886 | +0.6 (0.6) | +0.6 [-1.0, +1.6] | 0.281 | 1/20 | 0/20 |
| **real song** (README section 4) | Markov-1 | 1 x 1000 | 0.732 | 0.718 | +1.2 | | 0.108 | | |
| **real song** (README section 4) | Markov-2 | 1 x 1000 | 0.732 | 0.865 | -19.2 | | 1.000 | | |

### Calibration detail, ratio 0.75

| ground truth | null | datasets x N | synthetic 'real' R^2 mean | null R^2 mean | z mean (sd) | z median [min, max] | p median | datasets p <= 0.05 | datasets p >= 0.95 |
|---|---|---|---|---|---|---|---|---|---|
| order-1 chain | Markov-1 | 20 x 1000 | 0.917 | 0.935 | -12.1 (1.8) | -12.8 [-14.3, -7.5] | 1.000 | 0/20 | 20/20 |
| order-1 chain | Markov-2 | 20 x 1000 | 0.917 | 0.943 | -14.9 (2.1) | -14.9 [-19.6, -11.2] | 1.000 | 0/20 | 20/20 |
| order-2 chain | Markov-1 | 20 x 1000 | 0.944 | 0.936 | +5.5 (0.9) | +5.4 [+3.3, +7.7] | 0.001 | 20/20 | 0/20 |
| order-2 chain | Markov-2 | 20 x 1000 | 0.944 | 0.934 | +3.3 (0.4) | +3.3 [+2.4, +4.1] | 0.001 | 20/20 | 0/20 |
| order-3 chain | Markov-1 | 20 x 1000 | 0.943 | 0.936 | +4.9 (0.8) | +4.9 [+3.1, +6.0] | 0.001 | 20/20 | 0/20 |
| order-3 chain | Markov-2 | 20 x 1000 | 0.943 | 0.935 | +2.6 (0.4) | +2.7 [+1.7, +3.3] | 0.003 | 20/20 | 0/20 |
| order-4 chain | Markov-1 | 20 x 1000 | 0.942 | 0.935 | +4.4 (1.4) | +4.4 [+2.1, +6.7] | 0.001 | 20/20 | 0/20 |
| order-4 chain | Markov-2 | 20 x 1000 | 0.942 | 0.936 | +2.1 (0.8) | +2.2 [+0.3, +3.1] | 0.007 | 15/20 | 0/20 |
| order-2 chain per recording | Markov-1 | 20 x 1000 | 0.945 | 0.936 | +5.4 (0.8) | +5.7 [+3.6, +6.7] | 0.001 | 20/20 | 0/20 |
| order-2 chain per recording | Markov-2 | 20 x 1000 | 0.945 | 0.935 | +3.0 (0.5) | +3.0 [+2.2, +4.0] | 0.001 | 20/20 | 0/20 |
| order-3 chain per recording | Markov-1 | 20 x 1000 | 0.944 | 0.936 | +5.2 (1.1) | +5.2 [+2.9, +6.9] | 0.001 | 20/20 | 0/20 |
| order-3 chain per recording | Markov-2 | 20 x 1000 | 0.944 | 0.939 | +1.7 (0.5) | +1.7 [+0.3, +2.4] | 0.031 | 14/20 | 0/20 |
| **real song** (README section 4) | Markov-1 | 1 x 1000 | 0.864 | 0.918 | -24.3 | | 1.000 | | |
| **real song** (README section 4) | Markov-2 | 1 x 1000 | 0.864 | 0.944 | -51.9 | | 1.000 | | |

### Calibration detail, trigram TPs

| ground truth | null | datasets x N | synthetic 'real' R^2 mean | null R^2 mean | z mean (sd) | z median [min, max] | p median | datasets p <= 0.05 | datasets p >= 0.95 |
|---|---|---|---|---|---|---|---|---|---|
| order-1 chain | Markov-1 | 20 x 1000 | 0.744 | 0.794 | -6.1 (0.9) | -6.3 [-7.3, -3.4] | 1.000 | 0/20 | 20/20 |
| order-1 chain | Markov-2 | 20 x 1000 | 0.744 | 0.817 | -8.5 (1.2) | -8.4 [-10.7, -5.7] | 1.000 | 0/20 | 20/20 |
| order-2 chain | Markov-1 | 20 x 1000 | 0.864 | 0.796 | +8.3 (0.9) | +8.4 [+6.7, +9.7] | 0.001 | 20/20 | 0/20 |
| order-2 chain | Markov-2 | 20 x 1000 | 0.864 | 0.893 | -4.6 (0.9) | -4.4 [-6.7, -3.2] | 1.000 | 0/20 | 20/20 |
| order-3 chain | Markov-1 | 20 x 1000 | 0.906 | 0.801 | +13.1 (0.7) | +13.3 [+11.3, +13.8] | 0.001 | 20/20 | 0/20 |
| order-3 chain | Markov-2 | 20 x 1000 | 0.906 | 0.893 | +2.1 (0.8) | +2.2 [-0.2, +3.4] | 0.006 | 15/20 | 0/20 |
| order-4 chain | Markov-1 | 20 x 1000 | 0.908 | 0.800 | +13.4 (0.8) | +13.2 [+11.7, +14.7] | 0.001 | 20/20 | 0/20 |
| order-4 chain | Markov-2 | 20 x 1000 | 0.908 | 0.893 | +2.4 (0.8) | +2.6 [+0.4, +3.2] | 0.002 | 18/20 | 0/20 |
| order-2 chain per recording | Markov-1 | 20 x 1000 | 0.893 | 0.801 | +11.5 (0.6) | +11.4 [+10.3, +12.6] | 0.001 | 20/20 | 0/20 |
| order-2 chain per recording | Markov-2 | 20 x 1000 | 0.893 | 0.893 | +0.0 (0.5) | -0.0 [-1.1, +1.2] | 0.531 | 0/20 | 0/20 |
| order-3 chain per recording | Markov-1 | 20 x 1000 | 0.902 | 0.800 | +12.4 (0.8) | +12.2 [+11.3, +14.0] | 0.001 | 20/20 | 0/20 |
| order-3 chain per recording | Markov-2 | 20 x 1000 | 0.902 | 0.887 | +2.2 (0.5) | +2.1 [+1.2, +3.0] | 0.006 | 19/20 | 0/20 |
| **real song** (README section 4) | Markov-1 | 1 x 1000 | 0.755 | 0.742 | +1.4 | | 0.057 | | |
| **real song** (README section 4) | Markov-2 | 1 x 1000 | 0.755 | 0.861 | -14.2 | | 1.000 | | |

### Calibration detail, backward TPs

| ground truth | null | datasets x N | synthetic 'real' R^2 mean | null R^2 mean | z mean (sd) | z median [min, max] | p median | datasets p <= 0.05 | datasets p >= 0.95 |
|---|---|---|---|---|---|---|---|---|---|
| order-1 chain | Markov-1 | 20 x 1000 | 0.833 | 0.861 | -5.6 (0.8) | -5.6 [-7.4, -4.3] | 1.000 | 0/20 | 20/20 |
| order-1 chain | Markov-2 | 20 x 1000 | 0.833 | 0.902 | -23.0 (1.9) | -22.9 [-26.5, -18.6] | 1.000 | 0/20 | 20/20 |
| order-2 chain | Markov-1 | 20 x 1000 | 0.916 | 0.864 | +10.6 (0.5) | +10.7 [+9.5, +11.8] | 0.001 | 20/20 | 0/20 |
| order-2 chain | Markov-2 | 20 x 1000 | 0.916 | 0.918 | -0.7 (0.7) | -0.8 [-2.0, +0.3] | 0.802 | 0/20 | 2/20 |
| order-3 chain | Markov-1 | 20 x 1000 | 0.917 | 0.864 | +10.7 (0.6) | +10.7 [+9.7, +11.9] | 0.001 | 20/20 | 0/20 |
| order-3 chain | Markov-2 | 20 x 1000 | 0.917 | 0.919 | -0.8 (0.7) | -0.7 [-2.0, +0.3] | 0.767 | 0/20 | 3/20 |
| order-4 chain | Markov-1 | 20 x 1000 | 0.916 | 0.865 | +10.1 (0.8) | +10.2 [+8.8, +11.9] | 0.001 | 20/20 | 0/20 |
| order-4 chain | Markov-2 | 20 x 1000 | 0.916 | 0.921 | -1.7 (0.8) | -1.7 [-3.6, -0.0] | 0.949 | 0/20 | 10/20 |
| order-2 chain per recording | Markov-1 | 20 x 1000 | 0.919 | 0.865 | +11.0 (0.5) | +11.1 [+10.1, +11.9] | 0.001 | 20/20 | 0/20 |
| order-2 chain per recording | Markov-2 | 20 x 1000 | 0.919 | 0.919 | -0.2 (0.5) | -0.2 [-1.0, +0.8] | 0.598 | 0/20 | 0/20 |
| order-3 chain per recording | Markov-1 | 20 x 1000 | 0.919 | 0.867 | +10.6 (0.8) | +10.7 [+9.1, +12.4] | 0.001 | 20/20 | 0/20 |
| order-3 chain per recording | Markov-2 | 20 x 1000 | 0.919 | 0.922 | -1.2 (0.6) | -1.0 [-3.1, -0.3] | 0.837 | 0/20 | 4/20 |
| **real song** (README section 4) | Markov-1 | 1 x 1000 | 0.817 | 0.833 | -2.9 | | 0.996 | | |
| **real song** (README section 4) | Markov-2 | 1 x 1000 | 0.817 | 0.914 | -38.7 | | 1.000 | | |

## Held-out order choice

pooled bits per element by order: 0: 8.443, 1: 7.075, 2: 7.168, 3: 7.258, 4: 7.297; best order per group: [1, 1, 1, 1, 1, 1, 1, 1]; unseen order-2 contexts 50.0%

## Recording differences

- order-1 chain: 4.943–5.015 bits, 18.8–19.2% unseen
- order-2 chain: 3.547–4.024 bits, 19.4–23.3% unseen
- order-3 chain: 3.762–4.174 bits, 21.1–25.2% unseen
- order-4 chain: 3.849–4.593 bits, 22.0–28.0% unseen
- order-2 chain per recording: 7.720–7.959 bits, 55.7–58.1% unseen
- order-3 chain per recording: 7.723–8.059 bits, 55.6–59.0% unseen

## Copying

order-2 chain 2.6%, order-3 chain 11.0%, order-2 chain per recording 35.6%, order-3 chain per recording 72.2%

## TP cuts vs word boundaries

- ratio 0.5 (main): precision 0.965 (chance 0.821), recall 0.460, cuts 17866
- ratio 0.25: precision 0.976 (chance 0.821), recall 0.341, cuts 13093
- ratio 0.75: precision 0.957 (chance 0.821), recall 0.533, cuts 20869
- trigram TPs: precision 0.983 (chance 0.821), recall 0.304, cuts 11608
- backward TPs: precision 0.941 (chance 0.821), recall 0.423, cuts 16844
