# Tojo ↔ Dr. Mehta — Onboarding Conversation Script

**Project:** Virevo Agentic AI CEO · Sunrise Multispecialty Hospital
**Scope:** Step 1 (Project Brief & Problem Statement) → Step 2 (Model Validation & Data Monitoring, Week 2 + Week 5 updates)
**Mode:** Keyword-triggered dialogue. Dr. Mehta's phrasing can vary; Tojo's responses fire on detected keywords/patterns.
**Tone:** Operational. Clipped. No flourish.

---

## How to read this document

Each turn is laid out as:

- **Turn ID** — state machine reference
- **Actor** — `MEHTA` (user input, trigger-driven) or `TOJO` (response, scripted)
- **Example utterance** — one realistic phrasing of what the user types
- **Triggers** — regex patterns that fire this turn
- **Response** — Tojo's exact text
- **Notes** — implementation notes where useful

Section 1 = the **readable dialogue script** (turn-by-turn).
Section 2 = the **JS data structure** (drop into `app.js` or equivalent).

---

# SECTION 1 — DIALOGUE SCRIPT

## Phase 0 — Onboarding

### T0_OPENING `[MEHTA]`

> **Example:** *"So, how do I get started with this?"*

**Triggers:**
```
/how (do|should) (i|we) (start|begin|proceed|do this)/i
/where do (i|we) (start|begin)/i
/what (do|should) i do (now|first|next)/i
/how does this work/i
/ready to start/i
/^\s*(start|begin|hi|hello|hey)\s*$/i
```

---

### T1_TOJO_INTRO `[TOJO]`

> Hi Dr. Mehta. I'm **Tojo** — your point of contact through this engagement. Working with me is the **Virevo CEO Agent**: the analytical engine that ingests your hospital's data, builds a mathematical model of how everything fits together, and runs the simulations we'll use to make decisions. I handle the conversation; the Agent handles the maths.
>
> Quick choice before we begin: do you want me to walk you through the **whole process end-to-end** first, or take it **one step at a time** and explain each step as we get there?

---

### T2_WALKTHROUGH_CHOICE `[MEHTA]`

> **Example:** *"Let's go step by step."*

**Triggers:**
```
/step by step/i
/one (step )?at a time/i
/one by one/i
/as we go/i
/walk me through/i
/take me through/i
/each step/i
/the (latter|second)/i
```

---

### T3_STEP1_INTRO `[TOJO]`

> Good. We'll start with **Step 1 — Project Brief and Problem Statement.**
>
> This part is a conversation. I need to understand your hospital — what it does, how it runs, what's working, what isn't. You can **type or dictate**.
>
> If you're dictating: start the first time with **"Hey Tojo."** Do the same after any long pause. Otherwise, just keep going.
>
> Share whatever feels relevant — size, specialties, the problems on your mind, the causes you've already identified, anything you think I should know. I'll interject only when I need a clarification. Once I have a clear picture, I'll work out which datasets the Agent and I need access to.
>
> Take your time. Go ahead.

---

## Phase 1 — Step 1: Project Brief

This is a **multi-topic listener** phase. Dr. Mehta can talk about any of the topics below in any order, and bring up multiple in one message. The engine:

1. Detects all topics present in his message
2. Marks them covered
3. Composes an acknowledgment line per detected topic
4. Fires the next unfired probe at the end of the response

### Topic detection map

| Topic key | Patterns (illustrative) | Ack line |
|---|---|---|
| `beds` | `/150 beds?/i`, `/\b12 icu\b/i`, `/\b6 nicu\b/i`, `/\b3 ot/i`, `/operating theatres?/i` | `– 150 beds, 12 ICU + 6 NICU, 3 OTs (2 gen, 1 ortho)` |
| `specialties` | `/ortho/i`, `/gen(eral)? surg/i`, `/gyn(a\|ae)/i`, `/internal med/i`, `/cardio/i`, `/visiting/i`, `/multispecialty/i` | `– Ortho, gen surg, gynae, IM + visiting cardio` |
| `location` | `/nashik/i`, `/maharashtra/i`, `/tier[- ]?2/i` | `– Nashik, Tier-2` |
| `revenue_stagnation` | `/revenue.{0,30}(flat\|stagnant\|stuck\|not grow)/i`, `/73 ?cr/i`, `/high occupan/i`, `/occupan.{0,20}high/i` | `– ~80% occupancy, ₹73Cr revenue, stagnant 2 years` |
| `ebitda` | `/ebitda/i`, `/\b8 ?%/i`, `/everything (looks\|seems) (equally )?important/i`, `/don'?t know (where\|which) to focus/i`, `/which (lever\|area) to (pull\|prioritise)/i` | `– EBITDA stuck at 8%, priority unclear` |
| `los` | `/\blos\b/i`, `/length of stay/i`, `/(5\|five) days?/i`, `/(higher\|longer) than (benchmark\|target)/i` | `– LOS ~5 days vs ~4 target` |
| `diagnostic_leakage` | `/diagnostic leakage/i`, `/leak(age\|ing)/i`, `/scans? going (out\|outside)/i`, `/outside scans?/i` | `– Diagnostic leakage (your hypothesis: scans going out)` |
| `marketing` | `/marketing/i`, `/footfall/i`, `/opd.{0,20}(full\|maxed\|capacity)/i`, `/more patients/i` | `– Marketing pressure on an already-full OPD` |
| `manpower` | `/manpower/i`, `/staff(ing\| costs?)/i`, `/agency nurs/i`, `/nurs(e\|ing) costs?/i`, `/rationali[sz]e/i`, `/efficiency/i` | `– Manpower / agency nursing flagged for review` |

### Example flow through the listener

#### MEHTA_TURN_A `[MEHTA]`

> **Example:** *"Alright. Sunrise is 150 beds, multispecialty, in Nashik. 12 ICU beds, 6 NICU, 3 OTs — two general, one ortho. Specialties are orthopaedics, general surgery, gynae, internal medicine, plus a visiting cardiologist. Occupancy is around 80%, but revenue has been flat for two years. ₹73 crore last year. EBITDA stuck at 8% and I genuinely don't know where to focus first — everything looks equally important."*

**Topics detected:** `beds`, `specialties`, `location`, `revenue_stagnation`, `ebitda`

#### TOJO_TURN_A `[TOJO]` — ack + Probe 1

> Logged:
> – 150 beds, 12 ICU + 6 NICU, 3 OTs (2 gen, 1 ortho)
> – Ortho, gen surg, gynae, IM + visiting cardio
> – Nashik, Tier-2
> – ~80% occupancy, ₹73Cr revenue, stagnant 2 years
> – EBITDA stuck at 8%, priority unclear
>
> Before you go further — **how many MRI units do you have, and are they in-house or outsourced?**
>
> *(Diagnostic capacity is one of the quietest LOS levers — worth pinning early.)*

---

### Probe 1 — MRI (2-stage)

#### MEHTA_PROBE1_RESPONSE `[MEHTA]`

> **Example:** *"One MRI. It's outsourced — vendor runs it from a corner of radiology."*

**Triggers (confirm stage):**
```
/\b1 mri\b/i, /one mri/i, /single mri/i
/mri.{0,15}outsourced/i, /outsourced.{0,15}mri/i, /vendor/i
```

#### TOJO_PROBE1_FOLLOWUP `[TOJO]`

> Outsourced single unit, noted. Worth flagging now: diagnostic leakage in most units isn't about referrals going elsewhere for kickbacks — it's about **slot availability**. Patients who can't get a scan in 4 hours get sent out, and the case clock keeps running. Have you ever evaluated a second in-house MRI?

#### MEHTA_PROBE1_PUSHBACK `[MEHTA]`

> **Example:** *"Yes, but the capex is steep and I'm not convinced the volumes justify it. Maybe later."*

**Triggers (pushback stage):**
```
/capex/i, /\bcost\b/i, /steep/i, /expensive/i
/not (sure|convinced)/i, /volumes?/i, /justify/i
/(roi|return)/i, /maybe (later|down the line)/i
/not (now|yet)/i, /apprehensi/i
```

#### TOJO_PROBE1_PARK `[TOJO]`

> Fair concern. Parking it as an option, not a recommendation. The Agent will pull leakage volumes and run a capex-vs-return simulation before we revisit. Carry on.

---

### MEHTA_TURN_B `[MEHTA]` — continues with more topics

> **Example:** *"Other things on my mind — LOS averages 5 days, should be 3.5 to 4. Some of it I think is diagnostic leakage. Marketing keeps pushing for more OPD footfalls but OPD is already maxed. And I suspect we're overspending on manpower, especially agency nursing — but I'm worried cutting it will hurt efficiency."*

**Topics detected:** `los`, `diagnostic_leakage` (already covered → skip), `marketing`, `manpower`

#### TOJO_TURN_B `[TOJO]` — ack + Probe 2

> Logged:
> – LOS ~5 days vs ~4 target
> – Marketing pressure on an already-full OPD
> – Manpower / agency nursing flagged for review
>
> On LOS — **who sets the ICU admission and step-down protocols at Sunrise? And what's your nurse-to-bed ratio in ICU right now?**
>
> *(ICU LOS and delayed step-downs usually drive overall LOS more than ward stays.)*

---

### Probe 2 — ICU protocol

#### MEHTA_PROBE2_RESPONSE `[MEHTA]`

> **Example:** *"Intensivist on duty calls it. We have a written protocol but it's mostly his judgment. Nurse ratio is 1:2 in ICU."*

**Triggers:**
```
/intensivist/i, /protocol/i, /judg(e)?ment/i
/\b1:2\b/i, /1 to 2/i, /one is to two/i
/\bratio\b/i, /hospitalist/i
```

#### TOJO_PROBE2_FOLLOWUP `[TOJO]` — ack + Probe 3

> Noted — intensivist-led, 1:2 ratio. We'll cross-check protocol adherence against actual ICU LOS once data is in.
>
> One more on LOS — **what time do your consultants do morning in-patient rounds? And are they generally open to a routine change if data showed it was worth it?**
>
> *(Round timing sets the discharge clock for the whole day. Often invisible.)*

---

### Probe 3 — Rounds

#### MEHTA_PROBE3_RESPONSE `[MEHTA]`

> **Example:** *"Most start around 10:30. Some are open, some are not. Why are you asking?"*

**Triggers:**
```
/10:30/i, /10 ?am/i, /10 ?o'?clock/i
/morning/i, /rounds?/i
/open/i, /not (open|all)/i, /mix(ed)?/i
/some are/i, /why/i
```

#### TOJO_PROBE3_FOLLOWUP `[TOJO]`

> 10:30 rounds, mixed openness — noted. Not drawing a conclusion here. As I mentioned, all of this becomes clearer once the **Virevo CEO Agent** and I work through the datasets. I'll come back to round timing with numbers, not opinions.
>
> Anything else on your mind, or shall I read back what I have?

---

### T_WRAP `[MEHTA]`

> **Example:** *"I think that covers it. You have enough to start."*

**Triggers:**
```
/that.{0,15}(covers|is it|are the main)/i
/you have enough/i
/enough to start/i
/^that'?s (it|all)/i
/^no(thing)? (else|more)/i
/read.{0,5}back/i, /summary/i, /summari[sz]e/i
```

---

### T_STEP1_SUMMARY `[TOJO]`

> Right. Let me read back what I have so we're aligned.
>
> **Hospital snapshot:**
> 150 beds · 12 ICU + 6 NICU · 3 OTs (2 gen, 1 ortho) · Ortho, gen surg, gynae, IM + visiting cardio · Nashik · ₹73Cr revenue · 8% EBITDA · ~80% occupancy
>
> **Problems you've named:**
> 1. Revenue stagnant despite high occupancy
> 2. EBITDA stuck at 8% — priority unclear
> 3. LOS ~5 days vs ~4 target
> 4. Diagnostic leakage (your theory: scans going out)
> 5. Marketing pressure on an already-full OPD
> 6. Manpower / agency nursing possibly over-spent
>
> **Items I added to scope:**
> – Second MRI: parked, will revisit with leakage data + capex simulation
> – ICU protocols: intensivist-led, 1:2 nurse ratio — needs adherence audit against LOS
> – Consultant rounds: 10:30 start, mixed openness — flagged for timing analysis
>
> Enough to start. I'll compile the **data access request** and send it through — what we need from HIS, Meddoc billing, GreytHR, Tally, and the pharmacy and biomedical logs. You'll sign off the read permissions and we begin.
>
> Ready for **Step 2**?

---

### T_STEP2_CONSENT `[MEHTA]`

> **Example:** *"Yes, go ahead."*

**Triggers:**
```
/^\s*(yes|sure|ok(ay)?|go ahead|continue|next|proceed)/i
/step ?2/i
/move on/i
/let'?s (continue|go|move|proceed)/i
```

---

## Phase 2 — Step 2: Model Validation & Data Monitoring

### T_STEP2_INTRO `[TOJO]`

> **Step 2 — Model Validation and Data Monitoring.**
>
> Two streams running in parallel:
>
> **1. Retrospective build.** The Agent ingests the last 12-18 months of operational data from HIS, billing, HR, pharmacy, accounts, and biomedical logs. This becomes the historical baseline. Roughly 4-6 weeks.
>
> **2. Live monitoring.** Once retrospective is loaded, the Agent tracks live data for 4-8 weeks. This is how we validate the model against current operations — and surface anomalies the historical data alone won't show.
>
> Total elapsed: **roughly 1-2 months retrospective build + 1-2 months live monitoring**, with overlap.
>
> I won't go silent. You'll get periodic updates from me — coverage levels, early signals, anomalies worth flagging, anything that changes how we're thinking about the six problems you named.
>
> Once you authorise the data access request I'm sending through today, the Agent starts. First update from me in about two weeks.

---

### T_WAITING_WEEK2 `[MEHTA]` — acknowledgment

> **Example:** *"Sounds good. Will wait."*

**Triggers:**
```
/^\s*(ok(ay)?|sure|sounds good|acknowledg|got it|alright|will wait|fine|noted)/i
```

> **Note for implementation:** in the live build, the Week 2 update would fire on a real time delay or scheduler. For the demo, it can fire on the user's acknowledgment, with a UI delay (e.g., 1.5s typing indicator + "📅 2 weeks later" divider).

---

### T_WEEK2_UPDATE `[TOJO]`

> **Update — Week 2 of Step 2**
>
> Status:
>
> – **HIS (eHospital v4.2):** connected, retrospective ingestion at ~68% coverage. On track.
> – **Meddoc billing:** connected, ~52% coverage. Some line-item gaps in OT charge codes — Agent is reconciling.
> – **GreytHR:** connected, full coverage.
> – **Tally:** GL bridge built, monthly pulls running clean.
> – **Pharmacy inventory:** records sparse pre-October. Agent rebuilding par levels from dispensing logs.
> – **Biomedical maintenance logs:** partial. Will need a manual export for July-November.
>
> Early signal worth flagging — not a finding, just a signal: **OT cancellation rate looks meaningfully above benchmark.** Investigating. More in the next update.

---

### T_WAITING_WEEK5 `[MEHTA]` — acknowledgment

> **Example:** *"Noted. Keep going."*

**Triggers:**
```
/^\s*(noted|ok(ay)?|keep going|continue|acknowledg|got it|alright)/i
```

---

### T_WEEK5_UPDATE `[TOJO]`

> **Update — Week 5 of Step 2**
>
> Retrospective build effectively complete. Live monitoring is now running with three weeks of clean overlap against the historical baseline.
>
> Three observations so far — all preliminary, none of them findings yet:
>
> 1. **OT cancellations cluster on specific weekdays.** The pattern is too clean to be random. Agent is correlating against equipment maintenance schedules and pre-op clearance timings.
>
> 2. **ICU LOS materially above the comparable benchmark.** A non-trivial share of ICU-days appear to be patients clinically ready for step-down 12-36 hours earlier. Probing whether this is protocol, bed availability, or both.
>
> 3. **Insurance receivables ageing heavier than expected** for your payer mix. Separating submission lag from query-response lag to locate the friction.
>
> None of these are conclusions. They're signals the Agent is following. By the end of Step 2 I'll have a structured picture — what's confirmed, what's a probable cause, what the root cause looks like underneath.
>
> That's the **Step 3** conversation.

---

# SECTION 2 — JS DATA STRUCTURE

```javascript
// =============================================================================
// VIREVO — TOJO ↔ DR. MEHTA SCRIPTED CHAT ENGINE
// Step 1 (Project Brief) → Step 2 (Data Monitoring, weeks 2 & 5)
// =============================================================================

const conversationFlow = {

  // -------------------------------------------------------------------------
  // PHASE 0 — ONBOARDING
  // -------------------------------------------------------------------------
  T0_OPENING: {
    actor: 'mehta',
    triggers: [
      /how (do|should) (i|we) (start|begin|proceed|do this)/i,
      /where do (i|we) (start|begin)/i,
      /what (do|should) i do (now|first|next)/i,
      /how does this work/i,
      /ready to start/i,
      /^\s*(start|begin|hi|hello|hey)\s*$/i,
    ],
    next: 'T1_TOJO_INTRO'
  },

  T1_TOJO_INTRO: {
    actor: 'tojo',
    response: `Hi Dr. Mehta. I'm **Tojo** — your point of contact through this engagement. Working with me is the **Virevo CEO Agent**: the analytical engine that ingests your hospital's data, builds a mathematical model of how everything fits together, and runs the simulations we'll use to make decisions. I handle the conversation; the Agent handles the maths.

Quick choice before we begin: do you want me to walk you through the **whole process end-to-end** first, or take it **one step at a time** and explain each step as we get there?`,
    next: 'T2_WALKTHROUGH_CHOICE'
  },

  T2_WALKTHROUGH_CHOICE: {
    actor: 'mehta',
    triggers: [
      /step by step/i,
      /one (step )?at a time/i,
      /one by one/i,
      /as we go/i,
      /walk me through/i,
      /take me through/i,
      /each step/i,
      /the (latter|second)/i,
    ],
    next: 'T3_STEP1_INTRO'
  },

  T3_STEP1_INTRO: {
    actor: 'tojo',
    response: `Good. We'll start with **Step 1 — Project Brief and Problem Statement.**

This part is a conversation. I need to understand your hospital — what it does, how it runs, what's working, what isn't. You can **type or dictate**.

If you're dictating: start the first time with **"Hey Tojo."** Do the same after any long pause. Otherwise, just keep going.

Share whatever feels relevant — size, specialties, the problems on your mind, the causes you've already identified, anything you think I should know. I'll interject only when I need a clarification. Once I have a clear picture, I'll work out which datasets the Agent and I need access to.

Take your time. Go ahead.`,
    next: 'STEP1_LISTENER'
  },

  // -------------------------------------------------------------------------
  // PHASE 1 — STEP 1: MULTI-TOPIC LISTENER
  // -------------------------------------------------------------------------
  STEP1_LISTENER: {
    actor: 'mehta',
    mode: 'multi_topic',

    topics: {
      beds: {
        patterns: [
          /150 beds?/i, /\b12 icu\b/i, /\b6 nicu\b/i, /\b3 ot/i,
          /operating theatres?/i, /\bicu beds?\b/i, /\bnicu\b/i,
          /(general|semi-private|private) (beds?|ward)/i
        ],
        ack: '– 150 beds, 12 ICU + 6 NICU, 3 OTs (2 gen, 1 ortho)'
      },
      specialties: {
        patterns: [
          /ortho/i, /gen(eral)? surg/i, /gyn(a|ae)/i,
          /internal med/i, /cardio/i, /visiting/i, /multispecialty/i
        ],
        ack: '– Ortho, gen surg, gynae, IM + visiting cardio'
      },
      location: {
        patterns: [ /nashik/i, /maharashtra/i, /tier[- ]?2/i ],
        ack: '– Nashik, Tier-2'
      },
      revenue_stagnation: {
        patterns: [
          /revenue.{0,30}(flat|stagnant|stuck|not grow|not improving)/i,
          /73 ?cr/i, /73 ?crore/i,
          /high occupan|occupan.{0,20}high/i,
          /(80|81|82|83|84|85)% ?occupan/i
        ],
        ack: '– ~80% occupancy, ₹73Cr revenue, stagnant 2 years'
      },
      ebitda: {
        patterns: [
          /ebitda/i, /\b8 ?%/i,
          /everything (looks|seems) (equally )?important/i,
          /don'?t know (where|which) to focus/i,
          /which (lever|area|aspect) to (pull|focus|prioritise|prioritize)/i
        ],
        ack: '– EBITDA stuck at 8%, priority unclear'
      },
      los: {
        patterns: [
          /\blos\b/i, /length of stay/i, /(5|five) days?/i,
          /(higher|longer) than (benchmark|target|expected)/i,
          /staying (too )?long/i
        ],
        ack: '– LOS ~5 days vs ~4 target'
      },
      diagnostic_leakage: {
        patterns: [
          /diagnostic leakage/i, /leak(age|ing)/i,
          /scans? going (out|outside)/i, /outside scans?/i
        ],
        ack: '– Diagnostic leakage (your hypothesis: scans going out)'
      },
      marketing: {
        patterns: [
          /marketing/i, /footfall/i,
          /opd.{0,20}(full|maxed|capacity)/i,
          /more patients/i, /grow (the )?opd/i
        ],
        ack: '– Marketing pressure on an already-full OPD'
      },
      manpower: {
        patterns: [
          /manpower/i, /staff(ing| costs?)/i,
          /agency nurs/i, /nurs(e|ing) costs?/i,
          /rationali[sz]e/i, /efficiency/i,
          /(cut|reduce|trim) (staff|nursing|costs?)/i
        ],
        ack: '– Manpower / agency nursing flagged for review'
      }
    },

    compose_ack: (matched) =>
      `Logged:\n${matched.map(t => t.ack).join('\n')}`
  },

  // -------------------------------------------------------------------------
  // PROBES — fired in fixed order, one after each batch of Mehta disclosure
  // -------------------------------------------------------------------------
  probes: [
    {
      id: 'mri',
      question:
`Before you go further — **how many MRI units do you have, and are they in-house or outsourced?**

*(Diagnostic capacity is one of the quietest LOS levers — worth pinning early.)*`,

      stage_one_triggers: [
        /\b1 mri\b/i, /one mri/i, /single mri/i,
        /mri.{0,15}outsourced/i, /outsourced.{0,15}mri/i, /vendor/i
      ],
      stage_one_followup:
`Outsourced single unit, noted. Worth flagging now: diagnostic leakage in most units isn't about referrals going elsewhere for kickbacks — it's about **slot availability**. Patients who can't get a scan in 4 hours get sent out, and the case clock keeps running. Have you ever evaluated a second in-house MRI?`,

      stage_two_triggers: [
        /capex/i, /\bcost\b/i, /steep/i, /expensive/i,
        /not (sure|convinced)/i, /volumes?/i, /justify/i,
        /(roi|return)/i, /maybe (later|down the line)/i,
        /not (now|yet)/i, /apprehensi/i
      ],
      stage_two_response:
`Fair concern. Parking it as an option, not a recommendation. The Agent will pull leakage volumes and run a capex-vs-return simulation before we revisit. Carry on.`
    },

    {
      id: 'icu_protocol',
      question:
`On LOS — **who sets the ICU admission and step-down protocols at Sunrise? And what's your nurse-to-bed ratio in ICU right now?**

*(ICU LOS and delayed step-downs usually drive overall LOS more than ward stays.)*`,

      response_triggers: [
        /intensivist/i, /protocol/i, /judg(e)?ment/i,
        /\b1:2\b/i, /1 to 2/i, /one is to two/i,
        /\bratio\b/i, /hospitalist/i
      ],
      followup:
`Noted — intensivist-led, 1:2 ratio. We'll cross-check protocol adherence against actual ICU LOS once data is in.`
    },

    {
      id: 'rounds',
      question:
`One more on LOS — **what time do your consultants do morning in-patient rounds? And are they generally open to a routine change if data showed it was worth it?**

*(Round timing sets the discharge clock for the whole day. Often invisible.)*`,

      response_triggers: [
        /10:30/i, /10 ?am/i, /10 ?o'?clock/i,
        /morning/i, /rounds?/i,
        /open/i, /not (open|all)/i, /mix(ed)?/i,
        /some are/i, /why/i
      ],
      followup:
`10:30 rounds, mixed openness — noted. Not drawing a conclusion here. As I mentioned, all of this becomes clearer once the **Virevo CEO Agent** and I work through the datasets. I'll come back to round timing with numbers, not opinions.

Anything else on your mind, or shall I read back what I have?`
    }
  ],

  // -------------------------------------------------------------------------
  // STEP 1 WRAP + SUMMARY
  // -------------------------------------------------------------------------
  T_WRAP: {
    actor: 'mehta',
    triggers: [
      /that.{0,15}(covers|is it|are the main)/i,
      /you have enough/i,
      /enough to start/i,
      /^that'?s (it|all)/i,
      /^no(thing)? (else|more)/i,
      /read.{0,5}back/i, /summary/i, /summari[sz]e/i
    ],
    next: 'T_STEP1_SUMMARY'
  },

  T_STEP1_SUMMARY: {
    actor: 'tojo',
    response:
`Right. Let me read back what I have so we're aligned.

**Hospital snapshot:**
150 beds · 12 ICU + 6 NICU · 3 OTs (2 gen, 1 ortho) · Ortho, gen surg, gynae, IM + visiting cardio · Nashik · ₹73Cr revenue · 8% EBITDA · ~80% occupancy

**Problems you've named:**
1. Revenue stagnant despite high occupancy
2. EBITDA stuck at 8% — priority unclear
3. LOS ~5 days vs ~4 target
4. Diagnostic leakage (your theory: scans going out)
5. Marketing pressure on an already-full OPD
6. Manpower / agency nursing possibly over-spent

**Items I added to scope:**
– Second MRI: parked, will revisit with leakage data + capex simulation
– ICU protocols: intensivist-led, 1:2 nurse ratio — needs adherence audit against LOS
– Consultant rounds: 10:30 start, mixed openness — flagged for timing analysis

Enough to start. I'll compile the **data access request** and send it through — what we need from HIS, Meddoc billing, GreytHR, Tally, and the pharmacy and biomedical logs. You'll sign off the read permissions and we begin.

Ready for **Step 2**?`,
    next: 'T_STEP2_CONSENT'
  },

  // -------------------------------------------------------------------------
  // PHASE 2 — STEP 2: DATA MONITORING
  // -------------------------------------------------------------------------
  T_STEP2_CONSENT: {
    actor: 'mehta',
    triggers: [
      /^\s*(yes|sure|ok(ay)?|go ahead|continue|next|proceed)/i,
      /step ?2/i, /move on/i,
      /let'?s (continue|go|move|proceed)/i
    ],
    next: 'T_STEP2_INTRO'
  },

  T_STEP2_INTRO: {
    actor: 'tojo',
    response:
`**Step 2 — Model Validation and Data Monitoring.**

Two streams running in parallel:

**1. Retrospective build.** The Agent ingests the last 12-18 months of operational data from HIS, billing, HR, pharmacy, accounts, and biomedical logs. This becomes the historical baseline. Roughly 4-6 weeks.

**2. Live monitoring.** Once retrospective is loaded, the Agent tracks live data for 4-8 weeks. This is how we validate the model against current operations — and surface anomalies the historical data alone won't show.

Total elapsed: **roughly 1-2 months retrospective build + 1-2 months live monitoring**, with overlap.

I won't go silent. You'll get periodic updates from me — coverage levels, early signals, anomalies worth flagging, anything that changes how we're thinking about the six problems you named.

Once you authorise the data access request I'm sending through today, the Agent starts. First update from me in about two weeks.`,
    next: 'T_WAITING_WEEK2'
  },

  T_WAITING_WEEK2: {
    actor: 'mehta',
    triggers: [
      /^\s*(ok(ay)?|sure|sounds good|acknowledg|got it|alright|will wait|fine|noted)/i
    ],
    next: 'T_WEEK2_UPDATE',
    // Optional: insert a UI delay + "📅 2 weeks later" divider before firing next
    ui_delay_ms: 1500,
    ui_divider: '📅 2 weeks later'
  },

  T_WEEK2_UPDATE: {
    actor: 'tojo',
    response:
`**Update — Week 2 of Step 2**

Status:

– **HIS (eHospital v4.2):** connected, retrospective ingestion at ~68% coverage. On track.
– **Meddoc billing:** connected, ~52% coverage. Some line-item gaps in OT charge codes — Agent is reconciling.
– **GreytHR:** connected, full coverage.
– **Tally:** GL bridge built, monthly pulls running clean.
– **Pharmacy inventory:** records sparse pre-October. Agent rebuilding par levels from dispensing logs.
– **Biomedical maintenance logs:** partial. Will need a manual export for July-November.

Early signal worth flagging — not a finding, just a signal: **OT cancellation rate looks meaningfully above benchmark.** Investigating. More in the next update.`,
    next: 'T_WAITING_WEEK5'
  },

  T_WAITING_WEEK5: {
    actor: 'mehta',
    triggers: [
      /^\s*(noted|ok(ay)?|keep going|continue|acknowledg|got it|alright)/i
    ],
    next: 'T_WEEK5_UPDATE',
    ui_delay_ms: 1500,
    ui_divider: '📅 3 weeks later'
  },

  T_WEEK5_UPDATE: {
    actor: 'tojo',
    response:
`**Update — Week 5 of Step 2**

Retrospective build effectively complete. Live monitoring is now running with three weeks of clean overlap against the historical baseline.

Three observations so far — all preliminary, none of them findings yet:

1. **OT cancellations cluster on specific weekdays.** The pattern is too clean to be random. Agent is correlating against equipment maintenance schedules and pre-op clearance timings.

2. **ICU LOS materially above the comparable benchmark.** A non-trivial share of ICU-days appear to be patients clinically ready for step-down 12-36 hours earlier. Probing whether this is protocol, bed availability, or both.

3. **Insurance receivables ageing heavier than expected** for your payer mix. Separating submission lag from query-response lag to locate the friction.

None of these are conclusions. They're signals the Agent is following. By the end of Step 2 I'll have a structured picture — what's confirmed, what's a probable cause, what the root cause looks like underneath.

That's the **Step 3** conversation.`,
    next: null
  }
};

// =============================================================================
// DICTATION WAKE-PHRASE LOGIC
// =============================================================================
const DICTATION = {
  WAKE_PHRASES: [/^hey tojo[,.\s]*/i, /^ok tojo[,.\s]*/i, /^tojo[,.\s]+/i],
  TIMEOUT_MS: 60_000,

  isActive: false,
  lastActivityAt: null,

  needsWake() {
    if (!this.isActive) return true;
    if (!this.lastActivityAt) return true;
    return (Date.now() - this.lastActivityAt) > this.TIMEOUT_MS;
  },

  consumeWakeIfPresent(text) {
    for (const p of this.WAKE_PHRASES) {
      if (p.test(text)) {
        this.isActive = true;
        this.lastActivityAt = Date.now();
        return text.replace(p, '').trim();
      }
    }
    return null;
  },

  touch() { this.lastActivityAt = Date.now(); }
};

// =============================================================================
// STATE MACHINE / ROUTER
// =============================================================================
const tojoEngine = {
  state: 'T0_OPENING',
  step1: {
    coveredTopics: new Set(),
    firedProbes: new Set(),
    activeProbe: null,
    mriStage: null   // null | 'asked' | 'pushback' | 'done'
  },

  handleUserMessage(rawText, { isVoice = false } = {}) {
    let text = rawText;

    // Voice path: enforce wake phrase when required
    if (isVoice) {
      if (DICTATION.needsWake()) {
        const stripped = DICTATION.consumeWakeIfPresent(text);
        if (stripped === null) {
          return { say: `Say "Hey Tojo" to start dictation, or just type instead.` };
        }
        text = stripped;
      } else {
        DICTATION.touch();
      }
    }

    // Step 1 listener phase has special multi-topic / probe logic
    if (this.state === 'STEP1_LISTENER') {
      return this._handleStep1(text);
    }

    // Linear states — match triggers, advance, return scripted response
    const node = conversationFlow[this.state];
    if (!node || node.actor !== 'mehta' || !node.triggers) return this._fallback();

    if (node.triggers.some(t => t.test(text))) {
      this.state = node.next;
      const nextNode = conversationFlow[this.state];
      return {
        say: nextNode.response,
        delayMs: node.ui_delay_ms,
        divider: node.ui_divider,
        autoAdvanceTo: (this.state.startsWith('T_WAITING_')) ? null : null
      };
    }

    return this._fallback();
  },

  _handleStep1(text) {
    // If we're in the middle of a probe Q&A, route there first
    if (this.step1.activeProbe) {
      return this._resolveProbe(text);
    }

    // Wrap signal short-circuits the listener
    if (conversationFlow.T_WRAP.triggers.some(t => t.test(text))) {
      this.state = 'T_STEP1_SUMMARY';
      return { say: conversationFlow.T_STEP1_SUMMARY.response };
    }

    // Detect new topics
    const topics = conversationFlow.STEP1_LISTENER.topics;
    const matched = [];
    for (const [key, topic] of Object.entries(topics)) {
      if (this.step1.coveredTopics.has(key)) continue;
      if (topic.patterns.some(p => p.test(text))) {
        matched.push(topic);
        this.step1.coveredTopics.add(key);
      }
    }

    let response = '';
    if (matched.length) {
      response = conversationFlow.STEP1_LISTENER.compose_ack(matched);
    }

    // Fire the next unfired probe
    const probe = conversationFlow.probes.find(p => !this.step1.firedProbes.has(p.id));
    if (probe) {
      this.step1.firedProbes.add(probe.id);
      this.step1.activeProbe = probe.id;
      response += (response ? '\n\n' : '') + probe.question;
    } else if (matched.length) {
      response += `\n\nAnything else, or shall I read back what I have?`;
    } else {
      response = `Go on — I'm listening. Or say "that's it" when you're done.`;
    }

    return { say: response };
  },

  _resolveProbe(text) {
    const probe = conversationFlow.probes.find(p => p.id === this.step1.activeProbe);

    // MRI is a 2-stage probe
    if (probe.id === 'mri') {
      if (this.step1.mriStage === null || this.step1.mriStage === 'asked') {
        this.step1.mriStage = 'pushback';
        return { say: probe.stage_one_followup };
      }
      if (this.step1.mriStage === 'pushback') {
        this.step1.mriStage = 'done';
        this.step1.activeProbe = null;
        return { say: probe.stage_two_response };
      }
    }

    // Single-stage probes
    this.step1.activeProbe = null;
    return { say: probe.followup };
  },

  _fallback() {
    return { say: `Sorry — I didn't catch that. Could you rephrase?` };
  }
};

// =============================================================================
// USAGE
// =============================================================================
// const reply = tojoEngine.handleUserMessage(userText, { isVoice: false });
// renderTojoBubble(reply.say);
// if (reply.divider) renderDivider(reply.divider);
// if (reply.delayMs) await sleep(reply.delayMs);
```

---

# IMPLEMENTATION NOTES FOR DEV

1. **Wake-phrase UX.** The voice path enforces "Hey Tojo" only after `TIMEOUT_MS` of inactivity. While the user is actively dictating, no wake phrase is needed for subsequent utterances.

2. **Probe ordering.** Probes fire in fixed order: `mri → icu_protocol → rounds`. They don't fire all at once — one per Mehta batch. If Mehta covers multiple topics in a single message, Tojo still asks only one probe in response.

3. **The "everything will be clearer once the Agent runs the data" line.** Currently used in the rounds-probe followup. Sprinkle it in 1–2 more places if the conversation runs longer than the script anticipates.

4. **Demo mode for Week 2 / Week 5 updates.** In a real deployment these are scheduled triggers. For the demo, fire them on Mehta's acknowledgment with a UI delay + a `📅 2 weeks later` / `📅 3 weeks later` divider so it visually reads as time-skipping.

5. **Fallback.** Any user input that doesn't match a trigger in the current state returns the gentle `"Sorry — I didn't catch that. Could you rephrase?"` line. Keep this short; don't over-explain.

6. **Extending.** New probes go into the `probes` array. New topics go into `STEP1_LISTENER.topics`. The state machine doesn't care about counts.
