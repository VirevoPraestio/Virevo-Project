# Supply Chain & Procurement (consumables, medicines, materials) — index card

Covers consumables, medicines, surgical items and general materials end to end: vendor contracting and rates, inbound receipt and GRN, stores and sub-stores, the ERP architecture behind them, procure-to-pay, issue and consumption, returns, and the two pharmacy channels. A query belongs here when it touches stock-outs, inventory or expiry, vendor rates or payment, item or price masters, what a patient was charged for an item, pharmacy revenue, or a discharge delayed by pharmacy reconciliation. **Capital procurement — equipment, expansion projects, contractors, major AMC/CMC — is a separate file**; this one meets it at `sup.3b` row F.

**Group:** Pharmacy & Supply Chain
**Pinned with:** common-elements  **Co-fetches:** none <!--m-->(a Discharge pair is proposed and deliberately not adopted — see the manifest)<!--/m-->

| id | covers |
|---|---|
| sup.0 | why the file spans the whole vendor-to-patient chain |
| sup.1 | purpose: availability, controlled cost, reconcilable record |
| sup.2 | nine sub-functions, vendor contracting through financial monitoring |
| sup.3 | eight upstream and eight downstream dependencies, by priority |
| sup.3a | COO vs CFO reporting line; the gap is itself diagnostic |
| sup.3b | twelve couplings as mechanisms; where each is misattributed |
| sup.4 | seven non-negotiables incl. cold-chain monitoring |
| sup.5 | what flexes: stock-take cadence, substitution, bounded GRN lag |
| sup.6 | fourteen failure modes incl. buffer drawer, payment spiral |
| sup.7 | container heading for chat-agent handling |
| sup.7.1 | considerations; misattribution rule; two staffing peaks |
| sup.7.2 | how the three-part protocol runs, and in what order |
| sup.7.2.1 | ten data pulls, incl. ones Biomedical and OT hold |
| sup.7.2.2 | twenty internal practice questions |
| sup.7.2.3 | root-cause clusters A–F: OT, nursing, billing, discharge, finance, biomedical |
| sup.7.2.3.2 | root-cause clusters G–L: quality, pharmacy, housekeeping, beds, IT, HR |
| sup.7.3 | fifteen financial parameters incl. spot premium, closed-system share |
| sup.7.4 | scale-variant solution; automation itself not scale-gated |
| sup.7.4.1 | automation 1a: shared ledger, rights, three-way match, enforcement |
| sup.7.4.1.2 | automation 1b: GRN capture, prediction, Discharge tie-in, voice |
| sup.7.4.2 | eight process changes; indent discipline needs trustworthy lead time |
| sup.7.4.3 | cooperating teams incl. surgeons; COO approves the flows |
| sup.7.4.4 | Materials Manager ₹8–10L; ported trigger no longer fits |
| sup.7.5 | systems and manpower resistance, incl. where ambiguity is a feature |
| sup.8 | container heading; how the KPI list is organised |
| sup.8.1 | KPIs 1–17, supply side |
| sup.8.2 | KPIs 18–44, demand side and cross-function |
| sup.status | maintainer changelog and open items — never fetched (`retrieve: never`) |

**Retired ids:** none
