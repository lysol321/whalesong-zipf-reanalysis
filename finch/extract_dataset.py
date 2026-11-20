"""Recover the finch Dataset table from the SM PDF, where it is drawn as vector glyph outlines (no text layer).
Each filled path ('f') is one glyph; identical letters have identical outlines, so glyphs are clustered by
shape and each unique shape is labelled once by eye (glyph_labels.json).

Usage:
  python -I extract_dataset.py <sm.pdf> montage    -> glyph_montage.png + glyphs.json (cluster ids)
  python -I extract_dataset.py <sm.pdf> build      -> finch_bouts.tsv (bird, day, bout with spaces as printed)
"""
import json
import os
import re
import sys

import numpy as np
import pypdf

HERE = os.path.dirname(os.path.abspath(__file__))
PAGES = range(48, 58)  # 0-based: PDF pages 49-58
NUM = r"-?\d*\.?\d+(?:[eE][-+]?\d+)?"
TOK = re.compile(NUM + r"|[A-Za-z*'\"]+|/[A-Za-z0-9]+")


def glyphs_on_page(page):
    """-> list of (ops, bbox) for every black filled non-rectangle path, plus row bands from the bird column."""
    data = page.get_contents().get_data().decode("latin1")
    out, bands, stack, path, black = [], [], [], [], False
    for t in TOK.findall(data):
        if t[0].isdigit() or t[0] in "-.":
            stack.append(float(t))
            continue
        if t in ("m", "l", "c"):
            path.append((t, tuple(stack)))
        elif t == "re":
            x, y, w, h = stack[-4:]
            if abs(x - 78) < .01 and abs(w - 36) < .01 and h > 5:
                bands.append((y, y + h))
            path.append(("re", tuple(stack[-4:])))
        elif t == "h":
            path.append(("h", ()))
        elif t == "sc":
            black = stack[-3:] == [0.0, 0.0, 0.0]
        elif t in ("f", "n"):
            if t == "f" and black and path and not any(o == "re" for o, _ in path):
                pts = np.array([v for o, a in path for v in zip(a[0::2], a[1::2])])
                out.append((path, (pts[:, 0].min(), pts[:, 1].min(), pts[:, 0].max(), pts[:, 1].max())))
            path = []
        stack = []
    return out, sorted(set(bands), reverse=True)


def signature(ops, bbox):
    x0, y0 = bbox[0], bbox[1]
    sig = []
    for o, a in ops:
        rel = [round(v - (x0 if i % 2 == 0 else y0), 2) for i, v in enumerate(a)]
        sig.append(o + ",".join(f"{v:.2f}" for v in rel))
    return "|".join(sig)


def collect(pdf):
    r = pypdf.PdfReader(pdf)
    allg = []
    for pi in PAGES:
        g, bands = glyphs_on_page(r.pages[pi])
        for ops, bb in g:
            allg.append({"page": pi + 1, "bbox": [float(v) for v in bb], "sig": signature(ops, bb), "ops": ops})
        allg.append({"page": pi + 1, "bands": bands})
    return allg


def montage(pdf):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.path import Path
    from matplotlib.patches import PathPatch
    allg = collect(pdf)
    sigs = {}
    for g in allg:
        if "sig" in g:
            sigs.setdefault(g["sig"], []).append(g)
    order = sorted(sigs, key=lambda s: -len(sigs[s]))
    ids = {s: i for i, s in enumerate(order)}
    n = len(order)
    cols = 12
    rows = (n + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(cols * 1.1, rows * 1.3))
    for ax in axes.flat:
        ax.axis("off")
    for s, i in ids.items():
        g = sigs[s][0]
        verts, codes = [], []
        for o, a in g["ops"]:
            if o == "m":
                verts.append(a[-2:]); codes.append(Path.MOVETO)
            elif o == "l":
                verts.append(a[-2:]); codes.append(Path.LINETO)
            elif o == "c":
                verts += [a[0:2], a[2:4], a[4:6]]; codes += [Path.CURVE4] * 3
            elif o == "h":
                verts.append(verts[-1] if verts else (0, 0)); codes.append(Path.CLOSEPOLY)
        ax = axes.flat[i]
        ax.add_patch(PathPatch(Path(verts, codes), fc="black", lw=0))
        x0, y0, x1, y1 = g["bbox"]
        c = ((x0 + x1) / 2, (y0 + y1) / 2)
        ax.set_xlim(c[0] - 5, c[0] + 5); ax.set_ylim(c[1] - 5, c[1] + 5); ax.set_aspect("equal")
        ax.set_title(f"{i} (n={len(sigs[s])})", fontsize=7)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "glyph_montage.png"), dpi=110)
    json.dump({"ids": ids}, open(os.path.join(HERE, "glyphs.json"), "w"))
    print(n, "unique glyph shapes;", sum(len(v) for v in sigs.values()), "glyphs")


def build(pdf):
    ids = json.load(open(os.path.join(HERE, "glyphs.json")))["ids"]
    lab = json.load(open(os.path.join(HERE, "glyph_labels.json")))
    allg = collect(pdf)
    rows, page_glyphs, out = [], [], []
    for g in allg:
        if "bands" in g:
            for y0, y1 in g["bands"]:
                cell = [h for h in page_glyphs if y0 <= (h["bbox"][1] + h["bbox"][3]) / 2 < y1]
                rows.append(cell)
            page_glyphs = []
        else:
            page_glyphs.append(g)
    for cell in rows:
        cols = {"bird": [], "day": [], "seq": []}
        for h in cell:
            xc = (h["bbox"][0] + h["bbox"][2]) / 2
            cols["bird" if xc < 114 else "day" if xc < 139.5 else "seq"].append(h)
        txt = {}
        for k, gl in cols.items():
            # lines: group by vertical centre, top to bottom; within a line left to right; a gap > 2.2 pt = space (gaps are bimodal: <=1.75 within, >=2.75 between)
            gl = sorted(gl, key=lambda h: -(h["bbox"][1] + h["bbox"][3]) / 2)
            lines = []
            for h in gl:
                yc = (h["bbox"][1] + h["bbox"][3]) / 2
                if lines and abs(lines[-1][0] - yc) < 4:
                    lines[-1][1].append(h)
                else:
                    lines.append([yc, [h]])
            parts = []
            for _, ln in lines:
                ln.sort(key=lambda h: h["bbox"][0])
                s = ""
                for a, b in zip([None] + ln[:-1], ln):
                    if a is not None and b["bbox"][0] - a["bbox"][2] > 2.2:
                        s += " "
                    s += lab[str(ids[b["sig"]])]
                parts.append(s)
            txt[k] = "\n".join(parts)
        out.append(txt)
    with open(os.path.join(HERE, "finch_bouts.tsv"), "w", encoding="utf-8") as f:
        for t in out:
            f.write("\t".join(t[k].replace("\n", "/") for k in ("bird", "day", "seq")) + "\n")
    print(len(out), "rows written")


if __name__ == "__main__":
    {"montage": montage, "build": build}[sys.argv[2]](sys.argv[1])
