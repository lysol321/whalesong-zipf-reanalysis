## Table 1. Held-out cross-entropy, bits per element (interpolated Witten-Bell, leave-one-recording-out)

| year | recordings | elements | order 0 | order 1 | order 2 | order 3 | order 4 | best | unseen order-2 contexts |
|---|---|---|---|---|---|---|---|---|---|
| 2010 | 4 | 1053 | 5.079 | 4.326 | **4.203** | 4.252 | 4.377 | 2 | 29.9% |
| 2011 | 6 | 2028 | 4.765 | 3.808 | **3.531** | 3.615 | 3.735 | 2 | 19.4% |
| 2012 | 6 | 3351 | 4.711 | 2.869 | **2.740** | 2.846 | 2.908 | 2 | 12.1% |
| 2013 | 6 | 2664 | 4.689 | 3.228 | 2.938 | **2.920** | 3.036 | 3 | 14.0% |
| 2014 | 7 | 5765 | 5.110 | 3.264 | **2.963** | 2.997 | 3.128 | 2 | 9.2% |
| 2015 | 13 | 14429 | 3.891 | 2.215 | **1.913** | 1.916 | 1.969 | 2 | 4.0% |
| 2016 | 6 | 7282 | 5.314 | 3.870 | **3.599** | 3.636 | 3.728 | 2 | 16.3% |
| 2017 | 7 | 9177 | 4.925 | 3.274 | **3.003** | 3.100 | 3.277 | 2 | 8.4% |
| **pooled** | 55 | 45749 | 4.651 | 3.049 | **2.777** | 2.819 | 2.922 | 2 | 9.9% |

Unseen held-out contexts, pooled, by order: order 1: 1.7%, order 2: 9.9%, order 3: 20.9%, order 4: 31.5%

## Table 2. Synthetic negative control (main pipeline; z and one-sided p as for real song)

| ground truth | null | datasets x N | synthetic 'real' R^2 mean | null R^2 mean | z mean (sd) | z median [min, max] | p median | datasets p <= 0.05 | datasets p >= 0.95 |
|---|---|---|---|---|---|---|---|---|---|
| order-1 chain | Markov-1 | 20 x 1000 | 0.902 | 0.905 | -0.7 (1.0) | -0.6 [-3.9, +1.1] | 0.717 | 0/20 | 2/20 |
| order-1 chain | Markov-2 | 20 x 1000 | 0.902 | 0.916 | -3.4 (1.2) | -3.1 [-7.4, -1.5] | 0.998 | 0/20 | 19/20 |
| order-2 chain | Markov-1 | 20 x 1000 | 0.939 | 0.905 | +6.8 (0.9) | +6.7 [+4.7, +8.5] | 0.001 | 20/20 | 0/20 |
| order-2 chain | Markov-2 | 20 x 1000 | 0.939 | 0.945 | -1.5 (0.7) | -1.8 [-3.1, +0.1] | 0.953 | 0/20 | 12/20 |
| order-3 chain | Markov-1 | 20 x 1000 | 0.951 | 0.904 | +8.6 (1.3) | +8.7 [+5.9, +10.4] | 0.001 | 20/20 | 0/20 |
| order-3 chain | Markov-2 | 20 x 1000 | 0.951 | 0.943 | +1.8 (0.6) | +1.7 [+0.9, +2.9] | 0.020 | 16/20 | 0/20 |
| **real song** (README section 4) | Markov-1 | 1 x 1000 | 0.930 | 0.900 | +6.0 | | 0.001 | | |
| **real song** (README section 4) | Markov-2 | 1 x 1000 | 0.930 | 0.939 | -2.1 | | 0.974 | | |

## Table 3a. Synthetic negative control, forward TPs, ratio 0.25 (same synthetic datasets and surrogates as Table 2)

| ground truth | null | datasets x N | synthetic 'real' R^2 mean | null R^2 mean | z mean (sd) | z median [min, max] | p median | datasets p <= 0.05 | datasets p >= 0.95 |
|---|---|---|---|---|---|---|---|---|---|
| order-1 chain | Markov-1 | 20 x 1000 | 0.695 | 0.701 | -0.4 (1.0) | -0.4 [-2.6, +1.4] | 0.654 | 0/20 | 1/20 |
| order-1 chain | Markov-2 | 20 x 1000 | 0.695 | 0.726 | -2.2 (0.9) | -2.0 [-4.2, -0.4] | 0.972 | 0/20 | 15/20 |
| order-2 chain | Markov-1 | 20 x 1000 | 0.797 | 0.702 | +6.6 (0.8) | +6.8 [+5.0, +8.0] | 0.001 | 20/20 | 0/20 |
| order-2 chain | Markov-2 | 20 x 1000 | 0.797 | 0.814 | -1.3 (0.7) | -1.3 [-2.6, +0.0] | 0.891 | 0/20 | 6/20 |
| order-3 chain | Markov-1 | 20 x 1000 | 0.856 | 0.696 | +10.1 (1.4) | +9.7 [+7.5, +12.4] | 0.001 | 20/20 | 0/20 |
| order-3 chain | Markov-2 | 20 x 1000 | 0.856 | 0.809 | +3.3 (0.9) | +3.3 [+2.0, +4.8] | 0.001 | 20/20 | 0/20 |
| **real song** (README section 4) | Markov-1 | 1 x 1000 | 0.832 | 0.695 | +9.5 | | 0.001 | | |
| **real song** (README section 4) | Markov-2 | 1 x 1000 | 0.832 | 0.796 | +2.6 | | 0.002 | | |

## Table 3b. Synthetic negative control, forward TPs, ratio 0.75 (same synthetic datasets and surrogates as Table 2)

| ground truth | null | datasets x N | synthetic 'real' R^2 mean | null R^2 mean | z mean (sd) | z median [min, max] | p median | datasets p <= 0.05 | datasets p >= 0.95 |
|---|---|---|---|---|---|---|---|---|---|
| order-1 chain | Markov-1 | 20 x 1000 | 0.949 | 0.952 | -1.4 (0.5) | -1.3 [-2.6, -0.4] | 0.904 | 0/20 | 4/20 |
| order-1 chain | Markov-2 | 20 x 1000 | 0.949 | 0.956 | -3.7 (0.6) | -3.7 [-4.9, -2.7] | 1.000 | 0/20 | 20/20 |
| order-2 chain | Markov-1 | 20 x 1000 | 0.963 | 0.952 | +4.7 (1.4) | +5.1 [+0.5, +6.4] | 0.001 | 19/20 | 0/20 |
| order-2 chain | Markov-2 | 20 x 1000 | 0.963 | 0.962 | +0.4 (0.7) | +0.5 [-1.3, +1.4] | 0.313 | 0/20 | 0/20 |
| order-3 chain | Markov-1 | 20 x 1000 | 0.964 | 0.953 | +4.9 (1.5) | +5.0 [+1.6, +8.0] | 0.001 | 20/20 | 0/20 |
| order-3 chain | Markov-2 | 20 x 1000 | 0.964 | 0.961 | +1.0 (0.8) | +0.8 [-0.3, +2.6] | 0.237 | 4/20 | 0/20 |
| **real song** (README section 4) | Markov-1 | 1 x 1000 | 0.953 | 0.949 | +1.8 | | 0.027 | | |
| **real song** (README section 4) | Markov-2 | 1 x 1000 | 0.953 | 0.962 | -3.8 | | 0.998 | | |

## Table 3c. Synthetic negative control, trigram TPs, ratio 0.5 (same synthetic datasets and surrogates as Table 2)

| ground truth | null | datasets x N | synthetic 'real' R^2 mean | null R^2 mean | z mean (sd) | z median [min, max] | p median | datasets p <= 0.05 | datasets p >= 0.95 |
|---|---|---|---|---|---|---|---|---|---|
| order-1 chain | Markov-1 | 20 x 1000 | 0.885 | 0.890 | -1.0 (1.1) | -0.7 [-4.0, +0.9] | 0.775 | 0/20 | 5/20 |
| order-1 chain | Markov-2 | 20 x 1000 | 0.885 | 0.902 | -3.2 (0.9) | -3.2 [-5.7, -1.8] | 0.997 | 0/20 | 20/20 |
| order-2 chain | Markov-1 | 20 x 1000 | 0.918 | 0.891 | +4.8 (0.9) | +5.0 [+3.4, +6.1] | 0.001 | 20/20 | 0/20 |
| order-2 chain | Markov-2 | 20 x 1000 | 0.918 | 0.924 | -1.1 (0.8) | -0.9 [-2.5, +0.4] | 0.823 | 0/20 | 5/20 |
| order-3 chain | Markov-1 | 20 x 1000 | 0.937 | 0.890 | +7.4 (1.5) | +8.2 [+3.9, +9.1] | 0.001 | 20/20 | 0/20 |
| order-3 chain | Markov-2 | 20 x 1000 | 0.937 | 0.921 | +2.3 (0.8) | +2.6 [+0.2, +3.5] | 0.001 | 16/20 | 0/20 |
| **real song** (README section 4) | Markov-1 | 1 x 1000 | 0.925 | 0.885 | +7.2 | | 0.001 | | |
| **real song** (README section 4) | Markov-2 | 1 x 1000 | 0.925 | 0.918 | +1.4 | | 0.066 | | |

## Table 3d. Synthetic negative control, backward TPs, ratio 0.5 (same synthetic datasets and surrogates as Table 2)

| ground truth | null | datasets x N | synthetic 'real' R^2 mean | null R^2 mean | z mean (sd) | z median [min, max] | p median | datasets p <= 0.05 | datasets p >= 0.95 |
|---|---|---|---|---|---|---|---|---|---|
| order-1 chain | Markov-1 | 20 x 1000 | 0.896 | 0.898 | -0.5 (0.7) | -0.6 [-1.3, +1.1] | 0.736 | 0/20 | 0/20 |
| order-1 chain | Markov-2 | 20 x 1000 | 0.896 | 0.910 | -2.9 (0.7) | -3.0 [-3.8, -1.3] | 0.996 | 0/20 | 19/20 |
| order-2 chain | Markov-1 | 20 x 1000 | 0.939 | 0.901 | +7.2 (0.8) | +7.2 [+5.7, +8.5] | 0.001 | 20/20 | 0/20 |
| order-2 chain | Markov-2 | 20 x 1000 | 0.939 | 0.942 | -0.8 (0.8) | -0.9 [-2.3, +0.8] | 0.826 | 0/20 | 2/20 |
| order-3 chain | Markov-1 | 20 x 1000 | 0.949 | 0.898 | +8.4 (1.8) | +8.4 [+4.6, +10.7] | 0.001 | 20/20 | 0/20 |
| order-3 chain | Markov-2 | 20 x 1000 | 0.949 | 0.939 | +2.1 (0.9) | +2.0 [+0.3, +3.6] | 0.003 | 16/20 | 0/20 |
| **real song** (README section 4) | Markov-1 | 1 x 1000 | 0.941 | 0.896 | +8.8 | | 0.001 | | |
| **real song** (README section 4) | Markov-2 | 1 x 1000 | 0.941 | 0.938 | +0.8 | | 0.227 | | |

## Table 4a. All ground truths, forward TPs, ratio 0.5 (main) (adds an order-4 chain and per-recording order-2/3 chains)

| ground truth | null | datasets x N | synthetic 'real' R^2 mean | null R^2 mean | z mean (sd) | z median [min, max] | p median | datasets p <= 0.05 | datasets p >= 0.95 |
|---|---|---|---|---|---|---|---|---|---|
| order-1 chain | Markov-1 | 20 x 1000 | 0.902 | 0.905 | -0.7 (1.0) | -0.6 [-3.9, +1.1] | 0.717 | 0/20 | 2/20 |
| order-1 chain | Markov-2 | 20 x 1000 | 0.902 | 0.916 | -3.4 (1.2) | -3.1 [-7.4, -1.5] | 0.998 | 0/20 | 19/20 |
| order-2 chain | Markov-1 | 20 x 1000 | 0.939 | 0.905 | +6.8 (0.9) | +6.7 [+4.7, +8.5] | 0.001 | 20/20 | 0/20 |
| order-2 chain | Markov-2 | 20 x 1000 | 0.939 | 0.945 | -1.5 (0.7) | -1.8 [-3.1, +0.1] | 0.953 | 0/20 | 12/20 |
| order-3 chain | Markov-1 | 20 x 1000 | 0.951 | 0.904 | +8.6 (1.3) | +8.7 [+5.9, +10.4] | 0.001 | 20/20 | 0/20 |
| order-3 chain | Markov-2 | 20 x 1000 | 0.951 | 0.943 | +1.8 (0.6) | +1.7 [+0.9, +2.9] | 0.020 | 16/20 | 0/20 |
| order-4 chain | Markov-1 | 20 x 1000 | 0.955 | 0.906 | +9.1 (1.6) | +9.8 [+4.7, +11.5] | 0.001 | 20/20 | 0/20 |
| order-4 chain | Markov-2 | 20 x 1000 | 0.955 | 0.944 | +2.5 (0.9) | +2.7 [+0.9, +4.7] | 0.002 | 17/20 | 0/20 |
| order-2 chain per recording | Markov-1 | 20 x 1000 | 0.945 | 0.906 | +8.0 (1.0) | +8.2 [+5.6, +10.0] | 0.001 | 20/20 | 0/20 |
| order-2 chain per recording | Markov-2 | 20 x 1000 | 0.945 | 0.945 | +0.1 (0.8) | +0.2 [-2.0, +1.6] | 0.451 | 1/20 | 1/20 |
| order-3 chain per recording | Markov-1 | 20 x 1000 | 0.953 | 0.907 | +9.0 (0.9) | +9.1 [+7.4, +10.7] | 0.001 | 20/20 | 0/20 |
| order-3 chain per recording | Markov-2 | 20 x 1000 | 0.953 | 0.944 | +2.2 (0.7) | +2.3 [+0.9, +3.5] | 0.005 | 17/20 | 0/20 |
| **real song** (README section 4) | Markov-1 | 1 x 1000 | 0.930 | 0.900 | +6.0 | | 0.001 | | |
| **real song** (README section 4) | Markov-2 | 1 x 1000 | 0.930 | 0.939 | -2.1 | | 0.974 | | |

## Table 4b. All ground truths, forward TPs, ratio 0.25 (adds an order-4 chain and per-recording order-2/3 chains)

| ground truth | null | datasets x N | synthetic 'real' R^2 mean | null R^2 mean | z mean (sd) | z median [min, max] | p median | datasets p <= 0.05 | datasets p >= 0.95 |
|---|---|---|---|---|---|---|---|---|---|
| order-1 chain | Markov-1 | 20 x 1000 | 0.695 | 0.701 | -0.4 (1.0) | -0.4 [-2.6, +1.4] | 0.654 | 0/20 | 1/20 |
| order-1 chain | Markov-2 | 20 x 1000 | 0.695 | 0.726 | -2.2 (0.9) | -2.0 [-4.2, -0.4] | 0.972 | 0/20 | 15/20 |
| order-2 chain | Markov-1 | 20 x 1000 | 0.797 | 0.702 | +6.6 (0.8) | +6.8 [+5.0, +8.0] | 0.001 | 20/20 | 0/20 |
| order-2 chain | Markov-2 | 20 x 1000 | 0.797 | 0.814 | -1.3 (0.7) | -1.3 [-2.6, +0.0] | 0.891 | 0/20 | 6/20 |
| order-3 chain | Markov-1 | 20 x 1000 | 0.856 | 0.696 | +10.1 (1.4) | +9.7 [+7.5, +12.4] | 0.001 | 20/20 | 0/20 |
| order-3 chain | Markov-2 | 20 x 1000 | 0.856 | 0.809 | +3.3 (0.9) | +3.3 [+2.0, +4.8] | 0.001 | 20/20 | 0/20 |
| order-4 chain | Markov-1 | 20 x 1000 | 0.886 | 0.699 | +12.1 (1.3) | +12.0 [+8.4, +13.7] | 0.001 | 20/20 | 0/20 |
| order-4 chain | Markov-2 | 20 x 1000 | 0.886 | 0.812 | +5.5 (0.9) | +5.6 [+3.3, +7.4] | 0.001 | 20/20 | 0/20 |
| order-2 chain per recording | Markov-1 | 20 x 1000 | 0.828 | 0.701 | +8.5 (1.2) | +8.4 [+5.5, +10.4] | 0.001 | 20/20 | 0/20 |
| order-2 chain per recording | Markov-2 | 20 x 1000 | 0.828 | 0.813 | +1.1 (0.8) | +1.1 [-1.1, +2.6] | 0.123 | 5/20 | 0/20 |
| order-3 chain per recording | Markov-1 | 20 x 1000 | 0.876 | 0.699 | +11.4 (1.0) | +11.7 [+9.2, +12.9] | 0.001 | 20/20 | 0/20 |
| order-3 chain per recording | Markov-2 | 20 x 1000 | 0.876 | 0.811 | +4.7 (0.7) | +4.6 [+3.4, +6.4] | 0.001 | 20/20 | 0/20 |
| **real song** (README section 4) | Markov-1 | 1 x 1000 | 0.832 | 0.695 | +9.5 | | 0.001 | | |
| **real song** (README section 4) | Markov-2 | 1 x 1000 | 0.832 | 0.796 | +2.6 | | 0.002 | | |

## Table 4c. All ground truths, forward TPs, ratio 0.75 (adds an order-4 chain and per-recording order-2/3 chains)

| ground truth | null | datasets x N | synthetic 'real' R^2 mean | null R^2 mean | z mean (sd) | z median [min, max] | p median | datasets p <= 0.05 | datasets p >= 0.95 |
|---|---|---|---|---|---|---|---|---|---|
| order-1 chain | Markov-1 | 20 x 1000 | 0.949 | 0.952 | -1.4 (0.5) | -1.3 [-2.6, -0.4] | 0.904 | 0/20 | 4/20 |
| order-1 chain | Markov-2 | 20 x 1000 | 0.949 | 0.956 | -3.7 (0.6) | -3.7 [-4.9, -2.7] | 1.000 | 0/20 | 20/20 |
| order-2 chain | Markov-1 | 20 x 1000 | 0.963 | 0.952 | +4.7 (1.4) | +5.1 [+0.5, +6.4] | 0.001 | 19/20 | 0/20 |
| order-2 chain | Markov-2 | 20 x 1000 | 0.963 | 0.962 | +0.4 (0.7) | +0.5 [-1.3, +1.4] | 0.313 | 0/20 | 0/20 |
| order-3 chain | Markov-1 | 20 x 1000 | 0.964 | 0.953 | +4.9 (1.5) | +5.0 [+1.6, +8.0] | 0.001 | 20/20 | 0/20 |
| order-3 chain | Markov-2 | 20 x 1000 | 0.964 | 0.961 | +1.0 (0.8) | +0.8 [-0.3, +2.6] | 0.237 | 4/20 | 0/20 |
| order-4 chain | Markov-1 | 20 x 1000 | 0.962 | 0.952 | +4.0 (1.3) | +3.9 [+1.1, +6.1] | 0.001 | 19/20 | 0/20 |
| order-4 chain | Markov-2 | 20 x 1000 | 0.962 | 0.961 | +0.4 (0.8) | +0.5 [-1.1, +1.6] | 0.348 | 1/20 | 0/20 |
| order-2 chain per recording | Markov-1 | 20 x 1000 | 0.962 | 0.952 | +4.6 (1.0) | +4.7 [+2.4, +6.2] | 0.001 | 20/20 | 0/20 |
| order-2 chain per recording | Markov-2 | 20 x 1000 | 0.962 | 0.961 | +0.4 (0.7) | +0.6 [-1.2, +1.6] | 0.291 | 1/20 | 0/20 |
| order-3 chain per recording | Markov-1 | 20 x 1000 | 0.962 | 0.953 | +4.2 (1.1) | +4.1 [+2.7, +7.4] | 0.001 | 20/20 | 0/20 |
| order-3 chain per recording | Markov-2 | 20 x 1000 | 0.962 | 0.961 | +0.5 (0.8) | +0.5 [-1.1, +2.0] | 0.301 | 2/20 | 0/20 |
| **real song** (README section 4) | Markov-1 | 1 x 1000 | 0.953 | 0.949 | +1.8 | | 0.027 | | |
| **real song** (README section 4) | Markov-2 | 1 x 1000 | 0.953 | 0.962 | -3.8 | | 0.998 | | |

## Table 4d. All ground truths, trigram TPs, ratio 0.5 (adds an order-4 chain and per-recording order-2/3 chains)

| ground truth | null | datasets x N | synthetic 'real' R^2 mean | null R^2 mean | z mean (sd) | z median [min, max] | p median | datasets p <= 0.05 | datasets p >= 0.95 |
|---|---|---|---|---|---|---|---|---|---|
| order-1 chain | Markov-1 | 20 x 1000 | 0.885 | 0.890 | -1.0 (1.1) | -0.7 [-4.0, +0.9] | 0.775 | 0/20 | 5/20 |
| order-1 chain | Markov-2 | 20 x 1000 | 0.885 | 0.902 | -3.2 (0.9) | -3.2 [-5.7, -1.8] | 0.997 | 0/20 | 20/20 |
| order-2 chain | Markov-1 | 20 x 1000 | 0.918 | 0.891 | +4.8 (0.9) | +5.0 [+3.4, +6.1] | 0.001 | 20/20 | 0/20 |
| order-2 chain | Markov-2 | 20 x 1000 | 0.918 | 0.924 | -1.1 (0.8) | -0.9 [-2.5, +0.4] | 0.823 | 0/20 | 5/20 |
| order-3 chain | Markov-1 | 20 x 1000 | 0.937 | 0.890 | +7.4 (1.5) | +8.2 [+3.9, +9.1] | 0.001 | 20/20 | 0/20 |
| order-3 chain | Markov-2 | 20 x 1000 | 0.937 | 0.921 | +2.3 (0.8) | +2.6 [+0.2, +3.5] | 0.001 | 16/20 | 0/20 |
| order-4 chain | Markov-1 | 20 x 1000 | 0.944 | 0.891 | +8.5 (1.8) | +9.1 [+3.3, +10.9] | 0.001 | 20/20 | 0/20 |
| order-4 chain | Markov-2 | 20 x 1000 | 0.944 | 0.921 | +3.4 (0.8) | +3.5 [+1.5, +4.5] | 0.001 | 20/20 | 0/20 |
| order-2 chain per recording | Markov-1 | 20 x 1000 | 0.926 | 0.892 | +6.0 (0.8) | +6.0 [+4.6, +7.9] | 0.001 | 20/20 | 0/20 |
| order-2 chain per recording | Markov-2 | 20 x 1000 | 0.926 | 0.923 | +0.5 (0.6) | +0.5 [-0.5, +1.7] | 0.344 | 1/20 | 0/20 |
| order-3 chain per recording | Markov-1 | 20 x 1000 | 0.940 | 0.893 | +8.1 (0.9) | +8.2 [+6.5, +9.4] | 0.001 | 20/20 | 0/20 |
| order-3 chain per recording | Markov-2 | 20 x 1000 | 0.940 | 0.922 | +2.8 (0.7) | +2.9 [+0.9, +3.8] | 0.001 | 18/20 | 0/20 |
| **real song** (README section 4) | Markov-1 | 1 x 1000 | 0.925 | 0.885 | +7.2 | | 0.001 | | |
| **real song** (README section 4) | Markov-2 | 1 x 1000 | 0.925 | 0.918 | +1.4 | | 0.066 | | |

## Table 4e. All ground truths, backward TPs, ratio 0.5 (adds an order-4 chain and per-recording order-2/3 chains)

| ground truth | null | datasets x N | synthetic 'real' R^2 mean | null R^2 mean | z mean (sd) | z median [min, max] | p median | datasets p <= 0.05 | datasets p >= 0.95 |
|---|---|---|---|---|---|---|---|---|---|
| order-1 chain | Markov-1 | 20 x 1000 | 0.896 | 0.898 | -0.5 (0.7) | -0.6 [-1.3, +1.1] | 0.736 | 0/20 | 0/20 |
| order-1 chain | Markov-2 | 20 x 1000 | 0.896 | 0.910 | -2.9 (0.7) | -3.0 [-3.8, -1.3] | 0.996 | 0/20 | 19/20 |
| order-2 chain | Markov-1 | 20 x 1000 | 0.939 | 0.901 | +7.2 (0.8) | +7.2 [+5.7, +8.5] | 0.001 | 20/20 | 0/20 |
| order-2 chain | Markov-2 | 20 x 1000 | 0.939 | 0.942 | -0.8 (0.8) | -0.9 [-2.3, +0.8] | 0.826 | 0/20 | 2/20 |
| order-3 chain | Markov-1 | 20 x 1000 | 0.949 | 0.898 | +8.4 (1.8) | +8.4 [+4.6, +10.7] | 0.001 | 20/20 | 0/20 |
| order-3 chain | Markov-2 | 20 x 1000 | 0.949 | 0.939 | +2.1 (0.9) | +2.0 [+0.3, +3.6] | 0.003 | 16/20 | 0/20 |
| order-4 chain | Markov-1 | 20 x 1000 | 0.955 | 0.899 | +9.2 (1.9) | +9.5 [+4.7, +11.3] | 0.001 | 20/20 | 0/20 |
| order-4 chain | Markov-2 | 20 x 1000 | 0.955 | 0.941 | +3.2 (0.9) | +3.2 [+1.5, +4.8] | 0.001 | 20/20 | 0/20 |
| order-2 chain per recording | Markov-1 | 20 x 1000 | 0.944 | 0.900 | +7.8 (1.0) | +7.7 [+5.7, +9.6] | 0.001 | 20/20 | 0/20 |
| order-2 chain per recording | Markov-2 | 20 x 1000 | 0.944 | 0.942 | +0.3 (0.8) | +0.4 [-0.9, +1.7] | 0.350 | 1/20 | 0/20 |
| order-3 chain per recording | Markov-1 | 20 x 1000 | 0.953 | 0.902 | +8.8 (0.9) | +8.8 [+7.1, +10.8] | 0.001 | 20/20 | 0/20 |
| order-3 chain per recording | Markov-2 | 20 x 1000 | 0.953 | 0.942 | +2.5 (0.5) | +2.5 [+1.5, +3.5] | 0.001 | 20/20 | 0/20 |
| **real song** (README section 4) | Markov-1 | 1 x 1000 | 0.941 | 0.896 | +8.8 | | 0.001 | | |
| **real song** (README section 4) | Markov-2 | 1 x 1000 | 0.941 | 0.938 | +0.8 | | 0.227 | | |

## Table 5. Between-recording differences: leave-one-recording-out order-2 cross-entropy (bits per element) and share of held-out order-2 contexts unseen in the other recordings, pooled over years

| data | datasets | cross-entropy mean [min, max] | unseen contexts mean [min, max] |
|---|---|---|---|
| **real song** (Table 1) | 1 | 2.777 | 9.9% |
| order-1 chain | 20 | 2.381 [2.344, 2.416] | 1.8% [1.7, 1.9] |
| order-2 chain | 20 | 1.645 [1.610, 1.686] | 2.1% [1.8, 2.4] |
| order-3 chain | 20 | 1.708 [1.662, 1.810] | 2.6% [2.2, 3.4] |
| order-4 chain | 20 | 1.738 [1.663, 1.850] | 3.0% [2.3, 4.0] |
| order-2 chain per recording | 20 | 2.956 [2.797, 3.115] | 11.7% [10.8, 13.2] |
| order-3 chain per recording | 20 | 2.964 [2.781, 3.092] | 11.8% [10.9, 12.7] |
