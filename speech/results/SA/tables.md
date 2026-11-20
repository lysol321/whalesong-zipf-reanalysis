# Speech sample SA: CHILDES UCI_Brent_Syl syllables in the whale layout (1616 syllable types)

## Nulls: R² (null mean, z, p(null ≥ real))

| null | ratio 0.5 (main) | ratio 0.25 | ratio 0.75 | trigram TPs | backward TPs |
|---|---|---|---|---|---|
| real | 0.835 | 0.735 | 0.876 | 0.753 | 0.827 |
| shuffle (N=1000) | 0.420, z +42.7, p 0.001 | 0.250, z +33.6, p 0.001 | 0.523, z +45.6, p 0.001 | 0.209, z +24.7, p 0.001 | 0.468, z +28.7, p 0.001 |
| rotate (N=1000) | 0.665, z +21.9, p 0.001 | 0.492, z +18.0, p 0.001 | 0.752, z +22.6, p 0.001 | 0.433, z +19.1, p 0.001 | 0.635, z +22.1, p 0.001 |
| markov1 (N=1000) | 0.868, z -7.8, p 1.000 | 0.727, z +0.7, p 0.236 | 0.918, z -19.3, p 1.000 | 0.747, z +0.6, p 0.278 | 0.835, z -1.5, p 0.920 |
| markov2 (N=1000) | 0.931, z -47.3, p 1.000 | 0.873, z -22.8, p 1.000 | 0.945, z -42.7, p 1.000 | 0.864, z -15.6, p 1.000 | 0.914, z -30.5, p 1.000 |
| repeat (N=1000) | 0.860, z -5.2, p 1.000 | 0.724, z +0.9, p 0.183 | 0.911, z -14.1, p 1.000 | 0.744, z +1.0, p 0.160 | 0.831, z -0.7, p 0.778 |
| markov2cv (N=1000) | 0.931, z -47.9, p 1.000 | 0.875, z -23.1, p 1.000 | 0.945, z -40.3, p 1.000 | 0.869, z -18.5, p 1.000 | 0.916, z -31.9, p 1.000 |
| markov2wb (N=1000) | 0.818, z +3.0, p 0.002 | 0.686, z +4.5, p 0.001 | 0.873, z +0.7, p 0.249 | 0.700, z +4.6, p 0.001 | 0.802, z +3.4, p 0.001 |

## Brevity, main pipeline (z and p(null at least as strong as real))

| null | Kendall τ null mean | z | p | Poisson slope null mean | z | p |
|---|---|---|---|---|---|---|
| real | -0.318 | | | -0.367 | | |
| shuffle | -0.251 | -13.8 | 0.001 | -0.163 | -47.1 | 0.001 |
| rotate | -0.257 | -10.0 | 0.001 | -0.152 | -82.6 | 0.001 |
| markov1 | -0.365 | +6.2 | 1.000 | -0.396 | +3.4 | 1.000 |
| markov2 | -0.268 | -4.5 | 0.001 | -0.328 | -3.6 | 0.001 |
| repeat | -0.365 | +6.0 | 1.000 | -0.348 | -2.3 | 0.011 |
| markov2cv | -0.265 | -4.7 | 0.001 | -0.325 | -4.1 | 0.001 |
| markov2wb | -0.322 | +0.6 | 0.716 | -0.333 | -3.2 | 0.002 |

## Calibration bands (Markov-1 / Markov-2 z, [min, max] over fake datasets)

| pipeline | real | order-1 chain | order-2 chain | order-3 chain | order-4 chain | order-2 chain per recording | order-3 chain per recording |
|---|---|---|---|---|---|---|---|
| ratio 0.5 (main) | -7.8 / -47.3 | [-10.1, -7.0] / [-32.4, -9.6] | [+8.9, +10.9] / [-0.8, +0.8] | [+9.1, +11.2] / [-0.7, +1.3] | [+6.8, +11.5] / [-1.6, +0.8] | [+6.8, +11.4] / [-0.5, +1.8] | [+6.2, +10.2] / [-1.7, +0.6] |
| ratio 0.25 | +0.7 / -22.8 | [-3.8, -1.1] / [-14.8, -5.9] | [+10.1, +12.7] / [-5.7, -2.1] | [+12.2, +14.5] / [-0.1, +1.7] | [+11.9, +14.4] / [-0.6, +1.7] | [+10.6, +13.3] / [-3.3, +0.3] | [+10.6, +13.7] / [-1.5, +1.9] |
| ratio 0.75 | -19.3 / -42.7 | [-13.0, -9.6] / [-18.3, -10.9] | [+4.1, +6.6] / [+2.3, +3.9] | [+2.9, +6.0] / [+1.7, +3.2] | [+1.7, +6.5] / [+1.1, +2.8] | [+2.5, +7.7] / [+1.5, +3.2] | [+2.1, +6.7] / [+0.1, +3.1] |
| trigram TPs | +0.6 / -15.6 | [-8.1, -5.2] / [-11.3, -4.8] | [+6.5, +10.0] / [-7.0, -1.9] | [+12.0, +14.7] / [+1.3, +2.9] | [+11.2, +14.7] / [+0.9, +3.3] | [+6.7, +13.4] / [-2.4, +1.0] | [+8.8, +13.1] / [+1.1, +2.6] |
| backward TPs | -1.5 / -30.5 | [-7.1, -3.6] / [-24.7, -9.3] | [+8.2, +11.1] / [-3.2, -0.8] | [+9.5, +11.3] / [-2.4, +0.8] | [+7.4, +11.3] / [-4.9, -0.2] | [+6.0, +12.2] / [-3.0, +0.4] | [+6.6, +11.2] / [-3.3, -0.5] |

SD distance of real song's z from each truth's mean z (Markov-1 / Markov-2):

| pipeline | order-1 chain | order-2 chain | order-3 chain | order-4 chain | order-2 chain per recording | order-3 chain per recording |
|---|---|---|---|---|---|---|
| ratio 0.5 (main) | +0.5 / -5.0 | -33.0 / -95.6 | -34.3 / -78.7 | -18.1 / -78.2 | -11.7 / -77.2 | -15.3 / -74.9 |
| ratio 0.25 | +4.3 / -6.4 | -13.7 / -20.8 | -21.4 / -50.5 | -20.8 / -36.2 | -15.4 / -25.4 | -12.9 / -29.6 |
| ratio 0.75 | -8.6 / -16.1 | -33.7 / -123.0 | -24.9 / -92.4 | -19.6 / -113.8 | -19.2 / -97.8 | -19.2 / -69.5 |
| trigram TPs | +8.1 / -4.6 | -7.6 / -9.0 | -18.9 / -44.6 | -14.6 / -26.2 | -5.3 / -20.5 | -10.1 / -41.1 |
| backward TPs | +4.7 / -2.9 | -19.0 / -47.9 | -24.4 / -41.6 | -13.0 / -24.0 | -6.3 / -33.5 | -7.3 / -34.5 |

### Calibration detail, ratio 0.5 (main)

| ground truth | null | datasets x N | synthetic 'real' R^2 mean | null R^2 mean | z mean (sd) | z median [min, max] | p median | datasets p <= 0.05 | datasets p >= 0.95 |
|---|---|---|---|---|---|---|---|---|---|
| order-1 chain | Markov-1 | 20 x 1000 | 0.868 | 0.896 | -8.2 (0.9) | -8.0 [-10.1, -7.0] | 1.000 | 0/20 | 20/20 |
| order-1 chain | Markov-2 | 20 x 1000 | 0.868 | 0.925 | -26.2 (4.2) | -26.7 [-32.4, -9.6] | 1.000 | 0/20 | 20/20 |
| order-2 chain | Markov-1 | 20 x 1000 | 0.931 | 0.897 | +9.8 (0.5) | +9.8 [+8.9, +10.9] | 0.001 | 20/20 | 0/20 |
| order-2 chain | Markov-2 | 20 x 1000 | 0.931 | 0.931 | +0.2 (0.5) | +0.3 [-0.8, +0.8] | 0.414 | 0/20 | 0/20 |
| order-3 chain | Markov-1 | 20 x 1000 | 0.932 | 0.896 | +10.0 (0.5) | +10.0 [+9.1, +11.2] | 0.001 | 20/20 | 0/20 |
| order-3 chain | Markov-2 | 20 x 1000 | 0.932 | 0.931 | +0.4 (0.6) | +0.4 [-0.7, +1.3] | 0.341 | 0/20 | 0/20 |
| order-4 chain | Markov-1 | 20 x 1000 | 0.931 | 0.896 | +9.9 (1.0) | +10.0 [+6.8, +11.5] | 0.001 | 20/20 | 0/20 |
| order-4 chain | Markov-2 | 20 x 1000 | 0.931 | 0.932 | -0.3 (0.6) | -0.3 [-1.6, +0.8] | 0.647 | 0/20 | 0/20 |
| order-2 chain per recording | Markov-1 | 20 x 1000 | 0.932 | 0.895 | +9.2 (1.5) | +9.6 [+6.8, +11.4] | 0.001 | 20/20 | 0/20 |
| order-2 chain per recording | Markov-2 | 20 x 1000 | 0.932 | 0.931 | +0.5 (0.6) | +0.6 [-0.5, +1.8] | 0.288 | 1/20 | 0/20 |
| order-3 chain per recording | Markov-1 | 20 x 1000 | 0.931 | 0.893 | +8.5 (1.1) | +8.6 [+6.2, +10.2] | 0.001 | 20/20 | 0/20 |
| order-3 chain per recording | Markov-2 | 20 x 1000 | 0.931 | 0.932 | -0.3 (0.6) | -0.2 [-1.7, +0.6] | 0.589 | 0/20 | 0/20 |
| **real song** (README section 4) | Markov-1 | 1 x 1000 | 0.835 | 0.868 | -7.8 | | 1.000 | | |
| **real song** (README section 4) | Markov-2 | 1 x 1000 | 0.835 | 0.931 | -47.3 | | 1.000 | | |

### Calibration detail, ratio 0.25

| ground truth | null | datasets x N | synthetic 'real' R^2 mean | null R^2 mean | z mean (sd) | z median [min, max] | p median | datasets p <= 0.05 | datasets p >= 0.95 |
|---|---|---|---|---|---|---|---|---|---|
| order-1 chain | Markov-1 | 20 x 1000 | 0.726 | 0.751 | -2.2 (0.7) | -2.2 [-3.8, -1.1] | 0.976 | 0/20 | 13/20 |
| order-1 chain | Markov-2 | 20 x 1000 | 0.726 | 0.828 | -11.5 (1.8) | -11.6 [-14.8, -5.9] | 1.000 | 0/20 | 20/20 |
| order-2 chain | Markov-1 | 20 x 1000 | 0.875 | 0.750 | +11.1 (0.8) | +11.1 [+10.1, +12.7] | 0.001 | 20/20 | 0/20 |
| order-2 chain | Markov-2 | 20 x 1000 | 0.875 | 0.896 | -3.8 (0.9) | -3.8 [-5.7, -2.1] | 0.997 | 0/20 | 20/20 |
| order-3 chain | Markov-1 | 20 x 1000 | 0.901 | 0.747 | +13.5 (0.6) | +13.5 [+12.2, +14.5] | 0.001 | 20/20 | 0/20 |
| order-3 chain | Markov-2 | 20 x 1000 | 0.901 | 0.896 | +0.8 (0.5) | +0.7 [-0.1, +1.7] | 0.238 | 2/20 | 0/20 |
| order-4 chain | Markov-1 | 20 x 1000 | 0.900 | 0.749 | +13.3 (0.6) | +13.3 [+11.9, +14.4] | 0.001 | 20/20 | 0/20 |
| order-4 chain | Markov-2 | 20 x 1000 | 0.900 | 0.896 | +0.7 (0.6) | +0.8 [-0.6, +1.7] | 0.232 | 3/20 | 0/20 |
| order-2 chain per recording | Markov-1 | 20 x 1000 | 0.890 | 0.744 | +11.9 (0.7) | +11.8 [+10.6, +13.3] | 0.001 | 20/20 | 0/20 |
| order-2 chain per recording | Markov-2 | 20 x 1000 | 0.890 | 0.895 | -0.9 (0.9) | -0.8 [-3.3, +0.3] | 0.823 | 0/20 | 2/20 |
| order-3 chain per recording | Markov-1 | 20 x 1000 | 0.896 | 0.743 | +12.2 (0.9) | +12.1 [+10.6, +13.7] | 0.001 | 20/20 | 0/20 |
| order-3 chain per recording | Markov-2 | 20 x 1000 | 0.896 | 0.893 | +0.4 (0.8) | +0.5 [-1.5, +1.9] | 0.337 | 1/20 | 0/20 |
| **real song** (README section 4) | Markov-1 | 1 x 1000 | 0.735 | 0.727 | +0.7 | | 0.236 | | |
| **real song** (README section 4) | Markov-2 | 1 x 1000 | 0.735 | 0.873 | -22.8 | | 1.000 | | |

### Calibration detail, ratio 0.75

| ground truth | null | datasets x N | synthetic 'real' R^2 mean | null R^2 mean | z mean (sd) | z median [min, max] | p median | datasets p <= 0.05 | datasets p >= 0.95 |
|---|---|---|---|---|---|---|---|---|---|
| order-1 chain | Markov-1 | 20 x 1000 | 0.918 | 0.936 | -11.2 (0.9) | -11.3 [-13.0, -9.6] | 1.000 | 0/20 | 20/20 |
| order-1 chain | Markov-2 | 20 x 1000 | 0.918 | 0.943 | -14.3 (1.8) | -14.3 [-18.3, -10.9] | 1.000 | 0/20 | 20/20 |
| order-2 chain | Markov-1 | 20 x 1000 | 0.945 | 0.936 | +5.7 (0.7) | +6.0 [+4.1, +6.6] | 0.001 | 20/20 | 0/20 |
| order-2 chain | Markov-2 | 20 x 1000 | 0.945 | 0.936 | +2.9 (0.4) | +2.9 [+2.3, +3.9] | 0.001 | 20/20 | 0/20 |
| order-3 chain | Markov-1 | 20 x 1000 | 0.944 | 0.936 | +4.8 (1.0) | +5.1 [+2.9, +6.0] | 0.001 | 20/20 | 0/20 |
| order-3 chain | Markov-2 | 20 x 1000 | 0.944 | 0.936 | +2.4 (0.5) | +2.4 [+1.7, +3.2] | 0.003 | 20/20 | 0/20 |
| order-4 chain | Markov-1 | 20 x 1000 | 0.943 | 0.936 | +4.6 (1.2) | +4.6 [+1.7, +6.5] | 0.001 | 20/20 | 0/20 |
| order-4 chain | Markov-2 | 20 x 1000 | 0.943 | 0.937 | +2.0 (0.4) | +1.8 [+1.1, +2.8] | 0.022 | 19/20 | 0/20 |
| order-2 chain per recording | Markov-1 | 20 x 1000 | 0.946 | 0.937 | +5.2 (1.3) | +5.2 [+2.5, +7.7] | 0.001 | 20/20 | 0/20 |
| order-2 chain per recording | Markov-2 | 20 x 1000 | 0.946 | 0.938 | +2.5 (0.5) | +2.6 [+1.5, +3.2] | 0.003 | 19/20 | 0/20 |
| order-3 chain per recording | Markov-1 | 20 x 1000 | 0.945 | 0.937 | +4.7 (1.2) | +4.5 [+2.1, +6.7] | 0.001 | 20/20 | 0/20 |
| order-3 chain per recording | Markov-2 | 20 x 1000 | 0.945 | 0.940 | +1.8 (0.6) | +1.9 [+0.1, +3.1] | 0.022 | 15/20 | 0/20 |
| **real song** (README section 4) | Markov-1 | 1 x 1000 | 0.876 | 0.918 | -19.3 | | 1.000 | | |
| **real song** (README section 4) | Markov-2 | 1 x 1000 | 0.876 | 0.945 | -42.7 | | 1.000 | | |

### Calibration detail, trigram TPs

| ground truth | null | datasets x N | synthetic 'real' R^2 mean | null R^2 mean | z mean (sd) | z median [min, max] | p median | datasets p <= 0.05 | datasets p >= 0.95 |
|---|---|---|---|---|---|---|---|---|---|
| order-1 chain | Markov-1 | 20 x 1000 | 0.746 | 0.798 | -6.7 (0.9) | -6.6 [-8.1, -5.2] | 1.000 | 0/20 | 20/20 |
| order-1 chain | Markov-2 | 20 x 1000 | 0.746 | 0.824 | -9.2 (1.4) | -9.3 [-11.3, -4.8] | 1.000 | 0/20 | 20/20 |
| order-2 chain | Markov-1 | 20 x 1000 | 0.865 | 0.802 | +8.1 (1.0) | +8.1 [+6.5, +10.0] | 0.001 | 20/20 | 0/20 |
| order-2 chain | Markov-2 | 20 x 1000 | 0.865 | 0.894 | -4.4 (1.2) | -4.3 [-7.0, -1.9] | 1.000 | 0/20 | 20/20 |
| order-3 chain | Markov-1 | 20 x 1000 | 0.909 | 0.803 | +13.5 (0.7) | +13.6 [+12.0, +14.7] | 0.001 | 20/20 | 0/20 |
| order-3 chain | Markov-2 | 20 x 1000 | 0.909 | 0.894 | +2.1 (0.4) | +2.2 [+1.3, +2.9] | 0.003 | 19/20 | 0/20 |
| order-4 chain | Markov-1 | 20 x 1000 | 0.909 | 0.804 | +13.4 (0.9) | +13.6 [+11.2, +14.7] | 0.001 | 20/20 | 0/20 |
| order-4 chain | Markov-2 | 20 x 1000 | 0.909 | 0.895 | +2.2 (0.7) | +2.2 [+0.9, +3.3] | 0.004 | 16/20 | 0/20 |
| order-2 chain per recording | Markov-1 | 20 x 1000 | 0.889 | 0.803 | +10.5 (1.9) | +10.9 [+6.7, +13.4] | 0.001 | 20/20 | 0/20 |
| order-2 chain per recording | Markov-2 | 20 x 1000 | 0.889 | 0.889 | +0.1 (0.8) | +0.2 [-2.4, +1.0] | 0.466 | 0/20 | 1/20 |
| order-3 chain per recording | Markov-1 | 20 x 1000 | 0.904 | 0.804 | +11.4 (1.1) | +11.4 [+8.8, +13.1] | 0.001 | 20/20 | 0/20 |
| order-3 chain per recording | Markov-2 | 20 x 1000 | 0.904 | 0.886 | +1.9 (0.4) | +1.9 [+1.1, +2.6] | 0.006 | 17/20 | 0/20 |
| **real song** (README section 4) | Markov-1 | 1 x 1000 | 0.753 | 0.747 | +0.6 | | 0.278 | | |
| **real song** (README section 4) | Markov-2 | 1 x 1000 | 0.753 | 0.864 | -15.6 | | 1.000 | | |

### Calibration detail, backward TPs

| ground truth | null | datasets x N | synthetic 'real' R^2 mean | null R^2 mean | z mean (sd) | z median [min, max] | p median | datasets p <= 0.05 | datasets p >= 0.95 |
|---|---|---|---|---|---|---|---|---|---|
| order-1 chain | Markov-1 | 20 x 1000 | 0.839 | 0.864 | -5.4 (0.8) | -5.6 [-7.1, -3.6] | 1.000 | 0/20 | 20/20 |
| order-1 chain | Markov-2 | 20 x 1000 | 0.839 | 0.905 | -21.6 (3.1) | -22.3 [-24.7, -9.3] | 1.000 | 0/20 | 20/20 |
| order-2 chain | Markov-1 | 20 x 1000 | 0.914 | 0.864 | +10.1 (0.6) | +10.2 [+8.2, +11.1] | 0.001 | 20/20 | 0/20 |
| order-2 chain | Markov-2 | 20 x 1000 | 0.914 | 0.920 | -2.0 (0.6) | -2.0 [-3.2, -0.8] | 0.971 | 0/20 | 15/20 |
| order-3 chain | Markov-1 | 20 x 1000 | 0.918 | 0.865 | +10.4 (0.5) | +10.5 [+9.5, +11.3] | 0.001 | 20/20 | 0/20 |
| order-3 chain | Markov-2 | 20 x 1000 | 0.918 | 0.921 | -1.0 (0.7) | -1.1 [-2.4, +0.8] | 0.866 | 0/20 | 3/20 |
| order-4 chain | Markov-1 | 20 x 1000 | 0.916 | 0.865 | +10.0 (0.9) | +10.3 [+7.4, +11.3] | 0.001 | 20/20 | 0/20 |
| order-4 chain | Markov-2 | 20 x 1000 | 0.916 | 0.921 | -1.7 (1.2) | -1.4 [-4.9, -0.2] | 0.907 | 0/20 | 7/20 |
| order-2 chain per recording | Markov-1 | 20 x 1000 | 0.917 | 0.866 | +9.5 (1.8) | +9.4 [+6.0, +12.2] | 0.001 | 20/20 | 0/20 |
| order-2 chain per recording | Markov-2 | 20 x 1000 | 0.917 | 0.921 | -0.9 (0.9) | -0.9 [-3.0, +0.4] | 0.801 | 0/20 | 3/20 |
| order-3 chain per recording | Markov-1 | 20 x 1000 | 0.917 | 0.866 | +9.0 (1.4) | +8.9 [+6.6, +11.2] | 0.001 | 20/20 | 0/20 |
| order-3 chain per recording | Markov-2 | 20 x 1000 | 0.917 | 0.922 | -1.4 (0.8) | -1.3 [-3.3, -0.5] | 0.900 | 0/20 | 6/20 |
| **real song** (README section 4) | Markov-1 | 1 x 1000 | 0.827 | 0.835 | -1.5 | | 0.920 | | |
| **real song** (README section 4) | Markov-2 | 1 x 1000 | 0.827 | 0.914 | -30.5 | | 1.000 | | |

## Held-out order choice

pooled bits per element by order: 0: 8.452, 1: 6.995, 2: 7.054, 3: 7.137, 4: 7.169; best order per group: [1, 1, 1, 1, 1, 2, 1, 1]; unseen order-2 contexts 49.1%

## Recording differences

- order-1 chain: 4.910–4.975 bits, 18.5–19.1% unseen
- order-2 chain: 3.592–3.765 bits, 19.3–20.9% unseen
- order-3 chain: 3.644–4.104 bits, 20.4–24.2% unseen
- order-4 chain: 4.024–4.697 bits, 23.1–29.2% unseen
- order-2 chain per recording: 7.424–7.774 bits, 53.5–56.5% unseen
- order-3 chain per recording: 7.381–7.883 bits, 53.8–57.5% unseen

## Copying

order-2 chain 2.5%, order-3 chain 10.5%, order-2 chain per recording 35.9%, order-3 chain per recording 74.0%

## TP cuts vs word boundaries

- ratio 0.5 (main): precision 0.967 (chance 0.821), recall 0.461, cuts 17897
- ratio 0.25: precision 0.978 (chance 0.821), recall 0.346, cuts 13268
- ratio 0.75: precision 0.959 (chance 0.821), recall 0.533, cuts 20821
- trigram TPs: precision 0.985 (chance 0.821), recall 0.306, cuts 11632
- backward TPs: precision 0.942 (chance 0.821), recall 0.429, cuts 17090
