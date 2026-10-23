# Department: Supply Chain & Procurement — Consumables, Medicines & Materials

*Division: Supply Chain & Materials Management <!--m-->· Status: revision pass 2026-09-16 — restructured to the v2 eight-section template, §3b cross-function interdependency map added, §7.2 rebuilt in three parts with per-function root-cause question clusters, §7.4.1 and §8 split for the chunk ceiling, §9's resolved items folded into the content that supersedes them. Awaiting Avishek's section-by-section review.<!--/m-->*

**Part 1 of 2.** This file covers consumables, medicines, surgical items, and general materials — the high-frequency, high-volume, patient-charge-linked side of Supply Chain. Large-scale capital procurement (equipment, expansion projects, contractors, major AMC/CMC contracts) is a separate file, because its approval structure, financial evaluation method, and vendor relationship shape are fundamentally different. The seam between the two files is real and load-bearing, not administrative: equipment bought on a closed-system or reagent-rental contract determines this file's consumable economics for that machine's whole life, and that decision is made in the other file. See §3b(F).

---

<!--chunk
id: sup.0
title: Why this file spans several sub-functions
summary: Why Supply Chain is treated as one continuous chain rather than five adjacent topics, and why queries about it usually arrive named as something else.
keys: scope, department width, vendor to patient chain, billing accuracy origin, retrieval entry point, misattributed query, part 1 of 2
needs: none
see: sup.1, sup.3b
tokens: 290
-->
## 0. Why this file is unusually wide

Every other department file in this knowledge base stays inside one functional lane. This one can't, because the underlying reality doesn't separate cleanly: whether a patient's bill is accurate at discharge is a direct function of how an item was issued at the ward, which is a direct function of how it was received at the gate, which is a direct function of what was actually agreed with the vendor and configured in the ERP. Vendor negotiation, physical stores operation, ERP/systems design, procure-to-pay process, and the billing interface are one continuous chain, not five adjacent topics — so this file treats them as one department with several sub-functions, the same way Discharge Process treats clinical sign-off, billing closure, and physical bed turnover as one process rather than three.

The width has a retrieval consequence worth stating plainly: a query that names only one link of that chain ("our bills are wrong at discharge", "the OT started late again", "why is working capital so high") is usually a query about this department, and will not say so. §3b exists to make those entry points resolvable.

<!--chunk
id: sup.1
title: Purpose
summary: What the department must guarantee: availability at the point of need, at a controlled cost, with an unbroken reconcilable record from vendor to patient.
keys: purpose, availability, stock-out prevention, negotiated cost, traceability, reconciliation, billing accuracy, point of need
needs: none
see: sup.2
tokens: 140
-->
## 1. Purpose

Ensure that every consumable, medicine, surgical item, and general material required for patient care and hospital operation is available at the point of need, at a negotiated and controlled cost, with an unbroken system record from vendor to patient — so that what was procured, received, stored, issued, consumed, billed, returned, and paid for can always be reconciled against each other, and so that no patient ever waits on a stock-out and no bill is ever wrong because the supply chain behind it wasn't tracked in real time.

<!--chunk
id: sup.2
title: Sub-functions & core activities
summary: The nine sub-functions owned here, from vendor contracting and inbound receipt through stores, ERP architecture, procure-to-pay, issue, service mapping, pharmacy sale and financial monitoring.
keys: vendor management, rate contract, GRN, goods receipt, item master, store sub-store, ABC-VED, procure to pay, three-way match, issue and consumption, preference card, OPD pharmacy, IPD issue
needs: none
see: sup.1, sup.3
tokens: 1010
-->
## 2. Sub-functions & core activities

**A. Vendor management & contracting** — vendor sourcing, empanelment, and approval · category-wise negotiation and rate-contract finalization · MOQ (minimum order quantity) negotiation · payment-terms and credit-period negotiation · annual/periodic rate revalidation and re-negotiation · vendor performance scorecarding (fill rate, on-time-in-full delivery, quality rejection rate) · vendor re-approval, probation, or exit.

**B. Inbound logistics & receipt** — gate entry and security check of incoming vendor consignments · invoice/challan matching against the PO at the gate · quality/visual inspection, batch-number and expiry-date verification · Goods Receipt Note (GRN) creation in the ERP · put-away to the correct store or sub-store location · discrepancy, short-receipt, and damage handling, and the vendor debit-note process that follows.

**C. Inventory & stores management** — item master maintenance · store and sub-store stock ledgers · physical stock-taking and cycle counts · reorder-level/reorder-quantity (ROL/ROQ) monitoring and auto- or manual-replenishment triggers · ABC-VED classification and a differentiated stocking policy by class · near-expiry and expiry management · slow-moving and dead-stock identification.

**D. ERP & systems architecture for materials management** — item-master creation and governance (one item, one code, one master — no duplicate or store-local item codes) · store/sub-store hierarchy design and creation · user-rights configuration for indent creation, requisition approval, inter-store transfer, and returns · the conflict- and priority-resolution logic that applies when multiple stores draw on the same constrained item.

**E. Procure-to-pay process** — indent aggregation from stores/sub-stores into a consolidated purchase requirement · Purchase Order (PO) creation, whether system-generated straight-through against a pre-approved vendor/rate combination or manually raised for exception cases · the approval authority for a new vendor and for a negotiated rate (a separate, higher-level decision from day-to-day PO issuance) · three-way match of indent/PO, GRN, and vendor invoice before payment is cleared for release · payment execution against the agreed credit terms.

**F. Issue, consumption tracking & billing interface** — issue of stock from store/sub-store against an indent or requisition · point-of-care consumption recording · real-time linkage of issued and consumed items to the patient's running bill · returns processing for unused, unopened, in-date stock · write-off treatment for part-used, non-returnable items · reconciliation of what was issued against what was actually consumed, which is what feeds an accurate discharge bill (see `discharge-process.md` §7.4.1, points d and e).

**G. Service-to-item mapping (standard issue / package billing)** — bill-of-materials / preference-card definition for OT procedures · standardised bed and ICU daily-issue kits · billing-package presumed-consumption lists (e.g. a normal-delivery package, a cataract package) · periodic reconciliation of actual usage against the presumed kit, to catch the point where package pricing has stopped covering real consumption.

**H. Pharmacy sale tracking** — OPD walk-in retail sale (cash/card/insurance, real-time inventory decrement, immediate invoicing, standard retail-pharmacy economics) · IPD credit issue against the patient's running bill (ward/sub-store decrement, no immediate cash settlement, reconciled at discharge) · separate revenue and margin visibility for the two channels, since their pricing and cost economics are genuinely different businesses sharing one stock pool.

**I. Financial monitoring** — daily reconciliation of pharmacy sales revenue and provisional IPD revenue booked (from items indented, issued, or consumed and charged to running bills) against the actual cost of the goods issued · variance flagging by ward, department, or item category · inventory-linked working-capital monitoring.

<!--chunk
id: sup.3
title: Dependencies
summary: Which eight upstream teams this department needs work from and which eight downstream functions degrade when it fails, each with a priority rating.
keys: upstream dependency, downstream impact, finance, clinical indent, IT ERP, vendors, biomedical, quality compliance, bed management, housekeeping, patient billing, discharge, OT scheduling, nursing time
needs: none
see: sup.3a, sup.3b, sup.7.2
tokens: 730
-->
## 3. Dependencies

### Upstream — what this department needs from other teams

| Depends on | Nature of dependency | Priority |
|---|---|---|
| Finance | Budget approval, payment release authority, credit-term negotiation mandate, working-capital limits | Critical |
| Clinical / Nursing / OT / ICU teams | Indent origination — the entire pull-side of the supply chain starts here | Critical |
| IT / ERP team | The systems backbone: item master, store/sub-store configuration, rights, real-time consumption capture | Critical |
| Vendors | Supply reliability, rate/MOQ/lead-time compliance, quality consistency | Critical |
| Biomedical / Engineering | Equipment-linked consumables (e.g. reagents tied to an installed analyzer, AMC-bundled spares) — a materials decision this department can't make alone | High |
| Quality / Regulatory / Compliance | Drug licensing, Schedule H/H1/X and narcotic handling rules, biomedical-waste segregation at the consumable-disposal end | High |
| Bed Management | Forward occupancy and planned-admission picture — the only forward-looking demand signal available; without it, reorder runs on trailing consumption alone | Medium-High |
| Housekeeping | Linen and cleaning consumables typically draw from the same store/sub-store structure and rights model | Medium-High |

### Downstream — what depends on this department running well

| Affects | Nature of effect | Priority |
|---|---|---|
| Patient Billing | Direct driver of a correct, complete, real-time bill — this department is where most billing accuracy problems actually originate | Critical |
| Discharge Process | The provisional-evening/final-morning billing automation in `discharge-process.md` §7.4.1 is only possible if this department's issue/consumption tracking is real-time; if it isn't, Discharge inherits the delay | Critical |
| Clinical care continuity | A stock-out of any critical item halts or delays care directly | Critical |
| OT Scheduling & Utilisation | Case-cart / consumable readiness gates whether an OT slot can actually start on time | High |
| Finance / P&L & working capital | Inventory is one of the largest non-payroll working-capital commitments in most hospitals | Critical |
| Quality / Compliance & Accreditation | NABH and similar audits check stock traceability, expiry control, and cold-chain/storage discipline directly against this department's records | High |
| Pharmacy revenue (OPD retail) | A genuine, separately-measurable P&L line in its own right, not just a cost center | High |
| Nursing clinical time | Hours per shift absorbed by stock-taking, indenting and chasing the store — invisible to management because it's counted as nursing time, not supply chain cost | High |

<!--m-->*(Draft ratings — flag any that should move, and flag anything missing, e.g. a specific vendor-concentration or single-point-of-failure risk you've seen in practice.)*<!--/m-->

<!--chunk
id: sup.3a
title: Organizational placement — Operations or Finance
summary: Why this department should report to the COO with CFO approval limited to rates, terms and accounting practice, and why a hospital's actual reporting line is itself diagnostic.
keys: reporting line, COO, CFO, operations versus finance, org structure, automated financial control, rate approval, organizational design, diagnostic question
needs: sup.3
see: sup.7.1, sup.7.2.3, sup.7.4.4
tokens: 390
-->
### 3a. Organizational placement — Operations or Finance

This isn't a dependency in the usual sense — it's a prior question about where this department sits in the org chart at all, and it changes how every other dependency above actually behaves in practice. <!--m-->**Avishek's explicit position:**<!--/m--> traditionally, hospitals place Supply Chain & Procurement under Finance, because of the inherent financial/accounting content of the work (rates, payments, vendor accounting). But that's a historical default, not the ideal structure. This department's *efficiency* is what critically drives Operations — ALOS, discharge timing, OT start times, bed turnaround all run through it directly (§3 downstream table above) — while its financial-control content (rate approval, negotiated-term sign-off, accounting/costing practice) can be built into the system through automation rather than requiring the department itself to sit inside Finance. The ideal structure: this team reports to the **COO**, not the CFO, and seeks CFO/Finance **approval only** on rates, negotiated terms, and accounting practices — not day-to-day operational control of the function.

This is a stated ideal, not yet a settled universal rule, and the gap between a given hospital's actual reporting line and this ideal is itself diagnostic (see §7.2.3(E) Q1). <!--m-->It needs the same watch-and-wait treatment as any other common-elements promotion candidate before it moves out of this department file; tracked as an open item in the maintainer block at the end of this file.<!--/m-->

<!--chunk
id: sup.3b
title: Cross-function interdependency map
summary: The twelve couplings through which Supply Chain fails, each named as a mechanism with the failure that propagates along it and where it is misattributed.
keys: interdependency, cross-function, root cause, misattribution, preference card, ward buffer, item master price master, returns, payment delay loop, closed system reagent, audit parallel record, formulary, forward demand, enforced control
needs: sup.3
see: sup.6, sup.7.2.3, dis.3b, bed.3b
tokens: 2160
-->
### 3b. Cross-function interdependency map

The §3 tables say *who* this department is coupled to and how hard. This section says *through what specific mechanism*, and *what failure travels along it* — because a dependency named at the level of "we depend on OT for indents" cannot be verified, and produces a generic question. Every row here has a matching root-cause question cluster in §7.2.3, keyed by the same letter.

The organising insight: almost every cross-function failure involving Supply Chain is misattributed at the point where it surfaces. An OT delay is logged against OT. A wrong bill is logged against Billing. A stock-out is logged against Procurement. In most hospitals the true origin is one or two links back along a coupling that nobody owns end-to-end — which is why §7.2.3's questions are built to walk *backwards* along the coupling rather than to audit the department the complaint names.

| | Coupled function | The specific coupling mechanism | What propagates along it, and where it surfaces |
|---|---|---|---|
| **A** | **OT & Procedures** | The surgeon's preference card / case-cart bill-of-materials is the interface. It is the only thing that translates "a knee replacement is booked at 9 AM" into "these 41 items must be on a trolley by 8:30." | Where the card is undocumented, surgeon-specific and held in an OT nurse's memory, a schedule change reaches the store as a phone call or not at all. Surfaces as an **OT late start blamed on "consumables not ready"** — which conceals two completely different failures: the item was not in the hospital (Supply Chain), or the item was in the hospital but not on the trolley (mapping and notification). Also propagates in reverse: a cancelled case leaves opened sterile packs and implant consignment that nobody writes off. |
| **B** | **Nursing & Ward** | The ward sub-store, and the indent-to-receipt lead time that governs it. | Where that lead time is long or unreliable, nurses rationally build an informal buffer outside the sub-store — the "just-in-case drawer". That buffer is invisible stock, so it breaks the ledger, breaks reorder logic, and absorbs expiry losses silently. Surfaces as **phantom inventory, ward-level expiry write-offs, and cycle-count variance** — and is almost always diagnosed as ward indiscipline when it is actually a rational response to Supply Chain's own lead time. Second channel: hours of nursing clinical time absorbed into stock work, which is counted as nursing cost, never as supply chain cost. |
| **C** | **Billing & Revenue Cycle** | Two masters that must agree and usually don't: the **item master** (purchase-side, owned by Materials) and the **price/charge master** (patient-billable, owned by Billing or Finance). | A negotiated purchase rate changes and nothing triggers a review of the patient-billable rate, or a new item is created in one master and not the other. Surfaces as **margin erosion nobody can locate, items issued but never billed, and items billed at a price the hospital no longer pays**. Diagnosed at Billing, originates at the master-governance boundary. |
| **D** | **Discharge Process** | Returns of unused, unopened, in-date stock, and the final reconciliation of issued-vs-consumed. `discharge-process.md` §7.4.1(d)–(e) depends on this department producing that number in real time. | Where returns require a manual ward count before the bill can close, Discharge's entire provisional-evening/final-morning design is unbuildable. Surfaces as **discharge delay attributed to "pending pharmacy reconciliation"** — the single most common discharge bottleneck that is not actually a Discharge problem. |
| **E** | **Finance** | Payment release against agreed credit terms — and this is the one genuinely **self-reinforcing loop** in the map, which is why it is the highest-value thing in this section. | Payment runs late → the vendor deprioritises this hospital → fill rate and OTIF drop → stock-out → emergency spot purchase outside the rate contract at a premium → consumable cost rises → Finance tightens working capital further → payment runs later. Surfaces at the far end as **"Procurement is buying badly"**, and is investigated as a procurement failure. The premium paid on spot purchases is the measurable signature of the loop, and almost no hospital attributes it back to payment days. |
| **F** | **Biomedical & Engineering** | Closed-system / proprietary / reagent-rental equipment contracts, and AMC-bundled spares. | A capital decision made once, by a different team, removes this department's negotiating power over that machine's consumables permanently. Surfaces as **an uncompetitive cost-per-test that Procurement is held responsible for and cannot fix**. Second channel: spares covered by an AMC being purchased separately as well, because the AMC's inclusion list was never mapped into the item master — the same item bought twice. This is the live seam with Part 2 (capital procurement). |
| **G** | **Quality, Compliance & Accreditation** | Traceability evidence: batch, expiry, cold chain, Schedule H1/X and narcotic registers. | Where the live system cannot produce audit evidence on demand, the hospital maintains a **parallel manual record for the audit** — which means the accredited process and the operating process are two different processes, and the accreditation certifies the wrong one. Surfaces as a clean audit alongside real expiry and traceability failures. |
| **H** | **Pharmacy retail & OPD** | The shared stock pool serving two different price/margin logics, and the OPD prescription-to-dispense conversion at the retail counter. | Where the OPD formulary is not reconciled against what the hospital's own consultants actually prescribe, the patient walks past the in-house pharmacy and fills outside. Surfaces as **OPD pharmacy revenue underperformance**, diagnosed as pricing or patient preference, when the dominant cause is usually that the prescribed molecule or brand was not in stock at that moment. Directly analogous to, and often co-occurring with, the leakage mechanism in `opd-diagnostic-leakage.md`. |
| **I** | **Housekeeping** | Shares the item master, sub-store structure and indent workflow, but carries no clinical urgency. | Housekeeping indents are the ones that get silently deprioritised when the store is under pressure, and where a shared item is contested, clinical wins without a rule being invoked. Surfaces as **housekeeping running a parallel off-system procurement route** — which then reappears as untracked spend and an unreconciled second item list. |
| **J** | **Bed Management** | The forward occupancy and planned-admission picture — see `bed-management.md` §7.4.1's planned-admission-to-bed mapping. | Without it, reorder is computed from trailing consumption, so the supply chain is structurally blind to known future demand: a full elective OT list next week, a seasonal occupancy surge, a new unit opening. Surfaces as **stock-outs that were entirely predictable**, and as safety stock held against uncertainty that the hospital had already resolved elsewhere in its own systems. |
| **K** | **IT / ERP** | Not a peer department but the substrate. The distinction that matters is **enforced vs. merely configured**: a rule the ERP checks, versus a policy people are asked to follow. | Every control in §7.4.1 — single item master, two-sided transfer, three-way match, no rate override — degrades into a convention within months if the system permits the workaround. Surfaces as **controls that are documented, believed to be in place, and routinely bypassed**, with nobody aware the bypass is happening. |
| **L** | **HR / Workforce** | Staffing of the store, receiving and ward-sub-store functions against peak receipt and issue windows, per the Peak-Load Staffing Method in `common-elements.md`. | Receipt volume and issue volume are both strongly peaked (morning vendor deliveries, pre-OT issue windows, discharge-time returns). Staffed to average, the peaks produce GRN backlog and delayed issue. Surfaces as **a systems problem** ("the ERP is slow", "GRN entry lags") when it is a rostering problem. |

**How to use this map.** When a query enters from the *other* function's side — an OT query, a billing query, a discharge query, a working-capital query — check this table before accepting that the problem belongs to the department the user named. Where a row's mechanism is present, the correct move is to run that row's question cluster in §7.2.3 *first*, and only then diagnose. Where a hospital has never looked at the coupling from both ends, the fact that nobody owns the coupling is itself the finding.

<!--chunk
id: sup.4
title: Non-negotiables
summary: The seven things never traded away: critical-item stock-outs, expired stock, unissued billing, controlled-substance compliance, rate override, off-system issue, cold-chain monitoring.
keys: non-negotiable, critical item stock-out, expired item, billing without issue, Schedule H1 X, narcotics, rate override, courtesy issue, cold chain monitoring
needs: none
see: sup.5, sup.6
tokens: 220
-->
## 4. Non-negotiables

No stock-out of a critical/emergency/life-saving item — crash-cart drugs, OT-essential consumables, blood-bank consumables — ever, under any circumstance · no expired item is ever administered or dispensed to a patient · no item is billed to a patient that wasn't actually issued or consumed for that patient · drug-license and controlled-substance compliance (Schedule H1/X, narcotics) on every single transaction, with no exceptions for convenience · the rate charged on a vendor invoice must match the approved rate contract — no silent price override at the payment stage · every issue is traceable to a specific indent and a specific requisitioning authority — there is no such thing as an off-system "courtesy issue" · cold-chain items are under continuous temperature monitoring, with any excursion recorded and acted on rather than noted.

<!--chunk
id: sup.5
title: What can flex
summary: What may legitimately be traded under pressure: stock-take cadence for low-criticality items, rate-renewal timing, equivalent substitution, and a bounded GRN entry lag.
keys: flexibility, stock take frequency, desirable class, rate contract renewal, brand substitution, generic substitution, GRN entry lag, physical availability
needs: none
see: sup.4
tokens: 160
-->
## 5. What can flex

The frequency of full physical stock-take for low-criticality (Desirable-class) items can extend beyond the standard cycle without material harm · negotiated rate-contract renewal cadence can slip for low-value, low-volume items · non-critical item substitution (equivalent brand or generic, within clinical protocol) is acceptable · batch consolidation and non-urgent GRN system-entry can trail the physical receipt by a short, defined window, provided the physical stock itself is already available for issue — the ERP catching up a few hours later is a tolerable lag; the ward not having the stock physically is not.

<!--chunk
id: sup.6
title: Failure modes & early warning signs
summary: The fourteen recurring failure patterns, from phantom inventory and duplicate item masters to the ward buffer drawer, the payment-delay spiral and audit-only parallel records.
keys: failure mode, phantom inventory, duplicate item code, GRN backlog, courtesy issue, buffer drawer, rate drift, expiry at sub-store, pilferage, part-used return, vendor concentration, stale price master, payment delay spiral, predictable stock-out
needs: none
see: sup.3b, sup.7.2.2, sup.7.4.1
tokens: 770
-->
## 6. Failure modes & early warning signs

- **Phantom inventory** — the system shows stock that physically isn't there (or vice versa), usually from unrecorded manual issues, miscounted stock-takes, or transfers logged on only one side.
- **Duplicate or store-local item masters** — the same physical item exists under two or more codes because stores weren't forced onto one shared master, which silently breaks reorder logic and vendor-spend visibility: you can't see you're buying the same syringe under two names.
- **GRN backlog** — physical receipt happens at the gate, but system entry trails by days, so the ERP's picture of available stock is stale exactly when reorder decisions are being made off it.
- **Off-system "courtesy issue"** — stock handed out informally, especially in emergencies, without an indent. Well-intentioned, and the single most common source of billing leakage and untraceable shrinkage.
- **The ward buffer drawer** — an informal stock cache held outside the sub-store because the official indent lead time is too slow to rely on. Invisible to the ledger, absorbs expiry losses silently, and is a symptom of Supply Chain's own lead time rather than ward indiscipline (§3b(B)).
- **PO-to-invoice rate mismatch going unnoticed** — the negotiated rate contract and the actual paid price quietly diverge over time, one small override at a time, until nobody remembers what the "real" rate is.
- **Expired stock sitting in a sub-store** — near-expiry monitoring exists at the central store but doesn't reach ward-level sub-stores, where small quantities of low-visibility items expire unnoticed.
- **Pilferage at the ward/sub-store level**, masked as "adjustment" or "wastage" entries rather than investigated as loss.
- **Unreconciled part-used returns** — a medicine or consumable is opened and partially used, never formally returned or written off, and simply falls out of both the patient's bill and the stock ledger. A quiet, cumulative margin leak that is very hard to see except in aggregate.
- **Vendor concentration risk** — over-reliance on one or two vendors for a critical category, with no qualified backup, so a single vendor's supply disruption becomes a hospital-wide stock-out.
- **Stale price master** — the ERP's reference price for an item isn't kept current against the latest negotiated rate, so purchase-side and billing-side systems disagree about what an item actually costs (§3b(C)).
- **The payment-delay spiral** — late payment degrades vendor fill rate, which forces premium spot purchases, which raises cost, which tightens working capital, which delays payment further. Self-reinforcing, and diagnosed at the wrong end (§3b(E)).
- **The audit-only parallel record** — traceability evidence compiled specially for accreditation rather than produced from the live system, so the accredited process and the real one have quietly diverged (§3b(G)).
- **Predictable stock-outs** — reorder computed from trailing consumption while the hospital's own forward admission and OT schedules already contained the demand signal (§3b(J)).

<!--chunk
id: sup.7
title: Chat-agent handling
summary: Heading only; the handling components live in the sub-sections — considerations, dependency verification, financial parameters, solution construction, automation hurdles.
keys: chat agent handling, agent guidance, supply chain query handling, section container
needs: none
see: sup.7.1, sup.7.2, sup.7.3, sup.7.4
tokens: 10
-->
## 7. Chat-agent handling

<!--chunk
id: sup.7.1
title: Subject-matter considerations
summary: What to establish before diagnosing: the reporting line, that failures are misattributed at the point they surface, whether EBITDA impact is quantified, and the two staffing peaks.
keys: reporting line diagnostic, misattribution, EBITDA quantification, efficiency definition, billing accuracy origin, capital versus consumable, package margin erosion, OPD versus IPD pharmacy, two staffing peaks, retail practices
needs: common.peak-load
see: sup.3a, sup.3b, sup.7.2.2, sup.7.4
tokens: 1480
-->
### 7.1 Subject-matter considerations

- **Who this department reports to (Operations vs. Finance) is itself a live, high-leverage diagnostic, not background context.** Per §3a, the ideal is a COO-reporting structure with CFO approval limited to rates/terms/accounting practice — but most hospitals default to Finance ownership because Operations leadership often isn't conversant with the accounting side. Establish this early in any query touching Supply Chain, because it reframes almost everything downstream: a Finance-owned department optimizes for control and compliance first; an Operations-owned one (with the right automated financial guardrails) is positioned to optimize for the speed and availability that actually drive ALOS, discharge, and OT outcomes.
- **Almost every cross-function supply chain failure is misattributed at the point it surfaces.** This is the single most useful thing to hold in mind when a query arrives from another department's side. Before accepting the framing in the question, check §3b for a coupling that would produce that symptom, and run the matching §7.2.3 cluster. A hospital describing an OT delay problem, a billing accuracy problem, or a working-capital problem is frequently describing this department without knowing it.
- **Don't assume the hospital has actually quantified this department's EBITDA contribution.** Many hospital owners hold a general belief that "more efficient procurement/supply chain helps EBITDA" without having quantified it — e.g., the concrete link between automating stock-taking, returns and discharge-time charge finalization and an ALOS reduction of even ~2 hours, and what that's worth. Ask directly whether they've quantified this or are working off the general belief; the answer changes whether the conversation needs to start with quantification itself before any solution discussion.
- **Ask what "efficiency" even means to them here, and how they currently monitor it**, before assuming a shared definition. A concrete, recommendable proxy: discharge-process duration specifically — and within that, the time taken to finalize the list of chargeable items *after* returns, measured from the moment the doctor confirms discharge. This ties directly to `discharge-process.md` and gives a monitorable number where "efficiency" would otherwise stay a vague impression.
- **This is the department where billing accuracy actually gets decided**, even though the failure surfaces at Billing or Discharge. Any query about a wrong bill, a discharge delay caused by "pending pharmacy reconciliation," or unexplained revenue leakage should be traced back here before it's diagnosed as a Billing or Discharge problem in isolation — see `discharge-process.md` §3 and §7.4.1, and §3b(C)–(D) above.
- **Consumables/medicines procurement and capital-equipment procurement are genuinely different problems**, not one department at two scales — different approval authority, different negotiation cadence, different financial-evaluation method (rate/MOQ/credit-terms vs. ROI/depreciation/AMC-lifecycle). Don't reach for this file's logic when the query is about equipment purchase; that's the companion file. But do note §3b(F): the capital decision is what sets this file's consumable economics for that equipment, so the two files meet there.
- **Package/bundled billing is a silent margin-erosion risk, not a one-time pricing decision.** A billing package (OT procedure, delivery package, standard bed-day rate) is priced against a *presumed* item-consumption list at the time it's set. If actual consumption drifts upward over time — new surgeon preferences, protocol changes, product substitutions — nobody notices unless someone is actively reconciling actual usage against the presumed kit. Treat "when was this package's item list last reconciled against actual usage" as a standing question, not a one-off check.
- **OPD pharmacy and IPD pharmacy issue are different businesses sharing one stock pool.** OPD is retail economics (cash/insurance sale, real margin, competitive pricing pressure from outside pharmacies); IPD is cost-recovery economics (issue against a captive patient, margin embedded in the overall bill, no external price comparison). A query about "pharmacy revenue" needs to specify which one, or it's not actually answerable.
- **Automation here exposes shrinkage that manual process could keep ambiguous.** This is a genuine adoption dynamic, not a hypothetical one — see §7.5. Anticipate that some resistance to real-time tracking is about visibility, not workload.
- **Staffing applies at two distinct peaks, not one.** Per the Peak-Load Staffing & Manpower Cost-Benefit Method in `common-elements.md` and §3b(L): inbound receipt peaks with vendor delivery windows, and issue peaks with the pre-OT and discharge-return windows. They are different pools, different hours, and sizing either against a daily average produces the GRN backlog and slow-issue symptoms that get reported as system problems.
- **Retail-derived practices worth carrying into hospital materials management** (a point of comparison, not a direct copy — hospitals have criticality and regulatory constraints retail doesn't): ABC-VED-differentiated stocking policy (retail's ABC analysis combined with hospital-specific VED — Vital/Essential/Desirable — criticality); vendor scorecarding on fill rate and OTIF rather than price alone; category management with a named category owner instead of item-by-item negotiation; rolling cycle counts instead of one disruptive annual physical stock-take; demand forecasting tied to a forward occupancy/census forecast the same way retail ties replenishment to footfall forecasts, rather than to trailing average consumption alone (see §3b(J)); and centralized negotiation with decentralized fulfillment — one rate contract, many draw points — as the default shape for the store/sub-store hierarchy in §7.4.1.

<!--chunk
id: sup.7.2
title: Dependency verification protocol
summary: How the three-part protocol runs, in what order when a query arrives from another function, and which divergences most often carry the largest effect.
keys: verification protocol, data access, practice verification, cross-function probe, order of enquiry, divergence is the diagnosis, baseline comparison
needs: sup.3b
see: sup.7.2.1, sup.7.2.2, sup.7.2.3
tokens: 270
-->
### 7.2 Dependency verification protocol

Before diagnosing a specific hospital's supply-chain problem, verify how their actual practice compares to the baseline in §2, §3 and §3b — the gap is almost always where the real problem lives, not in the org chart. This protocol runs in three parts: get the data (§7.2.1), verify the department's own practice (§7.2.2), then verify the couplings (§7.2.3, in two parts). Where a query arrived from another function's side, **run §7.2.3's relevant cluster before §7.2.2**, not after.

**Where the hospital's actual practice diverges from this baseline, that divergence *is* the diagnosis** — name it specifically rather than defaulting to a generic "tighten inventory controls" answer. The divergences that most often carry the largest effect: §7.2.2 items 4, 6, 9, 13, 14 and 19, and §7.2.3 clusters **A3** (the OT delay split), **B1–B2** (lead time and the buffer it creates), **C2** (what triggers a billable-rate review), **E4–E5** (the spot-purchase premium and its misattribution) and **K1** (enforced versus merely configured).

<!--chunk
id: sup.7.2.1
title: Dependency verification — data/system access required
summary: The ten data pulls required before any supply chain diagnosis, including the ones held by Biomedical and OT rather than by Materials.
keys: data access, item master export, purchase register, vendor payment ledger, GRN log timestamps, cycle count variance, price master, OT delay reason codes, equipment contract type, roster, forward schedule
needs: sup.7.2
see: sup.3b, sup.7.2.2, sup.7.2.3
tokens: 480
-->
#### 7.2.1 Data/system access required

- **Item master export across every store and sub-store**, with creation dates and codes — the only reliable way to detect duplicate or store-local codes, which nobody self-reports because nobody believes they have them.
- **Purchase register for the last four quarters**, with each line flagged as against-rate-contract or spot/emergency, and its price — to size §3b(E)'s spot-purchase premium.
- **Vendor payment ledger: invoice date, due date per agreed terms, and actual payment date**, by vendor — the other half of §3b(E), and the only way to test the loop rather than assert it.
- **GRN log with gate-entry timestamp and system-entry timestamp** for the same consignment — the lag is the metric, and it is never the lag people report.
- **Issue and consumption transactions by sub-store, with timestamps**, plus **cycle-count variance history** — for §3b(B)'s buffer-drawer detection and the peak-load issue-window profile.
- **The patient charge master and the purchase item master, side by side**, with last-revision dates on both — for §3b(C).
- **OT schedule with booked-vs-actual start times, and the delay-reason codes attached** — for §3b(A). Ask specifically whether "consumables" is a single reason code or is split by cause; if it is single, that is itself the finding.
- **Installed-equipment list with consumable/reagent contract type** (open vs. closed system, reagent rental, AMC inclusion list) — for §3b(F). Usually held by Biomedical, not Materials, which is the point.
- **Store, receiving and pharmacy staff rosters by shift, against hourly receipt and issue volume** — for the §7.1 peak-load checks and §3b(L).
- **Forward planned-admission and elective OT schedules** as currently available to Bed Management and OT — for §3b(J). The question is not whether the hospital has them; it is whether anything in the supply chain reads them.

<!--chunk
id: sup.7.2.2
title: Dependency verification — internal practice questions
summary: Twenty questions on this department's own practice, from EBITDA quantification and the efficiency definition through item master, GRN lag, three-way match, landed cost and daily reconciliation.
keys: verification questions, EBITDA quantified, efficiency definition, retail concepts, item master, GRN lag, reorder trigger, indent rights, two-sided transfer, allocation rule, PO automation, three-way match, landed cost, rebates, real-time issue, consumption tracking, part-used policy, OPD POS, package reconciliation, daily reconciliation, near expiry
needs: sup.7.2
see: sup.7.1, sup.7.2.3, sup.6
tokens: 1090
-->
#### 7.2.2 Internal practice-verification questions

Framing and quantification, asked first because they shape how everything else reads:

1. To what extent do they believe efficiency in procurement/supply chain contributes to EBITDA — have they actually quantified it (e.g., the EBITDA effect of reducing ALOS by even ~2 hours through automating stock-taking, returns, and discharge-time charge finalization), or is it a general, unquantified belief that any efficiency gain "must" help EBITDA?
2. What is their actual working definition of "efficiency" in this department, and how do they monitor it today? If they don't have a clean answer, propose monitoring via discharge-process duration specifically — in particular, the time taken to finalize the list of chargeable items after returns, measured from the moment the doctor confirms discharge.
3. Which retail supply-chain concepts have they already adopted, or do they think they should adopt — or do they believe there isn't much to learn from retail, on the reasoning that a hospital's material list isn't as complex as a large retailer's? Their answer is itself diagnostic of how far along this thinking already is.

Systems and process:

4. Is there a single, de-duplicated item master shared across every store and sub-store, or does each store maintain its own local item list? Follow up against the export in §7.2.1 rather than the answer.
5. Is GRN entry done at the point of physical receipt, or does it batch/lag — and by how long, typically?
6. Is reorder triggered automatically off ROL/ROQ, or does it depend on someone manually noticing low stock?
7. Who can raise an indent at ward/OT/ICU level, and who approves it before it reaches the store — is this enforced in the ERP, or is it a paper/verbal convention the system doesn't actually check?
8. Is inter-store transfer a two-sided, system-acknowledged transaction (sender debits, receiver credits, both confirmed), or can a transfer be logged by only one side?
9. What happens, today, when the same scarce or backordered item is indented by two or more sub-stores at once — is there a defined allocation/priority rule, or is it whoever asks first, or whoever has the better relationship with the store?
10. Is a Purchase Order raised automatically against a pre-approved vendor/rate combination for routine reorders, or is every PO manually created and approved regardless of value?
11. Who actually approves a new vendor, and who approves a negotiated rate — a defined committee/authority, or informally whoever in Purchasing has the relationship?
12. Is a three-way match (indent/PO, GRN, invoice) enforced before payment release, or can an invoice be paid off a PO alone without confirming what was actually received?
13. Does their costing distinguish true landed cost — invoice price plus freight and taxes, and critically net of any volume-based vendor rebates — from the raw invoice price, or is invoice price treated as the cost? Rebates in particular are very commonly earned and never tracked back into per-item cost.
14. Is stock issued from the store decremented and linked to a specific patient's bill in real time, or does the patient bill get built later from a separate, manual reconciliation?
15. Is consumption tracked separately from issue — does the system know what was actually *used*, not just what left the store — down to a returnable unit level? See `discharge-process.md` §7.4.1(d)–(e) on tracking to strips, bottles and whole-unit denominations.
16. What is the actual policy today for a part-used, non-returnable item — is it consistently billed and written off, or does it fall through the cracks?
17. Is OPD pharmacy sale on a real-time POS system separate from IPD ward issue, with separate revenue and margin reporting — or is it all one pharmacy revenue number?
18. Does anyone reconcile actual per-procedure or per-package item consumption against the presumed kit/BOM the package was priced on — and when was that last done?
19. Is there a daily — not monthly, not on-audit — reconciliation of pharmacy and IPD provisional revenue booked against the actual cost of items issued, by ward or department?
20. How are near-expiry items surfaced at ward sub-store level specifically, as distinct from the central store — and can someone produce today's near-expiry list right now, without preparing it?

<!--chunk
id: sup.7.2.3
title: Cross-function root-cause clusters — part 1 (A–F)
summary: Six question clusters keyed to the §3b couplings for OT, Nursing, Billing, Discharge, Finance and Biomedical, each walking backwards from the symptom to its origin.
keys: root cause questions, OT late start, trolley versus hospital, consignment implant, ward buffer, indent lead time, price master trigger, returns credit, payment days, spot purchase premium, closed system, AMC spares
needs: sup.3b, sup.7.2
see: sup.7.2.2, sup.7.2.3.2, dis.3b
tokens: 1960
-->
#### 7.2.3 Cross-function root-cause clusters — part 1: clinical, billing and financial couplings (A–F)

One cluster per §3b row, keyed by the same letter. Each cluster is built to walk *backwards* along the coupling from the symptom to its origin, so the questions are usable when the conversation entered from the other department's side. Ask the cluster whose symptom the hospital has actually described; don't run all twelve. Part 2 (§7.2.3 continued) carries clusters G–L.

**A. OT & Procedures** — *symptom: OT late starts attributed to consumables.*
1. When a case is booked, what produces the list of items that must be on the trolley — a documented preference card per surgeon per procedure held in the system, or an OT nurse's knowledge? If documented: when was each card last updated, and by whom?
2. How far ahead is the OT list frozen, and what is the channel by which a change after that point reaches the store — a system event, or a phone call?
3. Of the OT delays in the last quarter coded to consumables, how many were **the item not being in the hospital**, versus **the item being in the hospital but not on the trolley**? If the hospital cannot split these, that inability *is* the answer, and it means every one of those delays has been attributed to Supply Chain without evidence.
4. When a case is cancelled after the trolley is picked, what happens to the opened sterile packs and the issued-but-unused items — returned, written off against the case, or absorbed?
5. For high-value implants held on consignment: who owns the stock until it is used, at what moment is it billed to the patient, and does the patient charge precede or follow the vendor's invoice? A gap here is where implant margin disappears.
6. Does the OT's own consumption get reconciled against the preference card afterwards, or only against the billing package?

**B. Nursing & Ward** — *symptom: phantom inventory, ward expiry write-offs, cycle-count variance.*
1. What is the actual elapsed time from a ward raising an indent to the item being in the nurse's hand — routine, and urgent? Ask for the two numbers separately.
2. Given that number, is there an informal buffer held at the ward outside the sub-store ledger? Ask it directly and without implied fault, because the honest answer is usually yes and the buffer is rational.
3. What happens when a drug is needed urgently at 2 AM and the sub-store is empty — what is the actual sequence, and does it generate a system record?
4. Who physically counts the ward sub-store, how often, and does that person also carry responsibility for shortages found in the count? Where the counter and the accountable party are the same person, the count is not independent evidence.
5. How many hours per shift do ward nurses spend on stock-taking, indenting and following up with the store or pharmacy? This is usually invisible to management because it's absorbed into "part of the job," but it is real lost clinical time and a direct automation-benefit quantifier.
6. When ward stock goes missing, what is it recorded as — loss, adjustment, or wastage? The label the hospital uses determines whether anyone ever investigates it.

**C. Billing & Revenue Cycle** — *symptom: wrong bills, unlocatable margin erosion.*
1. Who owns the patient-billable price of an item, and who owns its purchase price — one master or two, and which team maintains each?
2. When a negotiated purchase rate changes, what specifically triggers a review of the patient-billable rate? If the answer is "the annual pricing exercise," the two have been out of step for up to a year at any given moment.
3. When a new item is created, what guarantees it exists in both masters before it can be issued — a system block, or a process step someone can skip?
4. Where an item is issued but never billed, who detects it, and when — at discharge, at month-end, or never? Ask for the last instance they actually caught one.
5. Does anyone compute realised margin per item against *landed* cost rather than invoice cost (see §7.2.2 Q13), and at what frequency?

**D. Discharge Process** — *symptom: discharge delayed by "pending pharmacy reconciliation".*
1. At discharge, who physically verifies the returns, and is the return credit posted before or after the bill is finalised? If after, the bill cannot close without a second pass.
2. What is the median time from discharge confirmation to the return credit being posted, and how many discharges per day are actually waiting on it?
3. Is the returnable balance computed by the system from the issue-and-consumption record, or counted by a nurse at the point of discharge? This is the exact prerequisite `discharge-process.md` §7.4.1 depends on.
4. For a part-used, non-returnable item at discharge — who decides whether the patient is charged, and is that decision consistent across wards or made case by case?
5. Does the hospital know what proportion of its discharge cycle time is attributable to this step specifically? If not, that number is the flagship metric of this whole file (§8, KPI #18) and it doesn't exist yet.

**E. Finance** — *symptom: "procurement is buying badly", rising consumable cost, working-capital pressure.* **Run this cluster whenever consumable cost is described as rising, before examining negotiation practice.**
1. Who does the supply/procurement team actually report to today — Finance or Operations? If Finance, is that because accounting expertise genuinely needs to sit inside the function, or because Operations leadership isn't conversant enough in accounting principles to own it? Follow-up: in an ideal world where the accounting and financial-control piece was handled by the system rather than by the reporting line, would they agree this team should report to the Operations Head instead, given how heavily Operations depends on this function's efficiency (§3a)?
2. What is the actual average payment-days-outstanding against agreed credit terms, by vendor — not the policy, the ledger?
3. Has any vendor, in the last year, raised rates, shortened credit, reduced priority, or deprioritised deliveries to this hospital? What reason did they give, and what reason does Purchasing believe?
4. What proportion of purchase value in the last four quarters was emergency or spot purchase outside a rate contract, and what was the average price premium on it?
5. Does anyone attribute that premium back to payment delay, or is it logged as a procurement performance failure? This question is the hinge of the whole cluster — the loop in §3b(E) is usually visible in the data and invisible in the narrative.
6. Who sets the inventory holding target, against what — a working-capital number, a stock-out tolerance, or neither? And who is accountable when the two conflict?
7. Are vendor rebates earned, tracked, and netted back into per-item cost, or do they land as a lump credit nobody attributes to an item?

**F. Biomedical & Engineering** — *symptom: uncompetitive cost-per-test, spares bought twice.*
1. Which installed equipment runs on closed-system, proprietary or reagent-rental consumables, and what share of total consumable spend do those represent? Most hospitals have never computed the share.
2. For the last three significant equipment purchases, was Procurement consulted on the lifetime consumable-cost implication *before* the purchase was committed?
3. Is the reagent or consumable cost-per-test assumed in each machine's business case tracked against actuals afterwards — and by whom?
4. Which spares are covered inside an AMC/CMC, and is that inclusion list mapped into the item master so the same part can't also be purchased separately? Ask for an instance where it was caught.
5. When a closed-system contract comes up for renewal, who negotiates it — Biomedical, Procurement, or neither, because it auto-renews?

<!--chunk
id: sup.7.2.3.2
title: Cross-function root-cause clusters — part 2 (G–L)
summary: Six question clusters keyed to the §3b couplings for Quality, Pharmacy/OPD, Housekeeping, Bed Management, IT and HR, continuing part 1's letter keying.
keys: root cause questions, audit evidence, parallel record, narcotic register, cold chain excursion, OPD dispensing share, formulary reconciliation, housekeeping indent, forward demand signal, enforced versus configured, override log, receipt peak roster
needs: sup.3b, sup.7.2.3
see: sup.7.2.2, common.peak-load
tokens: 1160
-->
#### 7.2.3 Cross-function root-cause clusters — part 2: compliance, retail, support and systems couplings (G–L)

Continues part 1's letter keying against §3b. Same instruction: run the cluster whose symptom the hospital has described, not the whole set.

**G. Quality, Compliance & Accreditation** — *symptom: clean audits alongside real traceability failures.*
1. For the last accreditation audit, was the traceability evidence produced from the live system, or compiled specially for the audit? If compiled, the accredited process and the operating process are different processes.
2. Can someone produce, right now and without preparation, the current near-expiry list at ward sub-store level, and the batch-and-expiry trail for a specific item issued to a specific patient last month?
3. Is the narcotic register reconciled against system stock daily, by whom, and is the reconciler independent of the custodian?
4. Where cold-chain temperature is monitored, is an excursion recorded and acted on, or recorded and filed? Ask for the last excursion and what happened after it.
5. Who owns biomedical-waste segregation at the point where a consumable is disposed of — and is that the same person accountable for the consumable's issue record?

**H. Pharmacy retail & OPD** — *symptom: OPD pharmacy revenue below expectation.*
1. What proportion of OPD prescriptions written by the hospital's own consultants are dispensed at the in-house pharmacy? If this isn't measured, it is almost certainly worse than assumed.
2. Of those not dispensed in-house, how many were because the item wasn't in stock at that moment, versus price, versus patient preference? These need three different fixes and are routinely treated as one.
3. Is the OPD formulary reconciled against what this hospital's consultants actually prescribe — who does that, and how often? A formulary set by category and not by prescribing pattern guarantees counter-level stock-outs.
4. Are OPD retail and IPD issue reported with separate revenue and margin, or blended into one pharmacy number (see §7.2.2 Q17)?
5. Does OPD pharmacy stock-out at the counter get recorded as a lost-sale event at all, or does the patient simply leave without a trace?

**I. Housekeeping** — *symptom: untracked spend, a second parallel item list.*
1. Are housekeeping and linen consumables on the same item master and the same indent workflow as clinical consumables, or a separate parallel process?
2. When the store is under pressure, what actually happens to a housekeeping indent — and when a shared item is contested between a ward and housekeeping, what decides it?
3. Does Housekeeping ever purchase directly, outside the procurement process? Ask for the value, not just whether.

**J. Bed Management** — *symptom: stock-outs that were predictable.*
1. Does anything in the reorder calculation read the forward planned-admission or elective OT schedule, or is it entirely trailing-consumption-driven?
2. Who, if anyone, is told in advance about a known demand change — a new unit opening, a seasonal surge, a camp, a large elective list?
3. When the hospital last ran at unusually high occupancy, which items stocked out — and was that predictable from the admission picture it already held?

**K. IT / ERP** — *symptom: controls that exist on paper and are routinely bypassed.*
1. For each of: single item master, two-sided inter-store transfer, three-way match before payment, and no rate override at PO or payment — is the rule **enforced by the system** (the transaction cannot complete) or **configured as policy** (the transaction completes and someone is meant to have followed the rule)?
2. Who holds the rights to override each of those, how often was each overridden last quarter, and is the override logged with a reason?
3. Is the materials module purpose-built for perpetual inventory, or a batch-oriented module adapted to it? Ask specifically whether ward-level barcode or mobile indent capture exists at all.

**L. HR / Workforce** — *symptom: GRN backlog and slow issue reported as system problems.*
1. What is the hourly profile of inbound receipts across a typical day, and of issues — and how does the store and receiving roster map onto those two peaks?
2. Has anyone run the staffing ratio-check for receiving, store issue, or pharmacy counter against peak-hour volume rather than daily average (`common-elements.md`, Peak-Load Staffing & Manpower Cost-Benefit Method)?
3. Is the function currently staffed on the reasoning that headcount will be added once volume justifies it? If so, name it as the causal-direction error that method identifies, not as a neutral operating choice.

<!--chunk
id: sup.7.3
title: Financial parameters to check
summary: The fifteen financial parameters a supply chain case is argued against, including spot-purchase premium and closed-system spend share as the two the map added.
keys: inventory turnover, DIO, fill rate, GRN price variance, landed cost, rebates, payment days, spot purchase premium, pharmacy margin, COGS, ARPOB, closed system share, expiry write-off, shrinkage, working capital, discharge delay attributable
needs: none
see: sup.7.2.2, sup.7.4, sup.8.2
tokens: 380
-->
### 7.3 Financial parameters to check

Inventory turnover ratio and Days Inventory Outstanding (DIO) · fill rate and number of stock-out incidents, by criticality class · GRN-to-invoice price variance % · **true landed cost vs. invoice price** — freight, taxes and volume-based vendor rebates netted in, not just face invoice value (per §7.2.2 Q13; this distinction is commonly ignored and materially changes real vendor economics) · vendor payment days outstanding vs. agreed credit terms · **spot/emergency purchase value as a share of total purchase, and the price premium carried on it** (the measurable signature of §3b(E)'s loop) · pharmacy revenue and margin, tracked separately for OPD and IPD · Cost of Goods Sold as a % of pharmacy revenue · consumable and medicine cost as a % of ARPOB · **closed-system/proprietary consumable spend as a share of total consumable spend** (§3b(F) — the portion of this department's cost base it has no negotiating power over) · expiry write-off value and % of inventory · shrinkage/unexplained-adjustment value and % · working capital tied up in inventory, and its trend · **discharge-process delay attributable to this department specifically** — the portion of discharge-cycle time driven by manual stock-taking, returns processing and chargeable-item finalization after the doctor's discharge confirmation. That last one is the direct ALOS/EBITDA link raised in §7.1, and it is the number that actually answers "have you quantified the EBITDA impact."

<!--chunk
id: sup.7.4
title: Solution construction method
summary: That this department's solution is scale-variant unlike Discharge's, but that the automation itself is not scale-gated — only its configuration and surrounding staffing vary.
keys: solution construction, scale variant, scale invariant, configuration versus capability, cost benefit, before after comparison, four aspects, hospital size, store depth
needs: common.solution-method
see: sup.7.4.1, sup.7.4.2, sup.7.4.3, sup.7.4.4, dis.7.4, bed.7.4
tokens: 390
-->
### 7.4 Solution construction method

Follows the two universal rules in `common-elements.md`: mandatory cost-benefit analysis plus a side-by-side graphical before/after comparison, and the four-aspect solution shape.

**This department's solution is scale-variant**, unlike Discharge Process's scale-invariant pattern. Discharge Process's solution is the same recommendation at every hospital size, with only the cost-justification timing varying by occupancy and volume (`discharge-process.md` §7.4). Supply Chain doesn't follow that shape — a 50-bed hospital genuinely doesn't need the same store/sub-store depth, ERP sophistication, or staffing structure as a 400-bed one.

The nuance that matters: **the automation itself is not scale-gated.** Hospitals of any size can adopt the same underlying capabilities — item master, real-time issue and consumption tracking, GRN automation, predictive requisition — once automation is provided. What varies by scale is the *configuration* of that automation (how many store and sub-store levels are actually needed, how much of the four-aspect solution is warranted) and the staffing that sits around it (§7.4.4), not whether the underlying capability is available to smaller hospitals at all. <!--m-->This is a second confirmed data point, alongside Discharge Process's opposite finding, on the open question in `common-elements.md`'s "what is NOT assumed universal" — worth revisiting there once a few more departments are built, per that file's own note.<!--/m-->

Department-specific answers to the four required aspects:

<!--chunk
id: sup.7.4.1
title: Automation — the shared ledger and the closed loop
summary: The core architecture: one item master, a ledger per location, rights-based workflow, shortage allocation rules, straight-through PO logic, three-way match, and enforcement over configuration.
keys: automation, item master governance, store hierarchy, sub-store ledger, rights workflow, two-sided transfer, conflict resolution, allocation priority, PO automation, rate contract, three-way match, enforced control, override logging
needs: sup.7.4
see: sup.7.4.1.2, sup.7.4.2, sup.3b
tokens: 850
-->
#### 1a. Automation — the shared ledger and the closed loop

**Core capability:** one shared item master, one continuously-updated stock ledger per store and sub-store, and a closed loop from indent through issue through consumption through billing through return — so that at any moment the system knows exactly what is on hand, what has been promised (open indents and POs), what has been issued to a specific patient, and what has actually been consumed versus what is still returnable.

- **Item master governance**: one item, one code, no store-local duplicates. Every store and sub-store draws reorder parameters (ROL/ROQ, min/max) *specific to that location's velocity*, but against the same shared master, so aggregate demand stays visible centrally even though replenishment is managed locally.
- **Store/sub-store hierarchy**: a Central Store (main receiving, bonded stock) feeding a Pharmacy Store (bulk) and a Central Consumables Store, which in turn feed ward, OT and ICU sub-stores (floor stock), which is what's actually issued to a patient. Each level is its own inventory location with its own ledger, tied to the shared master.
- **Rights-based workflow**: indent-creation rights sit with the relevant clinical in-charge (ward nursing in-charge, OT in-charge); requisition approval sits one level up (ward manager or matron) before it reaches the store; inter-store transfer requires two-sided confirmation, so a transfer can't be logged as sent on one side and never received on the other; returns require the item to be unopened, undamaged and in date, and route back through the same approval chain in reverse.
- **Conflict and priority resolution**: conflicts don't arise from the same item being *mapped* to multiple stores — each sub-store's stock is genuinely its own ledger. They arise when procurement is centralized, demand is distributed, and a shortage hits. The system needs a defined allocation rule (Critical Care and OT indents take priority over General Ward during a shortage of a shared item) rather than first-come-first-served or relationship-based allocation, and it needs aggregate-demand visibility so two sub-stores don't independently place duplicate reorders for the same scarce item without either seeing the other's request. The same rule must cover the clinical-versus-Housekeeping contest in §3b(I), which otherwise resolves silently in clinical's favour every time.
- **PO logic**: routine reorders against a pre-approved vendor/rate combination generate a PO automatically and go straight through; new vendors, new rates, high-value items and emergency purchases route to manual review by the purchase authority. Vendor approval and rate approval sit with a defined committee or authority on an annual or quarterly rate-contract cycle — a distinct, higher-level decision from day-to-day PO issuance against an already-approved rate.
- **Three-way match**: no payment releases without indent/PO, GRN and invoice agreeing. Single most effective control against both overpayment and unauthorized rate drift.
- **Enforcement, not configuration.** Every control above must be one the system refuses to complete rather than one people are asked to follow, with any override rights named, logged and reason-coded (§3b(K), §7.2.3 K1–K2). A control that can be worked around becomes a convention within months, and nobody finds out until an audit or a loss.

<!--chunk
id: sup.7.4.1.2
title: Automation — capture, prediction and the Discharge tie-in
summary: What layers on the ledger: automated GRN, real-time issue-to-billing, returns policy, preference cards as system objects, predictive and forward-demand flagging, voice entry and a daily P&L.
keys: GRN automation, barcode OCR EDI, issue to billing linkage, consumption capture, returnable unit, returns write-off, preference card system object, predictive requisition, forward demand, price master coupling, voice entry, daily P&L dashboard, discharge tie-in
needs: sup.7.4.1
see: sup.7.4.2, dis.7.4.1, sup.3b
tokens: 1200
-->
#### 1b. Automation — capture, prediction and the Discharge tie-in

Layered on the ledger in 1a:

- **GRN entry itself is automated, not merely downstream of automation.** Capture the vendor invoice/challan and batch/expiry data at the gate — barcode, OCR or EDI against the PO — and auto-generate the GRN from that match, with a human touching only exceptions: short receipt, damage, price mismatch. This is the inbound-side equivalent of real-time issue and consumption capture on the outbound side, and both matter equally for the ledger to stay trustworthy.
- **Real-time issue-to-billing linkage**: stock issued from a sub-store against an indent decrements that location's ledger and simultaneously posts to the patient's running bill *for what was issued*. A separate consumption-recording step — ideally point-of-administration, eMAR-style — tracks what was actually used, down to a returnable-unit denomination (strips, bottles, whole units; never fractional, per `discharge-process.md` §7.4.1(d)–(e)). The gap between issued and consumed is exactly what determines what's returnable, what's billable and what's written off.
- **Returns and write-offs**: unopened, in-date stock returns to the sub-store ledger and is credited off the patient's bill; opened or part-used, non-returnable stock is billed for what was used and written off as wastage for the remainder. This must be a defined, consistently-applied policy, not a case-by-case judgment call at the ward (§7.2.3 D4).
- **Service-to-item mapping**: OT preference cards and standardised bed/ICU daily kits auto-issue against the relevant trigger — case booked, bed-day — rather than requiring a fresh manual indent each time, with periodic reconciliation of actual usage against the kit to catch drift. Critically, the preference card must be **a system object owned per surgeon per procedure**, and a change to the OT list must fire a store-side event, not a phone call (§3b(A)).
- **Predictive store and sub-store requirement flagging, ahead of any physical stock check**: derive expected requirement at each location — especially ward sub-stores — from the trend in issues and consumption, and flag a likely requirement before anyone has physically counted. This goes beyond ordinary ROL/ROQ reorder logic, which reacts to a known stock level crossing a threshold; here the system anticipates need from consumption velocity, closing the gap between "the ward actually needs this soon" and "someone happened to notice."
- **Forward-demand input, not trailing consumption alone**: the same predictive engine reads the planned-admission and elective OT schedules (§3b(J)), so known future demand enters the reorder calculation instead of arriving as a surprise. This is the retail footfall-forecast analogy in §7.1 made concrete.
- **Price-master coupling**: a change to a negotiated purchase rate raises a mandatory review of the corresponding patient-billable rate, and a new item cannot be issued until it exists in both masters (§3b(C)).
- **Voice-based entry**: offer voice capture as an input method for consumption entries, indents and requisitions — the same adoption logic as the doctor voice-capture pattern in `discharge-process.md` §7.4.3 and `bed-management.md` §7.4.3, extended to nursing, ward and store staff. It removes a friction point (typing and screen navigation at the point of care) that is a large part of why real-time entry gets skipped under pressure in the first place.
- **Daily P&L dashboard**: same-day reconciliation of pharmacy sales revenue (OPD) and provisional IPD revenue booked against the actual cost of items issued, by ward and department, surfacing variance the same day rather than at month-end audit.

**This department's automation and Discharge Process's automation are two halves of one build, not two separate initiatives.** The real-time stock-taking and returns capture described above *is* the data source `discharge-process.md` §7.4.1 needs for its provisional-evening/final-morning billing flow. Scope and sequence the two together — building this department's issue/consumption/returns automation without wiring it directly into Discharge's event log gets you accurate inventory but not the discharge-speed benefit that is the actual point.

**Net effect, once mature:** billing accuracy stops depending on a manual reconciliation step anywhere in the chain; Discharge's provisional-evening/final-morning automation becomes fully supportable because the consumption data it needs already exists in real time; stock-outs of critical items become rare because reorder is demand-driven, forward-looking and centrally visible rather than dependent on someone at the ward noticing; and shrinkage and leakage that were previously invisible inside "adjustment" entries become visible and attributable.

<!--chunk
id: sup.7.4.2
title: Solution construction — process changes
summary: The eight process shifts the automation presupposes, including that indent discipline only survives if lead time is trustworthy and that payment discipline becomes a supply chain control.
keys: process change, system indent, urgent indent discipline, lead time trust, cycle count, rate contract negotiation, consumption recording, predictive requisition, OT list freeze, payment run discipline, ERP enforcement
needs: sup.7.4.1
see: sup.7.4.1.2, sup.7.4.3, sup.7.5
tokens: 650
-->
#### 2. Process changes

The underlying flow — indent, approval, issue, consumption, billing, return — stays the same in shape. What changes is where a human decision is replaced by a system rule, and where a human is asked to confirm rather than perform a manual step:

- Ward, OT and ICU staff shift from informally requesting stock to raising a system indent every time, including for genuinely urgent needs. The discipline has to hold under pressure, not just in routine conditions, or the real-time picture breaks down exactly when it matters most. **This only survives if the indent-to-receipt lead time is short enough to be trusted** — otherwise the buffer drawer in §3b(B) returns, whatever the policy says.
- Store staff shift from being the sole gatekeepers of what's actually there to confirming what the system already shows, with physical stock-take becoming a periodic accuracy check (cycle counts) rather than the primary source of truth.
- Purchasing shifts from negotiating *and* issuing every PO to negotiating rate contracts up front and approving only exceptions — most POs no longer require a fresh individual decision.
- Nursing and clinical staff take on real-time consumption recording at or near the point of administration, positioned explicitly as capturing what they're already doing rather than new clinical work — the same adoption framing used in Discharge Process and Bed Management.
- **Predictive requisition replaces reactive requisition**: the process shifts from someone noticing stock is low to the system raising the requisition automatically once monitored levels against the consumption trend cross a threshold. Store and ward staff move from initiating requisitions to confirming system-generated ones, which is a materially different and lighter task.
- **The OT list becomes a system trigger.** Freezing the list at a defined point, and routing every post-freeze change through the system rather than a phone call, is a scheduling-discipline change that costs nothing and removes most of §3b(A)'s failure surface.
- **Payment-run discipline becomes a supply chain control, not just a Finance one.** Agreed credit terms are met or renegotiated openly; where they cannot be met, the resulting fill-rate and spot-premium cost is quantified and shown to Finance rather than absorbed silently by Procurement (§3b(E)).
- IT/ERP must guarantee that the item master and store hierarchy are genuinely enforced — no local workarounds — and that inter-store transfer and returns are two-sided by design, not by a policy people can route around.

<!--chunk
id: sup.7.4.3
title: Solution construction — key people & buy-in
summary: Whose cooperation is required including surgeons and Biomedical, why the COO approves the cross-departmental flows, and why the audit framing guarantees the resistance it tries to avoid.
keys: buy-in, stakeholders, IT ERP, purchasing, store staff, nursing, surgeons, preference cards, finance, biomedical, pharmacy, quality, COO, head of operations, adoption framing
needs: sup.7.4
see: sup.7.4.2, sup.7.4.4, sup.7.5
tokens: 480
-->
#### 3. Key people & buy-in

Teams whose cooperation is required: IT/ERP (the whole architecture depends on this being built and enforced correctly) · Purchasing and Materials Management (rate-contract negotiation shifts from a per-PO activity to a periodic, higher-stakes one) · store and sub-store staff (real-time accountability replaces the ambiguity manual stock-take allowed) · Nursing and clinical staff at every ward, OT and ICU (consumption recording at the point of care) · OT scheduling and the surgeons whose preference cards must become documented system objects · Finance (three-way match discipline, payment-term enforcement, and the §3b(E) conversation) · Biomedical (the closed-system contract inventory in §7.2.3 F) · Pharmacy (barcode and scan discipline for both OPD retail and IPD issue) · Quality (traceability evidence produced from the live system rather than compiled for audit).

**Head of Operations / COO.** Per §3a, this is the level the Materials Manager should report to, and the level whose sign-off the cross-departmental sequencing changes in §7.4.2 require — particularly the OT list-freeze discipline and the payment-run conversation with Finance, neither of which holds without authority above both functions. Its role is to **approve the process flows**, not to participate in daily materials activity.

Buy-in mechanism: the same sequencing used elsewhere in this knowledge base — introduce the system as an extension of what each role already does, capturing information they'd otherwise track on paper or from memory, not as a replacement or an audit mechanism, in the first phase. The visibility gains (traceability, shrinkage reduction, billing accuracy) are a later, proven-trust-stage consequence, not the opening pitch. For at least some of the resistance in §7.5, framing it as an audit mechanism from day one guarantees exactly the resistance it's trying to avoid.

<!--chunk
id: sup.7.4.4
title: Solution construction — team/role changes
summary: The Materials Manager at Rs8-10 lakhs, triggered by the 80% pivot and priced for its own proficiency, plus category owners and the GRN clerk question sized at peak.
keys: Materials Manager, salary 8-10 lakhs, occupancy pivot, hiring trigger, Procurement Head, store in-charge accountability, category owner, GRN receiving clerk, peak load staffing, proficiency not trigger
needs: sup.7.4, common.occupancy-pivot
see: common.peak-load, sup.3a, dis.7.4.4, bed.7.4.4
tokens: 1000
-->
#### 4. Team/role changes

Most roles see an expansion of existing scope — indenting, confirming, recording consumption in-system — rather than a new headcount need. The clearer new-role and role-redefinition cases:

- **Materials Manager — new dedicated role, ₹8–10 lakhs/year.** Owns stores, inventory and issue-side operations end-to-end and, per §3a, sits within the Operations reporting line. **Triggered by the 80% occupancy pivot** in `common-elements.md` — the universal hospital-wide inflection, not a threshold derived for this department alone. Above it, the shortage-allocation rule in §7.4.1 starts firing for real, buffer policy inverts from a working-capital choice into a care-continuity constraint, and the coordination load exceeds what a Procurement Head carrying it part-time can absorb.
  - **The cost follows the proficiency, not the trigger.** At ₹8–10 lakhs this is roughly double a Bed Manager or Discharge Manager (₹4–4.5 lakhs each), and that is correct rather than anomalous: the same pivot triggers a different role in each function, and each is priced for what it actually has to be good at. This role carries vendor negotiation, rate-contract authority, inventory economics, systems governance and cross-department accountability. A Bed Manager or Discharge Manager is a coordination role over a defined process with a defined counterpart — real seniority, narrower scope. **Never reason from one of those figures to this one, or back.** A hospital that has already priced its Bed Manager will try to; say plainly why the two are not comparable.
  - **The cost-benefit case is still built per-role.** Crossing the pivot establishes that this role is warranted, not that it is this quarter's priority. Build the case against the leakages this department specifically owns — the spot-purchase premium (§3b(E)), the item-to-price master gap (§3b(C)), expiry and shrinkage write-offs, and the ALOS contribution in KPI #18 — and where a hospital has crossed the pivot in several functions at once, rank by which is costing most and say the ranking is a sequencing judgment, not a verdict that the others are unnecessary.
  - **A secondary volume trigger is optional, not owed.** A supply-chain-specific condition — receipts/day, issues/day, active item count, spend under management — would catch a high-throughput hospital sitting below 80% occupancy, and is worth deriving if such a case shows up. It is a refinement, not a gap: the pivot is the primary trigger and stands on its own.
- **Procurement Head — assumed already in place.** Essentially all hospitals have one, so this is not a threshold-gated recruitment question the way Materials Manager is. What §3a and §7.4.1–7.4.3 apply to is *how* that existing role operates — rate-contract cadence, approval authority, and the working relationship with Finance — not whether the role should exist.
- **Store-in-charge accountability changes materially** once real-time stock visibility exists. Not a new role, but a genuine change in what the role is answerable for, and it should be expected to surface resistance (§7.5).
- **A named category owner** for each major consumable category, per the retail category-management practice in §7.1 — replacing item-by-item negotiation. Usually a redefinition of existing Purchasing scope rather than new headcount, and it is the role that makes the §7.2.3 F closed-system inventory somebody's actual job.
- **Whether a dedicated GRN/receiving clerk is still needed**, or whether gate-entry-to-GRN becomes largely system-driven with only exception handling requiring a person, is a genuine open question to be sized against actual receipt volume per hospital — and specifically against the **peak** receipt window, not the daily average (§3b(L)). This is exactly what the Peak-Load Staffing & Manpower Cost-Benefit Method in `common-elements.md` is built for: establish real receipt volume by hour, realistic per-transaction time, and shift structure, rather than a flat headcount assumption.

<!--chunk
id: sup.7.5
title: Anticipated hurdles and resistance to automation
summary: The systems-side and manpower-side resistance to expect, including surgeon resistance to documented preference cards and staff resistance where current ambiguity is a feature.
keys: automation hurdles, resistance, bolted-on materials module, item master migration, transfer acknowledgment, rate enforcement, PACS integration, nursing charting burden, barcode discipline, purchasing discretion, surgeon preference cards, shrinkage visibility
needs: none
see: sup.7.4.1, sup.7.4.2, sup.7.4.3
tokens: 830
-->
### 7.5 Anticipated hurdles and resistance if the process is automated

This department needs its own automation-readiness section, because the hurdles are as much about incentives as about systems capability. Two distinct sources.

**From the ERP/systems side:**

- Many hospital ERPs and HIS platforms have a materials module that was bolted on rather than designed for real-time perpetual inventory — batch-oriented GRN entry, weak or absent barcode/RFID support at ward level, indent workflows built for desktop rather than mobile or tablet use at the point of care.
- Enforcing a genuinely single, de-duplicated item master across a system that has run with store-local workarounds for years is a real migration problem, not a configuration setting. Expect resistance disguised as "our items are different" when the actual issue is unwillingness to give up a local list that has been quietly customized.
- Two-sided transfer acknowledgment and rate-card enforcement — no manual override at PO or payment — are both features many hospital ERPs don't support well out of the box, or support but don't enforce by default. This needs to be checked, not assumed (§7.2.3 K1).
- Integration with PACS, lab and OT systems for automatic consumption capture at the point of use is the same integration prerequisite `discharge-process.md` §7.4.2 flags for the billing side. It doesn't exist independently here; it is the same underlying work.

**From the manpower side:**

- Nursing and clinical staff resistance to real-time consumption charting, for the reason documented in Discharge Process and Bed Management: it reads as data-entry burden layered on clinical work unless it is positioned and built as capturing what they're already doing.
- Pharmacy and store staff resistance to barcode and scan discipline, particularly where the current informal process has built-in slack that scanning removes.
- Purchasing team resistance to losing negotiation discretion once rate-card automation takes over routine PO issuance. Informal vendor relationships — and sometimes informal benefits from them — are exactly what centralized, system-enforced rate contracts remove, and that should be expected to generate real pushback rather than being dismissed as simple change-resistance.
- **Surgeon resistance to documenting preference cards.** A preference card made explicit is a preference made auditable and comparable in cost against a peer's. This is a distinct resistance from the workload-based kind and should be anticipated as part of §3b(A)'s fix, not discovered during it.
- **Store and ward staff resistance to real-time stock visibility, specifically where it exposes previously-ambiguous shrinkage or pilferage** that manual, batch-timed stock-take allowed to stay unattributed. Worth naming plainly rather than euphemistically: some resistance to this automation will come from people for whom the current ambiguity is a feature rather than a bug. That doesn't mean assuming bad faith everywhere — most resistance genuinely is workload-based — but the rollout plan should anticipate this specific dynamic rather than be surprised by it, and shouldn't rely on the "extension of your role" framing to resolve it, since that framing works for workload-based resistance and doesn't work for this kind.

<!--chunk
id: sup.8
title: KPIs — how the list is organised
summary: Heading and reading note; the forty-four KPIs are split across the supply-side and demand-side sub-sections, with every §3b coupling now carrying at least one measure.
keys: KPI, metrics, cluster organisation, supply side, demand side, cross-function measures, interdependency KPI, section container
needs: none
see: sup.8.1, sup.8.2
tokens: 130
-->
## 8. KPIs

This department is wider than the others (§0), so this list is organized into clusters rather than one flat sequence — but it reads as one continuous, cross-referenced set. Several of these are the direct, trackable form of a question in §7.2, not generic textbook inventory metrics. The cluster at §8.2's end is new in this pass: every §3b coupling now has at least one measure attached to it, on the principle that an interdependency nothing measures is a gap in the library rather than in the hospital.

<!--chunk
id: sup.8.1
title: KPIs — vendor, inbound, inventory and procure-to-pay
summary: Seventeen supply-side KPIs covering vendor scorecarding and rate governance, GRN automation maturity, inventory accuracy by ABC-VED class, and procure-to-pay controls.
keys: KPI, vendor OTIF, rate contract spend share, price variance, vendor concentration, GRN cycle time, auto GRN, short receipt, inventory turnover, stock-out by class, fill rate, cycle count accuracy, expiry write-off, straight-through PO, three-way match, payment days, predictive requisition, voice capture
needs: none
see: sup.6, sup.7.4.1, sup.7.3
tokens: 720
-->
### 8.1 Supply-side: vendor, inbound, inventory and procure-to-pay

**Vendor & rate management**

1. **Vendor OTIF (On-Time-In-Full) delivery %**, by vendor and category — the retail-derived scorecard metric named in §7.1, replacing price-only vendor evaluation.
2. **% of purchase spend under an active, approved rate contract**, vs. ad-hoc or spot purchase — measures whether the rate-card-driven PO automation in §7.4.1a is actually governing real spend, or whether exceptions have quietly become the norm.
3. **Rate-contract price variance %** — negotiated rate vs. actual price paid at invoice — the direct tracker for the stale-price-master and silent-rate-drift failure modes in §6.
4. **Vendor concentration ratio** — top vendor's % of spend, by critical category.

**Inbound receipt & GRN automation**

5. **Gate-entry-to-GRN cycle time** — the direct measure of the GRN-backlog failure mode in §6, and the metric that shows whether §7.4.1b's GRN automation is actually reducing lag.
6. **% of GRNs auto-generated (system-matched)** vs. manually keyed.
7. **Short-receipt, damage and discrepancy rate**, and average debit-note resolution time.

**Inventory & stores accuracy**

8. **Inventory turnover ratio and DIO, by ABC-VED class** — a single blended turnover figure hides very different acceptable norms across Vital, Essential and Desirable items.
9. **Stock-out incidents, by ABC-VED/criticality class** — the direct tracker for the §4 non-negotiable that critical and emergency items never stock out.
10. **Fill rate** — % of indents fully met on first issue, without partial fulfillment or backorder.
11. **Cycle-count stock accuracy %** (system stock vs. physical count variance) — the retail cycle-counting practice from §7.1, and the tracker for the phantom-inventory failure mode in §6.
12. **Expiry write-off value and %, tracked separately at central-store and ward/sub-store level** — split deliberately, because §6 flags near-expiry stock going unnoticed at the sub-store specifically, not the central store.

**Procure-to-pay & systems automation maturity**

13. **% of Purchase Orders generated automatically (straight-through)** vs. manually raised.
14. **Three-way match compliance %** — % of payments released only after indent/PO, GRN and invoice all agree — the tracker for the §4 non-negotiable against unauthorized payment.
15. **Payment days actual vs. agreed credit terms** — tracks vendor-relationship and working-capital health together, and is the leading indicator of §3b(E)'s loop.
16. **% of requisitions system-generated (predictive)** vs. manually raised by ward or store staff.
17. **% of indent, requisition and consumption entries captured via voice** vs. typed or scanned — adoption tracker for §7.4.1b's voice capability, and an early signal of whether it is actually removing the point-of-care friction it exists to remove.

<!--chunk
id: sup.8.2
title: KPIs — issue, billing, pharmacy, financial and cross-function
summary: Twenty-seven KPIs from the discharge-linked flagship metric through pharmacy channel split, EBITDA contribution, staffing thresholds and the ten new cross-function interdependency measures.
keys: KPI, chargeable item finalisation, real-time reconciliation, part-used write-off, courtesy issue, package BOM variance, OPD versus IPD margin, prescription fill rate, daily P&L variance, landed cost, ARPOB, EBITDA contribution, nurse hours lost, Materials Manager threshold, reporting line, narcotic compliance, cold chain, OT delay split, preference card currency, buffer stock, price master lag, spot premium, closed system share, audit evidence time, lost sale, forward demand, control overrides
needs: none
see: sup.3b, sup.7.3, sup.7.4.4, dis.8
tokens: 1620
-->
### 8.2 Demand-side: issue, billing, pharmacy, financial, organisational and cross-function

**Issue, consumption & the billing interface**

18. **Time from doctor's discharge confirmation to a finalized chargeable-item list, post-returns** — the specific proxy for "efficiency" in this department named in §7.1 and §7.2.2 Q2. **Treat this as the flagship KPI of the whole file**, not one metric among many.
19. **% of discharges where issue/consumption reconciliation was available in real time**, without a manual stock-take gating step — the Supply-Chain-side mirror of `discharge-process.md` KPI #6.
20. **Unreconciled / part-used, non-returnable item write-off value** — tracker for the §6 failure mode where a part-used item falls out of both the bill and the stock ledger.
21. **Off-system "courtesy issue" incidents detected** — a zero-tolerance tracker against the §4 non-negotiable that every issue traces to an indent. Any non-zero count is itself the finding, not a number to trend gently.

**Service-to-item mapping & pharmacy sales**

22. **Package/kit actual-usage-vs-presumed-BOM variance %, by package type** (OT procedure, delivery package, standard bed/ICU kit) — tracker for the margin-erosion risk in §7.1 and §7.4.1b.
23. **OPD pharmacy revenue and margin %, tracked separately from IPD pharmacy issue value and margin %** — per §7.2.2 Q17 and §2H.
24. **OPD prescription fill/capture rate** — % of OPD-prescribed value actually dispensed in-house vs. filled outside — a retail-style leakage metric most hospitals don't track at all.

**Financial / P&L**

25. **Daily P&L variance** — same-day reconciliation of pharmacy and IPD provisional revenue booked against the actual cost of items issued, by ward and department. Surfacing variance same-day rather than at month-end audit is the point of this KPI, not merely having the number.
26. **True landed cost vs. invoice price variance %, and vendor-rebate value captured** — operationalizes §7.2.2 Q13 and §7.3's landed-cost distinction into an ongoing number rather than a one-time diagnostic.
27. **Consumable and medicine cost as a % of ARPOB**, trended.
28. **Quantified ₹ EBITDA contribution from Supply Chain efficiency gains** — derived the same way Discharge Process's freed-bed-day revenue is (ALOS-hours-saved via faster discharge-charge finalization × ARPOB × No. of Beds × 365, per `discharge-process.md` §7.4.1 and `common-elements.md`), once KPI #18 has a baseline. This is the direct answer to §7.2.2 Q1. Where a hospital can't produce this number, that gap is itself the finding.

**Staffing, ratios & organizational positioning**

29. **Nurse and ward-staff hours lost per day to stock-taking, indenting and store/pharmacy follow-up** — turns §7.2.3 B5 into an ongoing tracked number. Usually invisible to management precisely because nobody measures it.
30. **Receiving and store staffing ratio against peak-hour receipt and issue volume** — the Peak-Load Staffing Method applied to this department's own open staffing question in §7.4.4, at both peaks rather than one.
31. **Materials Manager threshold tracking** — occupancy % tracked against the **80% pivot** in `common-elements.md`, which §7.4.4 names as this role's primary and only derived trigger, as an operational trigger metric in its own right, the same way Bed Manager's and Discharge Manager's thresholds are tracked in their departments. *(No volume condition is tracked alongside it: per §7.4.4 a supply-chain-specific volume trigger — receipts/day, issues/day, active item count, spend under management — is a refinement that has not been derived, so tracking one would imply a threshold the file does not set. Procurement Head is not tracked here either, being assumed already in place rather than threshold-gated.)*
32. **Reporting-line status** (Operations vs. Finance) — not a numeric KPI but a standing status flag against the §3a ideal, reviewed periodically rather than continuously, and revisited whenever the organization restructures.

**Compliance & safety**

33. **Schedule H1/X and narcotic-handling audit compliance %** — zero-tolerance tracker against the §4 regulatory non-negotiable.
34. **Cold-chain temperature-excursion incidents**, and the proportion acted on rather than merely recorded (§7.2.3 G4).

**Cross-function interdependency** — *new in this pass; one measure per §3b coupling that would otherwise go unmeasured.*

35. **OT delays coded to consumables, split into "not in the hospital" vs. "not on the trolley"** (§3b(A), §7.2.3 A3). The split is the metric; a hospital that reports a single blended number has not yet separated a Supply Chain failure from a mapping failure.
36. **Preference-card coverage and currency** — % of OT procedures with a documented, in-system preference card, and the median age of those cards since last revision (§3b(A)).
37. **Ward buffer-stock value discovered at cycle count**, and median indent-to-receipt lead time, routine and urgent, tracked as a pair (§3b(B), §7.2.3 B1–B2). The pair matters: the buffer is the dependent variable and the lead time is the cause, and reporting either alone invites the wrong fix.
38. **Item-master-to-price-master reconciliation lag** — median days between a negotiated purchase-rate change and the corresponding patient-billable rate review (§3b(C), §7.2.3 C2).
39. **Spot/emergency purchase price premium, reported alongside payment-days-outstanding** (§3b(E)). Same principle as #37: these two numbers are only diagnostic when shown together, because the loop is invisible in either one alone.
40. **Closed-system/proprietary consumable spend as a share of total consumable spend** (§3b(F), §7.3) — the portion of this department's cost base it has no negotiating power over, and the number that makes the Part 1 / Part 2 seam visible in the P&L.
41. **Audit-evidence production time** — how long it takes to produce traceability evidence from the live system without preparation (§3b(G), §7.2.3 G1–G2). A hospital that needs days is maintaining a parallel record.
42. **OPD pharmacy lost-sale events recorded at the counter**, by cause — stock-out vs. price vs. patient choice (§3b(H), §7.2.3 H2).
43. **% of reorder value driven by forward demand signal** (planned admissions, elective OT list) vs. trailing consumption alone (§3b(J)).
44. **System-enforced control overrides per quarter, by control and by user, with reason codes** (§3b(K), §7.2.3 K2) — the measure of whether the controls in §7.4.1a are enforced or merely configured.

<!--m-->*(KPIs #1–34 were drafted 2026-09-04 and have never had your review pass; #35–44 are new in this revision and follow from the §3b work. All 44 are pending your line-by-line review, correction and approval, same as the other three departments' lists.)*<!--/m-->

---

<!--chunk
id: sup.status
title: Status, change log and open items
summary: What was approved when, the Materials Manager cost resolution, the trigger contradiction it opened, and what remains outstanding including the chunking and index work.
keys: status, change log, open items, approval, Materials Manager cost, trigger condition, cold chain deferred, common elements promotion, chunking pass, index card, manifest
needs: none
see: none
tokens: 1200
retrieve: never
-->
## Maintainer block — not for retrieval

*This section carries `retrieve: never` when the file is chunked. It is here for maintainers and must never reach a hospital.*

### Change log

- **2026-09-04** — First draft, §1–8, one full pass. Corrected the same day with Avishek's round-1 additions to §3 (organizational placement), §7.1–7.4 and the open-items section; KPI list (34 items, 9 clusters) delivered the same day.
- **2026-09-05** — Two structural resolutions. The solution is **scale-variant** (the opposite finding from Discharge Process's scale-invariant pattern — a second data point for `common-elements.md`'s open question there), with the automation itself not scale-gated, only its configuration and surrounding staffing. **Materials Manager** gated by the **>80% occupancy or >40 discharges/day** threshold ported directly from Discharge Executive. **Procurement Head** assumed already in place at essentially all hospitals, not a threshold-gated recruitment question.
- **2026-09-16** — v2 alignment and interdependency pass. Restructured from §0–§10 to the standard §0–§8 template (KPIs moved from §10 to §8; the old §8 automation-hurdles section became §7.5; the old §9 open-items section was retired, with its four items folded into the content that supersedes them and the genuinely open ones moved here). **New §3b cross-function interdependency map** — twelve couplings, each with its mechanism and the failure that propagates along it. **§7.2 rebuilt in three parts**: §7.2.1 data/system access (new, matching the Discharge file's shape), §7.2.2 internal practice questions (the former 21, reordered and trimmed of the ones now living in §7.2.3), §7.2.3 twelve per-function root-cause clusters keyed to §3b. **§7.4.1 split** into 1a (ledger and closed loop) and 1b (capture, prediction, Discharge tie-in) for the 2,000-token chunk ceiling. **§8 split** into §8.1 supply-side and §8.2 demand-side for the same reason, with a new cross-function cluster, KPIs #35–44. Provenance fragments wrapped in maintainer spans throughout.

### Still open — needs Avishek

1. **Cold chain.** Kept in scope of this file (the §4 non-negotiable and KPI #34 cover it at framework level), with the deeper protocol and equipment-integration detail deferred to a separate offline discussion. Still deferred.
2. **§3a's COO-vs-CFO position** is a common-elements promotion candidate. Nothing currently tracks promotion candidates across departments. Worth deciding whether that register lives in `common-elements.md` or here.

### Resolved 2026-09-16

§1–§8 approved in full by Avishek, including all 44 KPIs. Materials Manager cost set at **₹8–10 lakhs/year**, replacing the ported ₹3–3.5 lakh figure. §3 priority ratings approved as drafted, including the two rows added in this pass (Bed Management upstream, Nursing clinical time downstream). **§3b confirmed as a template change**, applied retroactively to `discharge-process.md`, `bed-management.md` and `opd-diagnostic-leakage.md` in the same pass. Supply Chain / Discharge co-fetch: "could be considered" — not adopted, left as a retrieval-tuning decision for after real query logs exist rather than asserted in the manifest now. **Materials Manager trigger resolved (Avishek):** 80% occupancy is a universal hospital-wide pivot triggering a different role in each function, with salary set by the proficiency each role requires rather than by the shared trigger. Promoted to `common-elements.md` as `common.occupancy-pivot` and referenced from all four §7.4.4 sections; the ₹8–10 lakh figure is no longer in tension with anything.

### Chunking pass — complete

Every item on this checklist was carried out in the 2026-09-22 pass: `sup.*` chunk IDs and full front-matter (id, title, summary, keys, needs, see, tokens) on all 28 sections · this block converted to a `sup.status` chunk carrying `retrieve: never` · `index/sup.card.md` written · `index/points/sup.points.md` written and merged into `POINT-INDEX.md`, including the cross-reference rows for the concepts §3b shares with the other files · `sup` added to `GROUP-CATALOGUE.md` group 9, which it no longer leaves empty · the file, its `common-elements` pin and the proposed-not-adopted co-fetch pair declared in `publish/manifest.yaml` · `SKILL.md`'s library table, chunk and token totals and description updated to 28 chunks / 21,770 tokens · renamed to `references/supply-chain-procurement.md` · `lint_chunks.py` gained `sup` in its `PREFIXES` tuple, and both lints run clean over this file.

The one item that is genuinely outstanding sits elsewhere: `lint_chunks.py` does not yet carry `seq` in `PREFIXES`, so the conversation-sequences file fails the lint. That is tracked in `HANDOVER-FOR-DEVELOPER.md` §5 step 1 and is not a defect in this file.

**Proposed co-fetch pair:** Supply Chain and Discharge Process, on the same reasoning that pairs Discharge and Bed Management — §3b(D) and §7.4.1b make them two halves of one build, and a discharge-delay query attributed to pharmacy reconciliation is unanswerable from either file alone. Needs your call, since it is a retrieval-cost decision as much as a content one.
