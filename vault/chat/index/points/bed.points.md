# Bed Management — point index

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
