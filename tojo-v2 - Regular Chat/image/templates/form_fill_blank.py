"""Form: fill-in-the-blank → filled — handing someone a structure to complete.

The same layout with a dashed blank field per step; when the answers come back,
the same layout and the same coordinates are redrawn with the values in. The
visual continuity is the point: same diagram, now answered.

Coordinates are guaranteed identical, not merely intended to be. The blank build
returns its geometry; the filled build is passed that geometry back, so the fit
search cannot quietly choose a different canvas for the answered version. The
blank reserves exactly the height a value line will occupy, so nothing moves
when the value lands in it.

Theme continuity is the other half: the filled redraw keeps the theme the blank
was drawn in, via tokens.pick_theme(..., continuity_of=<the blank's index>).

SLOTS
  title, subtitle   str
  steps             list of {"title": str, "hint": str, "value": str | None}
                      `value` present and `filled=True` renders the answered state
  filled            bool
  note              str | None
  effects           list of effect dicts, 0-3
"""

from core import (BOX_PAD_X, Box, LayoutError, arrow, arrow_down, blank_field,
                  build_fitted, provenance)
from layout import effect_row, note as note_row, to_boxes

FORM = "fill-in-the-blank"


def _boxes(steps, filled):
    out = []
    for s in steps:
        if filled:
            if not s.get("value"):
                raise LayoutError(f"step {s['title']!r} has no value to fill in")
            out.append(Box(s["title"], [s["value"]], caption=s.get("hint")))
        else:
            # A single space holds exactly one value line's height, so the
            # answered redraw lands on the same coordinates.
            out.append(Box(s["title"], [" "], caption=s.get("hint")))
    return out


def build(slots, ratio, theme_name, path, *, w=None, h=None, base_lock=None,
          mode="tpl"):
    steps = slots["steps"]
    filled = bool(slots.get("filled"))
    if not 2 <= len(steps) <= 5:
        raise LayoutError(f"fill-in-the-blank takes 2-5 steps, got {len(steps)}")
    if filled and not (w and h and base_lock):
        raise LayoutError(
            "the filled state must be built with the blank state's geometry — "
            "pass w, h and base_lock from the blank build's return value, or "
            "the two diagrams will not share coordinates")

    def compose(cv):
        boxes = _boxes(steps, filled)
        y = cv.head_h
        if cv.ratio == "wide":
            gap = 28
            bw = (cv.inner_w - gap * (len(boxes) - 1)) / len(boxes)
            if bw < 150:
                raise LayoutError(f"{len(boxes)} steps leaves {bw:.0f}px each")
            bh = max(b.height(bw, cv.sc) for b in boxes)
            for i, b in enumerate(boxes):
                x = cv.m + i * (bw + gap)
                cv.add(b.draw(x, y, bw, bh, cv.sc, cv.t))
                if not filled:
                    # On the value line the answer will occupy, not at the
                    # box's midpoint — the hint sits below it.
                    vy, vh = b.slot("value")
                    cv.add(blank_field(x + BOX_PAD_X / 2 + 6, vy - 3,
                                       bw - BOX_PAD_X - 12, vh + 6, cv.t))
                if i < len(boxes) - 1:
                    cv.add(arrow(x + bw + 6, x + bw + gap - 6,
                                 y + bh / 2, cv.t))
            y += bh
        else:
            gap = 24
            for i, b in enumerate(boxes):
                bh = b.height(cv.inner_w, cv.sc)
                cv.add(b.draw(cv.m, y, cv.inner_w, bh, cv.sc, cv.t))
                if not filled:
                    vy, vh = b.slot("value")
                    cv.add(blank_field(cv.m + cv.inner_w * 0.25, vy - 3,
                                       cv.inner_w * 0.5, vh + 6, cv.t))
                y += bh
                if i < len(boxes) - 1:
                    cv.add(arrow_down(cv.m + cv.inner_w / 2, y + 4,
                                      y + gap - 2, cv.t))
                    y += gap
        if slots.get("note"):
            y = note_row(cv, y, slots["note"])
        if slots.get("effects"):
            y = effect_row(cv, to_boxes(slots["effects"], kind="effect"), y + 22)
        return y

    return build_fitted(ratio, slots["title"], slots.get("subtitle"),
                        theme_name, provenance(FORM, mode=mode), compose,
                        path, w=w, h=h, base_lock=base_lock)
