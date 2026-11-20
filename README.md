# Whale song, Zipf's law and a Markov null

Hi! I'm not a specialist, just someone who reads papers on the weekend and got curious about Arnon, Kirby, Allen, Garrigue, Carroll & Garland
(2025), *Whale song shows language-like statistical structure*, Science 387:649 (doi:10.1126/science.adq7055). I
reran it with help from an AI assistant (Claude), using your data (Data S2) and a rewrite of your pipeline from
Code S1 v2. I did the same for the Bengalese finch paper; that's in `finch/README.md`.

## The short version

- **Everything reproduced exactly** (main R² 0.930289; post-erratum brevity slope −0.1197).
- **Real song beats shuffle, rotation and a bigram (Markov-1) null** (z = 6.0), same as your finch result.
- **A trigram (Markov-2) null matches real song on the main pipeline** (z = −2.1). That holds even when each
  recording's chain is fitted without that recording (z = −1.9). Real song only pulls ahead at ratio 0.25
  (z = 2.6). A smoothed trigram null loses (z = 3.0), but smoothing can itself inflate z, and I didn't
  test that.
- **Brevity: real song shows it, but the nulls show more.** Rotation is the fairest comparison, since it's the only
  null that keeps chunk lengths.
  - On Kendall τ, rotation shows more brevity than real song on all 5 pipelines.
  - On the corrected slope it does on 3 of 5, and only just on the main one (−0.128 vs −0.120).
  - The other nulls make far more chunk types (shuffle about 9,100 vs 3,386), which steepens their slopes on its
    own.
  - At ratio 0.25 (shuffle and rotation) and on trigram TPs (rotation), real song is steeper. Rotation at 0.25 is
    my run; you only ran rotation at 0.5.
- **Power law:** α ≈ 2.0, but the bootstrap test rejects it in 3 of 8 years. A lognormal fits better everywhere,
  but it does for the nulls too, so that doesn't say much.
- **The small-data question.** A refitted trigram model looks too Zipfian on small data.
  It does, usually (4 of 5 pipelines, even against fake song that really is trigram). So I made fake song from
  chains with a known memory (1 to 4 sounds back), at the real data's size, and checked where real song's
  z-scores land:
  - Main pipeline: real song looks two-back. At ratio 0.25 and with trigram or backward TPs it looks more like
    three-back.
  - Recordings from the same year differ from each other a lot more than my fake ones did. That's not surprising,
    since the song shifts through a season. Fake song built per recording gets closest, but nothing matches on
    every pipeline.
  - Per-recording chains also copy long stretches of the song, so I can't tell "recordings differ" from "longer
    memory".
  - Whatever it is, real song scores below a four-back chain on the trigram null on every pipeline (at this data
    size).
- **Where I landed.** This backs up your point that the Zipf fit reflects sequential structure beyond bigrams.
  What it can't do is tell the song apart from a two- or three-back chain fitted to it. Since the 0.5 cut only
  looks at three sounds in a row, a trigram null keeps that cue anyway.
- **Human checks.**
  - **Simon-game sequences** (`human/README.md`): a raw trigram null "matches" them too, but the calibration says
    the evolved generations look three-back. So a raw Markov-2 match isn't evidence against structure on its own.
  - **Child-directed speech** (`speech/README.md`): phonemes from CHILDES, cut to exactly the whale data's size
    and layout. It looks just like whale song on this statistic:
    - it beats the same nulls and is matched by the raw trigram null on the main pipeline (z −2.3 and −1.4 vs
      whale −2.1);
    - under calibration it lands in the same place, between two- and three-back, with nothing fitting at 0.75.

    So at this size the statistic can't tell whale song from human speech. Whale song looks about as
    "language-like" as speech here, but the statistic can't show more than short-range structure in either.
  - **Same speech as syllables** (second corpus, about 1,600 syllable types vs the whale's 239): real speech
    *fails* even the bigram null (z −7.8 and −10.4). Chains fitted to it, even one-back, make more Zipfian chunks
    than it does, and the calibration can't place it.

    So whether real language "beats a Markov null" here depends on the unit, and it isn't a reliable marker of
    language-likeness either way.

## How I did it

- **Pipeline (same as Code S1).** TPs per year; cut when TP[j] < ratio × TP[j−1]; per-year R² of log count vs
  log rank, averaged. Ratio 0.5 is the main run; I also did 0.25, 0.75, trigram TPs and backward TPs. Brevity:
  the corrected Poisson slope, plus Kendall τ, which I added.
- **Nulls.** 1000 fake datasets each, every one through the identical pipeline:
  - shuffle and rotate (yours);
  - Markov-1 and Markov-2 fitted per year;
  - Markov-2 fitted leave-one-recording-out;
  - a Witten-Bell smoothed Markov-2;
  - a repeat-skeleton null (keeps where and how often units repeat, fills them with Markov-1 content).
- **Calibration.** Fake song from a chain of known order fitted to the real song, with the real recording counts,
  lengths and start sounds. 20 fake datasets per chain, each run against the same Markov-1 and Markov-2 nulls as
  real song. The spread of those 20 z-scores is the chain's "band".
- **Hide-one-out.** Train on all recordings but one and predict the one left out. Looking two sounds back works
  best in 7 of 8 years. Longer contexts are thin at this data size.

## Results

**Reproduction.**

| | Paper / Code S1 | Mine |
|---|---|---|
| R², main / trigram TPs / backward TPs | 0.9303 / 0.9255 / 0.9406 | 0.9303 / 0.9255 / 0.9406 |
| Brevity slope (post-erratum), main / trigram / backward | −0.1197 / −0.0972 / −0.1015 | same |
| Sub-sequence types, main | 3386 | 3386 |
| Shuffle z / rotation z, main | 23.09 / 14.43 | 22.7 / 13.9 |

The erratum withdrew the original brevity result (R² 0.62); the corrected test didn't get baselines.

**Nulls: R² of the rank-frequency fit** (null mean, z = (real − null mean) / null SD):

| Null | ratio 0.5 (main) | 0.25 | 0.75 | trigram TPs | backward TPs |
|---|---|---|---|---|---|
| real song | 0.930 | 0.832 | 0.953 | 0.925 | 0.941 |
| shuffle | 0.738, z 22.7 | 0.480, z 20.6 | 0.862, z 19.9 | 0.669, z 26.4 | 0.717, z 24.8 |
| rotate | 0.876, z 13.9 | 0.740, z 8.7 | 0.917, z 13.3 | 0.840, z 17.3 | 0.876, z 16.7 |
| Markov-1 | 0.900, z 6.0 | 0.695, z 9.5 | 0.949, z 1.8 | 0.885, z 7.2 | 0.896, z 8.8 |
| repeat skeleton | 0.916, z 3.1 | 0.809, z 2.3 | 0.950, z 1.3 | 0.908, z 3.5 | 0.915, z 6.0 |
| Markov-2 | 0.939, z −2.1 | 0.796, z 2.6 | 0.962, z −3.8 | 0.918, z 1.4 | 0.938, z 0.8 |
| Markov-2, leave-one-recording-out | 0.939, z −1.9 | 0.797, z 2.7 | 0.963, z −3.7 | 0.919, z 1.1 | 0.938, z 0.6 |
| Markov-2, Witten-Bell | 0.914, z 3.0 | 0.739, z 6.0 | 0.950, z 1.2 | 0.906, z 3.6 | 0.920, z 4.2 |

The Markov-2 fakes aren't just copies: 46% of their 6-grams never occur in that year's real song.

**Brevity, main pipeline.** Kendall τ: real −0.25, nulls −0.34 to −0.40 (rotation −0.34). Poisson slope: real
−0.120, nulls −0.128 (rotation) to −0.253. Across all 35 null × pipeline cells, real is weaker on τ in 35 and on the slope in 32, two
of them not significant (p 0.83, 0.92).

**Calibration: real song's z against fake-song bands** ([min, max] over 20 fake datasets; Markov-1 / Markov-2).
One-back fake song never gets a Markov-1 z above +1.4, so real song is clearly past that everywhere.

| Pipeline | Real | Order 2, per year | Order 3, per year | Order 4, per year | Order 2, per recording | Order 3, per recording |
|---|---|---|---|---|---|---|
| ratio 0.5 (main) | +6.0 / −2.1 | [+4.7, +8.5] / [−3.1, +0.1] | [+5.9, +10.4] / [+0.9, +2.9] | [+4.7, +11.5] / [+0.9, +4.7] | [+5.6, +10.0] / [−2.0, +1.6] | [+7.4, +10.7] / [+0.9, +3.5] |
| ratio 0.25 | +9.5 / +2.6 | [+5.0, +8.0] / [−2.6, +0.0] | [+7.5, +12.4] / [+2.0, +4.8] | [+8.4, +13.7] / [+3.3, +7.4] | [+5.5, +10.4] / [−1.1, +2.6] | [+9.2, +12.9] / [+3.4, +6.4] |
| ratio 0.75 | +1.8 / −3.8 | [+0.5, +6.4] / [−1.3, +1.4] | [+1.6, +8.0] / [−0.3, +2.6] | [+1.1, +6.1] / [−1.1, +1.6] | [+2.4, +6.2] / [−1.2, +1.6] | [+2.7, +7.4] / [−1.1, +2.0] |
| trigram TPs | +7.2 / +1.4 | [+3.4, +6.1] / [−2.5, +0.4] | [+3.9, +9.1] / [+0.2, +3.5] | [+3.3, +10.9] / [+1.5, +4.5] | [+4.6, +7.9] / [−0.5, +1.7] | [+6.5, +9.4] / [+0.9, +3.8] |
| backward TPs | +8.8 / +0.8 | [+5.7, +8.5] / [−2.3, +0.8] | [+4.6, +10.7] / [+0.3, +3.6] | [+4.7, +11.3] / [+1.5, +4.8] | [+5.7, +9.6] / [−0.9, +1.7] | [+7.1, +10.8] / [+1.5, +3.5] |

- **Main pipeline:** inside the two-back band, and below every three- and four-back band on the Markov-2 null.
- **Ratio 0.25, trigram TPs, backward TPs:** against per-year chains, it looks three-back.
- **Two-back per recording (the closest match):** inside its bands for trigram and backward TPs, and just outside
  on the Markov-2 null at ratio 0.25 (+2.64 vs a max of +2.57) and on the main pipeline (−2.09 vs a min of
  −2.01), on opposite sides.
- **Ratio 0.75:** nothing fits, and the two- and three-back bands mostly overlap there anyway.

**Recordings differ.** How well each recording is predicted from the others in its year (order-2 chain):

| | Bits per element | Contexts unseen in the other recordings |
|---|---|---|
| Real song | 2.78 | 9.9% |
| Fake, one chain per year (orders 2–4) | 1.61–1.85 | 1.8–4.0% |
| Fake, one chain per recording | 2.78–3.11 | 10.8–13.2% |

Per-recording chains also copy more. Share of 8-grams found in their own source recording (mean of 20 datasets): order 2 per recording 34%, order 3 per recording 59%, order 3 per year 21%, order 2 per
year 14%.

**Power law (Clauset–Shalizi–Newman, main pipeline).** α 1.89–2.20 per year (pooled 2.01; Markov-2 surrogates
2.02). The bootstrap test rejects the power law (p < 0.1) in 3 of 8 years. A lognormal fits better in all 8
(significantly in 3), but it does in every pooled null sample too.

## Things to keep in mind

- z isn't an effect size: the null spread is about 0.005, so z = 6 against Markov-1 is an R² gap of 0.03.
- The bands come from only 20 fake datasets each, and some in/out calls hinge on about 0.1 z.
- I picked the per-recording chains after seeing the earlier results.
- I didn't model label noise (your random-forest check on a subset gave 19% out-of-bag error).
- My Markov fakes keep recording lengths and start sounds, but not theme order within a recording.

## Notes for the authors

A few things that came up along the way, in case they're useful:

- **A small-data baseline without smoothing:** compare real song with fake song of known order at the same size
  and structure, as above. `smalldata.py` worked for the finch data too.
- **Recordings differ a lot within a year,** and year-pooled TPs and nulls ignore that. It moved my calibration
  noticeably. Per-recording or hierarchical nulls might be fairer, and singer or date info could show what drives
  the differences.
- **R² gaps next to z** would help readers see the size of the effect.
- **A direct power-law test** might be worth adding: log-log R² is 0.74 even for shuffled song.
- **Brevity under the corrected metric could use a baseline,** ideally a length-matched one like rotation. On the
  whale main pipeline rotation is only slightly steeper than real song; in finches real song ties shuffled song.
- **Finch:** against fake song whose bouts are all alike, finch song at ratio 0.5 sits above the trigram, which is
  good news for your claim. Worth checking with bout-to-bout variation.
- **Cutting ratio:** the loosest ratio fits no plain chain in either species, so pre-registering the main ratio
  might help.
- **Finch data:** the table is only in the SM PDF as vector shapes, so I rebuilt it by clustering the glyphs. A CSV
  would make this much easier for the next person.
- **Label noise:** relabelling a range of shares of elements at random and rerunning would show how much results
  move.
- **Simon-game threshold:** in that notebook the ratio function never updates `last_tp`, so the 0.425 cut comes
  from TP ÷ first TP. The consistent version gives 0.441; it barely changes the results.

## What was already out there (checked 2026-10-17)

The paper used shuffle and rotation baselines. The erratum (Science 388, doi:10.1126/science.adx8687) replaced
the brevity test without rerunning baselines. The finch paper (Kirby et al. 2026, Sci. Adv.
doi:10.1126/sciadv.aea3015) added a bigram baseline, but it was never applied to the whale data. Four eLetters argued
about random segmentation, but nobody ran a Markov null. As far as I could find, the Markov-2 nulls, the corrected-brevity
baselines, the power-law tests and the calibration are new.

## Files and rerun

| File | Role |
|---|---|
| `pipeline.py` | load, TPs, segmentation, R², brevity, null generators; `python -I pipeline.py` = self-check |
| `run_nulls.py` | 1000 surrogates per null → `results/null_<name>.json` (checkpointed) |
| `reproduce.py`, `diagnostics.py`, `summarize.py` | real-data metrics, surrogate novelty and entropies, tables and figures |
| `powerlaw.py` | Clauset–Shalizi–Newman fit and tests |
| `smalldata.py` | held-out prediction (`ce`), calibration (`nc`, `ncv <1\|2\|3\|4\|rec2\|rec3>`), recording differences (`het`), copying (`copy`), `report` → `results/smalldata_tables.md` (full tables) |
| `finch/` | the finch rerun |
| `human/` | the Simon-game check (`run_human.py`; data not included) |
| `speech/` | the child-directed speech check (`make_speech.py`, `run_speech.py`, `compare.py`; data not included) |
| `download/` | the authors' supplementary files; read, never executed |

Data: `download/science.adq7055_data_s2.csv`. Everything ran at Windows idle priority with
numpy, scipy and matplotlib; the nulls take about 35 min and each calibration chain 65–80 min.

```bash
for n in shuffle rotate markov1 markov2 repeat markov2cv markov2wb; do python -I run_nulls.py download/science.adq7055_data_s2.csv $n 1000; done
```

```bash
python -I reproduce.py download/science.adq7055_data_s2.csv 1000 && python -I diagnostics.py download/science.adq7055_data_s2.csv 50 && python -I summarize.py download/science.adq7055_data_s2.csv > results/tables.md
```

```bash
python -I smalldata.py download/science.adq7055_data_s2.csv ce && python -I smalldata.py download/science.adq7055_data_s2.csv het && python -I smalldata.py download/science.adq7055_data_s2.csv copy && for t in 1 2 3; do python -I smalldata.py download/science.adq7055_data_s2.csv nc $t; done && for t in 1 2 3 4 rec2 rec3; do python -I smalldata.py download/science.adq7055_data_s2.csv ncv $t; done && python -I smalldata.py download/science.adq7055_data_s2.csv report
```
