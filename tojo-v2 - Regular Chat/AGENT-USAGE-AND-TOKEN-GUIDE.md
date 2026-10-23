# How these files are used, turn by turn — and how to keep the token bill down

Two parts. **Part A** is the operating procedure: what gets loaded when, and in
what order, for a single turn of a Tojo conversation. **Part B** is where the
tokens go and what to do about it.

---

# Part A — Step by step, for one turn

## Step 0 · Before the conversation starts

Nothing from this package is loaded per-user or per-hospital. The rule files are
fixed content. The only per-conversation state is:

- `flow_stage` — scripted or unscripted, which decides the register
- the hospital record — bed count, city, type, and every number they have given
- the six conversation-control fields (`HANDOVER-FOR-DEVELOPER.md` §4)

## Step 1 · Work out where the conversation is

Two positions, and they are different things.

- **`flow_stage`** says scripted or unscripted. It picks the register, and it is
  the only thing that does.
- **`sequence_step`** says where inside the unscripted consulting arc the
  conversation is — `C3`, `G2`, and so on. It comes from the step tables in the
  department overlay.

Increment `turns_in_step`. Neither position is ever spoken to the hospital.

## Step 2 · Build the cached prefix — identical every turn

```
00-core.md                 persona, source discipline, image triggers
00c-plain-english.md       every word the hospital can see
00d-conversation-control.md the sequence contract and the meander test
GROUP-CATALOGUE.md         twelve function groups
<one register: 00a or 00b> never both
───────────────── cache breakpoint ─────────────────
```

Order is fixed. A wrong order produces zero cache hits and no error message.

## Step 3 · Route the question to chunks

Query → group catalogue (top one or two groups) → point index (the hospital's
own words → chunk ids) → index cards → 3–6 chunks. Then:

- resolve each chunk's `needs`, **one hop only**
- add the pinned `common.*` chunks, unconditionally
- add the paired department if the group was Bed or Discharge
- `see` entries raise scores; they are **never** fetched

## Step 4 · Add the sequence chunks

On every unscripted turn, by stage rather than by topic score:

| | |
|---|---|
| Always | `seq.1` the canonical arc · `seq.2` the meander test |
| Overlay | `seq.3` discharge · `seq.4` bed · `seq.5` OPD · `seq.6` supply |
| Conditional | `seq.7` when `step_held > 0` |

They are fetched by stage because a topic match would drop them exactly when the
conversation has drifted off topic — which is the moment they are needed.

## Step 5 · Add the variable tail

Hospital record · conversation history with earlier figures reduced to one-line
stubs · the six control fields · the user's message.

## Step 6 · Decide whether the intervention fires

Evaluate `00d` §4 against the open step:

- exit condition met → close the step, reset the counter, carry on
- `turns_in_step >= 4` and exit unmet and not suppressed → **fire**
- justified deviation (correction / real data / their agenda) → hold the
  counter, up to twice per step

If it fires, append `05-case-intervention.md` to this one call.

## Step 7 · Add the on-demand rules this turn actually needs

| Condition | Files |
|---|---|
| turn builds a graphic | `01-response-rules` · `02-image-creation-rules` · `04-layout-patterns` |
| turn is about pricing | `03-subscription-pricing-rules` |
| the trigger fired | `05-case-intervention` |

None of these are loaded on a turn that does not meet its condition.

## Step 8 · Generate

The model returns response text, and for a graphic turn a **form name plus slot
values** — never raw SVG. It also returns the three judgements the state machine
needs: did the step close, was this a justified deviation, how did the hospital
receive the last case.

## Step 9 · Render and deliver

Call the named form twice, wide and tall. Store the build call — form name and
slots — not the SVG. Deliver two SVG files.

## Step 10 · Update state and log

Close or hold the step, update the counters, record the outcome if a case was
shown last turn. Log tokens by block, cache read versus write, chunks retrieved,
figures stubbed, whether the trigger fired, and any query that matched nothing.

---

# Part B — Where the tokens go, and how to spend fewer

## B1 · The shape of the bill

Per turn, roughly:

| Block | Tokens | Notes |
|---|---|---|
| Cached prefix | ~23,800 | charged at 0.1× on a hit; **this is the one to cache, not to shrink** |
| Sequence chunks | ~3,300 | `seq.1` + `seq.2` + one overlay, every unscripted turn |
| Retrieved knowledge | ~7,000 | 3–6 chunks plus one-hop needs and the pins |
| On-demand rules | 0–6,000 | only on the turns that need them |
| History + record | grows | the one that quietly dominates a long conversation |

The prefix is large and that is fine — it is cached. **The things worth
attacking are the blocks that are uncached and paid in full on every single
turn: the sequence chunks and the history.**

## B2 · Nine ways to spend less

Ordered by saving per hour of work.

### 1. Two cache breakpoints, not one *(largest, cheapest)*

Today there is one breakpoint, after the register. The register differs between
conversations, so nothing below it is shared.

Put the first breakpoint **after `GROUP-CATALOGUE.md`** and the second after the
register:

```
00-core · 00c · 00d · GROUP-CATALOGUE   ── breakpoint 1 (identical for EVERY conversation)
<one register>                           ── breakpoint 2 (identical for THIS conversation)
```

Block one is then shared across every live conversation, so a new conversation
starts on a warm cache instead of writing its own. The API supports up to four
breakpoints. This is a configuration change, not a code change.

### 2. Tier the sequence chunks by how close the trigger is

`seq.2` is the meander test — about 1,050 tokens of reasoning that only matters
when the counter is near four. `seq.1` is the full canonical arc with every
exit condition, about 1,480.

Send, on an ordinary turn: a **compiled step table** for the running department
(the overlay's own table plus the step currently open and the next one, roughly
350 tokens) plus the overlay. Send full `seq.1` and `seq.2` only when
`turns_in_step >= 3`, or when a deviation is being judged.

Saving: about **2,100 tokens on most turns** — the single biggest uncached
saving available.

### 3. Compact the history into the record, not the transcript

A closed step is settled. Once a step closes, replace its turns in the history
with one structured line in the hospital record — the question area, the answer,
and any figure it produced. Keep the last two or three turns in full for voice
continuity.

A thirty-turn conversation carries far more settled fact than live context, and
settled fact belongs in a record, not a transcript. Saving grows with
conversation length and is unbounded.

### 4. Confirm figure stubbing is actually wired

`FIGURE-STUBBING-SPEC.md` already specifies replacing past figures with one-line
stubs. **Check the stub count rises with conversation length in the logs.** If
it does not, stubbing is specified but not running, and this is the largest
single saving in the package going unclaimed.

### 5. Haiku for everything that is not consulting

Flow stage, sequence step, function group, chunk selection, extracting the
hospital's stated numbers into the record, and reading how a case landed. All
classification, none of it consulting. Batch them into one classifier call per
turn rather than four.

### 6. Do not re-send a chunk that is already in the history

Where a chunk was sent in the last two or three turns and that part of the
history has not been compacted away, it is already in the context window.
Reference it by id instead of re-sending its body. Needs a small per-conversation
record of what was sent when.

### 7. Use the one-hour cache TTL

A hospital conversation has gaps — the person reads a diagram, thinks, replies
ten minutes later. The default five-minute cache window expires inside a normal
pause. The longer TTL costs more to write and far less than re-writing the whole
prefix several times per conversation.

### 8. Keep rendering out of the model

The model emits a form name and slots; the renderer builds the SVG. A single
rendered diagram is thousands of output tokens, and output is the expensive
side. This is already the design — the saving comes from never quietly falling
back to the model drawing SVG when a form raises `LayoutError`. Surface the
error; do not swallow it.

### 9. Read the budget log

`retrieval.budget_tokens` is 12,000 and the retriever logs what it dropped. A
query that regularly hits the cap is either too broad or is hitting a chunk that
should have been split. That log is the list of things to fix, and it is free.

## B3 · What not to do to save tokens

- **Do not shrink the cached prefix.** It is charged at a tenth. Cutting a rule
  to save resident tokens trades a tenth of a token for a behaviour.
- **Do not make `05-case-intervention.md` resident** so you can skip the
  conditional load. It is correct only on the turn it fires.
- **Do not drop the pinned `common.*` chunks** when the budget is tight. Topic
  matching already drops them exactly when they matter.
- **Do not resolve `needs` transitively** to avoid a second lookup. Measured,
  that pulls over half the library.
- **Do not drop the sequence chunks** on a turn where the conversation has gone
  off topic. That is the turn they exist for.
