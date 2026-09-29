"""Form: fork / branch — one question, several alternative answers.

A rail splitting into arrows on the wide ratio. On the tall ratio the branches
stack with a small "or" between them rather than chaining with arrows, which
would misread as a sequence.

Two neutral options beat one leading question: where the point is to find out
which pattern someone is in, draw both and let them place themselves.

SLOTS
  title, subtitle   str
  question          box dict — the thing that branches
  branches          list of box dicts, 2-4
  note              str | None
  effects           list of effect dicts, 0-3
"""

from core import (LayoutError, arrow_down, build_fitted, esc, provenance,
                  rail)
from layout import effect_row, note as note_row, to_boxes

FORM = "fork"


def build(slots, ratio, theme_name, path, *, w=None, h=None, base_lock=None,
          mode="tpl"):
    branches = slots["branches"]
    if not 2 <= len(branches) <= 4:
        raise LayoutError(f"fork takes 2-4 branches, got {len(branches)}")

    def compose(cv):
        y = cv.head_h
        q = to_boxes([slots["question"]])[0]
        qw = cv.inner_w if cv.ratio == "tall" else cv.inner_w * 0.6
        qx = cv.m + (cv.inner_w - qw) / 2
        qh = q.height(qw, cv.sc)
        cv.add(q.draw(qx, y, qw, qh, cv.sc, cv.t))
        y += qh

        boxes = to_boxes(branches)
        if cv.ratio == "wide":
            gap = 22
            bw = (cv.inner_w - gap * (len(boxes) - 1)) / len(boxes)
            if bw < 150:
                raise LayoutError(f"{len(boxes)} branches leaves {bw:.0f}px each")
            centres = [cv.m + i * (bw + gap) + bw / 2 for i in range(len(boxes))]
            rail_y = y + 22
            cv.add(arrow_down(cv.W / 2, y + 4, rail_y + 2, cv.t))
            cv.add(rail(centres[0], centres[-1], rail_y, cv.t))
            by = rail_y + 30
            for c in centres:
                cv.add(arrow_down(c, rail_y, by - 4, cv.t))
            bh = max(b.height(bw, cv.sc) for b in boxes)
            for i, b in enumerate(boxes):
                cv.add(b.draw(cv.m + i * (bw + gap), by, bw, bh, cv.sc, cv.t))
            y = by + bh
        else:
            y += 14
            for i, b in enumerate(boxes):
                bh = b.height(cv.inner_w, cv.sc)
                cv.add(b.draw(cv.m, y, cv.inner_w, bh, cv.sc, cv.t))
                y += bh
                if i < len(boxes) - 1:
                    y += cv.sc.cap + 10
                    cv.add(f'<text x="{cv.W / 2:.0f}" y="{y:.0f}" class="i" '
                           f'fill="{cv.t["caption"]}" font-size="{cv.sc.cap}">'
                           f'{esc("or")}</text>')
                    y += 10
        if slots.get("note"):
            y = note_row(cv, y, slots["note"])
        if slots.get("effects"):
            y = effect_row(cv, to_boxes(slots["effects"], kind="effect"), y + 22)
        return y

    return build_fitted(ratio, slots["title"], slots.get("subtitle"),
                        theme_name, provenance(FORM, mode=mode), compose,
                        path, w=w, h=h, base_lock=base_lock)
