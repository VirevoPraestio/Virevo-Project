---
name: virevo-hospital-ops
description: Deep hospital-operations knowledge base for the Virevo/Tojo agent — chunked, indexed reference material on Bed Management, the Discharge Process, OPD-to-Diagnostics Conversion (diagnostic leakage), and Supply Chain & Procurement for consumables, medicines and materials, plus shared cross-department frameworks (a four-aspect solution-construction method, a shared Discharge/Bed/ALOS/Occupancy consideration set, a peak-load staffing ratio method, and the 80% occupancy pivot that triggers a differently-priced owner role in every function), covering dependencies, cross-function interdependency maps, financial parameters, hospital-practice verification questions, solution construction, and KPIs. Use this whenever a question needs real operational judgment about how a hospital runs — discharge delays, ALOS, bed occupancy/admissions/ICU step-down, OPD-to-diagnostics conversion, or stock-outs, inventory, vendor rates, pharmacy revenue and item-level billing accuracy — not just the scripted virevo-tojo-chat sales demo. Trigger even if the user doesn't name a department file or say "skill" directly, e.g. "why is our discharge process so slow", "how do we reduce diagnostic leakage in OPD", "our bills are always wrong at discharge", "we keep running out of stock in the wards", "what KPIs should we track for bed management".
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

Each reference file is cut into numbered **chunks**, each carrying an ID, a
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

100 chunks across six files, 73,830 tokens. Four of those chunks — 4,700 tokens
of maintainer change-log — carry `retrieve: never` and are held out of the model
entirely, which in v1 they were not.

| Function | File | Chunks | Tokens |
|---|---|---|---|
| Supply Chain & Procurement | `references/supply-chain-procurement.md` | 28 | 21,770 |
| Bed Management | `references/bed-management.md` | 18 | 17,200 |
| OPD-to-Diagnostics Conversion | `references/opd-diagnostic-leakage.md` | 20 | 15,350 |
| Discharge Process | `references/discharge-process.md` | 19 | 12,210 |
| Discharge conversation playbook | `references/discharge-process-conversation-playbook.md` | 10 | 3,620 |
| Common elements | `references/common-elements.md` | 5 | 3,680 |

Four departments follow the same template: Purpose; Sub-functions & core
activities; Dependencies (§3, plus §3b's cross-function interdependency map);
Non-negotiables; What can flex; Failure modes; Chat-agent handling (§7.1
subject-matter considerations, §7.2 dependency verification protocol, §7.3
financial parameters, §7.4 solution construction); and KPIs. Supply Chain adds a
§0 scope note and a §7.5 on automation-readiness hurdles, and numbers its KPIs at
§8 like the others.

The playbook is not one of those. It is a worked example of a full unscripted
Discharge consulting conversation, chunked by conversation stage, and its §9
states the rule for generalising the shape to other departments.

Expect further functions in `references/` over time, using the same template.
Check `index/GROUP-CATALOGUE.md` for what is actually there rather than assuming
these are the complete set. **Capital procurement — equipment, expansion
projects, contractors, major AMC/CMC — is deliberately not in the Supply Chain
file** and does not yet have one of its own; a query about buying a machine
rather than buying what it consumes belongs in the gap register.

## §3b — the cross-function interdependency map

Every department file carries one, and it is the section to reach for when a
query arrives already diagnosed.

§3 says *who* a department depends on and how hard. §3b says *through what
mechanism*, and *what failure travels along it* — because a dependency stated as
"Discharge needs the summary from doctors" cannot be verified and produces a
generic question. Each map is a table of that department's own couplings, each
with the mechanism, the failure that propagates, and where it surfaces; followed
by a root-cause probe per row that walks *backwards* from the symptom.

The organising insight, stated in all four: **almost every cross-function failure
is misattributed at the point where it surfaces.** An OT delay is logged against
OT. A wrong bill is logged against Billing. A stock-out is logged against
Procurement. So when a query names a department, check that department's §3b
before accepting the framing — and where a row names another department as the
origin, fetch that department's §3b too.

Each department's map is its own, not a copy. Where two maps name the same edge,
the reciprocal is stated in both rows, and `index/POINT-INDEX.md`'s
cross-department table lists which pairs those are.

## Finding the right chunks

Three levels, walked in order:

1. **`index/GROUP-CATALOGUE.md`** — twelve function groups, ~470 tokens, resident
   on every call. Narrows twelve groups to one or two. This list does not grow as
   the library does; adding the hundredth file adds a row to a group, not a
   group.
2. **`index/<prefix>.card.md`** — one index card per candidate function, ~120–350
   tokens, naming every chunk and what it covers. Narrows a function to the
   chunks that answer the question.
3. **The chunks themselves** — 3–6 per query, plus whatever their `needs`
   resolve to.

Underneath all three sits **`index/POINT-INDEX.md`**: every one of the 961
individually-named points in the library — questions, KPIs, financial
parameters, dependencies, couplings, considerations, failure modes, solution
elements — each with the chunk it lives in and the phrases a hospital would
actually use for it. It is a retriever-side lookup table and never enters the
prompt. It is what turns a question phrased in the hospital's words into a chunk
id, instead of leaving the retriever to guess which section a topic probably sits
in.

Its cross-department table matters as much as its rows: concepts named in more
than one file under different words resolve to the owning chunk rather than to
whichever department the query entered from. **The §3b rows are the shortest path
for a misattributed query** — they are the only rows whose phrasebook column is
written as the complaint rather than as the mechanism.

It is generated by merging `index/points/*.points.md`. Never edit it directly;
edit the per-file extract and rebuild, or the merge overwrites the edit.

## Retrieval contract

- **`common-elements` is pinned**, never scored as a retrieval candidate. Any
  department chunk fetched pulls the relevant `common.*` chunks alongside it, in
  code.
- **Discharge Process and Bed Management co-fetch.** They verify each other's
  numbers, not just their own. A query touching either pulls both, enforced in
  code rather than left to topic matching. *(A Supply Chain / Discharge pair is
  proposed in `publish/manifest.yaml` and deliberately not adopted — see the note
  there.)*
- **The playbook is conditional**: fetched when the function is Discharge Process
  **and** the turn is an open-ended consulting turn rather than a single-fact
  lookup.
- **`retrieve: never` chunks are never fetched**, under any score.
- **Inline `<!--m-->…<!--/m-->` spans are stripped before assembly.** They carry
  provenance — who drafted a section, who approved it, on what date — and a
  retrieved chunk carrying one hands a hospital Virevo's internal review trail.
- **Everything retrieved goes inside the `<internal_reference>` block**, below the
  resident rules and after the cache breakpoint.
- **Hard cap of 12,000 tokens of chunks per turn.** Past that the retriever
  returns the highest-scoring chunks within budget and logs what it dropped.
- Paths, pins, co-fetch pairs and the retrieval contract's own tests are declared
  in `publish/manifest.yaml`. Read them from there rather than hard-coding a file
  list, so adding a function is a manifest change and not a code change.

## Using the retrieved material

1. **Check §3b before accepting the query's framing**, where the query arrived
   already diagnosed or from another function's side. Run the matching root-cause
   probe first, then the department's own §7.2 questions.
2. **Work through §7 in order** where the query calls for the full method: ground
   the reasoning in §7.1's subject-matter considerations; verify this hospital's
   actual practice against §3's baseline dependencies and §3b's couplings using
   §7.2's questions; check the right §7.3 financial parameters; then construct a
   recommended solution per §7.4's four aspects. The cost-benefit analysis and the
   before/after comparison are mandatory parts of that last step.
3. **Apply the `common-elements` frameworks alongside the department content**,
   not instead of it. Four of them now: solution construction, the shared
   consideration set, peak-load staffing, and **the 80% occupancy pivot** — one
   hospital-wide state change that alters every function's strategy and triggers a
   differently-priced owner role in each. Where a hospital reports crossing 80%,
   that chunk governs; the department file says what it means *there*.
4. **For Bed Management, apply the Peak-Load Staffing Method from
   `common.peak-load` directly.** `bed-management.md` carries the resulting ratio
   at KPI #17 but does not itself walk through the method. Supply Chain is the
   only department with **two** peaks — inbound receipt and outbound issue are
   different pools at different hours — and `common.peak-load`'s own "which ratio
   applies where" list does not yet name it.
5. **Say what you do not know.** Where a query reaches past what the retrieved
   chunks establish, name the gap rather than presenting a construction as an
   established finding.

## Three things the IDs do not promise

**§7.4 sub-numbering is not parallel across departments.** `dis.7.4.1` and
`bed.7.4.1` are both automation, but `opd.7.4.1` is process changes and manpower:
the OPD file deliberately reverses the default order. Supply Chain splits
automation across `sup.7.4.1` and `sup.7.4.1.2`. A cross-reference to another
department's solution aspect must name the aspect, not the index.

**A section number is not an ID.** IDs are assigned once and never change, even
if a section is renumbered or moved. The v1 package carried a systematic two-turn
offset for exactly this reason.

**§3b is a section number that happens to be stable, not an ID pattern.** All
four maps are numbered §3b and carry ids `dis.3b`, `bed.3b`, `opd.3b`, `sup.3b`
— but that parallelism is a convenience of the retrofit, not a guarantee. A fifth
department could put its map elsewhere and keep a different id.

## The gap register

A query that matches no chunk above the relevance floor is answered from general
capability and logged: the question asked, that no section matched, and what was
said. That log is the file-writing backlog, so the remaining functions get
written in the order hospitals actually ask about them, and coverage rate becomes
a measurable signal of when the library is sufficient rather than a guess.
