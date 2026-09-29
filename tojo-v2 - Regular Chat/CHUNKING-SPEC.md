# Tojo v2 — Chunking, Indexing and Retrieval Spec

How a reference file is cut into retrievable units, how those units are found,
and what the retriever is contractually required to fetch alongside them.

The point is not smaller files. It is that the **resident cost stays flat as the
library grows**. A flat list of 150 file summaries would itself be about 20,000
resident tokens before a single answer is composed. A two-level catalogue does
not grow: twelve group names stay twelve group names whether there are three
reference files or a hundred and fifty.

---

## 1. The three levels

| Level | What it is | Size | When it is loaded |
|---|---|---|---|
| **Group catalogue** | Twelve function groups, each naming the functions it holds | ~360 tokens | Resident on every call |
| **Index card** | One card per candidate function: what it covers, and one line per chunk | ~120–200 tokens | Fetched for the candidate functions a query names |
| **Chunks** | The content itself | ~400–2,000 tokens each | 3–6 fetched per query |

A query walks down: the catalogue narrows twelve groups to one or two, the index
cards narrow a function to the chunks that answer the question, and only those
chunks are fetched. Per query this replaces ~36,500 tokens of whole files with
roughly 7,800.

**Retrieval quality becomes load-bearing.** That is the trade the chunking makes,
and it is why §5 exists: a chunk that needs a sibling to make sense declares the
sibling, in the file, rather than relying on the retriever to notice.

---

## 2. Chunk front-matter

Every retrievable unit is preceded by an HTML-comment block. The file still reads
as markdown to a human; the retriever splits on `<!--chunk` deterministically.

```
<!--chunk
id: bed.7.4.1
title: Solution construction — automation
summary: What the automation aspect of a bed-management solution must cover, and the double-control design that keeps prediction honest.
keys: bed prediction, double control, discharge timing, automation, allocation
needs: bed.7.1, common.solution-method
tokens: 640
-->
### 7.4.1 Automation

...the section's content...
```

**Every field is required.** `publish.py` fails the build on a chunk missing any
of them, the same way it already fails on hedges, dates and status notes.

| Field | Rule |
|---|---|
| `id` | Stable forever. `<prefix>.<section number>`. Never renumbered — see §3. |
| `title` | The heading text, without the number. |
| `summary` | One sentence, ≤ 200 characters, stating **what the section establishes** — not what it is about. "Dependencies on pharmacy and billing" is a topic; "Which upstream steps must complete before a bed can be released, and which of them can run in parallel" is a summary. The index card is built from these, so a weak summary is a retrieval failure waiting to happen. |
| `keys` | Retrieval keywords, comma separated. Include the words a hospital administrator would actually use, not only the ones in the heading. 4–10 of them. |
| `needs` | **At most two** chunk IDs, or `none`. Hard dependency: this chunk cannot be understood without them. Fetched with it, one hop only. See §5. |
| `see` | Chunk IDs that are related but not required, or `none`. Never auto-fetched; they gain a scoring boost when this chunk is selected. See §5. |
| `tokens` | Estimated size at 4 characters per token, rounded to the nearest 10. |
| `retrieve` | Optional. The only value is `never`. Omit it on anything retrievable — see §2.1. |

### 2.1 `retrieve: never` — maintainer content that must not reach the model

Three of the five reference files carry a status and change-log block: what was
revised, what is still open, what is awaiting approval. These are load-bearing
for a maintainer and actively harmful at inference.

The package's own publish spec already fails a build when a runtime file carries
a status note, and the reason is specific: a block saying a section is unfinished
makes the model discount that section, and a block saying it is approved makes
the model reason about its authority. Neither failure shows up in the output —
the answer is just quietly off-spec.

Chunking gives a cleaner answer than deletion. The block stays in the file where
a maintainer will find it, and carries `retrieve: never`, so the retriever will
not fetch it under any score. Three chunks carry the field today:

| Chunk | What it holds | Tokens kept out of the model |
|---|---|---|
| `bed.status` | Bed Management change log and open items | 1,510 |
| `dis.7.status` | Discharge Process change log and "still open" | 820 |
| `opd.status` | OPD-Diagnostics completion note | 60 |

That is 2,390 tokens of maintainer content which, in v1, was inside a file the
retriever fetched whole. It was reaching the model on every query into those
departments.

### 2.2 Inline maintainer spans

Not all maintainer content sits in its own block. Approval stamps and drafting
notes are woven into otherwise-retrievable prose — a KPI list whose header reads
"drafted 2026-09-02, approved as drafted 2026-09-09", a dependency table with a
parenthetical approval note in a cell.

A retrieved chunk carrying one of those hands a hospital Virevo's internal
review trail. Chunk-level `retrieve: never` is the wrong instrument, because the
rest of the section is exactly what the query wanted.

So a fragment can be marked inline:

```
### 8. KPIs <!--m-->(drafted 2026-09-02, approved as drafted 2026-09-09)<!--/m-->
```

The span stays in the file. The assembler strips `<!--m-->…<!--/m-->` before the
chunk reaches the model, and the lint ignores anything inside one when it scans
for dates, hedges and status notes. Eighteen fragments across four files carry
this today; every one of them was inherited from v1, where it was reaching the
model in full — including, in two files, a header line naming who drafted each
KPI list and who approved it on which date.

**Only chunks are assembled.** Text outside any `<!--chunk` marker — a file's H1
and its header line — is never fetched, so it is structurally out of reach. The
two file headers that carried a review trail are wrapped anyway, because
"structurally out of reach" is a claim about an assembler that has not been
written yet.

**Wrap provenance, never a correction.** The line is worth stating because it
comes up repeatedly. Who wrote a section, who approved it and when: wrap it. A
note saying a KPI's threshold has been superseded and the section is out of step:
leave it. One of those hides something private; the other is the only thing
stopping the model from asserting a stale figure to a hospital as current. Where
a correction note is the last line of defence, it stays visible and the real fix
is a human correcting the content it describes.

---

## 3. IDs are stable, and numbers are not identity

The `+2 turn-number offset` in the v1 package happened because four files
labelled themselves by a number that later moved. The same failure mode applies
to section numbers, so:

- An `id` is assigned once and never changes, even if the section is renumbered,
  moved, or its heading is rewritten.
- A section that is **split** keeps its ID for the first part and appends `.1`,
  `.2` … to the rest — `bed.7.4` splitting gives `bed.7.4`, `bed.7.4.1`, … only
  if the parent still holds content; otherwise the parent ID is retired and never
  reused.
- A section that is **removed** has its ID retired. Retired IDs are listed in the
  file's index card so a dangling `needs` reference is a lint failure rather than
  a silent miss.

File prefixes:

| Prefix | File |
|---|---|
| `bed` | Bed Management |
| `dis` | Discharge Process |
| `opd` | OPD-to-Diagnostics Conversion |
| `common` | Cross-department common elements |
| `play` | Discharge Process conversation playbook |

---

## 4. How big a chunk is

**Target: 400–2,000 tokens.** Below 400 the front-matter is a meaningful fraction
of what it describes; above 2,000 the chunk is doing the job whole files used to
do badly.

The existing eight-section department template is already a chunking scheme, and
most of it is comfortably inside the range: §1–§6 together come to roughly 1,700
tokens across all six. The weight sits in §7.1, §7.2, §7.4 and §8.

**§7.4 is split into its four aspects** — automation, process changes, key people
and buy-in, team and role changes — plus the cost-benefit analysis and the
before/after comparison, which are mandatory parts of the same step and therefore
declare each other in `needs`. After that split no unit exceeds about 2,000
tokens.

**Never split mid-argument to hit the range.** A section that runs to 2,400
tokens because it is one argument stays one chunk, and its `tokens` field says
so. The range is a target, not a cap; the cap is the one in §6.

---

## 5. `needs` is hard; `see` is soft

The v1 skill warns that pulling one paragraph out of a department file loses the
structure the file was written with: §7.2's verification questions reference
§7.1's considerations by number, and §7.4's solution cross-references §7.1
through §7.3 throughout.

Whole-file retrieval preserved that by accident. Chunked retrieval has to
preserve it on purpose, so the dependency is declared in the chunk rather than
left to the retriever to infer.

**But a dependency that fires on everything carries no information.** The first
cut of this library declared 194 dependency edges across 68 chunks, resolved
transitively, and the result was measured: starting from a typical §7 chunk and
following the edges to fixpoint pulled **27 chunks and 22,600 tokens — 56% of the
library**. One starting point pulled 78%. That is not retrieval; it is whole-file
retrieval with extra steps, and it would have quietly undone the entire saving
while looking correct in every per-file check.

The corpus really is that interconnected. The mistake was using one field for two
different jobs — documenting conceptual relatedness, and expressing a fetch
policy. So there are two fields.

### `needs` — cannot be read without

At most **two** IDs. Reserved for the case where the chunk is genuinely
unreadable alone:

- it continues an argument that starts in the other chunk;
- it is a question set whose questions are defined by the other chunk;
- it applies a framework whose statement lives in the other chunk.

**Resolved one hop only, never transitively.** A chunk's needs are fetched; their
needs are not. One hop is what keeps the fetch bounded: 3–6 selected chunks plus
at most two each is at most eighteen, and typically eight. Transitive resolution
is what produced the 56%.

If a chunk seems to need three or more, one of two things is true: the chunk is
really part of a larger unit and should not have been split, or the extra
dependencies are `see` entries wearing the wrong label.

### `see` — related, and worth knowing about

Any number of IDs, and **never automatically fetched**. A `see` entry raises the
other chunk's retrieval score when this chunk is selected, so a query that
genuinely reaches into the related material finds it, and a query that does not
never pays for it.

Most of the original 194 edges belong here: a KPI that cross-references another
department's KPI, a cost line set against a benefit line, a peer role named for
comparison. All real, none load-bearing for reading the section in front of you.

### The two pinned relationships are separate from both

Enforced in code, not in front-matter, because they are policy rather than
content:

- **`common-elements` is pinned.** Any department chunk fetched pulls the
  relevant `common.*` chunks. It is the file that says what applies *beyond* the
  department just retrieved, so topic matching would select it exactly when it is
  least needed.
- **Discharge and Bed Management co-fetch.** They verify each other's numbers, so
  a query into either pulls the other's matching chunks.

The index cards already express these correctly, on their `Pinned with:` and
`Co-fetches:` lines. Front-matter should not restate them.

### The one contract the files cannot enforce

`needs` is safe even under a wrong implementation: resolving it to fixpoint costs
about 100 tokens more than one hop on average, and nothing at the worst case,
because the graph is a shallow DAG.

`see` is the opposite. Followed to fixpoint it pulls **95% of the library** —
worse than having no chunking at all. Nothing in the files prevents that; the
guarantee lives entirely in the retriever honouring `see` as a scoring signal and
never as a fetch instruction.

So the retriever needs a test for it, not a comment: assert that the assembled
context for a known query contains no chunk that was reached only through a `see`
edge. That test is the difference between this design working and this design
looking like it works.

### Cycles are fine now

Two sections can genuinely require each other — a verification protocol and its
question set, a cost line and the benefit it is set against, a Bed Manager and a
Discharge Manager named as peers. Under transitive resolution a cycle was a
disaster; under one-hop resolution it is just a pair that travels together.

---

## 6. Budget

### 6.1 What the library actually measures

Measured after chunking, not estimated:

| File | Chunks | Tokens | Largest chunk |
|---|---|---|---|
| `bed-management` | 17 | 14,340 | `bed.7.4.1` — 1,920 |
| `opd-diagnostic-leakage` | 19 | 11,010 | `opd.7.2` — 2,060 |
| `discharge-process` | 18 | 9,390 | `dis.7.2.1` — 1,970 |
| `discharge-process-conversation-playbook` | 10 | 3,620 | `play.4` — 610 |
| `common-elements` | 4 | 2,270 | `common.peak-load` — 1,150 |
| **Total** | **68** | **40,630** | |

Of those, three chunks totalling 2,390 tokens are `retrieve: never`, leaving
**65 retrievable chunks and 38,240 tokens**. One chunk, `opd.7.2`, sits 3% over
the 2,000 ceiling: its only internal boundaries are bolded lead-ins, and
splitting there would sever fourteen numbered questions from the data-access
preamble they depend on, while other chunks cite them as "§7.2 point N". It
stays whole, and its `tokens` field says so. That is the rule in §4 working, not
an exception to it.

### 6.2 Per query

| | v1 per query | v2 per query |
|---|---|---|
| Resident rules | 25,125 | 21,435 cached (0.1×) |
| Group catalogue | — | ~360 |
| Index cards | — | ~400 (2–3 functions) |
| Knowledge | 36,500 (three whole files) | ~7,000 (3–6 chunks) |

**Hard cap: 12,000 tokens of retrieved chunks per turn.** With one-hop `needs`
this is headroom rather than a constraint: 3–6 selected chunks plus at most two
dependencies each lands near 7,000. Past that the retriever
returns the highest-scoring chunks within budget and logs the ones it dropped.
The log is the signal that a query is too broad or that a chunk is too big, and
it is read, not ignored.

**Content completeness still overrides everything.** The budget governs what is
*retrieved*, never what is *written*. A section is never trimmed to fit a budget;
if it is too big, it is split.

---

## 7. The gap register

Every query that finds no chunk above the relevance floor is logged: the question
asked, that no section matched, and what the agent said from general capability.

That log is the file-writing backlog. It means the remaining files get written in
the order hospitals actually ask about them, and coverage rate becomes a
measurable signal of when the library is sufficient rather than a guess.

---

## 8. What the retriever must do, in order

1. Resolve flow stage and select exactly one register. Register selection follows
   from the resolved stage, never from model judgment.
2. Assemble the cached prefix: core rules, the one register, the universal
   method, the group catalogue. Identical every turn, in this order.
3. **Cache breakpoint.**
4. Score the query against the group catalogue; take the top one or two groups.
5. Fetch the index cards for the candidate functions in those groups.
6. Score against the index cards, with `see` entries of already-selected chunks
   boosted; take 3–6 chunks.
7. Resolve `needs` **one hop**; apply the pins and the co-fetch. Never follow
   `needs` to fixpoint — measured, that pulls over half the library.
8. Add the hospital record, and the conversation history with past figures
   stubbed.
9. Compose.

A cache hit requires an identical opening prefix, so step 2's order is fixed. A
wrong order produces zero hits with **no error** — confirm with
`cache_read_input_tokens` in the response rather than assuming.

---

## 9. The point index — the level below a chunk

A chunk is the right unit to **fetch**. It is the wrong unit to **search**.

A section described as "eleven practice-verification questions" tells a retriever
that eleven questions live there. It does not tell it what any of them are. So a
hospital saying *"we don't record when housekeeping gets notified"* matches
nothing in the index, and the retriever has to guess that a chunk summarised as a
question set is where that lives. Sometimes it guesses right. When it guesses
wrong the model answers confidently from whatever else it was handed, and the
failure is invisible.

The section index is a table of contents. The point index is the back-of-book
index, and it is the one that answers a question phrased in the reader's words
rather than the author's.

### 9.1 What counts as a point

Anything the reference files **individually name or number**: a verification
question, a KPI, a financial parameter, an upstream or downstream dependency, a
subject-matter consideration, a failure mode, a non-negotiable, a named solution
element.

Not every sentence, and not every sub-bullet. The test is whether a hospital
could ask about it by name, or an engineer could be told to go and measure it.

### 9.2 Row format

```
| point            | what it is                              | chunk      | also called            |
| bed.7.2.2#q4     | when housekeeping is notified a bed is free | bed.7.2.2 | bed ready, cleaning trigger |
| bed.8#k17        | housekeeping and transport staffing ratio   | bed.8     | porter ratio, cleaning staff |
| dis.8#k2         | % of non-insurance discharges done by 10 AM | dis.8     | morning discharge rate |
```

| Field | Rule |
|---|---|
| `point` | `<chunk id>#<kind><n>`. Derived from the chunk ID, so it cannot drift independently of it: move a section and the point IDs move with it. |
| `what it is` | The point in the source's own terms, ≤ 12 words. Not a paraphrase that introduces new vocabulary. |
| `chunk` | The chunk to fetch. Always the prefix of the point ID; carried as its own column so the file is usable as a lookup table without parsing. |
| `also called` | 0–4 phrases a hospital administrator would actually say for this. This column is what makes the index work, and it is the column most likely to be written lazily. |

Kinds: `q` question · `k` KPI · `p` financial parameter · `d` dependency ·
`c` consideration · `f` failure mode · `n` non-negotiable · `x` what can flex ·
`a` activity · `s` solution element.

### 9.3 It is not a fourth thing the model reads

The group catalogue is resident. The index cards are fetched. The point index is
**neither** — it is a lookup table the retriever searches to decide which chunks
to fetch, and it never enters the prompt. So its size does not matter at
inference, which is exactly why it can afford to be exhaustive where the index
cards cannot.

```
query ──► group catalogue ──► index cards ──► chunks
              │                    │             ▲
              └──── point index ───┴─────────────┘
                    (retriever-side only, never in the prompt)
```

### 9.4 What it surfaces for free

Because it is a flat list of everything the library individually names, three
things fall out of building it that no per-file review would have found:

- **The same concept under two names.** ALOS is defined in one department's KPI
  list and referenced in another's; a point index makes the pair visible and
  lets both resolve to the same query.
- **Points nothing measures.** A consideration that appears in §7.1 with no KPI
  anywhere in §8 is a gap in the library, not in the hospital.
- **Dangling internal references.** A point citing "§7.2 point 8" that turns out
  to be a different point than the citing text assumes.
