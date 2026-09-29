"""Form: agenda grid — what you are about to establish, and what is left.

One card per area, each labelled with **the question it answers** rather than a
title alone, and the card you are starting from marked. A turn whose text is a
single question can still carry one of these honestly: it is the agenda, not the
questions, and it shows the person where the sequence is going so it does not
feel like an interrogation.

It doubles as the progress view. When someone asks what is left, re-showing the
overview breaches the no-replay rule and carries nothing new; mark the covered
areas `covered` instead and the same grid becomes the answer, with the remaining
ones still readable as choices.

SLOTS
  title, subtitle   str
  areas             list of 2-6:
                      {"title": str,
                       "question": str,      the question this area answers
                       "start": bool,        where you are beginning
                       "covered": bool}      already done — renders muted, ticked
  columns           int | None
  note              str | None
  effects           list of effect dicts, 0-3
"""

from core import Box, LayoutError, build_fitted, provenance
from layout import effect_row, note as note_row, row, to_boxes

FORM = "agenda-grid"


def build(slots, ratio, theme_name, path, *, w=None, h=None, base_lock=None,
          mode="tpl"):
    areas = slots["areas"]
    if not 2 <= len(areas) <= 6:
        raise LayoutError(f"agenda grid takes 2-6 areas, got {len(areas)}")
    if sum(bool(a.get("start")) for a in areas) > 1:
        raise LayoutError("only one area can be the one you are starting from")

    def _box(a):
        if a.get("covered"):
            return Box(a["title"], [a["question"]], kind="muted",
                       badge=("tick", "Covered"))
        return Box(a["title"], [a["question"]],
                   state="start" if a.get("start") else "plain",
                   tag="START HERE" if a.get("start") else None)

    def compose(cv):
        boxes = [_box(a) for a in areas]
        n = len(boxes)
        cols = slots.get("columns") or (
            (n if n <= 3 else (2 if n == 4 else 3)) if cv.ratio == "wide"
            else (1 if n <= 3 else 2))
        y, gap = cv.head_h, 22
        for i in range(0, n, cols):
            band = boxes[i:i + cols]
            if len(band) < cols:
                bw = (cv.inner_w - gap * (cols - 1)) / cols
                bh = max(b.height(bw, cv.sc) for b in band)
                x = cv.m
                for b in band:
                    cv.add(b.draw(x, y, bw, bh, cv.sc, cv.t))
                    x += bw + gap
                y += bh
            else:
                y = row(cv, band, y, gap=gap, arrows=False)
            if i + cols < n:
                y += gap
        if slots.get("note"):
            y = note_row(cv, y, slots["note"])
        if slots.get("effects"):
            y = effect_row(cv, to_boxes(slots["effects"], kind="effect"), y + 22)
        return y

    return build_fitted(ratio, slots["title"], slots.get("subtitle"),
                        theme_name, provenance(FORM, mode=mode), compose,
                        path, w=w, h=h, base_lock=base_lock)
