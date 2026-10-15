# Handover — Conversation Control and Plain English

**For the developer wiring this into Tojo. This file is written to be handed
whole to your own Claude session as context before you start.**

Everything described here is content and configuration. None of it runs. Your
job is the code around it.

---

## 0. If you are an AI assistant reading this

You have been given this file because a developer is adding a feature to an
existing system called Tojo — a hospital-operations consulting agent built on
the Claude API. Read this whole file before proposing any code.

Six files were added to the Tojo v2 package. One existing file was edited
(`publish/manifest.yaml`). Two code changes are needed, plus retriever work.
The sections below say exactly what, in the order that fails cheapest.

Do not redesign the retrieval architecture. It is measured, it works, and the
reasons for its odd-looking choices are written down in `CHUNKING-SPEC.md` and
`IMPLEMENTATION-GUIDE.md`. If something here looks wrong, check those two first.

---

## 1. What Tojo is, in one paragraph

Tojo talks to hospital owners and administrators about an operational problem —
beds not turning over, discharges taking too long, patients going elsewhere for
tests, supply chain. It runs a consulting conversation: verify how the hospital
actually works, size the loss in money, name the root cause, propose a
five-part solution, walk through each part. Its knowledge lives in a chunked
reference library retrieved per turn. Its behaviour lives in a set of rule
files, some resident in every call and some fetched on demand. It answers with
short text plus server-rendered SVG diagrams.

---

## 2. What this change does

Two problems were being solved.

**One: the conversation wanders.** Tojo asks a question, the hospital answers
and mentions something else, Tojo follows it, and four exchanges later the
original question is still unanswered. Nothing is wrong with any individual
turn; the conversation just never lands. The fix is a sequence of named steps
with checkable exit conditions, a counter on the open step, and an intervention
that fires at four turns: Tojo shows a comparable hospital's case — same bed
band, same city tier, different state — where the same problem turned out to
have a cause nobody assumed, and offers four ways to use it.

**Two: the writing drifts into management English.** Especially inside the
SVG diagrams, where short box titles look deliberate and survive editing. The
fix is an always-on rule covering every word the hospital can see, with a
procedure rather than an instruction.

---

## 3. The files

Added:

| Path | Loaded |
|---|---|
| `rules/always-on/00c-plain-english.md` | every call, inside the cached prefix |
| `rules/always-on/00d-conversation-control.md` | every call, inside the cached prefix |
| `rules/on-demand/05-case-intervention.md` | only on the turn the trigger fires |
| `skill/virevo-hospital-ops/references/conversation-sequences.md` | by stage, every unscripted turn |
| `skill/virevo-hospital-ops/index/seq.card.md` | per candidate function |
| `skill/virevo-hospital-ops/index/points/seq.points.md` | never at runtime — merged into POINT-INDEX |

Edited:

| Path | What changed |
|---|---|
| `publish/manifest.yaml` | new files in `lint_only`, `always_on`, `on_demand`, `generated.merge_of`; new `retrieved.sequences` block; new `conversation_control` block; two new tests |

Also written: `CONVERSATION-CONTROL-SPEC.md`, the design document. Read it
after this one.

---

## 4. The six state fields

These are the whole feature, from a code point of view. They live alongside
`flow_stage` and the hospital record, and are supplied in the variable tail of
each call.

| Field | Type | Meaning |
|---|---|---|
| `sequence_id` | `dis` / `bed` / `opd` / `sup` | which department's sequence is running |
| `sequence_step` | string, e.g. `C3`, `G2` | the smallest open step |
| `turns_in_step` | integer | user turns since that step opened, inclusive |
| `step_held` | integer, max 2 | turns the counter has been held for a justified deviation |
| `case_offers_made` | integer | case interventions delivered so far |
| `last_case_outcome` | `favourable` / `unfavourable` / unset | how the previous one landed |

Transitions:

```
step opens              turns_in_step = 0, step_held = 0
each user turn          turns_in_step += 1
exit condition met      close step -> open next -> reset
justified deviation     step_held += 1, this turn does not count (max 2 per step)
turns_in_step >= 4
  and exit unmet        FIRE: load 05-case-intervention.md for this turn
delivered               case_offers_made += 1, turns_in_step = 0
next turn               set last_case_outcome
case_offers_made >= 2
  and last unfavourable suppress the trigger for the rest of the conversation
```

**Split of responsibility.** The backend counts, resets and suppresses — that is
arithmetic. The model judges three things and returns them as structured output
alongside its response, never parsed back out of prose:

- did the open step's exit condition become true this turn, and what made it true
- was this turn a justified deviation (correction / real data / hospital's agenda)
- how did the hospital's last turn receive the case (favourable / unfavourable)

Use the Haiku classifier already planned for flow stage and function group. Do
not make the consulting model do bookkeeping in its reply.

**Before any of that exists**, the rules tell the model to infer the fields from
the conversation. So the feature works on day one and gets sharper when the
fields land. Inference drifts over long conversations, which is why the fields
exist.

---

## 5. Build order

Cheapest failure first.

**Step 1 — the one-line lint change.** In `publish/lint_chunks.py`:

```python
PREFIXES = ("bed", "dis", "opd", "sup", "common", "play", "seq")
```

Then run both lints over the library. `lint_chunks.py` must exit zero.
`lint_points.py` should need no change — run it and confirm.

**Step 2 — regenerate POINT-INDEX.** `seq.points.md` is now in
`generated.merge_of`. Regenerate from the extracts. Never hand-edit the merged
file; the next build discards it.

**Step 3 — the prefix.** Emit the cached prefix in this exact order:

```
00-core.md
00c-plain-english.md
00d-conversation-control.md
GROUP-CATALOGUE.md
<exactly one register: 00a or 00b>
--- cache breakpoint ---
```

This changes the prefix, so the first turn after deploy writes a new cache
instead of reading the old one. That is expected, once. **Confirm
`cache_read_input_tokens` is non-zero on turn two of a fresh conversation.** A
wrong order produces zero cache hits with no error at all.

**Step 4 — stage-fetched sequence chunks.** On every unscripted turn, add
`seq.1`, `seq.2`, and the overlay for `sequence_id` (`seq.3` dis, `seq.4` bed,
`seq.5` opd, `seq.6` sup). Add `seq.7` when `step_held > 0`. These are fetched
by stage, not scored against the query, and are exempt from the 3–6
`chunks_per_query` range while still counting against `budget_tokens`. See §7
for how to make this cheaper.

**Step 5 — the trigger.** When `turns_in_step >= 4` and the exit condition is
unmet and the trigger is not suppressed, append `rules/on-demand/05-case-intervention.md`
to that one call. Not before, not after.

**Step 6 — state tracking.** Wire the six fields and the classifier calls.

**Step 7 — logging.** Add to the existing per-turn log: `sequence_step`,
`turns_in_step`, `step_held`, whether the trigger fired, which variant, and the
outcome recorded on the following turn.

---

## 6. Acceptance tests

Two of these are the feature. The rest stop it being worse than nothing.

| Test | Pass condition |
|---|---|
| cache | `cache_read_input_tokens` > 0 from turn two of a new conversation |
| counter resets | `turns_in_step` returns to zero across a conversation; `sequence_step` advances |
| **fires correctly** | a conversation of four turns on four different topics with one unclosed step **fires** |
| **does not fire** | a four-turn chain of deepening follow-ups (each answer decomposing the last) **does not fire** |
| on-demand | `05-case-intervention.md` is absent from the assembled prompt on every turn except the one it fires |
| variant | variant matches `case_offers_made` and `last_case_outcome`; no permission asked on the first |
| suppression | no third intervention after two unfavourable outcomes |
| guardrails | no hospital name, person, date or contract value appears in any case |
| sequences present | `seq.1`, `seq.2` and exactly one overlay on every unscripted turn |
| existing guarantees | the five pre-existing retrieval tests still pass, especially `assert_no_chunk_reached_only_via_see` |

**Build the fire/do-not-fire eval before the feature, not after.** Twenty
conversations, a known-correct answer per turn. Half should be deepening chains
that must not fire. A trigger that is slightly too eager is worse than one
slightly too slow, because the hospital feels the interruption.

---

## 7. Five things that are easy to get wrong

**The counter runs on the step, not the stage and not the subject.** Dependency
verification is one stage and six steps. Counting on the stage fires an
intervention in the middle of normal verification, every time.

**A deepening follow-up chain must not fire.** Same subject for four turns is
fine when each turn goes one level deeper — that is the hospital working. The
test is direction, not subject: a chain goes down, meandering goes round.

**A justified deviation holds the counter; it does not reset it.** Two holds per
step, then the test runs anyway. If you implement hold as reset, the trigger can
be postponed forever by a hospital that keeps interrupting.

**`see` is still never a fetch instruction.** The new chunks add `see` edges.
Followed transitively, `see` pulls 95% of the library — worse than no chunking
at all. It is a scoring boost only. The existing test for this must stay green.

**`05-case-intervention.md` must not become resident.** It is the expensive part
and it is only correct on the turn it fires. If it is in every prompt the model
starts reaching for case studies unprompted, which is the opposite of the
design.

---

## 8. One product decision you should know about

The comparable hospital in a case intervention is **constructed**, not drawn
from a record of a real named engagement. It is matched to the hospital on bed
band, city tier and hospital type, and built from the patterns in the library.

`05-case-intervention.md` §4 therefore forbids the details that would turn an
illustration into a checkable claim: no hospital name, no person, no date, no
contract value, no offer of an introduction. Every figure inside a case carries
a `case` mark in the rendered SVG so it cannot be mistaken for something
measured at the hospital being talked to. If a hospital asks who it was, Tojo
says plainly that Virevo does not name the hospitals it works with.

**Do not relax any of those guardrails for realism.** If the business later
decides to use real anonymised engagements instead, the change is small — §3
becomes a lookup against a case bank — and someone should make that call
deliberately rather than by loosening the rule.

---

## 9. Where to read next

1. `CONVERSATION-CONTROL-SPEC.md` — the design behind this handover
2. `IMPLEMENTATION-GUIDE.md` — the existing eleven-step pipeline this plugs into
3. `CHUNKING-SPEC.md` — why retrieval looks the way it does
4. `publish/manifest.yaml` — the runtime contract; read the file list from here,
   not from code
5. `AGENT-USAGE-AND-TOKEN-GUIDE.md` — turn-by-turn use, and where the tokens go
