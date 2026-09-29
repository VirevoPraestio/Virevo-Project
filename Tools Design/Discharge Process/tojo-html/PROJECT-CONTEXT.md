# Tojo HTML — project context (read this first in a new chat)

Updated 28 Sep 2026.

## What this project is
Tojo is Virevo's hospital-operations consulting agent. Each answer has two halves. The **chat panel** holds the text, Tojo's Note, the @points, one structured question and three prompts. The **canvas** is an interactive HTML page built from approved blocks.

Claude writes only a JSON response spec. The offline generator (`diagnosis-html-generator/diagnosis_html.py`) validates the spec against the block registry and renders the canvas. No model writes HTML.

The app has five tabs in its rail: **Resources, Diagnosis, Solutions, Automations, Processes**. Each tool is one hospital problem, for example Discharge Process. Each tool's conversation runs across these tabs.

## Where things are

If the files were added to project knowledge one by one, the folder paths are lost. This table maps each name back to its place in the repository.

| File | Path in the repository | What it is |
|---|---|---|
| PROJECT-CONTEXT.md | `/` | This primer |
| LANDING-PAGES.md | `/` | Landing-page rules and samples for every tab |
| landing_common.py, build_landing.py, measure.py | `landing-common/` | Shared landing parts, build, QA |
| landing.py (×4) | each `<tab>-html-generator/` | That tab's landing samples |
| README.md | `/` | Pipeline, file map, quick start, backend wiring, review loop |
| DIAGNOSIS-TAB.md | `/` | Handover: what the Diagnosis tab closed with, and what carries over |
| CHANGELOG.md | `/` | Every change, newest first |
| 05-universal-answering-method.md | `rules/` | The general, industry-free answering method. 06 and 07 no longer depend on it. |
| 06-html-response-rules.md | `rules/` | Response rules, complete on their own: method, evidence, turn types, chat parts, block choice, budget, landing pages, feedback F1–F11 |
| 07-html-block-design-rules.md | `rules/` | Design rules, complete on their own: every tab's look, type, landing templates, both layouts, visual grammar, interaction, build discipline, adding a block |
| discharge-process.md | `references/` | Discharge domain reference: §7.2 dependencies, §7.3 money, §7.4 solution method, §8 KPIs |
| discharge-process-conversation-playbook.md | `references/` | The worked Discharge conversation arc |
| registry.json | `blocks/` | The block database: 26 blocks with slots, word limits, status, feedback, `plain_english` list, `tones` |
| samples.json | `blocks/` | Sample slot values for the gallery |
| tojo-response.schema.json | `schema/` | The JSON contract |
| tojo-api-system-prompt.md | `prompts/` | Output-contract template, filled by `diagnosis_html.py prompt` |
| system-section.md | `out/` | The assembled prompt section: rules 06 plus the live catalogue |
| diagnosis_html.py, preview.py, server.py, api_example.py, dc_export.py | `diagnosis-html-generator/` | Generator, preview shells, HTTP service, API loop, design-canvas export |
| tojo.css, tojo.js | `diagnosis-html-generator/assets/` | Design tokens, both layouts, small runtime |
| check_turns.py, calibrate.py | `tests/` | Browser test, height calibration (Playwright) |
| turn-01 … turn-12 *.json | `examples/` | Worked Diagnosis-tab turns dp-01 to dp-12 |
| turn-03b … turn-06 *.A-deep/B-mist.json | `examples/archive/` | Samples not chosen |

The fonts (`diagnosis-html-generator/assets/fonts/`) and the built HTML in `out/` are not text. They live only in the zip. The HTML can be rebuilt from the examples with the generator. Without the font files, set `TOJO_FONTS=google`.

## State of play

**Diagnosis tab: closed 26 Sep 2026.**
- 23 approved blocks. agenda-grid, fill-blank and fork are still draft.
- Turns dp-01 to dp-10 approved. dp-11 and dp-12 are built but not approved.
- House style is Version 3 (route map on sage). Shades change every third turn: sage for turns 1–3, mist for turns 4–6, and so on.
- Budgets: 824px on desktop, about 1,500px on mobile.
- Plain English is enforced by the validator.

**Tab landing pages approved 28 Sep:** Diagnosis C, Solutions B, Automations B, Processes A (see LANDING-PAGES.md). **Solutions tab: generator built, 11 blocks (8 draft), ten example turns (so-00 to so-09) awaiting review.** The Solutions tab is for discussing and iterating every solution and everything each one depends on. Its canvas designs differ from Diagnosis, and the chat panel stays exactly as it is.

**Carries over to every new tab:**
- Rules 06 and 07 (v2, complete on their own), and feedback F1–F11.
- The generator, and any existing block.
- New blocks go through the 07 §7 review loop.

## Rule files
06 (response rules) and 07 (block and template design rules) are **complete on their own** as of v2 (28 Sep 2026). They fold in everything they used to borrow from 01, 02, 04, 05 and the playbook, and they cover the per-tab looks and the landing pages. 05 stays in `rules/` as the general, industry-free method it was written as, but nothing in 06 or 07 depends on it. `00`–`04`, `bed-management.md` and `opd-diagnostic-leakage.md` are not needed for the Discharge tool.

## Working agreements
- Change the generator and registry, never the rendered HTML.
- Every build validates all example turns. Approvals are logged with `diagnosis_html.py feedback BLOCK approved "note"`.
- Approved turns go to both the gallery and the design canvas (`dc_export.py`).
