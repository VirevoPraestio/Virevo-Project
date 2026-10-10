---
name: virevo-hospital-ops
description: Deep hospital-operations knowledge base for the Virevo/Tojo agent — chunked, indexed reference material on Bed Management, the Discharge Process, and OPD-to-Diagnostics Conversion (diagnostic leakage), plus shared cross-department frameworks (a four-aspect solution-construction method, a shared Discharge/Bed/ALOS/Occupancy consideration set, and a peak-load staffing ratio method), covering dependencies, financial parameters, hospital-practice verification questions, solution construction, and KPIs. Use this whenever a question needs real operational judgment about how a hospital runs in one of these areas — discharge delays, ALOS, bed occupancy/admissions/ICU step-down, or OPD-to-diagnostics conversion/diagnostic leakage — not just the scripted virevo-tojo-chat sales demo. Trigger even if the user doesn't name a department file or say "skill" directly, e.g. "why is our discharge process so slow", "how do we reduce diagnostic leakage in OPD", "what KPIs should we track for bed management".
license: Proprietary — internal Virevo use.
---

# Virevo Hospital Operations Knowledge Base

Operating judgment on how a hospital actually runs, function by function. Use it
to give the Virevo/Tojo agent genuine operational insight on real
hospital-operations questions rather than generic AI-hospital-management
platitudes.

## Relationship to the Tojo rules package

The Tojo rules package governs persona, register, response format, and images on
every turn. This skill is the layer underneath it: use it whenever a question
calls for reasoning about a hospital's dependencies, verifying its practice
against a baseline, checking financial parameters, or constructing a real
solution.

The scripted sales flow's "Diagnostic Leakage in OPD" and "Discharge Process
Delays" problems draw on the same underlying domain, but this skill is written
for direct operational reasoning, not as scripted content. Do not substitute this
skill's content for the scripted flow's fixed stage structure, or the reverse.

## What changed in v2: retrieval is chunk-level

v1 retrieved whole department files — three of them, about 36,500 tokens, on
every query. v2 retrieves sections.

Each reference file is now cut into numbered **chunks**, each carrying an ID, a
summary of what it establishes, retrieval keywords, and — the part that makes
chunking safe — a `needs` list naming the sibling sections it cannot be read
without. The retriever resolves `needs` **one hop, in code**, before assembling
context, and never to fixpoint: measured, following these edges transitively
pulled over half the library from a typical section. A second field, `see`,
carries the merely-related sections as a scoring boost and is never fetched.

That last point is the whole design. The v1 manifest warned that pulling one
paragraph out of a department file loses the connective structure the file was
written with: §7.2's verification questions reference §7.1's considerations by
number, and §7.4's solution cross-references §7.1 through §7.3 throughout.
Whole-file retrieval preserved that by accident. Chunked retrieval preserves it
on purpose, because the dependency is declared in the file rather than left to
the retriever to notice.

Full format in `CHUNKING-SPEC.md`.

## The library

68 chunks across five files, 40,630 tokens. Three of those chunks — 2,390 tokens
of maintainer change-log — carry `retrieve: never` and are held out of the model
entirely, which in v1 they were not.

| Function | File | Chunks | Tokens |
|---|---|---|---|
| Bed Management | `references/bed-management.md` | 17 | 14,340 |
| OPD-to-Diagnostics Conversion | `references/opd-diagnostic-leakage.md` | 19 | 11,010 |
| Discharge Process | `references/discharge-process.md` | 18 | 9,390 |
| Discharge conversation playbook | `references/discharge-process-conversation-playbook.md` | 10 | 3,620 |
| Common elements | `references/common-elements.md` | 4 | 2,270 |

Three departments follow the same eight-section template: Purpose; Sub-functions
& core activities; Dependencies; Non-negotiables; What can flex; Failure modes;
Chat-agent handling (§7.1 subject-matter considerations, §7.2 dependency
verification protocol, §7.3 financial parameters, §7.4 solution construction);
and KPIs.

The playbook is not one of those. It is a worked example of a full unscripted
Discharge consulting conversation, chunked by conversation stage, and its §9
states the rule for generalising the shape to other departments.

Expect further functions in `references/` over time, using the same template.
Check `index/GROUP-CATALOGUE.md` for what is actually there rather than assuming
these are the complete set.

## Finding the right chunks

Three levels, walked in order:

1. **`index/GROUP-CATALOGUE.md`** — twelve function groups, ~360 tokens, resident
   on every call. Narrows twelve groups to one or two. This list does not grow as
   the library does; adding the hundredth file adds a row to a group, not a
   group.
2. **`index/<prefix>.card.md`** — one index card per candidate function, ~120–250
   tokens, naming every chunk and what it covers. Narrows a function to the
   chunks that answer the question.
3. **The chunks themselves** — 3–6 per query, plus whatever their `needs`
   resolve to.

Underneath all three sits **`index/POINT-INDEX.md`**: every one of the 524
individually-named points in the library — questions, KPIs, financial
parameters, dependencies, considerations, failure modes, solution elements —
each with the chunk it lives in and the phrases a hospital would actually use
for it. It is a retriever-side lookup table and never enters the prompt. It is
what turns a question phrased in the hospital's words into a chunk id, instead of
leaving the retriever to guess which section a topic probably sits in.

Its cross-department table matters as much as its rows: 31 concepts are named in
more than one file under different words, so a query entering from one
department's side still reaches the department that owns the definition.

## Retrieval contract

- **`common-elements` is pinned**, never scored as a retrieval candidate. Any
  department chunk fetched pulls the relevant `common.*` chunks alongside it, in
  code. It is the file that says what applies *beyond* the department just
  retrieved, so topic matching would select it exactly when it is least needed.
- **Discharge Process and Bed Management co-fetch.** They verify each other's
  numbers, not just their own: Bed Management's prediction accuracy depends on
  Discharge's real timings, and a hospital's *reported* Discharge turnaround can
  only be checked for authenticity against Bed Management's own bed-allocation
  and physical-admission timestamps. A query touching either pulls both, enforced
  in code rather than left to topic matching.
- **The playbook is conditional**: fetched when the function is Discharge Process
  **and** the turn is an open-ended consulting turn rather than a single-fact
  lookup.
- **`retrieve: never` chunks are never fetched**, under any score.
- **Everything retrieved goes inside the `<internal_reference>` block**, below the
  resident rules and after the cache breakpoint. The rules govern how the answer
  is delivered; these chunks govern what is in it.
- **Hard cap of 12,000 tokens of chunks per turn.** Past that the retriever
  returns the highest-scoring chunks within budget and logs what it dropped.
- Paths, pins and co-fetch pairs are declared in `publish/manifest.yaml`. Read
  them from there rather than hard-coding a file list, so adding a function is a
  manifest change and not a code change.

## Using the retrieved material

1. **Work through §7 in order** where the query calls for the full method: ground
   the reasoning in §7.1's subject-matter considerations; verify this hospital's
   actual practice against §3's baseline dependencies using §7.2's questions;
   check the right §7.3 financial parameters; then construct a recommended
   solution per §7.4's four aspects. The cost-benefit analysis and the
   before/after comparison are mandatory parts of that last step.
2. **Apply the `common-elements` frameworks alongside the department content**,
   not instead of it.
3. **For Bed Management, apply the Peak-Load Staffing Method from
   `common.peak-load` directly.** `bed-management.md` carries the resulting ratio
   at KPI #17 but does not itself walk through the method, so run it from
   `common.peak-load` at both the §7.2 verification stage and the §7.4
   solution-construction stage.
4. **Say what you do not know.** Where a query reaches past what the retrieved
   chunks establish, name the gap rather than presenting a construction as an
   established finding. Confidence-tagging applies here — see the active
   register's rules.

## Two things the IDs do not promise

**§7.4 sub-numbering is not parallel across departments.** `dis.7.4.1` and
`bed.7.4.1` are both automation, but `opd.7.4.1` is process changes and manpower:
the OPD file's own sequencing note states that it deliberately reverses the
default order, putting process and manpower before automation. A cross-reference
to another department's solution aspect must name the aspect, not the index.

**A section number is not an ID.** IDs are assigned once and never change, even
if a section is renumbered or moved. The v1 package carried a systematic
two-turn offset for exactly this reason — four files labelling themselves by a
number that later moved — and the same failure mode applies to sections.

## The gap register

A query that matches no chunk above the relevance floor is answered from general
capability and logged: the question asked, that no section matched, and what was
said. That log is the file-writing backlog, so the remaining functions get
written in the order hospitals actually ask about them, and coverage rate becomes
a measurable signal of when the library is sufficient rather than a guess.
