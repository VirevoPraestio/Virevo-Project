# Tojo — Point Index

This is the layer below the chunks: every individually named activity, dependency, non-negotiable, flex, failure mode, consideration, verification question, financial parameter, solution element and KPI in the Tojo v2 hospital-ops library, each carried with the chunk it lives in. It is a retrieval artefact only — the retriever searches it, and it never enters the prompt; what enters the prompt is the chunk a row points at. Read the columns as: `point` is the stable id, built as `<chunk>#<kind><n>` so the id itself names its chunk; `what it is` is a compressed statement of the thing, not a summary of the surrounding section; `chunk` is what to fetch; `also called` is the phrasebook — the words a hospital would actually use, which is what most queries will match on. 524 points across the five files cover 63 of the 65 retrievable chunks in the library (`dis.7` and `opd.7` are section-container headings with no content of their own and so carry no points).

## How a lookup works

1. A hospital says "we don't record when housekeeping is notified that a bed is free."
2. Match on `also called`, not on the formal description — here "bed cleaning time", "how long the bed sits empty", "getting the bed cleaned".
3. The matching rows hand back their chunk: `bed.8#k6` and `dis.8#k4` both give bed turnaround time, `dis.2#a9` gives the handoff itself, `bed.3#d2` gives the dependency.
4. Fetch that chunk, plus its one-hop `needs` from the chunk header — never the whole department file.
5. Where a concept spans departments, the Cross-department table below says which point is the definition and which are references, so the fetch starts from the owning chunk.

## Cross-department concepts

Each row is one underlying thing that is indexed under point ids in two or more files. The `note` says which id owns the definition and which merely reference or instantiate it — a retriever that lands on a reference should follow the note to the owner before answering.

| concept | points | note |
|---|---|---|
| ALOS (average length of stay) | `common.shared-considerations#c4`; `bed.7.3#p1`, `bed.3#d12`, `bed.8#k9`, `bed.7.4.1#p4`; `dis.3#d7`, `dis.8#k5`, `dis.7.4#s6` | Defined once in common as a baseline financial parameter. Bed carries it as a downstream dependency, a §7.3 parameter and a KPI; Discharge carries it as a Critical dependency and isolates the discharge-delay share of it (`dis.8#k5`). The 0.5-day reduction claim lives only in `dis.7.4#s6`. |
| ARPOB (average revenue per occupied bed) | `common.shared-considerations#c3`; `dis.7.3#p1`, `dis.3#d8`, `dis.8#k10`, `dis.7.4.1#p2`; `bed.7.3#p1` | Definition in common. Discharge instantiates it most heavily, including the annualisation formula in `dis.7.4.1#p2`. Bed references it only as part of the shared baseline block. |
| Bed Occupancy and ICU Occupancy | `bed.7.3#p2`; `bed.8#k8`, `bed.1#a3`; `dis.7.3#p5`, `dis.7.3#p6`; `opd.3#d18` | `bed.7.3#p2` is the owner and carries the rule that the two are tracked separately and never blended. Discharge lists them as two flat parameters, which is the same quantity stated without the rule. OPD reaches the same number indirectly, via admissions driven by diagnostic findings. |
| Daily / Daily Average Revenue | `bed.7.3#p3`, `bed.3#d11`, `bed.8#k15`; `dis.7.3#p2`, `dis.3#d14`, `dis.8#k10`; `opd.3#d12` | The same aggregate line appears as a §7.3 parameter, a Critical downstream dependency and a KPI in all three departments. No file owns it; treat `common.shared-considerations` as the baseline block it belongs beside. |
| OT scheduling, OT Utilisation and OT Revenue | `common.shared-considerations#c6`; `bed.3#d6`, `bed.3#d10`, `bed.2#a13`, `bed.7.2.2#q3`, `bed.7.3#p4`; `dis.3#d11`, `dis.3#d12`, `dis.3#d13`, `dis.7.3#p3`, `dis.7.3#p4`, `dis.8#k11` | The OT-to-bed link is defined as a shared consideration in common. Bed sees OT as both an upstream need (post-op reservation) and a downstream victim (elective cancelled for want of a bed); Discharge sees the same OT slots as revenue freed by earlier discharge. Same theatre, three vantage points. |
| Dead bed time (bill finalisation → next bill initiation) | `bed.7.3#p5`; `bed.6#c1`, `bed.7.1#c7`, `bed.7.4.1#p3`, `bed.8#c3`, `bed.7.2.1#c5`, `bed.7.2.2#q11`, `bed.7.4.2#s8`; `dis.7.2.1#c1` | Owned by Bed — `bed.7.3#p5` is the definition. `dis.7.2.1#c1` is Discharge's single reference to it, and is the one that explains why a good Discharge TAT can still sit inside dead bed time. A query about unbilled bed hours should land on the Bed chunk even when the hospital frames it as a discharge problem. |
| Bed turnaround time (physical discharge → usably available bed) | `bed.8#k6`; `dis.8#k4`; `dis.7.2.1#q12`, `bed.6#f4`, `dis.2#a9`, `bed.2#a9` | The identical KPI, worded differently, in both departments' §8 lists. Neither is the definition; they are co-equal. `dis.7.2.1#q12` is the verification question asking whether it is tracked as its own metric at all. Distinct from dead bed time — this clock is physical, that one is billing. |
| Discharge TAT — correct definition, ending at the next admission into that bed | `dis.7.2.1#q15`; `bed.7.1#c6`; `dis.7.2.1#q14`, `bed.7.1#c2`, `bed.7.2.2#q7`, `dis.8#k1` | Defined in Discharge (`dis.7.2.1#q15`) and restated verbatim in Bed (`bed.7.1#c6`) because Bed needs the same clock to test whether a claimed vacancy is real. The three-check verification appears on both sides too (`dis.7.2.1#q14`, `bed.7.2.2#q7`). |
| Admission timestamps — bed allocation and physical admission, and Admission TAT | `bed.7.1#c4`, `bed.7.1#c8`–`bed.7.1#c12`, `bed.7.2.1#c4`, `bed.7.2.1#c6`, `bed.7.2.2#q10`, `bed.7.4.2#s7`, `bed.7.4.1#p1`, `bed.8#c2`; `dis.7.2#d4`, `dis.7.2.1#q13`, `dis.7.4.2#s8` | Bed owns the measurement, including the five-stage decomposition. Discharge asks for exactly the same timestamps from the other side: `dis.7.2#d4` requests them as data, `dis.7.4.2#s8` names Bed Management as the team obliged to produce them. The same dependency on two tables, pointing opposite ways. |
| The serialised shared team — discharges till 12–2 PM, then admissions at 4–8 PM | `dis.6#f5`; `bed.6#f5`; `dis.7.2.1#q16`, `bed.7.2.2#q8`; `dis.7.4.2#s7`, `bed.7.4.2#s1`, `bed.7.4#s4` | One operational fact indexed seven times across two files — as a failure mode, as a verification question and as a fix, in each department. Neither file is the definition; both state it in full. The fix wording differs (split the roles vs. overlap the windows) but the change is the same change. |
| Provisional discharge as a formally tracked 24-hour-advance signal | `dis.2#a1`, `dis.8#k3`; `bed.7.4#s3`, `bed.7.4.2#s3`, `bed.8#k10`; `common.shared-considerations#c7` | Discharge owns the activity (early flagging) and measures how many discharges it triggers. Bed owns the service level demanded of it — 24 hours in advance — and measures the same signal as an inbound percentage. The two KPIs count the same events from either end. |
| ICU step-down signal and step-down mapping | `common.shared-considerations#c8`; `bed.3#d4`, `bed.2#a6`, `bed.7.2.2#q5`, `bed.7.4#s10`, `bed.7.4.1#s3`, `bed.7.4.2#s3`, `bed.8#k3`, `bed.8#k11`; `dis.3#d9` | The mapping requirement is defined in common. Bed instantiates it fully, down to the 1 PM signal deadline. `dis.3#d9` is the same protocol seen as a Critical dependency of Discharge — the ICU bed that will not clear. |
| Mapping planned admissions against provisional discharges and expected bed availability | `common.shared-considerations#c7`; `bed.7.2.2#q4`, `bed.7.4#s2`, `bed.7.4.1#s2`, `bed.7.4.1#s7`, `bed.8#k1`, `bed.8#k2` | Defined in common as a shared consideration; Bed is where it becomes an actual daily mechanism with a 2 PM pass and a 6 PM freeze. A query about tomorrow's bed picture should be answered from Bed, not from common. |
| Bed availability for admission ↔ timely bed release — the same edge, opposite directions | `bed.3#d1`; `dis.3#d10`; `bed.3#d8`, `bed.3#d9`, `bed.8#k7`, `bed.2#a8` | `bed.3#d1` lists Discharge as Bed's Critical upstream; `dis.3#d10` lists Bed Availability as Discharge's Critical downstream. One dependency, entered twice from either side. The ER boarding consequence is indexed only on the Bed side (`bed.3#d8`, `bed.8#k7`). |
| The Discharge–Bed double control | `bed.7.4#s6`, `bed.7.4.1#s4`; `dis.7.4.2#s5`, `dis.7.4.2#s8` | Bed names it as a control it applies to Discharge's timings; Discharge names it as downstream functions reading its agent's output directly. Same cross-check, described as an obligation by each file about the other. |
| Housekeeping and transport turnaround capacity | `common.peak-load#k5`; `bed.3#d2`, `bed.7.1#c3`, `bed.7.2.1#c2`, `bed.8#k17`, `bed.6#f4`; `dis.3#d5`, `dis.3#d6`, `dis.7.1#c3`, `dis.7.2#d2`, `dis.8#k15`; `opd.7.1.1#c7`, `opd.8#k13`, `common.peak-load#k3` | The ratio method is owned by common. Bed and Discharge run it against the same staff pool for the same beds — genuinely the same people counted twice. OPD's version (`common.peak-load#k3`) is a different duty for the same function: moving non-ambulatory patients to diagnostics, not turning beds. |
| Peak-load staffing ratio method and its six named instances | `common.peak-load#s1`–`#s6`, `#n1`–`#n3`; instances `common.peak-load#k1`–`#k6`; run as `opd.7.1.1#c3`, `opd.7.1.1#c5`, `opd.7.1.1#c7`, `dis.7.1#c2`, `dis.7.1#c3`, `bed.7.1#c3`, `bed.7.1#c5`; measured as `opd.8#k10`, `opd.8#k12`, `opd.8#k13`, `dis.8#k14`, `dis.8#k15`, `bed.8#k17`, `bed.8#c4`; applied as `play.4#s6`, `play.9#s3` | One method, defined once in common, with six named ratios and then a third copy of each as an ongoing KPI in the department files. `common.peak-load#k6` explicitly says the method lives in common and the KPI lives in Bed — the clearest statement of the pattern this whole table describes. |
| Staffing enables volume, not the reverse (the causality reversal) | `common.peak-load#f2`; `opd.7.1.2#c11`, `opd.0#f2`, `opd.6#f4`, `opd.7.2#q13`; `common.peak-load#n1` | Promoted to common as universal. OPD holds four separate instances of it — case-study fact, failure mode, reasoning principle and verification question — which is why an OPD query will hit the instance before the rule. |
| A single named owner of the process end-to-end | `common.shared-considerations#c2`; `dis.6#f4`, `dis.7.2.1#q9`, `dis.1#a1`, `dis.7.4.4#s3`; `bed.7.2.2#q2`, `bed.7.4#s1`; `opd.6#f3`, `opd.7.1.1#c4` | The check is defined in common. Each department names its own absence of one as a failure mode and its own creation of one as a fix. OPD's version is scoped to the scheduling protocol specifically rather than the whole department. |
| Whether the process is already automated — the maturity baseline | `common.shared-considerations#c1`; `dis.7.2.1#q10`; `bed.7.2.2#q1`; `opd.7.2#q8` | Defined in common; asked near-identically in all three departments' verification protocols. `bed.7.2.2#q1` is the broadest, covering Discharge, Admission and Bed Scheduling in one question. |
| The threshold-triggered Manager hire at ₹4–4.5 lakhs/year | `dis.7.4.4#s3`, `dis.7.4.4#p1`, `dis.7.4.4#s4`; `bed.7.4.4#s1`, `bed.7.4.1#p6`, `bed.7.4.4#c2`–`#c5`, `bed.7.4#s12`; `opd.7.4.3#s10`, `opd.7.4.4#s16`, `opd.7.4.4#s17` | The same role shape and the same price at the same >80% occupancy trigger in Discharge and Bed — `dis.7.4.4#s3` calls the Bed Manager its peer explicitly. OPD's Scheduling Manager copies the shape but anchors to OPD footfall and has no cost figure yet (`opd.7.4.4#s17`). |
| Two separate role decisions, triggered and priced differently — don't collapse them | `dis.7.4.4#s2`; `bed.7.4.4#c1` | The identical instruction, in near-identical words, in two files. Neither is derived from the other in the text; treat `dis.7.4.4#s2` as the earlier statement. |
| The volume-sized Executive hire at ₹3–3.5 lakhs/year each | `dis.7.4.4#s5`, `dis.7.4.4#p2`, `dis.7.4.4#s6`, `dis.7.4.4#s7`, `dis.7.4.4#s9`; `bed.7.4.4#s2`, `bed.7.4.1#p7`, `bed.7.4.4#c6` | Discharge Executives and Admissions Executives are the same hire at the same price, sized by the same peak-load check. The sizing rules differ in form — a flat 15 discharges/day rule in Discharge, a 5-admissions-per-hour throughput plus a coverage floor in Bed. |
| Role-threshold tracking as its own KPI | `dis.8#k13`; `bed.8#k16` with its correction `bed.8#c1`; `opd.8#k15` | All three departments track their own hiring trigger as an operational metric. `bed.8#c1` records that the Bed version is stale against `bed.7.4.4`'s three current conditions — the one place this shared pattern is known to be out of date. |
| Head of Operations / COO approves the process flows, not daily tasks | `dis.7.4.3#s6`; `bed.7.4.3#c1` | Word-for-word the same governance point in two departments' key-people sections. |
| OPD prescription capture as the intake point for planned-admission data | `opd.2#a1`, `opd.7.4.1#s1`, `opd.7.4.2#s5`; `bed.7.4#s5`, `bed.7.4.2#s4`, `bed.8#k13` | OPD owns the capture activity and the bot that reads it. Bed consumes the same artefact as the start of its planned-admission pipeline and measures whether it arrives. The clearest OPD→Bed data dependency in the library, and it is stated only from each end, never as one edge. |
| The four-aspect solution shape and its mandatory cost-benefit and before/after graphic | `common.solution-method#s1`–`#s4`, `#n1`–`#n4`; `dis.7.4#s1`, `dis.7.4#s2`; `opd.7.4#n1`; `play.3#s1`, `play.3#s2` | Defined in common. Discharge restates it as its own requirement; OPD re-orders it (process and manpower first) without changing the set; the playbook turns the same four plus KPIs into the five clickable parts. |
| Whether the solution scales with hospital size | `dis.7.4#s3`; `common.solution-method#f1`; `bed.7.4#c1`, `bed.7.4#c2`, `bed.7.4#c3` | Discharge's finding is that the solution is size-invariant. `common.solution-method#f1` exists specifically to stop that being generalised, and `bed.7.4#c1` is the counter-case where the solution does scale. Three points, one argument — a retriever answering "does this hold for a smaller hospital?" needs all three. |
| Reserved capacity held vacant with a defined release rule | `bed.7.4#s8`, `bed.7.4.1#s5`, `bed.8#k5`; `opd.7.1.2#c12`, `opd.7.4.1#s3`, `opd.7.4.2#s7`, `opd.8#k6` | The emergency bed reserve and the STAT diagnostic slot are the same mechanism applied to different resources: hold capacity back, release it to the next queued case if the emergency does not arrive. OPD states the release rule precisely; Bed states the derivation (2–3 years of trend) precisely. Each is missing what the other has. |
| Flagging Tojo's own constructed numbers as constructions | `bed.7.4.1#c2`; `play.2#n1`, `play.0#n2`, `play.8#n1` | The playbook owns the rule; `bed.7.4.1#c2` is the only department file that states it independently, and adds the "don't carry figures across hospitals" half. |
| IT/HIS extraction and integration as a prerequisite | `bed.3#d7`, `bed.7.4.2#s6`, `bed.7.4.1#p9`; `dis.7.4.2#s3`, `dis.7.4.3#s1`; `opd.3#d9`, `opd.7.4.3#s14` | Each department names the same IT work — extend extraction to the records this department needs — as its own prerequisite and its own cost line. Bed is the most specific (IP records), Discharge the broadest (ERP, PACS, everything holding reports and notes). |
| Doctors as the concentrated point of resistance | `bed.7.4.3#c2`, `bed.7.4.3#s1`, `bed.7.4.3#s2`; `dis.7.4.3#s3`, `dis.7.4.3#s7`; `opd.7.4.3#s11`, `opd.7.4.3#s12`; `common.solution-method#s3`; `play.4#s4`, `play.4#s5` | Common defines buy-in as an aspect; each department names doctors as where it concentrates, and each proposes the same mitigation shape — make the doctor's own work lighter. OPD is the exception, where the resistance may be a financial incentive to refer outside rather than workload. |

## Points by file

### bed.points.md — Bed Management

## bed.1

| point | what it is | chunk | also called |
|---|---|---|---|
| bed.1#a1 | own and balance bed inventory — allocation, availability, turnover | bed.1 | who owns beds, bed inventory, who decides which bed |
| bed.1#a2 | right patient into the right bed at the right time | bed.1 | bed allocation, correct bed for the patient, patient placement |
| bed.1#a3 | keep occupancy maximised and ER/admission wait times minimised | bed.1 | occupancy, how long patients wait for a bed, casualty waiting |

## bed.2

| point | what it is | chunk | also called |
|---|---|---|---|
| bed.2#a1 | real-time bed status tracking — bed board, occupied/vacant/blocked/being cleaned | bed.2 | bed board, which beds are free right now, live bed status |
| bed.2#a2 | bed allocation for planned admissions | bed.2 | booking a bed for a scheduled patient, elective admission bed |
| bed.2#a3 | bed allocation for emergency/ER admissions | bed.2 | bed for a casualty case, emergency admission, ER bed |
| bed.2#a4 | processing admissions at the admission desk | bed.2 | admission desk, admission formalities, front desk |
| bed.2#a5 | internal bed transfers and reallocations | bed.2 | moving a patient to another bed, shifting patients, bed change |
| bed.2#a6 | ICU/step-down prioritisation and transfer coordination | bed.2 | who gets the ICU bed, shifting out of ICU, step-down |
| bed.2#a7 | ward-to-ward transfers — isolation, specialty-specific moves | bed.2 | isolation bed, moving to another ward, specialty ward |
| bed.2#a8 | coordination with Discharge for release timing | bed.2 | when will that bed free up, talking to discharge |
| bed.2#a9 | coordination with Housekeeping for turnaround/terminal cleaning | bed.2 | getting the bed cleaned, housekeeping, terminal cleaning |
| bed.2#a10 | overflow/surge management at high occupancy | bed.2 | hospital is full, surge, where do we put patients |
| bed.2#a11 | bed-blocking management — reserved/maintenance holds | bed.2 | blocked beds, beds held back, beds out of service |
| bed.2#a12 | predictive bed-demand forecasting from admissions, OT schedule, expected discharges | bed.2 | tomorrow's bed picture, how many beds will we need |
| bed.2#a13 | liaison with OT scheduling for post-op bed reservation | bed.2 | post-op bed, holding a bed for surgery, theatre list |
| bed.2#a14 | occupancy reporting to management | bed.2 | occupancy report, MIS to management, daily bed report |

## bed.3

| point | what it is | chunk | also called |
|---|---|---|---|
| bed.3#d1 | Discharge Process — timely bed release and accuracy of the release timing (Critical) | bed.3 | discharge is holding up beds, when patients actually leave |
| bed.3#d2 | Housekeeping — turnaround/cleaning speed (Critical) | bed.3 | cleaning delay, bed not cleaned yet, housekeeping slow |
| bed.3#d3 | Emergency/ER — unplanned demand spikes (Critical) | bed.3 | casualty rush, sudden admissions, ER surge |
| bed.3#d4 | ICU Step-Down Protocol — step-down timing frees ICU and ward beds (Critical) | bed.3 | ICU not clearing, step-down delay, ICU blocked |
| bed.3#d5 | Admission/Registration — accurate incoming demand signal (High) | bed.3 | how many admissions are coming, front office numbers |
| bed.3#d6 | OT Scheduling — post-op bed reservation needs (High) | bed.3 | surgery list, post-op beds, theatre planning |
| bed.3#d7 | IT/HIS — real-time, accurate bed-status system (High) | bed.3 | HIS, software showing wrong beds, system not updated |
| bed.3#d8 | ER holding/boarding time — direct gate (Critical) | bed.3 | patients stuck in casualty, ER boarding, holding area |
| bed.3#d9 | Admission Process — direct gate (Critical) | bed.3 | admissions held up, patient waiting to be admitted |
| bed.3#d10 | OT Scheduling — elective surgery can't be confirmed without a post-op bed (Critical) | bed.3 | surgery postponed for want of a bed, case cancelled |
| bed.3#d11 | Daily/aggregate Revenue — aggregate effect (Critical) | bed.3 | daily revenue, top line, collections |
| bed.3#d12 | ALOS — bed pressure drives discharge urgency (High) | bed.3 | average length of stay, patients staying too long |
| bed.3#d13 | Nursing workload distribution (Medium) | bed.3 | nurse workload, ward staffing, nurses overloaded |
| bed.3#d14 | Patient experience/satisfaction (Medium-High) | bed.3 | patient complaints, satisfaction scores, feedback |

## bed.4

| point | what it is | chunk | also called |
|---|---|---|---|
| bed.4#n1 | isolation/infection-control placement never overridden for convenience | bed.4 | isolation room, cross infection, infection control bed |
| bed.4#n2 | ICU bed prioritisation by clinical acuity never overridden administratively | bed.4 | who gets the ICU bed, VIP pressure, how sick the patient is |
| bed.4#n3 | a bed shown as available must actually be available — no phantom vacancies | bed.4 | system says free but it isn't, wrong bed status, stale entry |

## bed.5

| point | what it is | chunk | also called |
|---|---|---|---|
| bed.5#x1 | ward preference — private vs sharing — can be temporarily reassigned under pressure | bed.5 | private room not available, room category, shifting to sharing |
| bed.5#x2 | elective admission scheduling can shift by a day | bed.5 | postpone the admission, come tomorrow instead, reschedule |
| bed.5#x3 | specific bed number within the same clinical category is flexible | bed.5 | any bed in that ward, bed number change |

## bed.6

| point | what it is | chunk | also called |
|---|---|---|---|
| bed.6#f1 | manual/whiteboard bed tracking going stale | bed.6 | whiteboard, register, board not updated, excel sheet |
| bed.6#f2 | no predictive view of upcoming vacancies, so allocation stays reactive | bed.6 | we only know when it happens, no forward view, firefighting |
| bed.6#f3 | bed management run per-ward instead of as one hospital-wide view | bed.6 | each ward keeps its own beds, ward silos, no central view |
| bed.6#f4 | housekeeping turnaround lag — beds physically vacant but not usably available | bed.6 | bed is empty but not ready, waiting for cleaning |
| bed.6#f5 | the serialised shared team — discharges till 12–2 PM, then admissions at 4–8 PM | bed.6 | one team doing both, late admissions, evening admissions |
| bed.6#c1 | the loss starts at bill finalisation, not at physical vacancy | bed.6 | billing stops in the morning, unbilled hours, bed earning nothing |

## bed.7.1

| point | what it is | chunk | also called |
|---|---|---|---|
| bed.7.1#c1 | apply the shared Discharge/Bed/Admission/ALOS/Occupancy 8-point consideration set | bed.7.1 | the standard checks, the common list |
| bed.7.1#c2 | verify the hospital's actual Discharge TAT and actual discharge time, not reported | bed.7.1 | is the discharge time real, reported versus actual, take it at face value |
| bed.7.1#c3 | Housekeeping and Transport staffing ratio — peak-load capacity check | bed.7.1 | enough housekeeping staff, porters, cleaning staff per shift |
| bed.7.1#c4 | Admission TAT and its stage-by-stage timestamps | bed.7.1 | how long an admission takes, admission turnaround |
| bed.7.1#c5 | Bed-management/admissions team staffing ratio — peak-load capacity check | bed.7.1 | enough people on the admission desk, staffing at peak |
| bed.7.1#c6 | correct Discharge TAT definition — ends at the next admission into that bed | bed.7.1 | when does the clock stop, till the next patient comes in |
| bed.7.1#c7 | the TAT clock and the revenue clock are not the same clock | bed.7.1 | billing clock versus movement clock, two different timings |
| bed.7.1#c8 | stage — patient arrives, or Emergency prescribes admission | bed.7.1 | when the patient reached, when casualty said admit |
| bed.7.1#c9 | stage — documentation time taken | bed.7.1 | paperwork time, form filling, registration time |
| bed.7.1#c10 | stage — time the bed is allocated in the system | bed.7.1 | when the bed was given, allotment time |
| bed.7.1#c11 | stage — Ward/ICU team confirms the bed is actually ready | bed.7.1 | ward says bed is ready, confirmation from the floor |
| bed.7.1#c12 | stage — transport from Admission Desk or Emergency to the bed | bed.7.1 | shifting the patient up, trolley time, porter time |
| bed.7.1#c13 | throughput constraint — one person handles up to 5 admissions per hour | bed.7.1 | how many admissions one person can do, per-hour capacity |
| bed.7.1#c14 | coverage floor — 1 per shift to 250 beds; 2 morning, 2 evening, 1 night above | bed.7.1 | minimum staff per shift, how many at the desk at night |

## bed.7.2.1

| point | what it is | chunk | also called |
|---|---|---|---|
| bed.7.2.1#c1 | bed board / bed-status system access, to test whether vacancy is real | bed.7.2.1 | log in to the bed board, show us the system |
| bed.7.2.1#c2 | Housekeeping and Transport staff rosters per shift, against turnover volume | bed.7.2.1 | duty roster, who is on which shift, shift chart |
| bed.7.2.1#c3 | bed-management/admissions team roster per shift, against admissions and transfers | bed.7.2.1 | admission desk roster, shift-wise staff list |
| bed.7.2.1#c4 | stage-by-stage admission timestamps for the five stages, not a headline TAT | bed.7.2.1 | timings at every step, not just the total |
| bed.7.2.1#c5 | bill finalisation and bill initiation timestamps, per bed | bed.7.2.1 | when the bill closed, when the next bill opened on that bed |
| bed.7.2.1#c6 | bed-allocation, physical-admission and actual discharge timestamps for the same beds | bed.7.2.1 | allotment and admission times, the real discharge time |

## bed.7.2.2

| point | what it is | chunk | also called |
|---|---|---|---|
| bed.7.2.2#q1 | is any of Discharge, Admission or Bed Scheduling automated, or still whiteboard/spreadsheet | bed.7.2.2 | is it on software, are you still manual, excel |
| bed.7.2.2#q2 | is there a single named owner of Bed Management end-to-end | bed.7.2.2 | who is in charge of beds, one person responsible |
| bed.7.2.2#q3 | is OT Scheduling linked, and is elective-vs-ER admission priority defined | bed.7.2.2 | is the surgery list linked, who gets priority, walk-in versus planned |
| bed.7.2.2#q4 | is there a mechanism mapping planned admissions against provisional discharges and bed availability | bed.7.2.2 | tomorrow's plan, matching admissions to expected discharges |
| bed.7.2.2#q5 | is there the same mapping for predicted ICU requirement against step-down | bed.7.2.2 | ICU planning, will ICU beds free up, step-down forecast |
| bed.7.2.2#q6 | has housekeeping/transport staffing ever been calculated against volume, peak vs off-peak | bed.7.2.2 | has anyone actually counted, is staffing just assumed adequate |
| bed.7.2.2#q7 | does the reported Discharge TAT and discharge timing actually hold up | bed.7.2.2 | is the TAT genuine, fudged discharge time, does it include TPA |
| bed.7.2.2#q8 | same team doubling discharge and admission, or two completely separate teams | bed.7.2.2 | one team or two, who does admissions, same people |
| bed.7.2.2#q9 | has admissions per team member per hour at peak been calculated, including transfers | bed.7.2.2 | workload per person, have you measured it, headcount by habit |
| bed.7.2.2#q10 | is Admission TAT defined, and are its five stage timings actually available | bed.7.2.2 | do you have an admission TAT, stage-wise breakup |
| bed.7.2.2#q11 | when does billing on a bed stop and when does it restart, and the gap between | bed.7.2.2 | when the bill closes, when the next bill opens, has anyone looked |
| bed.7.2.2#c1 | a claimed overlap is a claim — test it against admission clock times | bed.7.2.2 | they say both run together, bed not allocated till confirmed ready |
| bed.7.2.2#c2 | where practice differs from what fast turnover requires, that gap is the diagnosis | bed.7.2.2 | what exactly is wrong, don't just say improve coordination |

## bed.7.3

| point | what it is | chunk | also called |
|---|---|---|---|
| bed.7.3#p1 | ARPOB and ALOS — the baseline financial parameters from the shared block | bed.7.3 | revenue per bed per day, average length of stay |
| bed.7.3#p2 | Bed Occupancy and ICU Occupancy — tracked separately, never blended | bed.7.3 | occupancy percentage, ICU occupancy, how full are we |
| bed.7.3#p3 | Daily Average Revenue | bed.7.3 | daily collection, revenue per day, top line |
| bed.7.3#p4 | OT Utilisation and OT Revenue (daily) | bed.7.3 | theatre utilisation, OT revenue, surgeries per day |
| bed.7.3#p5 | dead bed time — outgoing patient's bill finalisation to incoming patient's bill initiation | bed.7.3 | bed earning nothing, idle bed, unbilled hours, dead bed days |
| bed.7.3#p6 | revenue foregone from admissions not captured — diverted, turned away, postponed | bed.7.3 | patients we turned away, lost admissions, cases postponed |
| bed.7.3#p7 | HR cost for Housekeeping and Transport, broken out separately | bed.7.3 | housekeeping salary cost, porter cost, manpower line |
| bed.7.3#p8 | HR cost for the bed-management/admissions team, and Bed Manager salary cost | bed.7.3 | admission desk salary cost, what a bed manager costs |

## bed.7.4

| point | what it is | chunk | also called |
|---|---|---|---|
| bed.7.4#c1 | the solution itself scales — it does not stay constant as in Discharge | bed.7.4 | does the same answer apply to a small hospital |
| bed.7.4#c2 | the scaling pivot — monthly-average daily admissions against last night's available beds | bed.7.4 | are beds actually short, demand versus supply |
| bed.7.4#c3 | below the pivot recommend the reduced form and say plainly it is the reduced form | bed.7.4 | the smaller version, lighter option, can't justify the full thing |
| bed.7.4#s1 | a single named owner of bed management end-to-end — holds at any size | bed.7.4 | one person in charge of beds |
| bed.7.4#s2 | some real mapping of planned admissions against provisional discharges existing at all | bed.7.4 | a proper plan for tomorrow's beds, not assembled informally |
| bed.7.4#s3 | provisional discharge and provisional step-down as formally tracked concepts | bed.7.4 | likely discharges recorded, expected step-downs |
| bed.7.4#s4 | admissions and discharges not being run serially by one team | bed.7.4 | stop doing discharges first then admissions, costs nothing to fix |
| bed.7.4#s5 | OPD prescription capture as the intake point for planned-admission data | bed.7.4 | capture the OPD prescription, where admission data starts |
| bed.7.4#s6 | the Discharge-linkage double control | bed.7.4 | cross-check discharge's timings against our own |
| bed.7.4#s7 | mapping cadence — twice daily, or a single daily pass below the pivot | bed.7.4 | how often we do the bed round, once or twice a day |
| bed.7.4#s8 | emergency bed reserve — needs 2–3 years history, only bites where capacity is scarce | bed.7.4 | beds kept aside for emergencies, reserve beds |
| bed.7.4#s9 | predictive LOS modelling depth — coarser by department at lower volumes | bed.7.4 | how detailed the LOS prediction is, enough cases to trend |
| bed.7.4#s10 | ICU mapping — only where there is a real ICU and a real step-down queue | bed.7.4 | separate ICU planning, do we need an ICU pass |
| bed.7.4#s11 | admissions-desk live link — a disciplined manual confirm-back below the pivot | bed.7.4 | live link to the desk, or just phone and confirm |
| bed.7.4#s12 | the dedicated Bed Manager hire — condition-triggered, the pivot is one trigger | bed.7.4 | do we need a bed manager |

## bed.7.4.1

| point | what it is | chunk | also called |
|---|---|---|---|
| bed.7.4.1#s1 | core capability — real-time visibility of the next day's bed picture | bed.7.4.1 | tomorrow's bed position, forward view, before it becomes a crisis |
| bed.7.4.1#s2 | (a) planned-admission-to-bed mapping, including predictive LOS-based vacancies | bed.7.4.1 | matching planned admissions to beds, who is likely to go home |
| bed.7.4.1#s3 | (b) the same mapping run for ICU beds and probable step-downs | bed.7.4.1 | ICU bed mapping, step-down prediction, intensivist confirmation |
| bed.7.4.1#s4 | (c) Discharge-process linkage as a double control | bed.7.4.1 | linking discharge and beds, each checks the other |
| bed.7.4.1#s5 | (d) emergency bed reserve, derived from 2–3 years of trend analysis | bed.7.4.1 | beds held for emergency, how many to keep back |
| bed.7.4.1#s6 | (e) admission call-in timing — work backwards and tell each patient when to come | bed.7.4.1 | when to call the patient in, calling patients earlier |
| bed.7.4.1#s7 | daily cadence — first mapping pass by 2 PM, final freeze by 6 PM | bed.7.4.1 | the 2 o'clock mapping, the 6 o'clock freeze |
| bed.7.4.1#c1 | occupancy gain must not be presented as this department's benefit | bed.7.4.1 | will occupancy go up, what is the benefit exactly |
| bed.7.4.1#c2 | derive magnitudes from this hospital's own numbers; flag Tojo's own constructions | bed.7.4.1 | are these our numbers or yours, don't carry figures across |
| bed.7.4.1#p1 | Admission TAT compressed to barely under 30 minutes | bed.7.4.1 | admission in half an hour, target admission time |
| bed.7.4.1#p2 | billing brought forward — admissions by ~12 PM instead of the 4–8 PM window | bed.7.4.1 | start billing earlier, admit before noon, extra billable hours |
| bed.7.4.1#p3 | dead bed time eliminated — quantified as one number, bill to bill | bed.7.4.1 | removing the idle bed stretch, first one to measure it |
| bed.7.4.1#p4 | ALOS reduction and earlier procedure scheduling — count the effect once | bed.7.4.1 | length of stay comes down, surgeries scheduled earlier |
| bed.7.4.1#p5 | manpower — workload relief rather than headcount reduction | bed.7.4.1 | will we save staff, headcount saving, settles at the floor |
| bed.7.4.1#p6 | Bed Manager at ₹4–4.5 lakhs/year where §7.4.4's conditions are met | bed.7.4.1 | bed manager salary, what the role costs |
| bed.7.4.1#p7 | Admissions Executives at ₹3–3.5 lakhs/year each where the ratio-check shows a shortfall | bed.7.4.1 | admission staff salary, cost per executive |
| bed.7.4.1#p8 | housekeeping/transport headcount where §7.1 point 3's check shows one | bed.7.4.1 | extra housekeeping cost, more porters |
| bed.7.4.1#p9 | automation/integration cost, including §7.4.2's IT extraction work | bed.7.4.1 | software cost, IT cost, integration spend |

## bed.7.4.2

| point | what it is | chunk | also called |
|---|---|---|---|
| bed.7.4.2#s1 | admissions and discharges stop being run serially by one team | bed.7.4.2 | split the team, overlap the two windows, no direct cost |
| bed.7.4.2#s2 | Discharge Process must actually be automated, or its logic replicated | bed.7.4.2 | fix discharge first, it's a prerequisite not a separate rollout |
| bed.7.4.2#s3 | provisional discharge 24 hours in advance; ICU step-down signal by 1 PM | bed.7.4.2 | tell us a day ahead, ICU by one o'clock |
| bed.7.4.2#s4 | OPD prescriptions become the intake point for planned-admission data | bed.7.4.2 | capture from the OPD slip, date procedure and expected stay |
| bed.7.4.2#s5 | Medical Supervisory rounds get a fixed checkpoint, latest by 5 PM | bed.7.4.2 | evening rounds, confirm discharges by five |
| bed.7.4.2#s6 | IT must extend extraction to IP records specifically | bed.7.4.2 | pull inpatient data, not just admission and discharge logs |
| bed.7.4.2#s7 | admission stage timestamps captured as a matter of course | bed.7.4.2 | record the timing at each stage, not just the total |
| bed.7.4.2#s8 | bill-close and bill-open timestamps held against the bed, not just the patient | bed.7.4.2 | join billing to the bed, it's a reporting change |
| bed.7.4.2#s9 | admissions desk gets a two-way live link to the Bed Management console | bed.7.4.2 | desk and console talking live, tentative bed number attached |

## bed.7.4.3

| point | what it is | chunk | also called |
|---|---|---|---|
| bed.7.4.3#d1 | teams whose cooperation is required, Billing included | bed.7.4.3 | who all needs to be on board, which departments |
| bed.7.4.3#c1 | Head of Operations / COO approves the process flows, not daily tasks | bed.7.4.3 | who signs off, the COO's role, escalation level |
| bed.7.4.3#c2 | resistance concentrates in the doctors; making their life easier is the design constraint | bed.7.4.3 | doctors won't agree, clinical pushback, more work for consultants |
| bed.7.4.3#s1 | doctors record observations verbally on rounds | bed.7.4.3 | doctors speak their notes, voice capture on rounds |
| bed.7.4.3#s2 | agent hands doctors a predictive model and summary for every patient on rounds | bed.7.4.3 | ready-made summary for the doctor, LOS benchmark per patient |

## bed.7.4.4

| point | what it is | chunk | also called |
|---|---|---|---|
| bed.7.4.4#c1 | two separate role decisions, triggered and priced differently — don't collapse them | bed.7.4.4 | one hire or two, don't lump them together |
| bed.7.4.4#s1 | (a) dedicated Bed Manager owning bed scheduling end-to-end, ₹4–4.5 lakhs/year | bed.7.4.4 | do we need a bed manager, peer of the discharge manager |
| bed.7.4.4#c2 | trigger — demand exceeds supply: daily admissions over last night's available beds | bed.7.4.4 | are we genuinely short of beds, the primary trigger |
| bed.7.4.4#c3 | trigger — occupancy above 80% | bed.7.4.4 | we're running at eighty-five percent |
| bed.7.4.4#c4 | trigger — sustained TAT breach, e.g. over 50% of admissions overrunning expected TAT | bed.7.4.4 | admissions keep taking too long, we always overrun |
| bed.7.4.4#c5 | below all three conditions, frame the hire as future efficiency and stress reduction | bed.7.4.4 | not justified yet, nice to have, reduces the team's load |
| bed.7.4.4#s2 | (b) Admissions Executives — volume-sized, ₹3–3.5 lakhs/year each | bed.7.4.4 | how many admission staff do we need, cost per person |
| bed.7.4.4#c6 | take whichever constraint fails first at peak; the coverage floor is not the answer alone | bed.7.4.4 | minimum per shift isn't enough, admissions cluster at peak |
| bed.7.4.4#s3 | (c) everything else is scope-augmentation, not headcount | bed.7.4.4 | existing staff do a bit more, no new hires there |

## bed.8

| point | what it is | chunk | also called |
|---|---|---|---|
| bed.8#k1 | % of planned admissions mapped to a bed by the 6 PM final freeze | bed.8 | did every planned admission get a bed, unmapped admissions |
| bed.8#k2 | % of 2 PM provisional mappings that hold unchanged through to the 6 PM freeze | bed.8 | how stable the afternoon plan is, does the plan change by evening |
| bed.8#k3 | % of ICU requirements unmapped at the 6 PM freeze | bed.8 | ICU shortfall, ICU cases with no bed |
| bed.8#k4 | predicted vs. actual LOS accuracy, by treatment/procedure type | bed.8 | is the stay prediction right, LOS estimate drift |
| bed.8#k5 | emergency bed reserve adequacy against actual same-day emergency demand | bed.8 | did we keep enough emergency beds, reserve ran out |
| bed.8#k6 | bed turnaround time — physical discharge to usably-available bed | bed.8 | how long a bed sits empty, cleaning delay, gap between patients |
| bed.8#k7 | ER/admission wait or boarding time | bed.8 | how long casualty patients wait, boarding in the ER |
| bed.8#k8 | Bed Occupancy and ICU Occupancy tracked as ongoing KPIs | bed.8 | occupancy percentage, how full are we, ICU occupancy |
| bed.8#k9 | ALOS | bed.8 | average length of stay, how long patients stay |
| bed.8#k10 | % of ward patients with a provisional discharge signal a full 24 hours in advance | bed.8 | do we get a day's notice, advance discharge intimation |
| bed.8#k11 | % of ICU patients with a provisional step-down signal given by 1 PM | bed.8 | step-down told by one o'clock, ICU intimation on time |
| bed.8#k12 | % of Medical Supervisory 5 PM rounds completed on schedule | bed.8 | are the evening rounds actually happening |
| bed.8#k13 | % of planned admissions with OPD-prescription-captured intake data available | bed.8 | is the OPD data coming through, intake capture |
| bed.8#k14 | Admissions-desk-to-Bed-Management console sync accuracy | bed.8 | does the desk booking show up in the console, live link working |
| bed.8#k15 | Daily/aggregate revenue attributable to bed-management efficiency | bed.8 | revenue from better bed handling, what it earned us |
| bed.8#k16 | Bed Manager threshold tracking — occupancy % and admissions/day against the trigger | bed.8 | are we past the bed manager trigger, when do we hire |
| bed.8#k17 | housekeeping/transport staff available per shift per bed, for admissions and discharges | bed.8 | cleaning and porter staffing per shift, staff per bed |
| bed.8#k18 | nursing workload distribution relative to occupancy/turnover volume | bed.8 | nurse workload versus occupancy, ward staffing balance |
| bed.8#c1 | #16 is now wrong — it must track §7.4.4's three current Bed Manager conditions | bed.8 | the hiring trigger changed, KPI is out of date |
| bed.8#c2 | Admission TAT needs KPIs — the headline against 30 minutes, plus five stage timings | bed.8 | no KPI for admission time, stage-wise tracking missing |
| bed.8#c3 | dead bed time needs a KPI, bill to bill, with its three stretches separable | bed.8 | nobody tracks the idle bed hours, needs its own number |
| bed.8#c4 | the bed-management/admissions team ratio needs a KPI, peak vs off-peak | bed.8 | no KPI for desk workload, admissions plus transfers per person |

### dis.points.md — Discharge Process

## dis.1

| point | what it is | chunk | also called |
|---|---|---|---|
| dis.1#a1 | clinical discharge decision to bed available again, one coordinated process | dis.1 | what discharge covers, where discharge starts and ends, end-to-end ownership |
| dis.1#a2 | clinical sign-off | dis.1 | doctor signing off, getting the doctor to clear the patient |
| dis.1#a3 | billing closure | dis.1 | closing the bill, finalising the bill |
| dis.1#a4 | insurance clearance | dis.1 | TPA clearance, getting insurance approval |
| dis.1#a5 | family/logistics | dis.1 | telling the family, arranging the patient's exit |

## dis.2

| point | what it is | chunk | also called |
|---|---|---|---|
| dis.2#a1 | discharge planning / early flagging of likely-discharge patients | dis.2 | knowing in advance who's going home, flagging discharges early |
| dis.2#a2 | doctor's discharge order and discharge summary | dis.2 | discharge order, writing the summary, DS |
| dis.2#a3 | nursing stock-take of medicines/consumables | dis.2 | counting leftover medicines, ward stock reconciliation |
| dis.2#a4 | billing finalization of investigations and billable items | dis.2 | closing the bill, final bill preparation |
| dis.2#a5 | insurance/TPA document compilation, submission and approval | dis.2 | TPA file, sending papers to insurance, approval wait |
| dis.2#a6 | pharmacy returns processing | dis.2 | returning unused medicines, medicine refund |
| dis.2#a7 | family/patient briefing on diet, medication, follow-up | dis.2 | discharge counselling, explaining medicines to the family |
| dis.2#a8 | final payment collection and clearance | dis.2 | settling the bill, cash counter clearance |
| dis.2#a9 | bed turnover handoff to housekeeping | dis.2 | telling housekeeping to clean the bed, bed cleaning handover |
| dis.2#a10 | physical discharge and transport out | dis.2 | wheelchair out, patient actually leaving, shifting to the car |

## dis.3

| point | what it is | chunk | also called |
|---|---|---|---|
| dis.3#d1 | Nursing Team — stock reconciliation, ward readiness (High) | dis.3 | what we need from nursing, ward nurses holding up discharge |
| dis.3#d2 | Doctor Team incl. transcriptionist — discharge order and summary originate here (Critical) | dis.3 | waiting on the doctor, summary not written, transcriptionist delay |
| dis.3#d3 | Billing Team — sign-off on chargeables, reconciliation, handoff to insurance (High) | dis.3 | billing taking too long, final bill delay |
| dis.3#d4 | Dietitian Team — diet-related briefing before discharge (Medium) | dis.3 | diet advice before going home, dietitian visit |
| dis.3#d5 | Housekeeping Team — bed prepared again for next admission (High) | dis.3 | bed cleaning, room not ready |
| dis.3#d6 | Transport Team — wheelchair/stretcher to move patient out (Medium-High) | dis.3 | no wheelchair available, patient waiting to be shifted |
| dis.3#d7 | ALOS — avoidable discharge time is added stay (Critical) | dis.3 | length of stay, patients staying longer than needed |
| dis.3#d8 | ARPOB — faster discharge protects realized revenue per bed (High) | dis.3 | revenue per bed, earning per occupied bed |
| dis.3#d9 | ICU Step-Down Protocol & ICU bed availability (Critical) | dis.3 | ICU beds blocked, can't move patients out of ICU |
| dis.3#d10 | Bed Availability for Admission, including ER (Critical) | dis.3 | no beds for new patients, ER patients waiting |
| dis.3#d11 | OT Scheduling — same-night slots if admissions land before 10 AM (High) | dis.3 | booking surgeries, same-day OT slots, 10 AM admission cut-off |
| dis.3#d12 | OT Utilisation — late-night slots for same-morning admissions (High) | dis.3 | how full our OTs are, empty OT slots |
| dis.3#d13 | OT Revenue — follows from OT scheduling/utilisation (High) | dis.3 | surgery income, OT earnings |
| dis.3#d14 | Daily Revenue — aggregate effect of all of the above (Critical) | dis.3 | day's collection, top line |

## dis.4

| point | what it is | chunk | also called |
|---|---|---|---|
| dis.4#n1 | clinical accuracy of discharge summary never sacrificed for speed | dis.4 | summary must be correct, don't rush the summary |
| dis.4#n2 | no billing errors introduced by rushing | dis.4 | wrong bill, billing mistakes from hurrying |
| dis.4#n3 | safety and medication instructions always delivered before physical discharge | dis.4 | family must be counselled, medicine instructions before they leave |

## dis.5

| point | what it is | chunk | also called |
|---|---|---|---|
| dis.5#x1 | stock-take vs. billing prep can run in parallel, not strict order | dis.5 | doing stock count and billing together, overlapping steps |
| dis.5#x2 | family briefing timing can flex if everything else is ready | dis.5 | counselling can happen later, brief them while paperwork moves |
| dis.5#x3 | non-critical documentation can trail the actual discharge briefly | dis.5 | paperwork can finish after the patient leaves |

## dis.6

| point | what it is | chunk | also called |
|---|---|---|---|
| dis.6#f1 | sequential, non-overlapping processing — nothing starts till previous step finishes | dis.6 | one thing at a time, everything waits in a queue |
| dis.6#f2 | manual handoffs losing time at every stage | dis.6 | files moving by hand, paper going desk to desk |
| dis.6#f3 | no predictive flagging — nothing starts until the doctor's order lands | dis.6 | we only know at the last minute, no advance warning |
| dis.6#f4 | no single owner, so delays attributed to "the process" | dis.6 | nobody's accountable, everyone blames the system |
| dis.6#f5 | one team doing both discharge and admissions, serialised, pushing admissions to 4–8 PM | dis.6 | same team does both, admissions only start after lunch, evening admissions |

## dis.7

Section container (heading only) — no points.

## dis.7.1

| point | what it is | chunk | also called |
|---|---|---|---|
| dis.7.1#c1 | shared Discharge/Bed/Admission/ALOS/Occupancy 8-point consideration set applies | dis.7.1 | how urgent is this for us, are we at 60% or 95% occupancy |
| dis.7.1#c2 | nursing and discharge-coordination staffing ratio, peak-load capacity check | dis.7.1 | do the nurses have time for this, is the ward short-staffed for discharges |
| dis.7.1#c3 | housekeeping and transport turnaround capacity per shift vs. volume | dis.7.1 | enough housekeeping staff, enough wheelchairs and porters |

## dis.7.2

| point | what it is | chunk | also called |
|---|---|---|---|
| dis.7.2#d1 | nursing roster and shift structure, plus timestamped daily discharge volume | dis.7.2 | nursing duty roster, how many discharges a day and at what time |
| dis.7.2#d2 | housekeeping and transport staff rosters per shift vs. actual volume | dis.7.2 | housekeeping shift chart, porter duty list |
| dis.7.2#d3 | billing sign-off and insurance/TPA handoff logs | dis.7.2 | billing system records, when the file went to TPA |
| dis.7.2#d4 | bed-allocation and physical-admission timestamps for the same bed | dis.7.2 | when the bed was given to the next patient, HIS bed log |
| dis.7.2#d5 | insurance/TPA correspondence timestamps — first request sent, final approval | dis.7.2 | when we asked the insurer, when approval came back |

## dis.7.2.1

| point | what it is | chunk | also called |
|---|---|---|---|
| dis.7.2.1#q1 | do doctors make a primary discharge call on evening rounds or only next morning | dis.7.2.1 | evening round decision, do they decide the night before |
| dis.7.2.1#q2 | what time discharge is typically confirmed | dis.7.2.1 | when does the doctor confirm, what time discharges get cleared |
| dis.7.2.1#q3 | do nursing/billing wait for all rounds to finish or start on flagging | dis.7.2.1 | do they wait for the full round, can they start patient by patient |
| dis.7.2.1#q4 | when documents are sent to doctors to prepare discharge summaries | dis.7.2.1 | when the file goes to the doctor for the summary |
| dis.7.2.1#q5 | who prepares the discharge summary — attending, transcriptionist, or junior-review chain | dis.7.2.1 | who writes the summary, does the consultant type it himself |
| dis.7.2.1#q6 | for multidisciplinary cases, who owns preparing and approving the summary | dis.7.2.1 | multiple doctors on one case, who signs the summary |
| dis.7.2.1#q7 | will doctors sign off on evening rounds for non-insurance patients, for 10 AM discharge | dis.7.2.1 | evening sign-off for cash patients, getting them out by 10 in the morning |
| dis.7.2.1#q8 | how long Billing actually takes to sign off, reconcile and hand off to insurance | dis.7.2.1 | real billing turnaround, how long the final bill actually takes |
| dis.7.2.1#q9 | is there a single point of ownership for the entire discharge process | dis.7.2.1 | who owns discharge, is anyone accountable end to end |
| dis.7.2.1#q10 | what level of automation is already built into their current process | dis.7.2.1 | what software do they already have, is any of this automated |
| dis.7.2.1#q11 | does anyone track discharges handled per staff per shift, or is staffing assumed adequate | dis.7.2.1 | has anyone ever counted the workload per nurse, is staffing just assumed fine |
| dis.7.2.1#q12 | is bed-turnaround time or transport availability tracked as its own metric | dis.7.2.1 | do we measure bed cleaning time separately, is the wheelchair wait tracked |
| dis.7.2.1#q13 | average admission time — bed allocation and physical admission — vs. discharge time | dis.7.2.1 | what time patients actually come in, the gap between one patient leaving and the next arriving, 30-minute gap |
| dis.7.2.1#q14 | cross-verify the hospital's reported Discharge TAT against three checks | dis.7.2.1 | is their TAT figure real, does the TAT include the insurance wait, where does their clock start |
| dis.7.2.1#q15 | correct Discharge TAT definition — ends at next patient's admission into that bed; check above 80% occupancy | dis.7.2.1 | what should TAT actually measure, measuring till the next patient comes in |
| dis.7.2.1#c1 | revenue clock stops earlier, at bill finalisation — the discharge tail sits inside dead bed time | dis.7.2.1 | when does the bed stop earning, dead bed time, good TAT but no revenue |
| dis.7.2.1#q16 | does one team double as discharge and admissions, or two separate teams | dis.7.2.1 | same team for both, do they do admissions only after discharges |

## dis.7.3

| point | what it is | chunk | also called |
|---|---|---|---|
| dis.7.3#p1 | ARPOB | dis.7.3 | revenue per occupied bed per day, earning per bed |
| dis.7.3#p2 | Daily Average Revenue | dis.7.3 | daily collection, average day's business |
| dis.7.3#p3 | OT Utilisation | dis.7.3 | how full the OTs run, theatre usage |
| dis.7.3#p4 | OT Revenue (daily) | dis.7.3 | surgery income per day, theatre earnings |
| dis.7.3#p5 | ICU Occupancy | dis.7.3 | how full the ICU is, ICU beds occupied |
| dis.7.3#p6 | Bed Occupancy | dis.7.3 | occupancy percentage, how full the hospital is |

## dis.7.4

| point | what it is | chunk | also called |
|---|---|---|---|
| dis.7.4#s1 | mandatory cost-benefit analysis plus side-by-side graphical before/after comparison | dis.7.4 | show me the numbers, what it costs vs what it saves, before and after picture |
| dis.7.4#s2 | the four-aspect solution shape | dis.7.4 | the four parts of the answer, standard solution format |
| dis.7.4#s3 | solution identical at any size or occupancy; only cost justification varies | dis.7.4 | same fix for every hospital, is it worth it for us right now |
| dis.7.4#s4 | worked example — dedicated Discharge Manager, same recommendation at any occupancy | dis.7.4 | hiring someone to own discharge, a discharge in-charge |
| dis.7.4#s5 | earlier discharge times — 11 AM for cash patients, 1 PM for insured | dis.7.4 | getting cash patients out by 11, insured by 1 o'clock |
| dis.7.4#s6 | 6–8 hours saved and ~0.5-day ALOS reduction justify the headcount at 95% | dis.7.4 | how many hours we save, half a day off length of stay |

## dis.7.4.1

| point | what it is | chunk | also called |
|---|---|---|---|
| dis.7.4.1#s1 | on any provisional mention of discharge, system assembles full summary and seeks approval | dis.7.4.1 | summary ready the moment the doctor says it, auto-generated discharge summary |
| dis.7.4.1#s2 | system continuously reads and logs clinical/operational events from admission onward | dis.7.4.1 | recording everything as it happens, no back-filling at discharge |
| dis.7.4.1#s3 | (a) history, symptoms, prognosis, diagnosis at admission | dis.7.4.1 | admission notes, what he came in with |
| dis.7.4.1#s4 | (b) all investigations and summarised findings, especially abnormalities | dis.7.4.1 | test reports, lab and scan findings |
| dis.7.4.1#s5 | (c) all procedures and surgeries done, with notes | dis.7.4.1 | operation notes, what procedures were done |
| dis.7.4.1#s6 | (d) medications prescribed/administered/changed, consumed vs. remaining by strip or bottle | dis.7.4.1 | medicine chart, what's left to return to pharmacy |
| dis.7.4.1#s7 | (e) consumables requisitioned, used and remaining balance, returnable in whole units | dis.7.4.1 | unused consumables, what can go back to stores |
| dis.7.4.1#s8 | (f) doctor's daily progress observations | dis.7.4.1 | daily progress notes, doctor's rounds notes |
| dis.7.4.1#s9 | (g) reasons behind every investigation, procedure, management step, prescription, and outcome | dis.7.4.1 | why each test was ordered, the reasoning and the result |
| dis.7.4.1#s10 | costs assigned per event from the ERP; bill auto-finalises when discharge is confirmed | dis.7.4.1 | running bill always ready, bill closes by itself |
| dis.7.4.1#s11 | for provisional discharge, costs and returns projected the evening before | dis.7.4.1 | tentative bill ready the night before, billing checks it first thing |
| dis.7.4.1#s12 | nursing stock-take stops gating billing — expected returns computed from event log | dis.7.4.1 | billing no longer waits for the nurses' count |
| dis.7.4.1#s13 | provisional bill goes to Insurance/TPA the same evening for primary approval | dis.7.4.1 | starting the TPA approval the night before |
| dis.7.4.1#s14 | on confirmation, final bill with reports and summary goes to Insurance immediately | dis.7.4.1 | final file to insurance automatically, no delay in submission |
| dis.7.4.1#s15 | for cash patients, provisional and final bills go straight to patient/family | dis.7.4.1 | cash patients get the bill directly, no TPA step |
| dis.7.4.1#s16 | doctor reviews and signs the final summary digitally on mobile/tablet | dis.7.4.1 | doctor signs on his phone, digital sign-off |
| dis.7.4.1#s17 | end state — bills go direct to insurer or family without manual cross-checking | dis.7.4.1 | no manual checking at all, once we trust the system |
| dis.7.4.1#p1 | time saved: 6–8 hours | dis.7.4.1 | how many hours we'd save per discharge |
| dis.7.4.1#p2 | revenue prorated as ARPOB × No. of Beds × 365 days | dis.7.4.1 | what the freed bed-days are worth a year, annualised revenue potential |
| dis.7.4.1#p3 | manpower savings — entire Insurance/TPA workload, reduced Billing headcount | dis.7.4.1 | how many staff we'd save, can we cut the TPA desk |

## dis.7.4.2

| point | what it is | chunk | also called |
|---|---|---|---|
| dis.7.4.2#s1 | underlying process stays the same — an automation layer, not a redesign | dis.7.4.2 | we're not changing how we work, just adding a layer |
| dis.7.4.2#s2 | team members onboarded to approve and access the agents as part of their role | dis.7.4.2 | staff approving on screen instead of doing it by hand, training the team |
| dis.7.4.2#s3 | IT must let agents extract from ERP, PACS and every system holding reports and notes | dis.7.4.2 | system integration, connecting to our HIS and PACS, IT prerequisite |
| dis.7.4.2#s4 | positioning — agent starts as extension of each job, replaces parts only later | dis.7.4.2 | how we sell it to staff, it's not taking your job |
| dis.7.4.2#s5 | Bed Management and other downstream functions check the agent's output directly | dis.7.4.2 | bed team reading the discharge system, until they're automated too |
| dis.7.4.2#s6 | Dietitian, Pharmacy, Housekeeping, Transport watch agent updates for when to act | dis.7.4.2 | alerting housekeeping and porters, who gets pinged when |
| dis.7.4.2#s7 | break the serialised shared team — separate the roles or overlap the two windows | dis.7.4.2 | stop doing admissions after discharges, run both together, split the teams |
| dis.7.4.2#s8 | Bed Management must produce accurate real-time bed-allocation and admission timestamps | dis.7.4.2 | logging when the bed was given and when the patient came in, real timings not reported ones |

## dis.7.4.3

| point | what it is | chunk | also called |
|---|---|---|---|
| dis.7.4.3#s1 | IT — integration | dis.7.4.3 | our IT team, systems people |
| dis.7.4.3#s2 | Diagnostic & Investigation teams — capturing events, updating reports on time | dis.7.4.3 | lab and radiology, getting reports uploaded on time |
| dis.7.4.3#s3 | Doctors — provisional discharge, real-time mobile approval, voice-command recording | dis.7.4.3 | getting consultants on board, doctors dictating notes, approving on the phone |
| dis.7.4.3#s4 | Nursing — real-time approval of captured notes and on-floor changes | dis.7.4.3 | nurses verifying what the system picked up |
| dis.7.4.3#s5 | Billing, Insurance/TPA, Admissions, Housekeeping, Dietitian, Ward Manager cooperation | dis.7.4.3 | the other departments we need on board |
| dis.7.4.3#s6 | Head of Operations / COO approves the process flows, not daily tasks | dis.7.4.3 | COO sign-off, who authorises this between departments |
| dis.7.4.3#s7 | buy-in mechanism — extension of the role first, headcount reduction later | dis.7.4.3 | how we get them to accept it, don't lead with job cuts |

## dis.7.4.4

| point | what it is | chunk | also called |
|---|---|---|---|
| dis.7.4.4#s1 | every team sees modest scope expansion — recording and approving in the system | dis.7.4.4 | small addition to everyone's job, extra steps for the staff |
| dis.7.4.4#s2 | two separate role decisions, triggered and priced differently — don't collapse them | dis.7.4.4 | two different hires, not one person for both |
| dis.7.4.4#s3 | Discharge Manager — owns the process end-to-end, single point of contact, Bed Manager's peer | dis.7.4.4 | a discharge in-charge, one person who owns discharge |
| dis.7.4.4#p1 | Discharge Manager cost — ₹4–4.5 lakhs/year | dis.7.4.4 | what that manager costs us, the salary |
| dis.7.4.4#s4 | Manager triggers — >80% occupancy, >40 discharges/day, or continual TAT overrun | dis.7.4.4 | when do we need this role, at what occupancy is it worth it |
| dis.7.4.4#s5 | Discharge Executives — processing layer, own each discharge from provisional signal | dis.7.4.4 | discharge coordinators, the people who actually chase each case |
| dis.7.4.4#p2 | Discharge Executive cost — ₹3–3.5 lakhs/year each | dis.7.4.4 | what each coordinator costs, their salary |
| dis.7.4.4#s6 | sizing at roughly 15 discharges/day per person — a flat rule to be ratio-checked | dis.7.4.4 | one person per 15 discharges, the thumb rule |
| dis.7.4.4#s7 | worked example — 40–45 discharges/day clustering into 8–11 AM and 6–9 PM windows, 2 Executives | dis.7.4.4 | two busy periods, morning and evening rush, one person per shift |
| dis.7.4.4#p3 | worked example combined cost — roughly ₹6–7 lakhs/year | dis.7.4.4 | total cost of the two coordinators |
| dis.7.4.4#s8 | same hospital also crosses the Manager condition — one Manager plus two Executives | dis.7.4.4 | we need both, a manager and two coordinators |
| dis.7.4.4#s9 | headcount is specific to that hospital's shift/volume pattern — re-run the ratio-check | dis.7.4.4 | don't copy the number, work it out for our own hospital |

## dis.8

| point | what it is | chunk | also called |
|---|---|---|---|
| dis.8#k1 | discharge-order-to-physical-discharge cycle time | dis.8 | how long discharge takes, discharge TAT, time from order to patient leaving |
| dis.8#k2 | % non-insurance discharges by 10 AM, % insured discharges by 1 PM | dis.8 | how many go out by 10, morning discharge percentage, cash vs insured timing |
| dis.8#k3 | % discharges triggered by provisional evening-round mention vs. same-day-only order | dis.8 | how many are decided the night before, advance flagging rate |
| dis.8#k4 | bed turnaround time — physical discharge to bed usably available | dis.8 | how long the bed sits empty, bed cleaning time, time to next admission |
| dis.8#k5 | ALOS contribution from discharge delay specifically | dis.8 | how much of the stay is our delay, avoidable extra days |
| dis.8#k6 | % discharges where nursing stock-take is no longer a gating step | dis.8 | how often billing didn't wait for the ward count |
| dis.8#k7 | billing finalization turnaround from discharge order to bill finalized | dis.8 | how long billing takes, final bill time |
| dis.8#k8 | insurance/TPA approval turnaround, provisional and final tracked separately | dis.8 | how long the insurer takes, TPA approval time |
| dis.8#k9 | % bills going straight to insurer or family without manual cross-checking | dis.8 | how much goes out untouched, trust level in the system |
| dis.8#k10 | ARPOB and Daily Average Revenue tracked as ongoing KPIs | dis.8 | revenue per bed, daily collection |
| dis.8#k11 | OT Utilisation and OT Revenue from slots freed by faster discharge | dis.8 | extra surgeries we got, theatre usage from early discharge |
| dis.8#k12 | realized vs. theoretical revenue impact of freed bed-days | dis.8 | how much of the projected gain we actually got |
| dis.8#k13 | role threshold tracking — occupancy %, discharges/day, TAT-overrun proportion | dis.8 | are we past the threshold for hiring, do we qualify for a discharge manager |
| dis.8#k14 | nursing ratio per bed for discharge functions, discharges per staff per hour peak vs off-peak | dis.8 | workload per nurse, how many discharges one person handles |
| dis.8#k15 | housekeeping and transport staff availability per shift vs. discharge volume | dis.8 | enough housekeeping per shift, porter availability |
| dis.8#k16 | family/patient briefing completion rate before physical discharge | dis.8 | how often counselling was actually done, documented instructions before leaving |

### opd.points.md — OPD-to-Diagnostics Conversion

## opd.0

| point | what it is | chunk | also called |
|---|---|---|---|
| opd.0#p1 | 40 new + 400 returning OPD patients per day | opd.0 | our daily OPD numbers, footfall, how many patients we see |
| opd.0#p2 | only 10% of new patients complete prescribed tests here | opd.0 | new patients not doing their tests, first-timers walking out |
| opd.0#p3 | only 20% of returning patients complete prescribed tests here | opd.0 | old patients not converting, repeat patients going elsewhere |
| opd.0#p4 | ₹1.5L/day revenue loss from unredeemed prescriptions | opd.0 | what we are losing daily, money walking out the door |
| opd.0#p5 | leakage equals 5% of EBITDA | opd.0 | what this is costing us on the bottom line, EBITDA hit |
| opd.0#f1 | sequential MRI scheduling with no buffer for walk-in prescriptions | opd.0 | MRI is always full, no slot for today's prescription, scan booking backlog |
| opd.0#f2 | "revenue must come first to justify staffing" causality reversal | opd.0 | we'll hire when volumes go up, can't add people without the business |
| opd.0#f3 | no one has visibility into the whole process to plan overlap | opd.0 | nobody owns end to end, each section sees only its own bit |

## opd.1

| point | what it is | chunk | also called |
|---|---|---|---|
| opd.1#a1 | prescribed tests completed here, same visit, not leaked or skipped | opd.1 | keeping tests in-house, stopping patients going outside for scans, same-day tests |

## opd.2

| point | what it is | chunk | also called |
|---|---|---|---|
| opd.2#a1 | OPD prescription capture — what, by whom, for whom | opd.2 | recording what the doctor prescribed, capturing the prescription |
| opd.2#a2 | diagnostic slot scheduling across modalities | opd.2 | booking the scan, giving the patient a test appointment |
| opd.2#a3 | real-time slot availability management across all modalities | opd.2 | knowing what's free right now, live slot position |
| opd.2#a4 | walk-in/same-day accommodation for freshly-prescribed tests | opd.2 | fitting in today's patient, taking walk-ins, not sending them back |
| opd.2#a5 | prescription-to-redemption tracking, new vs returning split | opd.2 | did the test actually get done, prescribed versus completed report |
| opd.2#a6 | report turnaround and delivery back to prescribing doctor | opd.2 | getting the report back to the doctor, report delivery |
| opd.2#a7 | follow-up/reminders for unredeemed prescriptions | opd.2 | calling the patient back, chasing pending tests |
| opd.2#a8 | capacity utilization monitoring by equipment/modality across operating window | opd.2 | how busy the machines are, is the CT being used |
| opd.2#a9 | OP-to-IP conversion tracking tied to diagnostic findings | opd.2 | scans leading to admissions, converting OPD into IP |
| opd.2#a10 | coordination with Billing for same-visit diagnostic charges | opd.2 | billing the test on the same visit, one bill at the counter |

## opd.3

| point | what it is | chunk | also called |
|---|---|---|---|
| opd.3#d1 | OPD Consultation/Doctors — accurate, timely prescription capture (Critical) | opd.3 | doctors writing it properly, legible prescriptions on time |
| opd.3#d2 | OPD booking protocol — hospital staff vs doctor's secretary owning the patient moment (Critical) | opd.3 | who handles the patient after consultation, secretary controls the patient, can our staff step in |
| opd.3#d3 | Radiology/Imaging capacity & scheduling — MRI the named bottleneck (Critical) | opd.3 | MRI is the choke point, radiology can't take more |
| opd.3#d4 | multi-unit imaging capacity considered per unit, not aggregated (Critical) | opd.3 | our second MRI, one machine is overloaded, unit-wise load |
| opd.3#d5 | Laboratory capacity & turnaround (High) | opd.3 | lab is slow, sample load |
| opd.3#d6 | this department's own manpower availability & salary costs (Critical) | opd.3 | do we have the technologists, staff cost for diagnostics |
| opd.3#d7 | doctor compensation structure — fixed vs revenue-share, diagnostics-linked payout (High) | opd.3 | how doctors are paid, do they get a cut of scans, conflict of interest |
| opd.3#d8 | HR training protocols for walk-in handling, follow-up, scheduling protocol (High) | opd.3 | is our staff trained, do they know what to say |
| opd.3#d9 | IT/HIS real-time slot visibility linked to the prescription (High) | opd.3 | our software doesn't show slots, HIS integration |
| opd.3#d10 | Front Office/Patient Services — booking and queue execution (High) | opd.3 | front desk, reception handling the queue |
| opd.3#d11 | Billing — same-visit billing that doesn't itself become friction (Medium) | opd.3 | billing queue holding patients up, counter delays |
| opd.3#d12 | Daily/OPD Revenue — direct effect (Critical) | opd.3 | daily collections, OPD topline |
| opd.3#d13 | EBITDA — 5% at stake per case study (Critical) | opd.3 | bottom line impact, profitability |
| opd.3#d14 | break-even period on diagnostic equipment (ROI) (High) | opd.3 | when the machine pays for itself, payback on the CT |
| opd.3#d15 | OP-to-IP conversion — findings drive admission decisions (High) | opd.3 | scans leading to admissions, filling beds from OPD |
| opd.3#d16 | manpower availability & salary costs change with conversion volume (Medium) | opd.3 | more volume means more staff, shift planning and cost |
| opd.3#d17 | HR training protocols — capture successful conversion practice into training (Medium) | opd.3 | making it standard training, not leaving it tribal knowledge |
| opd.3#d18 | Bed Occupancy — indirect, via admissions driven by findings (Medium) | opd.3 | occupancy, beds filling from diagnostics |
| opd.3#d19 | Service Excellence/Patient Experience (Medium) | opd.3 | patient experience, how patients feel about the visit |
| opd.3#d20 | Marketing/Referral Engine — repeat-visit trust (Medium) | opd.3 | will they come back, word of mouth, referrals |

## opd.4

| point | what it is | chunk | also called |
|---|---|---|---|
| opd.4#n1 | clinically urgent/STAT tests never wait for scheduling convenience | opd.4 | emergency scan can't be queued, urgent cases go first |
| opd.4#n2 | test accuracy and protocol never compromised for throughput | opd.4 | contrast allergy check, fasting and prep, don't rush the protocol |

## opd.5

| point | what it is | chunk | also called |
|---|---|---|---|
| opd.5#x1 | non-urgent tests can be same-day rather than immediate | opd.5 | do it later today, doesn't have to be right now |
| opd.5#x2 | specific time-of-day slot can shift within the day | opd.5 | move him to the afternoon, adjust the timing |
| opd.5#x3 | choice between clinically-equivalent modalities can flex to capacity | opd.5 | do the ultrasound instead, use whichever machine is free |

## opd.6

| point | what it is | chunk | also called |
|---|---|---|---|
| opd.6#f1 | purely sequential scheduling, no buffer slots for walk-in prescriptions | opd.6 | booked out for days, no room for today's prescription |
| opd.6#f2 | no prescription-to-redemption tracking, leakage invisible until revenue drops | opd.6 | we don't know what was prescribed, we only see it in the numbers later |
| opd.6#f3 | scheduling left to frontline staff with no manager-level process ownership | opd.6 | nobody owns scheduling, the girl at the desk decides |
| opd.6#f4 | causality backwards — waiting for revenue before adding staffing/capacity | opd.6 | hire only when volumes justify it, prove the revenue first |

## opd.7

_Section heading only — no individual points._

## opd.7.1.1

| point | what it is | chunk | also called |
|---|---|---|---|
| opd.7.1.1#c1 | how the leakage figure is known — modeled estimate or tracked prescriptions | opd.7.1.1 | where did that number come from, is it a guess or measured, do we actually track prescriptions |
| opd.7.1.1#c2 | if no prescription-tracking system, why not — facilities, manpower, priority, cooperation | opd.7.1.1 | why aren't we recording prescriptions, no one has time to enter it |
| opd.7.1.1#c3 | OPD floor-staff capacity ratio — billing bandwidth check with peak loading | opd.7.1.1 | do the billing staff have any time, patients per counter, are they only billing |
| opd.7.1.1#c4 | diagnostic scheduling ownership, system maturity, STAT slots, doctor override | opd.7.1.1 | who makes the schedule, can a senior doctor override it, is it a system or a guideline |
| opd.7.1.1#c5 | guest services capacity ratio, or sizing the gap if absent | opd.7.1.1 | do we have anyone guiding patients, PROs, who walks the patient to radiology |
| opd.7.1.1#c6 | off-peak discounted diagnostic slots as utilization, affordability and trust lever | opd.7.1.1 | cheaper rates in lean hours, discount for afternoon scans, filling idle machine time |
| opd.7.1.1#c7 | housekeeping/transport support for non-ambulatory patients at peak | opd.7.1.1 | wheelchair and trolley support, who shifts the patient to radiology |

## opd.7.1.2

| point | what it is | chunk | also called |
|---|---|---|---|
| opd.7.1.2#c8 | revenue is a function of the weakest link, not just prescriptions | opd.7.1.2 | one bottleneck holds everything up, the chain is only as strong as |
| opd.7.1.2#c9 | plan to peak hour, not daily average — redundancy cost vs peak-capture revenue | opd.7.1.2 | rush hour staffing, they'll be idle in lean hours, is the extra person worth it |
| opd.7.1.2#c10 | patient experience/service satisfaction is a real intangible revenue driver | opd.7.1.2 | patients feel attended to, seen on time, staff not visibly rushed |
| opd.7.1.2#c11 | staffing enables volume, not the reverse | opd.7.1.2 | staff ahead of demand, volumes only grow once you have capacity |
| opd.7.1.2#c12 | STAT slots kept vacant with defined release rule; IP-mapped slots stay fixed | opd.7.1.2 | keeping an emergency slot free, what if nobody uses it, IP slot can't be touched |
| opd.7.1.2#c13 | juniormost staff carry revenue — training, morale, appreciation not incentive | opd.7.1.2 | the junior staff are overworked, they can't upsell, recognising good performers |
| opd.7.1.2#c14 | low-volume hospital case — training gaps or intentional diversion instead | opd.7.1.2 | we're not busy and still losing tests, is someone sending patients outside |

## opd.7.2

| point | what it is | chunk | also called |
|---|---|---|---|
| opd.7.2#d1 | entire OPD billing details broken out by department, not aggregate | opd.7.2 | department-wise billing, split by radiology lab cardio, not one OPD number |
| opd.7.2#d2 | OPD staff roster and HR costs for ratio and cost-benefit checks | opd.7.2 | duty roster, salary cost of OPD staff, shift list |
| opd.7.2#d3 | scheduling systems and ownership of the scheduling protocol | opd.7.2 | show us how slots are actually booked, access to the scheduling module |
| opd.7.2#q1 | force a primary-cause selection — manpower, process, scheduling or diversion | opd.7.2 | what's the real reason, which one is the main problem |
| opd.7.2#q2 | if manpower, is the shortfall at manager or floor-executive level | opd.7.2 | are we short of supervisors or short of hands at the counter |
| opd.7.2#q3 | volume-inversion mismatch — highest volume handled by juniormost staff | opd.7.2 | OPD is bigger than IP but juniors run it, managers are less loaded |
| opd.7.2#q4 | EBITDA of OP services compared to IP services, used as leverage | opd.7.2 | which makes more money, OPD or IP, why is OPD getting less attention |
| opd.7.2#q5 | doctor employment type — full-time, part-time, or mixed | opd.7.2 | are they visiting consultants, do they have outside practice |
| opd.7.2#q6 | doctor and secretary cooperativeness — a direct temperature check | opd.7.2 | will the doctors play along, how much pushback from secretaries |
| opd.7.2#q7 | scheduling logic verified in detail, including bump vs vacant-slot variant | opd.7.2 | is it first come first served, do we push someone else out for an emergency |
| opd.7.2#q8 | automation history — prescription writing, scanning, or scheduling software tried | opd.7.2 | what software do we already have, did we try this before |
| opd.7.2#q9 | has diagnostic leakage actually been measured, or just sensed | opd.7.2 | have we put a number to it, or is it just a feeling |
| opd.7.2#q10 | guest relations services — existence check | opd.7.2 | do we have PROs at all, is there anyone guiding patients |
| opd.7.2#q11 | has peak-hour staffing adequacy ever been tested against the hospital's own TAT | opd.7.2 | has anyone checked wait times against our own standard |
| opd.7.2#q12 | is a TAT defined at all, and is it realistic and guidance-inclusive | opd.7.2 | do we have a turnaround standard, does it include explaining to the patient |
| opd.7.2#q13 | staffing-pivot-point / revenue-to-staff ratio defined, or decided ad hoc | opd.7.2 | at what volume do we add a person, when do we know to hire |
| opd.7.2#q14 | culture-of-blame check on floor-level executives for delays and dissatisfaction | opd.7.2 | do we blame the counter staff, who gets pulled up when patients complain |

## opd.7.3

| point | what it is | chunk | also called |
|---|---|---|---|
| opd.7.3#p1 | OPD revenue by department, by discipline, and by individual doctor | opd.7.3 | revenue doctor-wise, which consultant brings what, specialty-wise collection |
| opd.7.3#p2 | HR costs for OPD split by Billing & Floor, Guest Services, Housekeeping | opd.7.3 | manpower cost separately, what each team costs us |
| opd.7.3#p3 | diagnostic leakage quantified — % unredeemed, test quantity, revenue anticipated | opd.7.3 | how much are we losing, value of tests not done |
| opd.7.3#p4 | equipment utilization per unit, by specialty and by doctor | opd.7.3 | machine utilisation, how many scans per day on each unit |
| opd.7.3#p5 | OPD share of revenue and EBITDA, and leaked revenue's share of both | opd.7.3 | what OPD contributes, what the leakage costs us on EBITDA |

## opd.7.4

| point | what it is | chunk | also called |
|---|---|---|---|
| opd.7.4#n1 | department-specific order: process & manpower, automation, people, roles | opd.7.4 | fix the process before buying software, what comes first |
| opd.7.4#n2 | every capability needs an offline/manual version alongside the automated one | opd.7.4 | how do we do this without software, if we don't buy the system |

## opd.7.4.1

| point | what it is | chunk | also called |
|---|---|---|---|
| opd.7.4.1#s1 | prescription recording as a formal process — manual scan, manual or bot reading | opd.7.4.1 | scan every prescription, record what was prescribed and its value |
| opd.7.4.1#s2 | guest-services handholding introduced, or re-audited if it exists | opd.7.4.1 | put someone to guide the patient, relook at our PRO team |
| opd.7.4.1#s3 | logic-driven scheduling — vacant STAT slot, pre-pone next OP patient | opd.7.4.1 | keep a slot free for emergencies, pull the next patient forward if unused |
| opd.7.4.1#s4 | daily best-performer information share, information only, no judgement | opd.7.4.1 | share yesterday's numbers with everyone, no naming and shaming |

## opd.7.4.2

| point | what it is | chunk | also called |
|---|---|---|---|
| opd.7.4.2#s5 | prescription-reading bot — reads scan, calculates value, tracks lost revenue | opd.7.4.2 | software that reads prescriptions, automatic leakage tracking |
| opd.7.4.2#s6 | performance-sharing bot — distributes previous day's performance automatically | opd.7.4.2 | auto-send yesterday's numbers, daily report goes out by itself |
| opd.7.4.2#s7 | automated scheduling bot executing the STAT-vacant/pre-pone logic | opd.7.4.2 | system books the slots, auto-scheduling |
| opd.7.4.2#s8 | patient-facing virtual guest-service bot for the whole hospital visit | opd.7.4.2 | patient app, tells them wait time, call for a wheelchair, car at the gate |

## opd.7.4.3

| point | what it is | chunk | also called |
|---|---|---|---|
| opd.7.4.3#s9 | all floor-level executives — they execute capture, billing and follow-up | opd.7.4.3 | counter staff, the girls at billing, our frontline |
| opd.7.4.3#s10 | Scheduling Manager considered above 200 daily OPD footfall excluding relatives | opd.7.4.3 | someone dedicated to scheduling, do we need a separate person for slots |
| opd.7.4.3#s11 | doctors' and secretaries' buy-in, sensitive where outside-referral incentives exist | opd.7.4.3 | getting doctors on board, secretaries sending tests outside |
| opd.7.4.3#s12 | buy-in from radiologists, cardiologists, pathologists, sonologists on scheduling | opd.7.4.3 | radiologist keeps changing the list, specialists overriding slots |
| opd.7.4.3#s13 | HR to check staffing adequacy and training effectiveness | opd.7.4.3 | HR to confirm headcount, is the training actually working |
| opd.7.4.3#s14 | IT for all automations and integrations including ERP value extraction | opd.7.4.3 | IT team, integration with our HIS and ERP |
| opd.7.4.3#s15 | executive management sign-off on open sharing of performance dashboards | opd.7.4.3 | management approval to share the numbers openly, CEO buy-in |

## opd.7.4.4

| point | what it is | chunk | also called |
|---|---|---|---|
| opd.7.4.4#s16 | Scheduling Manager is the clear new recruitment above 200 daily footfall | opd.7.4.4 | new post for scheduling, recruit a scheduling manager |
| opd.7.4.4#s17 | cost figure for Scheduling Manager not yet given, to be confirmed | opd.7.4.4 | what will that role cost us, salary for the new post |
| opd.7.4.4#s18 | guest-services headcount may be new, sized by peak-load ratio check | opd.7.4.4 | how many PROs do we need, adding guest relations staff |
| opd.7.4.4#s19 | all other named roles are existing ones engaged, not new recruitment | opd.7.4.4 | no other new hiring, using our existing people |

## opd.8

| point | what it is | chunk | also called |
|---|---|---|---|
| opd.8#k1 | prescription redemption rate, separately for new vs returning patients | opd.8 | how many prescribed tests get done here, conversion rate |
| opd.8#k2 | revenue leakage in ₹/day and as % of OPD EBITDA | opd.8 | daily loss, what leakage costs us |
| opd.8#k3 | redemption rate by department/modality, by specialty and by doctor | opd.8 | which department is losing tests, doctor-wise conversion |
| opd.8#k4 | same-visit conversion rate vs later vs never redeemed | opd.8 | did they do it the same day, or come back, or never |
| opd.8#k5 | walk-in/same-day accommodation rate | opd.8 | how often we turn patients away, told to come tomorrow |
| opd.8#k6 | STAT-slot mechanism compliance vs bump variant vs ad hoc | opd.8 | are emergencies handled the right way, do we push patients out |
| opd.8#k7 | equipment utilization % by modality and by individual unit, peak vs off-peak | opd.8 | machine usage per unit, how busy is each MRI |
| opd.8#k8 | off-peak slot utilization % and uptake of off-peak discounted pricing | opd.8 | are lean hours filling up, is the discount working |
| opd.8#k9 | report turnaround time to the prescribing doctor | opd.8 | how fast reports reach the doctor, report delay |
| opd.8#k10 | OPD floor-staff patient/bill ratio, peak vs off-peak, tracked over time | opd.8 | patients per billing staff, counter load by hour |
| opd.8#k11 | TAT compliance rate against a guidance-inclusive TAT | opd.8 | are we meeting our turnaround standard, counter wait time |
| opd.8#k12 | guest-services coverage ratio, patients per staff per hour | opd.8 | how many patients each PRO handles, guest relations load |
| opd.8#k13 | non-ambulatory mobility support responsiveness — average wait | opd.8 | how long for a wheelchair, trolley wait time |
| opd.8#k14 | patient satisfaction isolated to service/professionalism/wait-time factors | opd.8 | service feedback separate from clinical, complaints about waiting |
| opd.8#k15 | Scheduling Manager threshold tracking — daily OPD footfall vs >200 trigger | opd.8 | have we crossed 200 a day, when do we add the role |
| opd.8#k16 | revenue-to-staff ratio by department/discipline against defined pivot points | opd.8 | revenue per staff, when to add the next person |
| opd.8#k17 | training completion % and a proxy effectiveness measure | opd.8 | who has been trained, does training change conversion |
| opd.8#k18 | best-performer information-share cadence adherence | opd.8 | is the daily share actually happening, has it lapsed |

### common.points.md — Common elements

## common.overview

| point | what it is | chunk | also called |
|---|---|---|---|
| common.overview#n1 | cross-department dependencies and frameworks apply alongside any department file, not optional | common.overview | the general rules, applies to every department, the baseline stuff |

## common.solution-method

| point | what it is | chunk | also called |
|---|---|---|---|
| common.solution-method#n1 | cost-benefit analysis: which financial parameters move, and by how much | common.solution-method | is it worth doing, what do we gain, the numbers |
| common.solution-method#n2 | where solution has direct cost (headcount, systems, equipment), benefit must justify it | common.solution-method | will it pay for itself, justify the spend, cost of hiring |
| common.solution-method#n3 | process-only change: benefit must justify disruption and team resistance | common.solution-method | is it worth the upheaval, staff will push back, too much change |
| common.solution-method#n4 | mandatory side-by-side before/after graphical comparison, not prose alone | common.solution-method | show me before and after, a chart of the change, comparison slide |
| common.solution-method#s1 | Automation — can the process be improved or made faster automatically | common.solution-method | can we automate this, put it on the system, software for it |
| common.solution-method#s2 | Process changes required to actually deploy the solution | common.solution-method | what has to change in the process, new SOP, new workflow |
| common.solution-method#s3 | Key people and buy-in — whose cooperation is needed, how secured | common.solution-method | who has to agree, getting the doctors on board, consultant buy-in |
| common.solution-method#s4 | Team/role changes — job profile changes or recruitment, via peak-load method | common.solution-method | do we need to hire, new roles, change the JD |
| common.solution-method#f1 | don't carry Discharge's size-invariance finding into other departments as a rule | common.solution-method | is it the same for a smaller hospital, does this hold everywhere |

## common.shared-considerations

| point | what it is | chunk | also called |
|---|---|---|---|
| common.shared-considerations#c1 | whether discharge, admission, bed scheduling or bed management is currently automated | common.shared-considerations | is any of this on the system, do we still do it manually |
| common.shared-considerations#c2 | who actually owns discharge, admission, bed scheduling — single owner or diffused | common.shared-considerations | who is in charge of discharges, whose job is this, nobody owns it |
| common.shared-considerations#c3 | ARPOB — also a baseline financial parameter | common.shared-considerations | revenue per bed, earning per bed per day, per-bed realisation |
| common.shared-considerations#c4 | ALOS — also a baseline financial parameter | common.shared-considerations | average length of stay, how long patients stay, days per patient |
| common.shared-considerations#c5 | discharge duration provisional → confirmation → actual, tracked insured vs non-insured separately | common.shared-considerations | how long a discharge takes, TPA cases take longer, insurance clearance time |
| common.shared-considerations#c6 | whether OT scheduling links to bed management; admission priority scheduled vs walk-in | common.shared-considerations | OT list versus beds, who gets the bed, emergency walk-in priority |
| common.shared-considerations#c7 | mechanism mapping planned admissions against provisional discharges and expected bed availability | common.shared-considerations | how many beds free tomorrow, planning admissions against discharges |
| common.shared-considerations#c8 | equivalent mapping for predicted ICU requirement against ICU beds and step-down | common.shared-considerations | will we have an ICU bed, post-op ICU planning, ICU is always full |

## common.peak-load

| point | what it is | chunk | also called |
|---|---|---|---|
| common.peak-load#f1 | assuming flat, uniform patient/admission/discharge flow across the operating day | common.peak-load | average per day, spread evenly across the day, per-hour average |
| common.peak-load#n1 | size staffing to peak window; show redundancy cost offset by captured revenue | common.peak-load | staff sitting idle in the afternoon, extra people for rush hour |
| common.peak-load#f2 | waiting for volume before adding manpower — causality is backwards | common.peak-load | we'll hire once volumes justify it, staff up later, prove the need first |
| common.peak-load#s1 | identify the relevant staff pool, excluding supervisory and non-contact support roles | common.peak-load | who actually does this work, which staff count, headcount on the floor |
| common.peak-load#s2 | establish shift structure, typically at least two shifts | common.peak-load | how many shifts, shift timings, duty roster |
| common.peak-load#s3 | establish total relevant volume — patients, bills, admissions, discharges, bed-turnovers | common.peak-load | how many cases a day, monthly numbers, daily footfall |
| common.peak-load#s4 | establish realistic per-unit time and units-per-person (~1.25 bills per patient) | common.peak-load | how long one billing takes, time per patient, minutes per turnover |
| common.peak-load#s5 | apply a function-appropriate peak-loading split, confirmed not assumed | common.peak-load | what share comes in peak hours, the rush period, morning crowd |
| common.peak-load#s6 | result: available time per staff per hour — real bandwidth, including upsell work | common.peak-load | do they have time, are they free enough, can they do extra work |
| common.peak-load#n2 | run the method at dependency verification (§7.2) for current-state staffing adequacy | common.peak-load | are we short staffed today, is the current team enough |
| common.peak-load#n3 | run it again at solution construction (§7.4 aspect 4) to justify headcount | common.peak-load | how many more people do we need, hiring justification, sanction posts |
| common.peak-load#k1 | OPD floor-staff-to-patient billing ratio | common.peak-load | billing counter staff, OPD billing queue, cash counter manpower |
| common.peak-load#k2 | OPD guest-services-to-patient ratio | common.peak-load | guest relations staff, help desk per patient, front office manpower |
| common.peak-load#k3 | OPD housekeeping/transport-to-patient ratio, non-ambulatory (~5% of patients) | common.peak-load | wheelchair and trolley staff, ward boys, who takes patients for scans |
| common.peak-load#k4 | Discharge nursing/discharge-coordination ratio, against two-window discharge pattern | common.peak-load | nurses per discharge, discharge coordinator, who does the paperwork |
| common.peak-load#k5 | Discharge housekeeping/transport per shift vs bed-turnover and transport volume | common.peak-load | housekeeping per shift, bed cleaning staff, how fast beds get ready |
| common.peak-load#k6 | Bed Management ratio for bed-turnover and admission-handling staff (method here, KPI #17 there) | common.peak-load | admission desk staff, bed turnover manpower, who manages beds |

### play.points.md — Discharge conversation playbook

## play.0

| point | what it is | chunk | also called |
|---|---|---|---|
| play.0#s1 | read alongside the discharge domain file and the chat-rules package | play.0 | opening this playbook, before running a discharge conversation |
| play.0#n1 | this is a pattern to recognise and adapt, never a script to replay | play.0 | tempted to copy the worked conversation, a hospital matches the example |
| play.0#n2 | never reuse the practice hospital's worked numbers for another hospital | play.0 | a new hospital, reaching for a number from the example |
| play.0#s2 | what transfers is the conversation's shape, not its numbers | play.0 | adapting the example, a different department or hospital |

## play.1

| point | what it is | chunk | also called |
|---|---|---|---|
| play.1#s1 | run the unscripted consulting arc in a fixed stage order | play.1 | hospital has committed to the problem, scripted part is over |
| play.1#s2 | dependency verification first: practice-pattern questions, one at a time | play.1 | start of the unscripted arc, before proposing anything |
| play.1#s3 | size financial and occupancy urgency for this hospital next | play.1 | dependencies verified, how urgent is this really |
| play.1#n1 | diagnosis is its own stage, separate from the solution | play.1 | root cause is clear, tempted to jump to what I'd build |
| play.1#s4 | five-part solution overview as clickable options plus one overview graphic | play.1 | diagnosis accepted, first solution content |
| play.1#s5 | deep-dive one part at a time, in the hospital's chosen order | play.1 | overview shown, hospital picks a part |
| play.1#s6 | handle follow-ups and objections as they come, mid-deep-dive | play.1 | hospital interrupts a deep-dive with a question or challenge |
| play.1#s7 | on real numbers, redo sizing and graphics and say what changed | play.1 | hospital shares its actual data |
| play.1#s8 | synthesize everything into a short, sequenced next-steps plan | play.1 | solution walked through, real data in hand |
| play.1#s9 | pivot to the subscription-pricing rules when the conversation reaches it | play.1 | hospital asks about buying, conversation naturally lands there |
| play.1#f1 | ending a diagnosis on "does this make sense to try?" with no solution shown | play.1 | diagnosis turn written, solution never presented |

## play.2

| point | what it is | chunk | also called |
|---|---|---|---|
| play.2#s1 | name the specific mechanism, not a flat root-cause label | play.2 | writing the diagnosis, root cause identified |
| play.2#s2 | identify a dead window in the hospital's existing process | play.2 | building the diagnosis mechanism |
| play.2#s3 | quantify how much of the process could already happen in that window | play.2 | dead window named, needs sizing |
| play.2#s4 | give concrete reasons nobody uses that window today | play.2 | explaining why the dead window stays dead |
| play.2#s5 | tie the ownership gap to a concrete hospital-specific trigger | play.2 | naming the second root cause, no single owner |
| play.2#n1 | flag Tojo-constructed numbers as construction and swap them on real data | play.2 | using assumed times before the hospital stated its own |

## play.3

| point | what it is | chunk | also called |
|---|---|---|---|
| play.3#s1 | present the solution as five named parts, four aspects plus KPIs | play.3 | diagnosis accepted, moving to solution |
| play.3#s2 | short intro line naming five parts, clickable options, one overview graphic | play.3 | first solution message |
| play.3#n1 | never unpack all five parts in one message | play.3 | tempted to deliver the whole solution at once |
| play.3#s3 | reveal each part's detail and its own graphic only on engagement | play.3 | hospital clicks or asks about one part |

## play.4

| point | what it is | chunk | also called |
|---|---|---|---|
| play.4#n1 | each part gets hospital-specific treatment, not restated generic content | play.4 | deep-diving any of the five parts |
| play.4#s1 | translate generic automation capability into this hospital's named bottlenecks | play.4 | deep-diving automations, bottlenecks surfaced earlier |
| play.4#s2 | function-by-function today-vs-with-Virevo before/after diagrams, not prose | play.4 | deep-diving process changes |
| play.4#s3 | flag the single biggest leak as the amber biggest-leak box | play.4 | before/after comparison built, one function dominates |
| play.4#s4 | narrow the generic role list to roles this conversation actually touched | play.4 | deep-diving key people and buy-in |
| play.4#s5 | tie each role's reassurance to something the hospital itself said | play.4 | addressing a role's resistance, hospital gave a constraint earlier |
| play.4#s6 | run the peak-load staffing ratio-check against confirmed shift and volume | play.4 | deep-diving team and role changes |
| play.4#f1 | sizing the new role by a naive single hire or flat daily division | play.4 | staffing recommendation, volume clusters into windows |
| play.4#s7 | curate KPIs to those with real or target numbers, mark the rest amber | play.4 | deep-diving KPIs and targets |
| play.4#f2 | inventing a placeholder number for a KPI with no baseline | play.4 | a KPI has no data, table looks incomplete |

## play.5

| point | what it is | chunk | also called |
|---|---|---|---|
| play.5#s1 | split a tell-me-more answer roughly half text, half new graphic | play.5 | hospital asks for more on a point already shown |
| play.5#s2 | name the gap between what the earlier graphic showed and this answer | play.5 | opening a follow-up answer |
| play.5#s3 | let each follow-up decompose the previous answer one level further | play.5 | a chain of successive tell-me-more questions |
| play.5#n1 | never fall back to pure prose in a follow-up chain | play.5 | third or fourth follow-up, detail getting fine-grained |
| play.5#c1 | judge whether pushback is a factual correction or resistance to hold against | play.5 | hospital contradicts something described as already happening |
| play.5#n2 | the hold-position rule does not apply to a factual correction | play.5 | tempted to argue past a correction about their systems |
| play.5#s4 | acknowledge the correction plainly, say it does not need to be true | play.5 | assumed capability turns out not to exist here |
| play.5#s5 | reframe the capability as a new layer Virevo adds | play.5 | hospital lacks a prerequisite the solution assumed |
| play.5#s6 | show concretely how little it asks of existing systems and staff | play.5 | hospital fears the solution needs them to change first |

## play.6

| point | what it is | chunk | also called |
|---|---|---|---|
| play.6#s1 | say plainly which findings shift and by how much | play.6 | hospital supplies real numbers replacing estimates |
| play.6#n1 | recompute every downstream number, never leave stale beside new | play.6 | a base estimate changed, dependent figures already published |
| play.6#s2 | name corroboration when two independent numbers clear the same threshold | play.6 | real number clears a trigger the estimate also pointed at |
| play.6#s3 | use the blank-then-filled two-state graphic to collect stage timestamps | play.6 | asking for granular stage-by-stage timings |

## play.7

| point | what it is | chunk | also called |
|---|---|---|---|
| play.7#s1 | open next steps with a low-commitment pilot, no new hires or systems | play.7 | diagnosis and solution walked through, closing the arc |
| play.7#s2 | make the pilot convert the biggest unconfirmed assumption into measured fact | play.7 | designing the pilot, a key estimate still untested |
| play.7#s3 | state a cleared threshold plainly as already-there, not softened | play.7 | confirmed numbers pass a named trigger |
| play.7#n1 | cost-versus-opportunity goes in stat cards, not narrated in text | play.7 | presenting the economics of the plan |
| play.7#s4 | offer a choice of next branch rather than one mandated path | play.7 | closing the next-steps message |
| play.7#s5 | lead systems scoping with one plain-language question, detail optional | play.7 | hospital picks the IT integration branch |
| play.7#c1 | treat "too technical" as a timing signal to defer, not a rejection | play.7 | hospital says a line of questioning is premature |

## play.8

| point | what it is | chunk | also called |
|---|---|---|---|
| play.8#s1 | answer the engagement-model question honestly from what's already implied | play.8 | hospital asks what Virevo's delivery actually consists of |
| play.8#n1 | flag the answer as Tojo's own construction when no rule settles it | play.8 | describing delivery with no subscription rule to cite |
| play.8#s2 | hand off to the pricing rules once it becomes a subscription-details ask | play.8 | question turns to what it costs and what's included |

## play.9

| point | what it is | chunk | also called |
|---|---|---|---|
| play.9#n1 | only the worked numbers and mechanism are discharge-specific, the shape is not | play.9 | reusing this playbook for another department |
| play.9#s1 | apply the same stage order to bed management and OPD-diagnostics | play.9 | running a non-discharge department conversation |
| play.9#s2 | find that department's own dead-window or ownership-gap framing | play.9 | building a diagnosis outside discharge |
| play.9#s3 | run the same peak-load ratio-check on that department's threshold role | play.9 | staffing deep-dive in another department |
| play.9#s4 | curate KPIs the same way against that department's own list | play.9 | KPI deep-dive in another department |
| play.9#c1 | once other worked examples exist, consider splitting shared method from per-department appendix | play.9 | maintaining this package, second and third playbooks written |
