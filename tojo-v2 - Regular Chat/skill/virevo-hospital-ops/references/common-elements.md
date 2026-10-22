<!--chunk
id: common.overview
title: Common Elements — Applies Across All Departments
summary: Establishes that the cross-department dependencies, considerations and frameworks in this file apply alongside any department file and are not optional detail.
keys: common elements, cross-department, applies to all departments, dependencies, considerations, reasoning frameworks, universal rules, department file
needs: none
see: none
tokens: 80
-->
# Common Elements — Applies Across All Departments

Dependencies, considerations, and reasoning frameworks that apply across departments. Apply these alongside whichever department file a query retrieves — the department file will reference this one rather than restate it, so its content is not optional detail.

<!--chunk
id: common.solution-method
title: Solution Construction Method
summary: Establishes the two universal requirements of every department solution: a cost-benefit analysis with a mandatory side-by-side before/after graphic, and four aspects.
keys: solution construction, cost-benefit analysis, before and after comparison, graphical comparison, automation, process changes, buy-in, team and role changes, recruitment, justify the cost
needs: none
see: common.peak-load
tokens: 580
-->
## Solution Construction Method (universal framework)

Two things are required of every department's solution, not just the department a query names.

### 1. Cost-benefit analysis + mandatory side-by-side graphical comparison

For every problem, once causes, dependencies, and financial effects are established — for both the current state and the state with the solution applied — two things are required before presenting it:

- A cost-benefit analysis: identify which financial parameters the improvement actually moves and by how much; where the solution has a direct cost (headcount, systems, equipment), the quantified benefit must justify that cost; where it's process-change-only with no direct cost, the quantum of benefit still has to justify the disruption and the resistance it will provoke from affected teams.
- A side-by-side graphical comparison of before vs. after — not prose alone. This is a hard rule for every department and every solution.

### 2. The four aspects every solution must address

- **Automation** — can the process be improved or made faster through some level of automation?
- **Process changes** — what process changes are required to actually deploy the solution?
- **Key people & buy-in** — who are the key team members whose cooperation is required, and how is their buy-in secured?
- **Team/role changes** — does this require any change in job profiles, or new recruitment? Answer this with the Peak-Load Staffing & Manpower Cost-Benefit Method below. It is the required method for every department, not a judgment call made fresh each time.

Every department's Solution Construction Method section walks through these four explicitly. What is department-specific is the content of each answer, not the four-part shape.

### What is NOT universal

Do not assume a department's recommended solution stays the same across hospitals of different sizes and occupancy levels, with only its cost-justification varying. That holds for Discharge Process (`discharge-process.md` §7.4) and is a finding about that department, not a general rule. Other departments may have solutions that genuinely differ by hospital size or severity, not just differ in whether they are worth acting on yet. Work each department through on its own rather than carrying Discharge Process's shape into it in advance.

<!--chunk
id: common.shared-considerations
title: Discharge / Bed Management / Admission / ALOS / Occupancy — shared query considerations
summary: Establishes the eight-point consideration set any query touching discharge, admission, bed management, ALOS or occupancy must work through, whichever department asks it.
keys: discharge, admission, bed management, bed scheduling, ALOS, occupancy, ARPOB, process ownership, OT scheduling, ICU beds
needs: none
see: none
tokens: 460
-->
## Discharge / Bed Management / Admission / ALOS / Occupancy — shared query considerations

Whenever a query touches ALOS, Discharge, Occupancy, or Bed Management/beds — as subject matter, as a dependency, or as context for another problem — consider:

1. Whether any part of Discharge Process, Admission Process, Bed Scheduling, or Bed Management is currently automated.
2. Who actually owns these three processes (Discharge, Admission, Bed Scheduling/Management) — a defined single owner, or left to individual executives/functions operating off whatever guidelines Operations, Administrative, or Finance have stipulated. This is the ownership-diffusion failure signature in Discharge Process §6, asked at a wider scope.
3. ARPOB.
4. ALOS.
5. Typical discharge duration — provisional discharge → discharge confirmation → actual discharge — tracked separately for insured and non-insured patients. They behave differently; see Discharge Process §7.4.1's provisional-evening/final-morning automation design.
6. Whether OT Scheduling is linked to Bed Management, and whether a protocol exists establishing admission priority between scheduled cases and sudden walk-ins.
7. Whether there's a mechanism mapping planned admissions against provisional discharges and provisional bed availability — actual empty beds plus beds expected to clear from discharges.
8. Whether there's an equivalent mapping mechanism for predicted ICU bed requirement — planned admissions expected to need ICU post-op or immediately — against ICU beds available or expected to free up from step-down.

Items 3–4 double as baseline financial parameters. Items 1, 2, 6, 7, and 8 double as dependency/practice-verification questions. Department files reference this block rather than repeating it, and add only what is genuinely specific to that one department beyond this shared set.

<!--chunk
id: common.peak-load
title: Peak-Load Staffing & Manpower Cost-Benefit Method
summary: Establishes that staffing is sized to peak-hour load by a six-step ratio check, run at both dependency verification and solution construction, staffing preceding volume.
keys: staffing, manpower, peak hour, peak load, headcount, shift structure, staff-to-patient ratio, recruitment, workload bandwidth, off-peak redundancy
needs: none
see: bed.8
tokens: 1260
-->
## Peak-Load Staffing & Manpower Cost-Benefit Method (universal)

### 1. Never assume linear/uniform flow — plan against peak-hour load

Assuming a flat, uniform rate of patients/admissions/discharges/bed-turnovers across the operating day is one of the most common and costly planning mistakes a hospital makes. Real demand is peaked — a large share of volume concentrates into specific windows (examples seen so far: ~80% of OPD patients in a 4-hour window with the rest spread thin; admissions/discharges front- and back-loaded into shift-start/shift-end windows). Staffing must be sized to the peak window specifically, which will visibly create redundancy during lean/off-peak periods. That redundancy is a real, visible cost — but it is what the cost-benefit comparison in point 3 below is for: showing that the redundancy cost is comfortably offset by the additional revenue the peak-hour adequacy actually captures. Don't treat off-peak redundancy as self-evidently wasteful; show the comparison.

### 2. The correct causality: adequate staffing enables volume, not the reverse

Decision-makers routinely get the causal direction backwards: they wait for workload/volume to visibly increase before adding manpower. The actual direction runs the other way — volumes, and the revenue that follows, only increase once staffing is already ahead of what current averages dictate, because that is what creates the spare capacity to absorb and convert additional demand. Treat "we'll staff up once volume justifies it" as a diagnosable planning error whenever it shows up in a query, not a neutral operating choice.

### 3. The ratio-check method — how to actually calculate staffing adequacy

For any function where staffing adequacy is in question, run the same style of calculation:

1. Identify the relevant staff pool for that function specifically (exclude staff who belong to other functions, management/supervisory layers, and support roles that aren't the actual point of contact/execution).
2. Establish shift structure (typically at least 2 shifts).
3. Establish total relevant volume for the period (patients, bills, admissions, discharges, bed-turnovers — whatever the function's real unit of work is).
4. Establish realistic per-unit time (e.g., minutes per billing transaction, minutes per patient interaction, time per bed turnover) and, where relevant, units-per-person (e.g., ~1.25 bills per patient).
5. Apply a peak-loading split appropriate to that function and shift pattern — not assumed identical across every function; confirm the actual shape for the function in question — rather than dividing volume evenly across operating hours.
6. The result: actual available time per staff member, hour by hour, which tells you concretely whether they have real bandwidth for what's being asked of them, including any secondary/upsell/conversion work layered on top of their primary task — not just whether headcount looks adequate on paper.

Apply this method at two distinct points in the working method, not one:

- **Dependency verification (§7.2 of each department)** — to establish this specific hospital's actual current-state staffing adequacy against real demand patterns, rather than an assumed or reported adequacy.
- **Solution construction (§7.4, aspect 4 — Team/role changes)** — to justify, quantitatively, whether headcount needs to increase, using the same peak/off-peak per-person-per-hour-per-shift math, rather than a qualitative judgment call.

### Which ratio applies in which department

- **OPD-to-Diagnostics Conversion**: OPD floor-staff-to-patient billing ratio, guest-services-to-patient ratio, housekeeping/transport-to-patient ratio for non-ambulatory mobility support (~5% of patients assumed to need it). See `opd-diagnostic-leakage.md` §7.1 and its KPIs #10 and #12.
- **Discharge Process**: nursing/discharge-coordination staffing ratio for discharge-associated functions, and housekeeping/transport staff available per shift relative to bed-turnover and discharge-transport volume — both run against this hospital's own confirmed two-window (morning/evening) discharge pattern rather than an even 24-hour spread. See `discharge-process.md` §7.1 points 2–3, §7.2 questions 11–12, and KPIs #14/#15.
- **Bed Management**: the equivalent ratio-check for bed-turnover and admission-handling staff. `bed-management.md` carries the ratio metric at KPI #17 but does not itself carry the method — apply the method from this file when a Bed Management query reaches staffing adequacy, at both the verification and the solution-construction stage.
- **Supply Chain & Procurement**: the only department with **two** distinct peaks, which must be sized separately — inbound receipt (vendor delivery windows, driving GRN entry) and outbound issue (pre-OT picking and discharge-time returns). Sizing either against a daily average produces the GRN-backlog and slow-issue symptoms that get reported as system problems. See `supply-chain-procurement.md` §7.1, §7.2.3 cluster L, and KPI #30.

<!--chunk
id: common.occupancy-pivot
title: The 80% Occupancy Pivot
summary: Establishes 80% occupancy as one hospital-wide state change that alters every function's operating strategy and triggers a differently-priced owner role in each.
keys: 80% occupancy, occupancy pivot, hospital-wide threshold, state change, slack, dedicated owner role, hiring trigger, manager salary, proficiency, sequencing
needs: none
see: common.peak-load, common.shared-considerations
tokens: 1300
-->
## The 80% Occupancy Pivot (universal)

### 1. It is one hospital-wide pivot, not a threshold each department set for itself

80% occupancy appears independently in three department files as a trigger, and it is the same pivot in all three, not a coincidence of three separate derivations. Treat it as a **state change for the whole hospital**, and read every department's numbers differently on either side of it.

Below the pivot, spare capacity absorbs coordination failure. A bed turned around slowly, an indent raised late, a discharge that runs to the afternoon — each is inefficient, and none of them costs a patient or a rupee, because there is somewhere else to put the next admission and time to recover. Above it, that absorption is gone. The same coordination failure now converts directly into a lost admission, a cancelled case, a stock-out at the point of care, or a bed-day that earns nothing. Nothing about the failure changed; what changed is that the hospital stopped having room to hide it.

This is why "we've always run like this and it was fine" is a true statement and an irrelevant one from a hospital that has crossed the pivot.

### 2. Every function needs a *different* strategy above it, not the same strategy harder

The pivot is universal; what it demands is not. Each department's answer to "what changes at 80%" is its own:

- **Bed Management** — prediction stops being a convenience and becomes the mechanism. The twice-daily mapping cadence, the earmarked emergency reserve and the call-in timing in `bed-management.md` §7.4.1 all earn their cost only here.
- **Discharge Process** — the TAT definition tightens. Measuring through to the next patient's admission into that bed becomes an active efficiency check rather than a definitional nicety (`discharge-process.md` §7.2 question 15), because that is where the time is now going.
- **Supply Chain & Procurement** — buffer policy inverts. Below the pivot, generous safety stock is a working-capital choice; above it, a stock-out stops care and the shortage-allocation rule in `supply-chain-procurement.md` §7.4.1 starts firing for real rather than sitting unused in the ERP.
- **OPD-to-Diagnostics** — the pivot is **not** this department's trigger, and that is worth stating. OPD is ambulatory: its load scales with footfall, not with how full the wards are, which is why its Scheduling Manager is anchored to >200 daily OPD footfall instead. Where occupancy does reach OPD it is through OP-to-IP conversion — above the pivot, a finding that would have become an admission may not.

When a hospital reports crossing 80%, work through what it means for the department in front of you. Do not carry another department's answer across.

### 3. It triggers a dedicated owner in each function — at different salaries

At the pivot, each function's coordination load exceeds what a shared or part-time owner can carry, so each warrants a dedicated role. Same trigger, different roles:

| Function | Role triggered | Indicative cost |
|---|---|---|
| Supply Chain & Procurement | Materials Manager | ₹8–10 lakhs/year |
| Bed Management | Bed Manager | ₹4–4.5 lakhs/year |
| Discharge Process | Discharge Manager | ₹4–4.5 lakhs/year |

**A common trigger does not imply a common price, and this is the error to avoid.** The salary follows the proficiency the role actually requires, not the threshold that surfaced it. A Materials Manager carries vendor negotiation, rate-contract authority, inventory economics, systems governance and cross-department accountability, and is priced accordingly. A Bed Manager and a Discharge Manager are coordination roles over a defined process with a defined counterpart — real seniority, narrower scope. Never reason from one of these figures to another, in either direction: do not talk a hospital down to a coordinator's salary for a materials role, and do not inflate a coordination role to a materials salary because the trigger was the same.

The processing layers beneath these roles are sized separately and by volume, not by this pivot — see `common.peak-load`.

### 4. A department may carry a sharper pivot of its own

Where a department has derived its own, more precise inflection, that one governs its solution shape and this one still governs whether the hospital is in the state at all. Bed Management is the case in the library: its scaling pivot is demand against supply — monthly-average daily admissions against the previous night's average available beds — which is deliberately not an occupancy measure and is sharper for that department's purpose. Both apply; they are not competing.

### 5. Crossing the pivot warrants the roles; it does not sequence them

A hospital that crosses 80% has, on this logic, become eligible for several dedicated roles at once, and the combined cost is real. The pivot establishes that each is *warranted*; it does not say hire them all this quarter. Rank them by which function's failure is currently costing this hospital the most, using that department's own §7.3 financial parameters, and say plainly that the ranking is a sequencing judgment rather than a claim that the unranked roles are unnecessary.
