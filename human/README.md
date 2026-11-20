# Human check: Simon-game sequences through the same nulls

This is the human comparison I mentioned. Rather than natural language, I used your own culturally evolved human
sequences: the "Simon game" data from Arnon & Kirby (2024), *Cultural evolution creates the statistical structure
of language*, Sci. Rep. 14:5255 (ref. 19 in the whale paper). The data is in
github.com/smkirby/cultural_evolution_of_statistical_structure (`simon_game_data.csv`). It isn't included here,
since the repo has no license file; put it in `download/` to rerun.

## The short version

- **Reproduced:** cut ratio 0.425 and R² rising 0.022 per generation, matching the paper (β = 0.022).
- **Bigram (Markov-1) null:** the sequences beat it from generation 1 on (all generations z = 11.6). Random
  generation 0 doesn't beat it (z = +0.6), which is the built-in sanity check.
- **Trigram (Markov-2) null:** it "matches" them, as it does for whale song (all generations z = −0.1;
  generations 8–10 z = +1.4, p = 0.07).
- **Calibration:** against fake sequences of known memory, the culturally evolved ones look **three-back**. Early
  generations are ambiguous between two- and three-back; late ones are clearly three-back.
- **What it means:** the calibration picks up longer memory in human-made sequences even when the raw trigram
  null seems to match. So a raw Markov-2 match isn't evidence against structure on its own, for these sequences
  or for whale song.

## Results

**Nulls** (mean per-set R², null mean and z; full table in `results/tables.md`):

| | gen 0 (random) | gens 1–3 | gens 8–10 | gens 1–10 |
|---|---|---|---|---|
| real | 0.311 | 0.593 | 0.744 | 0.669 |
| shuffle | 0.296, z +0.3 | 0.256, z +10.6 | 0.293, z +14.8 | 0.280, z +22.6 |
| Markov-1 | 0.277, z +0.6 | 0.436, z +5.2 | 0.549, z +7.1 | 0.497, z +11.6 |
| Markov-2 | 0.453, z −2.8 | 0.621, z −1.2 | 0.717, z +1.4 | 0.671, z −0.1 |
| Markov-2, leave-one-sequence-out | 0.450, z −2.5 | 0.618, z −1.1 | 0.717, z +1.5 | 0.670, z −0.1 |

At random generation 0, the trigram null is *more* Zipfian than the data (z −2.8). That's the small-data
effect again.

**Calibration** (z against bands of 20 fake datasets per memory length; Markov-1 / Markov-2):

| | real | one-back | two-back | three-back | looks like |
|---|---|---|---|---|---|
| gens 1–3 | +5.2 / −1.2 | [−2.6, +0.5] / [−5.5, −2.7] | [+4.1, +7.1] / [−3.3, +0.0] | [+4.9, +7.9] / [−3.0, +1.1] | two- or three-back |
| gens 8–10 | +7.1 / +1.4 | [−2.2, +1.3] / [−4.3, −1.5] | [+3.6, +6.9] / [−4.0, +0.3] | [+5.7, +8.0] / [−1.4, +1.5] | three-back (above every two-back dataset on both) |
| gens 1–10 | +11.6 / −0.1 | [−3.6, +0.3] / [−8.6, −4.5] | [+7.1, +11.2] / [−6.6, −1.6] | [+10.2, +13.7] / [−2.7, +1.7] | three-back (above every two-back dataset on both) |

**Held-out prediction, gens 8–10:** two and three back predict about equally well (1.759 vs 1.765 bits; each wins
7 of 18 sets).

**Are the fakes realistic?** Real sequences within a set are a bit less predictable from each other than the fake
ones (1.76 vs 1.68–1.73 bits). It's a small gap, like the finch, and nothing like the whale's 1-bit gap.

## Things to keep in mind

- This isn't natural language. It's short sequences (7–26 lights) over 4 colours, and they can't be matched to
  whale size, so it shows what the test can detect, not a size-matched comparison.
- Your pipeline here uses trigram TPs at a 0.425 cut. The closest whale run is the trigram-TP pipeline, where
  whale song also looked three-back against one-chain-per-year fakes, before allowing for recording differences.
- A small quirk in the notebook: the threshold function divides each TP by the sequence's *first* TP (`last_tp`
  is never updated), while the cut rule uses the previous TP. The consistent version gives 0.441 instead of 0.425,
  which barely changes anything (late R² 0.77 vs 0.74).

## Rerun

From `whalesong/human/`, with `download/simon_game_data.csv` in place. The nulls take about 15 min and each
calibration truth about 2 h, all at idle priority:

```bash
python -I run_human.py download/simon_game_data.csv real && for n in shuffle markov1 markov2 markov2cv; do python -I run_human.py download/simon_game_data.csv null $n 1000; done && for t in 1 2 3; do python -I run_human.py download/simon_game_data.csv ncv $t; done && python -I run_human.py download/simon_game_data.csv report
```
