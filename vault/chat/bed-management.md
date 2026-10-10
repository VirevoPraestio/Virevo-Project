---
id: bed-management
title: Bed management
description: Bed inventory, allocation and turnover across wards and ICU - occupancy, ALOS, admissions and step-down flow
keywords: [bed management, bed occupancy, occupancy rate, alos, average length of stay, bed turnover, bed allocation, icu, step down, admissions, ward, bed blocking, census, bed capacity]
kind: topic
version: 2026-09-15
source_file: skill/virevo-hospital-ops/references/bed-management.md
source_author: Avishek
---
# Department: Bed Management
*Division: Patient Flow & Hospital Operations<!--m--> · Status: content complete (§1–8; KPIs drafted by Claude 2026-09-02, approved by Avishek as drafted 2026-09-09; Discharge-Process TAT-verification linkage added to §3/§7.1/§7.2/§7.4.2 2026-09-09; Peak-Load Staffing retrofit into §7.1/§7.2 completed 2026-09-09; §7.3/§7.4 finalisation pass and Admission-TAT / team-staffing / role-taxonomy additions 2026-09-10; dead bed time redefined as a bill-to-bill quantity 2026-09-10)<!--/m-->*

<!--chunk
id: bed.1
title: Purpose
summary: The department's ownership: balancing bed inventory — allocation, availability and turnover — so the right patient gets the right bed while occupancy is maximised and waits minimised.
keys: purpose, bed inventory, bed allocation, bed availability, bed turnover, occupancy, ICU, ward, ER wait time, admission wait
needs: none
see: bed.2
tokens: 70
-->
## 1. Purpose
Own and continuously balance the hospital's bed inventory — allocation, availability, and turnover — across wards, ICU and other units, so the right patient gets the right bed at the right time while occupancy stays maximized and ER/admission wait times stay minimized.

<!--chunk
id: bed.2
title: Sub-functions & core activities
summary: The full activity list the department owns, and that the bed-management team and the admissions desk are in practice the same team.
keys: bed board, bed status tracking, admission desk, internal transfers, step-down, ward transfer, housekeeping turnaround, surge management, bed blocking, demand forecasting, OT scheduling, occupancy reporting
needs: none
see: bed.7.1, bed.3
tokens: 230
-->
## 2. Sub-functions & core activities
Real-time bed status tracking (bed board — occupied/vacant/blocked/being cleaned) · bed allocation for planned admissions · bed allocation for emergency/ER admissions · processing admissions at the admission desk (the bed-management team and the admissions desk are in practice the same team — see §7.1 point 5) · internal bed transfers and reallocations · ICU/step-down prioritization and transfer coordination · ward-to-ward transfers (isolation, specialty-specific moves) · coordination with Discharge for release timing · coordination with Housekeeping for turnaround/terminal cleaning · overflow/surge management at high occupancy · bed-blocking management (reserved/maintenance holds) · predictive bed-demand forecasting (scheduled admissions, OT schedule, expected discharges) · liaison with OT scheduling for post-op bed reservation · occupancy reporting to management.

<!--chunk
id: bed.3
title: Dependencies
summary: Which upstream teams Bed Management depends on and at what priority, what breaks downstream when it fails, and that Discharge's reported release timing must itself be verified.
keys: upstream dependency, downstream effect, discharge, housekeeping, emergency, ER, ICU step-down, admission registration, OT scheduling, HIS, ALOS, revenue, boarding time
needs: none
see: bed.7.1, bed.7.2.2, bed.7.3, dis.7.2.1
tokens: 380
-->
## 3. Dependencies

### Upstream — what Bed Management needs from other teams
| Depends on | Nature of dependency | Priority |
|---|---|---|
| Discharge Process | Timely bed release, *and* the accuracy of the release timing itself — see `discharge-process.md`, and this file's §7.1/§7.2 for verifying the hospital's actual Discharge TAT and discharge time rather than accepting what's reported | Critical |
| Housekeeping | Turnaround/cleaning speed | Critical |
| Emergency/ER | Unplanned demand spikes | Critical |
| ICU Step-Down Protocol | Step-down timing frees ICU and ward beds | Critical |
| Admission/Registration | Accurate incoming demand signal | High |
| OT Scheduling | Post-op bed reservation needs | High |
| IT/HIS | Real-time, accurate bed-status system | High |

### Downstream — what depends on Bed Management running well
| Affects | Nature of effect | Priority |
|---|---|---|
| ER holding/boarding time | Direct gate | Critical |
| Admission Process | Direct gate | Critical |
| OT Scheduling | Elective surgery can't be confirmed without a post-op bed | Critical |
| Daily/aggregate Revenue | Aggregate effect | Critical |
| ALOS | Bed pressure indirectly drives discharge urgency | High |
| Nursing workload distribution | — | Medium |
| Patient experience/satisfaction | — | Medium-High |

<!--m-->*(Approved as drafted; the Discharge Process row above was expanded 2026-09-09 per Avishek's instruction — see §7.1/§7.2 for the verification detail this points to.)*<!--/m-->

<!--chunk
id: bed.4
title: Non-negotiables
summary: The three things that may never be overridden: isolation and infection-control placement, clinical-acuity ICU priority, and a bed shown available that is not actually available.
keys: non-negotiable, patient safety, isolation, infection control, ICU priority, clinical acuity, phantom vacancy, bed status accuracy
needs: none
see: bed.7.2.1
tokens: 70
-->
## 4. Non-negotiables
Patient safety in bed placement — isolation/infection-control requirements are never overridden for convenience · ICU bed prioritization by clinical acuity is never overridden administratively · bed status shown as available must actually be available — no phantom vacancies.

<!--chunk
id: bed.5
title: What can flex
summary: What may be traded under pressure: ward class preference, a day's slip in elective admission scheduling, and the specific bed number within the same clinical category.
keys: flexibility, ward preference, private, sharing, elective admission, rescheduling, bed number, clinical category
needs: none
see: none
tokens: 60
-->
## 5. What can flex
Ward preference (private vs. sharing) can be temporarily reassigned under pressure · elective admission scheduling can shift by a day · specific bed number within the same clinical category is flexible.

<!--chunk
id: bed.6
title: Failure modes & early warning signs
summary: The department's signature failure mode — one team serialising discharges then admissions on a self-fulfilling assumption — and that the revenue loss starts at bill finalisation, not vacancy.
keys: failure mode, early warning, whiteboard tracking, reactive allocation, serialised team, shared team, late admissions, 4 to 8 PM, dead bed time, bill finalisation, housekeeping lag, ALOS
needs: none
see: bed.7.1, bed.7.2.2, bed.7.3, bed.7.4.1
tokens: 470
-->
## 6. Failure modes & early warning signs
Manual/whiteboard bed tracking going stale · no predictive view of upcoming vacancies, so allocation stays purely reactive · bed management run per-department/per-ward instead of as one hospital-wide view · housekeeping turnaround lag creating beds that are physically vacant but not usably available.

**The serialised shared team — this department's signature failure mode.** One team doubles as both the discharge team and the admissions desk. It works discharges through the morning until roughly 12–2 PM, and only then turns to admissions, scheduling them for later in the day. The reasoning is that discharges will take time, and without beds actually freeing up there is no point calling patients in earlier. That assumption then makes itself true: patients get admitted between 4 and 8 PM, the hospital loses every billable hour until then, ALOS rises, procedures get scheduled later because the patient arrived late, and the whole day pushes out. Two functions that should overlap are run in sequence by the same people, and nothing in the process ever tests whether the beds would in fact have been free earlier. See §7.1 point 5, §7.2 question 8, §7.4.1(e) and §7.4.1's net-effect block for the diagnosis, the verification and what it costs.

**Note where the loss actually starts.** It does not start when the bed empties. Billing on a bed stops the moment the outgoing patient's bill is finalised and sent for insurance approval — typically late morning — while the patient normally remains in that bed through approval, payment and family briefing and only leaves in the evening. So the unbilled stretch runs from bill finalisation, through the rest of the discharge tail and the housekeeping turnaround, to the moment a bill is opened on the next patient. Reasoning from physical vacancy alone understates it by hours. See §7.3 point 5.

<!--chunk
id: bed.7.1
title: Subject-matter considerations
summary: The five checks any bed query must run: the shared consideration set, Discharge-TAT verification, two peak-load staffing ratios, and Admission TAT broken into five stages.
keys: Discharge TAT, Admission TAT, stage timestamps, housekeeping staffing, transport staffing, admissions desk staffing, peak load, 5 admissions per hour, coverage floor, 250 beds, revenue clock, bed turnaround
needs: common.shared-considerations, common.peak-load
see: dis.7.2.1, dis.7.4.4, bed.7.2.2, bed.7.3, bed.7.4.1, bed.8
tokens: 1890
-->
## 7. Chat-agent handling

### 7.1 Subject-matter considerations

**1. Shared Discharge/Bed/Admission/ALOS/Occupancy considerations.**
Governed by the shared "Discharge / Bed Management / Admission / ALOS / Occupancy" consideration set in `references/common-elements.md` — apply that full 8-point list whenever Bed Management is the query subject. Bed Management is in fact the block's namesake department, so all 8 points apply directly, not just by extension.

**2. Discharge TAT and actual discharge-time verification.**
Because Bed Management's own prediction accuracy and next-admission timing depend directly on Discharge's real timings, not just its reported ones (§7.4.1(c)'s double-control design), any Bed Management query should also verify the hospital's actual Discharge TAT and actual discharge time — not just take Bed Management's own reported turnaround at face value.

Discharge TAT's *correct* definition ends when the next patient is physically admitted into that bed — or, where the bed is not reoccupied that day, when the patient physically leaves it. Hold a hospital to that definition as the proper one. Applying it as an active efficiency check is where the >80% occupancy condition in `discharge-process.md` §7.2 question 15 comes in: above that level, bed-turnaround speed matters enough that measuring through to the next admission is the only honest way to see where time is going.

Note that the TAT clock and the *revenue* clock are not the same clock. Discharge TAT runs on the patient's physical movement; dead bed time (§7.3 point 5) runs on billing, and it starts earlier — at bill finalisation, while the patient is still in the bed. Both are worth measuring, and confusing one for the other understates the loss.

See `discharge-process.md` §7.2 questions 13–15 for the specific cross-checks: the bed-turnaround gap against the next admission on that same bed, whether the TAT's clock starts from provisional or confirmed discharge, and whether it truly includes the Insurance/TPA approval window. A Bed Management problem that looks like a bed-allocation or housekeeping issue can just as easily be a Discharge-side timing or reporting issue wearing a Bed Management symptom — these two departments' numbers have to be cross-checked against each other, not read independently.

**3. Housekeeping and Transport staffing ratio (peak-load capacity check).**
Before treating a slow bed-turnaround or a stalled admission as a Bed Management allocation-logic problem, check whether the staff actually executing the physical turnover — Housekeeping (terminal cleaning/bed prep) and Transport (moving patients in for admission, and out for discharge) — have real bandwidth for the volume they're being asked to handle. Method, per the universal Peak-Load Staffing & Manpower Cost-Benefit Method in `references/common-elements.md`:
- Identify the relevant staff pool specifically for bed turnover and patient transport — exclude housekeeping/transport staff assigned to unrelated areas, and exclude supervisors.
- Establish shift structure (typically at least 2 shifts, matching this hospital's actual roster).
- Establish total daily bed-turnover volume (admissions + discharges together, since both sides generate a turnover event) and realistic per-turnover time — minutes for terminal cleaning/bed prep, minutes per patient transport.
- Apply a peak-loading split against this hospital's own confirmed admission and discharge pattern rather than an even 24-hour spread — admissions and discharges each have their own peak windows (discharge's per `discharge-process.md` §7.4.4's worked example; admissions often driven by OT scheduling and ER surge patterns), and the two peaks don't necessarily coincide.
- The result: bed-turnovers handled per housekeeping/transport staff member per hour, peak vs. off-peak — which tells you whether housekeeping/transport bandwidth, not Bed Management's allocation logic or Discharge's speed, is the actual bottleneck behind a slow or unreliable bed turnaround.

**4. Admission TAT and its stage-by-stage timestamps.**
Admission TAT is Bed Management's own core timing metric and the counterpart to Discharge TAT. It runs from the moment the patient presents at the hospital (for a planned admission), or the moment the Emergency Department prescribes admission to a bed or ICU, through to the patient being physically placed in that bed. Hospitals will normally have this number defined already — ask for it, and treat an undefined or loosely-defined Admission TAT as a finding in its own right rather than a data inconvenience to work around.

A single headline TAT is not enough to reason with. Establish each stage's timing separately, the same way `discharge-process.md` §7.2 establishes discharge's stage timings:
- Time the patient arrives, or the Emergency Department prescribes admission
- Documentation time taken
- Time the bed is allocated in the system
- Time the Ward/ICU team confirms the bed is actually ready
- Time taken to transport the patient from the Admission Desk or Emergency to the bed

Documentation is the only irreducible stage; every other stage is coordination time that automation and process change can compress. That is what makes the sub-30-minute target in §7.4.1's net-effect block a defensible floor rather than an assertion. This stage chain is also exactly what the fill-in-the-blank → filled two-state graphic pattern in `discharge-process-conversation-playbook.md` §6 is for — send the hospital the blank chain, redraw it with their own numbers in place.

**5. Bed Management / Admissions team staffing ratio (peak-load capacity check).**
The team running Bed Management is, in practice, the admissions desk as well: the same people process admissions and handle internal bed transfers and reallocations. Size it against both constraints below, and treat whichever fails first at peak as the binding one — do not stop at whichever happens to look comfortable:
- **Throughput constraint** — one person handles up to **5 admissions per hour**, applied against this hospital's actual admission peak rather than a daily average.
- **Coverage floor** — up to 250 beds, 1 person per shift; above 250 beds, 2 in the morning shift, 2 in the evening shift, 1 at night. This is a bed-count floor, not a substitute for the throughput check.

Method, per the universal Peak-Load Staffing & Manpower Cost-Benefit Method in `references/common-elements.md`:
- The staff pool is the bed-management/admissions team specifically. Exclude the discharge team where the two are genuinely separate (§7.2 question 8 establishes whether they are), and exclude the Bed Manager, whose role is coordination and process ownership rather than processing.
- The unit of work is admissions **plus internal bed transfers and allocations** — not admissions alone. Transfers consume the same team's time and are invisible in an admissions-only count.
- Admissions peak into two windows, mirroring discharge's two windows (`discharge-process.md` §7.4.4). Where the hospital runs one team for both functions, those windows collide — which is the failure mode named in §6, and the reason this ratio-check and the §6 diagnosis have to be read together rather than separately.

Points 3 and 5 are the two Bed-Management-specific instances of the universal Peak-Load Staffing & Manpower Cost-Benefit Method — see `references/common-elements.md`'s "Which ratio applies in which department" list, and KPI #17 in §8 below, which tracks point 3 on an ongoing basis once established.

<!--chunk
id: bed.7.2.1
title: Dependency verification protocol — data/system access required
summary: Which systems, rosters and timestamp sets must be obtained before any bed diagnosis, including the per-bed bill-close and bill-open times that alone make dead bed time measurable.
keys: data access, bed board access, staff roster, shift roster, admission timestamps, bill finalisation timestamp, bill initiation timestamp, discharge timestamp, bed allocation timestamp, verification data
needs: none
see: bed.3, bed.4, bed.7.1, bed.7.3, bed.7.2.2
tokens: 460
-->
### 7.2 Dependency verification protocol

**Data/system access required**, to verify how this hospital's actual practice compares against the §3 baseline dependencies and the §7.1 considerations above:
- **Bed board / bed-status system access**, to check whether bed status shown as available is actually, physically available (per §4's non-negotiable) rather than a stale or optimistic system entry.
- **Housekeeping and Transport staff rosters per shift**, against actual admission and discharge (bed-turnover) volume — to run the peak-load ratio check in §7.1 point 3.
- **Bed-management/admissions team roster per shift**, against actual admission volume *and* internal bed-transfer/reallocation volume — to run the ratio check in §7.1 point 5 against both its constraints.
- **Stage-by-stage admission timestamps** for the five stages in §7.1 point 4, not just a headline Admission TAT — arrival/Emergency prescription, documentation, bed allocated in system, Ward/ICU ready confirmation, transport to bed.
- **Bill finalisation and bill initiation timestamps, per bed** — when the outgoing patient's final bill was closed, and when the first billable entry was raised against the next patient in that same bed. These two timestamps are the actual start and end of dead bed time (§7.3 point 5); without them the quantity cannot be measured at all. Most hospitals hold both in the billing system already but have never put them side by side against the same bed, and that absence is itself a finding.
- **Bed-allocation and physical-admission timestamps, and actual (not just reported) discharge timestamps for the same beds** — to run the Discharge-TAT cross-checks in §7.1 point 2 and `discharge-process.md` §7.2 questions 13–15; this is Bed Management's own data feeding that verification, not a Discharge-side-only exercise.

<!--chunk
id: bed.7.2.2
title: Dependency verification protocol — practice-verification questions
summary: The eleven questions that test reported practice against reality, including the one-team-or-two question and its branch for a claimed overlap, and that the gap found is the diagnosis.
keys: verification questions, single owner, OT linkage, planned admission mapping, ICU mapping, staffing adequacy, Discharge TAT authenticity, one team or two, serialised team, Admission TAT, billing stop restart, diagnosis
needs: bed.7.2.1
see: common.shared-considerations, bed.6, bed.7.1, bed.7.3, dis.7.2.1
tokens: 1650
-->
**Practice-verification questions to put to the hospital directly**, one at a time, once the data picture above is in hand — drawn substantially from the shared "Discharge / Bed Management / Admission / ALOS / Occupancy" consideration set in `references/common-elements.md`, restated here as pointed questions specific to Bed Management, plus questions on staffing, Admission TAT and Discharge-TAT authenticity:

1. Is any part of Discharge, Admission, or Bed Scheduling/Management currently automated — or is bed allocation still run off a whiteboard or a manually-updated spreadsheet?
2. Is there a single, named owner of Bed Management end-to-end, or is it left to individual ward/unit staff operating off whatever guidelines Operations, Administrative, or Finance have stipulated?
3. Is OT Scheduling actually linked to Bed Management, and is there a defined protocol for admission priority between scheduled elective cases and sudden walk-ins/ER admissions — or does this get resolved ad hoc, case by case, as conflicts arise?
4. Is there an actual mechanism mapping planned admissions against provisional discharges and provisional bed availability (empty beds plus beds expected to clear from discharges) — or is tomorrow's bed picture assembled informally, if at all, before the day starts?
5. Is there an equivalent mapping mechanism for predicted ICU bed requirement — planned admissions expected to need ICU post-op or immediately — against ICU beds available or expected to free up from step-down?
6. **Housekeeping/Transport staffing adequacy** — has the hospital ever calculated housekeeping or transport staff availability per shift against actual admission/discharge volume, peak vs. off-peak, or is staffing for bed turnover simply assumed adequate because it hasn't caused a visible crisis yet? This is the practice-verification counterpart to §7.1 point 3's ratio-check — confirm whether the hospital has run this calculation before Tojo runs it for them.
7. **Does the hospital's reported Discharge TAT and discharge timing actually hold up?** Cross-check directly against `discharge-process.md` §7.2 questions 13–15 — the bed-turnaround gap to the next admission on the same bed (inefficiency or a fudged discharge time if it exceeds ~30 minutes), whether the TAT's clock starts from provisional or confirmed discharge, whether it genuinely includes the Insurance/TPA approval window, and — for hospitals above 80% occupancy — whether TAT is measured through to the next admission rather than stopping at the patient leaving the bed. Running this check needs Bed Management's own allocation/admission timestamps (per the data-access list above) to be clean and available; if they aren't, that gap is itself a finding, not just a data-access inconvenience.
8. **Does the hospital have the same team doubling with discharge and admission roles, or completely separate teams for the two roles?** Ask this directly and early — it is the single question that most often exposes §6's serialised-team failure mode. Where it is one team, follow it with what that team's day actually looks like: does it work discharges through the morning and only turn to admissions afterwards, and are admissions consequently scheduled for late afternoon or evening? A hospital that answers "one team, discharges first" has, in that answer, described the mechanism behind its own late admissions, its dead bed time and part of its ALOS — without necessarily recognising it as a problem at all. The same question appears in `discharge-process.md` §7.2, since it bears equally on both departments.

    Where the answer is the other one — two separate teams, or one team that says it runs both functions *together* — do not rule the failure mode out on that answer alone. It is a claim about practice, and this section's whole discipline is not to accept reported practice at face value. Test it against the hospital's own admission clock times (question 10). A claimed overlap sitting alongside admissions that only complete in the late afternoon or evening means the overlap is nominal and the serialisation has moved somewhere else — most commonly into a rule that a bed is not allocated until it has been confirmed physically ready, which produces exactly the same late admissions by a different route and is just as self-fulfilling. Where the clock times genuinely do show admissions landing across the day, the failure mode really is absent for that hospital, and the dead bed time in §7.3 point 5 is coming from the discharge tail, the housekeeping turnaround or allocation instead; move the enquiry there rather than closing it.
9. **Bed-management/admissions team staffing adequacy** — has anyone at the hospital calculated admissions handled per team member per hour at peak, counting internal bed transfers and reallocations alongside admissions, against the roster actually on duty? Or is this team sized by headcount-per-shift habit and assumed adequate? This is the practice-verification counterpart to §7.1 point 5's ratio-check, and it needs both of that point's constraints tested, not just the more comfortable one.
10. **Is Admission TAT defined, and are its stage timings actually available?** Ask for the hospital's own Admission TAT figure, then for the five stage timings behind it (§7.1 point 4). A hospital that has a headline number but cannot break it into stages cannot tell coordination delay from documentation time, which means it cannot know which part of its own admission process is the slow one.
11. **When does billing on a bed actually stop, and when does it restart?** Ask for the typical clock time at which the outgoing patient's final bill is closed, and the typical clock time at which the first billable entry is raised against the next patient in that bed. Then ask whether anyone has ever looked at the gap between the two. Most hospitals will answer the first two and have no answer to the third — which is exactly the finding, since that gap is dead bed time (§7.3 point 5) and nothing in the hospital currently owns it.

Where the hospital's actual practice differs from what reliable, fast bed turnover requires (e.g. no single owner, no real planned-admission-vs-discharge mapping, inadequate housekeeping/transport bandwidth at peak, one team serialising discharges and admissions per question 8, or a Discharge TAT that doesn't survive question 7's cross-check), that gap *is* the diagnosis — name it specifically rather than defaulting to a generic "improve coordination" answer, the same discipline `discharge-process.md` §7.2 applies on the Discharge side.

<!--chunk
id: bed.7.3
title: Financial parameters to check
summary: The eight financial parameters a bed diagnosis is built on, with dead bed time defined bill-to-bill rather than as physical vacancy, and HR costs broken out by function.
keys: ARPOB, ALOS, bed occupancy, ICU occupancy, daily revenue, OT utilisation, OT revenue, dead bed time, dead bed days, revenue foregone, HR cost, housekeeping cost, transport cost, Bed Manager salary
needs: none
see: common.shared-considerations, bed.3, bed.7.2.1, bed.7.4.1, bed.7.4.4, opd.7.3
tokens: 800
-->
### 7.3 Financial parameters to check

1. **ARPOB** and **ALOS** — from the shared "Discharge / Bed Management / Admission / ALOS / Occupancy" consideration set in `references/common-elements.md`, where they double as this department's baseline financial parameters.
2. **Bed Occupancy** and **ICU Occupancy** — Bed Management's own core operating numbers, per §3's downstream dependencies. Tracked separately, never blended: ICU scarcity and ward scarcity behave differently and carry very different revenue per bed-day.
3. **Daily Average Revenue** — §3 rates Daily/aggregate Revenue a Critical downstream effect of this department, so it belongs here as a checked parameter rather than only as a qualitative dependency.
4. **OT Utilisation** and **OT Revenue (daily)** — §3 rates OT Scheduling Critical on the specific ground that an elective case cannot be confirmed without a post-op bed. That makes OT the clearest place a bed-mapping failure converts directly into foregone revenue, so both numbers belong here and not only in `discharge-process.md` §7.3.
5. **Dead bed time (dead bed-days)** — the stretch during which a bed earns nothing, measured **from the finalisation of the outgoing patient's bill to the initiation of the incoming patient's bill**. This is deliberately *not* a measure of physical vacancy, and it begins well before the bed is empty: once the final bill is closed and sent for insurance approval, nothing further accrues against that bed, even though the patient normally stays in it through approval, payment, family briefing and physical exit. Every allied revenue line on that bed stops at the same moment and cannot restart until the next patient's bill is opened — pharmacy, diagnostics, procedures, and any OT slot that depends on that bed. The stretch therefore has three parts, and all three belong inside the measure: the remainder of the discharge tail after billing closes, the housekeeping turnaround, and the admission delay before the next patient arrives. Hospitals almost never separate any of this from ordinary vacancy, and most have never isolated it as a single number at all; where they haven't, that absence is itself a finding. It is the loss the whole §7.4.1 solution exists to remove, and the quantity the diagnosis should be built on. See §7.2's data-access list and question 11 for how to establish it.
6. **Revenue foregone from admissions not captured** — ER/walk-in patients diverted, turned away, or lost to boarding delay, plus elective cases postponed for want of a confirmed bed. Related to dead bed time but not the same: this is demand that never became an admission at all.
7. **HR cost for Housekeeping and Transport, broken out separately** — not blended into one hospital-wide manpower line. §7.1 point 3's peak-load ratio check cannot produce a real cost-benefit without its own cost figure, the same reason `opd-diagnostic-leakage.md` §7.3 point 2 breaks OPD HR costs out by function.
8. **HR cost for the bed-management/admissions team**, and the **Bed Manager salary cost** — the cost side of §7.4.4's two separate role decisions, needed alongside the benefit lines in §7.4.1 rather than estimated in the moment.

<!--chunk
id: bed.7.4
title: Solution construction method
summary: That this department's solution scales rather than staying constant, with the pivot set as daily admissions against the previous night's available beds, and what holds below it.
keys: solution scaling, demand versus supply, scaling pivot, reduced form, mapping cadence, emergency bed reserve, predictive LOS, ICU mapping, live link, Bed Manager trigger, four aspects
needs: common.solution-method, bed.7.4.1
see: dis.7.4, bed.7.2.2, bed.7.4.2, bed.7.4.4
tokens: 920
-->
### 7.4 Solution construction method
Follows the two universal rules in `references/common-elements.md` (cost-benefit + graphical comparison; the four-aspect shape).

**Specific to Bed Management — the solution itself scales, it does not stay constant.** This is the *opposite* of `discharge-process.md` §7.4, where the recommended solution is the same at any size and only its cost-justification varies. Per `references/common-elements.md`'s "What is NOT universal", that Discharge Process finding must not be carried across, and Bed Management's answer is genuinely different.

**The scaling pivot is demand against supply, not hospital size and not occupancy on its own:** on a monthly average, do daily admissions exceed the average number of beds that were available the previous night? Where they do, beds are genuinely contested, the full design below applies, and the hospital's discharge efficiency and admission planning are load-bearing rather than merely desirable. Where they don't, recommend the reduced form and say plainly that it *is* the reduced form — rather than presenting the full design and then arguing the hospital can't justify it yet.

*Holds at any size, occupancy or admission volume* — these are ownership and discipline requirements, not capacity-dependent ones:
- A single named owner of bed management end-to-end (§7.2 question 2).
- Some real mapping of planned admissions against provisional discharges and provisional bed availability existing *at all*, rather than tomorrow's bed picture being assembled informally (§7.2 question 4).
- Provisional discharge and provisional step-down as formally tracked concepts (§7.4.2).
- Admissions and discharges not being run serially by one team (§7.2 question 8, §7.4.2) — this costs a hospital of any size, and costs nothing to stop.
- OPD prescription capture as the intake point for planned-admission data (§7.4.2).
- The Discharge-linkage double control (§7.4.1(c)) — cross-checking Discharge's reported timings against Bed Management's own timestamps.

*Scales with the demand-vs-supply pivot above:*
- **Mapping cadence.** The twice-daily 2 PM provisional / 6 PM final freeze in §7.4.1 is sized for a hospital where beds are contested. Below the pivot, a single daily pass fed by the 5 PM Medical Supervisory checkpoint is enough — the second pass earns its place only once the day's picture actually moves between the two.
- **Emergency bed reserve.** §7.4.1(d)'s trend-derived reserve needs 2–3 years of usable history and only bites where spare capacity is scarce. Below the pivot the hospital's own slack *is* the reserve; carve out an earmarked reserve, and the trend analysis behind it, only once emergency demand actually collides with mapped planned admissions.
- **Predictive LOS modelling depth.** §7.4.1(a)/(b)'s "patients approaching typical LOS for their specific treatment" needs enough case volume per procedure type for a trend to mean anything. A lower-volume hospital gets a coarser version — LOS by department or broad procedure group rather than by specific intervention — and should be told that is what it is getting.
- **ICU mapping.** §7.4.1(b) applies where there is a real ICU with a real step-down queue. Where ICU is small, or step-down isn't a queue in practice, this collapses into the general mapping rather than running as its own pass.
- **Admissions-desk live link.** §7.4.2's two-way console link is the automated form of the control. Below the pivot, a disciplined manual confirm-back into the same day's mapping achieves the same thing.
- **The dedicated Bed Manager hire** (§7.4.4) — condition-triggered, and the pivot is one of its three triggers.

<!--chunk
id: bed.7.4.1
title: Solution construction — automation
summary: The five automation elements that produce a next-day bed picture, their 2 PM/6 PM cadence, and the benefit lines to quantify — with occupancy gain ruled out as one of them.
keys: automation, planned admission mapping, ICU bed mapping, discharge linkage, double control, emergency bed reserve, call-in timing, 2 PM mapping, 6 PM freeze, Admission TAT 30 minutes, billing brought forward, dead bed time, cost benefit
needs: common.solution-method, bed.7.4
see: bed.6, bed.7.1, bed.7.3, bed.7.4.2, bed.7.4.4, dis.7.4.1
tokens: 1920
-->
#### 1. Automation

**Core capability:** give the team running Bed Management, Admission, and Discharge together real-time visibility into what the *next day's* bed picture looks like — not just today's status — along with what could be done to mitigate any shortfall, well before it becomes a same-day crisis.

**a. Planned-admission-to-bed mapping.** Every planned admission — by department and by procedure/intervention/treatment type — gets mapped against: beds currently available, beds expected to become available, and beds likely to free up from patients approaching the typical LOS for their specific treatment (predictive, not just confirmed-discharge-based). Every planned admission ends up mapped to *some* bed. Two automatic notifications follow from this: to the Discharge team, to secure timely discharge once the doctor confirms it, and to the Medical Supervisory team, to talk to the treating doctor about beds nearing their expected LOS and get that confirmed back. The net output: an exact count of how many planned admissions remain without a confirmed bed.

**b. The same mapping, run for ICU beds.** Planned procedures are mapped against currently available ICU beds, provisional step-downs, and *probable* step-downs — patients approaching the average ICU LOS for their specific procedure — which triggers the Medical Supervisory team to confirm step-down timing with the ICU in-charge, the Intensivist, and the treating doctor. Output: a list of expected ICU requirements that could not be mapped to a bed.

**c. Discharge-process linkage as a double control.** Bed Management uses Discharge Process's actual timings to predict exactly when new patients can be admitted, and simultaneously monitors discharge efficiency itself — which function (doctors, nurses, housekeeping, dietitians, etc.) is causing delay at any given time. When both Discharge and Bed Management are automated and linked, each acts as a live check on the other, not just a one-way feed — including, per §7.1/§7.2 above, checking whether Discharge's *reported* numbers actually match what Bed Management's own allocation/admission timestamps show happened.

**d. Emergency bed reserve, trend-based.** A defined number of beds — both ICU and general — are held back from planned-admission mapping specifically for emergency/walk-in demand. The number isn't arbitrary: it's derived from 2–3 years of trend analysis by day of week, month, and time of day, showing actual historical emergency bed draw. Those beds are earmarked and excluded from the planned/anticipated-ICU/step-down mapping in (a) and (b). *(Scales with the demand-vs-supply pivot — see §7.4's scaling note above.)*

**e. Admission call-in timing — the mechanism that breaks §6's failure mode.** Because (c)'s discharge linkage gives Bed Management Discharge's *real* timings, the system can work backwards from when each mapped bed will actually be free to when that bed's incoming patient should be called in, and issue that call-in instruction rather than leaving the admissions team to guess. This is what removes the self-fulfilling assumption in §6: the team no longer has to assume beds won't free up early and default to late-afternoon admissions, because it is told, per bed, when each one will be ready. It is also what makes the sub-30-minute Admission TAT in the net-effect block below reachable — the patient is present and documented before the bed is free, rather than arriving hours after it was. Note what it attacks: not the physical vacancy, but the back end of the dead bed time defined in §7.3 point 5 — the stretch between the outgoing bill closing and the incoming one opening.

**Daily cadence:** the first mapping pass runs by **2 PM**, with immediate notifications to the relevant teams so they can start confirming with their respective doctors/functions whether every bed can be mapped or some will remain unmapped. The final mapping runs by **6 PM**, with the full mapping outcome — including how much remains unmapped and its criticality — shared with everyone concerned, so the whole hospital knows exactly what bed-management problems to expect the next day. *(This twice-daily cadence itself scales — see §7.4's scaling note above.)*

**Net effect of this level of automation — what to quantify, and against what.**
Every Bed Management solution carries the mandatory cost-benefit analysis and side-by-side before/after graphical comparison from `references/common-elements.md`. State at the outset what this department does **not** deliver: Bed Management does not directly raise occupancy, and an occupancy gain must not be presented as its benefit. What it delivers, working in conjunction with an efficient discharge process, is time and billing brought forward.

- **Time saved — Admission TAT compressed.** With the five-stage chain in §7.1 point 4 measured and its coordination stages automated, Admission TAT can come down to barely under **30 minutes**, documentation being the only irreducible stage. Quantify the gap between this hospital's own current stage timings and that floor.
- **Billing brought forward.** Patients admitted by around **12 PM** instead of the typical **4–8 PM** window means each admission's billing cycle starts several hours earlier. Multiplied across the hospital's bed-days, that is a real revenue shift with no additional clinical activity behind it — the cleanest benefit line this department has.
- **Dead bed time eliminated.** Per §7.3 point 5 — the stretch from the outgoing patient's bill being finalised to the incoming patient's bill being opened, during which the bed and every allied revenue line running through it earn nothing. Both ends of that stretch are attackable: the discharge tail after billing closes is compressed by `discharge-process.md` §7.4.1's automation, and the admission delay at the far end by (e)'s call-in timing. Quantify it as one number, bill to bill, rather than as two unrelated improvements — and expect to be the first party that has ever measured it for this hospital.
- **ALOS reduction and earlier procedure scheduling.** Indirect, and only in conjunction with an efficient discharge process: earlier admission means procedures get scheduled earlier, which pulls ALOS down, which recycles into further bed-days. Count this effect once, and state which of the lines above it is being counted in, rather than letting it inflate several.
- **Manpower.** Initially this is workload relief rather than headcount reduction — say so, rather than overclaiming a saving. Once automated, the team settles at §7.1 point 5's coverage floor: 1 person per shift up to 250 beds; 2 morning, 2 evening, 1 night above 250 beds. The Bed Manager sits on top of that and is condition-triggered per §7.4.4, irrespective of hospital size.
- **Costs to set against all of the above.** Bed Manager at **₹4–4.5 lakhs/year** where §7.4.4's conditions are met; Admissions Executives at **₹3–3.5 lakhs/year** each where §7.1 point 5's ratio-check shows a genuine shortfall; housekeeping/transport headcount where §7.1 point 3's check shows one; and the automation/integration cost, including §7.4.2's IT extraction work. Where a part of the solution is process-change-only with no direct cost — decoupling admissions from discharges is exactly that — the quantum of benefit still has to justify the disruption and the resistance §7.4.3 expects.

Derive the magnitudes from this hospital's own numbers. Do not carry a magnitude across from another hospital, from `discharge-process.md`, or from a prior conversation, and flag any figure that is still Tojo's own construction as such until the hospital confirms it.

<!--chunk
id: bed.7.4.2
title: Solution construction — process changes
summary: The nine process changes the automation presupposes, from decoupling admissions from discharges to joining bill-close and bill-open timestamps against the bed.
keys: process change, decoupling admissions, provisional discharge, provisional step-down, 24 hours advance, 1 PM ICU signal, OPD prescription capture, 5 PM rounds, IP record extraction, stage timestamps, bill-close bill-open join, admissions desk link
needs: bed.7.4.1
see: bed.7.1, bed.7.2.2, bed.7.3, bed.7.4.3, dis.7.4.1
tokens: 1130
-->
#### 2. Process changes

This solution depends on real change to existing hospital process, not just a new reporting layer on top of the old one:

- **Admissions and discharges stop being run serially by one team.** Where the hospital runs a single team for both functions (§7.2 question 8), the morning-discharges-then-afternoon-admissions sequence has to break — either by separating the two roles into distinct teams, or, where headcount won't allow that, by explicitly overlapping the two windows so admission processing for beds already mapped and call-in-scheduled (§7.4.1(e)) runs alongside the morning discharge work rather than queueing behind it. This is the process change that pays for itself fastest, because it carries no direct cost at all: the loss it removes is entirely self-inflicted.
- **Discharge Process must actually be automated — or, at minimum, its process changed enough to replicate that automation's logic** — with every allied process tied to it (per `discharge-process.md` §7.4.1, and specifically its real-time event log and the evening-provisional/morning-final timing discipline), since Bed Management's prediction accuracy depends directly on Discharge's real timings, not just its reported ones. This isn't an independent rollout, it's a prerequisite — and per §7.1/§7.2 above, it's also what makes Discharge's own reported TAT verifiable rather than taken on trust.
- **Provisional discharge (and provisional step-down) becomes a formally tracked concept**, not an informal aside during rounds. Concretely: ward patients need a provisional discharge signal **24 hours in advance**, and ICU patients need theirs **by 1 PM** (to feed the 2 PM/6 PM mapping cadence in §7.4.1). Hitting these timelines needs real predictive support from the agents — flagging likely-discharge/likely-step-down patients before a clinician has necessarily said so out loud — plus active cooperation from the clinical teams to confirm or correct those predictions promptly rather than let them sit unconfirmed.
- **OPD prescriptions become the intake point for planned-admission data.** For every planned admission, the originating OPD prescription needs to be captured to pull out the date, procedure, anticipated LOS, OT scheduling need, etc. — this is what §7.4.1(a)'s planned-admission-to-bed mapping actually maps *from*. Ideally the OPD prescription-capture step itself is automated too, not just the downstream mapping.
- **Medical Supervisory rounds get a new fixed checkpoint.** The team does rounds specifically of beds where discharge is anticipated — both provisionally confirmed ones and ones only flagged by trend analysis (average LOS for similar patient/treatment/management profiles) — to confirm or correct those predictions, **latest by 5 PM**. This is what lets Bed Management actually freeze its mapping for the next day at the 6 PM final-mapping step in §7.4.1.
- **IT must extend extraction to IP records specifically**, so the predictive-LOS trend analysis in §7.4.1(a)/(b) and this section's 5 PM round has real inpatient care data to run against, not just admission/discharge event logs.
- **Admission stage timestamps get captured as a matter of course**, for all five stages in §7.1 point 4 — not just a headline Admission TAT. Without stage-level capture the hospital cannot tell coordination delay from documentation time, and §7.4.1's net-effect claim cannot be verified after the fact.
- **Bill-close and bill-open timestamps get held against the bed, not just against the patient.** Dead bed time (§7.3 point 5) can only be measured if the outgoing patient's final-bill closure and the incoming patient's first billable entry can be read off the same bed. Most billing systems hold both facts already and simply never join them that way; making that join is a reporting change rather than a new data capture, and it is what turns dead bed time from an argument into a tracked number.
- **Admissions desk gets a two-way live link to the Bed Management console.** When a patient with a planned admission/procedure comes to Admissions to complete formalities, Admissions cross-checks live against Bed Management for unmapped-bed availability; once a prospective admission date is confirmed, it reflects immediately in the Bed Management console for that date, with a tentative bed number already attached — closing the loop from OPD prescription (point above) through to a mapped bed, in real time rather than as a batch update. *(Scales — see §7.4's scaling note above.)*

<!--chunk
id: bed.7.4.3
title: Solution construction — key people & buy-in
summary: Whose cooperation the solution needs, that the COO approves process flows rather than runs them, and that doctors are where resistance concentrates and must be made better off.
keys: buy-in, stakeholders, COO, Head of Operations, Medical Superintendent, ICU in-charge, intensivist, billing, resistance, doctors, verbal recording, rounds, predictive summary
needs: none
see: bed.7.4.2, bed.7.4.4, dis.7.4.1, dis.7.4.3
tokens: 460
-->
#### 3. Key people & buy-in

Teams whose cooperation is required: the Discharge Team/Discharge Managers · Admissions Desk · IT · Medical Superintendent, Medical Director and their teams · OPD In-charge · ICU in-charges and Intensivists · Doctors · Billing (for the bill-close/bill-open join in §7.4.2).

**Head of Operations / COO.** Both the Bed Manager and the Discharge Manager report to this level, which makes it the level that actually authorises cross-departmental coordination between the two — and the level whose sign-off the §7.4.2 process changes need. Its role here is to **approve the process flows**, not to contribute to daily tasks: don't design the solution around COO involvement in the 2 PM/6 PM cadence or the 5 PM rounds, but don't expect the decoupling of admissions from discharges to survive without their explicit approval either.

**Where the resistance concentrates, and the buy-in strategy for it:** the Clinical Team (doctors specifically) is where the most resistance is expected, so making their working life easier — not harder — is the central design constraint, not an afterthought. Two concrete mechanisms carry that:
- Doctors record observations **verbally**, on rounds, for each patient — this single capability is critical to both Bed Management's predictive mapping *and* the Discharge automation in `discharge-process.md` §7.4.1, so it's shared, load-bearing infrastructure rather than a one-off convenience.
- On rounds, the agent hands doctors a **predictive model and summary for every patient under their care**, benchmarked against historical LOS trends for similar patients — so the doctor is reviewing an already-assembled picture rather than reconstructing it themselves, making the provisional-discharge/step-down confirmations asked of them (§7.4.2) faster to give, not an added burden.

<!--chunk
id: bed.7.4.4
title: Solution construction — team/role changes
summary: The two separate role decisions — a condition-triggered Bed Manager and volume-sized Admissions Executives — their triggers, sizing and costs, plus scope-augmentation for everyone else.
keys: Bed Manager, hiring trigger, occupancy above 80%, TAT breach, demand exceeds supply, Admissions Executive, headcount, salary cost, 4-4.5 lakhs, 3-3.5 lakhs, coverage floor, scope augmentation
needs: none
see: bed.7.1, bed.7.3, bed.7.4, bed.7.4.1, bed.7.4.3, dis.7.4.4
tokens: 1000
-->
#### 4. Team/role changes

There are **two separate role decisions** here, triggered differently and priced differently. Don't collapse them into one recommendation.

**a. The Bed Manager — condition-triggered, ₹4–4.5 lakhs/year.**
A dedicated Bed Manager owns the entire bed-scheduling process end-to-end as its single point of contact. The role is about **coordination with other departments and ownership of the whole process**, not about processing volume — which is why it is not sized per admission. It sits at the same level as the Discharge Manager in `discharge-process.md` §7.4.4: the two are peers, coordination runs between their departments, and both report to the Head of Operations / COO (§7.4.3).

Three conditions trigger the role. Any one of them is sufficient:
- **Demand exceeds supply (the pivot).** On a monthly average, daily admissions exceed the average number of beds that were available the previous night. This is the primary trigger and is deliberately not an occupancy measure — it shows directly how critical discharge efficiency and admission planning have become for this hospital.
- **Occupancy above 80%.** Any hospital above this level should ideally have a Bed Manager on board.
- **Sustained TAT breach.** Where the hospital continually overruns its expected TAT — for example, more than 50% of admissions taking longer than the expected Admission TAT — a Bed Manager is required. A breach at that rate signifies coordination failure, and coordination with the Discharge Manager and the other dependent departments is precisely what this role, and only this role, can do.

Below all three conditions, the same hire is better framed as an investment in future efficiency — and notably also as direct stress reduction for the bed management team's daily workload, not purely a financial argument. The cost-benefit case, where the conditions are met, is built on §7.4.1's net-effect lines: earlier admissions bring billing forward, remove dead bed time, allow procedures to be scheduled earlier, and pull ALOS down in conjunction with an efficient discharge process.

**b. Admissions Executives — volume-sized, ₹3–3.5 lakhs/year each.**
The bed-management team *is* the admissions desk (§7.1 point 5), so this is the processing layer, sized by volume rather than triggered by condition. Size it by running §7.1 point 5's ratio-check against this hospital's own admission peak and internal-transfer volume — one person handles up to 5 admissions per hour, with a coverage floor of 1 per shift up to 250 beds and 2 morning / 2 evening / 1 night above 250 beds — and take whichever of the two constraints fails first at peak. Do not apply the coverage floor as the answer on its own; it is a floor, and a hospital whose admissions cluster into a narrow window will breach the throughput constraint long before the floor looks inadequate.

<!--m-->*(Known gap: this section still lacks a worked example of the ratio-check actually being run — the way `discharge-process.md` §7.4.4 now carries one for the Discharge Executive threshold, taking a hospital's confirmed volume and two-window pattern through to a specific headcount and cost. The method and both constraints are now stated; what's missing is the demonstration. Expected to come out of a practice conversation.)*<!--/m-->

**c. Everything else is scope-augmentation, not headcount.**
OPD, the Medical Supervisory team, the Admissions Desk and Billing each get their existing roles slightly expanded — capturing specific events (OPD prescription details, admission confirmations, the five admission stage timestamps, the bill-close/bill-open join) and, for Medical Supervisory specifically, doing the dedicated 5 PM rounds of beds with planned or anticipated discharges/step-downs (§7.4.2).

All of the role changes already established in `discharge-process.md` §7.4.4 carry over here too, since Bed Management's automation is built directly on top of Discharge's — they aren't separate change-management efforts.

<!--chunk
id: bed.status
title: Status and change log
summary: What was settled in each section and when, including the bill-to-bill redefinition of dead bed time and the question-8 branch, and the four items still open.
keys: status, change log, approvals, revision history, dead bed time redefinition, question 8 branch, practice conversation, open items, pending sync
needs: none
see: none
tokens: 1510
retrieve: never
-->
---

**Status: Bed Management content complete and KPIs approved.** All four Chat-agent handling components (§7.1–7.4) are filled. §8's KPI list, drafted by Claude and delivered 2026-09-02, was approved by Avishek as drafted on 2026-09-09 — Bed Management's KPIs are no longer pending review, and all three department files' KPI lists (OPD-Diagnostics, Discharge Process, Bed Management) are now approved. On 2026-09-09, §3's Discharge Process dependency row, §7.1, §7.2, and §7.4.2 were updated to require verifying the hospital's actual Discharge TAT and discharge timing — not just its reported numbers — whenever a Bed Management query touches Discharge, and to require Discharge Process automation (or, at minimum, a manual process disciplined enough to replicate its logic) as part of any Bed Management solution. Also on 2026-09-09, §7.1 and §7.2's Peak-Load Staffing Method retrofit was completed, and §7.2 was restructured from a checklist into numbered pointed interrogation questions.

On 2026-09-10 the department was worked through point by point with Avishek ahead of its practice conversation, and the following were settled. §6 gained this department's signature failure mode — the single team serialising discharges then admissions, and the self-fulfilling assumption that beds won't free up early — which is also its diagnosis mechanism. §7.1 gained two new points: Admission TAT with its five-stage timestamp chain (point 4), and the bed-management/admissions team staffing ratio (point 5), the team having been confirmed as the same people who staff the admissions desk and handle internal transfers. §7.1 point 2 now states the correct definition of Discharge TAT — through to the next admission into that bed, or to the patient leaving it where it isn't reoccupied — with the >80% occupancy condition retained as when to apply it as an efficiency check. §7.2 gained three questions (8: one team or two; 9: bed-management/admissions staffing adequacy; 10: Admission TAT and its stage timings) plus matching data-access items. §7.3 went from four parameters carrying an open marker to eight settled ones, including dead bed-days as a named quantity distinct from ordinary vacancy. §7.4's scaling pivot was set as demand against supply — monthly-average daily admissions against the previous night's average available beds — replacing an occupancy breakpoint. §7.4.1 gained element (e), admission call-in timing, and the quantified net-effect block it previously lacked, with occupancy gain explicitly ruled out as a benefit line. §7.4.2 gained the decoupling of admissions from discharges and stage-timestamp capture. §7.4.3 gained the Head of Operations / COO, whose role is to approve process flows rather than contribute to daily tasks. §7.4.4 was split into two separate role decisions — the Bed Manager, condition-triggered on three conditions at ₹4–4.5 lakhs/year, and the Admissions Executives, volume-sized at ₹3–3.5 lakhs/year — replacing the previous ">80% occupancy or ~40 admissions/day" threshold.

**Also on 2026-09-10, §7.2 question 8 gained a branch for the negative answer.** Practice conversation: a 300-bed hospital answered question 8 with "one team, but both functions run together" — the opposite of §6's serialised pattern — while simultaneously reporting beds not turning over, an emergency department short of beds, and a dead bed time it recognised as longer than the case example. Its own admission clock times then showed admissions completing between 4:30 PM and 8 PM. On the file's previous wording the signature failure mode would have been ruled out by that answer and the enquiry would have moved on. Question 8 now says a claimed overlap is a claim about practice, to be tested against question 10's clock times before the failure mode is ruled out, and names the variant this conversation surfaced: a rule that beds are not allocated until confirmed physically ready, which produces the same late admissions by a different route.

**Later on 2026-09-10, dead bed time was redefined as a bill-to-bill quantity**, per Avishek's correction during the Bed Management practice conversation. The previous wording — "time a bed sits vacant, or has nothing billed against it, because of a discharge or admission delay" — allowed the quantity to be read as physical vacancy, which understates it by hours. It is now defined in §7.3 point 5 as running **from the finalisation of the outgoing patient's bill to the initiation of the incoming patient's bill**: billing on a bed stops when the final bill is closed and sent for insurance approval, typically late morning, while the patient normally remains in the bed through approval, payment, briefing and physical exit; every allied revenue line through that bed — pharmacy, diagnostics, procedures, dependent OT slots — stops at the same moment and cannot restart until the next patient's bill is opened. The measure therefore spans three parts: the discharge tail after billing closes, the housekeeping turnaround, and the admission delay. Corresponding changes: §6 gained a note that the loss does not begin at physical vacancy; §7.1 point 2 now distinguishes the TAT clock from the revenue clock; §7.2's data-access list gained bill-finalisation and bill-initiation timestamps per bed, and §7.2 gained question 11 on when billing actually stops and restarts; §7.4.1(e) and the net-effect block now describe both ends of the stretch as separately attackable; §7.4.2 gained the bill-close/bill-open join as a reporting change; and §7.4.3 and §7.4.4(c) added Billing to the cooperating teams and to scope-augmentation respectively.

Still open: the worked ratio-check example in §7.4.4(b); §8's KPI list, which Avishek has agreed to extend but which has not yet been revised (see the note at its foot); the consistency and sync items shared with `references/common-elements.md`, `SKILL.md` and `README.md`, none of which reflect the 2026-09-09 or 2026-09-10 passes; and the playbook restructure provisionally agreed for after the practice conversation.

<!--chunk
id: bed.8
title: KPIs
summary: The eighteen approved KPIs across mapping accuracy, turnaround, process adoption and finance, and the four KPI revisions agreed but not yet made, including that #16 is now wrong.
keys: KPI, metrics, mapping accuracy, LOS accuracy, emergency reserve adequacy, bed turnaround time, boarding time, occupancy, ALOS, process adoption, console sync, revenue, staffing ratio, KPI gaps
needs: none
see: common.peak-load, bed.7.1, bed.7.3, bed.7.4.1, bed.7.4.2, bed.7.4.4, dis.8
tokens: 1340
-->
## 8. KPIs <!--m-->(drafted by Claude 2026-09-02, approved by Avishek as drafted 2026-09-09)<!--/m-->

### Core bed-mapping & prediction accuracy
1. **% of planned admissions mapped to a bed by the 6 PM final freeze** — the department's core forward-looking success metric (§7.4.1).
2. **% of 2 PM provisional mappings that hold unchanged through to the 6 PM final freeze** — measures how stable/accurate the earlier prediction pass actually is, not just whether the final number looks good.
3. **% of ICU requirements unmapped at the 6 PM freeze** — tracked separately from general-bed unmapped count, since ICU shortfalls carry different clinical urgency.
4. **Predicted vs. actual LOS accuracy**, by treatment/procedure type — since the whole predictive-mapping approach in §7.4.1(a)/(b) depends on LOS trend estimates being reasonably accurate; this is the metric that validates (or exposes drift in) that underlying model.
5. **Emergency bed reserve adequacy** — how often the trend-based emergency reserve (§7.4.1(d)) was sufficient for actual same-day emergency demand vs. how often it was exceeded, checked periodically against the rolling 2–3 year trend basis it's derived from.

### Turnaround, occupancy & wait time
6. **Bed turnaround time** — physical discharge to usably-available bed (shared metric with Discharge Process — see that department's KPI #4).
7. **ER/admission wait or boarding time** — direct downstream effect per §3.
8. **Bed Occupancy** and **ICU Occupancy** (from §7.3, tracked as ongoing KPIs).
9. **ALOS** (from the shared block in `references/common-elements.md`, tracked here as it's directly affected by bed-pressure-driven discharge urgency per §3).

### Process adoption
10. **% of ward patients with a provisional discharge signal given the full 24 hours in advance** required by §7.4.2.
11. **% of ICU patients with a provisional step-down signal given by 1 PM** as required by §7.4.2.
12. **% of Medical Supervisory 5 PM rounds completed on schedule** — a direct process-discipline check on the checkpoint §7.4.2 introduces, since the 6 PM final mapping depends on this happening reliably.
13. **% of planned admissions with OPD-prescription-captured intake data available** — measures whether the OPD-as-intake-point requirement (§7.4.2) is actually being fed, since without it the planned-admission-to-bed mapping in §7.4.1(a) has nothing to map from.
14. **Admissions-desk-to-Bed-Management console sync accuracy** — how often a confirmed admission date at the Admissions desk correctly and immediately reflects in the Bed Management console with a tentative bed attached (§7.4.2's two-way live link).

### Financial & staffing
15. **Daily/aggregate Revenue attributable to bed-management efficiency** — the direct downstream effect named in §3, made explicit as a tracked KPI rather than left as a qualitative dependency.
16. **Bed Manager threshold tracking** — occupancy % and admissions/day tracked against the **>80% occupancy or ~40 admissions/day** trigger in §7.4.4, as an operational trigger metric in its own right.
17. **Housekeeping/transport staff available per shift per bed, for admissions and discharges** — the Bed-Management-specific instance of the universal Peak-Load Staffing & Manpower Cost-Benefit Method in `references/common-elements.md`.
18. **Nursing workload distribution relative to occupancy/turnover volume** — the §3 downstream dependency made explicit as a tracked metric, to catch workload imbalance before it becomes a retention or care-quality issue.

<!--m-->*(All 18 were Claude's first draft, delivered per Avishek's 2026-09-02 request alongside OPD-Diagnostics' and Discharge Process's KPI lists, and approved by Avishek as drafted on 2026-09-09 — all three departments' KPI lists are now approved.)*<!--/m-->

**KPI revision agreed but not yet made.** <!--m-->Avishek agreed on 2026-09-10 to extend this list, deferring the actual revision. <!--/m-->Four things need doing, and until they are done §8 is out of step with §7:
- **#16 is now wrong.** It tracks *"occupancy % and admissions/day"* against a *">80% occupancy or ~40 admissions/day"* trigger that §7.4.4(a) has replaced. It needs to track the three current conditions instead: monthly-average daily admissions against the previous night's average available beds, occupancy above 80%, and the proportion of admissions overrunning expected Admission TAT.
- **Admission TAT needs KPIs** — the headline figure against the sub-30-minute target, and the five stage timings in §7.1 point 4 tracked individually so coordination delay stays separable from documentation time.
- **Dead bed time needs a KPI**, defined bill to bill per §7.3 point 5 — hours from the outgoing patient's final-bill closure to the incoming patient's first billable entry on the same bed, tracked as one number and kept distinct from both ordinary vacancy and physical bed-turnaround time (#6), with its three component stretches (post-billing discharge tail, housekeeping turnaround, admission delay) separable underneath it — alongside admissions actually being completed by around 12 PM rather than in the 4–8 PM window.
- **The bed-management/admissions team ratio needs a KPI** — admissions plus internal transfers handled per team member per hour, peak vs. off-peak, per §7.1 point 5 — as the ongoing counterpart to #17's housekeeping/transport ratio.
