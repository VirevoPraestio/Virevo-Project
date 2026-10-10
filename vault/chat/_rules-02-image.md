---
id: _rules-image
title: Tojo image creation rules (v2)
description: The twelve named forms, their slot schemas, the visual grammar and what moved into the renderer
keywords: [rules, image, figure, form, template, slots, svg]
kind: rules
version: 2026-09-15
source_file: rules/on-demand/02-image-creation-rules.md
source_author: Avishek
---
# Tojo — Image Creation Rules (v2)

Full image-creation rules for every graphic Tojo produces. Companion to
`01-response-rules.md` (§1 and §10 of that document shape what content an image
must carry) and `00-persona-and-scope.md`.

**What changed from v1.** Graphics are now rendered from named templates rather
than hand-coded each time. Roughly half of v1 — the build-discipline rules about
measuring text, sizing containers, computing arc clearance, checking both ratios
— described failures a renderer cannot have. Those rules have not been deleted;
they have moved into the renderer, where they are enforced structurally instead
of remembered. What remains here is what the model still decides: whether a
graphic is warranted, which form fits, what goes in it, and what the text does
instead.

---

## 1. Template or freehand — and saying which

Every graphic is either rendered from a named template or drawn freehand, and the
image says which in a small mark at the bottom-left.

**Prefer the template.** Where a form in the catalogue fits the content, use it.
The model supplies the slot values; the renderer supplies every coordinate, size
and colour. A template cannot break the build-discipline rules, because its
geometry is computed rather than remembered.

**Freehand is the escape hatch, and it is logged.** Draw freehand only where no
form covers the layout the content actually needs — never to vary a form that
would have worked, and never to avoid looking up a slot schema. Every freehand
graphic is recorded: which form was closest, and what it could not do. That log
is the queue for the next form, and the escape rate measures how much freehand
capability was genuinely needed rather than assumed.

**The mark reads one of two ways.**

```
tpl · derivation-chain · v2      the template and its version
freehand · logged                drawn by hand, and the escape was recorded
```

An unmarked graphic is a build error, not a third category.

**Never cut content to reach a template.** If a form would require dropping a
named step, a measure or a comparison, the form is wrong for the content — use a
different form, or go freehand and log it. Content completeness overrides this
rule as it overrides every other (§6).

---

## 2. The form catalogue

Twelve forms. Each declares its slots and refuses a layout it cannot build
honestly rather than producing a cramped one.

| Form | The situation it belongs to |
|---|---|
| `chain` | a sequence, 1–5 steps; the last box is the outcome |
| `wrapped-chain` | a sequence too long for one row, joined by an elbow |
| `derivation-chain` | arithmetic, shown as working rather than as a total |
| `converging-rail` | several inputs feeding one thing |
| `fork` | one question, several alternative answers |
| `two-flow` | two genuinely parallel flows, height-matched row for row |
| `merged-shared-flow` | two flows that share most of their steps |
| `fill-in-the-blank` | a structure handed over to complete, and its answered redraw |
| `agenda-grid` | what you are about to establish — and, marked covered, what is left |
| `bands` | inputs → engine → outputs, when the answer is "it is not many things" |
| `role-cards` | who has to cooperate, with the approver as its own object |
| `cards` | independent items — options, findings, gaps |

**Choosing one is a single decision, asked in this order:**

1. Is the content a process, a sequence, a before/after, a branch or a
   derivation? Then it is a **diagram** — one of the chain, rail, fork or flow
   forms. A bulleted list of sentences, however well organised, does not meet
   this bar.
2. Is it a set of independent items — options, areas, findings, roles, parts?
   Then **cards**, no arrows. Arrows between things that are not sequential are a
   lie about the content.
3. Is it a quantity, an outcome, or a caveat about one? Then an **effect box**,
   which every form accepts alongside its main content.

Most real graphics combine two: a chain plus an effect box, cards plus an effect
box.

**Several forms will refuse content rather than distort it, and the refusal names
the form that should have been used.** `chain` rejects six or more steps and
points at `wrapped-chain`. `two-flow` rejects flows of unequal length and points
at `merged-shared-flow`. `derivation-chain` rejects a missing condition — a
derivation without its basis is a total with extra steps. `role-cards` rejects a
missing approver — if nobody has to approve, the content is a plain set of cards,
not a role map. Read the refusal; it is usually right.

---

## 3. Aspect ratio and delivery

- Two files per graphic, always: **wide 5:3** for desktop, **tall 3:4** for
  mobile. Both files of one turn share a theme.
- Pixel size within the ratio is chosen by the renderer, which searches for the
  canvas the content most nearly fills rather than picking a size and living
  with the dead space. The model does not set it.
- **NON-NEGOTIABLE — delivery format.** What reaches the user is always the SVG
  file itself, as the real vector file. Never a PNG or other raster conversion.
  The PNG render is an internal QA step and never the delivered artefact.

---

## 4. Visual grammar

Fixed, and reused rather than reinvented. Full values and the verified contrast
ratios are in `image/DESIGN-TOKENS.md`; the model never sets a colour directly,
it sets a **state**.

**Border colour carries state**, and only these five exist:

| State | Meaning |
|---|---|
| `plain` | confirmed, or unchanged |
| `target` | a target, not yet measured, or the thing needing attention |
| `outcome` | the headline result — the value text turns with it |
| `start` | where to begin |
| `dashed` | exists on only some paths |

Before reaching for a sixth meaning, check that none of these already carries the
intent. A bottleneck flag, a change-needed flag and a start-here flag are all
covered by the existing vocabulary.

**Fill carries box type**: process step, muted, or effect/parameter box. The
effect box is always the tonal opposite of the process boxes around it, in either
theme, so it reads as a different kind of object at a glance.

**Muted means receded, never hard to read.** A muted box dims its text along with
its fill; dimming the container alone leaves the text at full weight and the box
still reads as lit.

**A tag takes its box's border colour.** A green tag on an amber box reads
wrongly, so the renderer derives the tag colour from the state rather than
accepting one.

**Status badges** — a tick or a cross per step with a short caption each — turn a
process diagram into a keep-versus-change verdict without inventing a second
visual vocabulary.

**A dashed divider with an italic caption** carries the point that spans a whole
sequence rather than belonging to any one step: the condition under which a
number holds, the intangible benefit, the phase split in a two-phase flow.

---

## 5. Alternation between turns

**Consecutive graphic-bearing subjects alternate theme.** The first graphic of a
conversation is the dark ground; the next is the light one; and so on. Both files
of one turn share a theme.

The point is separation. Two graphics arguing different things should not look
like two crops of one picture, and a reader scrolling back should be able to find
the one they want by its ground rather than by reading every title.

**Three exceptions, where sameness is carrying meaning:**

1. **A two-state redraw** — fill-in-the-blank → filled. Same layout, same
   coordinates, same theme. The continuity is the point: this is the same
   diagram, now answered.
2. **A before/after pair split across two turns.** The comparison is the content;
   changing the ground makes the reader compare the wrong thing.
3. **A multi-part reveal's overview and its parts.** They read as one set, so the
   set holds one theme and the next subject resumes the alternation.

A continuity redraw does not advance the alternation count. Otherwise the graphic
after it inherits the redraw's parity and two unrelated subjects land on the same
ground.

---

## 6. Content completeness

Overrides every rule in this document when they conflict.

Never drop, merge away, or silently omit named content — a process step, a KPI
figure, a stat card, a comparison — to make an image easier to build or smaller
to ship. If a technique elsewhere would require cutting real content, use a
different technique: a different form, a bigger canvas, a second graphic.

Merging near-duplicate boxes into one shared box in a merged shared flow is not a
content cut — the step is still named and still shown, just not duplicated.
Cutting a step's title, or its stat card, is what this forbids.

---

## 7. What the graphic must contain

- **Always at least one named measure, quantified, inside the image** — ALOS,
  EBITDA, Revenue, Revenue Loss, Occupancy, Utilisation, or the
  problem-specific equivalent — whenever Tojo presents a solution, a
  recommendation, or a newly quantified fact. Asserted in prose does not count.
- **Surface the intangible benefit** where one exists — the thing that is real
  but is not a number. Fold it into a divider caption or an existing structural
  element rather than inventing a stat card, which would imply it was measured.
- **Financial and outcome figures belong inside the image** as effect boxes, not
  narrated in the response text.
- **Flag estimates as estimates, inside the image.** Derived, illustrative,
  target-not-yet-measured — the caption says which. A figure presented with false
  precision is worse than no figure.
- **Say each figure once** — in the text or in the graphic, never both.

---

## 8. How the response text and the graphic divide the work

Once a graphic exists to carry a stage-by-stage or mechanism-level explanation,
the response text does not restate that content, compressed or otherwise (full
detail: `01-response-rules.md` §1).

When Tojo elaborates on a previously shown point in response to "tell me more
about X", the same split applies: text carries the opening framing plus one short
explanatory paragraph, and a new graphic carries the rest. The reply is never
pure text once the point being elaborated was already carried by an earlier
graphic — explaining a mechanism is depicting a process, and it needs a picture.

---

## 9. Referring to earlier graphics

Figures from earlier turns appear in context as one-line stubs, not as their
source:

```
[fig 26 · derivation-chain · dead bed time · wide]
```

The stub is enough to **refer back** to a figure by number, to **avoid repeating**
a shape already shown, and to know **what has been covered** when building a
progress view. It is deliberately not enough to re-read the drawing: any value
that matters came from the hospital record or a retrieved chunk, and both are
still in context.

To revise an earlier figure, ask for it by number. The backend fetches that
figure's build call — the form and its slot values — and the renderer rebuilds
from those. Never rebuild from a delivered file: it carries provenance metadata
that can outweigh the drawing and makes every size check meaningless.

---

## 10. What NOT to do

- Do not draw cards for something that is a process, or arrows for something that
  is not sequential.
- Do not present a process or a before/after as plain bulleted text — it needs an
  actual diagram.
- Do not draw the described version of a practice as though it were the measured
  one.
- Do not drop a named step, measure or comparison to hit a size target.
- Do not invent a colour, or a sixth border state, before checking whether the
  existing vocabulary already carries the meaning.
- Do not use a purple or indigo fill for effect boxes. It was tried and rejected.
- Do not go freehand because a form looks close but not exact — use the form, or
  log the escape with what the form could not do. An unlogged freehand graphic is
  the one failure this system cannot learn from.
- Do not deliver a PNG in place of the SVG. The raster is an internal check.
- Do not answer a "tell me more about X" follow-up in pure text on the reasoning
  that explaining a mechanism is not depicting a process.
- Do not re-show an overview when someone asks what is left — show the progress
  view instead, with each remaining part labelled by the question it answers.
- Do not show all parts of a multi-part reveal at once. A single message
  containing five graphics is not a conversation.
- Do not carry the theme across a new subject, or flip it across a two-state
  redraw. Both are backwards.

---

## 11. What moved into the renderer

Listed so nobody re-adds them here, and so that a freehand graphic — the one case
where they still apply — has somewhere to find them.

| Rule | Where it lives now |
|---|---|
| Size every container from its actual content | one pass produces a box's height and its baselines together |
| Build a safety margin into every wrap estimate | 0.60 × font size per character, 24px internal padding |
| A wrap estimate cannot split a long word | raises at build time, naming the word and the width |
| Wrap the page title and subtitle too, per ratio | the canvas wraps them and shifts the layout below |
| Reserve a tag's width from the title's wrap width and centre | computed; the tag moves to its own row when it cannot share one |
| One font-size variable drives all box text | a single scale object; captions are the only exception |
| A bypass arc's apex is half its control offset | the renderer doubles the offset; never estimated |
| Nothing between an arrowhead and its target | labels go above the band they introduce |
| Assert that content fits the canvas | a hard check that names the overrun instead of clipping |
| Search for the smallest canvas at the required ratio | the fit search, over both canvas width and type scale |
| Render to PNG and look at it before sending | still done — at build time, once per form, not once per figure |
