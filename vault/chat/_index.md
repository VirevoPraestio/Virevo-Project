---
id: _index
title: Hospital operations index
description: The twelve function groups and one card per function, naming the chunks each holds
keywords: [index, catalogue, groups, chunks, routing]
kind: index
version: 2026-09-15
source_file: skill/virevo-hospital-ops/index/GROUP-CATALOGUE.md + the five *.card.md
source_author: Avishek
---
# Hospital Operations — Function Group Catalogue

Resident on every call. Twelve groups; a query is scored against these first, and
only the index cards of the candidate groups' functions are then fetched.

This list does not grow as the library does. Adding the hundredth reference file
adds a row to a group, not a group.

| # | Group | Functions with reference files |
|---|---|---|
| 1 | Patient Access & Admissions | — |
| 2 | Bed & Capacity Management | `bed-management` |
| 3 | Inpatient Care Delivery | — |
| 4 | Discharge & Transitions | `discharge-process`, `discharge-process-conversation-playbook` |
| 5 | OPD & Ambulatory | `opd-diagnostic-leakage` |
| 6 | Diagnostics — Lab & Imaging | — |
| 7 | Operating Theatre & Procedures | — |
| 8 | Emergency & Critical Care | — |
| 9 | Pharmacy & Supply Chain | — |
| 10 | Revenue Cycle — Billing, Insurance & Claims | — |
| 11 | Workforce & Rostering | — |
| 12 | Quality, Compliance & Clinical Governance | — |

**Cross-cutting, never scored:** `common-elements` is pinned. Any department
chunk fetched pulls the relevant `common.*` chunks alongside it, in code. It is
the file that says what applies *beyond* the department just retrieved, so topic
matching would select it exactly when it is least needed.

**Enforced pairing:** groups 2 and 4 co-fetch. Bed Management's prediction
accuracy depends on Discharge's real timings, and a hospital's reported Discharge
turnaround can only be checked for authenticity against Bed Management's own
allocation and physical-admission timestamps. A query into either pulls both.

**Conditional:** `discharge-process-conversation-playbook` is fetched when the
group is 4 **and** the turn is open-ended consulting rather than a single-fact
lookup. It is a worked conversation arc, not an eight-section department file.

**A group with no file is not a gap in the answer — it is a gap in the library.**
When a query scores into an empty group, or scores into a populated one but
matches no chunk above the relevance floor, the turn is answered from general
capability and the miss is written to the gap register: the question asked, that
no section matched, and what was said. That register is the file-writing backlog,
so the remaining files get written in the order hospitals actually ask about them.


---

# Bed Management — index card

Covers bed allocation, availability and turnover, the admissions desk that runs with it, and when a bed starts earning again. Queries about beds not turning over, late admissions, occupancy, bed-side staffing or dead bed time belong here.

**Group:** Bed & Capacity Management
**Pinned with:** common-elements  **Co-fetches:** discharge-process

| id | covers |
|---|---|
| bed.1 | what the department owns and balances |
| bed.2 | activity list; admissions desk is same team |
| bed.3 | upstream and downstream dependencies, by priority |
| bed.4 | placement rules never overridden |
| bed.5 | what flexes under pressure |
| bed.6 | serialised discharge-then-admission failure; loss starts at billing |
| bed.7.1 | Discharge TAT, Admission TAT stages, two staffing ratios |
| bed.7.2.1 | data, rosters and timestamps to obtain first |
| bed.7.2.2 | eleven practice-verification questions and their branches |
| bed.7.3 | eight financial parameters; dead bed time bill-to-bill |
| bed.7.4 | demand-vs-supply pivot; what scales, what holds |
| bed.7.4.1 | automation elements, 2 PM/6 PM cadence, benefit lines |
| bed.7.4.2 | process changes the automation presupposes |
| bed.7.4.3 | cooperating teams, COO sign-off, doctor buy-in |
| bed.7.4.4 | Bed Manager triggers; Admissions Executive sizing, cost |
| bed.status | maintainer changelog — never fetched (`retrieve: never`) |
| bed.8 | eighteen KPIs; four revisions not yet made |

**Retired ids:** none


---

# Discharge Process — index card

Covers the discharge decision through to the bed being available again: clinical sign-off, billing, insurance/TPA, briefing, bed turnover. Route here for discharge speed, discharge TAT, ownership and discharge staffing.

**Group:** Discharge & Transitions
**Pinned with:** common-elements  **Co-fetches:** bed-management

| id | covers |
|---|---|
| dis.1 | scope: decision to bed availability |
| dis.2 | activities a discharge is made of |
| dis.3 | upstream teams, downstream metrics, priorities |
| dis.4 | what is never traded for speed |
| dis.5 | sequencing that may flex or parallelise |
| dis.6 | default failures; serialised discharge/admissions team |
| dis.7 | container heading for chat-agent handling |
| dis.7.1 | occupancy urgency; nursing, housekeeping, transport ratios |
| dis.7.2 | data and system access required first |
| dis.7.2.1 | the 16 questions, incl. TAT authenticity |
| dis.7.3 | financial parameters for the cost-benefit case |
| dis.7.4 | solution constant; cost justification varies |
| dis.7.4.1 | automation: event log, auto-bill, evening insurance |
| dis.7.4.2 | process shifts, integration, breaking serialisation |
| dis.7.4.3 | teams to win over; COO approves flows |
| dis.7.4.4 | Discharge Manager vs. Executives, sizing |
| dis.7.status | maintainer changelog — never fetched |
| dis.8 | the 16 approved KPIs |

**Retired ids:** none


---

# OPD-to-Diagnostics Conversion — index card

Covers whether tests prescribed in OPD actually get done at this hospital — prescription capture, diagnostic slot scheduling and walk-in capacity, guest-services handholding, and the revenue leaked when redemption happens elsewhere or not at all. A query belongs here when it touches prescribed-vs-completed tests, diagnostic equipment utilisation, OPD floor/billing staffing, or same-visit conversion.

**Group:** OPD & Ambulatory
**Pinned with:** common-elements  **Co-fetches:** none

| id | covers |
|---|---|
| opd.0 | case-study baseline: 10%/20% redemption, MRI bottleneck |
| opd.1 | purpose: same-visit redemption at own facility |
| opd.2 | sub-functions from capture to billing coordination |
| opd.3 | upstream/downstream dependencies with priority |
| opd.4 | non-negotiables: STAT timing, test accuracy |
| opd.5 | flex: same-day timing, slot, equivalent modality |
| opd.6 | failure modes: no buffer, no tracking, reversed causality |
| opd.7 | container heading for chat-agent handling |
| opd.7.1.1 | considerations 1-7: measurement, ratios, scheduling ownership |
| opd.7.1.2 | considerations 8-14: weakest link, peak load, morale |
| opd.7.2 | data access plus 14 practice-verification questions |
| opd.7.3 | five financial parameters anchoring the case |
| opd.7.4 | sequencing note and manual-plus-automated requirement |
| opd.7.4.1 | process changes and manpower, reasoned first |
| opd.7.4.2 | automation: four bots for the process items |
| opd.7.4.3 | key people and buy-in, Scheduling Manager threshold |
| opd.7.4.4 | team/role changes: Scheduling Manager, guest services |
| opd.status | maintainer status note — `retrieve: never`, never fetch |
| opd.8 | eighteen KPIs across four groups |

**Retired ids:** none


---

# Common elements — index card

Holds the three frameworks every department answer runs on: Solution Construction, the shared Discharge/Bed/ALOS/Occupancy considerations, and Peak-Load Staffing. Pinned, not scored: it says what applies beyond the department a query names, which is when topic matching would miss it.

**Group:** cross-cutting — pinned, never scored as a retrieval candidate
**Pinned with:** every department fetch

| id | covers |
|---|---|
| common.overview | why this file applies alongside every department file |
| common.solution-method | cost-benefit, before/after graphic, four solution aspects |
| common.shared-considerations | eight-point discharge, admission, bed, ALOS, occupancy set |
| common.peak-load | peak-load staffing ratio check and headcount justification |

**Retired ids:** none


---

# Discharge conversation playbook — index card

A worked, stage-by-stage example of a full unscripted Discharge consulting conversation — the arc from dependency verification through to next steps — plus the rule for reusing that arc in other departments. Fetch it when the department is Discharge Process AND the turn is an open-ended consulting turn rather than a single-fact lookup.

**Group:** Discharge & Transitions
**Pinned with:** common-elements  **Co-fetches:** discharge-process, bed-management

| id | covers |
|---|---|
| play.0 | how to use this file; adapt the pattern, re-derive the numbers |
| play.1 | the fixed order of the unscripted consulting arc |
| play.2 | diagnosis stage: name the mechanism, not the symptom |
| play.3 | the five-part solution overview, revealed progressively |
| play.4 | deep-diving each of the five parts, one at a time |
| play.5 | follow-ups and factual pushback mid-deep-dive |
| play.6 | swapping the hospital's real data in for estimates |
| play.7 | landing on a short, sequenced next-steps plan |
| play.8 | answering what Virevo's engagement actually consists of |
| play.9 | generalisation rule: same arc for other departments |

**Retired ids:** none
