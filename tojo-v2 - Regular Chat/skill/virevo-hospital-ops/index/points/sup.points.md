# Supply Chain & Procurement — point index

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
