---
id: discharge-process-conversation-playbook
title: Discharge process conversation playbook
description: A worked example of a full unscripted discharge consulting conversation, generalising to other departments
keywords: [playbook, discharge, conversation, worked example]
kind: topic
version: 2026-09-15
source_file: skill/virevo-hospital-ops/references/discharge-process-conversation-playbook.md
source_author: Avishek
---
<!--chunk
id: play.0
title: Discharge Process — Worked Conversation Playbook
summary: Establishes that this file is an adaptable pattern rather than a script, and that its worked numbers belong to one practice hospital and must be re-derived for any other.
keys: discharge process, conversation playbook, worked example, unscripted consulting, pattern not script, re-derive numbers, practice hospital, subscriber path
needs: none
see: play.1
tokens: 310
-->
# Discharge Process — Worked Conversation Playbook

A worked example of how Tojo should actually run an unscripted, subscriber-path consulting conversation about Discharge Process Delays — built from a full practice conversation (approved turn-by-turn, a 250-bed super-specialty hospital in Bhubaneswar) and generalized into a reusable pattern. Read this alongside `discharge-process.md` (the domain content this conversation draws on) and the `virevo-tojo-chat-rules` package (the behavioral rules this conversation demonstrates).

**How to use this file:** this is a pattern to recognize and adapt, not a script to replay. The specific numbers below (7 PM evening calls, 40–45 discharges/day, ₹2.7–3.0 Cr/yr, 2 Discharge Executives) belong to one practice hospital and must never be reused for a different hospital — always re-derive them from that hospital's own §7.2/§7.3 answers. What generalizes is the *shape* of the conversation: which question comes before which, when a diagnosis is separate from a solution, how a five-part solution gets unpacked one part at a time, and how to handle a hospital pushing back on an assumption. This same shape applies to Bed Management and OPD-Diagnostics conversations too — see §9.

<!--chunk
id: play.1
title: The overall arc
summary: Establishes the fixed order of the unscripted consulting arc and that diagnosis and solution must be delivered as two separate steps, not one.
keys: consulting arc, order of stages, dependency verification, financial sizing, occupancy sizing, diagnosis separate from solution, five-part solution, next steps, subscription pivot
needs: none
see: play.0, play.2, dis.7.2.1, dis.7.3, common.shared-considerations
tokens: 460
-->
## 1. The overall arc

Once a hospital has committed to Discharge Process Delays as its problem (past the scripted case-study/diagnostic-question turns — see the `virevo-tojo-chat` sales-flow rules for that part), the unscripted consulting arc runs in this order:

1. **Dependency verification** (`discharge-process.md` §7.2) — ask the practice-pattern questions, one at a time, before proposing anything.
2. **Financial/occupancy sizing** (`discharge-process.md` §7.3 + `common-elements.md`'s shared consideration set) — size how urgent this actually is for *this* hospital.
3. **Diagnosis** — a distinct turn, separate from the solution. Name the root cause plainly (see §2 below); don't jump straight to "here's what I'd build."
4. **Five-part solution overview** — a short intro naming the five parts, presented as clickable options plus one overview graphic (see §3).
5. **Deep-dive on each part, one at a time**, in whatever order the hospital engages with them — not all five unpacked at once (see §4).
6. **Handle follow-ups and objections** as they come, mid-deep-dive (see §5).
7. **Real-data substitution** — once the hospital shares real numbers, redo the sizing and the affected graphics with real data in place of estimates, and call out explicitly what changed (see §6).
8. **Next steps** — synthesize everything into a short, sequenced plan (see §7).
9. **Subscription pivot**, if the hospital asks or the conversation naturally reaches it (see `03-subscription-pricing-rules.md`).

Steps 1–3 happen before the hospital has seen any solution content at all. A common failure mode<!--m--> worth watching for explicitly<!--/m-->: presenting a diagnosis turn that ends on "does this make sense to try?" without the five-part solution ever actually having been shown is an easy gap to fall into — diagnosis and solution are two separate turns, not one.

<!--chunk
id: play.2
title: "Diagnosis: name the mechanism, not just the symptom"
summary: Establishes that the diagnosis stage names the concrete mechanism — a dead window plus an ownership gap — rather than a flat root-cause label, and flags constructed numbers as constructed.
keys: diagnosis, root cause, dead window, under-utilised time, lack of ownership, no single owner, occupancy threshold, confidence tag, estimates versus data
needs: none
see: play.1, play.6, dis.7.4.4
tokens: 410
-->
## 2. Diagnosis: name the mechanism, not just the symptom

A flat root-cause label ("no single owner") is weaker than naming the specific mechanism that root cause produces. The stronger pattern, worked out in this conversation:

> "Your real problem is not delays in discharge. It is under-utilised time and resource, and lack of ownership."

followed by the concrete mechanism: identify a dead window in the existing process (here, the gap between a doctor's evening provisional call and next-morning confirmation), name roughly how much of the process could already happen in that window if anyone used it, and give the concrete reasons nobody does today (no automation means doing the work twice; nothing is coordinated until confirmation; nobody has ever worked out how to use the window). Then name the second root cause (no single owner) tied to a concrete, hospital-specific trigger — here, the occupancy threshold from `discharge-process.md` §7.4.4.

This "X% of the process could already happen in this window, and here's why nobody uses it today" framing is a stronger diagnostic template than a flat label — it generalizes to any department where a similar dead window or ownership gap exists, not just Discharge.

Numbers used at this stage that come from Tojo's own construction, not the hospital's confirmed data (e.g., an assumed 7 PM call / 10–11 AM confirmation before the hospital has actually stated its own times), should be flagged as such — either with an explicit confidence tag or by saying plainly "these are still my construction, not your numbers" — and swapped out the moment real data arrives (see §6).

<!--chunk
id: play.3
title: The five-part solution overview
summary: Establishes that the solution is presented as five named parts revealed progressively, mapping the four-aspect Solution Construction Method plus KPIs and targets.
keys: five-part solution, automations, process changes, key people and buy-in, team and role changes, KPIs and targets, progressive reveal, clickable options, overview graphic
needs: none
see: play.2, play.4, common.solution-method
tokens: 180
-->
## 3. The five-part solution overview

Once a hospital's diagnosis is accepted, present the solution as five named parts — this maps directly onto `common-elements.md`'s four-aspect Solution Construction Method plus KPIs & targets as a fifth:

1. Automations
2. Process changes
3. Key people & buy-in
4. Team/role changes
5. KPIs & targets

Per the progressive multi-point reveal pattern (`01-response-rules.md` §3): a short intro line naming that there are five parts, the five presented as clickable options alongside one overview graphic showing all five at a glance, then each part's detail (with its own supporting graphic) revealed only as the hospital engages with it — never all five unpacked in one message.

<!--chunk
id: play.4
title: Deep-diving each part — what "done well" looks like per part
summary: Establishes what a well-done deep-dive looks like for each of the five parts: hospital-specific content, before/after diagrams, a real ratio-check, and curated KPIs.
keys: deep dive, automations, transcriptionist chain, before and after diagram, biggest leak, key people buy-in, discharge executive, peak-load staffing, KPI curation, no baseline yet
needs: play.3
see: play.5, dis.7.4, dis.7.4.1, dis.7.4.3, dis.7.4.4, dis.8, common.peak-load
tokens: 610
-->
## 4. Deep-diving each part — what "done well" looks like per part

Each of the five parts can carry a genuinely deep, hospital-specific treatment, not just a restatement of `discharge-process.md` §7.4's generic content. Worked examples from this conversation, generalizable to any hospital:

- **Automations**: translate `discharge-process.md` §7.4.1's generic capability description into this hospital's specific named bottlenecks (e.g. the transcriptionist chain identified in dependency verification, the specific billing turnaround time the hospital reported) rather than restating the generic automation description unchanged.
- **Process changes**: a function-by-function today-vs-with-Virevo comparison (doctor's evening round, discharge summary, nursing & billing prep, billing sign-off, insurance rounds, family/transport), each shown as an actual before/after diagram per `02-image-creation-rules.md` §3 — not prose. Flag the single biggest leak (here, discharge-summary drafting) as the amber "biggest leak" box.
- **Key people & buy-in**: narrow `discharge-process.md` §7.4.3's generic ten-role list down to the roles this specific conversation has actually touched, and tie each role's reassurance to something the hospital itself said (e.g. "your doctors already said they won't sign a final summary in the evening, but will sign a provisional one for cash patients — that's exactly the mechanism this automation runs on").
- **Team/role changes**: don't stop at the flat threshold figure in `discharge-process.md` §7.4.4 — run the actual Peak-Load Staffing ratio-check (`common-elements.md`) against this hospital's own confirmed shift/volume pattern. See the worked example in `discharge-process.md` §7.4.4 itself, which this conversation produced: a hospital whose 40–45 discharges/day cluster into two windows (morning confirm-through-completion, evening provisional intake) needs 2 Discharge Executives sized to each window, not a naive 1-hire or a flat 3-way division of the daily total.
- **KPIs & targets**: don't present all 16 KPIs from `discharge-process.md` §8 — curate down to the subset where this hospital's own real or target numbers already exist from earlier in the conversation, and mark the rest as targets pending live data (amber) vs. already-confirmed (plain). Inventing a placeholder number for a KPI with no real data yet misrepresents an untested figure as data — say "new metric, no baseline yet" instead.

<!--chunk
id: play.5
title: Handling follow-ups and pushback mid-deep-dive
summary: Establishes how to answer a tell-me-more follow-up and how to treat a hospital's factual correction as new information rather than an objection to hold position against.
keys: follow-up questions, tell me more, text plus graphic split, decomposition chain, pushback, factual correction, hold position rule, assumed capability, new layer
needs: none
see: play.4
tokens: 400
-->
## 5. Handling follow-ups and pushback mid-deep-dive

Two patterns worth carrying into any department's deep-dive:

**"Tell me more about X" on a point already shown.** Per `01-response-rules.md` §1, split roughly in half: a short text frame naming the gap between what the earlier graphic showed and what this turn explains, one short paragraph of actual explanation, then a new graphic carrying the rest. A worked chain of these in this conversation: "tell me more about the discharge summary being drafted continuously" → "explain the first three steps, how does draft assembly work" → "how would you actually capture these events" — each follow-up decomposes the previous answer one level further, each gets its own short-text-plus-graphic treatment, never a return to pure prose.

**A hospital pushing back on an assumed capability.** When a follow-up reveals that something Tojo described as already happening isn't actually true for this hospital (e.g., "we don't capture all of these details and our doctors don't use voice notes right now"), that's genuinely new information, not resistance to argue past (`01-response-rules.md` §4's hold-position rule doesn't apply to a factual correction). The right move: acknowledge the correction plainly ("Fair challenge — I described that as if it's already how your rounds work; it isn't, and it doesn't need to be"), then reframe the capability as something Virevo adds as a new layer rather than something the hospital must already have — and show, concretely, how little that actually requires of the hospital's existing systems or staff.

<!--chunk
id: play.6
title: Substituting real data for estimates
summary: Establishes how to replace estimates with a hospital's real numbers: state what shifts, recompute every dependent figure, and name corroboration when thresholds agree.
keys: real data, estimates, recompute, discharges per day, discharge executive threshold, revenue opportunity, ALOS impact, corroboration, fill-in-the-blank graphic, timestamps
needs: none
see: play.2, play.7, dis.7.4.4
tokens: 320
-->
## 6. Substituting real data for estimates

When a hospital supplies real numbers in place of the estimates used during diagnosis:

- Say plainly which specific findings shift and by how much (e.g., "the evening-to-morning call isn't happening at a fixed time — it swings from 6 PM to 9 PM... that's actually useful: it means the dead window isn't a neat [N] hours like we assumed, it moves around").
- Recompute every downstream number that depended on the old estimate (discharges/day against the Discharge Executive threshold, revenue-opportunity figures, ALOS-impact figures) rather than leaving stale numbers next to new ones.
- Where a real number clears a threshold the estimate didn't (or vice versa), say so explicitly — two independent numbers pointing the same direction (e.g. both occupancy and confirmed daily discharge count separately clearing the Discharge Executive trigger in `discharge-process.md` §7.4.4) is worth naming as corroboration, not just reported as two separate facts.
- Use the fill-in-the-blank → filled two-state graphic pattern (`02-image-creation-rules.md` §5) when asking for granular stage-by-stage timestamps: send the hospital a blank workflow diagram to complete, then redraw the same layout with their real values in place of the blanks.

<!--chunk
id: play.7
title: Landing on next steps
summary: Establishes the closing plan shape — a low-commitment pilot, a threshold-triggered recommendation, a cost-versus-opportunity comparison, and a choice rather than a mandate.
keys: next steps, two-week pilot, ALOS reduction, threshold trigger, cost versus opportunity, stat cards, offer a choice, IT integration, HIS PACS API, defer technical questions
needs: none
see: play.2, play.6
tokens: 390
-->
## 7. Landing on next steps

Once the diagnosis and solution have been walked through and real data is in hand, synthesize into a short, sequenced plan rather than repeating everything already covered:

1. **A low-commitment pilot first** — something the hospital can run without new hires or new systems, that converts the biggest still-unconfirmed assumption (here, the ALOS-reduction estimate) into a measured fact.
2. **A threshold-triggered recommendation** — if the hospital's own confirmed numbers already clear a named trigger (here, discharges/day past the Discharge Executive threshold), say so plainly as "not a maybe-someday, you're already there" rather than softening it.
3. **A cost-vs-opportunity comparison**, shown in the graphic as stat cards, not narrated in text.
4. **A choice offered to the hospital**, not a single mandated path (e.g. "want me to walk through what the full automation does day-to-day, or would you rather start by scoping the two-week pilot?").

When the hospital picks the technical/systems-scoping branch (e.g. "let's move on" toward IT integration), apply `01-response-rules.md` §7 directly: lead with one plain-language question about their current systems rather than a full HIS/PACS/API checklist, and offer the fuller technical detail as optional. If the hospital says a technical line of questioning is premature ("this is too technical, we'll discuss this later"), that's a timing signal to defer, not a rejection of the content — park it and follow whatever the hospital asks about instead.

<!--chunk
id: play.8
title: When the hospital asks what Virevo's engagement actually consists of
summary: Establishes how to answer a question about Virevo's own delivery model honestly, flag it as Tojo's construction, and hand off once it becomes a subscription-details ask.
keys: engagement model, delivery model, done over chat, other subscriptions, other services, running software, own construction, subscription handoff, pricing rules
needs: none
see: play.1
tokens: 180
-->
## 8. When the hospital asks what Virevo's engagement actually consists of

A genuinely different kind of question can come up mid-conversation: not about the hospital's operations, but about Virevo's own delivery model ("will this be done all by you over chat, or do I need other subscriptions or services?"). Answer honestly from what the rest of the conversation has already implied (real running software connected to the hospital's systems is not something a chat conversation alone produces), flag explicitly that this is Tojo's own construction if no subscription rule has settled it yet, and hand off to `03-subscription-pricing-rules.md` the moment the conversation turns into an actual subscription-details ask.

<!--chunk
id: play.9
title: Generalizing this pattern to other departments
summary: The generalisation rule: establishes that the arc's shape, not its worked numbers, transfers directly to Bed Management and OPD-to-Diagnostics conversations.
keys: generalize, other departments, bed management, OPD to diagnostics conversion, dead window, ownership gap, peak-load staffing, bed manager, scheduling manager, KPI curation
needs: play.1
see: bed.7.4.1, bed.7.4.4, bed.8, opd.8
tokens: 360
-->
## 9. Generalizing this pattern to other departments

Nothing in §1–7 above is Discharge-specific in its *shape* — only the worked numbers and the specific mechanism (the evening/morning dead window) are. The same arc applies directly to Bed Management and OPD-to-Diagnostics Conversion conversations:

- Dependency verification → financial sizing → a separate diagnosis turn → a five-part solution overview → one-at-a-time deep-dives → real-data substitution → next steps, in that order.
- A department-specific "dead window or ownership gap" diagnostic framing (Bed Management's candidate: the informal planned-admission-vs-provisional-discharge mapping described in `bed-management.md` §7.4.1; OPD-Diagnostics' candidate: the sequential-scheduling-with-no-buffer finding in `opd-diagnostic-leakage.md`'s case study).
- The same Peak-Load Staffing ratio-check worked-example treatment for that department's own threshold role (Bed Manager in `bed-management.md` §7.4.4; Scheduling Manager in `opd-diagnostic-leakage.md` §7.4).
- The same KPI-curation approach against that department's own §8 list.

If a second and third worked example (Bed Management, OPD-Diagnostics) get built out through real practice conversations the way this one was, consider splitting this file into one shared "how to run a department deep-dive" section plus a short per-department worked-example appendix, rather than three separate near-duplicate playbook files.
