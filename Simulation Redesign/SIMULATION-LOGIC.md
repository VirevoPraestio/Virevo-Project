# How simulation.html works today (read 13 Oct 2026)

Source: `Simulation Version 16.05/simulation.html` (6,483 lines; the engine is inline, lines 1665–5750). Checked by running it on the 51 sample CSVs.

## The eight pages
1. **Upload data**: 51 CSVs expected (11 required, 14 recommended, 23 optional, plus `sim_parameters.csv`) and an optional cost table.
2. **Define targets**: one "Your target" box per KPI and resource lever (about 45), grouped by six departments.
3. **Pick 6 KPIs** from 43, in six departments.
4. **Simulate**: key outcome tiles, then a ranked list of levers ("Resource Intervention Panel") to override, cost and approve.
5. **Dream target**: for each of the 6 KPIs, up to 3 capital and 2 operational interventions, each with an Achievable cost and a Dream cost. The user types or adopts a cost, presses Simulate, and sees the project total, duration and break-even.
6. **Freeze** (modal), then confirm.
7. **Implementation kickoff**: names and mobiles for up to 13 department heads; tasks shown by KPI or by department.
8. **Dashboards**: the owner view and one per department head (kanban, milestones, export), plus a dependency dashboard.

## 1. What it reads
- Only **16 of the 51 files** feed the engine: `sim_parameters`, `dim_wards`, `dim_staff`, nursing shifts, OT sessions, discharges, daily revenue, billing claims, insurance claims, pharmacy dispensing, ICU census, OPD visits, admissions, housekeeping log, housekeeping staff. The other 35 are loaded and ignored.
- `sim_parameters.csv` (70 rows) is read first and acts as the anchor: a baseline, a target, a slider range and a written formula for each lever.
- Several baselines are **fixed numbers from the case study**, not from the data: occupancy 73.4%, gross revenue ₹612 L, EBITDA 8.0%, ARPOB ₹3,110, LOS 5.28 days.

## 2. How the "formula" is built
- About 20 sub-formulas (F001–F025), each a straight line, a curve or a ratio, with a **slope fixed in the code** ("Sunrise priors").
- "Fitting" only moves each line's intercept so it passes through today's single observed point. The slopes never come from the data. The R² values shown are constants typed into the code.
- Only two things are truly estimated from data: the four OT-cancellation reason weights and the OT fill rate.
- The chain (`runSimulation`) runs: nursing → agency cost; biomed staff → PM adherence → OT cancels → OT use → OT revenue; ward-round time + discharge coordinators + report TAT → discharge lag → bed turnover and LOS → admissions → gross revenue; ICU beds → overflow → ICU LOS; billing and pre-auth staff → submission lag, insurance TAT → receivables; drug par days + generics → drug cost; counsellors, incentives, echo/CT/MRI → case mix → ARPOB; diagnostics → diagnostic revenue.
- **EBITDA = 8.0 + a sum of seven deltas** (drug cost, agency cost, cardio mix, ortho mix, ARPOB, receivables, bed turnover), each with a fixed weight.

## 3. How levers are ranked
A hand-written table (`INFLUENCE`) gives each lever a 0–1 score against each KPI. Scores for the 6 chosen KPIs are added, the top 25 are kept, and billing staff plus one lever per department are forced in. **The ranking does not come from the formula**: no lever is moved in the engine to measure its real effect.

## 4. "What can be achieved"
- **Achievable lever value = today + 75% of the way to the target** (target from `sim_parameters`, or a hard-coded default). Achievable KPIs = the engine run at those lever values.
- **User targets are worked backwards** through the inverse of eleven single formulas (OT use → biomed staff; LOS → discharge coordinators and an 8 AM ward round; OPD conversion → counsellors; insurance TAT → pre-auth staff; submission lag → billing staff; diagnostic revenue → machine use; ARPOB → incentive and MRI; ICU LOS → ICU beds; and three direct ones). A target for any other KPI, EBITDA included, is accepted on screen and **silently not used**.
- **Dream** = the full target; big infrastructure (ICU beds, theatres, ventilators, C-arms, scanners) appears only at Dream.
- **Cost** = units changed × capex or opex per unit. Opex is counted once, not per month.
- **Approving a cost** moves that lever in a straight line between today, Achievable and Dream. **Every lever not on screen also moves**, by a "blend fraction" set by the total money approved. Money approved for one item quietly improves all the others.
- **Duration** is a fixed number of months per kind of lever. **Break-even** = cost ÷ (influence score × ₹2 L a month), not the EBITDA gain the engine predicts.

## 5. What happens after freeze
Each approved lever has a fixed task template (`IMPL_TASK_MAP`: 6–8 tasks, departments, start week, duration, a go-live milestone). Tasks are laid onto a week grid and grouped by department head.

## 6. Faults found when run on the sample data
- Today is not reproduced: EBITDA comes out 9.1% (case 8.0%), bed turnover 14.2 h (data 15.1 h), ICU overflow hits its floor of 1%.
- **Occupancy is always 73.4%**: admissions are worked out from occupancy, then occupancy from admissions.
- Gross revenue rises whenever LOS falls, as if demand had no limit.
- Generic ratio reads 100% and readmissions 0% at baseline (wrong column or missing file).
- Turning on the MRI raises EBITDA but not diagnostic revenue (MRI capacity stays 0).
- KPIs such as diagnostic leakage, nursing vacancies and report TAT are just the input passed through.

## What this means for the rebuild (points 6 and 7 of the brief)
The new formula skill needs: slopes estimated from the hospital's own history where enough data exists, and taken from the reference files' dependency weights where it does not, with each link marked "from your data" or "from reference"; lever ranking by actually moving each lever in the engine; costs per month over the project; and no movement in levers the user did not approve.
