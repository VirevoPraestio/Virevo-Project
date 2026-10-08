# Bed Management — Worked Conversation Playbook

A worked example of how Tojo should actually run an unscripted, subscriber-path consulting conversation about beds not turning over — built from a full practice conversation (approved turn by turn, a 300-bed super-specialty single unit in Nagpur, 31 turns, closed at the first-step proposal) and generalized into a reusable pattern. Read this alongside `bed-management.md` (the domain content this conversation draws on) and `claude/06-bed-management-answering-rules.md` (the behaviour rules this conversation produced).

**What this file is, and what it is not.** `06-bed-management-answering-rules.md` is the operational file — it holds the rules distilled out of this conversation, written for any hospital, and it is what a live bed query should load. This document is the worked conversation *behind* those rules, in the same nine-section shape as `discharge-process-conversation-playbook.md`, kept for reference. It is not a second runtime file, and it should not be chunked into the skill package alongside `06`, which would duplicate it.

**How to use this file:** this is a pattern to recognize and adapt, not a script to replay. The specific numbers below — 1 PM arrivals, 4–5 hours of dead bed time, ₹1.5–2 crore, ₹17–19.5 lakhs, three Admissions Executives — belong to one practice hospital and must never be reused for a different hospital. Always re-derive them from that hospital's own §7.2/§7.3 answers. What generalizes is the *shape*: which question comes before which, when a claim has to be tested rather than accepted, where the roles get introduced, and how an objection gets narrowed instead of argued.

---

## 1. The overall arc

Once a hospital has committed to beds as its problem, the arc runs in this order. Stage numbering follows `discharge-process-conversation-playbook.md` §1 so the two can be read side by side; the notes say where this conversation actually diverged.

1. **Case reveal** — the comparable hospital's day, shown as a revenue clock. One turn, ask and reveal merged.
2. **Dependency verification** (`bed-management.md` §7.2) — five areas, agenda shown as a graphic, questions put one at a time.
3. **Financial sizing** (`bed-management.md` §7.3) — but *not* at the end of verification. See the ordering note below; this is the arc's sharpest difference from Discharge.
4. **Diagnosis** — a distinct turn, separate from the solution. **This conversation did not deliver one. See §2.**
5. **Five-part solution overview** — a short intro, the five as clickable options, one overview graphic.
6. **Deep-dive on each part, one at a time**, in the order the hospital picks them.
7. **Handle follow-ups and objections** as they come, mid-deep-dive.
8. **Summary** on request.
9. **First step** — a sequenced, low-commitment plan that includes its own exit.
10. **Subscription pivot**, if the hospital reaches it (`03-subscription-pricing-rules.md`).

**The ordering difference that matters: sizing moves earlier.** Discharge's arc puts financial sizing after dependency verification. Bed Management cannot wait that long, and this conversation established why as a universal rule. The moment the first real quantity lands — here, dead bed time computed from the hospital's own two billing timestamps — the next turn asks for ARPOB, ALOS, average daily revenue, bed and ICU occupancy separately, and OT utilisation and daily OT revenue. Batched, like facility intake. Hours on their own move nobody; the conversion is what makes everything already collected land. Any verification questions still outstanding get asked *after* the conversion, not before.

**Do not scale a duration across the bed base before the parameters are in.** The mistake made and corrected in this conversation was to defer the conversion on the grounds that ARPOB had not been asked for. The first half of that reasoning was wrong — the conversion belongs at the point the quantity lands — and the second half was the actual failure: ARPOB should already have been asked.

---

## 2. Diagnosis — and the gap this conversation left

**The honest finding first: this conversation never gave a diagnosis turn.** Verification ran to Turn 16, the consolidation deliberately listed the findings in collection order rather than causal order (because causal order *is* the diagnosis), and Turn 17 went straight to the five-part overview. The mechanism was never named to the hospital as its own beat. It surfaced piecemeal instead — two reasons offered inside a verification turn, then a "today" box inside the process-changes part five turns later.

Discharge's playbook warns about the inverse error: a diagnosis turn that ends on "does this make sense to try?" with the solution never shown. This is the other half of the same failure. **Both departments need stage 4 as its own turn, and a future run of this conversation should insert one between consolidation and the overview.**

**What that turn should have said.** The mechanism was fully assembled by Turn 11 and is stronger than the one the department file leads with:

> The hospital allocates a bed only once it has been confirmed physically ready, or about to be. So allocation cannot happen until the bed is nearly free. So there is nothing to call a patient in against until late in the day. So the patient arrives at 1 PM and is in the bed at 4:30 PM — and the assumption that beds would not be free earlier has made itself true.

That is `bed-management.md` §6's self-fulfilling loop with the serialised team taken out and a process rule put in its place. It was discovered in conversation, and it is a cleaner statement of the mechanism than the team-shaped version, because it survives a hospital that has already fixed its team structure.

**The stronger diagnostic template for this department** is not "a dead window nobody uses" as it is for Discharge, but **a rule that forbids committing to a bed before it is free** — then the arithmetic showing what that rule costs. Name the rule, trace the four consequences in order, then put the hospital's own clock times against it.

**Do not start the loss at physical vacancy.** This was the single biggest correction in the session and it cascaded through eight sections of the department file. Dead bed time is a **bill-to-bill** quantity: it begins when the outgoing patient's final bill closes — typically late morning, with the patient still in the bed — and ends when the first billable entry appears against the next patient. Everything in between earns nothing on that bed, pharmacy, diagnostics, procedures and any dependent OT slot included. Reasoning from vacancy understates it by hours. The turnaround clock and the revenue clock are different clocks, and a good Discharge TAT is not evidence the bed was earning.

---

## 3. The five-part solution overview

Same five parts as Discharge, same source — `common-elements.md`'s four-aspect Solution Construction Method plus KPIs as the fifth:

1. Automations
2. Process changes
3. Key people & buy-in
4. Team/role changes
5. KPIs & targets

Per the progressive reveal pattern: a short intro naming that there are five, the five as clickable options alongside one overview graphic, then each part's detail as the hospital engages with it. **All five at once was built as a reference and explicitly rejected** — five graphics in one message is not a conversation, and the hospital loses the ability to go deep on the part it actually cares about. One part per turn, even in a review context.

Two things this department requires of the overview turn specifically, both of which Discharge does not:

- **State whether this is the full design or the reduced form, and show the two figures that decided it.** §7.4's scaling pivot is monthly-average daily admissions against the average beds available the previous night. Here: roughly 41 admissions against roughly 33 beds free overnight, so the pivot is crossed and the full design applies. This is the beat where the pivot finding is legitimately revealed — it is a recommendation, and this is the recommendation stage.
- **Rule out the occupancy gain at the outset, in its own box.** Occupancy is set by demand and length of stay. It does not improve because scheduling improved. Carrying this as a graphic box rather than prose means the text never has to repeat it, and it is the claim most likely to get softened later.

---

## 4. Deep-diving each part — what "done well" looks like per part

Each part is three bullets plus its own graphic. **The bullets carry *why*, never *what*** — the graphic already holds what changes, so a bullet restating a box is wasted.

- **Automations**: the daily cadence as a chain, ending on call-in timing as the outcome, because that is the element that breaks the mechanism. Tie one bullet directly to the hospital's own clock time (here, the 1 PM arrival) — that is the only place the turn should invoke their data. Effect box: sub-30-minute Admission TAT, with documentation named as the only irreducible stage.
- **Process changes**: **this part carries more than it looks like it does, and it took three attempts to get right.** Four bands, in this order: the day as it runs today (muted, ending on the hospital's own late-afternoon timings) → the day as it would run → the four smaller changes as cards → **the two owners, both amber, joined by a two-way arrow**. The decoupling of admissions from discharges belongs here, not in the teams part, because it is the change the whole solution rests on. So do both manager roles: they come out of the process change, and the teams part only sizes and prices what has already been explained.
- **Key people & buy-in**: name where the resistance concentrates instead of reassuring six groups equally. It is not the voice recording — that is a spoken note on a round they already do. It is the 24-hour discharge commitment, which is a clinical judgement stated a day early, and it holds only where the system puts a *predicted* date in front of the doctor to confirm or correct. Ask a clinician to produce a date and it fails; ask them to check one and it does not. **Draw the reporting shape rather than describing it** — one box across the top with the sign-off tag, one line down splitting into two equal amber boxes. Said in prose it does not land. Quantify the ask on the most resistant group even when the answer is zero, and attach what would falsify it: a separate round, a form or a login appearing in the build.
- **Team/role changes**: run the two sizing chains **side by side, same shape, different closing colour**. The settled side ends red; the unsettled side ends amber, because amber is the dependency colour and that number genuinely depends on data you do not have. Here the admissions side settled (41 admissions/day, 5 per person per hour, a narrow arrival window → three on the afternoon shift, with the peak hour setting the number rather than minimum cover) and the discharge side did not, for want of the hospital's discharge day pattern. **Cite our own wrong default as the reason not to guess** — `discharge-process.md` §7.4.4(b)'s case where the flat 15-a-day rule said three and the two-window check said two. Refusing to apply a rule is credible when you can point to the time it failed. Two effect boxes: what it costs, and what is still needed.
- **KPIs & targets**: eight, not the eighteen in §8 — roughly six new plus the two or three they already track, with their own figures written into the existing ones. Then name **one** to start with; dead bed time, because it moves whenever any of the others improve. Separate the adoption measures from the outcome measures and say which are which: beds mapped by the freeze, discharge signals given in time, admissions finished by noon fail first and fail visibly, which makes them the early warning. Weekly, not monthly — a month hides a bad week. And hold the occupancy line here hardest, because the last turn of a pitch is where the temptation to soften it peaks.

---

## 5. Handling follow-ups and pushback mid-deep-dive

Four patterns, all of which arrived in this conversation and three of which have no equivalent in the Discharge playbook.

**A claim that contradicts the hospital's own figures.** This is the pattern that produced the universal evidence-over-assertion rule, and it is the most important thing in this file. Asked directly and early whether one team runs both discharges and admissions, the hospital said the two run *together*, with admissions spread across the day — the opposite of the department's signature failure mode. Two turns later its own clock times put patients in the bed between 4:30 and 8 PM. **A claimed overlap does not close the enquiry.** Take the numbers as the better guide; say so gently and specifically, attributing the difference to the gap between intent and the floor rather than to the user being wrong; give one or two reasons drawn from the hospital's *own* answers rather than general theory; and keep going, because a divergence is a finding and not a verdict. The boundary condition matters: the rule fires on a conflict between the user's account and the user's own facts, never against an estimate of Tojo's own.

**"How would all of this be achieved? There seem to be multiple things to be done."** Split the reply — a short frame naming the gap between what the earlier graphic showed and what this turn explains, one paragraph of actual explanation, then a new graphic carrying the rest. The useful answer here was that six steps are not six projects: almost all of it falls out of one engine reading data the hospital already holds. Three bands — what you provide, what we build, what comes out — plus the one prerequisite and the one blocker. **Name the Discharge prerequisite in a box where it cannot be skimmed past**, rather than letting the hospital believe Bed Management can be bought on its own. That is commercially inconvenient and the file requires it.

**"Will you be doing all this for me? What if I don't have such systems?"** Two questions bundled, and answering only the first reads as a dodge. Split what is supplied from what is required, then **name the threshold at which the answer changes**. Three of five inputs are the provider's — voice capture with its own transcription, prescription capture automated rather than handed back as a form, admission stage timestamps captured as the new flow runs. Two are genuine dependencies and are marked amber: read access to whatever holds admissions, discharges, investigations and charges today, and the bill-close/bill-open join, which is a reporting change on a billing system they already run. Then the threshold: where most of the record is still on paper, this is **a different project rather than a slower one**. A vendor willing to name where the project becomes a different project is making a checkable claim.

**"A hospital is too dynamic. Will such hard rules work? There will be resistance."** Two objections that get different treatment. Concede the resistance half in the first line and park it for the key-people part. Answer the dynamism half here, because it is testable against figures already given. Argue at the level the mechanism actually works at: the mapping never needed to know *which* bed frees when, only *how many* will free and roughly when — and occupancy, average stay and the admissions volume derived from them supply exactly that, and are stable at a hospital that feels chaotic bed by bed. Use their own earlier answers as the second piece of evidence: a hospital that gave admission stage timings to the half-hour has described a repeating process, and nobody can characterise a random one that precisely. Give one or two reasons the floor feels more chaotic than the figures say — the exceptional day is what staff carry home while the ordinary week passes unremarked, and there is no baseline today, so every deviation reads as chaos because nothing ever defined normal. **Then narrow what is being claimed, visually:** what is fixed is *when* decisions get made; what is untouched is *what* gets decided. Most of the objection dissolves once the claim is that size. Close on a change being absorbed rather than forbidden — something moves, the map re-runs, only the affected call-in times re-issue, the change is recorded. An override is a logged event, not a rule broken; a hospital hears "hard rule" as "something I will be blamed for breaching", and that reading has to be dismantled explicitly. Do not promise nothing will go wrong, and do not claim the cadence removes variability. It makes the consequence of variability visible within minutes instead of at the end of the day, and that is the honest claim.

**"Other than these automations, what else would you be doing?"** Do not re-show the overview — that replays a turn already seen and carries nothing new. Show a **progress view**: the covered part muted with a COVERED tag, the remaining four plain, each labelled not with its title but with **the question it answers**. The titles were already on screen; a graphic repeating them with a tick added is a replay.

---

## 6. Substituting real data for estimates

- **Hand the stage question over as a blank chain, then redraw the same layout filled.** Five stages, dashed `hh:mm` fields, a caption saying typical clock times are enough. The filled state reuses the same coordinates so the continuity carries "same diagram, now answered". Same technique for the two billing timestamps, as a two-box blank pair rather than a selector, since the ask is two clock times.
- **Arithmetic on the hospital's own numbers is not interpretation and may be shown.** What the total *means* waits for the diagnosis. In practice that meant showing that about an hour of a three-and-a-half-hour Admission TAT is documentation, without yet saying what the rest of it is.
- **Show the working; never hand over a total without it.** The revenue conversion ran as a four-box derivation chain — occupied beds → turnovers a day → hours recoverable per turnover → bed-days a year — so every line could be audited rather than taken on trust.
- **Where the hospital's own figures do not reconcile, use the conservative basis and say in the caption that it understates.** Here, 267 occupied beds × ₹8,000 ARPOB came to ₹21.4 lakhs a day against a stated average daily revenue of ₹28 lakhs, so ARPOB was evidently a bed-linked figure rather than total revenue per occupied bed. The conversion used the lower basis and the effect box said the real loss is probably higher.
- **Count each effect once and name the line it is counted in.** Earlier admission → earlier procedure → shorter stay produces the *same* bed-days already in the revenue line. Give the length-of-stay effect its own box and say in that box that it is counted once, above. Never add it on top. And never assert an ALOS-day figure carried over from another department's practice hospital.
- **Name what is excluded rather than estimating it.** OT was left out and said to be left out: 75% utilisation on ₹5 lakhs a day is real headroom, but sizing it needs to know how many cases are actually lost or deferred for want of a confirmed bed, which had not been asked.
- **Flag a derived figure as derived, in the image.** The ~41 admissions a day was computed from the hospital's own occupancy and stay, not measured, and every graphic carrying it said so.
- **Carry the missing inputs openly, turn after turn.** Four remained outstanding at close: the desk roster per shift on both sides, the hour-by-hour arrival pattern, internal bed-transfer volume, and when discharges actually happen through the day. Without the roster, a headcount recommendation is a gross requirement rather than an incremental change — say that rather than presenting the total as the cost.

---

## 7. Landing on next steps

Four steps, and **the hospital's day does not change until the third**. Read access from IT, about two weeks. Then four weeks of measurement — dead bed time per bed, the five admission stages — during which nobody works differently. Then the day changes: the two jobs start running together and call-in times go out per bed. Then the build, Discharge first, because the bed plan runs on its timings.

**The load-bearing box is the exit.** At the end of step two the hospital has its own dead bed time rather than ours — and if it is smaller than we said, they know that before spending anything on people or process. A close that includes its own exit is more persuasive than one that does not, and where the headline figure was derived from parameters they have not fully verified, it is the only honest close available.

**Sequencing follows the files, not sales convenience.** Discharge automation before bed mapping, because `bed-management.md` §7.4.2 makes Discharge a prerequisite rather than an independent rollout. The commercially easier order is the reverse.

**Ask for the minimum that starts it.** Two things: read access, and one name to own this until the two managers are in place.

On the summary that precedes it, when asked for: three findings across the top, **muted, because they are the hospital's facts and not our proposals**; the five parts as one-line cards; worth against cost side by side, with the comparison left for the reader to draw rather than asserted as a multiple. Do not re-show any of the five part graphics.

---

## 8. Two rules about the conversation itself, both learned the hard way

**Every part ends by offering the next one, by name.** Inside a multi-part reveal the close is always the handover — one sentence naming what comes next. That holds for a side question answered inside a part exactly as much as for the part itself. Ending on your own last point and leaving the hospital to navigate is a miss.

**Introduce a role before you price it, and explain a dependent department before you ask about it.** A salary attached to a job title the hospital has never heard of reads as a sales line however sound the arithmetic. Introduce the Bed Manager by the job — hold the plan for the day, decide which patient goes to which bed and when to call each one in, sort out the beds that do not free on time — then why it cannot be added to a desk role at this size: on a busy day the patient in front of you wins, so tomorrow's plan never gets made. The Discharge Manager follows immediately and is not optional, on one line that has to be said: *the bed plan is only as good as the discharge times it is built on.* Give one side an owner and not the other and the side without one sets the pace. They are peers; neither reports to the other, because the moment one does, that side's problems stop being raised. Then ask — do they have someone on the job full time, would they consider creating it, or do they want the reasoning in more detail. Never ask about the role before explaining why it exists; a bare question invites a "no" that then has to be argued back.

A dependent department gets **explained, not mentioned** — a dependency named in passing raises a doubt and leaves it open — and it gets explained in **process changes, key people and team/role changes only, never in automation**. Dependencies are about how the work is run, who runs it and who is needed. Opening two departments during an automation conversation turns one solution into two and loses the person before either is understood.

**And plain English is a second pass, not an intention.** Write the response, then rewrite every sentence: work out what it is trying to say and say that instead. One idea per sentence — a thought added after a dash or semicolon is a second sentence. The everyday word over the professional one. A verb, not a noun phrase built from it. Read it aloud; if the hospital's own administrator could not say it that way in their own board meeting, rewrite it. The tests exist because the instruction alone kept being satisfied by the writer and not the reader. Box titles inside graphics are where dense phrasing survives longest, because they are short and look deliberate. Most turns under about 150 words.

---

## 9. What this second worked example changes about the pattern

With two departments now worked end to end, the shape in §1–§7 holds — but this conversation moved three things that the Discharge playbook states differently, and they should be treated as corrections to the shared pattern rather than as Bed Management quirks:

- **Financial sizing moves from after verification to the moment the first quantity lands.** Universal, now in the response rules.
- **Both manager roles, and the decoupling that creates the need for them, belong in process changes** — the teams part only sizes and prices what has already been explained. Likely true for any department with a threshold role.
- **A claimed absence of the failure mode is a claim about practice, to be tested against the hospital's own clock times before the failure mode is ruled out.** Also universal, and the origin of the evidence-over-assertion rule.

Two things remain genuinely department-specific and must not be carried across: **Discharge's finding that its solution is identical at every hospital size, with only the cost-justification varying — Bed Management is the opposite, its solution scales with the demand-vs-supply pivot**; and the bill-to-bill definition of dead bed time, which is this department's own quantity even though bill finalisation is a Discharge-side event.

**Still open from this run**, and worth fixing before a third department is worked:

- The missing diagnosis turn in §2 — the conversation went from consolidation to solution overview with the mechanism never named as its own beat.
- Turns 1 to 21 predate the plain-English rules and were never redone in the approved style. The rules are now specific enough that a redo pass is mechanical.
- The conversation stopped at the first-step ask, so the subscription pivot in stage 10 has never been exercised for this department.
- `bed-management.md` §8 and `discharge-process.md` §8 KPI revisions are still deferred — the bill-to-bill dead-bed-time KPI, the Admission TAT KPIs and their five stage timings, and the corrected manager-threshold tracking.
