"""Build whale-matched speech samples from the CHILDES Brent-Ratner phonemic transcript (br-phono.txt).

Design (fixed before download, NEXT_HUMAN_CONTROL.md): phonemes (one ASCII character each in Brent's code), word
boundaries removed, utterances concatenated in corpus order into one stream. The stream is cut into 55 "recordings"
with exactly the whale recording lengths, grouped into the 8 whale "years" in the same order. Sample A is the first
45,749 phonemes, sample B the next 45,749. Output: Data S2-format CSVs (so pipeline.load reads them unchanged) plus
the true word-start positions of every recording, for the cut-versus-word check.

Usage (from whalesong/speech; inputs are untrusted text, read only):
  python -I make_speech.py <br-phono.txt> <whale data_s2.csv>     -> data/speech_A.csv, speech_B.csv, words_*.json
  python -I make_speech.py <brent9mos-text-klatt-syls.txt> <whale data_s2.csv> syl   -> data/speech_SA.csv, speech_SB.csv
                                                                  (syllables from UCI_Brent_Syl, same layout)
  python -I make_speech.py                                        self-check
"""
import csv
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))  # whalesong/: pipeline
import pipeline as P

OUT = os.path.join(HERE, "data")


def stream(lines):
    """-> (phonemes, word_start flags, utterance_start flags), one entry per phoneme."""
    ph, ws, us = [], [], []
    for line in lines:
        words = line.split()
        assert words and all(w.isascii() and w.isprintable() for w in words), line
        for i, w in enumerate(words):
            for j, c in enumerate(w):
                ph.append(c)
                ws.append(j == 0)
                us.append(i == 0 and j == 0)
    return ph, ws, us


def stream_syl(lines):
    """Syllables as the UCI_Brent_Syl corpus marks them: words split by spaces, syllables within a word by '/'.
    Empty utterances (fillers the corpus removed) are skipped. -> (syllables, word_start, utterance_start)."""
    sy, ws, us = [], [], []
    for line in lines:
        words = line.split()
        if not words:
            continue
        for i, w in enumerate(words):
            parts = w.split("/")
            assert all(parts) and w.isascii() and w.isprintable(), line
            for j, s in enumerate(parts):
                sy.append(s)
                ws.append(j == 0)
                us.append(i == 0 and j == 0)
    return sy, ws, us


def layout(whale):
    """Whale structure: [(year, [recording lengths])] in pipeline.load order."""
    return [(y, [len(r) for r in recs]) for y, recs in whale.items()]


def cut(ph, ws, lay, offset):
    """Slice the stream into the whale layout from `offset`. -> ({year: [phoneme lists]}, {year: [[word starts]]})."""
    data, words, i = {}, {}, offset
    for y, lens in lay:
        for L in lens:
            data.setdefault(y, []).append(ph[i:i + L])
            words.setdefault(y, []).append([k for k in range(L) if ws[i + k]])
            i += L
    return data, words, i


def write(tag, data, words):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, f"speech_{tag}.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["song_type", "string"])
        for y, recs in data.items():
            for r in recs:
                w.writerow([f"{tag}{y}", repr(list(r))])
    json.dump({f"{tag}{y}": v for y, v in words.items()}, open(os.path.join(OUT, f"words_{tag}.json"), "w"))


def main(src, whale_csv, unit="phon"):
    """unit 'phon': br-phono.txt -> samples A, B. unit 'syl': UCI_Brent_Syl brent9mos-text-klatt-syls.txt -> SA, SB."""
    lines = open(src, encoding="utf-8").read().splitlines()
    ph, ws, us = (stream if unit == "phon" else stream_syl)(lines)
    whale, _ = P.load(whale_csv)
    lay = layout(whale)
    total = sum(sum(lens) for _, lens in lay)
    assert 2 * total <= len(ph), (len(ph), total)
    end = 0
    for tag in (("A", "B") if unit == "phon" else ("SA", "SB")):
        data, words, end = cut(ph, ws, lay, end)
        write(tag, data, words)
        back, voc = P.load(os.path.join(OUT, f"speech_{tag}.csv"))
        assert [[len(r) for r in v] for v in back.values()] == [lens for _, lens in lay]
        assert [c for y in data for r in data[y] for c in r] == ph[end - total:end]
        nw = sum(len(x) for v in words.values() for x in v)
        print(f"sample {tag}: {total} units, {len(voc)} types, {nw} word starts, "
              f"stream {end - total}-{end} of {len(ph)}")
    print(f"utterances {sum(us)}, words {sum(ws)}, units {len(ph)}")


def _selfcheck():
    ph, ws, us = stream(["ab c", "de"])
    assert ph == list("abcde") and ws == [1, 0, 1, 1, 0] and us == [1, 0, 0, 1, 0]
    data, words, end = cut(ph, ws, [("y1", [2, 1]), ("y2", [2])], 0)
    assert data == {"y1": [["a", "b"], ["c"]], "y2": [["d", "e"]]} and words == {"y1": [[0], [0]], "y2": [[0]]}
    assert end == 5
    sy, ws, us = stream_syl(["kI/ti Iz ", "", "o/ke "])
    assert sy == ["kI", "ti", "Iz", "o", "ke"] and ws == [1, 0, 1, 1, 0] and us == [1, 0, 0, 1, 0]
    print("make_speech selfcheck ok")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        _selfcheck()
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "phon")
