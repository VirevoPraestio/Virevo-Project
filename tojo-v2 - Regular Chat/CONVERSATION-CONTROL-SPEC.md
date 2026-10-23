# Tojo v2 — Conversation Control and Plain English

What was added, where each piece sits in the pipeline, and what has to change in
code for it to work. Read alongside `IMPLEMENTATION-GUIDE.md`, which this
extends rather than replaces.

---

## 1. What was added

| File | Loaded | Job |
|---|---|---|
| `rules/always-on/00c-plain-english.md` | every call, cached | every word the hospital can see — chat, SVG, HTML, selector labels — plus the pre-send quality check |
| `rules/always-on/00d-conversation-control.md` | every call, cached | the sequence contract, the movement test, the meander test, the intervention trigger |
| `rules/on-demand/05-case-intervention.md` | when the trigger fires | the three variants, matching rules, honesty guardrails, the reveal's shape, the close |
| `references/conversation-sequences.md` | by stage, every unscripted turn | eight `seq.*` chunks: canonical arc, meander test, four department overlays |
| `index/seq.card.md` | per candidate function | the index card |
| `index/points/seq.points.md` | never | the point extract, merged into POINT-INDEX |

Resident cost rises by roughly 2,350 tokens — the two new always-on files —
which is a cached-prefix cost at 0.1×, paid once per conversation rather than
per turn. Per-turn retrieval rises by roughly 2,500–3,100 tokens on unscripted
turns, inside the existing 12,000-token budget.

### Why two of them are always-on

`00c` governs every word the hospital can see. A turn that builds no graphic
loads none of the on-demand rules, and that is exactly the turn where dense
phrasing survives — a one-line answer, a question, a handover.

`00d` has to evaluate on every turn. A rule that is only loaded once something
has gone wrong cannot be the thing that notices it is going wrong. The case
material is the expensive part and that stays on-demand.

---

## 2. Where it sits in the pipeline

Insert into the existing eleven-step pipeline:

- **Step 1, resolve flow stage** — also resolve `sequence_id` and
  `sequence_step`, and increment `turns_in_step`. The stage resolver already
  exists; this is a second, finer position alongside it.
- **Step 2, cached prefix** — the order becomes `00-core`, `00c`, `00d`,
  `GROUP-CATALOGUE`, then exactly one register. **This changes the prefix, so
  the first turn after deploy writes a new cache rather than reading the old
  one.** Expected, once.
- **Step 6, assemble the knowledge block** — add the stage-fetched sequence
  chunks: `seq.1`, `seq.2`, and the overlay for `sequence_id`. These are fetched
  by stage, not scored, and are exempt from `chunks_per_query` while still
  counting against `budget_tokens`.
- **Step 7, variable tail** — add the six conversation-control fields.
- **Step 8, on-demand rules** — add `05-case-intervention.md` when the trigger
  fired on this turn.
- **Step 11, log** — add `sequence_step`, `turns_in_step`, whether the trigger
  fired, which variant ran, and the outcome recorded on the following turn.

---

## 3. The state machine

Six fields, defined in `manifest.yaml` under `conversation_control`. The
transitions:

```
step opens              turns_in_step = 0, step_held = 0
each user turn          turns_in_step += 1
exit condition met      step closes -> next step opens (reset)
justified deviation     step_held += 1, turns_in_step suspended for that turn
                        (hold is capped at 2 per step)
turns_in_step >= 4
  and exit unmet        TRIGGER -> load 05, deliver the intervention
intervention delivered  case_offers_made += 1, turns_in_step = 0
following turn          last_case_outcome = favourable | unfavourable
two unfavourable        trigger suppressed for the rest of the conversation
```

**Who decides what.** The backend counts; the model judges. Incrementing,
resetting and suppressing are arithmetic and belong in code. Whether an exit
condition is met, whether a deviation is justified, and whether the hospital's
next turn was favourable are judgements the model returns alongside its
response — as a small structured field, not parsed back out of the prose.

**The classifier can carry this.** The Haiku classifier already planned for
function group and flow stage is the right place for step resolution and
outcome reading. Do not make the consulting model do the bookkeeping in prose.

**Inference fallback.** Where the fields are absent, the rules tell the model to
infer them from the conversation and say nothing about having done so. That is
what makes the rules work before the backend work lands. It drifts over long
conversations, which is the reason the fields exist.

---

## 4. Code changes required

**`lint_chunks.py` — one line.** The prefix tuple gains `seq`:

```python
PREFIXES = ("bed", "dis", "opd", "sup", "common", "play", "seq")
```

Without it, every chunk in the new file fails on `prefix not in PREFIXES`.

**`lint_points.py`** — no change expected; it resolves point ids against chunk
ids and the new extract follows the existing row format. Run it and confirm.

**POINT-INDEX regeneration** — `seq.points.md` is in the merge list. Regenerate
before the next build; a hand-edit of the merged file is discarded.

**The retriever** — one new fetch path (stage-fetched, not scored) and one new
on-demand condition. Neither touches the `needs`/`see` resolution, and the new
chunks use at most one `needs` each, so the worst-case one-hop pull is
unaffected.

---

## 5. What to verify

| After | Verify | How it fails if you don't |
|---|---|---|
| deploy | `cache_read_input_tokens` > 0 from the second turn of a new conversation | The prefix changed; a wrong order now produces zero hits with no error, as before |
| step resolution | `sequence_step` changes over a conversation and `turns_in_step` returns to zero | A counter that never resets fires an intervention on every fourth turn forever |
| the meander test | a deepening follow-up chain does **not** fire the trigger | The worst failure mode: cutting into a hospital that is working, with a case study |
| the meander test | four turns of different topics on one unclosed step **does** fire | The behaviour the whole addition exists for, silently never happening |
| the trigger | `05-case-intervention.md` is absent from the prompt until the turn it fires | Resident cost rises for nothing, and the model reaches for cases unprompted |
| the intervention | variant matches `case_offers_made` and `last_case_outcome` | Asking permission on the first one, or showing a fourth after two refusals |
| the intervention | no hospital name, person, date or contract value appears | A claim the hospital may check |
| outcome reading | `last_case_outcome` is set from what they did, not how warmly they said it | A polite brush-off read as acceptance, and the next variant opens wrong |
| plain English | spot-check words inside SVGs, not only chat text | Box titles are where dense phrasing survives longest |

**Build the meander eval the way the retrieval eval was built, before the
feature.** Twenty conversations with a known-correct answer per turn — fire or
do not fire. Half should be deepening chains that must not fire. A trigger that
is slightly too eager is worse than one slightly too slow, because the hospital
feels it.

---

## 6. Two decisions that need a human

**The case is constructed, and the guardrails are where the honesty lives.**
The agreed behaviour is that Tojo presents a single comparable hospital, matched
on bed band, city tier and hospital type, built from the library's own patterns
rather than from a record of a named engagement. `05-case-intervention.md` §4
therefore forbids the details that would make it a checkable claim — no
hospital name, no person, no date, no contract value, no offer of an
introduction — and requires that every figure inside the case carry a `case`
mark in the graphic so it cannot be mistaken for something measured at this
hospital.

Where a hospital asks directly who it was, the rule has Tojo answer plainly that
Virevo does not name the hospitals it works with, and that what is on offer is
the pattern rather than the introduction. That is the one place the rule will
not construct: a named client, a referral or a verification the hospital could
chase. If Virevo would rather these cases were drawn from real anonymised
engagements, the change is small — `05` §3 becomes a lookup against a case bank
and §4's guardrails mostly fall away — and it is a stronger position in front of
a hospital that probes.

**Two of the four overlays are derived, not observed.** `seq.3` and `seq.4` come
from worked, approved conversations. `seq.5` and `seq.6` come from the shared
arc plus each file's own §7 structure, and their candidate mechanisms are
reasoned rather than practised. Both say so in the chunk. Re-cut them from a
real conversation before they are relied on to decide whether a conversation is
meandering.

---

## 7. Knock-on edits worth making

Not required for this to work, and each is a small, separate change:

- **`00-core.md` §4** now duplicates two lines of `00c` (plain English, no
  jargon; say a figure once). Leave the duplication or cut the lines from core —
  but do not let the two drift, because core wins on sight and `00c` is the one
  with the procedure.
- **`00a` and `00b`** each carry a banned-phrase list. `00c` §4 is now the same
  list in a third place. One list, three homes; worth consolidating into `00c`
  and having the registers point at it.
- **The Bed playbook's §8** holds the plain-English rules this package now takes
  from it. That section can shrink to a pointer once `00c` is live.
- **`GROUP-CATALOGUE.md` is untouched**, deliberately. The sequence file is
  fetched by stage rather than scored by topic, so it needs no group.
