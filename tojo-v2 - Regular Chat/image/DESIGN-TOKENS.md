# Tojo Image System v2 — Design Tokens and Templates

The visual specification for every graphic Tojo produces from a template. It sits
under `02-image-creation-rules` rather than replacing it: the rules say *what a
graphic must contain and when one is warranted*; this file says *what it looks
like and how it is built*.

Nothing here is a new visual idea. The palette, the border-colour vocabulary and
the effect-box treatment are the ones already in use, given names and verified.
What is new is that they are now values in one file instead of literals repeated
across build scripts, and that a renderer applies them rather than a model
remembering them.

---

## 1. Why templates, and what stays freehand

A hand-drawn SVG follows the grammar by remembering it, and fails silently when
it forgets. Ten of the build-discipline rules exist because a hand-drawn figure
broke in ten specific ways — a fixed offset meeting content that varied, a tag
colliding with a taller title, a wrapped caption leaving its box, a stat card
pushed past the canvas edge. A renderer cannot break those rules, because the
geometry is computed rather than estimated.

So graphics come from one of two places, and the image says which:

- **Template.** A named form with a declared set of slots. The model supplies the
  content; the renderer supplies every coordinate, size and colour.
- **Freehand.** The escape hatch, for a layout no form covers. Kept deliberately,
  logged every time. Each logged escape is a candidate for the next form, and the
  escape rate measures how much freehand capability is genuinely needed rather
  than assumed.

The rules clause that carries this distinction into `02` is in Appendix A.

---

## 2. Colour

### 2.1 Two themes, one set of roles

Every colour is a **role**, not a hue. The two themes assign different values to
the same roles; no renderer refers to a hex value.

The roles are arranged so the two themes are genuine tonal inversions rather than
the same picture on a different background:

| | night | day |
|---|---|---|
| Canvas | deep navy | near-white blue-grey |
| Process box | navy fill, light text | white fill, navy text |
| Effect / parameter box | **light fill, dark text** | **navy fill, light text** |

The effect box is always the tonal opposite of the process boxes around it. That
is what makes it read as a different *kind* of object at a glance, and it holds in
either theme — the distinction survives the flip instead of depending on it.

### 2.2 The tokens

**night**

| Role | Value | Used for |
|---|---|---|
| `canvas` | `#0f2740` | page background |
| `h1` / `sub` | `#ffffff` / `#9fb8cf` | page title, subtitle |
| `caption` | `#9fb8cf` | divider captions, box captions |
| `footer` | `#6d88a3` | provenance mark |
| `divider` | `#3a5f84` | dashed phase/condition rule |
| `arrow` | `#7be0b8` | connectors |
| `proc_fill` / `proc_stroke` | `#1c3f61` / `#2c5580` | process-step box |
| `proc_title` / `proc_value` | `#eaf1f8` / `#7be0b8` | box title, box value |
| `muted_fill` / `muted_stroke` | `#16324f` / `#244562` | present but not the subject |
| `muted_title` / `muted_value` | `#93aec6` | dimmed **with** the fill, never alone |
| `effect_fill` / `effect_stroke` | `#d9dde3` / `#aab2bc` | effect / parameter box |
| `effect_label` / `effect_value` / `effect_cap` | `#0f2740` / `#7a4f00` / `#43505e` | its label, value, caption |
| `state_target` | `#ffb400` | a target, not yet measured |
| `state_outcome` | `#ff8b82` | the headline result |
| `state_start` | `#7be0b8` | where to begin |

**day**

| Role | Value |
|---|---|
| `canvas` | `#f1f5f9` |
| `h1` / `sub` | `#0f2740` / `#4d6076` |
| `caption` | `#4d6076` |
| `footer` | `#71839a` |
| `divider` | `#a6b8cb` |
| `arrow` | `#0c6b4f` |
| `proc_fill` / `proc_stroke` | `#ffffff` / `#b0c0d1` |
| `proc_title` / `proc_value` | `#0f2740` / `#0c6b4f` |
| `muted_fill` / `muted_stroke` | `#e4eaf1` / `#cfd9e4` |
| `muted_title` / `muted_value` | `#57687d` |
| `effect_fill` / `effect_stroke` | `#0f2740` / `#2c5580` |
| `effect_label` / `effect_value` / `effect_cap` | `#b9cee0` / `#f0b74a` / `#9fb8cf` |
| `state_target` | `#9a6205` |
| `state_outcome` | `#b7352b` |
| `state_start` | `#0c6b4f` |

Purple and indigo are not in the system. They were tried for effect boxes and
rejected; the light-fill / strong-value treatment is the standard.

### 2.3 What each colour means

**Border colour carries state**, and only these five exist. Before adding a
sixth, check that none of these already carries the intent.

| State | Border | Meaning |
|---|---|---|
| `plain` | `proc_stroke` | confirmed, or unchanged |
| `target` | `state_target` | a target, not yet measured, or the thing needing attention |
| `outcome` | `state_outcome` | the headline result — the value text turns with it |
| `start` | `state_start` | where to begin |
| `dashed` | `proc_stroke`, dashed | exists on only some paths |

**Fill carries box type**: `process`, `muted`, `effect`. A muted box dims its
text along with its fill — dimming the container alone leaves the text at full
weight and the box still reads as lit. Muted means receded, never hard to read,
so the dimmed text is still held above 4.5:1 against its own fill.

**A tag takes its box's border colour.** A green tag on an amber box reads
wrongly, so the tag colour is derived from the state rather than passed in.

### 2.4 Contrast is verified, not judged

`templates/contrast_check.py` computes the WCAG ratio for every text-on-fill pair
the system can produce, in both themes, and exits non-zero on a failure. Body
text must clear 4.5:1; borders and rules have their own lower floors for
non-text separation. Run it after any palette edit — three of the values above
are the corrected versions of colours that looked fine and measured under.

---

## 3. Type

```
Poppins, 'Segoe UI', Verdana, sans-serif
```

Declared, never embedded. Poppins for viewers that have it, a plain sans
fallback for those that don't.

**One variable drives everything.** Box titles, box values, section labels and
effect-box label and value all render at the base size `s`, so they cannot drift
apart. Every other size is derived from it:

| Element | Size | Weight |
|---|---|---|
| Page title | `1.75 × s` | 700 |
| Page subtitle | `1.05 × s` | 400 |
| Box title | `s` | 600 |
| Box value | `s` | 700 |
| Section label | `s` | 500 |
| Effect label / value | `s` | 500 / 700 |
| Caption, badge caption | `0.82 × s`, min 10 | 400 |
| Provenance footer | `0.72 × s`, min 9 | 400 |

Captions are the single exception to the one-variable rule. They are secondary
content and stay visually smaller.

`s` starts at 13 on the wide ratio and 16 on the tall one, and the fit search may
raise it by up to 4 to fill a canvas the ratio has made taller than the content
needs (§4.2). It is never lowered to make content fit — that is the byte-ceiling
mistake in a different costume.

### 3.1 Measuring

Width is estimated at `0.60 × font size` per character, deliberately wider than
the tightest plausible figure, with 24px of combined internal padding taken out
of a box before a line is judged to fit. A local QA render can use a narrower
fallback font than the one that reaches the reader, so a line that measures as
fitting can still overflow in production; the margin is what absorbs that.

The estimate cannot split a word. A single word too wide for its container raises
at build time rather than being discovered in the render.

---

## 4. Geometry

### 4.1 Ratios

Two files per graphic, always: **wide 5:3** (desktop) and **tall 3:4** (mobile).
Pixel size within the ratio is free; the ratio is not.

### 4.2 The canvas is searched, not chosen

The renderer does not pick a canvas size and live with the dead space. It
searches candidate widths and type sizes, composes the graphic at each, and keeps
the combination the content most nearly fills — preferring, among equals, the
smaller canvas and the larger type. Whatever height the ratio still forces beyond
what the content needs is split above and below the body, so the page reads as
composed rather than as content that ran out.

Two floors bound the search. A row refuses to make boxes narrower than 150px,
because below that every title wraps into a column of single words. And the fit
assertion is hard: content that would overrun the canvas raises with a message
naming the overrun, rather than clipping silently.

| Constant | Value |
|---|---|
| Margin | 40px wide · 60px tall |
| Box internal padding | 24px horizontal (combined) · 10px vertical |
| Corner radius | 8px |
| Minimum box width in a row | 150px |
| Arrow gap | 30px wide · 26px tall |
| Canvas search range | 880–1480px wide · 660–1140px tall |
| Type headroom | +4 on the base size |

### 4.3 Boxes size themselves

One pass computes a box's height and the baseline of every line inside it, so the
two cannot disagree. This is the structural fix for the failure that recurred
most in the hand-built era: a height computed one way, content drawn another, and
the difference discovered only when something crossed an edge.

A box in a height-matched row centres its content block rather than leaving it
stranded against the top edge.

A tag shares the title's line only while it leaves the title a workable share of
the width; otherwise it takes its own row above the title. Either way its width
comes out of the title's wrap width *and* its centre point, so the two cannot
collide.

### 4.4 Connectors

Arrows are drawn as paths, not typed as glyphs. A font substitution cannot change
a path's weight or shift it off the line it belongs on.

Nothing may sit between an arrowhead and the thing it points at.

---

## 5. Alternation between turns

**Consecutive graphic-bearing turns alternate theme.** The first graphic of a
conversation is `night`; the next is `day`; and so on. Both files of one turn —
wide and tall — always share a theme.

The point is separation. Two graphics in the same conversation arguing different
things should not look like two crops of one picture, and a reader scrolling back
should be able to find the one they want by its ground rather than by reading
every title.

**Three exceptions, and only three.** In each, sameness is carrying meaning that
alternation would destroy:

1. **A two-state redraw.** Fill-in-the-blank → filled. The whole point is that it
   is the same diagram, now answered — same layout, same coordinates, same theme.
2. **A before/after pair shown across two turns.** The comparison is the content;
   changing the ground makes the reader compare the wrong thing.
3. **A multi-part reveal's overview and its parts.** The overview and the part
   graphics that stack beneath it read as one set, so the set holds one theme and
   the *next* subject starts the alternation again.

In code: `pick_theme(graphic_index, continuity_of=...)`. Passing `continuity_of`
is how a renderer says "this is a redraw of that", and continuity always wins
over alternation.

---

## 6. The provenance mark

Every graphic carries a small footer mark at the bottom-left, in the footer
colour at footer size:

```
tpl · chain · v2          a template, which form, which version
freehand · logged         the escape hatch, and that the escape was recorded
```

It is visible deliberately, for now, so that a reviewer can tell at a glance
which pictures the renderer produced and which were drawn by hand. It is one flag
in the renderer, so it comes out of the client-facing build in one edit without
touching a form.

---

## 7. Byte budget

Template output is consistently
smaller than the hand-built equivalents because shared declarations live in one
stylesheet rather than being repeated inline, and because the renderer has no
reason to hedge a coordinate.

The ceiling still flexes before content is cut. Content completeness overrides
every technique in this document: never drop or merge away a named step, measure
or comparison to make a graphic smaller or easier to build.

---

## 8. The form catalogue

Twelve forms, one per entry in the universal method's catalogue. Each declares
its slots, validates them, and refuses a layout it cannot build honestly rather
than producing a cramped one.

| Form | Module | The situation it belongs to |
|---|---|---|
| `chain` | `form_chain.py` | a sequence, 1–5 steps; the last box is the outcome |
| `wrapped-chain` | `form_wrapped_chain.py` | a sequence too long for one row, joined by an elbow |
| `derivation-chain` | `form_derivation.py` | arithmetic, shown as working rather than as a total |
| `converging-rail` | `form_rail.py` | several inputs feeding one thing |
| `fork` | `form_fork.py` | one question, several alternative answers |
| `two-flow` | `form_two_flow.py` | two genuinely parallel flows, height-matched row for row |
| `merged-shared-flow` | `form_merged_flow.py` | two flows that share most of their steps |
| `fill-in-the-blank` | `form_fill_blank.py` | a structure handed over to complete, and its answered redraw |
| `agenda-grid` | `form_agenda.py` | what you are about to establish — and, marked `covered`, what is left |
| `bands` | `form_bands.py` | inputs → engine → outputs, when the answer is "it is not many things" |
| `role-cards` | `form_roles.py` | who has to cooperate, with the approver as its own object |
| `cards` | `form_cards.py` | independent items — options, findings, gaps |

Several forms refuse content rather than distorting it, and the refusal names the
form that should have been used instead:

- `chain` rejects six or more steps and points at `wrapped-chain`.
- `two-flow` rejects flows of unequal length and points at `merged-shared-flow`.
- `derivation-chain` rejects a missing `condition`: a derivation without its
  basis is a total with extra steps.
- `role-cards` rejects a missing approver: if nobody has to approve, the content
  is a plain set of cards, not a role map.
- `merged-shared-flow` rejects a bypassed step at either end of the chain, since
  the arc has nowhere to leave from or rejoin at.
- Any row refuses to make its boxes narrower than 150px.

### 8.1 Two things the forms guarantee rather than intend

**The bypass arc clears the box it arcs over.** The visual apex of a symmetric
quadratic bezier sits at half the control point's offset from the chord, so the
renderer sets the control offset to twice the clearance actually wanted. This is
computed, never estimated — estimating it is what once put an arc through the box
it was meant to clear.

**The answered redraw lands on the blank's coordinates.** `fill-in-the-blank`
returns its geometry; the filled build is passed that geometry back and refuses
to run without it, so the fit search cannot quietly choose a different canvas for
the answered version. The blank reserves exactly the height the value line will
occupy and draws its dashed field on that line, so nothing moves when the answer
arrives. Verified by comparing the box rectangles of the two files, not by eye.

**Supporting files**

| File | What it is |
|---|---|
| `templates/tokens.py` | every colour, size and constant in this document |
| `templates/core.py` | measuring, wrapping, the box, connectors, the canvas and its fit search |
| `templates/layout.py` | rows, columns, effect rows, dividers |
| `templates/contrast_check.py` | the WCAG verification in §2.4 |
| `templates/qa_render.py` | SVG → PNG for the look-at-it step; the PNG is never delivered |
| `templates/sheet.py` | contact sheets of every sample, for reviewing the set at once |
| `templates/demo.py` | the sample set in `samples/` — thirteen turns, one per form |

Sample output runs **2.2–4.3 KB** across all thirteen, inside the 4–5 KB default
and well under the ~10 KB text-heavy ceiling.

## Appendix A — clause for `02-image-creation-rules` v2

Drop-in text for the image-creation rules. It states the template/freehand split
and what the mark on each image means.

> ### Template or freehand — and saying which
>
> Every graphic is either rendered from a named template or drawn freehand, and
> the image says which in a small mark at the bottom-left.
>
> **Prefer the template.** Where a form in the catalogue fits the content, use it.
> The model supplies the slot values; the renderer supplies every coordinate,
> size and colour. The build-discipline rules cannot be broken by a template,
> because the geometry is computed rather than remembered.
>
> **Freehand is the escape hatch, and it is logged.** Draw freehand only where no
> form covers the layout the content actually needs — never to vary a form that
> would have worked, and never to avoid looking up the slot schema. Every
> freehand graphic is recorded: which form was closest, and what it could not do.
> That log is the queue for the next form.
>
> **The mark reads one of two ways.** `tpl · <form> · v<n>` names the template and
> its version. `freehand · logged` says the graphic was drawn by hand and the
> escape was recorded. An unmarked graphic is a build error, not a third
> category.
>
> **Never cut content to reach a template.** If a form would require dropping a
> named step, a measure or a comparison, the form is wrong for the content — use
> a different form, or go freehand and log it. Content completeness overrides
> this rule as it overrides every other.

## Appendix B — slot schemas of the three built forms

**chain** — a sequence. Horizontal on the wide ratio, vertical on the tall one.
One to five steps; six or more belongs to the wrapped-chain form.

```python
{
  "title": str,
  "subtitle": str,
  "steps": [                       # 1-5
    {"title": str,
     "values": [str, ...],
     "state": "plain|target|outcome|start|dashed",   # optional
     "tag": str,                                      # optional
     "badge": ("tick"|"cross", str),                  # optional
     "caption": str},                                 # optional
  ],
  "note": str,                     # optional dashed-divider caption
  "effects": [                     # optional, 0-3 effect boxes
    {"title": str, "values": [str, ...], "caption": str},
  ],
}
```

**derivation-chain** — arithmetic. Two to five steps, each carrying its input and
its result. The `condition` slot is required: a derivation without its basis is a
total with extra steps.

```python
{
  "title": str,
  "subtitle": str,
  "steps": [                       # 2-5
    {"title": str, "input": str, "result": str,
     "state": str, "tag": str, "caption": str},       # optional
  ],
  "answer": {"title": str, "values": [str, ...], "caption": str},  # optional
  "condition": str,                # REQUIRED
  "outputs": [                     # 1-3 effect boxes
    {"title": str, "values": [str, ...], "caption": str},
  ],
}
```

**cards** — independent items, no arrows. Two to six cards. Serves as the agenda
grid with the starting card carrying `state: "start"` and a short tag.

```python
{
  "title": str,
  "subtitle": str,
  "cards": [                       # 2-6, same shape as a chain step
    {"title": str, "values": [str, ...],
     "state": str, "tag": str, "badge": tuple, "caption": str},
  ],
  "columns": int,                  # optional override
  "note": str,                     # optional
  "effects": [ ... ],              # optional, 0-3
}
```

Every form is called the same way, and the remaining nine declare their slots in
their own module docstrings:

```python
form_chain.build(slots, ratio, theme_name, path,
                 w=None, h=None, base_lock=None, mode="tpl")
#   ratio       "wide" | "tall"
#   theme_name  from tokens.pick_theme(graphic_index, continuity_of=None)
#   w/h/base_lock   geometry to reuse, for a redraw that must share coordinates
#   mode        "tpl" | "freehand" — what the provenance mark says
#   returns     {"bytes": int, "w": int, "h": int, "base": int}
```

The return value carries the geometry precisely so a later redraw can be locked
to it. Hold it for any graphic you may need to redraw.
