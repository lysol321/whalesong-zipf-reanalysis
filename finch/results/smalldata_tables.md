## Table F1. Held-out cross-entropy, bits per syllable (interpolated Witten-Bell, leave-one-bout-out within each of the 30 recordings), pooled

| | order 0 | order 1 | order 2 | order 3 | order 4 |
|---|---|---|---|---|---|
| pooled | 2.877 | 1.148 | 0.732 | 0.702 | 0.745 |
| recordings where this order is best | 0 | 0 | 16 | 10 | 4 |

Unseen held-out contexts, pooled, by order: order 1: 0.0%, order 2: 0.9%, order 3: 2.6%, order 4: 5.3%

## Table F2a. Synthetic negative control, ratio 0.5 (main)

| ground truth | null | datasets x N | synthetic 'real' R^2 mean | null R^2 mean | z mean (sd) | z median [min, max] | p median | datasets p <= 0.05 | datasets p >= 0.95 |
|---|---|---|---|---|---|---|---|---|---|
| order-1 chain | Markov-1 | 20 x 1000 | 0.807 | 0.809 | -0.1 (0.7) | -0.1 [-1.5, +1.1] | 0.558 | 0/20 | 0/20 |
| order-1 chain | Markov-2 | 20 x 1000 | 0.807 | 0.815 | -0.6 (0.7) | -0.7 [-1.7, +1.2] | 0.744 | 0/20 | 0/20 |
| order-2 chain | Markov-1 | 20 x 1000 | 0.877 | 0.801 | +5.7 (0.4) | +5.7 [+4.8, +6.5] | 0.001 | 20/20 | 0/20 |
| order-2 chain | Markov-2 | 20 x 1000 | 0.877 | 0.880 | -0.4 (0.5) | -0.3 [-1.6, +0.5] | 0.643 | 0/20 | 0/20 |
| order-3 chain | Markov-1 | 20 x 1000 | 0.897 | 0.804 | +7.0 (0.5) | +6.9 [+6.2, +8.3] | 0.001 | 20/20 | 0/20 |
| order-3 chain | Markov-2 | 20 x 1000 | 0.897 | 0.883 | +1.7 (0.7) | +1.5 [-0.2, +3.0] | 0.050 | 10/20 | 0/20 |
| **real song** (README section 4) | Markov-1 | 1 x 1000 | 0.889 | 0.804 | +6.6 | | 0.001 | | |
| **real song** (README section 4) | Markov-2 | 1 x 1000 | 0.889 | 0.878 | +1.2 | | 0.116 | | |

## Table F2b. Synthetic negative control, ratio 0.3

| ground truth | null | datasets x N | synthetic 'real' R^2 mean | null R^2 mean | z mean (sd) | z median [min, max] | p median | datasets p <= 0.05 | datasets p >= 0.95 |
|---|---|---|---|---|---|---|---|---|---|
| order-1 chain | Markov-1 | 20 x 1000 | 0.537 | 0.541 | -0.2 (0.8) | -0.1 [-1.4, +1.0] | 0.550 | 0/20 | 0/20 |
| order-1 chain | Markov-2 | 20 x 1000 | 0.537 | 0.551 | -0.6 (0.8) | -0.6 [-2.0, +0.5] | 0.746 | 0/20 | 1/20 |
| order-2 chain | Markov-1 | 20 x 1000 | 0.728 | 0.534 | +7.9 (0.9) | +8.0 [+6.6, +9.7] | 0.001 | 20/20 | 0/20 |
| order-2 chain | Markov-2 | 20 x 1000 | 0.728 | 0.732 | -0.2 (0.7) | -0.2 [-1.5, +1.4] | 0.589 | 0/20 | 0/20 |
| order-3 chain | Markov-1 | 20 x 1000 | 0.768 | 0.537 | +9.3 (0.7) | +9.2 [+8.2, +10.8] | 0.001 | 20/20 | 0/20 |
| order-3 chain | Markov-2 | 20 x 1000 | 0.768 | 0.733 | +1.6 (0.6) | +1.7 [+0.5, +3.1] | 0.043 | 11/20 | 0/20 |
| **real song** (README section 4) | Markov-1 | 1 x 1000 | 0.751 | 0.534 | +8.9 | | 0.001 | | |
| **real song** (README section 4) | Markov-2 | 1 x 1000 | 0.751 | 0.722 | +1.3 | | 0.102 | | |

## Table F2c. Synthetic negative control, ratio 0.7

| ground truth | null | datasets x N | synthetic 'real' R^2 mean | null R^2 mean | z mean (sd) | z median [min, max] | p median | datasets p <= 0.05 | datasets p >= 0.95 |
|---|---|---|---|---|---|---|---|---|---|
| order-1 chain | Markov-1 | 20 x 1000 | 0.888 | 0.892 | -0.5 (0.6) | -0.5 [-1.7, +0.6] | 0.682 | 0/20 | 0/20 |
| order-1 chain | Markov-2 | 20 x 1000 | 0.888 | 0.893 | -0.6 (0.5) | -0.5 [-1.7, +0.6] | 0.710 | 0/20 | 1/20 |
| order-2 chain | Markov-1 | 20 x 1000 | 0.908 | 0.886 | +2.4 (0.6) | +2.4 [+1.0, +3.9] | 0.005 | 19/20 | 0/20 |
| order-2 chain | Markov-2 | 20 x 1000 | 0.908 | 0.904 | +0.7 (0.7) | +0.7 [-0.8, +2.7] | 0.245 | 1/20 | 0/20 |
| order-3 chain | Markov-1 | 20 x 1000 | 0.910 | 0.885 | +2.8 (0.4) | +2.8 [+2.2, +4.0] | 0.002 | 20/20 | 0/20 |
| order-3 chain | Markov-2 | 20 x 1000 | 0.910 | 0.905 | +1.0 (0.7) | +1.0 [-0.2, +2.5] | 0.160 | 2/20 | 0/20 |
| **real song** (README section 4) | Markov-1 | 1 x 1000 | 0.899 | 0.886 | +1.5 | | 0.065 | | |
| **real song** (README section 4) | Markov-2 | 1 x 1000 | 0.899 | 0.907 | -1.5 | | 0.926 | | |
