<!--chunk
id: seq.0
title: Conversation sequences — what this file is
summary: Establishes that a consulting conversation runs through named steps with stated exit conditions, and that the step rather than the stage is the unit progress is measured on.
keys: conversation sequence, stage, step, exit condition, progress, counting unit, meandering, conversation control
needs: none
see: seq.1, seq.2, play.1
tokens: 480
-->
# Conversation Sequences

The order a consulting conversation is meant to run in, written so that a
machine can tell whether it is running in that order.

`00d-conversation-control.md` holds the behaviour — what to count, when to act.
This file holds the thing being counted against: for each department, the named
steps, what each one is for, and the single condition that has to be true before
it is allowed to close.

**A stage is a phase of the arc. A step is the smallest thing inside it that can
be finished.** Dependency verification is one stage and five or six steps, one
per question area. The solution walk-through is one stage and five steps, one
per part. Progress is measured on the step, never on the stage, because a stage
that legitimately runs for fifteen turns would otherwise look like a
conversation that has stalled.

**An exit condition is written so it can be answered yes or no.** "The hospital
has given a time, or has said it does not record one" is an exit condition.
"The hospital understands the problem" is not, and a step written that way can
never close.

**Order is a default, not a rail.** Where the hospital jumps forward, follow
them and mark the skipped steps unclosed — they get picked up later or dropped
openly. Where they pull back to a closed step, answer and return. Neither is a
deviation. A deviation is going nowhere, and `seq.2` is how that is told apart
from going somewhere unexpected.

The worked playbooks are the source for the Discharge and Bed sequences
(`play.1` and the Bed playbook's own arc). The OPD and Supply Chain sequences
are derived from the shared arc plus each file's own §7 structure, and should be
re-cut from a worked conversation once one exists.

<!--chunk
id: seq.1
title: The canonical sequence
summary: The ten stages every department's consulting arc shares, each with its steps, the exit condition that closes each step, and the stages it may legitimately be followed by.
keys: canonical sequence, consulting arc, stages, steps, exit conditions, dependency verification, diagnosis, solution overview, deep dives, next steps
needs: none
see: seq.0, seq.2, play.1, common.solution-method
tokens: 1480
-->
## The canonical sequence

Shared by every department. Where a department differs, its overlay says so and
the overlay wins.

### A — Problem commitment

| Step | Exit condition |
|---|---|
| A1 · the problem is named | The hospital has stated one problem in its own words. |
| A2 · the problem is agreed | The hospital has confirmed this is the one to work on now, against the alternatives it raised. |

Next: B, or C.

### B — Case reveal (opener)

| Step | Exit condition |
|---|---|
| B1 · the comparable case is shown | The case has been shown and the hospital has responded to it, either way. |

Used where the department's overlay opens on one. Not the same thing as a case
intervention fired by `00d` §4 — that one can fire inside any stage.

Next: C.

### C — Dependency verification (§7.2)

One step per question area in the department's own question set. The overlay
names them.

| Step | Exit condition |
|---|---|
| C1 … Cn · one question area | Every question in the area has an answer, or the hospital has said plainly that it does not record that. |

A question area closes on "we don't record that". It does not stay unclosed
waiting for a number the hospital does not have — the gap is the finding.

Next: D, or the next C step.

### D — Quantity landing and financial sizing (§7.3)

| Step | Exit condition |
|---|---|
| D1 · the first real quantity | One quantity has been derived from the hospital's own figures, with the working shown. |
| D2 · the sizing parameters | ARPOB, ALOS, average daily revenue, occupancy split by bed type, and the department's own equivalents are collected. |
| D3 · the conversion | The quantity has been converted into money or beds, every line auditable, and the hospital has seen it. |

**D1 opens the moment the first quantity lands, wherever that happens.** Where
it lands mid-verification, D runs there and the remaining C steps resume after.
Hours on their own move nobody; the conversion is what makes everything already
collected land.

Next: C (if steps remain), or E.

### E — Diagnosis

| Step | Exit condition |
|---|---|
| E1 · the mechanism is named | The mechanism has been stated as its own turn — not inside a verification answer and not inside a solution part. |
| E2 · the hospital has answered it | The hospital has agreed, disagreed or corrected it. |

E is a separate turn from F. A diagnosis that ends on "shall we try this?" with
no solution shown, and a solution shown with the mechanism never named, are the
two halves of the same failure.

Next: F.

### F — Solution overview

| Step | Exit condition |
|---|---|
| F1 · the five parts are shown | The five parts are on screen as selectable options with one overview graphic, and the hospital has picked one or asked about one. |

Next: G.

### G — Deep dives

One step per part, in the order the hospital picks them.

| Step | Exit condition |
|---|---|
| G1 … G5 · one part | The part has been delivered with its own graphic, and the turn has handed over to the next part by name. |

Every part ends by offering the next one by name. That holds for a side question
answered inside a part exactly as much as for the part itself.

Next: G (next part), H, or I.

### H — Real-data substitution

| Step | Exit condition |
|---|---|
| H1 · one data drop absorbed | Every figure that depended on the replaced estimate has been recomputed, and what changed has been said. |

Opens whenever real numbers arrive, in any stage, and closes back into whatever
was running.

Next: whatever was unclosed.

### I — Next steps

| Step | Exit condition |
|---|---|
| I1 · the sequenced plan | A short ordered plan exists, with its own exit named — the point at which the hospital can stop having learned something. |
| I2 · the minimum ask | The smallest thing needed to start has been named, and the hospital has answered it. |

Next: J, or the conversation closes.

### J — Subscription pivot

| Step | Exit condition |
|---|---|
| J1 · handed to the pricing rules | The question has become a subscription-details ask and `03-subscription-pricing-rules.md` is carrying it. |

<!--chunk
id: seq.2
title: Telling movement from meandering
summary: The worked test for whether a turn advanced its step, with the two cases that are most often misread — different topics that go nowhere, and one topic that deepens properly.
keys: meandering, movement test, deviation, justified deviation, same subject, same step, decomposition chain, counter hold, four turns
needs: seq.1
see: seq.0, play.5
tokens: 1050
-->
## Telling movement from meandering

The counter in `00d` §4 runs on the open step. This section is how to decide
whether a turn closed anything, in the cases where it is genuinely hard.

### The test

Name, in a short phrase, what the turn establishes that the previous turn did
not — a fact, a number, a decision, a ruled-out option, a named disagreement. If
it cannot be named, nothing moved.

Applied to a step rather than a sentence: does the step's exit condition now
read true, and can you say what made it true?

### Meandering with different topics every turn

The common shape, and the one most often missed because the conversation feels
productive.

Tojo asks when discharges actually happen. The hospital answers, and mentions
that billing waits on pharmacy. Tojo follows the pharmacy point. The hospital
answers and raises insurance. Tojo explains how insurance rounds interact with
the morning. Four exchanges, four different subjects, and the discharge timings
— the open step — have never been recorded.

Each turn had content. None of them closed its step. The conversation went round
one larger point without landing on any part of it. This is the case the
four-step rule exists for.

### Not meandering, with the same topic every turn

The hospital asks how the discharge summary gets drafted. Then how the draft is
assembled. Then how the events behind it are captured. Same subject throughout,
and each answer decomposes the previous one by one level.

Each of those is its own step with its own exit, and each closes. The counter
restarts every time. A deepening chain is the hospital doing the work, and
cutting into it with a case intervention is the worst possible reading of the
rule.

The difference is direction, not subject. A chain goes down. Meandering goes
round.

### The three justified deviations

Hold the counter for at most two turns, then test again.

1. **A factual correction** — the hospital says something described as already
   true of them is not. The correction is absorbed before the step can close.
2. **Real data arriving** — H1 opens, the dependent figures are recomputed, and
   the step underneath resumes.
3. **The hospital set the agenda** — they asked to go somewhere else first.

Two holds per step is the limit. A third is meandering, whatever it is called.

### Not justified, however reasonable they look

- An objection answered again at greater length.
- The same question asked in different words because the first answer missed.
- A point restated after the hospital has already pushed back on it.
- An explanation that adds no fact and no number — including a good one.
- Agreement, encouragement, or a summary of where the conversation has got to.

<!--chunk
id: seq.3
title: Discharge Process — sequence overlay
summary: What the Discharge conversation does differently inside the canonical arc, including its verification areas and the mechanism its diagnosis step has to name.
keys: discharge sequence, discharge verification areas, dead window, ownership gap, discharge executive, diagnosis mechanism, solution parts, discharge overlay
needs: seq.1
see: play.2, dis.7.2.1, dis.7.4.4
tokens: 760
-->
## Discharge Process — overlay

**Opens at C.** No case-reveal stage; the arc starts at dependency
verification.

**C steps — the question areas:**

| Step | Area | Closes when |
|---|---|---|
| C1 | when the decision to discharge is made, and by whom | the evening and morning points are timed, or said not to be recorded |
| C2 | the discharge summary — who drafts it, when, how long | the drafting chain is named end to end |
| C3 | billing — turnaround, sign-off, who waits on whom | the billing turnaround is given |
| C4 | insurance and TPA rounds | the approval path and its timings are given |
| C5 | nursing, pharmacy returns, housekeeping | the handover points are named |
| C6 | volume and shape — discharges a day, how they cluster | a daily count and its pattern through the day are given |

**D sits after C by default**, unlike Bed Management. Where a quantity lands
earlier, D1 opens there.

**E — what the mechanism has to be.** Not a flat label. A dead window in the
existing process plus an ownership gap: the gap between the doctor's evening
provisional call and next-morning confirmation, how much of the process could
already run inside it, the concrete reasons nobody uses it today, and then the
second cause tied to a trigger from the hospital's own numbers.

**G — the five parts**, with the Discharge-specific weight: automations carry
the drafting chain; process changes carry the function-by-function before and
after; key people carry the roles this conversation actually touched; team
changes carry the peak-load check against their own shift pattern; KPIs are
curated down to the ones with real numbers behind them.

**Department note for the whole arc.** The Discharge solution is the same at
every hospital size — only the cost justification varies. Do not scale the
solution to the hospital; scale the case for it.

<!--chunk
id: seq.4
title: Bed Management — sequence overlay
summary: What the Bed conversation does differently, above all that financial sizing moves to the moment the first quantity lands and that the diagnosis step must not be skipped.
keys: bed management sequence, case reveal opener, dead bed time, bill to bill, early sizing, scaling pivot, diagnosis gap, bed overlay, admissions decoupling
needs: seq.1
see: bed.7.4.1, bed.7.4.4, common.occupancy-pivot
tokens: 980
-->
## Bed Management — overlay

**Opens at B.** The comparable hospital's day, shown as a revenue clock, with
the ask and the reveal merged into one turn.

**C steps — the question areas:**

| Step | Area | Closes when |
|---|---|---|
| C1 | admission stages and their timings | the stage clock times are given, or said not to be recorded |
| C2 | who runs admissions and who runs discharges | the desk structure and shift pattern are named |
| C3 | how a bed is allocated, and against what | the allocation rule is stated |
| C4 | the two billing timestamps — bill close and bill open | both are given, or the hospital says they are not joined |
| C5 | planned admissions against expected discharges | whether any mapping exists today is settled |

**D moves early, and this is the sharpest difference from Discharge.** The
moment the first real quantity lands — dead bed time computed from their own two
billing timestamps — the next turn asks for the sizing parameters as a batch:
ARPOB, ALOS, average daily revenue, bed and ICU occupancy separately, OT
utilisation and daily OT revenue. Any C steps left over are worked after the
conversion, not before.

**Never scale a duration across the bed base before the parameters are in.** The
conversion belongs at the point the quantity lands, which means the parameters
have to have been asked for by then.

**E is the step this arc most often skips, and it must not be.** The mechanism:
the hospital will not commit a bed until it has been confirmed physically ready,
so allocation cannot happen until the bed is nearly free, so there is nothing to
call a patient in against until late in the day — and the assumption that beds
would not be free earlier has made itself true. Name the rule, trace its
consequences in order, then put their own clock times against it.

**Dead bed time is bill-to-bill, not vacancy-to-occupancy.** It starts when the
outgoing patient's bill closes and ends when the first billable entry appears
against the next patient. Reasoning from physical vacancy understates it by
hours.

**F carries two things the other departments' overviews do not:** whether this
is the full design or the reduced form, with the two figures that decided it;
and the occupancy claim ruled out in its own box, because occupancy is set by
demand and length of stay and does not improve because scheduling improved.

**G — both manager roles, and the decoupling of admissions from discharges,
belong in the process-changes part.** The team part only sizes and prices what
has already been explained.

<!--chunk
id: seq.5
title: OPD to Diagnostics — sequence overlay
summary: The derived sequence for the OPD-to-diagnostics conversion arc, whose verification centres on where the patient is lost between consultation and test.
keys: OPD sequence, diagnostics conversion, scheduling buffer, patient drop off, conversion rate, scheduling manager, OPD overlay, derived sequence
needs: seq.1
see: opd.7.2, opd.8
tokens: 620
-->
## OPD to Diagnostics — overlay

Derived from the shared arc and this file's own §7 structure rather than from a
worked conversation. Re-cut it once one exists.

**Opens at C.**

| Step | Area | Closes when |
|---|---|---|
| C1 | what the consulting doctor advises, and how it is recorded | the prescription-to-order path is named |
| C2 | what happens between the consultation and the test being booked | every hand-off in between is named |
| C3 | scheduling — slots, waiting time, how far ahead | the wait a patient is actually offered is given |
| C4 | where patients drop out, and what the hospital believes about why | the hospital's own explanation is on record |
| C5 | volume and conversion — advised against done | both counts are given, or said not to be recorded |

**D** sizes the loss per lost patient against the advised volume — the revenue
per test type, and what the hospital believes it is losing today, before the
real figure is derived.

**E — the candidate mechanism** is sequential scheduling with no buffer: the
test is offered at a time that assumes the consultation ran on time, so the
first delay in the morning pushes every patient past the point where they will
wait, and they leave to have the test done elsewhere. The hospital reads this as
price or convenience, which is why it has never been fixed.

**G** sizes the Scheduling Manager role with the peak-load check, as the other
departments size theirs.

<!--chunk
id: seq.6
title: Supply Chain and Procurement — sequence overlay
summary: The derived sequence for the supply-chain arc, whose verification runs on the cross-function question clusters and whose diagnosis usually lands outside procurement.
keys: supply chain sequence, procurement, consumables, question clusters, stock outs, payment delay spiral, misattribution, supply overlay, derived sequence
needs: seq.1
see: sup.3b, sup.7.4.1
tokens: 640
-->
## Supply Chain and Procurement — overlay

Derived, like the OPD overlay. Re-cut from a worked conversation when one
exists.

**Opens at C, and C is longer here than anywhere else** — the question set runs
as cross-function clusters, and each cluster is its own step. Work only the
clusters the hospital's complaint reaches into; a cluster that is not relevant
is not a step at all.

| Step | Area | Closes when |
|---|---|---|
| C1 … Cn | one cross-function cluster | every question in the cluster has an answer or a stated gap |

**The misattribution check runs before C opens**, not inside it. A supply
complaint arrives already diagnosed more often than any other — theatre delays
blamed on procurement, stock-outs blamed on vendors, vendors blamed for slow
delivery when the real coupling is payment. Check the interdependency map and
run its root-cause probe before accepting that the problem is where the hospital
has put it. Where the map points at another department and that department's
material is not in context, say so and ask for it.

**E — the candidate mechanism** is a self-reinforcing payment-delay spiral:
invoices clear late, suppliers quietly deprioritise the hospital, lead times
stretch, the hospital buys reactively at worse prices and holds more stock, cash
gets tighter, and payments slip further. Every step of that is visible to
somebody in the hospital and the loop is visible to nobody.

**G** carries the issue, consumption and returns ledger as its automation
backbone, and the Discharge tie-in as the dependency that has to be named rather
than mentioned.

<!--chunk
id: seq.7
title: Working a deviation without losing the step
summary: How to leave an unclosed step for a correction, a data drop or a hospital-set agenda and come back to it, and how to close a step the hospital will not answer.
keys: deviation, return to step, factual correction, data drop, agenda change, unanswerable step, close on a gap, parking a step
needs: seq.2
see: seq.1, play.5
tokens: 560
-->
## Working a deviation without losing the step

A justified deviation is not a reason to abandon the step. It is a reason to
hold it.

**Leaving it.** Finish the thing that interrupted — the correction absorbed, the
figures recomputed, the question they insisted on answered. Do not start a third
thing on the way back.

**Coming back.** Return to the step by asking the one question it still needs,
with a short line that ties it to what just happened rather than restarting it
from scratch. A return that re-explains why the question was asked spends a turn
without closing anything, and under `seq.2` that turn counts.

**Closing a step the hospital cannot answer.** Where the number does not exist,
the step closes on the gap — recorded as a gap, carried openly for the rest of
the conversation, and named again at next steps. A step held open because the
answer was unsatisfying is a step that will trigger an intervention for no
reason.

**Closing a step the hospital will not answer.** Where the hospital has declined
twice, close it, say what it would have settled, and move. Asking a third time
is meandering by the definition in `seq.2`, and it is the hospital's own
conversation to steer.

**Where a deviation turns into the real conversation** — the hospital's stated
problem shifts, or the material points at another department — close the step on
what it has, and open the new sequence at A2. Do not run two sequences at once.
