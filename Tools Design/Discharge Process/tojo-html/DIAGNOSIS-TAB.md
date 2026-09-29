# Diagnosis tab — closed 26 Sep 2026

## What was built
- **Look.** Version 3, route map on sage. The chat panel is forest green, and the canvas is always the lighter half.
- **Shades.** Sage and mist, applied by the generator from the turn number in sets of three. Nothing stored carries a colour.
- **Language.** Plain English only, enforced by the validator's word list.
- **Screens.** One screen on desktop (824px of canvas at 1440×900), and about two phone screens on mobile. Mobile layouts reflow and never shrink.

## Approved templates (23)

| Category | Templates |
|---|---|
| Frame | heading, handnote |
| Process | route-map, chain, time-window, converge, bands, shared-flow |
| Comparison | two-flow, compare-table, threshold-gauges, balance, narrow-claim |
| Numbers | stat-strip, calculator, hour-load, was-now, scorecard |
| Progress | progress-trail, zoom-trail, phases |
| Items | cards, role-cards |

Still draft (usable, flagged in builds): agenda-grid, fill-blank, fork.

## Approved worked turns (10)
The conversation playbook for Discharge Process, turns dp-01 to dp-10: walking the chain, pricing the wait, the diagnosis, the five-part fix, each part in depth, and the plan. dp-11 and dp-12 (trial times, blank and filled) are built and pass every test, but were not approved.

## Carries over to Solutions, Automations and Processes
- **Rules:** 05 (answering method), 06 (response), 07 (block design) and the standing feedback F1–F10.
- **References:** `references/discharge-process.md` and `references/discharge-process-conversation-playbook.md`.
- **The generator:** validator, renderer, shades, plain-English check, web service and tests.
- **Blocks:** any block can be reused. A new tab adds blocks through the same review loop (07 §7): registry entry, renderer, both layouts, samples, gallery, approval.
- **Design canvas:** approved turns go to the design canvas with `dc_export.py`, and the template library with `dc_export.py library`.
