"""Form: cards (plus an optional effect box) — a set of independent items.

Options, areas of enquiry, findings, roles, parts. No arrows: arrows between
things that are not sequential are a lie about the content. Also serves as the
agenda grid, with the card you are starting from carrying a `start` state and a
short tag.

SLOTS
  title       str
  subtitle    str
  cards       list of {title, values[], state?, tag?, badge?, caption?}   2-6
  columns     int | None    override the automatic column count
  note        str | None    dashed divider caption beneath the grid
  effects     list of {title, values[], caption?}   0-3 effect boxes
"""

from core import LayoutError, build_fitted, provenance
from layout import effect_row, note as note_row, row, to_boxes

FORM = "cards"


def _columns(n, ratio, override):
    if override:
        return override
    if ratio == "wide":
        return n if n <= 3 else (2 if n == 4 else 3)
    return 1 if n <= 3 else 2


def build(slots, ratio, theme_name, path, *, w=None, h=None, base_lock=None,
          mode="tpl"):
    cards = slots["cards"]
    if not 2 <= len(cards) <= 6:
        raise LayoutError(f"cards takes 2-6 items, got {len(cards)} — split the "
                          f"graphic rather than shrinking the cards")

    def compose(cv):
        cols = _columns(len(cards), cv.ratio, slots.get("columns"))
        boxes = to_boxes(cards)
        y, gap = cv.head_h, 22
        for i in range(0, len(boxes), cols):
            band = boxes[i:i + cols]
            if len(band) < cols:        # short final row keeps the column width
                bw = (cv.inner_w - gap * (cols - 1)) / cols
                h_ = max(b.height(bw, cv.sc) for b in band)
                x = cv.m
                for b in band:
                    cv.add(b.draw(x, y, bw, h_, cv.sc, cv.t))
                    x += bw + gap
                y += h_
            else:
                y = row(cv, band, y, gap=gap, arrows=False)
            if i + cols < len(boxes):
                y += gap
        if slots.get("note"):
            y = note_row(cv, y, slots["note"])
        if slots.get("effects"):
            y = effect_row(cv, to_boxes(slots["effects"], kind="effect"), y + 22)
        return y

    return build_fitted(ratio, slots["title"], slots.get("subtitle"),
                        theme_name, provenance(FORM, mode=mode), compose,
                        path, w=w, h=h, base_lock=base_lock)
