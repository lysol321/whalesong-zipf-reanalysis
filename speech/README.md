# Speech check: child-directed speech, cut to whale size, through the same tests

The Simon-game check (`../human/`) showed the calibration can pick up longer memory in human-made sequences. This
one asks the harder question: does real language, at exactly the whale data's size and layout, look any different
from whale song on this statistic?

**Data.** The CHILDES Brent–Ratner corpus (the standard phonemic transcript used in word-segmentation research):
nine mothers talking to their 13–21-month-olds, 9,790 utterances, 33,399 words, 95,809 phonemes.
- Source: https://talkbank.org/childes/access/Derived/Brent_Ratner.html (doi:10.21415/pfnx-wksd-fka8-5ac0).
- Citations: MacWhinney & Snow 1985; Bernstein-Ratner 1987; Brent & Cartwright 1996.
- License: CC BY-NC-SA 3.0. Not included here; `make_speech.py` rebuilds the samples from `br-phono.txt`.

**Design (written down before downloading, `../NEXT_HUMAN_CONTROL.md`).**
- Units are phonemes (49–50 types, close to the whale's 33–92 per year), with word breaks removed.
- Utterances are strung together in order and cut into exactly the whale's 55 recording lengths, in its 8 "years".
- Sample A is the first 45,749 phonemes; sample B, the next 45,749, is a replication.
- Then the identical whale code runs on both.

## The short version

- **The pipeline finds real structure in speech.** About 66% of TP cuts land on a true word boundary (chance is
  35%), and they find about 62% of all word boundaries.
- **Raw nulls look just like whale song.**
  - Speech beats shuffle, rotation, the bigram null and the smoothed trigram null by a wide margin.
  - It's matched by the plain trigram null on the main pipeline (z −2.3 and −1.4; whale song −2.1).
  - It beats that null at ratio 0.25 and loses at 0.75, the same as whale song.
- **Brevity looks like whale song too.** On Kendall τ, speech shows weaker brevity than the Markov nulls (and than
  shuffle in sample A). So that whale result doesn't set whale song apart from language either.
- **Under calibration, speech and whale song land in the same place:**
  - above two-back on the sharper cuts, and well short of three-back;
  - closest to two-back per recording;
  - no fake song fits on every pipeline, and nothing fits at ratio 0.75.

  Where they differ, it goes both ways. On the main pipeline speech edges just past two-back while whale song
  stays inside it. On three other pipelines, whale song sits *closer* to three-back than speech does.
- **Where I landed.** At this data size, this statistic can't tell whale song from human speech. That cuts both
  ways: whale song looks about as "language-like" as phonemic speech here. But the statistic can't show anything
  beyond short-range sequential structure in either, so it can't be evidence for language-like organisation as
  such.

## Results

**Raw trigram (Markov-2) null, z** (full null tables in `results/A/tables.md` and `results/B/tables.md`):

| pipeline | whale | speech A | speech B |
|---|---|---|---|
| ratio 0.5 (main) | −2.1 | −2.3 | −1.4 |
| ratio 0.25 | +2.6 | +3.4 | +2.3 |
| ratio 0.75 | −3.8 | −4.1 | −5.4 |
| trigram TPs | +1.4 | +1.4 | +2.5 |
| backward TPs | +0.8 | −0.2 | +2.5 |

**Calibration, on one scale:** how far real data sits from each kind of fake (in that fake's SD units, trigram
null; * = inside the band on both nulls). Both nulls and all truths are in `results/compare.md`.

| pipeline | two-back per year: whale / A / B | three-back per year: whale / A / B | two-back per recording: whale / A / B |
|---|---|---|---|
| ratio 0.5 (main) | −0.8* / +2.9 / +2.8 | −6.8 / −10.0 / −5.8 | −2.6 / −6.3 / −3.3 |
| ratio 0.25 | +5.6 / +6.7 / +6.2 | −0.7* / −7.8 / −4.7 | +1.9 / +0.7* / −0.1* |
| ratio 0.75 | −6.1 / −9.0 / −16.7 | −5.9 / −6.9 / −10.8 | −5.7 / −9.6 / −12.1 |
| trigram TPs | +3.2 / +5.5 / +5.6 | −1.1* / −8.0 / −3.1 | +1.7* / −1.2 / +0.8* |
| backward TPs | +2.1 / +3.2 / +7.9 | −1.5* / −11.1 / −3.1 | +0.5* / −2.0 / +0.8 |

**Side checks:**

| | speech A | speech B | whale |
|---|---|---|---|
| Hide-one-out, best order (pooled) | 3 (by 0.03 bits) | 3 (by 0.04 bits) | 2 (7 of 8 years) |
| Recordings differ: held-out bits, real | 3.33 | 3.37 | 2.78 |
| … fakes, one chain per year / per recording | 2.53–2.62 / 3.57–3.66 | 2.50–2.59 / 3.60–3.71 | 1.61–1.85 / 2.78–3.11 |
| Unseen contexts, real / per-year fakes / per-recording fakes | 6.0% / 3% / 9% | 6.0% / 3% / 9% | 9.9% / 2–4% / 11–13% |
| TP cuts on true word boundaries (main pipeline; chance 0.35) | 0.66 | 0.67 | n/a |

As with the whale, real recordings differ more than one-chain-per-year fakes do and less than per-recording fakes
do, so the right band lies somewhere between the two.

## Things to keep in mind

- **Phonemes are one choice of unit.** The syllable version is below, and it comes out very differently.
- **This is child-directed speech:** short, repetitive utterances. Adult conversation or read text might differ.
- **Cross-dataset z-scores aren't directly comparable.** That's why the calibration compares each dataset with
  its own fakes.

## Syllables (a second corpus)

Same layout and same tests, but in syllables, using Phillips & Pearl's syllabified Brent corpus.
- Source: CHILDES UCI_Brent_Syl (https://talkbank.org/childes/access/Derived/UCI_Brent_Syl.html,
  doi:10.21415/x5a6-qsh7-z5g0-89nv). It's 16 mothers talking to infants aged 9 months or younger: 28,391
  utterances, 96,467 words and 117,528 syllables.
- Citations: Phillips & Pearl 2015 (Cogn. Sci., doi:10.1111/cogs.12217); MacWhinney 2000; Brent & Siskind 2001.
- License: CC BY-NC-SA 3.0, not included.
- Samples SA and SB each hold 45,749 syllables with about 1,600 syllable types, against the whale's 239.

**The short version.**
- **Real speech fails even the bigram null.** Chains fitted to it, even one-back, make chunks that are *more*
  Zipfian than the speech itself (main pipeline bigram-null z −7.8 and −10.4; trigram-null z −47 and −57).
- **The calibration can't place it.** On the trigram null, real speech is below every fake-song band on every
  pipeline:
  - 3–17 SD below even the one-back fakes;
  - 9–132 SD below two-back and up, including the per-recording fakes that copy most of the real song.

  On the bigram null it sits around the one-back fakes. So no chain fits on both nulls.
  - Real R² is 0.83 in both samples. Fakes from one-back chains reach 0.87, and every fake of two-back or more
    reaches 0.93.
  - Real speech also makes more distinct chunks than its trigram null does (about 10,000 vs 7,700).
  - Something in real syllable speech that no plain chain reproduces drags its Zipf fit down. I don't know what.
- **Hide-one-out picks one-back** in 7 of 8 and 8 of 8 groups. At this size, half the two-syllable contexts in a
  held-out recording are unseen elsewhere in its group.
- **Brevity runs the other way from phonemes and whales.** Real speech shows *more* brevity than shuffle, rotation
  and the trigram null, but less than the bigram null.

**What it means.** Neither of the two outcomes I'd planned for fits. With syllables at whale size, real language
would fail the very test whale song passes. So whether real language "beats a Markov null" here depends on the
unit and the inventory size. It's not something language reliably does under this pipeline, which makes it a
poor marker of language-likeness in either direction. Whale song's 239 element types sit between the two cases
(50 phonemes, about 1,600 syllables).

| syllables, main pipeline | SA | SB |
|---|---|---|
| real R² / bigram null / trigram null | 0.835 / 0.868 / 0.931 | 0.822 / 0.867 / 0.929 |
| z vs bigram / trigram null | −7.8 / −47.3 | −10.4 / −57.1 |
| one-back fakes' band (bigram / trigram null z) | [−10.1, −7.0] / [−32.4, −9.6] | [−10.2, −3.9] / [−28.9, −16.7] |
| hide-one-out best order (pooled bits, order 1 vs 2) | 1 (7.00 vs 7.05) | 1 (7.08 vs 7.17) |
| TP cuts on word boundaries (chance) | 0.97 (0.82) | 0.97 (0.82) |

Full tables: `results/SA/tables.md`, `results/SB/tables.md`; side by side with the whale and phonemes:
`results/compare.md`.

## Rerun

From `whalesong/speech/`, with the TalkBank zip unpacked under `download/`. About 2 h per calibration truth at
idle priority, all in parallel:

```bash
python -I make_speech.py "download/BR/brent_ratner copy/br-phono.txt" ../download/science.adq7055_data_s2.csv && python -I make_speech.py "download_syl/UCI/uci-brent-syl-Dec2013 copy/data/brent9mos-text-klatt-syls.txt" ../download/science.adq7055_data_s2.csv syl && for s in A B SA SB; do python -I run_speech.py $s real && python -I run_speech.py $s words && for n in shuffle rotate markov1 markov2 repeat markov2cv markov2wb; do python -I run_speech.py $s null $n 1000; done && python -I run_speech.py $s ce && python -I run_speech.py $s het && python -I run_speech.py $s copy && for t in 1 2 3 4 rec2 rec3; do python -I run_speech.py $s ncv $t; done && python -I run_speech.py $s report; done && python -I compare.py
```
