"""Form: inputs → engine → outputs — three labelled bands.

For when someone asks how a many-step thing gets built and the answer is that it
is not many things. Three bands, each labelled above itself, with an arrow
between them.

SLOTS
  title, subtitle   str
  bands             list of exactly 3:
                      {"label": str, "items": [box dict, ...]}
                    conventionally inputs, the engine, outputs; the engine band
                    is usually one item
  note              str | None
  effects           list of effect dicts, 0-3
"""

from core import (LayoutError, arrow_down, band_label, build_fitted,
                  provenance)
from layout import effect_row, note as note_row, to_boxes

FORM = "bands"


def build(slots, ratio, theme_name, path, *, w=None, h=None, base_lock=None,
          mode="tpl"):
    bands = slots["bands"]
    if len(bands) != 3:
        raise LayoutError("this form is exactly three bands")

    def compose(cv):
        y = cv.head_h
        gap, band_gap = 18, 30
        for bi, band in enumerate(bands):
            cv.add(band_label(cv.m, y, band["label"], cv.sc, cv.t))
            y += cv.sc.s + 10
            items = to_boxes(band["items"])
            cols = len(items) if cv.ratio == "wide" else min(2, len(items))
            bw = (cv.inner_w - gap * (cols - 1)) / cols
            if bw < 130:
                raise LayoutError(f"band {band['label']!r} leaves {bw:.0f}px "
                                  f"per item")
            for i in range(0, len(items), cols):
                sub = items[i:i + cols]
                bh = max(b.height(bw, cv.sc) for b in sub)
                x = cv.m
                for b in sub:
                    cv.add(b.draw(x, y, bw, bh, cv.sc, cv.t))
                    x += bw + gap
                y += bh
                if i + cols < len(items):
                    y += gap
            if bi < 2:
                cv.add(arrow_down(cv.W / 2, y + 6, y + band_gap - 4, cv.t))
                y += band_gap
        if slots.get("note"):
            y = note_row(cv, y, slots["note"])
        if slots.get("effects"):
            y = effect_row(cv, to_boxes(slots["effects"], kind="effect"), y + 22)
        return y

    return build_fitted(ratio, slots["title"], slots.get("subtitle"),
                        theme_name, provenance(FORM, mode=mode), compose,
                        path, w=w, h=h, base_lock=base_lock)
