# Tojo — Point Index

This is the layer below the chunks: every individually named activity, dependency, coupling, non-negotiable, flex, failure mode, consideration, verification question, financial parameter, solution element and KPI in the Tojo v2 hospital-ops library, each carried with the chunk it lives in. It is a retrieval artefact only — the retriever searches it, and it never enters the prompt; what enters the prompt is the chunk a row points at. Read the columns as: `point` is the stable id, built as `<chunk>#<kind><n>` so the id itself names its chunk; `what it is` is a compressed statement of the thing, not a summary of the surrounding section; `chunk` is what to fetch; `also called` is the phrasebook — the words a hospital would actually use, which is what most queries will match on. 961 points across the six files cover 92 of the 96 retrievable chunks in the library (`dis.7`, `opd.7`, `sup.7` and `sup.8` are section-container headings and carry no points of their own).

## How a lookup works

1. A hospital says "we don't record when housekeeping is notified that a bed is free."
2. Match on `also called`, not on the formal description — here "bed cleaning time", "how long the bed sits empty", "when did they actually get told".
3. The matching rows hand back their chunk: `bed.8#k6` and `dis.8#k4` both give bed turnaround time, `dis.3b#d8` gives the notification mechanism specifically, `dis.2#a9` gives the handoff itself, `bed.3#d2` gives the dependency.
4. Fetch that chunk, plus its one-hop `needs` from the chunk header — never the whole department file.
5. Where a concept spans departments, the Cross-department table below says which point is the definition and which are references, so the fetch starts from the owning chunk.

**The §3b rows are the shortest path for a misattributed query.** Every department file now carries a cross-function interdependency map at §3b, and those maps are built for exactly the case where a hospital names the wrong department. A query that arrives as "our billing is slow" or "housekeeping can't keep up" or "procurement is buying badly" should be matched against the §3b rows first: they are the only rows in this index whose `also called` column is phrased as the *complaint* rather than as the mechanism.

## Cross-department concepts

Each row is one underlying thing that is indexed under point ids in two or more files. The `note` says which id owns the definition and which merely reference or instantiate it — a retriever that lands on a reference should follow the note to the owner before answering.

| concept | points | note |
|---|---|---|
| The cross-function interdependency map itself | `sup.3b`, `dis.3b`, `bed.3b`, `opd.3b` | The same template section in all four department files, introduced with Supply Chain and applied retroactively. Each map is that department's own couplings, not a copy. Where two maps name the same edge, the reciprocal is stated in both rows. |
| Failures are misattributed at the point they surface | `sup.3b#c1`; `dis.3b#c1`; `bed.3b#c1`; `opd.3b#c1` | The organising principle behind all four maps, stated once in each with a department-specific twist: Supply Chain is blamed late, Discharge is blamed for others' delays, Bed Management is disbelieved on its own numbers, and OPD has no symptom at all. |
| Pharmacy returns and the returnable balance at discharge | `sup.3b#d7`, `sup.7.2.3#q18`–`#q22`, `sup.8.2#k18`, `sup.8.2#k19`; `dis.3b#d4`, `dis.3b#q3`, `dis.7.4.1#s6`, `dis.7.4.1#s7`, `dis.7.4.1#s12`, `dis.8#k6`; `dis.2#a3`, `dis.2#a6` | Supply Chain owns the computation (`sup.7.4.1.2#s5` — the issued-vs-consumed gap); Discharge owns the consequence. `sup.8.2#k18` is the flagship metric of the Supply Chain file and measures exactly what `dis.8#k6` measures from the other side. A query about "pending pharmacy reconciliation" belongs in Supply Chain even though it is always reported by Discharge. |
| OPD prescription leakage — diagnostics and pharmacy as one mechanism | `sup.3b#d13`, `sup.7.2.3.2#q6`–`#q10`, `sup.8.2#k24`, `sup.8.2#k42`; `opd.3b#d7`, `opd.3b#q7`, `opd.3b#c2`, `opd.8#k19` | The largest addition the §3b pass made. The same patient, at the same moment, decides whether to redeem a test here and whether to fill a prescription here, and the mechanism is identical — but the two are owned, measured and fixed by different departments in every hospital. `opd.3b#c2` names this as the most commonly missed row in that file's map. |
| Closed-system and reagent-rental equipment contracts | `sup.3b#d10`, `sup.3b#d11`, `sup.7.2.3#q30`–`#q34`, `sup.7.3#p10`, `sup.8.2#k40`; `opd.3b#d8`, `opd.3b#q8`; `opd.3#d14` | Owned by Supply Chain, and the live seam with the capital-procurement file (Part 2). OPD feels it as an uncompetitive cost-per-test and as downtime; Supply Chain holds the explanation, which is a capital decision made once by Biomedical. `sup.8.2#k40` is the only measure of how much of the cost base is unnegotiable. |
| Housekeeping — cleaning speed vs the notification and ready-confirmation moments | `dis.3b#d8`, `dis.3b#q7`, `dis.8#k17`; `bed.3b#d2`, `bed.3b#q2`, `bed.8#k22`; `bed.6#f4`, `dis.3#d5`, `bed.3#d2`, `bed.8#k6`, `dis.8#k4` | Three distinct clocks that hospitals report as one. Discharge owns the *notification* gap (told late), Bed Management owns the *ready-confirmation* gap (cleaned but not released), and both departments' KPI #4/#6 measure only the middle stretch. Both gaps are now measured — `dis.8#k17` isolates the notification gap and `bed.8#k22` the ready-confirmation gap — so the two clocks either side of cleaning are separable for the first time. |
| Ward consumable-kit readiness as a condition on a bed being usable | `bed.3b#d9`, `bed.3b#q9`; `sup.3b#d15`, `sup.2#a29`, `sup.7.4.1.2#s7` | One edge, each file naming the half it owns: Bed Management names the kit as a readiness condition, Supply Chain names the forward-demand signal it needs from Bed Management to have stocked it. Neither states the full loop; read both. |
| OT as the shared downstream victim, via three different mechanisms | `sup.3b#d1`, `sup.3b#d2`, `sup.8.2#k35`; `bed.3b#d3`, `bed.3b#q3`, `bed.8#k23`; `dis.3b#d10`, `dis.3b#q9`; `dis.3#d11`, `bed.3#d10`, `common.shared-considerations#c6` | An OT late start or cancellation has three unrelated upstream causes, each owned elsewhere: the trolley wasn't picked (Supply Chain), the post-op bed wasn't reserved or was reserved too early (Bed Management), or the bed freed too late in the day to convert (Discharge). A query framed as an OT problem needs all three checked before OT itself. |
| ALOS (average length of stay) | `common.shared-considerations#c4`; `bed.7.3#p1`, `bed.3#d12`, `bed.8#k9`, `bed.7.4.1#p4`; `dis.3#d7`, `dis.8#k5`, `dis.7.4#s6`; `sup.8.2#k28` | Defined once in common as a baseline financial parameter. Bed carries it as a downstream dependency, a §7.3 parameter and a KPI; Discharge carries it as a Critical dependency and isolates the discharge-delay share of it (`dis.8#k5`). The 0.5-day reduction claim lives only in `dis.7.4#s6`. Supply Chain derives its EBITDA contribution from the same ALOS-hours arithmetic. |
| ARPOB (average revenue per occupied bed) | `common.shared-considerations#c3`; `dis.7.3#p1`, `dis.3#d8`, `dis.8#k10`, `dis.7.4.1#p2`; `bed.7.3#p1`; `sup.7.3#p9`, `sup.8.2#k27` | Definition in common. Discharge instantiates it most heavily, including the annualisation formula in `dis.7.4.1#p2`. Supply Chain uses it as a denominator for consumable cost, which is a different use of the same number. |
| Bed Occupancy and ICU Occupancy | `bed.7.3#p2`; `bed.8#k8`, `bed.1#a3`; `dis.7.3#p5`, `dis.7.3#p6`; `opd.3#d18`; `bed.3b#d11` | `bed.7.3#p2` is the owner and carries the rule that the two are tracked separately and never blended. `bed.3b#d11` adds the further caution that a midnight-census occupancy figure conceals intraday dead bed time, so occupancy must not be read as evidence the beds were earning. |
| Daily / Daily Average Revenue | `bed.7.3#p3`, `bed.3#d11`, `bed.8#k15`; `dis.7.3#p2`, `dis.3#d14`, `dis.8#k10`; `opd.3#d12` | The same aggregate line appears as a §7.3 parameter, a Critical downstream dependency and a KPI in all three departments. No file owns it; treat `common.shared-considerations` as the baseline block it belongs beside. |
| OT scheduling, OT Utilisation and OT Revenue | `common.shared-considerations#c6`; `bed.3#d6`, `bed.3#d10`, `bed.2#a13`, `bed.7.2.2#q3`, `bed.7.3#p4`; `dis.3#d11`, `dis.3#d12`, `dis.3#d13`, `dis.7.3#p3`, `dis.7.3#p4`, `dis.8#k11` | The OT-to-bed link is defined as a shared consideration in common. Bed sees OT as both an upstream need (post-op reservation) and a downstream victim (elective cancelled for want of a bed); Discharge sees the same OT slots as revenue freed by earlier discharge. Same theatre, three vantage points — and see the three-mechanism row above. |
| Dead bed time (bill finalisation → next bill initiation) | `bed.7.3#p5`; `bed.6#c1`, `bed.7.1#c7`, `bed.7.4.1#p3`, `bed.8#k20`, `bed.7.2.1#c5`, `bed.7.2.2#q11`, `bed.7.4.2#s8`, `bed.3b#d7`, `bed.3b#q7`; `dis.7.2.1#c1` | Owned by Bed — `bed.7.3#p5` is the definition. `dis.7.2.1#c1` is Discharge's single reference to it, and is the one that explains why a good Discharge TAT can still sit inside dead bed time. `bed.3b#d7` names the Billing coupling that makes it measurable at all. |
| Bed turnaround time (physical discharge → usably available bed) | `bed.8#k6`; `dis.8#k4`; `dis.7.2.1#q12`, `bed.6#f4`, `dis.2#a9`, `bed.2#a9` | The identical KPI, worded differently, in both departments' §8 lists. Neither is the definition; they are co-equal. Distinct from dead bed time — this clock is physical, that one is billing — and distinct again from the notification and confirmation gaps in the Housekeeping row above. |
| Discharge TAT — correct definition, ending at the next admission into that bed | `dis.7.2.1#q15`; `bed.7.1#c6`; `dis.7.2.1#q14`, `bed.7.1#c2`, `bed.7.2.2#q7`, `dis.8#k1`, `dis.3b#d6`, `dis.3b#q5` | Defined in Discharge (`dis.7.2.1#q15`) and restated verbatim in Bed (`bed.7.1#c6`) because Bed needs the same clock to test whether a claimed vacancy is real. `dis.3b#d6` adds why the figure is incomparable between hospitals at all: the TPA window may or may not be inside it. |
| Admission timestamps — bed allocation and physical admission, and Admission TAT | `bed.7.1#c4`, `bed.7.1#c8`–`bed.7.1#c12`, `bed.7.2.1#c4`, `bed.7.2.1#c6`, `bed.7.2.2#q10`, `bed.7.4.2#s7`, `bed.7.4.1#p1`, `bed.8#k19`; `dis.7.2#d4`, `dis.7.2.1#q13`, `dis.7.4.2#s8` | Bed owns the measurement, including the five-stage decomposition. Discharge asks for exactly the same timestamps from the other side. The same dependency on two tables, pointing opposite ways. |
| The Discharge–Bed double control | `bed.7.4#s6`, `bed.7.4.1#s4`, `bed.3b#d1`, `bed.3b#q1`; `dis.7.4.2#s5`, `dis.7.4.2#s8`, `dis.3b#d7`, `dis.3b#q6` | Bed names it as a control it applies to Discharge's timings; Discharge names it as downstream functions reading its agent's output directly. The §3b rows are the first statement of it as one reciprocal edge rather than two obligations, and both carry the same probe: reconcile bed by bed, not in aggregate. |
| The serialised shared team — discharges till 12–2 PM, then admissions at 4–8 PM | `dis.6#f5`; `bed.6#f5`; `dis.7.2.1#q16`, `bed.7.2.2#q8`; `dis.7.4.2#s7`, `bed.7.4.2#s1`, `bed.7.4#s4`; `bed.3b#d2` | One operational fact indexed eight times across two files — as a failure mode, as a verification question and as a fix, in each department. `bed.3b#d2` names the variant that survives a denial: a no-allocation-before-confirmed-ready rule reproduces the same late admissions by a different route. |
| Provisional discharge as a formally tracked 24-hour-advance signal | `dis.2#a1`, `dis.8#k3`; `bed.7.4#s3`, `bed.7.4.2#s3`, `bed.8#k10`; `common.shared-considerations#c7` | Discharge owns the activity (early flagging) and measures how many discharges it triggers. Bed owns the service level demanded of it — 24 hours in advance — and measures the same signal as an inbound percentage. |
| ICU step-down signal and step-down mapping | `common.shared-considerations#c8`; `bed.3#d4`, `bed.2#a6`, `bed.7.2.2#q5`, `bed.7.4#s10`, `bed.7.4.1#s3`, `bed.7.4.2#s3`, `bed.8#k3`, `bed.8#k11`, `bed.3b#d4`; `dis.3#d9` | The mapping requirement is defined in common. Bed instantiates it fully, down to the 1 PM signal deadline. `bed.3b#d4` adds the mechanism behind why ICU beds free in bursts: step-down is decided on a round, not in a queue. |
| Mapping planned admissions against provisional discharges and expected bed availability | `common.shared-considerations#c7`; `bed.7.2.2#q4`, `bed.7.4#s2`, `bed.7.4.1#s2`, `bed.7.4.1#s7`, `bed.8#k1`, `bed.8#k2` | Defined in common as a shared consideration; Bed is where it becomes an actual daily mechanism with a 2 PM pass and a 6 PM freeze. |
| Bed availability for admission ↔ timely bed release — the same edge, opposite directions | `bed.3#d1`; `dis.3#d10`; `bed.3#d8`, `bed.3#d9`, `bed.8#k7`, `bed.2#a8` | `bed.3#d1` lists Discharge as Bed's Critical upstream; `dis.3#d10` lists Bed Availability as Discharge's Critical downstream. One dependency, entered twice from either side. |
| Housekeeping and transport turnaround capacity | `common.peak-load#k5`; `bed.3#d2`, `bed.7.1#c3`, `bed.7.2.1#c2`, `bed.8#k17`, `bed.6#f4`; `dis.3#d5`, `dis.3#d6`, `dis.7.1#c3`, `dis.7.2#d2`, `dis.8#k15`, `dis.3b#d9`; `opd.7.1.1#c7`, `opd.8#k13`, `opd.3b#d6`, `common.peak-load#k3` | The ratio method is owned by common. Bed and Discharge run it against the same staff pool for the same beds. OPD's version is a different duty for the same function: moving non-ambulatory patients to diagnostics, not turning beds. `dis.3b#d9` and `opd.3b#d6` add that the pool is shared across all of these with one peak. |
| Peak-load staffing ratio method and its named instances | `common.peak-load#s1`–`#s6`, `#n1`–`#n3`; instances `common.peak-load#k1`–`#k6`; run as `opd.7.1.1#c3`, `opd.7.1.1#c5`, `opd.7.1.1#c7`, `dis.7.1#c2`, `dis.7.1#c3`, `bed.7.1#c3`, `bed.7.1#c5`, `sup.7.1#c10`, `sup.7.2.3.2#q21`; measured as `opd.8#k10`, `opd.8#k12`, `opd.8#k13`, `dis.8#k14`, `dis.8#k15`, `bed.8#k17`, `bed.8#k21`, `sup.8.2#k30` | One method, defined once in common, with named ratios and then a third copy of each as an ongoing KPI in the department files. Supply Chain adds the only two-peak instance in the library: inbound receipt and outbound issue are different pools at different hours (`sup.7.1#c10`). `common.peak-load`'s own "which ratio applies where" list does not yet name it. |
| Staffing enables volume, not the reverse (the causality reversal) | `common.peak-load#f2`; `opd.7.1.2#c11`, `opd.0#f2`, `opd.6#f4`, `opd.7.2#q13`; `sup.7.2.3.2#q22`; `common.peak-load#n1` | Promoted to common as universal. OPD holds four separate instances of it; Supply Chain adds a fifth as a named probe in its HR cluster. |
| A single named owner of the process end-to-end | `common.shared-considerations#c2`; `dis.6#f4`, `dis.7.2.1#q9`, `dis.1#a1`, `dis.7.4.4#s3`; `bed.7.2.2#q2`, `bed.7.4#s1`; `opd.6#f3`, `opd.7.1.1#c4`; `sup.7.4.4#s1` | The check is defined in common. Each department names its own absence of one as a failure mode and its own creation of one as a fix. Supply Chain's version is the Materials Manager. |
| Whether the process is already automated — the maturity baseline | `common.shared-considerations#c1`; `dis.7.2.1#q10`; `bed.7.2.2#q1`; `opd.7.2#q8`; `sup.7.2.3.2#q19` | Defined in common; asked near-identically in every department's verification protocol. Supply Chain's variant is sharper: not whether a system exists, but whether it was built for perpetual inventory or adapted to it. |
| Enforced by the system vs configured as policy | `sup.3b#d16`, `sup.7.2.3.2#q17`, `sup.7.2.3.2#q18`, `sup.7.4.1#s11`, `sup.8.2#k44`; `bed.3b#d10`; `bed.4#n3` | Introduced by Supply Chain and the sharpest control distinction in the library: a rule the system refuses to complete, versus one people are asked to follow. `bed.3b#d10` is the same distinction applied to bed status, and it is what makes `bed.4#n3`'s no-phantom-vacancies non-negotiable structurally achievable rather than a matter of diligence. |
| **The 80% occupancy pivot** | `common.occupancy-pivot#c1`–`#c4`, `#s1`–`#s6`, `#n1`–`#n3`, `#p1`; `bed.7.4.4#c3`, `bed.7.4#c2`; `dis.7.4.4#s4`, `dis.7.2.1#q15`; `sup.7.4.4#s2`; `opd.7.4.4#s20` | **Owned by common.** One hospital-wide state change, not three departments' separate thresholds — it appeared independently in three files before being promoted. Above it, each function needs a *different* strategy and each warrants its own dedicated owner. `opd.7.4.4#s20` is the documented exception: OPD is ambulatory and scales with footfall, so the pivot reaches it only via OP-to-IP conversion. `bed.7.4#c2` is a sharper department-specific pivot that coexists with it rather than competing. |
| The dedicated owner role each function gets at the pivot | `common.occupancy-pivot#s5`, `#p1`, `#n1`, `#n2`, `#n3`; `dis.7.4.4#s3`, `dis.7.4.4#p1`; `bed.7.4.4#s1`, `bed.7.4.1#p6`; `sup.7.4.4#s1`, `sup.7.4.4#p1`; `opd.7.4.3#s10`, `opd.7.4.4#s16`, `opd.7.4.4#s17` | Same trigger, different role, **different price**. Materials Manager ₹8–10 lakhs; Bed Manager and Discharge Manager ₹4–4.5 lakhs each; OPD's Scheduling Manager on its own footfall trigger with no figure yet. The salary follows the proficiency the role requires, not the threshold that surfaced it — `common.occupancy-pivot#n2` is the instruction not to benchmark one against another, and it is the error a hospital will make unprompted. |
| Two separate role decisions, triggered and priced differently — don't collapse them | `dis.7.4.4#s2`; `bed.7.4.4#c1` | The identical instruction, in near-identical words, in two files. Treat `dis.7.4.4#s2` as the earlier statement. |
| The volume-sized Executive hire at ₹3–3.5 lakhs/year each | `dis.7.4.4#s5`, `dis.7.4.4#p2`, `dis.7.4.4#s6`, `dis.7.4.4#s7`, `dis.7.4.4#s9`; `bed.7.4.4#s2`, `bed.7.4.1#p7`, `bed.7.4.4#c6` | Discharge Executives and Admissions Executives are the same hire at the same price, sized by the same peak-load check. The sizing rules differ in form — a flat 15 discharges/day rule in Discharge, a 5-admissions-per-hour throughput plus a coverage floor in Bed. |
| Role-threshold tracking as its own KPI | `dis.8#k13`; `bed.8#k16`; `opd.8#k15`; `sup.8.2#k31` | All four departments track their own hiring trigger as an operational metric. `bed.8#k16` was realigned to `bed.7.4.4`(a)'s three current conditions on 2026-09-22 and is no longer stale. |
| Head of Operations / COO approves the process flows, not daily tasks | `dis.7.4.3#s6`; `bed.7.4.3#c1`; `sup.7.4.3#s9` | Word-for-word the same governance point in three departments' key-people sections. Supply Chain adds the reporting-line question behind it (`sup.3a#c2`). |
| Reporting line as a diagnostic — Operations vs Finance | `sup.3a#c1`–`#c4`, `sup.7.1#c1`, `sup.7.2.3#q23`, `sup.8.2#k32` | Supply Chain only, and a promotion candidate for common-elements rather than a cross-department concept yet. Recorded here so the next department that raises an ownership-structure question can be checked against it. |
| OPD prescription capture as the intake point for planned-admission data | `opd.2#a1`, `opd.7.4.1#s1`, `opd.7.4.2#s5`, `opd.3b#d9`, `opd.3b#q9`, `opd.8#k22`; `bed.7.4#s5`, `bed.7.4.2#s4`, `bed.8#k13`, `bed.3b#d6`, `bed.3b#q6` | OPD owns the capture activity and the bot that reads it. Bed consumes the same artefact as the start of its planned-admission pipeline and measures whether it arrives. Now stated as one edge from both ends via the §3b rows, where previously it was stated only from each end separately. |
| The four-aspect solution shape and its mandatory cost-benefit and before/after graphic | `common.solution-method#s1`–`#s4`, `#n1`–`#n4`; `dis.7.4#s1`, `dis.7.4#s2`; `opd.7.4#n1`; `sup.7.4#s1`; `play.3#s1`, `play.3#s2` | Defined in common. Discharge restates it as its own requirement; OPD re-orders it (process and manpower first) without changing the set; the playbook turns the same four plus KPIs into the five clickable parts. |
| Whether the solution scales with hospital size | `dis.7.4#s3`; `common.solution-method#f1`; `bed.7.4#c1`, `bed.7.4#c2`, `bed.7.4#c3`; `sup.7.4#s1`, `sup.7.4#s2`, `sup.7.4#s3` | Discharge's finding is that the solution is size-invariant; Bed's is the counter-case. Supply Chain is the third data point and the most refined: the solution scales, but the *automation* within it does not — only its configuration and surrounding staffing do (`sup.7.4#s2`). A retriever answering "does this hold for a smaller hospital?" needs all four. |
| Reserved capacity held vacant with a defined release rule | `bed.7.4#s8`, `bed.7.4.1#s5`, `bed.8#k5`, `bed.3b#d5`, `bed.3b#q5`; `opd.7.1.2#c12`, `opd.7.4.1#s3`, `opd.7.4.2#s7`, `opd.8#k6`; `sup.7.4.1#s6` | The emergency bed reserve and the STAT diagnostic slot are the same mechanism applied to different resources. Supply Chain's shortage-allocation rule is the third instance: hold priority, not capacity. OPD states the release rule precisely; Bed states the derivation precisely; each is missing what the other has. |
| Flagging Tojo's own constructed numbers as constructions | `bed.7.4.1#c2`; `play.2#n1`, `play.0#n2`, `play.8#n1` | The playbook owns the rule; `bed.7.4.1#c2` is the only department file that states it independently, and adds the "don't carry figures across hospitals" half. |
| IT/HIS extraction and integration as a prerequisite | `bed.3#d7`, `bed.7.4.2#s6`, `bed.7.4.1#p9`; `dis.7.4.2#s3`, `dis.7.4.3#s1`; `opd.3#d9`, `opd.7.4.3#s14`; `sup.3#d3`, `sup.7.5#f5`, `sup.7.4.3#s1` | Each department names the same IT work as its own prerequisite and its own cost line. `sup.7.5#f5` is the one that says plainly it is *one* integration, not four. |
| Doctors as the concentrated point of resistance | `bed.7.4.3#c2`, `bed.7.4.3#s1`, `bed.7.4.3#s2`; `dis.7.4.3#s3`, `dis.7.4.3#s7`; `opd.7.4.3#s11`, `opd.7.4.3#s12`; `sup.7.5#f9`; `common.solution-method#s3`; `play.4#s4`, `play.4#s5` | Common defines buy-in as an aspect; each department names doctors as where it concentrates. Supply Chain adds a distinct variety: surgeon resistance to documenting a preference card, because documenting it makes their cost comparable with a peer's — a status objection, not a workload one, and the standard mitigation does not work on it. |
| Resistance where the current ambiguity is a feature | `sup.7.5#f10`, `sup.3b#d17`, `sup.7.1#c9`; `opd.7.1.2#c14`, `opd.7.2#q1` | Supply Chain states it plainly for shrinkage; OPD states it for deliberate patient diversion. The only two places the library names resistance that is not workload-based, and both note that the "extension of your role" framing does not resolve it. |

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

## bed.3b

| point | what it is | chunk | also called |
|---|---|---|---|
| bed.3b#c1 | Bed Management's exposure is its own numbers being unbelievable | bed.3b | the board says one thing, the wards say another |
| bed.3b#d1 | (A) Discharge — the double control on each other's timestamps | bed.3b | cross-checking discharge timings, neither number is the finding |
| bed.3b#d2 | (B) Housekeeping — the ready-confirmation, not the cleaning speed | bed.3b | bed clean but not released, waiting for confirmation |
| bed.3b#d3 | (C) OT Scheduling — post-op reservation pulling both ways | bed.3b | holding beds for surgery, reserved beds sitting empty |
| bed.3b#d4 | (D) ICU — step-down gated by a rounds schedule, not a queue | bed.3b | ICU frees up only after rounds, no step-down queue |
| bed.3b#d5 | (E) Emergency — an untested reserve forces an unrecognised choice | bed.3b | how many beds to keep for emergencies, boarding or bumping |
| bed.3b#d6 | (F) OPD — the prescription is the planned-admission intake point | bed.3b | admissions arriving as surprises, no forecast input |
| bed.3b#d7 | (G) Billing — the bill-close/bill-open join makes dead bed time measurable | bed.3b | nobody reports the idle hours, hidden loss |
| bed.3b#d8 | (H) Nursing — allocation ignoring ward nurse-to-patient ratio | bed.3b | wards refusing beds, dumping into an overloaded ward |
| bed.3b#d9 | (I) Supply Chain — the ward consumable kit as a condition on usability | bed.3b | bed ready but no stock, marked ready then wasn't |
| bed.3b#d10 | (J) IT/HIS — status as a captured event vs. an entry someone makes | bed.3b | board drifts within hours, phantom vacancy |
| bed.3b#d11 | (K) Finance — midnight-census occupancy hiding intraday loss | bed.3b | occupancy looks fine but revenue per bed doesn't |
| bed.3b#q1 | (A) reconcile one day's discharges bed by bed, not in aggregate | bed.3b | check them one by one, averages hide it |
| bed.3b#q2 | (B) time from cleaning complete to allocatable, and who confirms | bed.3b | who releases the bed in the system |
| bed.3b#q3 | (C) when a post-op bed is reserved, and how many went unused | bed.3b | reservation timing, wasted holds |
| bed.3b#q4 | (D) when ICU rounds happen, and is there a step-down queue at all | bed.3b | rounds timing, how step-down is decided |
| bed.3b#q5 | (E) how the reserve number was arrived at, and how often it failed | bed.3b | where did that number come from, was it ever tested |
| bed.3b#q6 | (F) share of planned admissions known over 24 hours ahead, and from where | bed.3b | how much notice we get, where the data comes from |
| bed.3b#q7 | (G) bill-close and next bill-open on the same bed, and has anyone looked | bed.3b | the gap nobody has measured |
| bed.3b#q8 | (H) does allocation consider ward nursing ratio, and how often wards push back | bed.3b | do we check the ward's load, refusals recorded |
| bed.3b#q9 | (I) has a bed been marked ready then found unusable, and how recorded | bed.3b | ready then not ready, how it was logged |
| bed.3b#q10 | (J) is a status change a system event or typed in, and when last audited | bed.3b | who updates the board, physical walk-round check |
| bed.3b#q11 | (K) when occupancy is measured, and compared against billable bed-hours | bed.3b | census timing, occupancy versus earning |
| bed.3b#c2 | treat the contradiction as the symptom and find the coupling behind it | bed.3b | two numbers that don't agree, where to start |

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
| bed.8#k16 | Bed Manager threshold — demand-vs-supply pivot, 80% occupancy pivot, TAT-overrun rate | bed.8 | are we past the bed manager trigger, when do we hire |
| bed.8#k17 | housekeeping/transport staff available per shift per bed, for admissions and discharges | bed.8 | cleaning and porter staffing per shift, staff per bed |
| bed.8#k18 | nursing workload distribution relative to occupancy/turnover volume | bed.8 | nurse workload versus occupancy, ward staffing balance |
| bed.8#k19 | Admission TAT headline against the 30-minute target, plus five stage timings | bed.8 | how long an admission takes, stage-wise breakup |
| bed.8#k20 | dead bed time bill-to-bill, three stretches separable, with % admitted by noon | bed.8 | idle bed hours, when the bed stops and starts earning |
| bed.8#k21 | admissions plus internal transfers per team member per hour, peak vs off-peak | bed.8 | desk workload, how many one person handles |
| bed.8#k22 | housekeeping ready-confirmation gap, separate from cleaning time | bed.8 | release delay not cleaning delay, bed clean but not allocatable |
| bed.8#k23 | post-op bed reservations held but unused — count and bed-hours | bed.8 | cost of reserving early, wasted holds |
| bed.8#k24 | % of allocations checked against ward nursing ratio, and push-backs with reason | bed.8 | do we check the ward's load before allocating |

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

## dis.3b

| point | what it is | chunk | also called |
|---|---|---|---|
| dis.3b#c1 | Discharge is the last visible step, so upstream delays surface as its symptom | dis.3b | discharge gets blamed, it's not really us |
| dis.3b#d1 | (A) Doctors — the summary-authoring chain, and rounds timing gating the start | dis.3b | waiting for the consultant's round, who writes the summary |
| dis.3b#d2 | (A) multidisciplinary cases have no summary owner at all | dis.3b | several doctors on one case, nobody signs |
| dis.3b#d3 | (B) Nursing — the ward stock-take as a hard gate on billing closure | dis.3b | billing waiting for the ward count |
| dis.3b#d4 | (C) Supply Chain — the returnable balance, computed or counted | dis.3b | pending pharmacy reconciliation, medicine returns |
| dis.3b#d5 | (D) Billing — a late charge reopening a finalised bill | dis.3b | bill revised after closing, charge came in late |
| dis.3b#d6 | (E) Insurance/TPA — a window outside our control, inside or outside the TAT | dis.3b | does the TAT include the insurance wait |
| dis.3b#d7 | (F) Bed Management — the double control on each other's timestamps | dis.3b | good TAT but beds don't turn over, cross-checking timings |
| dis.3b#d8 | (G) Housekeeping — the notification moment, not the cleaning speed | dis.3b | when housekeeping was told, not how fast they clean |
| dis.3b#d9 | (H) Transport — porters pooled across every demand, one peak | dis.3b | waiting for a wheelchair, the last twenty minutes |
| dis.3b#d10 | (I) OT Scheduling — the admission-hour gate on same-day slots | dis.3b | bed freed too late for tonight's list, empty evening slots |
| dis.3b#d11 | (J) the briefing chain — several uncoordinated people before exit | dis.3b | dietitian, counselling, pharmacy advice before leaving |
| dis.3b#d12 | (K) Finance/cash counter — peak staffing and release authority | dis.3b | queue at the counter, who can let them go with a balance |
| dis.3b#q1 | (A) who drafts, reviews and signs — and who owns a multidisciplinary case | dis.3b | who actually writes it, who takes responsibility |
| dis.3b#q2 | (B) how long after confirmation does the stock-take start, and why | dis.3b | the gap before the count starts |
| dis.3b#q3 | (C) median time to post the return credit, and discharges waiting on it | dis.3b | how long returns take, how many are stuck |
| dis.3b#q4 | (D) how many bills were reopened last month, and by what charge | dis.3b | bill revisions, what came in late |
| dis.3b#q5 | (E) does the reported TAT include the TPA window end to end | dis.3b | is the insurance time counted |
| dis.3b#q6 | (F) reconcile the same beds against Bed Management's own timestamps | dis.3b | check our times against the bed team's |
| dis.3b#q7 | (G) time from physical discharge to housekeeping being notified | dis.3b | when did they actually get told |
| dis.3b#q8 | (H) porters on duty at the discharge peak, and what else they serve | dis.3b | porter availability at the busy hour |
| dis.3b#q9 | (I) latest hour a freed bed can still become a same-day OT slot | dis.3b | cut-off for tonight's surgery |
| dis.3b#q10 | (J) who must reach the patient before exit, and who sequences them | dis.3b | who all has to see the patient first |
| dis.3b#q11 | (K) counter staff at peak, and who authorises release with a balance | dis.3b | cash counter manning, settlement authority |
| dis.3b#c2 | treat a query's stated cause as the symptom column, then run that probe | dis.3b | they already think they know the reason |

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
| dis.7.2#c1 | run the §3b probe alongside these when the query came from another function | dis.7.2 | starting from another department's complaint |

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
| dis.8#k13 | all three Discharge Manager conditions — 80% pivot, >40 discharges/day, TAT-overrun rate | dis.8 | are we past the threshold for hiring, do we qualify for a discharge manager |
| dis.8#k14 | nursing ratio per bed for discharge functions, discharges per staff per hour peak vs off-peak | dis.8 | workload per nurse, how many discharges one person handles |
| dis.8#k15 | housekeeping and transport staff availability per shift vs. discharge volume | dis.8 | enough housekeeping per shift, porter availability |
| dis.8#k16 | family/patient briefing completion rate before physical discharge | dis.8 | how often counselling was actually done, documented instructions before leaving |
| dis.8#k17 | housekeeping notification gap, tracked separately from cleaning time | dis.8 | when housekeeping was told versus how fast they clean |
| dis.8#k18 | bills reopened after finalisation — count, value and the charge type | dis.8 | bill revisions, what keeps coming in late |
| dis.8#k19 | transport wait from full clearance to the patient physically leaving | dis.8 | the last twenty minutes, waiting for a wheelchair |
| dis.8#k20 | cash-counter settlements per staff per hour at peak, and discharges held by a disputed balance | dis.8 | queue at the counter, who can release with a balance |

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

## opd.3b

| point | what it is | chunk | also called |
|---|---|---|---|
| opd.3b#c1 | diagnostic leakage has no symptom of its own — nothing breaks, nobody complains | opd.3b | we only see it in the revenue, silent loss |
| opd.3b#d1 | (A) Doctors and secretaries — who owns the patient in the thirty seconds after the consult | opd.3b | secretary takes the patient, we can't step in |
| opd.3b#d2 | (B) Radiology — per-unit capacity, not modality capacity | opd.3b | one machine overloaded while another is free |
| opd.3b#d3 | (C) Laboratory — report turnaround as a trust signal to the prescribing doctor | opd.3b | doctor stopped sending tests here, burned once |
| opd.3b#d4 | (D) Billing and front office — the billing desk is the conversion window | opd.3b | staff take payment and point at a corridor |
| opd.3b#d5 | (E) Guest services — the physical journey from consult to diagnostic to payment | opd.3b | nobody walks the patient, they wander off |
| opd.3b#d6 | (F) Housekeeping and transport — mobility for non-ambulatory patients at peak | opd.3b | no wheelchair, slot missed and logged as a no-show |
| opd.3b#d7 | (G) Pharmacy and Supply Chain — reagent availability, and pharmacy leakage as the same mechanism | opd.3b | same problem at the medicine counter, two halves of one thing |
| opd.3b#d8 | (H) Biomedical — equipment downtime converting directly into leakage | opd.3b | the MRI was down, bad month for scans |
| opd.3b#d9 | (I) Bed Management — OP-to-IP conversion, and OPD as planned-admission intake | opd.3b | admissions from findings, feeding the bed forecast |
| opd.3b#d10 | (J) HR — training ownership and the blame culture | opd.3b | conversion varies by shift, who trains the counter staff |
| opd.3b#d11 | (K) Finance — equipment ROI and authority over off-peak pricing | opd.3b | who can approve a discount, who owns the payback case |
| opd.3b#q1 | (A) for the three lowest-redemption doctors, who books the next step | opd.3b | ask about those doctors specifically |
| opd.3b#q2 | (B) utilisation per individual unit, and which unit a walk-in lands on | opd.3b | machine-wise load, who decides where it goes |
| opd.3b#q3 | (C) report turnaround against redemption by doctor over six months | opd.3b | has any doctor ever complained about report delay |
| opd.3b#q4 | (D) what staff say to a patient after payment, and does TAT include it | opd.3b | does the transaction end at the receipt |
| opd.3b#q5 | (E) guest-services headcount at peak, and same-visit bookings not attended | opd.3b | who is on during the rush, booked but didn't turn up |
| opd.3b#q6 | (F) mobility-assistance volume, wait time, and whether a missed slot was attributed | opd.3b | wheelchair waits, was it ever recorded as the cause |
| opd.3b#q7 | (G) in-house dispensing share compared against diagnostic redemption | opd.3b | pharmacy conversion next to test conversion |
| opd.3b#q8 | (H) equipment downtime by unit against redemption in the same weeks | opd.3b | put the breakdown log next to the numbers |
| opd.3b#q9 | (I) share of OPD-originated planned admissions reaching Bed Management 24h ahead | opd.3b | how much notice the bed team gets from us |
| opd.3b#q10 | (J) who trains the handoff, who checks it, and who is asked first on a complaint | opd.3b | training ownership, who gets blamed |
| opd.3b#q11 | (K) who can approve an off-peak discount, and who sees redemption data | opd.3b | pricing authority, who owns the machine's payback |
| opd.3b#c2 | the most commonly missed row is G — pharmacy and diagnostic leakage are one mechanism | opd.3b | fixing half the problem, two departments one cause |

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
| opd.7.1.1#c8 | the two-peak arrival curve — ~80% of footfall inside ~4 peak hours split across two shifts, not one block | opd.7.1.1 | when do the crowds actually come, morning rush and evening rush, peak hours at the counter, is the load even through the day |
| opd.7.1.1#c9 | derive the real arrival curve from hourly OPD billing data, never from registration data | opd.7.1.1 | where do we get the arrival pattern from, registration only counts new patients, how do we count returning patients |

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
| opd.7.2#q15 | who owns floor-staff training — HR, departmental head, floor managers or COO — and how that ownership is evidenced, monitored and analysed | opd.7.2 | whose job is it to train the counter staff, nobody owns training, is training recorded anywhere, who is accountable for the floor staff |
| opd.7.2#c1 | run the §3b probe alongside these when the query came from another function | opd.7.2 | starting from another department's complaint |

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
| opd.7.4.3#s13 | HR to check staffing adequacy and training effectiveness, and to settle who owns training where §7.2 point 15 found no named owner | opd.7.4.3 | HR to confirm headcount, is the training actually working, who should own training |
| opd.7.4.3#s14 | IT for all automations and integrations including ERP value extraction | opd.7.4.3 | IT team, integration with our HIS and ERP |
| opd.7.4.3#s15 | executive management sign-off on open sharing of performance dashboards | opd.7.4.3 | management approval to share the numbers openly, CEO buy-in |

## opd.7.4.4

| point | what it is | chunk | also called |
|---|---|---|---|
| opd.7.4.4#s16 | Scheduling Manager is the clear new recruitment above 200 daily footfall | opd.7.4.4 | new post for scheduling, recruit a scheduling manager |
| opd.7.4.4#s17 | Scheduling Manager cost scales with footfall across three bands — ₹3–3.5L (200–500), ₹5.5–6L (500–1,500), ₹7–7.5L (above 1,500) | opd.7.4.4 | what will that role cost us, salary for the new post, how much does a scheduling manager cost, budget for the scheduling role |
| opd.7.4.4#s18 | guest-services headcount may be new, sized by peak-load ratio check | opd.7.4.4 | how many PROs do we need, adding guest relations staff |
| opd.7.4.4#s19 | all other named roles are existing ones engaged, not new recruitment | opd.7.4.4 | no other new hiring, using our existing people |
| opd.7.4.4#s20 | OPD is the exception to the 80% occupancy pivot — ambulatory load scales with footfall | opd.7.4.4 | does the occupancy rule apply to us, busy counter but empty wards |
| opd.7.4.4#s21 | salary follows the proficiency the volume demands, not the fact that a threshold was crossed | opd.7.4.4 | why does the same role cost more at a bigger hospital, paying more for the same job title |

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
| opd.8#k19 | OPD prescription-to-pharmacy fill rate, reported beside diagnostic redemption | opd.8 | how many prescriptions we fill, medicine counter conversion |
| opd.8#k20 | equipment downtime by unit set against redemption in the same period | opd.8 | the scanner was down, bad month for scans |
| opd.8#k21 | tests deferred for want of a reagent, recorded under that cause not as a no-show | opd.8 | test couldn't run, no reagent, logged as patient didn't come |
| opd.8#k22 | % of OPD-originated planned admissions reaching Bed Management over 24h ahead | opd.8 | how much notice the bed team gets from us |

### sup.points.md — Supply Chain & Procurement
## sup.0

| point | what it is | chunk | also called |
|---|---|---|---|
| sup.0#c1 | vendor, stores, ERP, procure-to-pay and billing are one continuous chain | sup.0 | it's all connected, one long process from supplier to bill |
| sup.0#c2 | a query naming one link is usually a query about this whole department | sup.0 | the problem isn't where it looks like it is |
| sup.0#c3 | capital procurement is deliberately out of scope, in a separate file | sup.0 | equipment buying is different, machines vs consumables |

## sup.1

| point | what it is | chunk | also called |
|---|---|---|---|
| sup.1#a1 | every item available at the point of need, no patient waits on a stock-out | sup.1 | never run out, stock always on the floor |
| sup.1#a2 | at a negotiated and controlled cost | sup.1 | buying at the right rate, controlling purchase price |
| sup.1#a3 | unbroken system record from vendor to patient, always reconcilable | sup.1 | full traceability, being able to tie it all back |

## sup.2

| point | what it is | chunk | also called |
|---|---|---|---|
| sup.2#a1 | vendor sourcing, empanelment and approval | sup.2 | finding suppliers, adding a new vendor |
| sup.2#a2 | category-wise negotiation and rate-contract finalization | sup.2 | rate contracts, annual price negotiation |
| sup.2#a3 | MOQ and payment-terms/credit-period negotiation | sup.2 | minimum order quantity, credit period, payment terms |
| sup.2#a4 | vendor scorecarding on fill rate, OTIF and quality rejection | sup.2 | rating our suppliers, which vendor is reliable |
| sup.2#a5 | gate entry, invoice/challan match against the PO at receipt | sup.2 | material coming in at the gate, checking the challan |
| sup.2#a6 | batch-number and expiry verification at receipt | sup.2 | checking batch and expiry when goods arrive |
| sup.2#a7 | Goods Receipt Note creation in the ERP | sup.2 | GRN, booking the receipt in the system |
| sup.2#a8 | discrepancy, short-receipt and damage handling, vendor debit note | sup.2 | short supply, damaged goods, raising a debit note |
| sup.2#a9 | item master maintenance | sup.2 | item codes, the material master |
| sup.2#a10 | store and sub-store stock ledgers | sup.2 | ward stock, floor stock, store registers |
| sup.2#a11 | physical stock-taking and cycle counts | sup.2 | stock count, physical verification |
| sup.2#a12 | ROL/ROQ monitoring and replenishment triggers | sup.2 | reorder level, when to reorder, minimum stock |
| sup.2#a13 | ABC-VED classification and differentiated stocking policy | sup.2 | vital essential desirable, classifying items by criticality |
| sup.2#a14 | near-expiry, expiry, slow-moving and dead-stock management | sup.2 | expiring stock, items not moving, dead inventory |
| sup.2#a15 | item-master governance — one item, one code, one master | sup.2 | duplicate codes, same item twice, single master |
| sup.2#a16 | store/sub-store hierarchy design | sup.2 | central store, pharmacy store, ward sub-store structure |
| sup.2#a17 | user-rights configuration for indent, approval, transfer, returns | sup.2 | who can raise an indent, system rights |
| sup.2#a18 | conflict and priority resolution for constrained shared items | sup.2 | two wards want the same thing, who gets it |
| sup.2#a19 | indent aggregation into a consolidated purchase requirement | sup.2 | clubbing indents, consolidating requirements |
| sup.2#a20 | PO creation, system-generated or manually raised for exceptions | sup.2 | raising a purchase order, auto PO |
| sup.2#a21 | approval authority for a new vendor and a negotiated rate | sup.2 | who approves a vendor, who signs off on rates |
| sup.2#a22 | three-way match of indent/PO, GRN and invoice before payment | sup.2 | three way matching, checking before we pay |
| sup.2#a23 | issue of stock against an indent or requisition | sup.2 | issuing to the ward, giving out stock |
| sup.2#a24 | point-of-care consumption recording | sup.2 | recording what was actually used at the bedside |
| sup.2#a25 | real-time linkage of issued and consumed items to the running bill | sup.2 | charging it to the patient as it's used |
| sup.2#a26 | returns processing for unused, unopened, in-date stock | sup.2 | returning medicines, pharmacy refund |
| sup.2#a27 | write-off treatment for part-used, non-returnable items | sup.2 | opened but not fully used, wastage |
| sup.2#a28 | OT preference cards / bill-of-materials definition | sup.2 | surgeon's list, case cart, what goes on the trolley |
| sup.2#a29 | standardised bed and ICU daily-issue kits | sup.2 | daily kit, per bed-day consumables |
| sup.2#a30 | billing-package presumed-consumption lists and their reconciliation | sup.2 | package rates, what's assumed inside a package |
| sup.2#a31 | OPD walk-in retail sale — cash/card/insurance, immediate invoicing | sup.2 | pharmacy counter sale, outpatient pharmacy |
| sup.2#a32 | IPD credit issue against the patient's running bill | sup.2 | ward issue, charging to the inpatient bill |
| sup.2#a33 | daily reconciliation of revenue booked against cost of goods issued | sup.2 | daily pharmacy P&L, same-day reconciliation |
| sup.2#a34 | inventory-linked working-capital monitoring | sup.2 | money tied up in stock, working capital in inventory |

## sup.3

| point | what it is | chunk | also called |
|---|---|---|---|
| sup.3#d1 | Finance — budget, payment release, credit-term mandate, working capital (Critical) | sup.3 | finance holding up payments, budget approval |
| sup.3#d2 | Clinical/Nursing/OT/ICU — indent origination, the entire pull side (Critical) | sup.3 | the wards raising requirements, where demand starts |
| sup.3#d3 | IT/ERP — item master, store configuration, rights, real-time capture (Critical) | sup.3 | our HIS, the ERP, system limitations |
| sup.3#d4 | Vendors — supply reliability, rate/MOQ/lead-time compliance, quality (Critical) | sup.3 | suppliers not delivering, vendor reliability |
| sup.3#d5 | Biomedical/Engineering — equipment-linked consumables, AMC spares (High) | sup.3 | reagents tied to a machine, spares under AMC |
| sup.3#d6 | Quality/Regulatory — drug licensing, Schedule H1/X, biomedical waste (High) | sup.3 | drug licence, narcotics rules, waste segregation |
| sup.3#d7 | Bed Management — forward occupancy and planned-admission picture (Medium-High) | sup.3 | knowing how full we'll be, upcoming admissions |
| sup.3#d8 | Housekeeping — linen and cleaning consumables on the same structure (Medium-High) | sup.3 | housekeeping materials, cleaning supplies |
| sup.3#d9 | Patient Billing — where most billing accuracy problems originate (Critical) | sup.3 | wrong bills, billing errors, items missed on the bill |
| sup.3#d10 | Discharge Process — real-time tracking is what makes its automation possible (Critical) | sup.3 | discharge waiting on pharmacy, slow discharge |
| sup.3#d11 | Clinical care continuity — a critical stock-out halts care (Critical) | sup.3 | running out of a life-saving drug, care delayed |
| sup.3#d12 | OT Scheduling & Utilisation — consumable readiness gates the start (High) | sup.3 | OT not starting on time, trolley not ready |
| sup.3#d13 | Finance / P&L and working capital — inventory is a major commitment (Critical) | sup.3 | too much money in stock, inventory investment |
| sup.3#d14 | Quality/Accreditation — NABH checks traceability and expiry directly (High) | sup.3 | NABH audit, accreditation evidence |
| sup.3#d15 | Pharmacy revenue (OPD retail) — a P&L line, not just a cost centre (High) | sup.3 | pharmacy income, retail counter revenue |
| sup.3#d16 | Nursing clinical time absorbed by stock work (High) | sup.3 | nurses doing stock counts, time away from patients |

## sup.3a

| point | what it is | chunk | also called |
|---|---|---|---|
| sup.3a#c1 | hospitals default to Finance ownership for historical, not ideal, reasons | sup.3a | purchase reports to finance, the CFO owns it |
| sup.3a#c2 | the ideal is COO reporting, with CFO approval only on rates, terms, accounting | sup.3a | should it sit under operations, who should this team report to |
| sup.3a#c3 | financial control can be built into the system rather than the reporting line | sup.3a | automating the financial checks instead of the structure |
| sup.3a#c4 | the gap between actual reporting line and the ideal is itself diagnostic | sup.3a | what their org chart tells you |

## sup.3b

| point | what it is | chunk | also called |
|---|---|---|---|
| sup.3b#c1 | cross-function failures are misattributed at the point they surface | sup.3b | blaming the wrong department, it's not where it shows up |
| sup.3b#d1 | (A) OT — the preference card is the interface between schedule and trolley | sup.3b | surgeon's list, case cart, what the OT needs ready |
| sup.3b#d2 | (A) the OT delay split — not in the hospital vs. not on the trolley | sup.3b | was it out of stock or just not sent up |
| sup.3b#d3 | (A) cancelled case leaves opened packs and consignment nobody writes off | sup.3b | surgery cancelled after opening the set |
| sup.3b#d4 | (B) Nursing — indent lead time creates the informal buffer drawer | sup.3b | nurses keeping their own stock, hidden ward stock |
| sup.3b#d5 | (B) nursing clinical time absorbed into stock work, counted as nursing cost | sup.3b | nurses doing store work, time lost to indenting |
| sup.3b#d6 | (C) Billing — item master and price master owned by different teams | sup.3b | purchase rate vs charge rate, two different masters |
| sup.3b#d7 | (D) Discharge — the returnable balance is the coupling | sup.3b | pending pharmacy reconciliation, waiting on returns |
| sup.3b#d8 | (E) Finance — the self-reinforcing payment-delay spiral | sup.3b | paying vendors late, suppliers deprioritising us |
| sup.3b#d9 | (E) spot-purchase premium is the measurable signature of that loop | sup.3b | emergency purchases costing more, buying at market rate |
| sup.3b#d10 | (F) Biomedical — closed-system contracts remove negotiating power for the machine's life | sup.3b | reagent rental, proprietary consumables, locked in |
| sup.3b#d11 | (F) AMC-covered spares also purchased separately, bought twice | sup.3b | paying twice for the same part |
| sup.3b#d12 | (G) Quality — a parallel manual record maintained for the audit | sup.3b | preparing files for NABH, audit-only records |
| sup.3b#d13 | (H) Pharmacy/OPD — formulary not reconciled against actual prescribing | sup.3b | we don't stock what our doctors write |
| sup.3b#d14 | (I) Housekeeping — its indents silently deprioritised, driving off-system buying | sup.3b | housekeeping buying on their own, parallel purchase |
| sup.3b#d15 | (J) Bed Management — reorder blind to known future demand | sup.3b | stock-outs we could have seen coming, no forecasting |
| sup.3b#d16 | (K) IT/ERP — enforced by the system vs. merely configured as policy | sup.3b | can people bypass it, is the rule actually checked |
| sup.3b#d17 | (L) HR — receipt and issue peaks staffed to average | sup.3b | store short-staffed at the busy hour, GRN piling up |
| sup.3b#c2 | when a query enters from another function, check the map before diagnosing | sup.3b | is this really our problem, where should we look first |

## sup.4

| point | what it is | chunk | also called |
|---|---|---|---|
| sup.4#n1 | no stock-out of a critical/emergency/life-saving item, ever | sup.4 | crash cart must be full, never run out of emergency drugs |
| sup.4#n2 | no expired item ever administered or dispensed | sup.4 | expired medicine reaching a patient |
| sup.4#n3 | no item billed that wasn't issued or consumed for that patient | sup.4 | charging for something not given |
| sup.4#n4 | drug-licence and controlled-substance compliance on every transaction | sup.4 | narcotics register, Schedule H1, licence conditions |
| sup.4#n5 | invoice rate must match the approved rate contract, no silent override | sup.4 | paying more than the contracted rate |
| sup.4#n6 | every issue traceable to an indent and a requisitioning authority | sup.4 | no off-the-book issues, everything on system |
| sup.4#n7 | cold-chain items under continuous temperature monitoring | sup.4 | vaccine fridge, temperature log |

## sup.5

| point | what it is | chunk | also called |
|---|---|---|---|
| sup.5#x1 | full stock-take cadence can extend for low-criticality Desirable items | sup.5 | counting the small stuff less often |
| sup.5#x2 | rate-contract renewal can slip for low-value, low-volume items | sup.5 | not renegotiating everything every year |
| sup.5#x3 | non-critical substitution within clinical protocol is acceptable | sup.5 | equivalent brand, generic alternative |
| sup.5#x4 | GRN system entry may trail physical receipt briefly, if stock is issuable | sup.5 | entering it in the system later, catching up on paperwork |

## sup.6

| point | what it is | chunk | also called |
|---|---|---|---|
| sup.6#f1 | phantom inventory — system shows stock that physically isn't there | sup.6 | system says we have it but we don't |
| sup.6#f2 | duplicate or store-local item masters breaking reorder and spend visibility | sup.6 | same item under two codes, each store's own list |
| sup.6#f3 | GRN backlog making the ERP stale when reorder decisions are made | sup.6 | receipts entered days later, system out of date |
| sup.6#f4 | off-system courtesy issue, the most common source of billing leakage | sup.6 | giving stock without an indent, emergency handouts |
| sup.6#f5 | the ward buffer drawer held outside the sub-store ledger | sup.6 | nurses' private stock, just-in-case drawer |
| sup.6#f6 | PO-to-invoice rate mismatch drifting unnoticed over time | sup.6 | paying a different rate than agreed |
| sup.6#f7 | expired stock at ward sub-store level, unmonitored | sup.6 | expiry in the ward cupboard, nobody checks the floor stock |
| sup.6#f8 | pilferage masked as adjustment or wastage entries | sup.6 | stock going missing, written off as wastage |
| sup.6#f9 | unreconciled part-used returns falling out of bill and ledger | sup.6 | half-used items nobody accounts for |
| sup.6#f10 | vendor concentration risk with no qualified backup | sup.6 | only one supplier, no alternative vendor |
| sup.6#f11 | stale price master disagreeing with the negotiated rate | sup.6 | system price is old, wrong rate in the master |
| sup.6#f12 | the payment-delay spiral, diagnosed at the wrong end | sup.6 | late payments causing supply problems |
| sup.6#f13 | audit-only parallel record diverging from the real process | sup.6 | records made for the audit, two sets of books |
| sup.6#f14 | predictable stock-outs, with the demand signal already in the hospital | sup.6 | we should have known, it was in the schedule |

## sup.7

Section container (heading only) — no points.

## sup.7.1

| point | what it is | chunk | also called |
|---|---|---|---|
| sup.7.1#c1 | reporting line (Operations vs Finance) is a live, high-leverage diagnostic | sup.7.1 | who owns purchase, does it sit under finance |
| sup.7.1#c2 | check §3b for a coupling before accepting the query's own framing | sup.7.1 | is this really a supply chain problem |
| sup.7.1#c3 | don't assume the EBITDA contribution has been quantified | sup.7.1 | have they put a number on it, or just a belief |
| sup.7.1#c4 | ask what efficiency means to them; propose the discharge-duration proxy | sup.7.1 | how do you measure efficiency here |
| sup.7.1#c5 | billing accuracy is decided here even though it surfaces at Billing | sup.7.1 | wrong bills start in the store |
| sup.7.1#c6 | consumables and capital procurement are genuinely different problems | sup.7.1 | buying machines vs buying supplies |
| sup.7.1#c7 | package billing is a silent margin-erosion risk, not a one-time price | sup.7.1 | package rates going underwater, consumption creeping up |
| sup.7.1#c8 | OPD and IPD pharmacy are different businesses sharing one stock pool | sup.7.1 | retail counter vs ward issue, which pharmacy revenue |
| sup.7.1#c9 | automation exposes shrinkage manual process kept ambiguous | sup.7.1 | some people don't want it visible |
| sup.7.1#c10 | two distinct staffing peaks — inbound receipt and outbound issue | sup.7.1 | morning deliveries, pre-OT rush, discharge returns |
| sup.7.1#c11 | retail practices worth carrying over — ABC-VED, OTIF, category owner, cycle counts, forecast-linked replenishment, central negotiation with decentralised fulfilment | sup.7.1 | what we can learn from retail, how big stores do it |

## sup.7.2

| point | what it is | chunk | also called |
|---|---|---|---|
| sup.7.2#c1 | the protocol runs in three parts: data, internal practice, couplings | sup.7.2 | how to work through this, what order to ask in |
| sup.7.2#c2 | when the query comes from another function, run the §3b cluster first | sup.7.2 | start from the other department's symptom |
| sup.7.2#c3 | the divergences carrying the largest effect are named explicitly | sup.7.2 | what matters most, where to focus |

## sup.7.2.1

| point | what it is | chunk | also called |
|---|---|---|---|
| sup.7.2.1#d1 | item master export across every store, with codes and creation dates | sup.7.2.1 | full item list, material master dump |
| sup.7.2.1#d2 | four quarters of purchase register, each line flagged contract vs spot | sup.7.2.1 | purchase history, what we bought and how |
| sup.7.2.1#d3 | vendor payment ledger — invoice, due and actual payment dates | sup.7.2.1 | when we actually paid, payment records |
| sup.7.2.1#d4 | GRN log with gate-entry and system-entry timestamps | sup.7.2.1 | when goods arrived vs when we booked them |
| sup.7.2.1#d5 | issue and consumption transactions by sub-store, plus cycle-count variance | sup.7.2.1 | ward issue records, count differences |
| sup.7.2.1#d6 | charge master and item master side by side, with revision dates | sup.7.2.1 | selling price list and purchase price list together |
| sup.7.2.1#d7 | OT schedule with booked vs actual starts and delay-reason codes | sup.7.2.1 | OT delay register, why cases started late |
| sup.7.2.1#d8 | installed-equipment list with consumable contract type | sup.7.2.1 | which machines, what reagent contract |
| sup.7.2.1#d9 | store, receiving and pharmacy rosters against hourly volume | sup.7.2.1 | store duty roster, who's on at what hour |
| sup.7.2.1#d10 | forward planned-admission and elective OT schedules | sup.7.2.1 | next week's list, upcoming admissions |

## sup.7.2.2

| point | what it is | chunk | also called |
|---|---|---|---|
| sup.7.2.2#q1 | have they quantified the EBITDA effect, or is it a general belief | sup.7.2.2 | have you put a number to it |
| sup.7.2.2#q2 | what is their working definition of efficiency, and how is it monitored | sup.7.2.2 | what does efficient mean here |
| sup.7.2.2#q3 | which retail supply-chain concepts have they adopted or rejected | sup.7.2.2 | anything learned from retail |
| sup.7.2.2#q4 | one de-duplicated item master, or a local list per store | sup.7.2.2 | single item master, does each store have its own codes |
| sup.7.2.2#q5 | is GRN entered at physical receipt, or does it batch and lag | sup.7.2.2 | when do you do the GRN |
| sup.7.2.2#q6 | is reorder automatic off ROL/ROQ or dependent on someone noticing | sup.7.2.2 | does the system tell you to reorder |
| sup.7.2.2#q7 | who can raise and approve an indent — enforced in the ERP or convention | sup.7.2.2 | indent rights, who signs off |
| sup.7.2.2#q8 | is inter-store transfer two-sided and confirmed by both ends | sup.7.2.2 | transfer between stores, does the receiver confirm |
| sup.7.2.2#q9 | what happens when two sub-stores indent the same scarce item | sup.7.2.2 | who gets it when there isn't enough |
| sup.7.2.2#q10 | is a PO auto-raised against an approved vendor/rate, or always manual | sup.7.2.2 | automatic purchase orders, straight-through PO |
| sup.7.2.2#q11 | who approves a new vendor, and who approves a negotiated rate | sup.7.2.2 | vendor approval committee, rate sign-off |
| sup.7.2.2#q12 | is three-way match enforced before payment release | sup.7.2.2 | do you check GRN before paying |
| sup.7.2.2#q13 | does costing distinguish landed cost, net of rebates, from invoice price | sup.7.2.2 | true cost of an item, freight and rebates |
| sup.7.2.2#q14 | is issued stock linked to the patient's bill in real time | sup.7.2.2 | does it hit the bill immediately |
| sup.7.2.2#q15 | is consumption tracked separately from issue, to a returnable unit | sup.7.2.2 | do you know what was actually used, not just sent |
| sup.7.2.2#q16 | what is the actual policy for a part-used, non-returnable item | sup.7.2.2 | opened strip, half-used bottle, who pays |
| sup.7.2.2#q17 | is OPD sale on a separate POS with separate margin reporting | sup.7.2.2 | is the counter separate from ward issue |
| sup.7.2.2#q18 | does anyone reconcile package consumption against the presumed BOM | sup.7.2.2 | checking what packages actually consume |
| sup.7.2.2#q19 | is there a daily revenue-vs-cost reconciliation by ward or department | sup.7.2.2 | daily not monthly reconciliation |
| sup.7.2.2#q20 | how is near-expiry surfaced at sub-store level, and can they show it now | sup.7.2.2 | ward expiry list, show me today's near-expiry |

## sup.7.2.3

| point | what it is | chunk | also called |
|---|---|---|---|
| sup.7.2.3#q1 | (A) what produces the trolley list — a documented card or a nurse's memory | sup.7.2.3 | is the surgeon's preference written down |
| sup.7.2.3#q2 | (A) how far ahead is the OT list frozen, and how do changes reach the store | sup.7.2.3 | last-minute case changes, how the store finds out |
| sup.7.2.3#q3 | (A) split last quarter's consumable-coded OT delays by actual cause | sup.7.2.3 | was it out of stock or not sent up |
| sup.7.2.3#q4 | (A) what happens to opened packs when a case is cancelled | sup.7.2.3 | cancelled surgery, opened set |
| sup.7.2.3#q5 | (A) consignment implants — ownership, billing moment, vendor invoice order | sup.7.2.3 | implant on consignment, when do we pay and charge |
| sup.7.2.3#q6 | (A) is OT consumption reconciled against the card or only the package | sup.7.2.3 | checking actual usage per surgery |
| sup.7.2.3#q7 | (B) actual indent-to-hand time, routine and urgent, as two numbers | sup.7.2.3 | how long from asking to getting it |
| sup.7.2.3#q8 | (B) is there an informal buffer held outside the sub-store ledger | sup.7.2.3 | hidden ward stock, private drawer |
| sup.7.2.3#q9 | (B) what actually happens when a drug is needed urgently at 2 AM | sup.7.2.3 | night emergency, store closed |
| sup.7.2.3#q10 | (B) is the person who counts the ward stock also accountable for shortages | sup.7.2.3 | who counts and who answers for it |
| sup.7.2.3#q11 | (B) nurse hours per shift on stock-taking, indenting and follow-up | sup.7.2.3 | how much nursing time goes on stores work |
| sup.7.2.3#q12 | (B) is missing ward stock recorded as loss, adjustment or wastage | sup.7.2.3 | what do you call it when stock goes missing |
| sup.7.2.3#q13 | (C) who owns the billable price and who owns the purchase price | sup.7.2.3 | two masters, who maintains each |
| sup.7.2.3#q14 | (C) what triggers a billable-rate review when a purchase rate changes | sup.7.2.3 | does the selling price get updated |
| sup.7.2.3#q15 | (C) what guarantees a new item exists in both masters before issue | sup.7.2.3 | new item created in one system only |
| sup.7.2.3#q16 | (C) who detects an item issued but never billed, and when | sup.7.2.3 | items missed on the bill, when do you catch it |
| sup.7.2.3#q17 | (C) does anyone compute realised margin against landed cost | sup.7.2.3 | real margin per item |
| sup.7.2.3#q18 | (D) who verifies returns at discharge, and is credit posted before the bill closes | sup.7.2.3 | return credit timing, before or after the final bill |
| sup.7.2.3#q19 | (D) median time to post the return credit, and discharges waiting on it | sup.7.2.3 | how long returns take, how many discharges stuck |
| sup.7.2.3#q20 | (D) is the returnable balance computed by the system or counted by a nurse | sup.7.2.3 | manual count at discharge |
| sup.7.2.3#q21 | (D) who decides on a part-used item at discharge, consistently or case by case | sup.7.2.3 | does every ward do it differently |
| sup.7.2.3#q22 | (D) does the hospital know what share of discharge time this step is | sup.7.2.3 | how much of the delay is pharmacy |
| sup.7.2.3#q23 | (E) who does the team report to, and would they move it to Operations | sup.7.2.3 | reporting line, finance or operations |
| sup.7.2.3#q24 | (E) actual payment-days-outstanding by vendor, from the ledger not the policy | sup.7.2.3 | how late do we actually pay |
| sup.7.2.3#q25 | (E) has any vendor raised rates, cut credit or deprioritised us this year | sup.7.2.3 | supplier pushing back, losing priority |
| sup.7.2.3#q26 | (E) spot/emergency purchase share of value, and its price premium | sup.7.2.3 | emergency buying, what it costs extra |
| sup.7.2.3#q27 | (E) is that premium attributed to payment delay or logged as a procurement failure | sup.7.2.3 | whose fault is the higher price |
| sup.7.2.3#q28 | (E) who sets the inventory holding target and against what | sup.7.2.3 | how much stock should we hold |
| sup.7.2.3#q29 | (E) are vendor rebates tracked and netted into per-item cost | sup.7.2.3 | volume discounts, annual rebates |
| sup.7.2.3#q30 | (F) which equipment runs on closed-system consumables, and what spend share | sup.7.2.3 | proprietary reagents, locked-in machines |
| sup.7.2.3#q31 | (F) was Procurement consulted on lifetime consumable cost before purchase | sup.7.2.3 | did anyone check the running cost before buying |
| sup.7.2.3#q32 | (F) is the business-case cost-per-test tracked against actuals | sup.7.2.3 | did the machine deliver the cost it promised |
| sup.7.2.3#q33 | (F) is the AMC inclusion list mapped into the item master | sup.7.2.3 | what's covered under AMC, buying it twice |
| sup.7.2.3#q34 | (F) who negotiates a closed-system contract at renewal, or does it auto-renew | sup.7.2.3 | contract renewal, nobody renegotiates |

## sup.7.2.3.2

| point | what it is | chunk | also called |
|---|---|---|---|
| sup.7.2.3.2#q1 | (G) was the last audit's evidence produced from the live system or compiled | sup.7.2.3.2 | preparing for NABH, making files for the audit |
| sup.7.2.3.2#q2 | (G) can they produce the near-expiry list and a batch trail right now | sup.7.2.3.2 | show me without preparing it |
| sup.7.2.3.2#q3 | (G) is the narcotic register reconciled daily by someone independent | sup.7.2.3.2 | narcotics check, who counts it |
| sup.7.2.3.2#q4 | (G) is a cold-chain excursion acted on or recorded and filed | sup.7.2.3.2 | fridge temperature breach, what happened next |
| sup.7.2.3.2#q5 | (G) who owns biomedical-waste segregation at the point of disposal | sup.7.2.3.2 | waste segregation, who is accountable |
| sup.7.2.3.2#q6 | (H) what share of own-consultant OPD prescriptions is dispensed in-house | sup.7.2.3.2 | how many prescriptions we actually fill |
| sup.7.2.3.2#q7 | (H) of those not dispensed, how many were stock-out vs price vs preference | sup.7.2.3.2 | why patients go outside for medicines |
| sup.7.2.3.2#q8 | (H) is the formulary reconciled against actual prescribing patterns | sup.7.2.3.2 | do we stock what our doctors write |
| sup.7.2.3.2#q9 | (H) are OPD retail and IPD issue reported with separate margin | sup.7.2.3.2 | blended pharmacy number |
| sup.7.2.3.2#q10 | (H) is a counter stock-out recorded as a lost-sale event at all | sup.7.2.3.2 | do we track the sale we didn't make |
| sup.7.2.3.2#q11 | (I) are housekeeping consumables on the same master and workflow | sup.7.2.3.2 | housekeeping materials on the same system |
| sup.7.2.3.2#q12 | (I) what happens to a housekeeping indent when the store is under pressure | sup.7.2.3.2 | whose indent gets dropped first |
| sup.7.2.3.2#q13 | (I) does Housekeeping ever purchase directly, and at what value | sup.7.2.3.2 | buying outside the process |
| sup.7.2.3.2#q14 | (J) does reorder read the forward admission or elective OT schedule | sup.7.2.3.2 | do you plan stock off the upcoming list |
| sup.7.2.3.2#q15 | (J) who is told in advance about a known demand change | sup.7.2.3.2 | new unit opening, camp coming up |
| sup.7.2.3.2#q16 | (J) at last high occupancy, which items stocked out and was it predictable | sup.7.2.3.2 | what ran out when we were full |
| sup.7.2.3.2#q17 | (K) for each control — enforced by the system or configured as policy | sup.7.2.3.2 | can the system be bypassed |
| sup.7.2.3.2#q18 | (K) who holds override rights, how often used, is it logged with a reason | sup.7.2.3.2 | who can override, override log |
| sup.7.2.3.2#q19 | (K) is the materials module built for perpetual inventory or adapted to it | sup.7.2.3.2 | is our ERP actually made for this |
| sup.7.2.3.2#q20 | (L) hourly profile of receipts and issues against the store roster | sup.7.2.3.2 | when is the store busiest, who's on then |
| sup.7.2.3.2#q21 | (L) has the staffing ratio-check been run against peak, not daily average | sup.7.2.3.2 | staffing worked out properly |
| sup.7.2.3.2#q22 | (L) is staffing held back until volume justifies it — the causality error | sup.7.2.3.2 | we'll hire when it gets busier |

## sup.7.3

| point | what it is | chunk | also called |
|---|---|---|---|
| sup.7.3#p1 | inventory turnover ratio and Days Inventory Outstanding | sup.7.3 | stock turns, how long stock sits |
| sup.7.3#p2 | fill rate and stock-out incidents by criticality class | sup.7.3 | how often we run out |
| sup.7.3#p3 | GRN-to-invoice price variance % | sup.7.3 | price differences at invoice |
| sup.7.3#p4 | true landed cost vs invoice price, net of freight, taxes and rebates | sup.7.3 | real cost of an item |
| sup.7.3#p5 | vendor payment days outstanding vs agreed credit terms | sup.7.3 | how late we pay, creditor days |
| sup.7.3#p6 | spot/emergency purchase share and its price premium | sup.7.3 | emergency buying cost |
| sup.7.3#p7 | pharmacy revenue and margin, OPD and IPD separately | sup.7.3 | pharmacy income split |
| sup.7.3#p8 | cost of goods sold as % of pharmacy revenue | sup.7.3 | pharmacy COGS, gross margin |
| sup.7.3#p9 | consumable and medicine cost as % of ARPOB | sup.7.3 | material cost per occupied bed |
| sup.7.3#p10 | closed-system consumable spend as share of total consumable spend | sup.7.3 | how much we can't negotiate |
| sup.7.3#p11 | expiry write-off value and % of inventory | sup.7.3 | expiry losses |
| sup.7.3#p12 | shrinkage and unexplained-adjustment value and % | sup.7.3 | stock losses, unexplained differences |
| sup.7.3#p13 | working capital tied up in inventory and its trend | sup.7.3 | money locked in stock |
| sup.7.3#p14 | discharge-process delay attributable to this department specifically | sup.7.3 | how much discharge time is ours |

## sup.7.4

| point | what it is | chunk | also called |
|---|---|---|---|
| sup.7.4#s1 | this department's solution is scale-variant, unlike Discharge's | sup.7.4 | does the answer change by hospital size |
| sup.7.4#s2 | the automation itself is not scale-gated — only its configuration | sup.7.4 | small hospitals can have the same system |
| sup.7.4#s3 | store depth, sub-store levels and staffing are what vary by scale | sup.7.4 | how many stores do we actually need |

## sup.7.4.1

| point | what it is | chunk | also called |
|---|---|---|---|
| sup.7.4.1#s1 | one shared item master, one ledger per location, one closed loop | sup.7.4.1 | single system, one source of truth |
| sup.7.4.1#s2 | location-specific reorder parameters against a shared master | sup.7.4.1 | each ward's own min-max on the same codes |
| sup.7.4.1#s3 | central store to pharmacy/consumables store to ward, OT, ICU sub-stores | sup.7.4.1 | store structure, how many levels |
| sup.7.4.1#s4 | rights-based workflow — indent, approval one level up, two-sided transfer | sup.7.4.1 | who raises, who approves, who confirms |
| sup.7.4.1#s5 | returns require unopened, undamaged, in-date, and reverse approval | sup.7.4.1 | return rules, what can go back |
| sup.7.4.1#s6 | defined shortage allocation rule — critical care and OT take priority | sup.7.4.1 | who gets it first when short |
| sup.7.4.1#s7 | aggregate-demand visibility to prevent duplicate reorders | sup.7.4.1 | two wards ordering the same thing |
| sup.7.4.1#s8 | straight-through PO on approved vendor/rate; exceptions to manual review | sup.7.4.1 | auto PO for routine, manual for the rest |
| sup.7.4.1#s9 | vendor and rate approval sit with a defined committee on a cycle | sup.7.4.1 | rate contract committee, annual cycle |
| sup.7.4.1#s10 | three-way match before payment — the single most effective control | sup.7.4.1 | matching before we pay |
| sup.7.4.1#s11 | every control enforced by the system, not merely configured, with logged overrides | sup.7.4.1 | the system must refuse it, not just ask |

## sup.7.4.1.2

| point | what it is | chunk | also called |
|---|---|---|---|
| sup.7.4.1.2#s1 | GRN auto-generated from barcode/OCR/EDI match at the gate | sup.7.4.1.2 | scanning the invoice at receipt, automatic GRN |
| sup.7.4.1.2#s2 | humans touch only exceptions — short receipt, damage, price mismatch | sup.7.4.1.2 | only handle the problems |
| sup.7.4.1.2#s3 | issue decrements the location ledger and posts to the running bill | sup.7.4.1.2 | charging as it leaves the store |
| sup.7.4.1.2#s4 | separate point-of-administration consumption capture to returnable unit | sup.7.4.1.2 | eMAR, recording what was given |
| sup.7.4.1.2#s5 | the issued-vs-consumed gap determines returnable, billable and write-off | sup.7.4.1.2 | what goes back, what gets charged |
| sup.7.4.1.2#s6 | returns and write-offs as a defined policy, not a ward judgment call | sup.7.4.1.2 | one rule for everyone |
| sup.7.4.1.2#s7 | preference cards and bed-day kits auto-issue on their trigger | sup.7.4.1.2 | automatic issue when a case is booked |
| sup.7.4.1.2#s8 | the preference card is a system object per surgeon per procedure | sup.7.4.1.2 | documented surgeon preferences in the system |
| sup.7.4.1.2#s9 | an OT list change fires a store-side event, not a phone call | sup.7.4.1.2 | the store gets told automatically |
| sup.7.4.1.2#s10 | predictive requirement flagging from consumption velocity, before any count | sup.7.4.1.2 | system predicts the need, before stock is checked |
| sup.7.4.1.2#s11 | forward-demand input from planned admissions and the elective OT list | sup.7.4.1.2 | planning stock off the upcoming schedule |
| sup.7.4.1.2#s12 | a purchase-rate change raises a mandatory billable-rate review | sup.7.4.1.2 | selling price follows the buying price |
| sup.7.4.1.2#s13 | voice capture for consumption entries, indents and requisitions | sup.7.4.1.2 | speaking it instead of typing |
| sup.7.4.1.2#s14 | daily P&L dashboard reconciling revenue against cost of items issued | sup.7.4.1.2 | same-day pharmacy P&L by ward |
| sup.7.4.1.2#s15 | this and Discharge's automation are two halves of one build | sup.7.4.1.2 | do them together, one project not two |

## sup.7.4.2

| point | what it is | chunk | also called |
|---|---|---|---|
| sup.7.4.2#s1 | system indent every time, including urgent needs | sup.7.4.2 | no phone requests, everything on system |
| sup.7.4.2#s2 | that discipline only holds if indent lead time is trustworthy | sup.7.4.2 | they'll go back to hoarding if it's slow |
| sup.7.4.2#s3 | store staff confirm what the system shows rather than being its source | sup.7.4.2 | stock count becomes a check, not the truth |
| sup.7.4.2#s4 | purchasing negotiates rate contracts up front, approves only exceptions | sup.7.4.2 | negotiate once, not per order |
| sup.7.4.2#s5 | nursing consumption recording positioned as capturing existing work | sup.7.4.2 | not extra work, just recording what you do |
| sup.7.4.2#s6 | predictive requisition replaces reactive requisition | sup.7.4.2 | system raises it, staff confirm |
| sup.7.4.2#s7 | OT list freeze and post-freeze changes routed through the system | sup.7.4.2 | freezing the list, no more phone changes |
| sup.7.4.2#s8 | payment-run discipline becomes a supply chain control, quantified to Finance | sup.7.4.2 | showing finance what late payment costs |
| sup.7.4.2#s9 | IT must enforce the master, hierarchy, two-sided transfer and returns | sup.7.4.2 | no local workarounds |

## sup.7.4.3

| point | what it is | chunk | also called |
|---|---|---|---|
| sup.7.4.3#s1 | IT/ERP — the architecture must be built and enforced correctly | sup.7.4.3 | our systems team |
| sup.7.4.3#s2 | purchasing — negotiation becomes periodic and higher-stakes | sup.7.4.3 | the purchase department |
| sup.7.4.3#s3 | store and sub-store staff — real-time accountability replaces ambiguity | sup.7.4.3 | storekeepers, ward stock holders |
| sup.7.4.3#s4 | nursing and clinical staff — consumption recording at the point of care | sup.7.4.3 | getting the nurses on board |
| sup.7.4.3#s5 | OT scheduling and surgeons — preference cards become system objects | sup.7.4.3 | getting surgeons to document their lists |
| sup.7.4.3#s6 | Finance — three-way match discipline and the payment-days conversation | sup.7.4.3 | finance sign-off, payment terms |
| sup.7.4.3#s7 | Biomedical — the closed-system contract inventory | sup.7.4.3 | biomedical engineering, machine contracts |
| sup.7.4.3#s8 | Pharmacy and Quality — scan discipline and live audit evidence | sup.7.4.3 | barcode scanning, audit readiness |
| sup.7.4.3#s9 | COO approves the process flows, not daily materials activity | sup.7.4.3 | who authorises this across departments |
| sup.7.4.3#s10 | introduce as extension of the role; audit framing guarantees resistance | sup.7.4.3 | how to pitch it to staff |

## sup.7.4.4

| point | what it is | chunk | also called |
|---|---|---|---|
| sup.7.4.4#s1 | Materials Manager — new dedicated role, Operations reporting line | sup.7.4.4 | a materials head, someone to own stores |
| sup.7.4.4#p1 | Materials Manager cost — ₹8–10 lakhs/year | sup.7.4.4 | what that role costs, the salary |
| sup.7.4.4#s2 | triggered by the 80% occupancy pivot, the universal hospital-wide inflection | sup.7.4.4 | when do we need this role, are we past the threshold |
| sup.7.4.4#s3 | above the pivot the shortage rule fires and buffer policy inverts to care continuity | sup.7.4.4 | what changes when we're full, why now |
| sup.7.4.4#s4 | the cost follows the proficiency the role requires, not the trigger it shares | sup.7.4.4 | why it costs double a bed manager |
| sup.7.4.4#s5 | never reason from the Bed or Discharge Manager figure to this one, or back | sup.7.4.4 | we pay our bed manager less, benchmark the salaries |
| sup.7.4.4#s6 | Procurement Head assumed already in place, not a threshold decision | sup.7.4.4 | we already have a purchase head |
| sup.7.4.4#s7 | store-in-charge accountability changes materially under real-time visibility | sup.7.4.4 | the storekeeper's job changes |
| sup.7.4.4#s8 | a named category owner per major consumable category | sup.7.4.4 | category management, someone owning each group |
| sup.7.4.4#s9 | GRN/receiving clerk sized against peak receipt volume, not average | sup.7.4.4 | do we still need a receiving clerk |
| sup.7.4.4#s10 | the cost-benefit case is still built per-role, against this department's own leakages | sup.7.4.4 | is it worth it for us, what does the role recover |
| sup.7.4.4#s11 | where several functions cross the pivot at once, rank by cost — sequencing, not a verdict | sup.7.4.4 | which role do we hire first, can we do them all |
| sup.7.4.4#s12 | a secondary volume trigger is optional, not owed — a refinement, not a gap | sup.7.4.4 | busy store but low occupancy, does the rule still fit |

## sup.7.5

| point | what it is | chunk | also called |
|---|---|---|---|
| sup.7.5#f1 | materials modules bolted on rather than built for perpetual inventory | sup.7.5 | our ERP wasn't designed for this |
| sup.7.5#f2 | item-master de-duplication is a migration problem, not a setting | sup.7.5 | cleaning up the codes, it's a big job |
| sup.7.5#f3 | resistance disguised as "our items are different" | sup.7.5 | they say their list is special |
| sup.7.5#f4 | two-sided transfer and rate enforcement often unsupported out of the box | sup.7.5 | the system can't do it, or doesn't by default |
| sup.7.5#f5 | PACS/lab/OT integration is the same work Discharge needs | sup.7.5 | one integration, not two |
| sup.7.5#f6 | nursing resistance to real-time charting as added data entry | sup.7.5 | nurses say it's more work |
| sup.7.5#f7 | pharmacy and store resistance to barcode and scan discipline | sup.7.5 | scanning slows them down |
| sup.7.5#f8 | purchasing resistance to losing negotiation discretion | sup.7.5 | buyers losing their relationships |
| sup.7.5#f9 | surgeon resistance to documenting preference cards — it makes cost comparable | sup.7.5 | surgeons won't write their list down |
| sup.7.5#f10 | staff resistance where current ambiguity conceals shrinkage | sup.7.5 | some don't want it visible, pilferage |

## sup.8

Section container (heading and reading note) — no points.

## sup.8.1

| point | what it is | chunk | also called |
|---|---|---|---|
| sup.8.1#k1 | vendor OTIF delivery %, by vendor and category | sup.8.1 | on time in full, supplier reliability score |
| sup.8.1#k2 | % of purchase spend under an active approved rate contract | sup.8.1 | how much we buy on contract |
| sup.8.1#k3 | rate-contract price variance % — negotiated vs actually paid | sup.8.1 | are we paying the agreed rate |
| sup.8.1#k4 | vendor concentration ratio by critical category | sup.8.1 | dependence on one supplier |
| sup.8.1#k5 | gate-entry-to-GRN cycle time | sup.8.1 | how long to book a receipt |
| sup.8.1#k6 | % of GRNs auto-generated vs manually keyed | sup.8.1 | automation level at receipt |
| sup.8.1#k7 | short-receipt/damage rate and debit-note resolution time | sup.8.1 | short supplies, damage claims |
| sup.8.1#k8 | inventory turnover and DIO by ABC-VED class | sup.8.1 | stock turns by criticality |
| sup.8.1#k9 | stock-out incidents by ABC-VED/criticality class | sup.8.1 | how often vital items run out |
| sup.8.1#k10 | fill rate — % of indents fully met on first issue | sup.8.1 | did the ward get everything asked for |
| sup.8.1#k11 | cycle-count stock accuracy % | sup.8.1 | count accuracy, system vs physical |
| sup.8.1#k12 | expiry write-off value and %, central store and sub-store separately | sup.8.1 | expiry losses by location |
| sup.8.1#k13 | % of POs generated straight-through vs manually raised | sup.8.1 | automatic purchase orders |
| sup.8.1#k14 | three-way match compliance % | sup.8.1 | payments properly matched |
| sup.8.1#k15 | payment days actual vs agreed credit terms | sup.8.1 | are we paying on time |
| sup.8.1#k16 | % of requisitions system-generated (predictive) vs manual | sup.8.1 | how much the system raises itself |
| sup.8.1#k17 | % of entries captured via voice vs typed or scanned | sup.8.1 | voice adoption |

## sup.8.2

| point | what it is | chunk | also called |
|---|---|---|---|
| sup.8.2#k18 | time from discharge confirmation to finalized chargeable-item list, post-returns | sup.8.2 | how long the pharmacy step takes at discharge |
| sup.8.2#k19 | % of discharges with real-time issue/consumption reconciliation | sup.8.2 | how often no manual count was needed |
| sup.8.2#k20 | unreconciled part-used, non-returnable write-off value | sup.8.2 | half-used items written off |
| sup.8.2#k21 | off-system courtesy-issue incidents detected | sup.8.2 | issues without an indent |
| sup.8.2#k22 | package/kit actual-vs-presumed-BOM variance % by package type | sup.8.2 | package consumption drift |
| sup.8.2#k23 | OPD pharmacy revenue and margin, separate from IPD issue value | sup.8.2 | counter vs ward margin |
| sup.8.2#k24 | OPD prescription fill/capture rate, in-house vs outside | sup.8.2 | how many prescriptions we keep |
| sup.8.2#k25 | daily P&L variance by ward/department, same-day | sup.8.2 | daily reconciliation, not month-end |
| sup.8.2#k26 | landed cost vs invoice price variance %, and rebate value captured | sup.8.2 | true cost tracking, rebates earned |
| sup.8.2#k27 | consumable and medicine cost as % of ARPOB, trended | sup.8.2 | material cost per bed |
| sup.8.2#k28 | quantified ₹ EBITDA contribution from supply chain efficiency | sup.8.2 | what this is worth to EBITDA |
| sup.8.2#k29 | nurse/ward-staff hours lost per day to stock work | sup.8.2 | nursing time on stores |
| sup.8.2#k30 | receiving and store staffing ratio against peak receipt and issue volume | sup.8.2 | store staffing at the busy hours |
| sup.8.2#k31 | Materials Manager threshold tracking | sup.8.2 | are we past the hiring trigger |
| sup.8.2#k32 | reporting-line status, Operations vs Finance | sup.8.2 | who we report to, reviewed periodically |
| sup.8.2#k33 | Schedule H1/X and narcotic-handling audit compliance % | sup.8.2 | narcotics compliance |
| sup.8.2#k34 | cold-chain excursion incidents and the proportion acted on | sup.8.2 | fridge breaches and what followed |
| sup.8.2#k35 | OT delays coded to consumables, split not-in-hospital vs not-on-trolley | sup.8.2 | why the OT was late, which kind of failure |
| sup.8.2#k36 | preference-card coverage and median age since last revision | sup.8.2 | documented surgeon lists, how current |
| sup.8.2#k37 | ward buffer-stock value at cycle count, paired with indent lead time | sup.8.2 | hidden ward stock and why it exists |
| sup.8.2#k38 | item-master-to-price-master reconciliation lag, in days | sup.8.2 | how long before selling price catches up |
| sup.8.2#k39 | spot purchase price premium reported alongside payment-days-outstanding | sup.8.2 | emergency buying cost against how late we pay |
| sup.8.2#k40 | closed-system consumable spend as share of total consumable spend | sup.8.2 | spend we can't negotiate |
| sup.8.2#k41 | audit-evidence production time from the live system, unprepared | sup.8.2 | how fast can we show the auditor |
| sup.8.2#k42 | OPD pharmacy lost-sale events recorded by cause | sup.8.2 | sales we didn't make and why |
| sup.8.2#k43 | % of reorder value driven by forward demand signal vs trailing consumption | sup.8.2 | planning ahead vs reacting |
| sup.8.2#k44 | system-enforced control overrides per quarter, by control, user and reason | sup.8.2 | who overrode what, override log |

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

## common.occupancy-pivot

| point | what it is | chunk | also called |
|---|---|---|---|
| common.occupancy-pivot#c1 | 80% occupancy is one hospital-wide pivot, not three separate department thresholds | common.occupancy-pivot | the eighty percent mark, when things change, are we past it |
| common.occupancy-pivot#c2 | below it spare capacity absorbs coordination failure; above it, it converts to lost revenue | common.occupancy-pivot | we've always run like this, why is it a problem now, no room to recover |
| common.occupancy-pivot#c3 | every function needs a different strategy above it, not the same strategy harder | common.occupancy-pivot | what changes when we're full, do we just work faster |
| common.occupancy-pivot#s1 | Bed Management — prediction becomes the mechanism; cadence and reserve earn their cost here | common.occupancy-pivot | why plan beds twice a day, when the reserve is worth it |
| common.occupancy-pivot#s2 | Discharge — TAT measured through to the next admission becomes an active check | common.occupancy-pivot | tighter discharge measurement, where the time actually goes |
| common.occupancy-pivot#s3 | Supply Chain — buffer policy inverts; the shortage-allocation rule starts firing for real | common.occupancy-pivot | safety stock when we're full, who gets it when short |
| common.occupancy-pivot#s4 | OPD is the exception — ambulatory load scales with footfall, not ward occupancy | common.occupancy-pivot | does this apply to OPD, busy counter but empty wards |
| common.occupancy-pivot#s5 | the pivot triggers a dedicated owner role in each function, not one shared owner | common.occupancy-pivot | do we need a manager for each, one person for everything |
| common.occupancy-pivot#p1 | Materials Manager ₹8–10 lakhs; Bed Manager and Discharge Manager ₹4–4.5 lakhs each | common.occupancy-pivot | what these roles cost, salary for each manager |
| common.occupancy-pivot#n1 | a common trigger does not imply a common price — salary follows proficiency | common.occupancy-pivot | why does one cost double, same trigger different salary |
| common.occupancy-pivot#n2 | never reason from one role's figure to another's, in either direction | common.occupancy-pivot | we pay our bed manager this much, benchmark the salaries |
| common.occupancy-pivot#c4 | a department may carry a sharper pivot of its own — Bed's demand-vs-supply | common.occupancy-pivot | which pivot applies, two different thresholds |
| common.occupancy-pivot#n3 | crossing the pivot warrants the roles; it does not sequence them | common.occupancy-pivot | do we hire all of them at once, which one first |
| common.occupancy-pivot#s6 | rank by which function's failure costs most, using that department's §7.3 parameters | common.occupancy-pivot | where do we start, what's hurting most |

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
