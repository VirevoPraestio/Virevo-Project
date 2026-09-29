"""Form: merged shared flow — two flows that turn out to share most of their steps.

One chain rather than two near-identical rows. Steps identical across both flows
render once; steps identical in title but different in value render once with
stacked per-flow values; a step that exists on only one path takes a dashed
border and a bypass arc showing where the other path skips ahead and rejoins.

Clearer and smaller at the same time — try it before reaching for a bigger
canvas or a non-standard ratio.

SLOTS
  title, subtitle   str
  flows             list of 2 short labels, e.g. ["Ins", "Cash"]
  steps             list of:
                      {"title": str,
                       "value": str,            shared value, or
                       "values": [str, str],    one per flow, stacked
                       "only_on": str | None,   a flow label: dashed + bypassed
                       "bypass": str | None,    caption on the arc
                       "state", "tag", "caption"}
  note              str | None
  effects           list of effect dicts, 0-3
"""

from core import (Box, LayoutError, arrow, arrow_down, build_fitted,
                  bypass_arc, provenance)
from layout import effect_row, note as note_row, to_boxes

FORM = "merged-shared-flow"
CLEAR = 26


def _boxes(steps, flows):
    out = []
    for s in steps:
        if s.get("values"):
            vals = [f"{flows[i]} {v}" for i, v in enumerate(s["values"])]
        else:
            vals = [s["value"]] if s.get("value") else []
        out.append(Box(s["title"], vals,
                       state="dashed" if s.get("only_on") else
                             s.get("state", "plain"),
                       tag=s.get("tag"), caption=s.get("caption")))
    return out


def build(slots, ratio, theme_name, path, *, w=None, h=None, base_lock=None,
          mode="tpl"):
    steps, flows = slots["steps"], slots["flows"]
    if len(flows) != 2:
        raise LayoutError("a merged shared flow merges exactly two flows")
    for i, s in enumerate(steps):
        if s.get("only_on") and i in (0, len(steps) - 1):
            raise LayoutError("a bypassed step needs a step on each side of it "
                              "for the arc to leave from and rejoin at")

    def compose(cv):
        boxes = _boxes(steps, flows)
        has_bypass = any(s.get("only_on") for s in steps)
        y = cv.head_h
        if has_bypass:
            y += CLEAR + cv.sc.cap + 10      # head room for the arc and its label

        if cv.ratio == "wide":
            gap = 30
            bw = (cv.inner_w - gap * (len(boxes) - 1)) / len(boxes)
            if bw < 150:
                raise LayoutError(f"{len(boxes)} steps leaves {bw:.0f}px each")
            bh = max(b.height(bw, cv.sc) for b in boxes)
            xs = [cv.m + i * (bw + gap) for i in range(len(boxes))]
            for i, b in enumerate(boxes):
                cv.add(b.draw(xs[i], y, bw, bh, cv.sc, cv.t))
                if i < len(boxes) - 1:
                    cv.add(arrow(xs[i] + bw + 6, xs[i] + bw + gap - 6,
                                 y + bh / 2, cv.t))
            for i, s in enumerate(steps):
                if s.get("only_on"):
                    other = [f for f in flows if f != s["only_on"]]
                    svg, _ = bypass_arc(xs[i - 1] + bw / 2, xs[i + 1] + bw / 2,
                                        y, CLEAR,
                                        s.get("bypass") or
                                        f"{other[0] if other else 'other'} skips",
                                        cv.sc, cv.t)
                    cv.add(svg)
            y += bh
        else:
            reserve = 44 if has_bypass else 0
            bw = cv.inner_w - reserve
            gap = 24
            ys = []
            for i, b in enumerate(boxes):
                bh = b.height(bw, cv.sc)
                ys.append((y, bh))
                cv.add(b.draw(cv.m, y, bw, bh, cv.sc, cv.t))
                y += bh
                if i < len(boxes) - 1:
                    cv.add(arrow_down(cv.m + bw / 2, y + 4, y + gap - 2, cv.t))
                    y += gap
            for i, s in enumerate(steps):
                if s.get("only_on"):
                    x = cv.m + bw
                    y1 = ys[i - 1][0] + ys[i - 1][1] / 2
                    y2 = ys[i + 1][0] + ys[i + 1][1] / 2
                    c = cv.t["arrow"]
                    cv.add(f'<path d="M{x:.0f} {y1:.0f}Q{x + reserve:.0f} '
                           f'{(y1 + y2) / 2:.0f} {x:.0f} {y2:.0f}" '
                           f'stroke="{c}" stroke-width="1.6" fill="none" '
                           f'stroke-dasharray="5 4"/>')
        if slots.get("note"):
            y = note_row(cv, y, slots["note"])
        if slots.get("effects"):
            y = effect_row(cv, to_boxes(slots["effects"], kind="effect"), y + 22)
        return y

    return build_fitted(ratio, slots["title"], slots.get("subtitle"),
                        theme_name, provenance(FORM, mode=mode), compose,
                        path, w=w, h=h, base_lock=base_lock)
