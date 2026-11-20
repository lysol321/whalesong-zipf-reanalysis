# Speech sample A: CHILDES Brent-Ratner phonemes in the whale layout (49 phoneme types)

## Nulls: R² (null mean, z, p(null ≥ real))

| null | ratio 0.5 (main) | ratio 0.25 | ratio 0.75 | trigram TPs | backward TPs |
|---|---|---|---|---|---|
| real | 0.920 | 0.811 | 0.950 | 0.924 | 0.917 |
| shuffle (N=1000) | 0.638, z +25.5, p 0.001 | 0.271, z +24.8, p 0.001 | 0.813, z +24.8, p 0.001 | 0.468, z +30.3, p 0.001 | 0.586, z +27.4, p 0.001 |
| rotate (N=1000) | 0.795, z +22.6, p 0.001 | 0.542, z +17.4, p 0.001 | 0.881, z +20.9, p 0.001 | 0.739, z +18.4, p 0.001 | 0.796, z +23.0, p 0.001 |
| markov1 (N=1000) | 0.852, z +13.3, p 0.001 | 0.656, z +12.6, p 0.001 | 0.920, z +10.6, p 0.001 | 0.821, z +15.6, p 0.001 | 0.838, z +12.7, p 0.001 |
| markov2 (N=1000) | 0.926, z -2.3, p 0.985 | 0.779, z +3.4, p 0.001 | 0.957, z -4.1, p 1.000 | 0.918, z +1.4, p 0.080 | 0.918, z -0.2, p 0.601 |
| repeat (N=1000) | 0.864, z +11.9, p 0.001 | 0.685, z +11.1, p 0.001 | 0.925, z +9.7, p 0.001 | 0.834, z +15.3, p 0.001 | 0.853, z +11.6, p 0.001 |
| markov2cv (N=1000) | 0.928, z -2.9, p 0.997 | 0.784, z +2.7, p 0.003 | 0.957, z -3.8, p 1.000 | 0.919, z +1.2, p 0.104 | 0.919, z -0.5, p 0.711 |
| markov2wb (N=1000) | 0.876, z +9.4, p 0.001 | 0.699, z +9.6, p 0.001 | 0.931, z +7.0, p 0.001 | 0.878, z +8.8, p 0.001 | 0.876, z +7.5, p 0.001 |

## Brevity, main pipeline (z and p(null at least as strong as real))

| null | Kendall τ null mean | z | p | Poisson slope null mean | z | p |
|---|---|---|---|---|---|---|
| real | -0.335 | | | -0.393 | | |
| shuffle | -0.361 | +3.7 | 1.000 | -0.080 | -89.9 | 0.001 |
| rotate | -0.357 | +3.1 | 0.999 | -0.277 | -42.0 | 0.001 |
| markov1 | -0.435 | +14.6 | 1.000 | -0.489 | +8.1 | 1.000 |
| markov2 | -0.383 | +4.6 | 1.000 | -0.427 | +2.9 | 0.998 |
| repeat | -0.425 | +11.8 | 1.000 | -0.485 | +7.5 | 1.000 |
| markov2cv | -0.380 | +4.2 | 1.000 | -0.425 | +2.8 | 0.999 |
| markov2wb | -0.377 | +4.9 | 1.000 | -0.435 | +3.6 | 0.999 |

## Calibration bands (Markov-1 / Markov-2 z, [min, max] over fake datasets)

| pipeline | real | order-1 chain | order-2 chain | order-3 chain | order-4 chain | order-2 chain per recording | order-3 chain per recording |
|---|---|---|---|---|---|---|---|
| ratio 0.5 (main) | +13.3 / -2.3 | [-2.9, +0.4] / [-11.0, -6.9] | [+12.5, +14.3] / [-6.7, -3.6] | [+17.2, +19.0] / [+3.6, +6.4] | [+17.3, +19.7] / [+2.3, +6.5] | [+15.6, +17.3] / [+0.0, +2.6] | [+17.5, +19.3] / [+4.3, +6.8] |
| ratio 0.25 | +12.6 / +3.4 | [-2.7, +1.3] / [-6.3, -2.1] | [+8.5, +11.3] / [-4.5, -1.3] | [+15.9, +19.1] / [+7.1, +9.1] | [+18.7, +22.0] / [+10.0, +12.8] | [+11.9, +15.2] / [+1.1, +4.4] | [+18.9, +21.6] / [+9.4, +12.4] |
| ratio 0.75 | +10.6 / -4.1 | [-3.6, -0.9] / [-13.3, -9.4] | [+11.1, +13.8] / [-0.2, +1.9] | [+9.1, +13.2] / [-1.7, +1.5] | [+8.9, +13.5] / [-2.0, +1.5] | [+12.3, +14.6] / [+0.3, +2.8] | [+9.3, +13.2] / [-1.5, +1.7] |
| trigram TPs | +15.6 / +1.4 | [-4.0, +0.3] / [-11.1, -7.6] | [+13.3, +16.7] / [-3.5, -1.0] | [+18.2, +21.1] / [+4.0, +6.2] | [+18.6, +21.7] / [+3.2, +6.6] | [+16.3, +18.5] / [+0.3, +3.3] | [+18.6, +21.9] / [+4.6, +6.7] |
| backward TPs | +12.7 / -0.2 | [-2.2, +0.7] / [-7.9, -5.1] | [+10.8, +13.2] / [-5.6, -1.9] | [+15.2, +17.0] / [+4.1, +6.0] | [+14.4, +17.3] / [+2.3, +6.6] | [+13.2, +15.4] / [+0.3, +3.3] | [+14.7, +16.7] / [+2.7, +6.1] |

SD distance of real song's z from each truth's mean z (Markov-1 / Markov-2):

| pipeline | order-1 chain | order-2 chain | order-3 chain | order-4 chain | order-2 chain per recording | order-3 chain per recording |
|---|---|---|---|---|---|---|
| ratio 0.5 (main) | +17.4 / +6.3 | -0.4 / +2.9 | -10.6 / -10.0 | -8.1 / -5.8 | -7.9 / -6.3 | -8.9 / -12.0 |
| ratio 0.25 | +16.1 / +8.9 | +4.4 / +6.7 | -6.9 / -7.8 | -9.0 / -11.4 | -1.0 / +0.7 | -9.6 / -11.0 |
| ratio 0.75 | +19.4 / +6.9 | -3.0 / -9.0 | -1.4 / -6.9 | -0.3 / -5.2 | -4.3 / -9.6 | -0.9 / -5.5 |
| trigram TPs | +17.0 / +11.0 | +0.8 / +5.5 | -6.0 / -8.0 | -6.2 / -5.0 | -3.2 / -1.2 | -5.1 / -6.7 |
| backward TPs | +19.0 / +8.8 | +0.8 / +3.2 | -6.6 / -11.1 | -4.2 / -3.9 | -2.5 / -2.0 | -5.3 / -5.1 |

### Calibration detail, ratio 0.5 (main)

| ground truth | null | datasets x N | synthetic 'real' R^2 mean | null R^2 mean | z mean (sd) | z median [min, max] | p median | datasets p <= 0.05 | datasets p >= 0.95 |
|---|---|---|---|---|---|---|---|---|---|
| order-1 chain | Markov-1 | 20 x 1000 | 0.852 | 0.860 | -1.6 (0.9) | -1.9 [-2.9, +0.4] | 0.960 | 0/20 | 12/20 |
| order-1 chain | Markov-2 | 20 x 1000 | 0.852 | 0.889 | -9.2 (1.1) | -9.6 [-11.0, -6.9] | 1.000 | 0/20 | 20/20 |
| order-2 chain | Markov-1 | 20 x 1000 | 0.926 | 0.860 | +13.5 (0.5) | +13.5 [+12.5, +14.3] | 0.001 | 20/20 | 0/20 |
| order-2 chain | Markov-2 | 20 x 1000 | 0.926 | 0.938 | -5.1 (0.9) | -5.1 [-6.7, -3.6] | 1.000 | 0/20 | 20/20 |
| order-3 chain | Markov-1 | 20 x 1000 | 0.950 | 0.860 | +18.3 (0.5) | +18.4 [+17.2, +19.0] | 0.001 | 20/20 | 0/20 |
| order-3 chain | Markov-2 | 20 x 1000 | 0.950 | 0.938 | +5.1 (0.7) | +5.2 [+3.6, +6.4] | 0.001 | 20/20 | 0/20 |
| order-4 chain | Markov-1 | 20 x 1000 | 0.949 | 0.861 | +18.4 (0.6) | +18.3 [+17.3, +19.7] | 0.001 | 20/20 | 0/20 |
| order-4 chain | Markov-2 | 20 x 1000 | 0.949 | 0.938 | +4.6 (1.2) | +4.3 [+2.3, +6.5] | 0.001 | 20/20 | 0/20 |
| order-2 chain per recording | Markov-1 | 20 x 1000 | 0.942 | 0.859 | +16.6 (0.4) | +16.7 [+15.6, +17.3] | 0.001 | 20/20 | 0/20 |
| order-2 chain per recording | Markov-2 | 20 x 1000 | 0.942 | 0.938 | +1.6 (0.6) | +1.6 [+0.0, +2.6] | 0.044 | 10/20 | 0/20 |
| order-3 chain per recording | Markov-1 | 20 x 1000 | 0.950 | 0.860 | +18.2 (0.5) | +18.0 [+17.5, +19.3] | 0.001 | 20/20 | 0/20 |
| order-3 chain per recording | Markov-2 | 20 x 1000 | 0.950 | 0.938 | +5.1 (0.6) | +5.0 [+4.3, +6.8] | 0.001 | 20/20 | 0/20 |
| **real song** (README section 4) | Markov-1 | 1 x 1000 | 0.920 | 0.852 | +13.3 | | 0.001 | | |
| **real song** (README section 4) | Markov-2 | 1 x 1000 | 0.920 | 0.926 | -2.3 | | 0.985 | | |

### Calibration detail, ratio 0.25

| ground truth | null | datasets x N | synthetic 'real' R^2 mean | null R^2 mean | z mean (sd) | z median [min, max] | p median | datasets p <= 0.05 | datasets p >= 0.95 |
|---|---|---|---|---|---|---|---|---|---|
| order-1 chain | Markov-1 | 20 x 1000 | 0.657 | 0.661 | -0.4 (0.8) | -0.4 [-2.7, +1.3] | 0.649 | 0/20 | 1/20 |
| order-1 chain | Markov-2 | 20 x 1000 | 0.657 | 0.705 | -4.1 (0.8) | -4.1 [-6.3, -2.1] | 1.000 | 0/20 | 20/20 |
| order-2 chain | Markov-1 | 20 x 1000 | 0.779 | 0.662 | +9.5 (0.7) | +9.4 [+8.5, +11.3] | 0.001 | 20/20 | 0/20 |
| order-2 chain | Markov-2 | 20 x 1000 | 0.779 | 0.806 | -2.9 (0.9) | -2.9 [-4.5, -1.3] | 0.993 | 0/20 | 17/20 |
| order-3 chain | Markov-1 | 20 x 1000 | 0.881 | 0.661 | +17.8 (0.8) | +17.8 [+15.9, +19.1] | 0.001 | 20/20 | 0/20 |
| order-3 chain | Markov-2 | 20 x 1000 | 0.881 | 0.805 | +8.1 (0.6) | +8.1 [+7.1, +9.1] | 0.001 | 20/20 | 0/20 |
| order-4 chain | Markov-1 | 20 x 1000 | 0.914 | 0.665 | +20.6 (0.9) | +20.8 [+18.7, +22.0] | 0.001 | 20/20 | 0/20 |
| order-4 chain | Markov-2 | 20 x 1000 | 0.914 | 0.810 | +11.8 (0.7) | +12.0 [+10.0, +12.8] | 0.001 | 20/20 | 0/20 |
| order-2 chain per recording | Markov-1 | 20 x 1000 | 0.831 | 0.659 | +13.5 (1.0) | +13.7 [+11.9, +15.2] | 0.001 | 20/20 | 0/20 |
| order-2 chain per recording | Markov-2 | 20 x 1000 | 0.831 | 0.805 | +2.7 (0.9) | +2.7 [+1.1, +4.4] | 0.002 | 18/20 | 0/20 |
| order-3 chain per recording | Markov-1 | 20 x 1000 | 0.909 | 0.662 | +20.1 (0.8) | +20.1 [+18.9, +21.6] | 0.001 | 20/20 | 0/20 |
| order-3 chain per recording | Markov-2 | 20 x 1000 | 0.909 | 0.808 | +11.2 (0.7) | +11.2 [+9.4, +12.4] | 0.001 | 20/20 | 0/20 |
| **real song** (README section 4) | Markov-1 | 1 x 1000 | 0.811 | 0.656 | +12.6 | | 0.001 | | |
| **real song** (README section 4) | Markov-2 | 1 x 1000 | 0.811 | 0.779 | +3.4 | | 0.001 | | |

### Calibration detail, ratio 0.75

| ground truth | null | datasets x N | synthetic 'real' R^2 mean | null R^2 mean | z mean (sd) | z median [min, max] | p median | datasets p <= 0.05 | datasets p >= 0.95 |
|---|---|---|---|---|---|---|---|---|---|
| order-1 chain | Markov-1 | 20 x 1000 | 0.920 | 0.927 | -2.5 (0.7) | -2.4 [-3.6, -0.9] | 0.989 | 0/20 | 19/20 |
| order-1 chain | Markov-2 | 20 x 1000 | 0.920 | 0.942 | -11.4 (1.1) | -11.4 [-13.3, -9.4] | 1.000 | 0/20 | 20/20 |
| order-2 chain | Markov-1 | 20 x 1000 | 0.958 | 0.927 | +12.5 (0.6) | +12.5 [+11.1, +13.8] | 0.001 | 20/20 | 0/20 |
| order-2 chain | Markov-2 | 20 x 1000 | 0.958 | 0.956 | +0.9 (0.5) | +0.9 [-0.2, +1.9] | 0.180 | 2/20 | 0/20 |
| order-3 chain | Markov-1 | 20 x 1000 | 0.957 | 0.927 | +12.0 (1.0) | +12.1 [+9.1, +13.2] | 0.001 | 20/20 | 0/20 |
| order-3 chain | Markov-2 | 20 x 1000 | 0.957 | 0.956 | +0.6 (0.7) | +0.7 [-1.7, +1.5] | 0.241 | 0/20 | 0/20 |
| order-4 chain | Markov-1 | 20 x 1000 | 0.954 | 0.927 | +10.9 (1.0) | +10.9 [+8.9, +13.5] | 0.001 | 20/20 | 0/20 |
| order-4 chain | Markov-2 | 20 x 1000 | 0.954 | 0.955 | -0.1 (0.8) | -0.1 [-2.0, +1.5] | 0.577 | 0/20 | 1/20 |
| order-2 chain per recording | Markov-1 | 20 x 1000 | 0.960 | 0.926 | +13.2 (0.6) | +13.1 [+12.3, +14.6] | 0.001 | 20/20 | 0/20 |
| order-2 chain per recording | Markov-2 | 20 x 1000 | 0.960 | 0.955 | +1.8 (0.6) | +1.7 [+0.3, +2.8] | 0.025 | 12/20 | 0/20 |
| order-3 chain per recording | Markov-1 | 20 x 1000 | 0.956 | 0.927 | +11.5 (0.9) | +11.6 [+9.3, +13.2] | 0.001 | 20/20 | 0/20 |
| order-3 chain per recording | Markov-2 | 20 x 1000 | 0.956 | 0.955 | +0.2 (0.8) | +0.3 [-1.5, +1.7] | 0.422 | 1/20 | 0/20 |
| **real song** (README section 4) | Markov-1 | 1 x 1000 | 0.950 | 0.920 | +10.6 | | 0.001 | | |
| **real song** (README section 4) | Markov-2 | 1 x 1000 | 0.950 | 0.957 | -4.1 | | 1.000 | | |

### Calibration detail, trigram TPs

| ground truth | null | datasets x N | synthetic 'real' R^2 mean | null R^2 mean | z mean (sd) | z median [min, max] | p median | datasets p <= 0.05 | datasets p >= 0.95 |
|---|---|---|---|---|---|---|---|---|---|
| order-1 chain | Markov-1 | 20 x 1000 | 0.823 | 0.831 | -1.4 (1.0) | -1.5 [-4.0, +0.3] | 0.925 | 0/20 | 7/20 |
| order-1 chain | Markov-2 | 20 x 1000 | 0.823 | 0.869 | -9.3 (1.0) | -9.4 [-11.1, -7.6] | 1.000 | 0/20 | 20/20 |
| order-2 chain | Markov-1 | 20 x 1000 | 0.920 | 0.831 | +14.8 (0.9) | +14.9 [+13.3, +16.7] | 0.001 | 20/20 | 0/20 |
| order-2 chain | Markov-2 | 20 x 1000 | 0.920 | 0.929 | -2.3 (0.7) | -2.4 [-3.5, -1.0] | 0.982 | 0/20 | 16/20 |
| order-3 chain | Markov-1 | 20 x 1000 | 0.949 | 0.832 | +19.6 (0.7) | +19.5 [+18.2, +21.1] | 0.001 | 20/20 | 0/20 |
| order-3 chain | Markov-2 | 20 x 1000 | 0.949 | 0.928 | +5.5 (0.5) | +5.6 [+4.0, +6.2] | 0.001 | 20/20 | 0/20 |
| order-4 chain | Markov-1 | 20 x 1000 | 0.950 | 0.834 | +20.1 (0.7) | +19.9 [+18.6, +21.7] | 0.001 | 20/20 | 0/20 |
| order-4 chain | Markov-2 | 20 x 1000 | 0.950 | 0.929 | +5.5 (0.8) | +5.5 [+3.2, +6.6] | 0.001 | 20/20 | 0/20 |
| order-2 chain per recording | Markov-1 | 20 x 1000 | 0.937 | 0.831 | +17.5 (0.6) | +17.8 [+16.3, +18.5] | 0.001 | 20/20 | 0/20 |
| order-2 chain per recording | Markov-2 | 20 x 1000 | 0.937 | 0.928 | +2.1 (0.6) | +2.1 [+0.3, +3.3] | 0.006 | 19/20 | 0/20 |
| order-3 chain per recording | Markov-1 | 20 x 1000 | 0.950 | 0.833 | +19.6 (0.8) | +19.5 [+18.6, +21.9] | 0.001 | 20/20 | 0/20 |
| order-3 chain per recording | Markov-2 | 20 x 1000 | 0.950 | 0.928 | +5.7 (0.6) | +5.7 [+4.6, +6.7] | 0.001 | 20/20 | 0/20 |
| **real song** (README section 4) | Markov-1 | 1 x 1000 | 0.924 | 0.821 | +15.6 | | 0.001 | | |
| **real song** (README section 4) | Markov-2 | 1 x 1000 | 0.924 | 0.918 | +1.4 | | 0.080 | | |

### Calibration detail, backward TPs

| ground truth | null | datasets x N | synthetic 'real' R^2 mean | null R^2 mean | z mean (sd) | z median [min, max] | p median | datasets p <= 0.05 | datasets p >= 0.95 |
|---|---|---|---|---|---|---|---|---|---|
| order-1 chain | Markov-1 | 20 x 1000 | 0.838 | 0.843 | -0.8 (0.7) | -0.8 [-2.2, +0.7] | 0.791 | 0/20 | 2/20 |
| order-1 chain | Markov-2 | 20 x 1000 | 0.838 | 0.872 | -6.5 (0.7) | -6.5 [-7.9, -5.1] | 1.000 | 0/20 | 20/20 |
| order-2 chain | Markov-1 | 20 x 1000 | 0.918 | 0.844 | +12.1 (0.7) | +12.3 [+10.8, +13.2] | 0.001 | 20/20 | 0/20 |
| order-2 chain | Markov-2 | 20 x 1000 | 0.918 | 0.929 | -3.9 (1.1) | -3.9 [-5.6, -1.9] | 1.000 | 0/20 | 20/20 |
| order-3 chain | Markov-1 | 20 x 1000 | 0.943 | 0.844 | +16.1 (0.5) | +16.0 [+15.2, +17.0] | 0.001 | 20/20 | 0/20 |
| order-3 chain | Markov-2 | 20 x 1000 | 0.943 | 0.928 | +5.0 (0.5) | +5.1 [+4.1, +6.0] | 0.001 | 20/20 | 0/20 |
| order-4 chain | Markov-1 | 20 x 1000 | 0.941 | 0.845 | +15.9 (0.8) | +16.0 [+14.4, +17.3] | 0.001 | 20/20 | 0/20 |
| order-4 chain | Markov-2 | 20 x 1000 | 0.941 | 0.929 | +4.3 (1.1) | +4.0 [+2.3, +6.6] | 0.001 | 20/20 | 0/20 |
| order-2 chain per recording | Markov-1 | 20 x 1000 | 0.933 | 0.842 | +14.3 (0.7) | +14.2 [+13.2, +15.4] | 0.001 | 20/20 | 0/20 |
| order-2 chain per recording | Markov-2 | 20 x 1000 | 0.933 | 0.928 | +1.5 (0.9) | +1.4 [+0.3, +3.3] | 0.075 | 9/20 | 0/20 |
| order-3 chain per recording | Markov-1 | 20 x 1000 | 0.941 | 0.844 | +15.8 (0.6) | +15.7 [+14.7, +16.7] | 0.001 | 20/20 | 0/20 |
| order-3 chain per recording | Markov-2 | 20 x 1000 | 0.941 | 0.928 | +4.5 (0.9) | +4.7 [+2.7, +6.1] | 0.001 | 20/20 | 0/20 |
| **real song** (README section 4) | Markov-1 | 1 x 1000 | 0.917 | 0.838 | +12.7 | | 0.001 | | |
| **real song** (README section 4) | Markov-2 | 1 x 1000 | 0.917 | 0.918 | -0.2 | | 0.601 | | |

## Held-out order choice

pooled bits per element by order: 0: 5.076, 1: 3.897, 2: 3.330, 3: 3.304, 4: 3.402; best order per group: [2, 2, 2, 2, 3, 3, 2, 3]; unseen order-2 contexts 6.0%

## Recording differences

- order-1 chain: 3.893–3.925 bits, 2.9–3.1% unseen
- order-2 chain: 2.532–2.572 bits, 2.8–3.2% unseen
- order-3 chain: 2.525–2.583 bits, 2.8–3.3% unseen
- order-4 chain: 2.540–2.621 bits, 2.9–3.5% unseen
- order-2 chain per recording: 3.576–3.638 bits, 8.3–9.2% unseen
- order-3 chain per recording: 3.570–3.660 bits, 8.5–9.3% unseen

## Copying

order-2 chain 1.0%, order-3 chain 5.7%, order-2 chain per recording 13.6%, order-3 chain per recording 53.0%

## TP cuts vs word boundaries

- ratio 0.5 (main): precision 0.659 (chance 0.350), recall 0.617, cuts 14968
- ratio 0.25: precision 0.741 (chance 0.350), recall 0.420, cuts 9069
- ratio 0.75: precision 0.594 (chance 0.350), recall 0.735, cuts 19785
- trigram TPs: precision 0.731 (chance 0.350), recall 0.673, cuts 14715
- backward TPs: precision 0.600 (chance 0.350), recall 0.556, cuts 14813
