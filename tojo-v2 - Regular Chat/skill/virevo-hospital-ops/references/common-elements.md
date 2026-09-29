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
tokens: 1150
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
