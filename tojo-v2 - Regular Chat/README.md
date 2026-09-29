# Tojo v2 — Package Overview

The second version of the Tojo runtime package. v1 is untouched at
`claude/final/`; everything here is a parallel tree.

Three changes, each targeting one of the four fixes in the architecture note:
figures are **stubbed** out of history, knowledge is **chunked and indexed**, and
graphics are **rendered from templates** rather than hand-coded.

---

## What is here

```
v2/
  README.md                        this file
  IMPLEMENTATION-GUIDE.md          for the developer: pipeline, build order, checks
  CHUNKING-SPEC.md                 how a reference file is cut, found and fetched
  FIGURE-STUBBING-SPEC.md          how a past figure collapses to one line
  image/
    DESIGN-TOKENS.md               the visual system: colour, type, geometry, alternation
    templates/                     twelve form renderers plus the shared core
    samples/                       thirteen worked examples, both ratios
  rules/
    always-on/00-core.md           resident, in the cached prefix
    on-demand/01-response-rules.md
    on-demand/02-image-creation-rules.md
    on-demand/04-layout-patterns.md
  skill/virevo-hospital-ops/
    SKILL.md                       manifest and retrieval contract
    index/GROUP-CATALOGUE.md       twelve function groups, resident
    index/*.card.md                one index card per function
    index/POINT-INDEX.md           524 named points, retriever-side only
    index/points/*.points.md       the per-file extracts it merges
    references/*.md                the five chunked reference files
  publish/
    lint_chunks.py                 the whole-library chunk lint
    lint_points.py                 the point-index lint
```

**Carried over from v1 unchanged**, because nothing in this work touches them:
`00a-register-sales.md`, `00b-register-advisor.md`, and
`03-subscription-pricing-rules.md`. Re-versioning a file that did not change
makes the diff lie about what was done.

---

## 1. Knowledge — chunked and indexed

68 chunks across five files, 40,630 tokens. Each chunk carries an ID, a summary
of what it establishes, retrieval keywords, a hard `needs` list and a soft `see`
list.

Retrieval walks three levels: a twelve-group catalogue resident on every call
(~360 tokens, and it does not grow as the library does), one index card per
candidate function, then the chunks themselves.

**Below that sits the point index**, and it is the layer that makes the rest
usable. A chunk is the right unit to fetch and the wrong unit to search: a
section described as "eleven practice-verification questions" tells a retriever
that eleven questions live there, not what any of them are. So a hospital saying
*"we don't record when housekeeping is notified"* would match nothing, and the
retriever would have to guess.

`index/POINT-INDEX.md` names all 524 individually-named points in the library —
every question, KPI, financial parameter, dependency, consideration, failure mode
and solution element — each with the chunk it lives in and the phrases a hospital
administrator would actually say for it. It is searched by the retriever and
**never enters the prompt**, so it costs nothing per turn and can afford to be
exhaustive where the index cards cannot.

Building it surfaced **31 concepts that appear in more than one department under
different names** — ALOS defined in one KPI list and referenced in another, the
same staffing ratio stated once in common-elements and instantiated six times,
dead bed time owned by Bed Management and referenced by Discharge, the serialised
shared team indexed seven times across two files as failure mode, verification
question and fix. Those are in the file's own cross-reference table, so a query
phrased from one department's side resolves to both.

**The failure this nearly shipped with.** The first cut declared 194 dependency
edges resolved transitively. Measured, that pulled 27 chunks and 22,600 tokens —
**56% of the library** — from a typical starting chunk, and 78% from the worst.
Whole-file retrieval with extra steps, and it would have looked correct in every
per-file check.

The fix was to split one field into two. `needs` is now the hard case only — at
most two IDs, resolved one hop, never transitively — and `see` carries everything
else as a scoring boost that is never auto-fetched. Re-measured:

| | before | after |
|---|---|---|
| Worst-case pull | 38 chunks · 31,870 tokens · 78% | 3 chunks · 3,500 tokens · **9%** |
| Mean pull | — | 1.46 chunks · 939 tokens · **2.5%** |
| Realistic query, 5 chunks + pins | — | mean **6,280**, p95 **9,250** |

Against a 12,000-token cap, 200 simulated queries produced zero breaches.

The graph is also safe under the wrong implementation: resolving `needs` to
fixpoint costs about 100 tokens more than one hop on average and nothing at the
worst case. **`see` is the opposite** — followed to fixpoint it pulls 95% of the
library. That contract lives in the retriever, not in the files, and it needs a
test there.

### 1.1 Maintainer content that was reaching the model

Three chunks — 2,390 tokens of change log — now carry `retrieve: never`. In v1
they sat inside files the retriever fetched whole.

Fifteen further fragments are wrapped in inline `<!--m-->…<!--/m-->` spans,
stripped before assembly: approval stamps, drafting dates, and two file header
lines naming who drafted each KPI list and who signed it off. A retrieved chunk
was handing a hospital Virevo's internal review trail.

**One thing was deliberately left visible.** Bed Management's "KPI revision
agreed but not yet made" block is exactly the kind of status note the rule
suppresses — but hiding it would leave the model retrieving KPI #16 and stating
its superseded trigger as current, contradicting §7.4.4 on the same page. Wrap
provenance; never wrap a correction. Where a correction note is the only thing
stopping the model asserting a stale figure, it stays, and the real fix is a
human correcting the content.

---

## 2. Figures — stubbed out of history

A past figure reaches the model as one line:

```
[fig 26 · derivation-chain · dead bed time · wide]
```

25,200 tokens at turn 15 become 420, and the saving grows with conversation
length — which is exactly where the cost was worst. Full detail in
`FIGURE-STUBBING-SPEC.md`, including how a revision request rehydrates the
figure's **build call** rather than its rendered SVG.

---

## 3. Images — rendered from templates

Twelve named forms, one per entry in the universal method's catalogue. The model
supplies slot values; the renderer supplies every coordinate, size and colour.
Freehand remains as a logged escape hatch, and every image says which it is.

Roughly half of v1's image rules described failures a renderer cannot have. They
have not been deleted — they moved into the renderer, where they are enforced
structurally. `02-image-creation-rules.md` §11 lists what moved, so nobody
re-adds them and so a freehand graphic still has somewhere to find them.

Two things the forms guarantee rather than intend: a bypass arc's clearance is
computed from the true apex of a quadratic bezier rather than the control point's
raw offset, and a fill-in-the-blank's answered redraw is locked to the blank's
geometry and refuses to build without it.

The palette is verified, not judged: `contrast_check.py` computes WCAG ratios for
every text-on-fill pair in both themes. Three colours in the shipped set are
corrected versions of ones that looked fine and measured under 4.5:1.

Sample output runs 2.2–4.3 KB across thirteen worked examples, inside the 4–5 KB
default.

---

## 4. Prompt order, for the cache

Rules are identical every turn; knowledge is different every query. The cache
breakpoint goes between them.

```
── cached, identical every turn ────────────────────────
   00-core · one register · the universal method
   01 response + 04 layout + the form catalogue
   the department answering rules for this conversation
   index/GROUP-CATALOGUE.md
── CACHE BREAKPOINT ────────────────────────────────────
── variable, billed full rate ──────────────────────────
   index cards · retrieved chunks · hospital record
   history with past figures stubbed · user message
```

A cache hit requires an identical opening prefix, so fixed material comes first
and in a fixed order. **A wrong order produces zero hits with no error** —
confirm with `cache_read_input_tokens` in the response rather than assuming.

Note the consequence for editing: `00-core.md` is inside the cached prefix, so
its wording is part of the cache key. An edit invalidates the cache for every
conversation until the next write.

---

## 5. What a human needs to fix

None of these were introduced here. All were found while chunking, and all are
content problems that need someone with authority over the material. They are
listed in the order they would embarrass you in front of a hospital.

**Contradictions the model can state as fact**

1. **Bed Management KPI #16** still tracks the superseded ">80% occupancy or ~40
   admissions/day" trigger that §7.4.4(a) replaced with three conditions. §8 and
   §7.4.4 contradict each other on the page.
2. **Discharge §7.4's worked example says 11 AM** for cash-patient discharge,
   where §3, §7.2 q7 and KPI #2 all say 10 AM — and KPI #2 cites §7.4 as the
   source of the 10 AM figure it does not contain. §7.4 is the outlier.
3. **Discharge KPI #13's wording predates the §7.4.4 role split** and omits the
   third, TAT-overrun condition. It is marked approved as drafted.

**Cross-references that do not resolve**

4. **OPD KPI 17** cites "§7.2 point 8's training-ownership question". Point 8 is
   automation history; training ownership is §7.1 point 13.
5. **OPD §7.4 item 11** cites §7.1 points 2 and 12 for the diversion-incentive
   argument. Point 4 looks like the intended referent.
6. **OPD §7.1 point 2** cites "points 1 and 4 of §3". §3's table rows are not
   numbered at all.
7. **The playbook cites `opd-diagnostic-leakage.md` §7.4** alongside "§7.4.4"
   citations to the other two departments. OPD does not number its §7.4
   subsections and deliberately reverses the aspect order, so no fine-grained
   parallel exists.

**Gaps and unreconciled figures**

8. **Two unreconciled peak-load curves inside OPD §7.1** — point 3 assumes 80% of
   patients in one four-hour window, point 5 assumes 40/40 across two shift
   edges, and point 7 says to use "the same style of calculation as points 3 and
   5" without saying which applies.
9. **`common-elements`' "which ratio applies in which department" list names one
   of Bed Management's two peak-load instances.** Bed Management's own text
   asserts both are listed there.
10. **Bed Management §7.1 point 5's staffing ratio has no KPI** anywhere in §8.
11. **The OPD Scheduling Manager cost is "to be confirmed"**, where the Discharge
    Executive and Bed Manager both carry figures.
12. **Bed Management §7.4.4(b) carries a "Known gap"** — no worked example of the
    ratio-check, unlike Discharge's.

**Housekeeping**

13. **The playbook's §9 closing paragraph is a note-to-self** about future
    refactoring, living in a runtime reference file. It will be retrieved and
    read as instruction.
14. **The playbook cites the rules package under two different names** —
    `virevo-tojo-chat-rules` and `virevo-tojo-chat` — neither matching this
    layout.
15. **The playbook hard-codes "all 16 KPIs"** against Discharge §8. A count that
    breaks silently the next time that list changes.
16. **The playbook's §6 contains a literal `[N]` placeholder** inside what reads
    as a verbatim quote.
17. **The playbook's §9 scopes its generalisation claim to §1–7**, silently
    excluding §8, where the preamble claims the whole shape generalises.

---

## 6. Before any of this ships

1. **Instrument first.** Log per turn: input tokens split by block, cache read vs
   write, output tokens, which chunks were retrieved and why, figures stubbed,
   cost. Every number in this package is arithmetic from file sizes and measured
   graphs. A week of real logs will show which assumption is wrong far more
   cheaply before the build than after.
2. **Build the 50-query eval set before the retriever, not after.** Known-correct
   chunks per query. A routing mistake is invisible: the model simply answers
   well from the wrong material.
3. **Test that `see` is never followed.** It is the one place where the entire
   budget argument depends on the retriever honouring a contract that nothing in
   the files enforces.
4. **Verify the cache is actually hitting.** `cache_read_input_tokens`, on a real
   turn, before believing any of §4.
