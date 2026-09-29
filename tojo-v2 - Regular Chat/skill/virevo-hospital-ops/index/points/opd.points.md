# OPD-to-Diagnostics Conversion — point index

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
