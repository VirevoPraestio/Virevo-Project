# Tojo v2 — Implementation Guide

For the developer wiring this package into the Claude API integration.

Everything in `tojo-v2/` is content and specification. None of it runs. This
document says what to build around it, in what order, and which file is used at
which step.

---

## 1. The pipeline, end to end

```
 USER MESSAGE
      │
      ▼
┌─────────────────────────────────────────────────────────────────────┐
│ 1  RESOLVE FLOW STAGE                                               │
│    Decide scripted vs unscripted. Resolve the subscriber bypass of  │
│    the token gate BEFORE this, so the register follows the stage.   │
│    USES:  publish/manifest.yaml  (stage map — carried over from v1) │
└───────────────────────────────┬─────────────────────────────────────┘
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│ 2  BUILD THE CACHED PREFIX        identical every turn, fixed order  │
│    USES:  rules/always-on/00-core.md                                │
│           rules/always-on/09-reply-check-rules.md                   │
│           rules/always-on/00a-register-sales.md    ── exactly ONE    │
│              OR  00b-register-advisor.md           ──                │
│           skill/.../index/GROUP-CATALOGUE.md                        │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
         ═══════════════════════╪═══════════════════════  CACHE BREAKPOINT
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│ 3  ROUTE  — which function group is this?                           │
│    Score the query against the twelve groups. Take the top 1–2.     │
│    USES:  index/GROUP-CATALOGUE.md                                  │
└───────────────────────────────┬─────────────────────────────────────┘
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│ 4  LOOK UP POINTS  — which sections actually hold the answer?       │
│    Match the query against `also called` and `what it is`.          │
│    Each hit names its chunk. This is the step that turns a          │
│    hospital's own words into chunk ids.                             │
│    USES:  index/POINT-INDEX.md        (524 points, never in prompt) │
│           its "Cross-department concepts" table, so a concept        │
│           owned by one department but asked about from another       │
│           resolves to both                                           │
└───────────────────────────────┬─────────────────────────────────────┘
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│ 5  CONFIRM AND FILL  — score the candidate chunks                   │
│    USES:  index/<prefix>.card.md  for the candidate functions only  │
│    Take 3–6 chunks.                                                 │
└───────────────────────────────┬─────────────────────────────────────┘
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│ 6  ASSEMBLE THE KNOWLEDGE BLOCK                                     │
│    a. fetch the selected chunks                                     │
│    b. + each chunk's `needs`, ONE HOP, never to fixpoint            │
│    c. + the pinned common.* chunks, unconditionally, in code        │
│    d. + the paired department if the group was Bed or Discharge     │
│    e. strip every <!--m-->…<!--/m--> span                           │
│    f. never fetch a `retrieve: never` chunk, at any score           │
│    g. `see` entries are a SCORING BOOST ONLY — never fetched        │
│    USES:  skill/.../references/*.md                                 │
└───────────────────────────────┬─────────────────────────────────────┘
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│ 7  ADD THE VARIABLE TAIL                                            │
│    hospital record · conversation history with past figures as      │
│    one-line stubs · the user message                                │
│    USES:  FIGURE-STUBBING-SPEC.md                                   │
└───────────────────────────────┬─────────────────────────────────────┘
                                ▼
                    ┌───────────┴───────────┐
           graphic turn?                 no │
                    │ yes                   │
                    ▼                       │
┌─────────────────────────────────────┐     │
│ 8  ADD THE ON-DEMAND RULES          │     │
│    rules/on-demand/01-response      │     │
│    rules/on-demand/02-image         │     │
│    rules/on-demand/04-layout        │     │
│    (03-pricing on pricing turns)    │     │
└───────────────┬─────────────────────┘     │
                └───────────┬───────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│ 9  GENERATE                                                         │
│    The model returns response text, and for a graphic turn a FORM   │
│    NAME plus SLOT VALUES — not SVG.                                 │
└───────────────────────────────┬─────────────────────────────────────┘
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│ 10 RENDER                                                           │
│    Call the named form twice, wide and tall. Store the build call.  │
│    USES:  image/templates/form_<name>.py                            │
│           image/templates/tokens.py   (theme for this turn)         │
└───────────────────────────────┬─────────────────────────────────────┘
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│ 11 LOG                                                              │
│    tokens by block · cache read vs write · chunks retrieved and why │
│    · figures stubbed · freehand escapes · queries that matched      │
│    nothing (the gap register) · the turn's `reply_check` record     │
│    USES:  schema/reply-check-report.schema.json  ($defs.turn_record)│
└───────────────────────────────┬─────────────────────────────────────┘
                                ▼
                          RESPONSE + 2 SVG FILES
```

---

## 2. What each file is for

| File | Loaded | Purpose |
|---|---|---|
| `rules/always-on/00-core.md` | every call, cached | persona, source discipline, response and image trigger rules |
| `rules/always-on/09-reply-check-rules.md` | every call, cached | reading each reply, the opening line, the rating every 10th turn, the reset after two misses, the per-turn record and the end-of-day report |
| `schema/reply-check-report.schema.json` | log step, and the midnight report job | the per-turn `reply_check` record and the end-of-day report the back-end agent reads |
| `rules/always-on/00a` / `00b` | every call, one only | the register. Never both — the model cannot blend two voices it cannot both see |
| `index/GROUP-CATALOGUE.md` | every call, cached | twelve function groups. Does not grow as the library does |
| `index/POINT-INDEX.md` | **never in the prompt** | 524 named points → chunk ids. Retriever-side lookup only |
| `index/<prefix>.card.md` | per candidate function | what each chunk of that function covers |
| `index/points/*.points.md` | never | the per-file extracts POINT-INDEX is merged from. Keep for maintenance |
| `references/*.md` | 3–6 chunks per query | the content |
| `rules/on-demand/01, 02, 04` | graphic turns | response split, form catalogue, layout patterns |
| `rules/on-demand/03` | pricing turns | dictated pricing content (carried over from v1) |
| `image/templates/` | render time | the twelve forms and their shared core |
| `image/DESIGN-TOKENS.md` | never at runtime | the visual spec, for whoever maintains the renderers |
| `publish/lint_chunks.py` | CI | front-matter, ids, `needs`/`see`, maintainer leakage |
| `publish/lint_points.py` | CI | point ids resolve, no orphans, chunk coverage |

---

## 2a. The reply check (rule 09)

Three things around the model, none of them inside it:

1. **The three fixed lines live in the app,** not in the prompt. When the turn's `reply_check.say` is `opening`, `rating` or `reset`, show that line as its own message: the opening and reset lines before the turn, and the rating question on its own, holding the user's message until it is answered. The exact words are in 09 §2.2, §4.2 and §5.2.
2. **Store every `reply_check` record** at the log step, keyed by chat and turn. Validate it against `$defs.turn_record`. Strip it from what the user sees.
3. **At midnight India time, run the report job.** Give the model rule 09, the schema and the day's records. It returns one report. Validate it against the schema, then send it to the back-end agent (`Backend Agent/skills/reply-check-review`). Changes the back-end agent applies after approval go live at the next midnight, never part-way through a day.

---

## 3. Build order

Not the order of the diagram. This is the order that fails cheapest.

**Week 1 — the two changes with no dependencies.**

1. **Instrument first.** Log per turn: input tokens split by block, cache read vs
   write, output tokens, which chunks were retrieved, cost. Every number in this
   package is arithmetic from file sizes and measured graphs. A week of real logs
   will show which assumption is wrong far more cheaply now than later.
2. **Stub figures out of history** (step 7). One day. No dependency on anything
   else, and it is the largest single saving.
3. **Split the prompt and add the cache breakpoint** (step 2). Two days. Then
   verify — see §4.

**Week 2–3 — retrieval.**

4. **Build the 50-query eval set BEFORE the retriever**, with known-correct chunk
   ids per query. A routing mistake is invisible: the model answers well from the
   wrong material. Without the eval you will not find out.
5. **Build the retriever** (steps 3–6). Start with the point index — it is a flat
   lookup and it does most of the work. The card layer is a refinement on top.

**Week 4–5 — the renderer.**

6. **Wire the twelve forms** (steps 9–10). The model emits a form name and slots;
   your code calls `form_<name>.build(slots, ratio, theme, path)`. Keep freehand
   as a logged fallback.

**Week 6+ — the router and the loop.**

7. **Haiku for classification** — function group, chunk selection, flow stage,
   extracting the hospital's stated numbers into the record. Not for consulting.
8. **The gap register and the harvest loop.**

---

## 4. What to verify, and when

Each of these has failed silently in a system like this. None of them announces
itself in the output.

| After | Verify | How it fails if you don't |
|---|---|---|
| step 2 | `cache_read_input_tokens` > 0 on turn two | A wrong prefix order produces **zero cache hits with no error**. You pay full rate and never know |
| step 4 | the eval set's known-correct chunks are in the top 6 | The model answers fluently from the wrong section |
| step 6b | assembled context contains **no chunk reached only via `see`** | `see` followed transitively pulls 95% of the library — worse than no chunking at all. This is the one guarantee the files cannot enforce |
| step 6c | `common.*` present whenever any department chunk is | Topic matching drops it exactly when it is most needed |
| step 6e | no `<!--m-->` content in the assembled prompt | A hospital receives Virevo's internal review trail |
| step 6f | no `retrieve: never` chunk ever assembled | The model discounts a section because a changelog says it is unfinished |
| step 7 | stub count rises with conversation length | If history is not shrinking, stubbing is not wired |
| step 10 | every delivered file is SVG, never PNG | The raster is an internal QA step only |
| CI | both lints exit zero | Ids drift, `needs` dangles, points orphan |

---

## 5. Three rules that are easy to get backwards

**`needs` is one hop. `see` is never fetched.** Measured: resolving `needs`
transitively pulled 56% of the library from a typical section and 78% from the
worst; the split into hard and soft brought the worst case to 12%. If you
implement `see` as a fetch instruction you will undo the entire saving while
every per-file check still passes.

**The pinned and co-fetch relationships are enforced in code, not in the
front-matter.** `common-elements` is pinned because topic matching would select
it exactly when it is least needed. Discharge and Bed co-fetch because they
verify each other's numbers. Do not make either conditional on a score.

**§7.4 sub-numbering is not parallel across departments.** `dis.7.4.1` and
`bed.7.4.1` are automation; `opd.7.4.1` is process changes, because that file
deliberately reverses the order. Never map a solution aspect across departments
by index — map it by name.

---

## 6. The renderer contract

The model emits a form name and slot values. Your code renders.

```python
import form_chain
result = form_chain.build(slots, "wide", theme_name, "out/fig26-wide.svg")
# result == {"bytes": 3825, "w": 960, "h": 576, "base": 15}
```

- `theme_name` comes from `tokens.pick_theme(subject_index, continuity_of=None)`.
  The index counts graphic-bearing **subjects**, not files or turns; a redraw
  does not advance it.
- **Store the returned geometry with the figure.** A fill-in-the-blank's answered
  redraw must be built with the blank's `w`, `h` and `base` or the two will not
  share coordinates, and the form refuses to build without them.
- **Store the build call — form name plus slots — not the SVG.** That is what a
  later revision request rehydrates.
- A form raises `LayoutError` rather than producing a cramped layout, and the
  message names the form that should have been used. Surface it; do not swallow
  it and fall back to freehand silently.
- Freehand output must still carry the `freehand · logged` footer mark, and the
  escape must be logged with which form was closest and what it could not do.

---

## 7. Content that needs a human before go-live

Seventeen content problems were found while chunking, listed in `README.md` §5.
Three of them are contradictions the model can state to a hospital as fact — a
superseded occupancy trigger, a 10 AM/11 AM disagreement between a worked example
and the KPI that cites it, and a KPI whose wording predates the role split it
describes.

None of these are retrieval problems and none can be fixed in code. They need
someone with authority over the material.
