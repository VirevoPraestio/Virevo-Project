"""Form: converging rail — several inputs feeding one thing.

A rail spans the whole input block and one arrow leaves its centre. An arrow
rising out of the gap between two boxes reads as coming from nowhere; the rail
says the block itself is the source.

SLOTS
  title, subtitle   str
  inputs            list of box dicts, 2-4
  target            box dict — the thing they feed
  inputs_label      str | None    section label above the input band
  note              str | None
  effects           list of effect dicts, 0-3
"""

from core import (LayoutError, arrow_down, band_label, build_fitted,
                  provenance, rail)
from layout import effect_row, note as note_row, row, to_boxes

FORM = "converging-rail"


def build(slots, ratio, theme_name, path, *, w=None, h=None, base_lock=None,
          mode="tpl"):
    inputs = slots["inputs"]
    if not 2 <= len(inputs) <= 4:
        raise LayoutError(f"converging rail takes 2-4 inputs, got {len(inputs)}")

    def compose(cv):
        y = cv.head_h
        if slots.get("inputs_label"):
            # The label goes above the band it introduces, never under the
            # arrows, which would make them read as pointing at the label.
            cv.add(band_label(cv.m, y, slots["inputs_label"], cv.sc, cv.t))
            y += cv.sc.s + 12

        gap = 20
        cols = len(inputs) if cv.ratio == "wide" else min(2, len(inputs))
        boxes = to_boxes(inputs)
        bw = (cv.inner_w - gap * (cols - 1)) / cols
        stems, bottom = [], y
        for i in range(0, len(boxes), cols):
            band = boxes[i:i + cols]
            bh = max(b.height(bw, cv.sc) for b in band)
            x = cv.m
            for b in band:
                cv.add(b.draw(x, bottom, bw, bh, cv.sc, cv.t))
                x += bw + gap
            bottom += bh
            if i + cols < len(boxes):
                bottom += gap
        for c in range(cols):
            stems.append(cv.m + c * (bw + gap) + bw / 2)

        rail_y = bottom + 18
        cv.add(rail(stems[0], stems[-1], rail_y, cv.t,
                    stems=stems, stem_from=bottom))
        target = to_boxes([slots["target"]])[0]
        ty = rail_y + 30
        cv.add(arrow_down(cv.W / 2, rail_y, ty - 4, cv.t))
        tw = cv.inner_w if cv.ratio == "tall" else cv.inner_w * 0.62
        tx = cv.m + (cv.inner_w - tw) / 2
        th = target.height(tw, cv.sc)
        cv.add(target.draw(tx, ty, tw, th, cv.sc, cv.t))
        y = ty + th
        if slots.get("note"):
            y = note_row(cv, y, slots["note"])
        if slots.get("effects"):
            y = effect_row(cv, to_boxes(slots["effects"], kind="effect"), y + 22)
        return y

    return build_fitted(ratio, slots["title"], slots.get("subtitle"),
                        theme_name, provenance(FORM, mode=mode), compose,
                        path, w=w, h=h, base_lock=base_lock)
