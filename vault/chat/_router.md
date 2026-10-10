---
id: _router
title: Router
description: Chooses which hospital-operations topic a question belongs to
keywords: [router]
kind: router
version: 2026-09-09
source_author: authored during conversion from Avishek's department files - pending AB sign-off
---

## Overview

Routing across three hospital-operations topics: discharge process, bed management, and OPD-to-diagnostics conversion (diagnostic leakage). Every topic is an operational process inside a hospital, addressed to owners, CEOs and COOs rather than clinicians. Nothing here is clinical. The router chooses a topic and the knowledge sections a question needs; it never answers.

The three topics are not equally distinct. Discharge and bed management overlap heavily because they share the same two headline measures - average length of stay and bed occupancy - so most routing mistakes will be between those two. OPD-to-diagnostics has its own vocabulary and rarely collides with either.

## How to route

Discharge and bed management are separated by **which lever the question is reaching for**, not by which measure it mentions. Both topics talk about ALOS and occupancy, so those words decide nothing on their own.

Choose **discharge-process** when the question is about getting a patient who is already clinically ready out of the bed: the discharge decision reaching the ward, the summary being written, billing and insurance or TPA clearance, pharmacy and take-home medication, porter and housekeeping turnaround, discharge timing across the day, or discharge against medical advice. "Why is our ALOS high", "discharges all happen at 6pm", "patients wait hours for the final bill" are all discharge questions - discharge is the lever even though ALOS is the measure.

Choose **bed-management** when the question is about deciding and balancing where patients go: bed inventory and mapping, allocation between wards, ICU admission and step-down flow, admissions waiting for a bed, ward or bed-type mix, isolation and cohorting, surge and escalation during a capacity crunch, and prediction of beds becoming free. "Occupancy is 95% and we are still turning admissions away", "ICU patients wait two days for a step-down bed", "how many beds should be in which ward" are bed-management questions.

When a question genuinely spans both - "we want to raise occupancy without adding beds" - pick the topic that owns the **action** being asked about and offer the other as one of the follow-up questions. If the question is about releasing beds faster, that is discharge. If it is about using the beds you already release better, that is bed management.

Choose **opd-diagnostic-leakage** when the question is about investigations prescribed during an outpatient consultation not being completed at the hospital: conversion rate from OPD to diagnostics, tests going to an outside lab or imaging centre, patients skipping tests, report turnaround, diagnostics scheduling and capacity, or walk-in versus appointment flow for lab and radiology. The words leakage, conversion, lab, radiology, imaging, pathology and "prescribed tests" point here almost unambiguously.

A question about money alone - "how do we improve margin", "where is revenue leaking" - is not enough to route on. Diagnostics leakage is a revenue topic, but so is length of stay. Ask which area they mean rather than guessing, unless the question names a department, a measure or a process step.

## When to attach the shared framework

The three department files each defer to a shared set of cross-department frameworks rather than
restating them: the four-aspect solution construction method, the shared discharge/bed/ALOS/occupancy
consideration set, and the peak-load staffing ratio method. Those live in the shared skill, and
`shared_sections` attaches them alongside the chosen topic.

Attach them when the question asks for something to be **built or sized**, not merely explained:
constructing a solution, working out how many people a function needs, comparing a change against its
cost, or reasoning about occupancy and length of stay together. "What is bed management" needs none of
it. "We are at 95% occupancy — what do we actually do about it" needs solution construction. "How many
discharge executives should we have" needs the staffing method.

Attach at most two. Attaching the whole framework on every question defeats the point of choosing.

## When to say not covered

Say the topic is not covered, rather than routing to the nearest match, when the question is about:

- Anything clinical: diagnosis, treatment, medication, test selection, clinical protocols, or whether a specific patient is fit for anything.
- Departments outside the three above - emergency, operating theatres, pharmacy stock, dietary, biomedical, laundry, housekeeping as a department in its own right.
- Hospital functions that are not operations: HR and payroll, accreditation and NABH or JCI preparation, EMR or HIS selection, construction and expansion, marketing, or medico-legal questions.
- Benchmarks for a named hospital, city or chain, or any request for figures the reference material does not contain.

Routing to the closest topic when none fits produces a confident answer built on material that does not address the question, which is worse than saying it is not covered.

## When to ask the user

Ask one short clarifying question instead of routing when:

- The first message is broad - "we have operational problems", "help us improve efficiency", "our hospital is losing money". Offer the three areas and let them choose.
- The question names a measure both discharge and bed management own - ALOS, occupancy, bed turnover - with no indication of which lever they want. Ask whether they mean releasing beds faster or allocating them better.
- The question could be about diagnostics capacity or about OPD flow itself, and the two would be answered differently.

Ask once, then route on the answer. Do not ask two questions in a row, and do not ask when the question already names a department, a process step or a clearly-owned measure.

## Keyword rules

- discharge -> discharge-process
- "discharge summary" -> discharge-process
- "discharge delay" -> discharge-process
- "discharge tat" -> discharge-process
- alos -> discharge-process
- "length of stay" -> discharge-process
- "final bill" -> discharge-process
- "tpa" -> discharge-process
- "insurance clearance" -> discharge-process
- ama -> discharge-process
- "bed management" -> bed-management
- occupancy -> bed-management
- "bed occupancy" -> bed-management
- "bed turnover" -> bed-management
- "bed allocation" -> bed-management
- "step down" -> bed-management
- icu -> bed-management
- admissions -> bed-management
- "bed blocking" -> bed-management
- census -> bed-management
- "diagnostic leakage" -> opd-diagnostic-leakage
- leakage -> opd-diagnostic-leakage
- opd -> opd-diagnostic-leakage
- "conversion rate" -> opd-diagnostic-leakage
- diagnostics -> opd-diagnostic-leakage
- radiology -> opd-diagnostic-leakage
- pathology -> opd-diagnostic-leakage
- imaging -> opd-diagnostic-leakage
- "prescribed tests" -> opd-diagnostic-leakage
