"""Form: chain — a sequence.

Horizontal on the wide ratio, vertical on the tall one. The final box is marked
as the outcome. Use when the content is a process, a sequence or a before/after.

SLOTS
  title       str
  subtitle    str
  steps       list of {title, values[], state?, tag?, badge?, caption?}
                one to five; six or more belongs to the wrapped-chain form
  note        str | None      dashed divider caption spanning the sequence
  effects     list of {title, values[], caption?}   0-3 effect/parameter boxes
"""

from core import LayoutError, build_fitted, provenance
from layout import column, effect_row, note as note_row, row, to_boxes

FORM = "chain"
MAX_STEPS = 5


def build(slots, ratio, theme_name, path, *, w=None, h=None, base_lock=None,
          mode="tpl"):
    steps = slots["steps"]
    if not 1 <= len(steps) <= MAX_STEPS:
        raise LayoutError(
            f"chain takes 1-{MAX_STEPS} steps, got {len(steps)} — use the "
            f"wrapped-chain form; a single row of six forces unreadably "
            f"narrow boxes")

    def compose(cv):
        y = cv.head_h
        y = (row(cv, to_boxes(steps), y) if cv.ratio == "wide"
             else column(cv, to_boxes(steps), y))
        if slots.get("note"):
            y = note_row(cv, y, slots["note"])
        if slots.get("effects"):
            y = effect_row(cv, to_boxes(slots["effects"], kind="effect"), y + 22)
        return y

    return build_fitted(ratio, slots["title"], slots.get("subtitle"),
                        theme_name, provenance(FORM, mode=mode), compose,
                        path, w=w, h=h, base_lock=base_lock)
