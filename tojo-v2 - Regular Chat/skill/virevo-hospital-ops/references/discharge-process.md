# Department: Discharge Process
*Division: Patient Flow & Hospital Operations <!--m-->· Status: content complete (§1–8; KPIs drafted by Claude 2026-09-02, approved by Avishek as drafted 2026-09-09; Peak-Load Staffing retrofit into §7.1/§7.2 completed 2026-09-09; TAT-authenticity verification questions and Bed-Management-linkage added to §7.2/§7.4 2026-09-09; TAT definition, shared-team verification question and role-taxonomy split 2026-09-10; revenue-clock note added to §7.2 q15 2026-09-10)<!--/m-->*

<!--chunk
id: dis.1
title: Purpose
summary: Discharge owns everything from the clinical decision to the bed becoming available again as one coordinated process, not a chain of departmental handoffs.
keys: discharge scope, discharge definition, bed release, clinical sign-off, billing closure, insurance clearance, family logistics, end-to-end ownership
needs: none
see: none
tokens: 80
-->
## 1. Purpose
Manage everything from the clinical discharge decision to the patient physically leaving the bed and that bed becoming available again — clinical sign-off, billing closure, insurance clearance, and family/logistics — as one coordinated process rather than a chain of separate departmental handoffs.

<!--chunk
id: dis.2
title: Sub-functions & core activities
summary: The activities a discharge is made of, from early flagging and the doctor's order through billing, insurance, pharmacy returns, briefing, payment, bed turnover and transport out.
keys: discharge planning, early flagging, discharge summary, nursing stock-take, billing finalization, TPA documents, pharmacy returns, family briefing, bed turnover, patient transport
needs: none
see: none
tokens: 130
-->
## 2. Sub-functions & core activities
Discharge planning / early flagging of likely-discharge patients · doctor's discharge order and discharge summary · nursing stock-take of medicines/consumables · billing finalization of investigations and billable items · insurance/TPA document compilation, submission and approval · pharmacy returns processing · family/patient briefing (diet, medication, follow-up) · final payment collection and clearance · bed turnover handoff to housekeeping · physical discharge and transport out.

<!--chunk
id: dis.3
title: Dependencies
summary: Which six upstream teams Discharge needs work from and which eight downstream metrics degrade when discharge runs slowly, each with a priority rating.
keys: upstream dependency, downstream impact, nursing, doctors, billing, housekeeping, transport, ALOS, ARPOB, OT scheduling
needs: none
see: dis.7.2.1
tokens: 430
-->
## 3. Dependencies

### Upstream — what Discharge needs from other teams
| Depends on | Nature of dependency | Priority |
|---|---|---|
| Nursing Team | Practices and schedules — stock reconciliation, ward readiness | High |
| Doctor Team (incl. transcriptionist) | Practices and schedules — the discharge order and summary originate here; see practice-pattern questions in §7.2 | Critical |
| Billing Team | Sign-off on chargeables, reconciliation, handoff to insurance | High |
| Dietitian Team | Diet-related briefing/instructions before discharge | Medium |
| Housekeeping Team | A discharge is not *fully* complete until the vacated bed is prepared again for the next admission | High |
| Transport Team | Wheelchair/stretcher availability to move the patient out to their vehicle or ambulance | Medium-High |

### Downstream — what depends on Discharge running well
| Affects | Nature of effect | Priority |
|---|---|---|
| ALOS | Direct driver — avoidable discharge time is added stay | Critical |
| ARPOB | Faster, cleaner discharge protects realized revenue per bed | High |
| ICU Step-Down Protocol & ICU bed availability | Ward discharge speed gates how fast ICU can step down patients | Critical |
| Bed Availability for Admission | Direct gate on next admission, including ER | Critical |
| OT Scheduling | Same-night OT slots become plannable if enough admissions land before 10 AM (esp. non-insurance patients) | High |
| OT Utilisation | Late-night OT slots for same-morning admissions depend on this | High |
| OT Revenue | Follows from OT scheduling/utilisation above | High |
| Daily Revenue | Aggregate effect of all of the above | Critical |

<!--m-->*(Draft ratings — flag any that should move.)*<!--/m-->

<!--chunk
id: dis.4
title: Non-negotiables
summary: Clinical accuracy of the summary, billing correctness, and delivery of safety and medication instructions are never traded away for discharge speed.
keys: non-negotiable, clinical accuracy, discharge summary quality, billing errors, patient safety, medication instructions, family briefing, speed tradeoff
needs: none
see: none
tokens: 60
-->
## 4. Non-negotiables
Clinical accuracy of the discharge summary is never sacrificed for speed · no billing errors introduced by rushing · patient/family safety and medication instructions always delivered before physical discharge.

<!--chunk
id: dis.5
title: What can flex
summary: Stock-take and billing prep may run in parallel, family briefing timing can shift, and non-critical documentation may trail the physical discharge by a short window.
keys: flexibility, parallel processing, sequencing, stock-take, billing prep, family briefing timing, documentation lag
needs: none
see: none
tokens: 70
-->
## 5. What can flex
The exact sequencing of stock-take vs. billing prep can run in parallel rather than strict order · family briefing timing can flex somewhat if everything else is ready · non-critical documentation can trail the actual discharge by a short window.

<!--chunk
id: dis.6
title: Failure modes & early warning signs
summary: Sequential processing, manual handoffs, no predictive flagging and no single owner are the default failures, plus a shared discharge/admissions team that pushes admissions into 4–8 PM.
keys: failure mode, serialised shared team, discharge and admissions team, manual handoff, no single owner, predictive flagging, late admissions, billable hours, ALOS
needs: none
see: dis.7.2.1, bed.6
tokens: 280
-->
## 6. Failure modes & early warning signs
Default failure mode is sequential, non-overlapping processing across teams (nothing starts until the previous step fully finishes) · manual handoffs losing time at every stage · no predictive flagging, so nothing starts until the doctor's order actually lands · no single owner, so delays get attributed to "the process" rather than a stage anyone is accountable for.

**The serialised shared team.** Hospitals commonly run one team as both the discharge team and the admissions desk. That team works discharges through the morning until roughly 12–2 PM and only then turns to admissions — so admissions get scheduled late, on the assumption that beds won't free up early enough to call patients in sooner. From the Discharge side this looks like adequate morning focus; what it actually does is push the hospital's admissions into a 4–8 PM window, costing billable hours, ALOS and OT scheduling. It is the same failure mode described in `bed-management.md` §6, seen from the other end, and it is why §7.2 question 16 asks whether the two functions share a team at all.

<!--chunk
id: dis.7
title: Chat-agent handling
summary: Heading only; the four handling components live in the sub-sections — considerations, dependency verification, financial parameters, solution construction.
keys: chat agent handling, agent guidance, discharge query handling, section container
needs: none
see: dis.7.1, dis.7.2, dis.7.3, dis.7.4
tokens: 10
-->
## 7. Chat-agent handling

<!--chunk
id: dis.7.1
title: Subject-matter considerations
summary: Three things to establish before diagnosing a discharge problem: this hospital's occupancy-driven urgency, nursing/coordination peak-load bandwidth, and housekeeping/transport turnaround capacity.
keys: occupancy urgency, nursing ratio, discharge coordination bandwidth, peak load staffing, shift structure, housekeeping capacity, bed turnover staffing, transport staffing, discharge volume
needs: common.shared-considerations
see: common.peak-load, dis.7.4.4, dis.8
tokens: 760
-->
### 7.1 Subject-matter considerations

**1. Shared Discharge/Bed/Admission/ALOS/Occupancy considerations.**
Governed by the shared "Discharge / Bed Management / Admission / ALOS / Occupancy" consideration set in `references/common-elements.md` — apply that full 8-point list whenever Discharge is the query subject. It sets how urgent discharge speed actually is for *this* hospital right now: a hospital at 60% occupancy has a different discharge-speed calculus than one at 95% with an ER backlog.

**2. Nursing and discharge-coordination staffing ratio (peak-load capacity check).**
Before diagnosing a discharge-speed problem as purely a process or ownership issue, check whether the staff actually executing discharge-associated tasks — nursing stock-take/reconciliation, discharge-summary handoff support, family/diet briefing coordination — have real bandwidth for it on top of their existing ward duties. Method, per the universal Peak-Load Staffing & Manpower Cost-Benefit Method in `references/common-elements.md`:
- Identify the relevant staff pool specifically for discharge-associated nursing/coordination work — exclude nurses whose time is dominantly bedside clinical care unrelated to discharge, and exclude ward managers/supervisors.
- Establish shift structure (typically at least 2 shifts, matching this hospital's actual nursing roster).
- Establish total daily discharge volume, and realistic per-discharge time for stock-take, handoff, and briefing support.
- Apply a peak-loading split against this hospital's own confirmed discharge pattern rather than an even 24-hour spread — per §7.4.4's worked example, discharge activity commonly clusters into a morning confirmation-through-completion window and a separate evening provisional-intake window, and the two windows can carry very different loads.
- The result: discharges (and the nursing/coordination tasks tied to them) handled per staff member per hour, peak vs. off-peak — which tells you whether nursing/coordination bandwidth, not just Discharge Executive headcount (§7.4.4), is itself a bottleneck, distinct from it.

**3. Housekeeping and Transport turnaround capacity.**
The same ratio-check method applies to the two remaining §3 upstream dependencies with a direct staffing dimension: housekeeping staff available per shift relative to bed-turnover volume (cleaning/preparing a bed between a discharge and the next admission), and transport staff (wheelchair/stretcher) available per shift relative to discharge volume. A discharge can be fully cleared clinically, financially, and administratively and still sit idle waiting on either of these — worth checking as its own bottleneck rather than assuming it's covered once nursing/billing capacity looks adequate.

These are the Discharge-specific instances of the universal Peak-Load Staffing & Manpower Cost-Benefit Method — see `references/common-elements.md`'s "Which ratio applies in which department" list, and KPI #14/#15 in §8 below, which track these on an ongoing basis once established.

<!--chunk
id: dis.7.2
title: Dependency verification protocol
summary: The four data pulls — staffing rosters, timestamped discharge volume, billing and TPA logs, and Bed Management's allocation and admission timestamps — required before any discharge diagnosis.
keys: data access, HIS, nursing roster, housekeeping roster, discharge timestamps, billing sign-off logs, TPA correspondence, bed allocation timestamps, practice pattern, verification
needs: dis.7.2.1
see: dis.3, dis.7.1, bed.7.2.1
tokens: 380
-->
### 7.2 Dependency verification protocol

Before reasoning about a specific hospital's discharge problem, check how *this* hospital's actual practice compares to the baseline dependency list in §3 — the real bottleneck is almost always in the practice pattern, not the org chart.

**Data/system access required**, to verify how this hospital's actual practice compares against the §3 baseline dependencies and the §7.1 considerations above:
- **Nursing roster and shift structure for discharge-associated duties**, and **daily discharge volume with timestamps** — to run the peak-load ratio checks in §7.1 points 2–3 and feed the cost-benefit comparisons those checks require.
- **Housekeeping and Transport staff rosters per shift**, against actual bed-turnover and discharge-transport volume — same purpose, for §7.1 point 3's remaining two dependencies.
- **Billing sign-off and insurance/TPA handoff logs**, to verify the actual (not just reported) turnaround named in question 8 below, directly against the system rather than a described-but-unverified process.
- **Bed-allocation and physical-admission timestamps for the same bed** (from Bed Management/HIS — when the bed was allocated to the next patient, and when that patient was physically admitted into it), and **Insurance/TPA correspondence timestamps** (first request sent, final approval received) — to run the TAT-authenticity cross-checks in questions 13–15 below, since a hospital's discharge time cannot be verified as genuine using Discharge's own records alone.

<!--chunk
id: dis.7.2.1
title: Practice-verification questions to put to the hospital directly
summary: Sixteen questions that locate the real bottleneck in practice, including three that test whether a reported Discharge TAT is genuine against Bed Management's own timestamps.
keys: verification questions, evening round sign-off, discharge summary ownership, billing turnaround, single point of ownership, automation level, discharge TAT authenticity, dead bed time, shared discharge admissions team, bed turnaround gap
needs: dis.7.2
see: dis.7.1, dis.7.4.4, common.peak-load, bed.7.1, bed.7.2.2, bed.7.3
tokens: 1970
-->
**Practice-verification questions to put to the hospital directly**, one at a time, once the data picture above is in hand:

1. Whether doctors make a *primary* discharge call during evening rounds, or only confirm the next morning.
2. What time discharge is typically confirmed.
3. Whether nursing/billing wait for all of a doctor's rounds to finish before starting stock-take and billing prep, or start as soon as their own patient is flagged.
4. When documents are sent to doctors to prepare discharge summaries.
5. Who actually prepares the discharge summary: the attending doctor directly, or a transcriptionist-drafts / junior-doctor-reviews / attending-confirms chain.
6. For multidisciplinary cases (multiple doctors involved), who owns preparing and approving the summary.
7. Whether doctors are willing to sign off on discharge during evening rounds for non-insurance patients specifically, so that patient can be arranged for discharge by 10 AM the next morning.
8. How long Billing actually takes to sign off on all chargeables, reconcile the final amount, and hand off to the insurance team.
9. Whether there is a single point of ownership for the entire discharge process, or whether it's diffused across teams with no one accountable end-to-end.
10. What level of automation, if any, is already built into their current process.
11. **Nursing/coordination staffing adequacy** — does anyone at the hospital already track discharges (or discharge-related nursing tasks) handled per staff member per shift, or is staffing for this simply assumed adequate because ward staffing overall looks adequate? This is the practice-verification counterpart to §7.1 point 2's ratio-check — confirm whether the hospital has ever run this calculation before Tojo runs it for them.
12. **Housekeeping/Transport turnaround adequacy** — is bed-turnaround time or transport availability for discharge ever tracked as its own metric, separately from discharge-process time itself? A discharge that's clinically/financially/administratively complete can still stall here, and a hospital that only tracks "time to discharge order signed off" can miss this entirely.
13. **Average admission time, alongside average discharge time.** Ask not only for average discharge duration/timing (questions 1–2) but also the average time of admission — specifically both when a bed is actually allocated to a waiting patient, and when that patient is physically admitted into it. This does two jobs at once: (i) it produces the real turnaround gap between a patient physically leaving a bed and the next patient physically arriving in it — a gap beyond roughly 30 minutes flags a genuine inefficiency somewhere in Bed Management's allocation, Housekeeping's turnaround, or another handoff, worth naming specifically rather than assumed away; (ii) it doubles as a check on whether the discharge time the hospital reports is genuine, or has been adjusted to show a lower discharge TAT than actually occurred. A gap beyond 30 minutes means one of the two is true — real inefficiency, or a recorded discharge time that doesn't reflect when the patient actually left — and both are worth surfacing rather than taking the reported figure at face value.
14. **Cross-verify the hospital's own reported Discharge TAT — don't just accept it.** Ask what Discharge TAT the hospital currently reports, then check its authenticity against:
    - The actual gap to the next admission on that same bed (question 13) — a genuine TAT should be consistent with a genuine bed-turnaround gap; a mismatch between the two is itself a finding.
    - Whether the hospital's TAT clock starts from the provisional discharge call in the evening, or only from discharge confirmation the next morning — these are two different starting points for the same underlying process and produce very different numbers, without necessarily being labeled as such.
    - Whether the reported TAT actually includes the Insurance/TPA approval window end-to-end, or whether the hospital has quietly excluded it — stripping out the time between the first request sent to Insurance and their final approval, so the figure reflects only the hospital's own portion of the process rather than what the patient/family actually experiences. This is a common way a hospital's quoted TAT understates the real one, and it needs to be checked explicitly, not assumed away.
15. **The correct definition of Discharge TAT, and when to hold a hospital to it as a check.** Properly defined, Discharge TAT ends when the next patient is physically admitted into that same bed — or, where the bed is not reoccupied that day, when the patient physically leaves the bed. That is the correct definition in principle, for any hospital: it closes the loop on the entire process rather than letting inefficiency hide in whatever time isn't being tracked. Where it becomes an active efficiency *check* rather than a definitional point is **above 80% occupancy** — that is where bed-turnaround speed matters most, it is the same threshold as the Discharge Manager trigger in §7.4.4, and it is the natural point at which to measure through to the next admission and hold the hospital to what that reveals. Note that `bed-management.md` §7.1 point 2 carries the same definition from the Bed Management side, and that this measurement can only be made using Bed Management's own allocation and admission timestamps, per §7.4.2.

    **The revenue clock is not the same clock, and it starts earlier.** Discharge TAT runs on the patient's physical movement. Revenue on that bed stops at a different, earlier moment — when the outgoing patient's bill is finalised and sent for insurance approval, typically late morning, while the patient normally stays in the bed through approval, payment, family briefing and physical exit. Everything billable through that bed stops with it: pharmacy, diagnostics, procedures, and any OT slot depending on it. That stretch, running from bill finalisation to the initiation of the next patient's bill, is **dead bed time**, defined in `bed-management.md` §7.3 point 5 and measured there. It matters on the Discharge side because the discharge tail *after* billing closes — approval, payment, briefing, physical exit, turnaround — sits entirely inside it and is Discharge's to compress. Do not treat a good Discharge TAT as evidence that this stretch is short; they measure different things, and only the bill-to-bill number tells the hospital what the bed actually cost it.
16. **Does the hospital have the same team doubling with discharge and admission roles, or completely separate teams for the two roles?** Ask this directly. Where it is one team, follow it with what that team's day actually looks like — does it work discharges through the morning and only turn to admissions afterwards, with admissions consequently scheduled for late afternoon or evening? A hospital that answers "one team, discharges first" has described §6's serialised-team mechanism without necessarily recognising it as a problem. This bears on Discharge as much as on Bed Management: it means the hospital's morning discharge focus is being paid for out of its own admission revenue. The same question appears in `bed-management.md` §7.2 as question 8, and where a Bed Management conversation is running alongside, ask it once and use the answer in both.

Where the hospital's actual practice differs from what fast discharge requires (e.g., no early evening sign-off, no single owner, fully manual handoffs, no visibility into nursing or housekeeping/transport bandwidth, one team serialising discharges and admissions per question 16, or a reported Discharge TAT that doesn't hold up against questions 14–15's cross-checks), that gap *is* the diagnosis — the agent should name it specifically rather than defaulting to a generic "improve coordination" answer.

<!--chunk
id: dis.7.3
title: Financial parameters to check
summary: The six financial parameters every discharge cost-benefit case is argued against: ARPOB, daily average revenue, OT utilisation, OT revenue, ICU occupancy and bed occupancy.
keys: ARPOB, daily average revenue, OT utilisation, OT revenue, ICU occupancy, bed occupancy, financial parameters, cost benefit
needs: none
see: dis.7.4, dis.8
tokens: 30
-->
### 7.3 Financial parameters to check
ARPOB · Daily Average Revenue · OT Utilisation · OT Revenue (daily) · ICU Occupancy · Bed Occupancy

<!--chunk
id: dis.7.4
title: Solution construction method
summary: For Discharge the recommended solution is identical at any size or occupancy; only whether its cost is justified right now varies, decided by cost-benefit against the §7.3 parameters.
keys: solution construction, cost benefit analysis, before after comparison, four aspects, discharge manager, occupancy level, ALOS reduction, scale invariance, worked example
needs: common.solution-method, dis.7.3
see: dis.7.4.1, dis.7.4.2, dis.7.4.3, dis.7.4.4, bed.7.4
tokens: 390
-->
### 7.4 Solution construction method
Follows the two genuinely universal rules in `references/common-elements.md`: mandatory cost-benefit analysis + side-by-side graphical before/after comparison, and the four-aspect solution shape.

**Specific to Discharge Process** (not a general rule — see `references/common-elements.md`'s "what is NOT assumed universal"): for this problem specifically, the actual recommended solution is the same for hospitals of any size or occupancy level — what varies is whether the solution's cost implications are justified *right now* for a given hospital, decided via cost-benefit analysis against §7.3's financial parameters. Note that this finding is Discharge-specific and does **not** carry across: `bed-management.md` §7.4 records the opposite finding for that department, where the solution itself scales with a demand-vs-supply pivot.

Worked example: recommending a dedicated Discharge Manager to handle a hospital's discharge process end-to-end is the same recommendation at any occupancy level. At 95% occupancy, the 6–8 hours saved and earlier discharge times (11 AM for cash patients, 1 PM for insured) driving a ~0.5-day ALOS reduction plus better OT utilisation and OT revenue make the added headcount cost obviously worth it. At 60% occupancy, the same fix may not yet be pressing enough to justify that cost. Solution content stays constant; whether/when to act on a given cost-bearing part of it is gated by that hospital's current numbers.

Department-specific answers to the four required aspects:

<!--chunk
id: dis.7.4.1
title: Automation
summary: Continuous event logging from admission onward lets the summary assemble on a provisional mention, the bill auto-finalise, stock-take stop gating billing, and insurance start the evening before.
keys: automation, event log, discharge summary generation, provisional discharge, auto billing, pharmacy returns, consumables balance, insurance TPA approval, digital sign-off, manpower savings
needs: dis.7.4
see: dis.7.4.2, dis.7.4.3
tokens: 940
-->
#### 1. Automation

**Core capability:** the moment a doctor even provisionally mentions discharge — including a passing mention on an evening round, not a formal order — the system immediately assembles and presents a full discharge summary, with approval sought from the doctor right there. This is possible because the system continuously reads and logs clinical/operational events for that patient from admission onward, rather than reconstructing everything retrospectively at the point of discharge. What it continuously tracks:

a. History, symptoms, prognosis, diagnosis at admission (direct or via Emergency)
b. All investigations carried out and their summarised findings, especially abnormalities
c. All procedures and surgeries done, with notes
d. All medications prescribed, administered, and changed — with real-time consumed vs. remaining quantities, calculated at the level of strips/bottles/minimum dispensable denomination (not exact individual units), specifically so the system knows what's realistically returnable to pharmacy
e. All consumables requisitioned, used, and remaining balance — returnable to the extent the balance is in discrete whole units
f. Doctor's daily progress observations
g. The reasons behind every investigation, procedure, clinical management step and prescription, and its outcome

**Billing follows automatically from the same event log.** Because every event is logged, costs and charges get assigned per event (drawn from the ERP), so the running bill-to-date is continuously available. Because stock issued/used/balance is tracked in real time, expected pharmacy/consumable reversals are known too — in effect, the bill auto-finalises the moment discharge is confirmed. For a *provisional* discharge (doctor signals it the evening before, anticipating confirmation next morning), the system projects costs and returns through the anticipated discharge point and has that ready that same evening, for the billing team to check first thing the next morning — or that same evening, if time permits.

**Nursing's stock-take stops being a gating step.** Since actual stock usage and returnable balances are already computed from the event log, Nursing receives the expected return calculation directly instead of having to perform it manually before billing can close — billing no longer waits on nursing stock-take.

**Insurance approval starts the evening before.** A provisional bill (assuming costs and returns through the anticipated next-day discharge) goes to the Insurance/TPA team that same evening for primary approval. Once the doctor confirms discharge the next morning, the final bill — with all reports and the discharge summary — goes to Insurance immediately and automatically for final payment approval. For cash-paying patients, both the provisional and final bills go straight to the patient/family without delay.

**Doctor sign-off is digital and immediate.** The final discharge summary is re-presented to the doctor on mobile/tablet the moment he confirms discharge the next morning, for digital review and sign-off right there — which then triggers the send to Insurance for final approval.

**End state (once trust is established):** provisional bills (evening) and final bills (morning) go directly to the insurer or patient/family without manual cross-checking by the Insurance or Billing teams at all — this is a maturity endpoint the automation is built toward, not necessarily day-one behavior.

**Net effect of this level of automation:**
- Time saved: 6–8 hours
- Revenue: prorated as ARPOB × No. of Beds × 365 days (the freed bed-days converted to annualised revenue potential)
- Manpower cost savings: the entire Insurance/TPA team's workload, and a reduction in Billing team headcount need

<!--chunk
id: dis.7.4.2
title: Process changes
summary: The existing flow is kept as an automation layer, but ERP/PACS integration, agent-approval duties, breaking the shared discharge/admissions team, and real bed timestamps are required.
keys: process change, ERP integration, PACS, agent approval, adoption positioning, serialised team, admissions overlap, bed allocation timestamps, downstream functions, dietitian pharmacy housekeeping transport
needs: dis.7.4, dis.7.4.1
see: dis.7.2.1, dis.7.4.3, bed.7.4.1, bed.7.4.2
tokens: 730
-->
#### 2. Process changes

The underlying process stays essentially the same — this is an automation layer on the existing flow, not a redesign of it — but with these shifts:
- A large share of team members need to be onboarded to *approve and access* the deployed agents as part of their role, rather than performing the equivalent step manually.
- IT must ensure the agents can extract data from the ERP, PACS, and every other system holding investigations, reports, and clinical notes, so the clinical, financial, and administrative aspects of every event (per §7.4.1's event list) are actually captured — this is the integration prerequisite everything else depends on.
- Positioning matters for adoption: initially, the agent operates as an automated extension of each team member's existing job — capturing and surfacing what they'd otherwise do manually — not a replacement. Only later, once the automation is trusted and proven, does it start actually removing the need for parts of their daily work. (This sequencing is also the buy-in mechanism — see §7.4.3.)
- Bed Management and any other downstream function affected by discharge timing needs to check the discharge-automation agent's output directly, for as long as *that* function itself isn't automated.
- Dietitian, Pharmacy, Housekeeping, and Transport teams need to watch for the agent's updates on when they're required to act to keep the discharge on schedule, for as long as their own individual functions aren't automated.
- **Where one team runs both discharges and admissions (§7.2 question 16), that serialisation has to break.** Either separate the two roles into distinct teams, or explicitly overlap the two windows so admission processing runs alongside the morning discharge work rather than queueing behind it. This is a Discharge-side change as much as a Bed Management one — see `bed-management.md` §7.4.2, which carries the same requirement — and it costs nothing but sequencing discipline.
- **Bed Management's own system needs to produce accurate, real-time bed-allocation and physical-admission timestamps**, for §7.2's TAT-authenticity checks (questions 13–15) to mean anything at all — without them, a hospital's reported Discharge TAT can only be checked against Discharge's own records, not against what actually happened. The proper fix is Bed Management's own automation (see `bed-management.md` §7.4.1's planned-admission-to-bed mapping, and specifically §7.4.1(c)'s discharge-linkage double control, where Bed Management and Discharge each verify the other's actual timings, not just their own reported ones) — or, at minimum, where that automation isn't yet in place, a manual Bed Management process disciplined enough to replicate its logic: real-time, accurate logging of when a bed is allocated and when the next patient is physically admitted into it, not just of when the previous patient was discharged.

<!--chunk
id: dis.7.4.3
title: Key people & buy-in
summary: Which teams must cooperate, why the COO approves the cross-departmental process flows rather than daily work, and why the agent is pitched as an extension of each role.
keys: buy-in, stakeholders, IT integration, doctors, voice commands, nursing approval, billing, insurance TPA, COO, head of operations, process flow approval, adoption
needs: dis.7.4
see: dis.7.4.1, dis.7.4.2, dis.7.4.4
tokens: 380
-->
#### 3. Key people & buy-in

Teams whose cooperation is required: IT (integration) · Diagnostic & Investigation teams (capturing events, updating reports on time) · Doctors (initiating provisional discharge, approving provisional/final summaries in real time on mobile/tablet, recording remarks/diagnosis/prescriptions/management via voice commands integrated into the agent's interface) · Nursing (real-time approval of notes/information the system captures from doctors' voice notes and any on-floor changes made afterward) · Billing · Insurance/TPA · Admissions · Housekeeping · Dietitian · Ward Manager.

**Head of Operations / COO.** Both the Discharge Manager and the Bed Manager report to this level, which makes it the level that authorises coordination between the two departments — and the level whose sign-off the §7.4.2 process changes need, particularly the decoupling of discharges from admissions. Its role here is to **approve the process flows**, not to contribute to daily tasks: don't design the solution around COO involvement in daily discharge activity, but don't expect a cross-departmental sequencing change to hold without their explicit approval.

Buy-in mechanism: per §7.4.2, the agent is introduced as an automated extension of what each of these roles already does — reducing their manual burden and errors — rather than as a threat to the role itself. The reduction in headcount need (§7.4.1's manpower savings, §7.4.4 below) is a later-stage consequence of proven trust, not the opening pitch.

<!--chunk
id: dis.7.4.4
title: Team/role changes
summary: Two separately triggered and priced roles — a condition-triggered Discharge Manager owning the process end-to-end, and volume-sized Discharge Executives sized by ratio-check, not a flat rule.
keys: discharge manager, discharge executive, headcount sizing, salary cost, occupancy threshold, discharges per day, peak load ratio check, role split, worked example, two windows
needs: dis.7.4
see: dis.7.1, dis.7.4.3, common.peak-load, bed.7.4.4
tokens: 880
-->
#### 4. Team/role changes

Almost every team involved sees a modest expansion of scope — recording and approving information in the system so the agents can capture every event accurately — rather than a wholesale role change.

Beyond that there are **two separate role decisions**, triggered differently and priced differently. Don't collapse them into one recommendation.

**a. The Discharge Manager — ₹4–4.5 lakhs/year.**
Owns the entire discharge process end-to-end as its single point of contact. The role is about **coordination with other departments and ownership of the whole process**, not processing volume — which is why it is not sized per discharge. It sits at the same level as the Bed Manager in `bed-management.md` §7.4.4(a): the two are peers, coordination runs between their departments, and both report to the Head of Operations / COO (§7.4.3).

Recommend the role for hospitals at **>80% occupancy or >40 discharges/day** — and, mirroring `bed-management.md` §7.4.4(a)'s third condition, wherever the hospital continually overruns its own expected Discharge TAT, since a sustained breach signifies exactly the cross-departmental coordination failure this role exists to fix. Below those conditions the role is optional, and better framed as an investment in efficiency and future team-optimisation potential than as an immediately self-justifying cost.

**b. Discharge Executives — volume-sized, ₹3–3.5 lakhs/year each.**
The processing layer: owning each discharge from the moment a doctor signals a provisional discharge, and catching efficiency gaps or offline hurdles/delays as they arise. Sized at roughly **15 discharges/day per person** — a flat rule of thumb, which the Peak-Load Staffing Method requires be checked against the hospital's actual shift pattern and volume before it is used to size headcount.

**Worked example — running the ratio-check instead of applying the flat figure.** Worked example from a practice conversation, illustrating the method rather than fixing a new universal number: a hospital confirmed at 40–45 discharges/day naively divides by ~15/day into "about 3 people" — but that hospital's own confirmed activity pattern doesn't spread evenly across 24 hours; it clusters into two windows (morning confirmation-through-completion, roughly 8–11 AM into early afternoon, and evening provisional intake, 6–9 PM). Running the ratio-check properly against that two-window pattern — identify the Discharge Executive function specifically as the staff pool, use the hospital's real volume and shift pattern rather than a flat 24-hour spread, and size per-person capacity at peak rather than off-peak — lands on **2 Discharge Executives, one anchored to each window**, at a combined cost of roughly **₹6–7 lakhs/year**: narrower than a naive flat-ratio division, but more than the single hire a cruder reading would imply. That same hospital, at 40–45 discharges/day, independently crosses the Discharge Manager condition in (a) above — so the correct recommendation for it is one Manager plus two Executives, not one hire covering both jobs. The revenue opportunity the roles are justified against is unchanged by this correction — only the headcount conclusion is sharper. Treat the resulting headcount number as specific to that hospital's own shift/volume pattern, not a new default to reuse elsewhere — re-run the ratio-check for each hospital. See `discharge-process-conversation-playbook.md` §4 for the full worked dialogue this example is drawn from.

<!--chunk
id: dis.7.status
title: Status and change log
summary: Which parts of this file are complete and approved, which revisions produced the current §7.2 and §7.4.4 wording, and which corrections are still outstanding elsewhere.
keys: status, change log, open items, role split, revenue clock, question 15, question 16, playbook correction, KPI 13, approval
needs: none
see: none
tokens: 820
retrieve: never
-->
---

**Status: Discharge Process content complete and KPIs approved.** All four Chat-agent handling components (§7.1–7.4) are filled. §8's KPI list, drafted by Claude and delivered 2026-09-02, was approved by Avishek as drafted on 2026-09-09. §7.1 and §7.2's Peak-Load Staffing Method retrofit — nursing/housekeeping/transport ratio-check considerations woven into §7.1, and matching data-access + numbered practice-verification questions woven into §7.2 — was completed 2026-09-09, mirroring OPD-Diagnostics' §7.1/§7.2 treatment. On the same date, §7.2 gained three further practice-verification questions (13–15) on cross-verifying a hospital's reported Discharge TAT for authenticity, and §7.4.2 gained a dependency on Bed Management's own system producing genuine, real-time bed-allocation and admission timestamps for those TAT checks to be verifiable at all; see `bed-management.md` §7.1/§7.2/§7.4.2 for the reciprocal update made there the same day.

On 2026-09-10, three changes were made alongside the Bed Management finalisation pass. §7.2 question 15 was rewritten: measuring Discharge TAT through to the next patient's admission into that bed (or to the patient leaving it where it isn't reoccupied) is now stated as the *correct definition* for any hospital, with the >80% occupancy threshold retained as the point at which to apply it as an active efficiency check rather than as a condition on the definition itself. §7.2 gained question 16, on whether the hospital runs one team doubling as discharge and admissions or two separate teams — with §6 gaining the corresponding serialised-shared-team failure mode, seen from the Discharge side. And §7.4.4 was split into two separate role decisions: the **Discharge Manager** at ₹4–4.5 lakhs/year, condition-triggered and owning the process end-to-end as the Bed Manager's peer, and the **Discharge Executives** at ₹3–3.5 lakhs/year each, volume-sized at ~15 discharges/day via the ratio-check. Previously this section conflated the two, recruiting an "Executive" to "own the entire process end-to-end" at a single ₹3–3.5 lakh figure. The worked example's headcount and ₹6–7 lakhs/year cost are unaffected by the split and stand as they were.

**Later on 2026-09-10, §7.2 question 15 gained the revenue-clock note**, the reciprocal of the dead-bed-time redefinition made in `bed-management.md` §7.3 point 5 the same day. Discharge TAT runs on the patient's physical movement; revenue on that bed stops earlier, at bill finalisation, while the patient is still in the bed. The stretch from that moment to the initiation of the next patient's bill is dead bed time, and the part of it that Discharge owns is the tail after billing closes — approval, payment, briefing, physical exit and turnaround. The note exists so a good Discharge TAT is not mistaken for evidence that the bed was earning.

Still open: `discharge-process-conversation-playbook.md` refers to the old single-role framing in §4 and §7 (including "the Discharge Executive threshold") and needs correcting to match §7.4.4's split; §8's KPI #13 tracks the threshold under the old framing; and the restructure of that playbook into a shared department-deep-dive file plus per-department appendices is provisionally agreed for after the Bed Management practice conversation.

<!--chunk
id: dis.8
title: KPIs
summary: Sixteen approved KPIs covering discharge timing, automation maturity and adoption, financial conversion, staffing ratios, and family-briefing completion.
keys: KPI, discharge cycle time, discharge by 10 AM, bed turnaround time, ALOS contribution, billing finalization turnaround, insurance approval turnaround, ARPOB, OT revenue, staffing ratio, briefing completion
needs: none
see: dis.3, dis.7.3, dis.7.4.1, dis.7.4.4, common.peak-load
tokens: 1050
-->
## 8. KPIs <!--m-->(drafted by Claude 2026-09-02, approved by Avishek as drafted 2026-09-09)<!--/m-->

### Core discharge timing
1. **Discharge-order-to-physical-discharge cycle time** — the department's core end-to-end metric.
2. **% of non-insurance discharges completed by 10 AM**, and **% of insured discharges completed by 1 PM** — the two target times named in §7.4's worked example, tracked separately since insured and non-insured patients follow different bill-clearance paths.
3. **% of discharges triggered by a provisional evening-round mention** vs. **same-day-only order** — measures how much of the automation's core value proposition (§7.4.1 — acting on a passing mention, not waiting for a formal order) is actually landing in practice.
4. **Bed turnaround time** — from physical discharge to the bed being usably available for the next admission (ties directly to Housekeeping's dependency in §3 and to Bed Management's own KPIs).
5. **ALOS contribution from discharge delay specifically** — isolating the portion of ALOS attributable to avoidable discharge-process time (per §6's failure-mode framing), distinct from clinically-necessary stay length.

### Automation maturity & process adoption
6. **% of discharges where Nursing's stock-take is no longer a gating step** — i.e. the expected-return calculation was available from the event log rather than requiring manual reconciliation before billing could proceed (§7.4.1).
7. **Billing finalization turnaround** — time from the doctor's discharge order/confirmation to the bill being fully finalized.
8. **Insurance/TPA approval turnaround**, tracked separately for the provisional (evening) and final (morning) approval steps (§7.4.1).
9. **% of provisional/final bills going straight to the insurer or patient/family without manual cross-checking by Billing or Insurance** — the direct measure of progress toward §7.4.1's stated maturity end-state, useful as a trend line showing how much trust has actually been built rather than a static automation flag.

### Financial
10. **ARPOB** and **Daily Average Revenue** (from §7.3, tracked as ongoing KPIs, not just diagnostic parameters).
11. **OT Utilisation** and **OT Revenue (daily)** — specifically the portion attributable to same-night/early-morning OT slots freed up by faster discharge (§3's OT-Scheduling downstream dependency).
12. **Realized vs. theoretical revenue impact** — actual freed-bed-day revenue captured, benchmarked against the ARPOB × No. of Beds × 365 potential named in §7.4.1, to show how much of the theoretical upside is actually being converted.

### Staffing & ratios
13. **Role threshold tracking** — occupancy % and discharges/day tracked against the **>80% occupancy or >40 discharges/day** Discharge Manager conditions in §7.4.4(a), plus the proportion of discharges overrunning expected Discharge TAT (the third condition), as operational trigger metrics in their own right. <!--m-->*(Wording predates §7.4.4's 2026-09-10 role split; the third condition is not yet reflected in the approved text and needs a revision pass alongside `bed-management.md` §8's.)*<!--/m-->
14. **Nursing ratio per bed for discharge-associated functions**, and **discharges handled per staff per hour (peak vs. off-peak)** — the Discharge-specific instances of the universal Peak-Load Staffing & Manpower Cost-Benefit Method in `references/common-elements.md`, now also grounded directly in §7.1 point 2 and §7.2 question 11's verification protocol.
15. **Housekeeping and Transport staff availability per shift, relative to discharge volume** — same method, applied to the two remaining §3 upstream dependencies with a clear staffing-ratio dimension, per §7.1 point 3 and §7.2 question 12.

### Patient/family experience
16. **Family/patient briefing completion rate before physical discharge** — % of discharges with documented delivery of diet, medication, and follow-up instructions before the patient leaves, directly enforcing the non-negotiable in §4 that this is never skipped for speed.

<!--m-->*(All 16 were Claude's first draft, delivered per Avishek's 2026-09-02 request alongside OPD-Diagnostics' and Bed Management's KPI lists, and approved by Avishek as drafted on 2026-09-09.)*<!--/m-->
