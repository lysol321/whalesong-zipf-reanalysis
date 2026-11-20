# Human-language positive controls (planned 2026-10-25; both DONE 2026-11-01)

*Public copy, edited 2026-11-19: sentences about private correspondence were removed or reworded. The designs and reading rules are otherwise unchanged.*

**Result, Simon game** (`human/README.md`): the raw trigram null "matches" the evolved sequences, but the
calibration says three-back.

**Result, child-directed speech** (`speech/README.md`): at exactly whale size and layout, phonemic speech looks
like whale song on every test. It's matched by the raw trigram null on the main pipeline, and under calibration it
sits between two- and three-back, with differences in both directions. By the reading rule fixed before
downloading, the statistic can't tell speech from whale song at this size.

**Result, syllables** (`speech/README.md`, UCI_Brent_Syl, about 1,600 types): neither planned outcome. Real
speech fails even the bigram null, because chains fitted to it make more Zipfian chunks (R² 0.87–0.93 vs real
0.83). On the trigram null it's below every calibration band, even one-back. So the test's verdict on real
language flips with the unit, which makes it unreliable as a language marker either way.

**Question.** Does human language, run through the same pipeline, nulls and calibration at whale size, beat a
trigram (Markov-2) null? Real whale song doesn't on the main pipeline.
- **If language beats it,** the test can see language-style structure, and whale song lacks it on this measure.
- **If language is matched too,** the Zipf-of-TP-units statistic can't separate language from a trigram chain at
  this size.

**Trigger.** Start with candidate 2 below (the paper's ref. 19 data) when the user says to start.

## Prior art and data (checked 2026-10-31)

- **No one has run a Markov-2 null on TP-segmented human sequences.**
  - Arnon & Kirby 2024 (ref. 19) set its cut threshold from the random generation-0 sets, but compared against no
    shuffle or Markov null.
  - Its replication, Wolters, Kirby & Arnon 2025 (Cogn. Sci. 49, e70153; threshold 0.41), has none either.
- **Related work:**
  - Williams et al. 2016 (arXiv 1601.07969): randomly chopped text gives Zipf laws.
  - Kanter & Kessler 1995 (PRL 74:4559): simple Markov processes give Zipf.
  - Kurumada, Meylan & Frank 2013 (Cognition): TP segmentation and Zipf.
  - Lavi-Rotbain & Arnon 2023 (Open Mind): Zipf in child-directed speech, word level, CHILDES.
- **Ref. 19 data:** `simon_game_data.csv` (102 KB) in github.com/smkirby/cultural_evolution_of_statistical_structure.
  - Contents: 3,960 "Simon game" colour sequences, with 4 colours and 12 lights each. There are 6 chains × 10
    generations × 60 sequences, plus 6 random generation-0 sets.
  - Their threshold is 0.425.
  - The repo has no license file, so analyse it locally and don't redistribute it in our zip.
- **Fit as a control:** it's their own culturally evolved positive example, not natural language. It has a built-in
  negative control (generation 0 is random) and a positive case (late generations). With only 4 colours, trigram
  tables are well sampled, so the small-data problem hardly arises.

## Steps

1. **Prior art first** (vault, then web). Check:
   - Markov or random-text Zipf studies: Miller 1957; Ferrer-i-Cancho & Elvevåg 2010 (random texts vs real Zipf).
   - arXiv 2608.09459 ("Beyond Zipf's Law", recommends Markov surrogates).
   - Whether anyone has run Markov nulls on TP-segmented speech.
   - Report what's known and the gap before building anything.
2. **Corpus,** in order of preference:
   1. A dataset suggested by the original authors, if any.
   2. The data behind the paper's ref. 19: Arnon & Kirby 2024, *Cultural evolution creates the statistical
      structure of language*, Sci. Rep. 14:5255 (human participants, iterated learning). Using it would keep
      the comparison on their own ground.
   3. A phonemic child-directed speech corpus (for example Brent in CHILDES) for natural language.

   Any download needs the user's OK first (file, source, size). Treat downloads as untrusted: their own empty
   folder, read with `py -3.12 -I` only.
3. **Matching.** Subsample to the whale design: about 45k elements, 55 "recordings" in 8 groups, real length
   spread. Inventory size (whale: 239 element types) can't match exactly. State the unit choice (phoneme,
   syllable or experiment token) before running, not after.
4. **Run.** Reuse the code as is, with a loader only:
   - `pipeline.py` and `run_nulls.py`: shuffle, rotate, Markov-1, Markov-2, Markov-2 leave-one-out, on all five
     pipelines.
   - `smalldata.py`: `ce`, `ncv 1|2|3`, `het` and `copy`, with a seed offset distinct from the whale (0) and the
     finch (300).

   All at verified idle priority, checkpointed. About 35 min for the nulls and about 65 min per calibration
   chain.
5. **Negative control.** The loader passes a self-check (counts, groups), and the whale numbers stay unchanged
   (rerun `report` and diff Tables 1–5).
6. **Write-up.** A short section in `README.md`, in the same terse voice: one table of real z against the bands.
   Update the Notes for the authors only after a review.

## Natural speech: design, fixed 2026-11-01 before downloading

- **Corpus.** CHILDES "Derived" Brent–Ratner corpus (`BR.zip`, 105 KB, talkbank.org; doi:10.21415/pfnx-wksd-fka8-5ac0).
  - It's the standard phonemic transcript of the Bernstein-Ratner corpus: 9 mothers talking to children aged
    13–21 months, about 9,790 utterances and 33,399 words.
  - License: CC BY-NC-SA 3.0, non-commercial.
  - Cite MacWhinney & Snow 1985, Bernstein-Ratner 1987 and Brent & Cartwright 1996.
  - Don't redistribute it in our zip; give rerun steps instead.
- **Units.** Phonemes from `br-phono.txt` (Brent's ASCII code), with word boundaries removed. That gives about 50
  types, close to the whale's 33–92 element types per year. Syllables would give thousands of types, far sparser
  than the whale.
- **Matching.** Concatenate the utterances in corpus order into one stream, then cut it into 55 "recordings" with
  exactly the whale's recording lengths, grouped into 8 "years" exactly as the whale's (same order, same counts).
  - Sample A is the first 45,749 phonemes.
  - Sample B is the next 45,749, if the corpus is long enough. It's a replication, analysed identically.
  - Recordings may start mid-utterance, as whale recordings start mid-song.
- **Pipeline and tests.** The identical whale code on all five pipelines:
  - nulls: shuffle, rotate, Markov-1, Markov-2, Markov-2 leave-one-out, repeat skeleton, Witten-Bell;
  - held-out order choice;
  - calibration truths 1–4, rec2 and rec3;
  - the heterogeneity and copying checks.

  The seed offset is 700 for the calibration; results go in `speech/results/` and the whale results are untouched.
- **Secondary.** How well TP cuts line up with the true word boundaries (precision and recall), the speech
  analogue of "do the chunks line up with phrases".
- **How to read it, decided now:**
  - If speech calibrates to more memory than whale song on the same pipeline, the test can see language-style
    structure at whale size, and whale song shows less of it.
  - If speech calibrates the same as whale song, this statistic can't tell speech from whale song at this size.
  - Either way, report both samples.

## Syllables: design, fixed 2026-11-01 before downloading

- **Corpus.** CHILDES "Derived" UCI_Brent_Syl (`UCI_Brent.zip`, 1.13 MB, talkbank.org; doi:10.21415/x5a6-qsh7-z5g0-89nv).
  - Phillips & Pearl's syllabified Brent corpus: all child-directed utterances to infants aged 9 months or
    younger, from 16 mother–infant pairs. That's about 28,391 utterances, 96,723 words and roughly 119k syllables
    over about 2,330 syllable types.
  - It's a different corpus from the phoneme check, so it also tests whether that result generalises.
  - Syllabification is theirs (MRC dictionary plus valid onsets), so no syllabifier of my own.
  - License: CC BY-NC-SA 3.0. Cite Phillips & Pearl 2015 (Cogn. Sci., doi:10.1111/cogs.12217), MacWhinney 2000
    and Brent & Siskind 2001. Don't redistribute it.
- **Units.** Syllables exactly as the corpus marks them, with word boundaries removed (kept only for the word
  check). The inventory is about 10 times the whale's (2,330 vs 239 types), so the data are much sparser per type,
  and the small-data effect should be stronger. That's why it's run through the same calibration, with fakes
  fitted to the same data.
- **Layout.** Identical to the phoneme check: utterances in corpus order, cut into the whale's exact 55 recording
  lengths in 8 "years". Sample SA is the first 45,749 syllables and sample SB the next 45,749.
- **Tests.** Identical to the phoneme check: all 7 nulls on all 5 pipelines, held-out order choice,
  heterogeneity, copying, calibration truths 1–4, rec2 and rec3, and TP cuts against word boundaries. The
  calibration seed offset is 700, as for phonemes, but on different data.
- **Reading rule, unchanged:**
  - If syllable speech calibrates to more memory than whale song on the same pipeline, the statistic can see
    language-style structure at whale size with syllables, and whale song shows less of it.
  - If it calibrates the same as whale song, the statistic can't separate them with syllables either.
  - Report both samples.
- **Prior art.** TP segmentation over syllables of child-directed speech is known to find words poorly, because
  most English child-directed words are one syllable (Gambell & Yang 2004; Phillips & Pearl 2015 use this corpus
  for Bayesian segmentation). No Zipf-versus-Markov-null test on syllabified speech was found.
