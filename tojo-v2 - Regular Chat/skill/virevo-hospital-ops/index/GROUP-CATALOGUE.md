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
| 9 | Pharmacy & Supply Chain | `supply-chain-procurement` |
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

**Scoring a query into the wrong group is now a recoverable error.** Every
department file carries a cross-function interdependency map at §3b naming the
couplings through which its failures reach — and are misattributed to — other
functions. A query phrased as the *symptom* ("our bills are wrong", "the OT
started late", "housekeeping can't keep up", "procurement is buying badly")
scores into the group where it surfaces, and that group's §3b chunk names the
group where it originates. The point index's §3b rows are phrased as complaints
for exactly this reason, so the second hop is usually available on the first
pass. Where the map points elsewhere, fetch the named department's §3b too
rather than answering from the symptom's own department.

**Supply Chain spans group 9 only for consumables, medicines and materials.**
Large-scale capital procurement — equipment, expansion projects, contractors,
major AMC/CMC contracts — is a separate file, not yet written. A query about
buying a machine rather than buying what the machine consumes has no reference
file yet and belongs in the gap register, not in `supply-chain-procurement`.

**A group with no file is not a gap in the answer — it is a gap in the library.**
When a query scores into an empty group, or scores into a populated one but
matches no chunk above the relevance floor, the turn is answered from general
capability and the miss is written to the gap register: the question asked, that
no section matched, and what was said. That register is the file-writing backlog,
so the remaining files get written in the order hospitals actually ask about them.
