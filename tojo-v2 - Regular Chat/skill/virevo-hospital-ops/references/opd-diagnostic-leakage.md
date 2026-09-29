<!--chunk
id: opd.0
title: Department header & case-study grounding
summary: That this department is the Diagnostics/OPD-linked function whose baseline numbers come from the demo case study: 10%/20% redemption, Rs1.5L/day lost, 5% of EBITDA, MRI scheduling as root cause.
keys: diagnostic leakage, OPD to diagnostics conversion, case study baseline, MRI scheduling bottleneck, revenue loss, EBITDA, prescription redemption, walk-in buffer
needs: none
see: opd.1, opd.7.3, opd.8
tokens: 210
-->
# Department: OPD-to-Diagnostics Conversion (Diagnostic Leakage)
*Division: Diagnostics & Clinical Support Services (cross-linked to OPD/Clinical Care Delivery and Marketing/Referral Engine)<!--m--> · Status: content complete (§1–8, approved 2026-09-02)<!--/m-->*

Grounded in the existing Tojo demo's Problem 2 case study (`virevo-tojo-chat/references/case-studies.md`): 40 new + 400 returning OPD patients/day; only 10% of new patients and 20% of returning patients complete prescribed tests at this hospital; ₹1.5L/day revenue loss, 5% of EBITDA. Root cause per that case study: sequential MRI scheduling with no buffer for walk-in prescriptions — not patient unwillingness — plus a "revenue must come first to justify staffing" causality reversal, and no one having visibility into the whole process to plan overlapping activity.

<!--chunk
id: opd.1
title: Purpose
summary: That the department exists to make prescribed tests get completed at this hospital, same visit where possible, by removing scheduling, capacity and turnaround friction.
keys: purpose, scope, in-house diagnostics, same-visit redemption, leakage to competitor, scheduling friction, turnaround, capacity
needs: none
see: opd.0, opd.2
tokens: 90
-->
## 1. Purpose
Ensure tests and investigations prescribed during an OPD consultation actually get completed at this hospital's own diagnostic facilities — rather than leaking to a competitor or being skipped entirely — by making scheduling, capacity, and turnaround frictionless enough that redemption happens here, same visit wherever possible.

<!--chunk
id: opd.2
title: Sub-functions & core activities
summary: Which activities belong to this department, from prescription capture and cross-modality slot scheduling through redemption tracking, report turnaround, follow-up and billing coordination.
keys: sub-functions, prescription capture, slot scheduling, radiology, lab, cardiology diagnostics, endoscopy, walk-in accommodation, redemption tracking, equipment utilization, OP to IP conversion
needs: none
see: opd.1, opd.3
tokens: 210
-->
## 2. Sub-functions & core activities
OPD prescription capture (what's prescribed, by whom, for whom) · diagnostic slot scheduling across modalities (Radiology/Imaging — X-ray, CT, MRI, USG, Mammography; Lab — pathology, microbiology; Cardiology diagnostics — ECG, TMT, Echo; Endoscopy) · real-time slot availability management across all modalities · walk-in/same-day accommodation for freshly-prescribed tests, not just pre-booked appointments · prescription-to-redemption tracking, split by new vs. returning patients · report turnaround and delivery back to the prescribing doctor · follow-up/reminders for unredeemed prescriptions · capacity utilization monitoring by equipment/modality across the operating window · OP-to-IP conversion tracking tied to diagnostic findings · coordination with Billing for same-visit diagnostic charges.

<!--chunk
id: opd.3
title: Dependencies
summary: Which teams this function depends on and which depend on it, with priority, including the booking-protocol gatekeeper, per-unit imaging capacity and doctor compensation structure.
keys: upstream dependencies, downstream impact, doctor secretary booking protocol, MRI CT multi-unit capacity, doctor compensation, HR training, IT HIS slot visibility, billing, EBITDA, OP to IP conversion
needs: none
see: opd.0, opd.7.1.1, opd.7.2
tokens: 840
-->
## 3. Dependencies

### Upstream — what this needs from other teams
| Depends on | Nature of dependency | Priority |
|---|---|---|
| OPD Consultation/Doctors | Accurate, timely prescription capture | Critical |
| OPD Doctor Consultation Booking schedule & protocol | How appointments are booked and who owns the patient interaction at that moment — hospital front-office staff vs. the doctor's own secretary — and specifically whether that arrangement *allows hospital staff to step in* for diagnostics follow-up, further-consultation booking, and pharmacy handoff once the patient steps out with prescriptions in hand. This is the structural gatekeeper for the same-visit conversion moment: if a doctor's secretary controls that interaction and doesn't cede it, the conversion opportunity may be blocked before scheduling logic even applies. | Critical |
| Radiology/Imaging | Capacity & scheduling — MRI specifically is the named bottleneck in the case study | Critical |
| Radiology/Imaging — multi-unit capacity | Where a hospital runs multiple MRI/CT/Mammography units, each unit's schedule and bottleneck must be considered individually, not aggregated — a hospital-wide capacity average can mask a single overloaded unit | Critical |
| Laboratory | Capacity & turnaround | High |
| Manpower availability & salary costs (this department's own staffing) | Technologist/radiologist/lab-staff headcount and cost directly determine whether walk-in buffer capacity can exist at all — this is the resourcing side of the case study's staffing-vs-revenue causality question | Critical |
| Doctor compensation structure | Whether doctors are on fixed salary or revenue-share, and — independent of that — whether any payout is linked to diagnostics revenue specifically. Shapes incentive alignment (or conflict of interest) around prescribing and supporting conversion. | High |
| HR training protocols | Whether frontline and technical staff are trained on walk-in accommodation, cross-selling/follow-up conversations, and the scheduling protocol itself — execution quality depends on this, not just headcount | High |
| IT/HIS | Real-time slot visibility linked to the prescription itself | High |
| Front Office/Patient Services | Booking and queue execution | High |
| Billing | Same-visit billing that doesn't itself become a friction point | Medium |

### Downstream — what depends on this running well
| Affects | Nature of effect | Priority |
|---|---|---|
| Daily/OPD Revenue | Direct | Critical |
| EBITDA | Case study: 5% of EBITDA at stake | Critical |
| Break-even period on diagnostic equipment (ROI) | — | High |
| OP-to-IP Conversion | Findings drive admission decisions | High |
| Manpower availability & salary costs | Higher conversion volume changes required staffing levels and shift/cost planning for diagnostics and front-office teams — feeds back into whether added headcount is justified | Medium |
| HR training protocols | Successful conversion practices (walk-in handling, follow-up scripts, handoff etiquette) need to be captured into standard onboarding/training rather than staying tribal knowledge with whoever currently does it well | Medium |
| Bed Occupancy | Indirect, via admissions driven by findings | Medium |
| Service Excellence/Patient Experience | — | Medium |
| Marketing/Referral Engine | Repeat-visit trust | Medium |

<!--chunk
id: opd.4
title: Non-negotiables
summary: That STAT/urgent tests are never delayed for scheduling convenience and that test accuracy and prep/contrast protocol are never traded for throughput.
keys: non-negotiables, STAT tests, urgent investigations, contrast allergy, prep requirements, patient safety, throughput limits
needs: none
see: opd.5, opd.7.4.1
tokens: 50
-->
## 4. Non-negotiables
Clinically urgent/STAT tests never wait for scheduling convenience · test accuracy and protocol (contrast allergies, prep requirements) never compromised for throughput.

<!--chunk
id: opd.5
title: What can flex
summary: That non-urgent timing, the specific slot within the day, and the choice between clinically equivalent modalities are the legitimate flex levers.
keys: flexibility, same-day scheduling, slot shifting, modality substitution, non-urgent tests, capacity matching
needs: none
see: opd.4
tokens: 50
-->
## 5. What can flex
Non-urgent tests can be same-day rather than immediate · specific time-of-day slot can shift within the day · choice between clinically-equivalent modalities can flex to available capacity.

<!--chunk
id: opd.6
title: Failure modes & early warning signs
summary: Which four patterns signal leakage: no walk-in buffer slots, no prescription-to-redemption tracking, no manager-level process ownership, and reversed staffing/revenue causality.
keys: failure modes, early warning, sequential scheduling, no buffer slots, redemption tracking gap, process ownership, staffing before revenue, causality reversal
needs: none
see: opd.0, opd.7.1.1, opd.7.1.2
tokens: 120
-->
## 6. Failure modes & early warning signs
Purely sequential scheduling with no buffer slots for walk-in prescriptions (the case study's core finding) · no prescription-to-redemption tracking, so leakage stays invisible until it shows up in revenue much later · scheduling left entirely to frontline staff with no manager-level process ownership · causality backwards — assuming revenue has to come first to justify added staffing/capacity, when staffing is actually what drives the revenue.

<!--chunk
id: opd.7
title: Chat-agent handling
summary: That Tojo handling of this department is organised into four parts: subject-matter considerations, dependency verification, financial parameters, and solution construction.
keys: chat agent handling, Tojo reasoning structure, considerations, verification protocol, financial parameters, solution construction
needs: none
see: opd.7.1.1, opd.7.1.2, opd.7.2, opd.7.3, opd.7.4
tokens: 10
-->
## 7. Chat-agent handling

<!--chunk
id: opd.7.1.1
title: Subject-matter considerations — points 1-7 (first round)
summary: Which seven things must be established first: how leakage is known, why tracking is absent, floor-staff bandwidth, scheduling ownership, guest-services ratio, off-peak pricing and mobility.
keys: leakage measurement basis, prescription tracking, floor staff ratio, billing bandwidth, peak loading, scheduling ownership, STAT slots, guest services ratio, off-peak discount, PACS reports, housekeeping transport, non-ambulatory patients
needs: common.peak-load
see: opd.7.1.2, opd.3, opd.7.2, opd.7.4.1, common.solution-method
tokens: 2000
-->
### 7.1 Subject-matter considerations

These are the things Tojo needs to establish before it can reason usefully about *any* query touching OPD-to-diagnostics conversion or diagnostic leakage. Points 1–7 (first round) run roughly in the order a real diagnostic conversation would surface them — from "how do you even know this is a problem" down to specific operational bottlenecks. Points 8–14 (second round) add the underlying reasoning principles and refine a couple of the first-round points.

**1. How is the leakage figure actually known?**
First and foremost, establish whether the diagnostic-leakage claim is an *observation based on empirical/estimated calculation* — i.e. modeling expected diagnostic volume, department-by-department, by quantity and by revenue, off of OPD footfall and typical prescription rates, then comparing that estimate to actuals — or whether the hospital *actually tracks every prescription*: what was prescribed, in what quantities, mapping an estimated total revenue value of everything prescribed, and then checking that against what was finally carried out and the revenue actually collected. These are fundamentally different starting points — one is a modeled inference, the other is a measured fact — and the confidence Tojo can place in any leakage number, and the kind of solution that follows, depends on which one this hospital is working from. *(§7.2 restates this directly as a practice-verification question — has the hospital actually measured it, or just sensed it?)*

**2. If there's no prescription-tracking system, why not?**
If the hospital does not record every prescription and produce daily prescribed-vs-completed reports, find out *why*: lack of facilities to scan/capture every prescription, lack of manpower to do it, the hospital simply not deeming it important or relevant, non-cooperation from patients, doctors, or doctors' secretaries, or some other reason. The reason matters because it points to a different fix — a facilities gap is solved with capture infrastructure, a manpower gap with staffing or automation, a priority gap with making the revenue case visible, and a cooperation gap with the incentive/authority questions in points 1 and 4 of §3 upstream dependencies (doctor booking protocol, doctor compensation structure).

**3. OPD floor-staff capacity ratio (billing bandwidth check).**
Calculate the ratio of patients to floor-level OPD staff to determine whether staff actually have spare time to do anything beyond billing — such as the follow-up/handoff work that drives diagnostic conversion. Method:
- Count total OPD staff who are floor-level executives only — exclude staff assigned to diagnostic sections, and exclude managers, supervisors, guest relations/services, and other support staff.
- Assume this staff is deployed across 2 shifts (the typical minimum).
- Take total average OPD footfall: new patients + returning/old patients + diagnostic-services patients.
- Estimate total bills to be generated at a minimum of 1 per patient, more realistically ~1.25 bills per patient.
- Assume ~3–4 minutes per complete billing transaction. *(This figure is the billing mechanics alone — selecting line items, generating the bill, taking payment. It does not include the guidance/query-handling time §7.2's TAT-definition question raises; once this hospital's actual TAT is established, the ratio check should ideally be re-run against that fuller, TAT-inclusive time rather than the billing-only estimate.)*
- **Do not assume uniform/linear patient flow across the day** — most hospitals wrongly do. Instead assume peak-loading: ~80% of patients arrive crammed into a 4-hour window, with the remaining 20% spread across the rest of the operating duration.
- Combining shift headcount, hourly patient/bill volume (peak vs. off-peak), and time-per-bill gives the actual hourly time available per staff member — which tells you concretely whether that staff realistically has bandwidth, hour by hour, to do the other work needed to convert diagnostics, or whether they're fully consumed by billing alone, especially during the peak window.
- *(This is the OPD-specific instance of the universal Peak-Load Staffing & Manpower Cost-Benefit Method in `references/common-elements.md` — see that file for the general method and its two points of application.)*

**4. Diagnostic scheduling ownership and system maturity.**
For every diagnostic service/equipment, establish:
- Is there a single process owner across all units, or does each unit have its own manager focused on their own unit's convenience/comfort rather than the hospital-wide picture?
- Who actually prepares the schedule, and is scheduling done against a real system, or is it just a guideline that leaves the actual scheduling — and any override — to human judgment?
- Are emergency/STAT slots accounted for as a designed-in part of the schedule, or handled ad hoc as they arrive? *(See point 12 below, §7.2's scheduling-logic question, and §7.4's process-changes section, for the specific correct-process detail to check here.)*
- Who owns the scheduling process and the logic behind it, end to end?
- Do doctors — radiologists, cardiologists, sonologists, etc. — interfere in scheduling, and do they hold authority to override the schedule?
- Would the hospital be better served by a system automated enough that seniority alone can no longer be used to override schedules, interfere with the process, or create stumbling blocks? (This is a genuine question to explore with the hospital, not an assumed yes — see §7.4 for how it plays into the solution's people/authority dimension.)

**5. Guest services capacity ratio.**
Find out whether the hospital has guest services staff who guide patients through the hospital, help with diagnostic bookings, and see the process through to completion.
- If yes: run the same kind of ratio as point 3 — guest-service staff available per hour vs. total patients for that hour — using a peak-loading assumption of 40% of patients in the first 2 hours of the first shift, 40% in the last 2 hours of the second shift, and the balance spread across the rest of the duration. Assume 5–10 minutes per patient interaction. This tells you exactly how many patients guest services can realistically handle during peak vs. off-peak hours, and where the gap is.
- If no: this becomes a gap to size, not just note. The hospital may need to add this function. Build a sample cost-benefit: monthly cost of new/additional guest-services staff, translated against the diagnostic (and other) revenue that better guided-conversion could realistically capture.

**6. Off-peak discounted diagnostic slots.**
Check whether the hospital offers discounted rates for off-peak diagnostic slots, and whether they'd be open to introducing this if they don't. The case for it: it improves equipment utilization (fills otherwise-idle off-peak capacity), gives patients with genuine affordability constraints a way to still get tests done in-house rather than walking out, and — because the tests are then done at the hospital's own facility — reports flow directly to the treating doctor through PACS or the hospital's own reporting systems, and doctors are generally more comfortable relying on reports from trusted in-house/known colleagues than from an unknown external facility. This is both a conversion lever and a trust/quality lever, not purely a pricing one.

**7. Housekeeping/transport support for non-ambulatory patients.**
Check availability of housekeeping and transport staff during peak hours and shifts, specifically to ensure timely mobility of non-ambulatory patients between OPD and diagnostic areas — a mobility bottleneck here can silently cause missed or delayed diagnostic slots regardless of how well scheduling itself is designed. Run the same style of ratio calculation as points 3 and 5, assuming ~5% of patients require ambulatory/mobility support, against available housekeeping/transport headcount per shift.

<!--chunk
id: opd.7.1.2
title: Subject-matter considerations — points 8-14 (second round)
summary: Which principles govern the diagnosis: weakest-link resourcing, peak-hour staffing with paid redundancy, staffing-before-volume causality, STAT slot release, staff morale, low-volume exception.
keys: weakest link, bottleneck, peak hour staffing, redundancy cost, patient experience, service satisfaction, staffing causality, STAT slot release rule, IP mapped slots, junior staff training, morale, appreciation not incentive, low volume hospital, patient diversion
needs: opd.7.1.1
see: opd.7.2, opd.7.4.1, common.peak-load
tokens: 1430
-->
#### Points 8–14 (second round)

**8. Revenue is a function of the weakest link, not just of prescriptions.**
Revenue depends not only on what's prescribed but on whether every function required to deliver it has adequate resourcing — front office, diagnostic clinical teams, and equipment alike. The entire process is bottlenecked by whichever single link is weakest, even if every other link is adequately staffed/equipped. Check every parameter as an average against actual resource availability — manpower, time, and equipment alike — rather than assuming one well-resourced function compensates for another.

**9. Peak-hour planning, not daily averages — and the redundancy trade-off.**
Assuming linear, uniform patient flow across the day is the single worst planning mistake a hospital can make. Staffing has to be planned against peak-hour estimation, with adequate headcount for those windows specifically — which will create visible redundancy during lean/off-peak periods. That redundancy is a real cost, but it is comfortably offset by the additional revenue potential the peak-hour adequacy unlocks. This comparison — redundancy cost vs. peak-capture revenue — needs to be shown explicitly, not asserted. *(This is now the confirmed universal Peak-Load Staffing principle in `references/common-elements.md` — points 3, 5, and 7 above are its OPD-specific applications.)*

**10. Patient experience/service-satisfaction is a real, if intangible, revenue driver.**
In OPD specifically, the final decision a patient makes is shaped by more than diagnosis and price — service satisfaction and convenience matter heavily. Being seen on time and made to feel attended-to are intangible factors, but they are directly driven by adequate manpower and even by visible redundancy (staff not visibly rushed or overloaded) — not something separate from the staffing question above.

**11. The correct causality: staffing enables volume, not the reverse.**
Most managers and decision-makers get this backwards — they wait for workload/volume to visibly increase before adding manpower. The actual causal direction runs the other way: volumes only increase once staffing is already ahead of what current averages dictate, because that's what creates the spare capacity to absorb and convert additional demand. *(Confirmed now across three departments — Discharge, Bed Management, and OPD-Diagnostics — and promoted to `references/common-elements.md` as a universal principle. §7.2's staffing-pivot-point question checks whether a hospital has ever formalized this or decides ad hoc, i.e. only after wait-time complaints — itself an instance of the same backwards causality.)*

**12. Scheduling protocol detail — STAT slots and IP-mapped slots.**
Refines point 4 above: check specifically whether the hospital's scheduling protocol keeps intermediate slots deliberately vacant for STAT/emergency needs, with a defined release rule — if a STAT slot goes unused, it should hand over automatically to the next OP patient in queue, while any slot already mapped to an inpatient (IP) stays fixed regardless. Establish whether the hospital actually follows a defined process like this, or whether slot handling is entirely ad hoc. Also revisit whether seniority-based override or secretary non-cooperation (per point 4 and per §3's booking-protocol dependency) is actually interfering with this specific mechanism. *(§7.2 draws a further distinction<!--m--> worth watching for<!--/m-->: some hospitals handle STAT not by releasing an unused vacant slot, but by directly pushing down/bumping an already-scheduled patient — a more disruptive variant of ad hoc handling, and a different failure mode than simply having no logic at all.)*

**13. The juniormost staff carry the department's revenue and success — training and morale matter as much as headcount.**
The entire revenue outcome of OPD-and-Diagnostics ultimately rests on the juniormost staff in the hospital. If the department is understaffed or only just adequate in a high-volume hospital, that staff will be overworked — and an overworked employee is not in the frame of mind needed to upsell, which is exactly what diagnostic conversion requires. This has two components: headcount adequacy (per points 9/11 above), and training — who actually trains this staff (HR, or their direct managers?), and who monitors that the training is happening and effective. Note: a formal, explicit incentive scheme to reward upselling is *not* recommended — but an informal institutional-appreciation mechanism (recognizing/fast-tracking better-performing staff monthly, giving them a visible sense of growing within the organization) is a reasonable middle ground worth exploring. *(This appreciation mechanism becomes a concrete process in §7.4's process-changes section: the daily best-performer information share. §7.2's blame-culture question checks for the opposite dynamic — whether this same juniormost staff is instead being scapegoated for delays and dissatisfaction that are actually structural.)*

**14. This all assumes a high-volume hospital — the low-volume case is different.**
Everything above (points 9, 11, 13 especially) assumes a high-volume hospital where demand is straining capacity. For a lower-volume hospital — where staffing is actually adequate or more than adequate relative to footfall, whether because footfall is genuinely low or because the hospital is newer and yet to ramp up — if diagnostic leakage is still noticed and quantified, the diagnosis has to shift: look at staff training gaps, or other underlying causes such as intentional diversion of patients elsewhere by doctors, their secretaries, or even hospital staff themselves.

<!--chunk
id: opd.7.2
title: Dependency verification protocol
summary: Which data access and which fourteen direct questions verify a hospital actual practice, forcing a primary-cause selection and exposing TAT, scheduling-logic, incentive and blame-culture gaps.
keys: verification questions, data access, department-wise billing, staff roster HR cost, primary cause, manpower versus process, OP versus IP EBITDA, doctor employment type, secretary cooperation, scheduling logic, bump versus vacant slot, automation maturity, TAT definition, staffing pivot point, blame culture
needs: none
see: opd.3, opd.7.1.1, opd.7.1.2, opd.7.3, opd.7.4.1, opd.7.4.3
tokens: 2060
-->
### 7.2 Dependency verification protocol

**Data/system access required**, to verify how this hospital's actual practice compares against the §3 baseline dependencies and the §7.1 considerations above:
- **Entire OPD billing details, by department** — Consultation, Basic Radiology, Radiology, Cardio Diagnostics, Sonology, Dermatology, Pathology, etc. — broken out individually rather than as one aggregate OPD revenue figure, since the weakest-link principle (§7.1 point 8) requires seeing each department's numbers separately, not a blended average that could hide a single underperforming modality.
- **OPD staff roster and HR costs** — to run the manpower/peak-load ratio checks in §7.1 (points 3, 5, 7, 9, 11, 13) and feed the cost-benefit comparisons those checks require.
- **Scheduling systems and ownership of the scheduling protocol** — to verify §7.1 points 4 and 12, and §3's scheduling-related dependencies, directly against the actual system rather than a described-but-unverified process.

**Practice-verification questions to put to the hospital directly**, once the data picture above is in hand — these are designed to force a specific, defensible answer rather than let the hospital settle on a vague or comfortable one:

1. **Force a primary-cause selection.** Ask directly: is this a manpower issue, a process issue, a scheduling issue, or a corruption/diversion-related issue? It may genuinely be a combination of all four — but push for which one is the *primary* driver. This selection is what determines where §7.4's solution construction should place its emphasis first, rather than trying to fix all four with equal weight.
2. **If manpower is selected as primary, push one level deeper.** Is the actual shortfall at the manager level, or at the floor-level-executive level? These point to different fixes — a manager-level gap is a supervision/ownership problem (per §7.1 point 4's process-ownership question), while a floor-level gap is a headcount/ratio problem (per §7.1 points 3, 5, 7, 9, 11).
3. **Surface the volume-inversion mismatch directly.** OPD footfall is typically far greater than IPD's, and yet the bulk of that higher-volume workload — which per §7.1 point 8 and §7.3 point 5 is also where the weakest link actually sits — is handled by the juniormost, busiest staff in the hospital, while managers are comparatively far less loaded. Put this observation to the hospital plainly and ask where they think the problem truly lies — this is designed to make the seniority/resourcing misallocation visible rather than letting it stay an unexamined assumption.
4. **Press the financial-expertise mismatch.** Ask directly: what is the EBITDA of OP services compared to IP services? If OP EBITDA is disproportionately high, put the follow-up question to the hospital directly — purely from a financial standpoint, doesn't a function generating that much EBITDA warrant *more* expertise and seniority applied to it, not less? This uses §7.3 point 5's financial parameter as leverage in the actual conversation, not just as a number to report.
5. **Doctor employment type.** Are OPD doctors full-time or part-time (or a mix)? Part-time doctors specifically may carry competing interests — an outside practice or referral relationships elsewhere — that make it more likely tests get directed away from this hospital. This sits alongside, but is distinct from, §3's doctor-compensation-structure dependency: employment type and pay structure are two separate incentive questions, both worth checking.
6. **Doctor and secretary cooperativeness — a direct temperature check.** Beyond the structural incentive questions above (employment type, compensation structure, booking-protocol control per §3), directly assess how cooperative doctors and their secretaries are actually likely to be. This is a practical read on how much resistance to expect before proposing any scheduling or handoff change that depends on their cooperation (see §7.4's key-people-and-buy-in section).
7. **Scheduling logic — verified in detail, including which failure variant.** Does diagnostic scheduling follow any preset logic, or is it ad hoc, first-come-first-served? Specifically: does it account for emergency slots at all, and if a STAT test needs to be slotted in, does the hospital push down/bump the next already-scheduled patient — a more disruptive practice — rather than releasing a slot that was deliberately held vacant and went unused (the correct mechanism per §7.1 point 12 and §7.4's process item 3)? Distinguishing which of these is actually happening matters: both are failure modes relative to the recommended process, but they have different patient-experience severity and different fixes.
8. **Automation history.** Has the hospital tried any level of automation already — whether in software for writing prescriptions, scanning prescriptions, or the scheduling process itself? This establishes the hospital's actual automation-maturity baseline before proposing §7.4's bot-based solutions, so the pitch starts from where they already are rather than assuming a blank slate.
9. **Has diagnostic leakage actually been measured, or just sensed?** A direct, practical version of §7.1 point 1's measurement-basis question: has the hospital ever quantified diagnostic leakage, or do they just have a general sense that it's happening without having put a number to it?
10. **Guest relations services — existence check.** Does the hospital have guest relations/guest services at all? This is the direct practice-verification counterpart to §7.1 point 5's capacity-ratio calculation — confirm existence first, then run the same footfall-vs-staff-availability, peak-hour ratio method on whatever is (or isn't) there.
11. **Has the hospital ever theoretically tested peak-hour staffing adequacy against its own TAT?** Specifically: has anyone at the hospital actually checked whether staffing during peak hours is enough to keep patient wait times — for billing or other services — within whatever turnaround time (TAT) the hospital has set for itself? This is asking whether the hospital has done any version of §7.1 points 3/9's ratio-check method on its own, prior to Tojo doing it for them.
12. **Does the hospital even have a TAT defined — and is it realistic?** A TAT calculation has to account for the *entire* transaction, not just the mechanical billing step: selecting line items that may span 5 different tests across 5 different departments, generating the bill, taking payment, **and then actually guiding the patient** — explaining what needs to be done next, how long it will take, and addressing at least one follow-up query — before handing the patient over to Guest Services. At most hospitals, staff completes the bill and payment and simply points the patient toward the next station, treating that as the end of the transaction; a properly defined TAT does not stop there. Where a hospital's TAT is undefined, or is defined but only measures the billing mechanics, this is a gap to name explicitly — and it's the reason §7.1 point 3's 3–4-minutes-per-bill figure is flagged there as billing-mechanics-only, not TAT-inclusive.
13. **Staffing-pivot-point / revenue-to-staff ratio check.** Does the hospital have a defined way of knowing, for each department or discipline, at what level of daily patients/bills it needs to add staff — i.e. actual revenue-to-staff ratios that identify the pivot point — or do they decide ad hoc, only once wait-time complaints have already gotten bad? The ad hoc version is itself an instance of §7.1 point 11's backwards causality (waiting for the problem to become visible before adding capacity, rather than staffing ahead of it).
14. **Culture-of-blame check.** Does the hospital have a culture of blaming floor-level executives for all delays and patient dissatisfaction — specifically dissatisfaction rooted in service-level professionalism or delays, not dissatisfaction on medical grounds? This matters directly for §7.1 point 13: a blame culture actively undermines the morale and training investment that point argues is just as important as headcount, and any people-and-buy-in strategy in §7.4 needs to reckon with it if it's present.

<!--chunk
id: opd.7.3
title: Financial parameters to check
summary: Which five financial figures anchor the case: OPD revenue at doctor granularity, split HR costs, quantified leakage, per-unit equipment utilization, and OPD share of revenue and EBITDA.
keys: financial parameters, OPD revenue by doctor, HR cost split, guest services cost, housekeeping cost, leakage quantified, unredeemed prescription value, equipment utilization, EBITDA contribution, cost benefit anchor
needs: none
see: opd.0, opd.3, opd.7.1.1, opd.7.1.2, opd.7.2, opd.7.4
tokens: 500
-->
### 7.3 Financial parameters to check

1. **OPD Revenue** — broken out by department, and further by clinical discipline/specialty (Ortho, Neuro, etc.), and further still by individual doctor within that discipline. This granularity matters directly for §7.1 point 8 (the weakest-link principle) and for spotting whether leakage or under-conversion concentrates around a specific discipline or specific doctor, rather than being a uniform hospital-wide problem.
2. **HR Costs for OPD** — broken out by Billing & Floor Team, Guest Services, and Housekeeping specifically (not one blended OPD manpower-cost line). This is what feeds the peak-load ratio cost-benefit checks in §7.1 (points 3, 5, 7) and §7.2 — each function's ratio check needs its own cost figure to run a real cost-benefit against.
3. **Diagnostic Leakage itself, quantified** — percentage of prescriptions not redeemed, the quantity of tests not completed, and the revenue anticipated from those unredeemed prescriptions. This is the core measured (or estimated — per §7.1 point 1) quantity the whole department exists to close.
4. **Equipment Utilization** — daily utilization numbers per piece of equipment/modality, broken down further by which specialties and which doctors account for how much of that utilization. Feeds directly into §3's multi-unit-capacity dependency (each MRI/CT/Mammography unit needs its own utilization picture) and into identifying whether a bottleneck is equipment-wide or concentrated in specific referral patterns.
5. **Overall OPD contribution to hospital Revenue and EBITDA, and the leaked revenue's contribution to overall Revenue and EBITDA specifically** — i.e. not just what OPD contributes in aggregate, but what share of *that* contribution is currently being lost to leakage. This is the figure that ultimately anchors the cost-benefit case in §7.4 — the case study's "5% of EBITDA" framing is exactly this parameter. *(Also directly used as the leverage point in §7.2's OP-vs-IP EBITDA verification question.)*

<!--chunk
id: opd.7.4
title: Solution construction method
summary: That for this department the four aspects are reasoned process-and-manpower first, then automation, people, roles, and that every capability must be offered manually as well as automated.
keys: solution construction, sequencing, process before automation, four aspects, offline manual path, automated path, system design, client may decline automation
needs: none
see: opd.7.4.1, opd.7.4.2, opd.7.4.3, opd.7.4.4, common.solution-method
tokens: 380
-->
### 7.4 Solution construction method

**Sequencing note (department-specific):** the four required aspects from `references/common-elements.md` (automation, process changes, key people & buy-in, team/role changes) are still all required here, but for OPD-Diagnostics specifically the reasoning order is different from the default: **process & manpower first, then automation, then key people & buy-in, and finally team/role changes.** The logic is that the process and manpower picture has to be right (or at least defined) before automation is layered on top of it — automation here is explicitly framed as accelerating/executing an already-correct process, not a substitute for getting the process right. This is a department-specific sequencing choice, not (yet) a change to the universal default order in `common-elements.md`.

**Standing requirement — offline and automated paths, both required:** for every capability below, Tojo must be able to present both an *offline/manual* version of the solution and the *automated* version — including the underlying logic and system design for the manual version — because a client may choose not to adopt the automation. The automation is an accelerant and error-reducer on top of a correct manual process, not the only way the process can work. *(This requirement is currently department-specific to OPD-Diagnostics; it is a strong candidate for promotion to `references/common-elements.md` as a universal requirement on Tojo's solution-construction behavior more broadly.)*

<!--chunk
id: opd.7.4.1
title: Solution construction — process changes & manpower
summary: Which four process changes are proposed: formal prescription scanning and recording, guest-services handholding, vacant-STAT-slot pre-pone scheduling, and a daily no-judgement performance share.
keys: process changes, manpower, prescription scanning, prescription recording, ERP item value, guest services handholding, logic-driven scheduling, STAT slot pre-pone, daily performance sharing, best performer, information only
needs: opd.7.4
see: opd.7.4.2, opd.7.1.1, opd.7.1.2, opd.7.2, common.solution-method
tokens: 650
-->
#### Process changes & manpower (reasoned first for this department)

1. **Prescription recording must be initiated as a formal process.** Every prescription gets scanned — this scanning step is manual regardless of automation level (a human has to physically scan it). What can vary is the next step, reading and recording the scan's content: for investigations/procedures specifically (this department's scope), or, more broadly, the entire prescription mapped against symptoms, diagnosis, treatment, and advice. This reading/recording step can be done manually, **or** a bot can now do it — reading the scanned prescription, categorizing it by multiple parameters, and calculating the total value of the prescription (split by OPD and IP services) by pulling per-item values from the ERP. *(This is the manual/automated pair for automation item 5 below.)*
2. **Guest-services handholding must be introduced, or re-audited if it already exists.** Ties directly to §7.1 point 5's capacity ratio check and §7.2's existence-check question — if the function exists, its adequacy needs re-verification; if it doesn't, this is where the decision to introduce it gets made as a process matter before it becomes a staffing/automation question.
3. **Scheduling must move from ad hoc to logic-driven, automated where warranted.** Specifically: intermediate slots are kept deliberately vacant for STAT/emergency needs; when that slot's time actually comes up and no emergency case has arrived to claim it, the next scheduled OP patient is pre-poned into that slot rather than leaving it idle. *(This is the precise mechanic behind §7.1 points 4 and 12, and the correct-process benchmark for §7.2's scheduling-logic verification question — including its warning against the more disruptive push-down/bump variant.)*
4. **A new daily best-performer information-sharing process.** Share, by department (for staff), by specialty, and by doctor, the previous day's performance — read from the value of prescriptions issued and the actual revenue booked against those prescriptions. Critically: this is shared as *information only*, with no framing of who did well or badly. The intent isn't to instruct anyone to compete — competitiveness is human nature and will emerge on its own once everyone can see where they stand relative to others. *(This is the concrete process implementing the institutional-appreciation idea in §7.1 point 13, and a direct counter to the blame-culture dynamic §7.2 checks for — recognition instead of scapegoating. Also automatable, by the same bot as item 1/5 — see automation item 6.)*

<!--chunk
id: opd.7.4.2
title: Solution construction — automation
summary: Which four bots automate the process items: prescription-reading and value tracking, performance distribution, scheduling execution, and a patient-facing virtual guest-service companion.
keys: automation, prescription reading bot, lost revenue tracking, performance sharing bot, scheduling bot, patient app, wait time notification, housekeeping call, parking attendant, virtual guest service
needs: opd.7.4, opd.7.4.1
see: opd.7.2, common.solution-method
tokens: 360
-->
#### Automation

5. **Prescription-reading bot** — reads the scanned prescription, calculates its value, and tracks lost revenue (unredeemed value) over time. Automated counterpart to process item 1.
6. **Performance-sharing bot** — generates and distributes the previous day's performance information (by department/specialty/doctor) automatically. Automated counterpart to process item 4.
7. **Automated scheduling bot** — manages scheduling directly from prescriptions already read in real time by item 5's bot, once confirmed by staff; executes the STAT-slot-vacant/pre-pone-next-patient logic in process item 3 without needing a human to manually re-sequence the schedule each time.
8. **Patient-facing virtual guest-service bot** — acts as a virtual Guest Service presence for the patient's entire duration on hospital premises: informs the patient of wait times and queue sequence, reminds them when their slot comes up, lets the patient call for staff help directly through the bot/app, calls for housekeeping based on the patient's tracked movement through the various stations of their OPD visit, and — at the end of the visit — can even notify the parking attendant to bring the patient's car around to the mount/dismount area in front of the hospital or OPD section. This is the automated extension of (not a replacement for, per the standing offline-path requirement above) the human guest-services function in process item 2.

<!--chunk
id: opd.7.4.3
title: Solution construction — key people & buy-in
summary: Whose cooperation the solution needs, from floor executives and a >200-footfall Scheduling Manager to doctors, secretaries, diagnostic specialists, HR, IT and executive sign-off on dashboards.
keys: key people, buy-in, floor level executives, scheduling manager threshold, 200 OPD footfall, doctor buy-in, secretary resistance, radiologist override, HR staffing adequacy, IT integration, CEO CFO COO, dashboard transparency
needs: opd.7.4.1
see: opd.7.4, opd.7.4.4, opd.7.1.2, opd.7.2, bed.7.4, dis.7.4
tokens: 560
-->
#### Key people & buy-in

9. **All floor-level executives** are key to this entire process — they're the ones actually executing the prescription-capture, billing, and follow-up work day to day.
10. **A Scheduling Manager threshold.** For a hospital with **more than 200 daily OPD patient footfall (excluding accompanying relatives)**, a dedicated Scheduling Manager should be considered — at that volume, enough prescriptions get generated that scheduling becomes a genuinely critical function in its own right, not something that can be left as a side responsibility. *(This is a new-role recommendation — carried into Team/role changes below, since it follows the same threshold-based-recruitment shape already established for Discharge Executive and Bed Manager, though note the metric here is OPD footfall specifically, not occupancy or a per-day-handled figure like the other two roles.)*
11. **Doctors and their secretaries' buy-in.** Genuinely important, and especially sensitive where there's a possibility that doctors or secretaries have any incentive — financial or otherwise — to send tests to outside agencies instead of keeping them in-house. Ties directly to §3's doctor-compensation-structure dependency and §7.1 points 2 and 12, and to §7.2's doctor-employment-type and cooperativeness questions.
12. **Buy-in from radiologists, cardiologists, pathologists, sonologists, etc.** — specifically so they understand the (now logic-driven) scheduling process and don't try to influence or override it. Ties directly to §7.1 point 4's question about doctor authority over scheduling.
13. **HR** — needs to check staffing adequacy, and the effectiveness of the training currently being given (per §7.1 point 13's training-ownership question).
14. **IT** — for all the automations and integrations (prescription-reading bot, scheduling bot, patient-facing bot, ERP value extraction).
15. **Executive Management (CEO, CFO, COO, etc.)** — buy-in specifically to agree to sharing the performance dashboards from process item 4 openly with everyone, so the intrinsic competitive effect described there can actually take hold. Without this level's sign-off, the transparency the whole mechanism depends on doesn't happen.

<!--chunk
id: opd.7.4.4
title: Solution construction — team/role changes
summary: That the only clear new recruitment is a Scheduling Manager above 200 daily OPD footfall, with guest-services headcount sized by ratio check and all other named roles being existing ones.
keys: team changes, role changes, new recruitment, scheduling manager, cost figure pending, discharge executive, bed manager, guest services headcount, peak load ratio, existing roles, status closeout
needs: opd.7.4.1, opd.7.4.3
see: opd.7.4, opd.7.1.1, bed.7.4, dis.7.4, common.peak-load
tokens: 300
-->
#### Team/role changes

The clear new-recruitment case here is the **Scheduling Manager** from point 10 above: for hospitals crossing **>200 daily OPD footfall (excluding relatives)**, this role becomes justified by the sheer volume of prescriptions requiring active scheduling logic, not left as a secondary duty for existing staff. *(Cost figure not yet given for this role — unlike the ~₹3–3.5 lakhs/year quoted for the Discharge Executive and Bed Manager roles — to be confirmed. Also note: unlike those two roles' occupancy/volume-handled thresholds, this one is anchored to OPD footfall specifically, since scheduling load here scales with prescriptions generated, not beds or discharges.)*

Beyond that, the guest-services staffing decision from process item 2 may itself require new headcount if the function doesn't currently exist — sized using the same peak-load ratio-check method as §7.1 point 5, per the universal method in `references/common-elements.md`. All other roles listed under Key people & buy-in (floor executives, HR, IT, doctors, diagnostic specialists, executive management) are existing roles being engaged for cooperation and scope, not new recruitment.

<!--chunk
id: opd.status
title: Status note (maintainer changelog — not retrievable)
summary: That the department was signed off as content complete with all eight sections filled and approved; a maintainer changelog carrying no operational content.
keys: status note, changelog, content complete, sign-off, approval record, maintainer metadata, not for retrieval
needs: none
see: none
tokens: 60
retrieve: never
-->
---

**Status: OPD-to-Diagnostics Conversion (Diagnostic Leakage) content complete.** §1–8 all filled and approved (§8 approved by Avishek 2026-09-02 without changes to Claude's draft). This department is fully closed out.

<!--chunk
id: opd.8
title: KPIs
summary: Which eighteen metrics track the department across four groups: leakage and conversion, scheduling and capacity, staffing/TAT/service, and staffing decisions and adoption.
keys: KPIs, redemption rate, new versus returning, revenue leakage, same-visit conversion, walk-in accommodation, STAT slot compliance, equipment utilization, off-peak uptake, report turnaround, staff ratio, TAT compliance, guest services coverage, patient satisfaction, scheduling manager threshold, revenue to staff ratio, training effectiveness, information share adherence
needs: none
see: opd.0, opd.7.1.1, opd.7.1.2, opd.7.2, opd.7.3, opd.7.4.1
tokens: 1150
-->
## 8. KPIs<!--m--> (approved 2026-09-02)<!--/m-->

### Core leakage & conversion
1. **Prescription redemption rate** — % of prescribed tests actually completed at this hospital's own facility, tracked separately for new vs. returning patients (per the case study's own 10%/20% split — the two populations behave differently and should never be blended into one number).
2. **Revenue leakage, in ₹/day and as % of OPD EBITDA** — the direct financial expression of (1), tying straight back to §7.3 points 3 and 5.
3. **Redemption rate by department/modality** (Radiology, Lab, Cardiology diagnostics, Endoscopy, etc.) and **by specialty and by doctor** — per §7.1 point 8's weakest-link principle, a single blended hospital-wide rate can hide where the actual problem concentrates.
4. **Same-visit conversion rate** — % of prescriptions redeemed on the same day as the OPD consultation, vs. redeemed later, vs. not redeemed at all — distinguishes a scheduling/capacity problem (same-visit conversion low, eventual redemption acceptable) from a genuine leakage problem (redeemed elsewhere or not at all).

### Scheduling & capacity
5. **Walk-in/same-day accommodation rate** — % of freshly-prescribed tests successfully slotted in without the patient being turned away or told to come back another day.
6. **STAT-slot mechanism compliance** — % of STAT/emergency needs handled via the correct vacant-slot-release mechanism (§7.1 point 12 / §7.4 process item 3) vs. the more disruptive bump/push-down variant (§7.2 point 7) vs. fully ad hoc handling — a direct read on scheduling-process maturity.
7. **Equipment utilization %, by modality and by individual unit** (not aggregated across multiple MRI/CT/Mammography units — per §3's multi-unit dependency) — both overall and split by peak vs. off-peak windows.
8. **Off-peak slot utilization %** specifically, and uptake rate of any off-peak discounted pricing (§7.1 point 6) — measures whether the off-peak lever is actually being used, not just offered.
9. **Report turnaround time** — from test completion to report delivered to the prescribing doctor, since a slow report loop discourages doctors from trusting/using in-house diagnostics for future prescriptions (§7.1 point 6's trust argument).

### Staffing, TAT & service
10. **OPD floor-staff patient/bill ratio, peak vs. off-peak** — actual hourly bandwidth per staff member against the §7.1 point 3 method, tracked over time rather than calculated once — this is the ongoing operating version of that one-time diagnostic ratio check.
11. **TAT compliance rate** — % of billing/service transactions completed within the hospital's defined TAT, **once that TAT is properly defined as inclusive of guidance/query-handling time** (§7.2 point 12) — not measured against billing-mechanics time alone.
12. **Guest-services coverage ratio** — patients actually handled per guest-services staff member per hour, peak vs. off-peak, against the §7.1 point 5 method; tracked as an ongoing metric once the function exists.
13. **Non-ambulatory mobility support responsiveness** — average wait time for housekeeping/transport support for patients needing mobility assistance between OPD and diagnostic areas (§7.1 point 7).
14. **Patient satisfaction score, isolated to service/professionalism/wait-time factors specifically** — deliberately separated from clinical/medical satisfaction, per §7.1 point 10 and §7.2 point 14's blame-culture distinction, so this metric can't be diluted or excused by unrelated clinical outcomes.

### Staffing decisions & adoption
15. **Scheduling Manager threshold tracking** — daily OPD footfall (excluding relatives) tracked against the >200/day trigger in §7.4, as an operational trigger metric in its own right, the same way Discharge Executive and Bed Manager thresholds are tracked in their departments.
16. **Revenue-to-staff ratio, by department/discipline** — the hospital's own defined staffing pivot-points (§7.2 point 13), tracked over time to confirm staffing decisions are being made ahead of demand rather than reactively.
17. **Training completion & effectiveness** — % of floor staff who've completed defined training (§7.1 point 13 / §7.2 point 8's training-ownership question), and a proxy effectiveness measure such as conversion-rate difference between trained and newly-onboarded-but-not-yet-trained staff.
18. **Best-performer information-share cadence adherence** — % of days the daily performance-sharing process (§7.4 process item 4) actually ran, as a simple process-discipline check on whether this mechanism is being kept up or has quietly lapsed.
