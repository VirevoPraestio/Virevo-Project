"""Form: role cards plus an approver box — who has to cooperate.

Cards for the people who do the work; the approver gets its own bordered box
with a tag, because approving is a different act from doing. An approver outside
the daily routine is easy to leave out of the plan, and is usually the reason a
change does not survive its first difficult day — so the form will not let the
approver be drawn as one more doer.

Where a role is being asked to give something up, say what, and quantify the ask
even when the honest number is zero.

SLOTS
  title, subtitle   str
  roles             list of 2-5:
                      {"title": str, "asked": str, "caption": str,
                       "resistant": bool}    the group with most to lose
  approver          {"title": str, "values": [str, ...], "caption": str,
                     "tag": str}
  fails_if          str | None   what fails if the approval never comes
  effects           list of effect dicts, 0-3
"""

from core import Box, LayoutError, build_fitted, provenance
from layout import effect_row, note as note_row, row, to_boxes

FORM = "role-cards"


def build(slots, ratio, theme_name, path, *, w=None, h=None, base_lock=None,
          mode="tpl"):
    roles = slots["roles"]
    if not 2 <= len(roles) <= 5:
        raise LayoutError(f"role cards takes 2-5 roles, got {len(roles)}")
    if not slots.get("approver"):
        raise LayoutError(
            "this form requires an approver — if nobody has to approve, the "
            "content is a plain set of cards, not a role map")

    def compose(cv):
        boxes = [Box(r["title"], [r.get("asked", "")],
                     state="target" if r.get("resistant") else "plain",
                     tag="MOST TO LOSE" if r.get("resistant") else None,
                     caption=r.get("caption"))
                 for r in roles]
        n = len(boxes)
        cols = (n if n <= 3 else 2) if cv.ratio == "wide" else min(2, n)
        y, gap = cv.head_h, 20
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

        a = slots["approver"]
        ap = Box(a["title"], a.get("values", ()), state="start",
                 tag=a.get("tag", "APPROVES"), caption=a.get("caption"))
        aw = cv.inner_w if cv.ratio == "tall" else cv.inner_w * 0.7
        ax = cv.m + (cv.inner_w - aw) / 2
        y += 26
        ah = ap.height(aw, cv.sc)
        cv.add(ap.draw(ax, y, aw, ah, cv.sc, cv.t))
        y += ah
        if slots.get("fails_if"):
            y = note_row(cv, y, slots["fails_if"])
        if slots.get("effects"):
            y = effect_row(cv, to_boxes(slots["effects"], kind="effect"), y + 22)
        return y

    return build_fitted(ratio, slots["title"], slots.get("subtitle"),
                        theme_name, provenance(FORM, mode=mode), compose,
                        path, w=w, h=h, base_lock=base_lock)
