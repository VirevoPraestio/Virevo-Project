"""Form: two-flow comparison — two genuinely parallel flows.

Side by side in columns on **both** ratios, with rows height-matched so they stay
comparable step for step. On the tall ratio that means two narrower columns
running slightly taller, never one flow stacked above the other.

Check first whether the flows actually share most of their steps. If they do,
this is the wrong form — use the merged shared flow, which is clearer and
smaller at the same time.

SLOTS
  title, subtitle   str
  flows             list of exactly 2:
                      {"label": str, "steps": [box dict, ...]}
  note              str | None
  effects           list of effect dicts, 0-3
"""

from core import (LayoutError, arrow_down, band_label, build_fitted,
                  provenance)
from layout import effect_row, note as note_row, to_boxes

FORM = "two-flow"


def build(slots, ratio, theme_name, path, *, w=None, h=None, base_lock=None,
          mode="tpl"):
    flows = slots["flows"]
    if len(flows) != 2:
        raise LayoutError("two-flow compares exactly two flows")
    if len({len(f["steps"]) for f in flows}) != 1:
        raise LayoutError(
            "the two flows have different step counts — pad the shorter one "
            "with the step it actually lacks, or use the merged shared flow")

    def compose(cv):
        gap = 26 if cv.ratio == "wide" else 18
        cw = (cv.inner_w - gap) / 2
        if cw < 150:
            raise LayoutError(f"two columns leave {cw:.0f}px each")
        y = cv.head_h
        for i, f in enumerate(flows):
            cv.add(band_label(cv.m + i * (cw + gap), y, f["label"],
                              cv.sc, cv.t))
        y += cv.sc.s + 12

        cols = [to_boxes(f["steps"]) for f in flows]
        n = len(cols[0])
        arrow_gap = 22
        for r in range(n):
            pair = [c[r] for c in cols]
            rh = max(b.height(cw, cv.sc) for b in pair)   # rows stay comparable
            for i, b in enumerate(pair):
                cv.add(b.draw(cv.m + i * (cw + gap), y, cw, rh, cv.sc, cv.t))
            y += rh
            if r < n - 1:
                for i in range(2):
                    cv.add(arrow_down(cv.m + i * (cw + gap) + cw / 2,
                                      y + 4, y + arrow_gap - 2, cv.t))
                y += arrow_gap
        if slots.get("note"):
            y = note_row(cv, y, slots["note"])
        if slots.get("effects"):
            y = effect_row(cv, to_boxes(slots["effects"], kind="effect"), y + 22)
        return y

    return build_fitted(ratio, slots["title"], slots.get("subtitle"),
                        theme_name, provenance(FORM, mode=mode), compose,
                        path, w=w, h=h, base_lock=base_lock)
