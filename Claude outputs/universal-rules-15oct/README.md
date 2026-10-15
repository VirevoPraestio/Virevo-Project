# Your Universal Conversation Rules in Tojo — what we did, our edits, and three questions

15 Oct 2026. From the developer side, for AB.

## Where each file went

- **00c Plain English** is in **both chats**, the regular chat and every tool. It is one copy in the vault (`vault/chat/_rules-00c-plain-english.md`), and both chats read it by id. Your text is unchanged.
- **00d Conversation control** goes to the **tools only**, by KT's decision. It travels with **05** and the **sequences** in `vault/tools/`. Your 00d and sequences text is unchanged.
- **Not used at runtime:**
  - `seq.card.md` and `seq.points.md` — the tools do not use the chat's index or point index.
  - `publish/manifest.yaml`.
  - The three developer documents.

## How 00d works in the tools

1. On every turn, the router call (the small model, which already runs every turn) also reads Tojo's last turn and the user's reply against the tool's sequence. That sequence is seq.1 and seq.2 plus the tool's own overlay: seq.3 for Discharge, seq.4 for Bed.
2. It reports:
   - which step was open;
   - whether the step closed, and what closed it;
   - whether the reply went one level deeper on the open point;
   - which step is open now;
   - whether the reply was a justified deviation;
   - how the last case landed.
3. The app does the counting:
   - Four user turns on an unclosed step fire the case.
   - A justified deviation holds the count, at most twice per step.
   - A reply that goes one level deeper closes its own step. This follows your seq.2 "a chain goes down". Without it, a long chain of "why" questions counted up to a case.
   - Two cases not taken up stop the trigger for the rest of the conversation.
   - A case never fires on the first turn, or inside Bed's stage B opener.
4. **05 is in the prompt only on the firing turn.** If that same turn is a rule-09 reset, the reset goes first and the case waits one turn.
5. 00d and the sequence are also in the answer's prompt on every tool turn. Tojo is told the count each turn, and told plainly when no case is due.

## Our edits to your texts (KT's decisions)

Please adopt these in your files, or tell us what to change, so the next drop does not undo them. The exact changes are in the `.diff` files beside this note.

1. **05, option (b)** (`05-case-intervention.diff`).
   - The comparable hospital is **"our illustration, built from similar problems we have solved"**. It is never a specific client, a record, or something Tojo saw himself.
   - The opening lines and the variant B lines are reworded to match. There is no "we worked with" and no "from my records".
   - When asked who it was: **"we can't disclose hospital names"**, plus that it is our illustration.
   - Figures in the case carry the tools' `illustrative` source, which shows as "Example only".
   - "Where they are now" becomes where a hospital like this typically ends up.
   - §7's provenance line (the regular chat's `tpl · <form> · v2`) is dropped, because it does not apply in the tools.
2. **Rule 09** (`09-reply-check.diff`). Only a negative reply is a miss.
   - `ignored` and `changed_subject` are now readings that are recorded in §3.1 but are not misses.
   - §8's Medium list no longer has them.
   - The reasoning: in the tools, a conversation drifting off its step is 00d's to notice.
3. **Rule 20** (`20-scripted-flow.diff`). The scripted case reveal now says "lines up closely with problems we've solved. Here is our illustration of a hospital like yours". It no longer says "a hospital we worked with".

## Your fire / do-not-fire test

- **The set:** 12 conversations built from your seq.2 examples, each starting at an open step.
  - 5 wander and should fire. One of them has a correction first, so it should fire at turn 5.
  - 7 go deeper or are held by corrections and real data, and must not fire. Two are six-turn "why" chains.
- **What it checks:** the router's judgement plus the app's counting. The case itself is not drawn.
- **No false fires in any run.** The misses all sit on question 1 below. Full numbers: see the last section.

## Three questions

1. **Your billing example in seq.2.** Tojo asks when discharges happen. The hospital mentions billing, then insurance, then pharmacy, and Tojo follows each one.
   - The judge sometimes reads this as the hospital moving forward through C3, C4 and C5, because each of those gets an answer. That is 00d §1: "follow them forward".
   - Sometimes it reads it as going round C1, because the discharge timings were never recorded. That is seq.2.
   - Which reading do you want? One line in 00d §1 or seq.2 saying when a side remark counts as moving forward would settle it.
   - **KT decided (15 Oct): it is drifting.** The judge now works to this: a side topic the user raises, with Tojo following it, does not move the conversation to another step. The open step stays open until its exit condition is met, or the user asks to move on. Please put the same line in 00d §1 or seq.2, so your text and the judge agree.
2. **Rule 09 and 00d on the same turn.** We let rule 09's reset go first, and the case waits one turn. Is that right?
3. **How a case is drawn in the tools.** 05 §7 describes the graphics in the regular chat's forms (the two-state pattern, the `tpl` mark). In the tools the case is drawn with your canvas blocks. Which blocks should a case use? For example, a time-window for the process with clock times, and an effect block for what moved.

## Test results

| Run | Judge | Right | Fired when it shouldn't | Missed | Cost |
|---|---|---|---|---|---|
| 1 (10 conversations) | separate small-model call | 10 of 10 | 0 | 0 | $0.25 |
| 2 (12, with `deeper`) | separate small-model call | 10 of 12 | 0 | 2 (your billing example; vague answers read as deeper) | $0.32 |
| 3 (12) | inside the router call | 8 of 12 | 0 | 4 (only 1 of the 5 wandering conversations fired) | $0.45 |
| 4 (12) | separate call, with KT's "drifting" reading | 10 of 12 | 2 (the six-turn why chains: deeper was measured against the open step) | 0 | $0.30 |
| 5 (12) | separate call, deeper = one level below the previous answer with no new subject | **12 of 12** | 0 | 0 | $0.30 |

The live app uses the separate call, as in runs 4 and 5. Inside the router call, the judgement got more generous. "The CEO. He is travelling most of the time" was read as going deeper, and "Can you also look at our pharmacy stock-outs?" as the hospital setting the agenda. KT switched 00d on for local and the dev box on 15 Oct.
