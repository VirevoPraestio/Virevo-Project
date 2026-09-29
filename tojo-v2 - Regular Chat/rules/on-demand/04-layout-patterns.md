# Tojo — Reusable Layout Patterns (v2)

Retrieved at generation time alongside `01-response-rules.md` and
`02-image-creation-rules.md`. These patterns generalise across departments and
problems, not only Discharge.

In v1 these were descriptions of layouts to build by hand. Most are now **forms**
with declared slots, so the pattern names below map onto renderers. The pattern
is still the thinking; the form is how it gets drawn.

| Pattern | Form | What it is for |
|---|---|---|
| **Progressive multi-point reveal** | `agenda-grid` overview, then one form per part | Any multi-part solution or option set: intro plus overview graphic, then each part's detail and graphic stacked beneath as the user engages. |
| **Progress view** | `agenda-grid` with parts marked `covered` | When the user asks what is left. Never re-show the overview; mark what is covered and label each remaining part with the question it answers. |
| **Fill-in-the-blank → filled** | `fill-in-the-blank` | Any turn handing the hospital a structure to complete with its own numbers. The answered redraw reuses the blank's geometry and theme, so it lands on the same coordinates. |
| **Time-value ↔ status-badge** | `chain`, with badges | The same box grammar showing "what happens, and when" in one turn and a keep-versus-change verdict in the next, without inventing a second visual vocabulary. |
| **Merged shared flow** | `merged-shared-flow` | Any pair of processes that turn out to be mostly the same process. Common steps appear once; differing-value steps once with stacked values; flow-specific steps as dashed boxes with a bypass arc. Clearer and smaller at once. |
| **Genuinely parallel flows** | `two-flow` | Two processes that really are different. Side by side in columns on both ratios, rows height-matched so they stay comparable step for step. |
| **Derivation with its basis** | `derivation-chain` | Any quantity becoming a headline number. One box per step, input and result in each, the condition the number holds on beneath. The form will not build without the condition. |
| **Converging inputs** | `converging-rail` | Several sources feeding one figure. A rail spans the whole input block and one arrow leaves its centre — an arrow rising out of the gap between two boxes reads as coming from nowhere. |
| **Two neutral options** | `fork` | Where you want to know which pattern someone is in. Draw both and let them place themselves; drawing only the one you expect and asking "is this you?" leads the witness. |
| **It is not many systems** | `bands` | When someone asks how a many-step thing gets built and the answer is that it is three things. |
| **Who has to cooperate** | `role-cards` | Cards for the doers, a bordered box for the approver. The form requires an approver, because an approver outside the daily routine is the usual reason a change does not survive its first difficult day. |

## Argument shapes worth reusing

These are not layouts. They are the shape of a good answer, and they choose the
layout rather than the other way round.

- **"Under-utilised time plus no ownership"** — "X% of the process could already
  happen in this window, and here is why nobody uses it today." A stronger
  diagnostic template than a flat root-cause label. Works for any department, not
  only Discharge.
- **Confidence-tagged assumptions versus hospital-confirmed data** — the
  distinction is carried into the graphic itself, in captions, not only in the
  prose. A derived figure says derived; an illustrative one says illustrative.
- **Concede the half that is true, and park it** — most objections carry two
  claims, one testable against their numbers and one about people. Name the
  second in the first line, say it will get a proper turn, and spend the response
  on the first.
- **Narrow the claim rather than defending it** — "this will never work here" is
  almost always aimed at a bigger claim than the one being made. Split what is
  genuinely fixed from what is deliberately left alone, show the two side by
  side, and let the picture do the narrowing.
- **Quantify the ask on the most resistant group, even when the honest number is
  zero** — and attach the condition that keeps it true. "No extra time beyond
  what they already do" is checkable; saying in the same breath what would
  falsify it is what makes it credible rather than promotional.

## Theme alternation across a sequence

Consecutive graphic-bearing subjects alternate ground. A multi-part reveal's
overview and its parts count as **one** subject and share a theme, so the set
reads as a set; the next subject resumes the alternation. A two-state redraw
keeps the theme it is redrawing.
