"""Form: derivation chain — arithmetic, shown as working rather than as a total.

One box per step carrying the input and the result, the answer as the final box
marked as the outcome, the condition under which the number holds on a divider
beneath, and the consequences as effect boxes. Use whenever a quantity becomes a
headline number: the person audits the steps instead of being handed a total.

SLOTS
  title       str
  subtitle    str
  steps       list of {title, input, result, state?, tag?}   2-5
  condition   str        the capturability / basis condition (required)
  outputs     list of {title, values[], caption?}            1-3 effect boxes
  answer      {title, values[], caption?} | None
                optional explicit final box; otherwise the last step is the
                outcome

Evidence discipline this form encodes:
  * a step whose figure is derived rather than measured says so in its caption
  * the condition line is required, because a derivation without its basis is
    a total with extra steps
"""

from core import LayoutError, build_fitted, provenance
from layout import column, effect_row, note as note_row, row, to_boxes

FORM = "derivation-chain"


def build(slots, ratio, theme_name, path, *, w=None, h=None, base_lock=None,
          mode="tpl"):
    steps = list(slots["steps"])
    if not 2 <= len(steps) <= 5:
        raise LayoutError(f"derivation chain takes 2-5 steps, got {len(steps)}")
    if not slots.get("condition"):
        raise LayoutError(
            "derivation chain requires `condition` — the basis the number holds "
            "on. A derivation without its basis is a total with extra steps.")

    specs = []
    for s in steps:
        specs.append({"title": s["title"],
                      "values": [s.get("input"), s.get("result")],
                      "state": s.get("state", "plain"),
                      "tag": s.get("tag"), "caption": s.get("caption")})
    if slots.get("answer"):
        a = slots["answer"]
        specs.append({"title": a["title"], "values": a.get("values", ()),
                      "state": "outcome", "tag": a.get("tag"),
                      "caption": a.get("caption")})
    elif specs[-1]["state"] == "plain":
        specs[-1]["state"] = "outcome"

    def compose(cv):
        y = cv.head_h
        y = (row(cv, to_boxes(specs), y, gap=26) if cv.ratio == "wide"
             else column(cv, to_boxes(specs), y))
        y = note_row(cv, y, slots["condition"])
        return effect_row(cv, to_boxes(slots.get("outputs", []), kind="effect"),
                          y + 20)

    return build_fitted(ratio, slots["title"], slots.get("subtitle"),
                        theme_name, provenance(FORM, mode=mode), compose,
                        path, w=w, h=h, base_lock=base_lock)
