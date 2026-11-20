# Speech sample B: CHILDES Brent-Ratner phonemes in the whale layout (50 phoneme types)

## Nulls: R² (null mean, z, p(null ≥ real))

| null | ratio 0.5 (main) | ratio 0.25 | ratio 0.75 | trigram TPs | backward TPs |
|---|---|---|---|---|---|
| real | 0.921 | 0.788 | 0.943 | 0.926 | 0.916 |
| shuffle (N=1000) | 0.607, z +26.7, p 0.001 | 0.240, z +24.1, p 0.001 | 0.801, z +23.6, p 0.001 | 0.439, z +24.8, p 0.001 | 0.552, z +26.9, p 0.001 |
| rotate (N=1000) | 0.794, z +21.8, p 0.001 | 0.535, z +10.5, p 0.001 | 0.884, z +19.6, p 0.001 | 0.736, z +19.2, p 0.001 | 0.780, z +23.7, p 0.001 |
| markov1 (N=1000) | 0.844, z +12.6, p 0.001 | 0.634, z +11.0, p 0.001 | 0.919, z +8.3, p 0.001 | 0.812, z +16.7, p 0.001 | 0.821, z +14.1, p 0.001 |
| markov2 (N=1000) | 0.925, z -1.4, p 0.922 | 0.757, z +2.3, p 0.005 | 0.952, z -5.4, p 1.000 | 0.915, z +2.5, p 0.001 | 0.907, z +2.5, p 0.005 |
| repeat (N=1000) | 0.855, z +12.1, p 0.001 | 0.659, z +9.4, p 0.001 | 0.923, z +7.4, p 0.001 | 0.823, z +16.0, p 0.001 | 0.835, z +13.1, p 0.001 |
| markov2cv (N=1000) | 0.926, z -1.6, p 0.946 | 0.756, z +2.3, p 0.008 | 0.952, z -5.7, p 1.000 | 0.915, z +2.6, p 0.002 | 0.909, z +2.1, p 0.016 |
| markov2wb (N=1000) | 0.873, z +8.8, p 0.001 | 0.676, z +7.7, p 0.001 | 0.930, z +4.8, p 0.001 | 0.875, z +9.0, p 0.001 | 0.859, z +9.4, p 0.001 |

## Brevity, main pipeline (z and p(null at least as strong as real))

| null | Kendall τ null mean | z | p | Poisson slope null mean | z | p |
|---|---|---|---|---|---|---|
| real | -0.345 | | | -0.381 | | |
| shuffle | -0.343 | -0.3 | 0.392 | -0.060 | -119.0 | 0.001 |
| rotate | -0.367 | +3.3 | 0.999 | -0.259 | -46.8 | 0.001 |
| markov1 | -0.439 | +13.6 | 1.000 | -0.483 | +9.2 | 1.000 |
| markov2 | -0.397 | +5.2 | 1.000 | -0.424 | +4.0 | 1.000 |
| repeat | -0.430 | +11.6 | 1.000 | -0.478 | +8.6 | 1.000 |
| markov2cv | -0.396 | +5.0 | 1.000 | -0.423 | +3.6 | 1.000 |
| markov2wb | -0.392 | +5.7 | 1.000 | -0.433 | +4.4 | 1.000 |

## Calibration bands (Markov-1 / Markov-2 z, [min, max] over fake datasets)

| pipeline | real | order-1 chain | order-2 chain | order-3 chain | order-4 chain | order-2 chain per recording | order-3 chain per recording |
|---|---|---|---|---|---|---|---|
| ratio 0.5 (main) | +12.6 / -1.4 | [-3.6, +0.1] / [-9.8, -6.1] | [+11.4, +14.4] / [-5.6, -2.6] | [+14.1, +17.0] / [+1.2, +4.8] | [+13.9, +17.6] / [+0.3, +4.0] | [+14.0, +16.4] / [+0.1, +3.5] | [+15.0, +18.2] / [+2.3, +4.9] |
| ratio 0.25 | +11.0 / +2.3 | [-2.0, +0.5] / [-5.1, -2.4] | [+6.7, +9.8] / [-3.7, -1.1] | [+14.5, +16.9] / [+4.9, +7.9] | [+16.7, +19.9] / [+7.5, +11.9] | [+10.5, +13.5] / [+0.7, +3.8] | [+16.2, +19.4] / [+7.1, +9.7] |
| ratio 0.75 | +8.3 / -5.4 | [-5.0, -0.6] / [-13.9, -8.6] | [+9.2, +11.9] / [+0.9, +2.4] | [+7.4, +10.3] / [-1.1, +0.6] | [+5.5, +10.1] / [-2.4, +0.0] | [+9.1, +12.1] / [+0.5, +2.5] | [+6.6, +10.6] / [-1.7, +1.2] |
| trigram TPs | +16.7 / +2.5 | [-3.4, -0.1] / [-10.3, -7.1] | [+12.3, +15.5] / [-3.9, -0.6] | [+16.5, +18.5] / [+3.3, +5.0] | [+16.3, +18.6] / [+2.2, +5.0] | [+15.1, +17.5] / [+1.3, +3.0] | [+16.5, +19.0] / [+2.8, +4.8] |
| backward TPs | +14.1 / +2.5 | [-2.5, +1.3] / [-9.4, -4.9] | [+12.0, +13.7] / [-5.6, -2.7] | [+15.4, +17.8] / [+3.5, +6.6] | [+15.1, +17.8] / [+1.5, +6.2] | [+14.4, +16.1] / [+0.7, +3.3] | [+14.9, +17.8] / [+3.9, +7.0] |

SD distance of real song's z from each truth's mean z (Markov-1 / Markov-2):

| pipeline | order-1 chain | order-2 chain | order-3 chain | order-4 chain | order-2 chain per recording | order-3 chain per recording |
|---|---|---|---|---|---|---|
| ratio 0.5 (main) | +14.6 / +6.9 | -0.6 / +2.8 | -5.7 / -5.8 | -3.8 / -3.8 | -4.1 / -3.3 | -5.6 / -6.6 |
| ratio 0.25 | +16.5 / +8.8 | +3.3 / +6.2 | -6.4 / -4.7 | -8.9 / -7.7 | -1.4 / -0.1 | -8.1 / -7.3 |
| ratio 0.75 | +9.4 / +4.0 | -3.5 / -16.7 | -0.5 / -10.8 | +0.6 / -6.8 | -2.8 / -12.1 | -0.3 / -6.6 |
| trigram TPs | +21.8 / +14.3 | +3.2 / +5.6 | -1.7 / -3.1 | -1.2 / -1.5 | +0.3 / +0.8 | -1.6 / -3.3 |
| backward TPs | +15.0 / +8.5 | +2.7 / +7.9 | -3.4 / -3.1 | -3.2 / -1.4 | -2.7 / +0.8 | -3.9 / -3.2 |

### Calibration detail, ratio 0.5 (main)

| ground truth | null | datasets x N | synthetic 'real' R^2 mean | null R^2 mean | z mean (sd) | z median [min, max] | p median | datasets p <= 0.05 | datasets p >= 0.95 |
|---|---|---|---|---|---|---|---|---|---|
| order-1 chain | Markov-1 | 20 x 1000 | 0.844 | 0.853 | -1.5 (1.0) | -1.6 [-3.6, +0.1] | 0.938 | 0/20 | 8/20 |
| order-1 chain | Markov-2 | 20 x 1000 | 0.844 | 0.883 | -8.3 (1.0) | -8.3 [-9.8, -6.1] | 1.000 | 0/20 | 20/20 |
| order-2 chain | Markov-1 | 20 x 1000 | 0.926 | 0.853 | +13.0 (0.6) | +13.2 [+11.4, +14.4] | 0.001 | 20/20 | 0/20 |
| order-2 chain | Markov-2 | 20 x 1000 | 0.926 | 0.936 | -3.8 (0.9) | -3.8 [-5.6, -2.6] | 1.000 | 0/20 | 20/20 |
| order-3 chain | Markov-1 | 20 x 1000 | 0.945 | 0.851 | +16.3 (0.6) | +16.4 [+14.1, +17.0] | 0.001 | 20/20 | 0/20 |
| order-3 chain | Markov-2 | 20 x 1000 | 0.945 | 0.935 | +3.7 (0.9) | +4.0 [+1.2, +4.8] | 0.001 | 19/20 | 0/20 |
| order-4 chain | Markov-1 | 20 x 1000 | 0.942 | 0.854 | +15.9 (0.9) | +15.9 [+13.9, +17.6] | 0.001 | 20/20 | 0/20 |
| order-4 chain | Markov-2 | 20 x 1000 | 0.942 | 0.936 | +2.5 (1.1) | +2.8 [+0.3, +4.0] | 0.001 | 15/20 | 0/20 |
| order-2 chain per recording | Markov-1 | 20 x 1000 | 0.939 | 0.850 | +15.4 (0.7) | +15.5 [+14.0, +16.4] | 0.001 | 20/20 | 0/20 |
| order-2 chain per recording | Markov-2 | 20 x 1000 | 0.939 | 0.935 | +1.8 (1.0) | +2.0 [+0.1, +3.5] | 0.018 | 13/20 | 0/20 |
| order-3 chain per recording | Markov-1 | 20 x 1000 | 0.944 | 0.851 | +16.4 (0.7) | +16.3 [+15.0, +18.2] | 0.001 | 20/20 | 0/20 |
| order-3 chain per recording | Markov-2 | 20 x 1000 | 0.944 | 0.935 | +3.7 (0.8) | +3.6 [+2.3, +4.9] | 0.001 | 20/20 | 0/20 |
| **real song** (README section 4) | Markov-1 | 1 x 1000 | 0.921 | 0.844 | +12.6 | | 0.001 | | |
| **real song** (README section 4) | Markov-2 | 1 x 1000 | 0.921 | 0.925 | -1.4 | | 0.922 | | |

### Calibration detail, ratio 0.25

| ground truth | null | datasets x N | synthetic 'real' R^2 mean | null R^2 mean | z mean (sd) | z median [min, max] | p median | datasets p <= 0.05 | datasets p >= 0.95 |
|---|---|---|---|---|---|---|---|---|---|
| order-1 chain | Markov-1 | 20 x 1000 | 0.633 | 0.638 | -0.4 (0.7) | -0.2 [-2.0, +0.5] | 0.597 | 0/20 | 2/20 |
| order-1 chain | Markov-2 | 20 x 1000 | 0.633 | 0.681 | -3.5 (0.7) | -3.5 [-5.1, -2.4] | 0.999 | 0/20 | 20/20 |
| order-2 chain | Markov-1 | 20 x 1000 | 0.761 | 0.638 | +8.4 (0.8) | +8.6 [+6.7, +9.8] | 0.001 | 20/20 | 0/20 |
| order-2 chain | Markov-2 | 20 x 1000 | 0.761 | 0.787 | -2.1 (0.7) | -2.0 [-3.7, -1.1] | 0.965 | 0/20 | 11/20 |
| order-3 chain | Markov-1 | 20 x 1000 | 0.865 | 0.634 | +15.8 (0.7) | +15.9 [+14.5, +16.9] | 0.001 | 20/20 | 0/20 |
| order-3 chain | Markov-2 | 20 x 1000 | 0.865 | 0.787 | +6.3 (0.9) | +6.6 [+4.9, +7.9] | 0.001 | 20/20 | 0/20 |
| order-4 chain | Markov-1 | 20 x 1000 | 0.904 | 0.640 | +18.6 (0.9) | +18.6 [+16.7, +19.9] | 0.001 | 20/20 | 0/20 |
| order-4 chain | Markov-2 | 20 x 1000 | 0.904 | 0.792 | +9.4 (0.9) | +9.4 [+7.5, +11.9] | 0.001 | 20/20 | 0/20 |
| order-2 chain per recording | Markov-1 | 20 x 1000 | 0.813 | 0.634 | +12.2 (0.9) | +12.3 [+10.5, +13.5] | 0.001 | 20/20 | 0/20 |
| order-2 chain per recording | Markov-2 | 20 x 1000 | 0.813 | 0.783 | +2.4 (0.7) | +2.5 [+0.7, +3.8] | 0.002 | 18/20 | 0/20 |
| order-3 chain per recording | Markov-1 | 20 x 1000 | 0.892 | 0.635 | +17.6 (0.8) | +17.6 [+16.2, +19.4] | 0.001 | 20/20 | 0/20 |
| order-3 chain per recording | Markov-2 | 20 x 1000 | 0.892 | 0.786 | +8.3 (0.8) | +8.4 [+7.1, +9.7] | 0.001 | 20/20 | 0/20 |
| **real song** (README section 4) | Markov-1 | 1 x 1000 | 0.788 | 0.634 | +11.0 | | 0.001 | | |
| **real song** (README section 4) | Markov-2 | 1 x 1000 | 0.788 | 0.757 | +2.3 | | 0.005 | | |

### Calibration detail, ratio 0.75

| ground truth | null | datasets x N | synthetic 'real' R^2 mean | null R^2 mean | z mean (sd) | z median [min, max] | p median | datasets p <= 0.05 | datasets p >= 0.95 |
|---|---|---|---|---|---|---|---|---|---|
| order-1 chain | Markov-1 | 20 x 1000 | 0.918 | 0.924 | -2.4 (1.1) | -2.2 [-5.0, -0.6] | 0.983 | 0/20 | 14/20 |
| order-1 chain | Markov-2 | 20 x 1000 | 0.918 | 0.940 | -11.3 (1.5) | -11.4 [-13.9, -8.6] | 1.000 | 0/20 | 20/20 |
| order-2 chain | Markov-1 | 20 x 1000 | 0.952 | 0.925 | +10.8 (0.7) | +10.9 [+9.2, +11.9] | 0.001 | 20/20 | 0/20 |
| order-2 chain | Markov-2 | 20 x 1000 | 0.952 | 0.948 | +1.6 (0.4) | +1.6 [+0.9, +2.4] | 0.041 | 12/20 | 0/20 |
| order-3 chain | Markov-1 | 20 x 1000 | 0.947 | 0.924 | +8.7 (0.9) | +8.7 [+7.4, +10.3] | 0.001 | 20/20 | 0/20 |
| order-3 chain | Markov-2 | 20 x 1000 | 0.947 | 0.948 | -0.3 (0.5) | -0.3 [-1.1, +0.6] | 0.625 | 0/20 | 0/20 |
| order-4 chain | Markov-1 | 20 x 1000 | 0.945 | 0.925 | +7.6 (1.1) | +7.5 [+5.5, +10.1] | 0.001 | 20/20 | 0/20 |
| order-4 chain | Markov-2 | 20 x 1000 | 0.945 | 0.947 | -1.0 (0.6) | -1.0 [-2.4, +0.0] | 0.848 | 0/20 | 3/20 |
| order-2 chain per recording | Markov-1 | 20 x 1000 | 0.952 | 0.924 | +10.9 (0.9) | +10.9 [+9.1, +12.1] | 0.001 | 20/20 | 0/20 |
| order-2 chain per recording | Markov-2 | 20 x 1000 | 0.952 | 0.948 | +1.5 (0.6) | +1.6 [+0.5, +2.5] | 0.045 | 11/20 | 0/20 |
| order-3 chain per recording | Markov-1 | 20 x 1000 | 0.946 | 0.924 | +8.6 (1.1) | +8.5 [+6.6, +10.6] | 0.001 | 20/20 | 0/20 |
| order-3 chain per recording | Markov-2 | 20 x 1000 | 0.946 | 0.948 | -0.6 (0.7) | -0.8 [-1.7, +1.2] | 0.789 | 0/20 | 1/20 |
| **real song** (README section 4) | Markov-1 | 1 x 1000 | 0.943 | 0.919 | +8.3 | | 0.001 | | |
| **real song** (README section 4) | Markov-2 | 1 x 1000 | 0.943 | 0.952 | -5.4 | | 1.000 | | |

### Calibration detail, trigram TPs

| ground truth | null | datasets x N | synthetic 'real' R^2 mean | null R^2 mean | z mean (sd) | z median [min, max] | p median | datasets p <= 0.05 | datasets p >= 0.95 |
|---|---|---|---|---|---|---|---|---|---|
| order-1 chain | Markov-1 | 20 x 1000 | 0.809 | 0.821 | -1.8 (0.8) | -1.8 [-3.4, -0.1] | 0.954 | 0/20 | 11/20 |
| order-1 chain | Markov-2 | 20 x 1000 | 0.809 | 0.859 | -8.5 (0.8) | -8.5 [-10.3, -7.1] | 1.000 | 0/20 | 20/20 |
| order-2 chain | Markov-1 | 20 x 1000 | 0.913 | 0.822 | +13.8 (0.9) | +13.8 [+12.3, +15.5] | 0.001 | 20/20 | 0/20 |
| order-2 chain | Markov-2 | 20 x 1000 | 0.913 | 0.923 | -2.3 (0.9) | -2.4 [-3.9, -0.6] | 0.982 | 0/20 | 12/20 |
| order-3 chain | Markov-1 | 20 x 1000 | 0.940 | 0.821 | +17.6 (0.5) | +17.6 [+16.5, +18.5] | 0.001 | 20/20 | 0/20 |
| order-3 chain | Markov-2 | 20 x 1000 | 0.940 | 0.922 | +4.0 (0.5) | +4.0 [+3.3, +5.0] | 0.001 | 20/20 | 0/20 |
| order-4 chain | Markov-1 | 20 x 1000 | 0.939 | 0.824 | +17.5 (0.7) | +17.4 [+16.3, +18.6] | 0.001 | 20/20 | 0/20 |
| order-4 chain | Markov-2 | 20 x 1000 | 0.939 | 0.924 | +3.7 (0.8) | +3.8 [+2.2, +5.0] | 0.001 | 20/20 | 0/20 |
| order-2 chain per recording | Markov-1 | 20 x 1000 | 0.932 | 0.820 | +16.4 (0.7) | +16.6 [+15.1, +17.5] | 0.001 | 20/20 | 0/20 |
| order-2 chain per recording | Markov-2 | 20 x 1000 | 0.932 | 0.922 | +2.2 (0.4) | +2.2 [+1.3, +3.0] | 0.003 | 18/20 | 0/20 |
| order-3 chain per recording | Markov-1 | 20 x 1000 | 0.941 | 0.821 | +17.7 (0.7) | +17.9 [+16.5, +19.0] | 0.001 | 20/20 | 0/20 |
| order-3 chain per recording | Markov-2 | 20 x 1000 | 0.941 | 0.921 | +4.2 (0.5) | +4.2 [+2.8, +4.8] | 0.001 | 20/20 | 0/20 |
| **real song** (README section 4) | Markov-1 | 1 x 1000 | 0.926 | 0.812 | +16.7 | | 0.001 | | |
| **real song** (README section 4) | Markov-2 | 1 x 1000 | 0.926 | 0.915 | +2.5 | | 0.001 | | |

### Calibration detail, backward TPs

| ground truth | null | datasets x N | synthetic 'real' R^2 mean | null R^2 mean | z mean (sd) | z median [min, max] | p median | datasets p <= 0.05 | datasets p >= 0.95 |
|---|---|---|---|---|---|---|---|---|---|
| order-1 chain | Markov-1 | 20 x 1000 | 0.823 | 0.825 | -0.3 (1.0) | -0.1 [-2.5, +1.3] | 0.539 | 0/20 | 1/20 |
| order-1 chain | Markov-2 | 20 x 1000 | 0.823 | 0.858 | -6.5 (1.1) | -6.4 [-9.4, -4.9] | 1.000 | 0/20 | 20/20 |
| order-2 chain | Markov-1 | 20 x 1000 | 0.907 | 0.825 | +12.8 (0.5) | +12.8 [+12.0, +13.7] | 0.001 | 20/20 | 0/20 |
| order-2 chain | Markov-2 | 20 x 1000 | 0.907 | 0.919 | -3.9 (0.8) | -3.8 [-5.6, -2.7] | 1.000 | 0/20 | 20/20 |
| order-3 chain | Markov-1 | 20 x 1000 | 0.935 | 0.824 | +16.7 (0.8) | +16.8 [+15.4, +17.8] | 0.001 | 20/20 | 0/20 |
| order-3 chain | Markov-2 | 20 x 1000 | 0.935 | 0.919 | +5.0 (0.8) | +5.0 [+3.5, +6.6] | 0.001 | 20/20 | 0/20 |
| order-4 chain | Markov-1 | 20 x 1000 | 0.933 | 0.826 | +16.4 (0.7) | +16.4 [+15.1, +17.8] | 0.001 | 20/20 | 0/20 |
| order-4 chain | Markov-2 | 20 x 1000 | 0.933 | 0.920 | +4.2 (1.2) | +4.3 [+1.5, +6.2] | 0.001 | 19/20 | 0/20 |
| order-2 chain per recording | Markov-1 | 20 x 1000 | 0.925 | 0.825 | +15.3 (0.5) | +15.3 [+14.4, +16.1] | 0.001 | 20/20 | 0/20 |
| order-2 chain per recording | Markov-2 | 20 x 1000 | 0.925 | 0.918 | +2.1 (0.6) | +2.0 [+0.7, +3.3] | 0.015 | 16/20 | 0/20 |
| order-3 chain per recording | Markov-1 | 20 x 1000 | 0.936 | 0.824 | +16.7 (0.7) | +16.8 [+14.9, +17.8] | 0.001 | 20/20 | 0/20 |
| order-3 chain per recording | Markov-2 | 20 x 1000 | 0.936 | 0.919 | +5.4 (0.9) | +5.4 [+3.9, +7.0] | 0.001 | 20/20 | 0/20 |
| **real song** (README section 4) | Markov-1 | 1 x 1000 | 0.916 | 0.821 | +14.1 | | 0.001 | | |
| **real song** (README section 4) | Markov-2 | 1 x 1000 | 0.916 | 0.907 | +2.5 | | 0.005 | | |

## Held-out order choice

pooled bits per element by order: 0: 5.149, 1: 3.950, 2: 3.369, 3: 3.328, 4: 3.419; best order per group: [2, 2, 3, 2, 3, 3, 2, 3]; unseen order-2 contexts 6.0%

## Recording differences

- order-1 chain: 3.937–3.970 bits, 2.7–3.0% unseen
- order-2 chain: 2.498–2.534 bits, 2.7–3.1% unseen
- order-3 chain: 2.502–2.572 bits, 2.8–3.3% unseen
- order-4 chain: 2.511–2.592 bits, 2.7–3.4% unseen
- order-2 chain per recording: 3.612–3.676 bits, 8.4–9.0% unseen
- order-3 chain per recording: 3.604–3.706 bits, 8.4–9.3% unseen

## Copying

order-2 chain 1.0%, order-3 chain 6.4%, order-2 chain per recording 15.6%, order-3 chain per recording 56.9%

## TP cuts vs word boundaries

- ratio 0.5 (main): precision 0.667 (chance 0.346), recall 0.627, cuts 14896
- ratio 0.25: precision 0.752 (chance 0.346), recall 0.420, cuts 8840
- ratio 0.75: precision 0.601 (chance 0.346), recall 0.741, cuts 19537
- trigram TPs: precision 0.745 (chance 0.346), recall 0.683, cuts 14526
- backward TPs: precision 0.608 (chance 0.346), recall 0.544, cuts 14155
