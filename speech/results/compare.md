# Whale song vs child-directed speech (phonemes A, B; syllables SA, SB) under the same calibration

Samples A, B are phonemes; SA, SB syllables. Cell: real z's distance from the truth's mean z in that truth's SD, Markov-1 / Markov-2; * = inside the [min, max] band on both nulls.

## two-back per year

| pipeline | whale | phonemes A | phonemes B | syllables SA | syllables SB |
|---|---|---|---|---|---|
| ratio 0.5 (main) | -1.0 / -0.8 * | -0.4 / +2.9 | -0.6 / +2.8 | -33.0 / -95.6 | -24.6 / -89.8 |
| ratio 0.25 | +3.5 / +5.6 | +4.4 / +6.7 | +3.3 / +6.2 | -13.7 / -20.8 | -15.6 / -28.1 |
| ratio 0.75 | -2.1 / -6.1 | -3.0 / -9.0 | -3.5 / -16.7 | -33.7 / -123.0 | -32.0 / -132.1 |
| trigram TPs | +2.7 / +3.2 | +0.8 / +5.5 | +3.2 / +5.6 | -7.6 / -9.0 | -8.0 / -10.3 |
| backward TPs | +2.0 / +2.1 | +0.8 / +3.2 | +2.7 / +7.9 | -19.0 / -47.9 | -25.9 / -58.1 |

## three-back per year

| pipeline | whale | phonemes A | phonemes B | syllables SA | syllables SB |
|---|---|---|---|---|---|
| ratio 0.5 (main) | -1.9 / -6.8 | -10.6 / -10.0 | -5.7 / -5.8 | -34.3 / -78.7 | -29.8 / -112.0 |
| ratio 0.25 | -0.4 / -0.7 * | -6.9 / -7.8 | -6.4 / -4.7 | -21.4 / -50.5 | -16.2 / -41.6 |
| ratio 0.75 | -2.1 / -5.9 | -1.4 / -6.9 | -0.5 / -10.8 | -24.9 / -92.4 | -34.7 / -128.5 |
| trigram TPs | -0.2 / -1.1 * | -6.0 / -8.0 | -1.7 / -3.1 | -18.9 / -44.6 | -16.6 / -20.7 |
| backward TPs | +0.2 / -1.5 * | -6.6 / -11.1 | -3.4 / -3.1 | -24.4 / -41.6 | -21.6 / -52.2 |

## two-back per recording

| pipeline | whale | phonemes A | phonemes B | syllables SA | syllables SB |
|---|---|---|---|---|---|
| ratio 0.5 (main) | -2.0 / -2.6 | -7.9 / -6.3 | -4.1 / -3.3 | -11.7 / -77.2 | -29.7 / -103.6 |
| ratio 0.25 | +0.8 / +1.9 | -1.0 / +0.7 * | -1.4 / -0.1 * | -15.4 / -25.4 | -14.5 / -30.5 |
| ratio 0.75 | -2.8 / -5.7 | -4.3 / -9.6 | -2.8 / -12.1 | -19.2 / -97.8 | -35.9 / -117.5 |
| trigram TPs | +1.5 / +1.7 * | -3.2 / -1.2 | +0.3 / +0.8 * | -5.3 / -20.5 | -16.7 / -26.3 |
| backward TPs | +1.1 / +0.5 * | -2.5 / -2.0 | -2.7 / +0.8 | -6.3 / -33.5 | -27.3 / -81.1 |

## Real z (Markov-1 / Markov-2)

| pipeline | whale | phonemes A | phonemes B | syllables SA | syllables SB |
|---|---|---|---|---|---|
| ratio 0.5 (main) | +6.0 / -2.1 | +13.3 / -2.3 | +12.6 / -1.4 | -7.8 / -47.3 | -10.4 / -57.1 |
| ratio 0.25 | +9.5 / +2.6 | +12.6 / +3.4 | +11.0 / +2.3 | +0.7 / -22.8 | +1.2 / -19.2 |
| ratio 0.75 | +1.8 / -3.8 | +10.6 / -4.1 | +8.3 / -5.4 | -19.3 / -42.7 | -24.3 / -51.9 |
| trigram TPs | +7.2 / +1.4 | +15.6 / +1.4 | +16.7 / +2.5 | +0.6 / -15.6 | +1.4 / -14.2 |
| backward TPs | +8.8 / +0.8 | +12.7 / -0.2 | +14.1 / +2.5 | -1.5 / -30.5 | -2.9 / -38.7 |
