"""Form: wrapped chain — a sequence too long for one row.

Wrap it and join the rows with an elbow connector out of the last box, across,
and down into the first box of the next row. A single row of six leaves most of
a wide canvas empty and forces unreadably narrow boxes.

On the tall ratio a long sequence is simply a column; there is nothing to wrap.

SLOTS
  title, subtitle   str
  steps             list of step dicts (same shape as chain), 4-12
  per_row           int | None    override the automatic row width
  note              str | None
  effects           list of effect dicts, 0-3
"""

from core import LayoutError, build_fitted, elbow, provenance
from layout import ARROW_GAP, column, effect_row, note as note_row, to_boxes

FORM = "wrapped-chain"


def _per_row(n, override):
    if override:
        return override
    if n <= 6:
        return (n + 1) // 2         # 4->2, 5->3, 6->3
    return (n + 2) // 3


def build(slots, ratio, theme_name, path, *, w=None, h=None, base_lock=None,
          mode="tpl"):
    steps = slots["steps"]
    if not 4 <= len(steps) <= 12:
        raise LayoutError(f"wrapped chain takes 4-12 steps, got {len(steps)}")

    def compose(cv):
        y = cv.head_h
        if cv.ratio == "tall":
            y = column(cv, to_boxes(steps), y)
        else:
            per = _per_row(len(steps), slots.get("per_row"))
            gap = ARROW_GAP["wide"]
            bw = (cv.inner_w - gap * (per - 1)) / per
            if bw < 150:
                raise LayoutError(f"{per} boxes per row leaves {bw:.0f}px each")
            boxes = to_boxes(steps)
            rows = [boxes[i:i + per] for i in range(0, len(boxes), per)]
            row_gap = 46
            for ri, band in enumerate(rows):
                bh = max(b.height(bw, cv.sc) for b in band)
                x = cv.m
                from core import arrow
                for bi, b in enumerate(band):
                    cv.add(b.draw(x, y, bw, bh, cv.sc, cv.t))
                    if bi < len(band) - 1:
                        cv.add(arrow(x + bw + 6, x + bw + gap - 6,
                                     y + bh / 2, cv.t))
                    x += bw + gap
                if ri < len(rows) - 1:
                    last_cx = cv.m + (len(band) - 1) * (bw + gap) + bw / 2
                    cv.add(elbow(last_cx, y + bh, cv.m + bw / 2,
                                 y + bh + row_gap, cv.t,
                                 mid=y + bh + row_gap / 2))
                    y += bh + row_gap
                else:
                    y += bh
        if slots.get("note"):
            y = note_row(cv, y, slots["note"])
        if slots.get("effects"):
            y = effect_row(cv, to_boxes(slots["effects"], kind="effect"), y + 22)
        return y

    return build_fitted(ratio, slots["title"], slots.get("subtitle"),
                        theme_name, provenance(FORM, mode=mode), compose,
                        path, w=w, h=h, base_lock=base_lock)
