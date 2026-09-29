# tojo-html — Tojo’s interactive answers, built offline

Tojo’s answers are now **interactive HTML canvases built from a library of approved blocks**, plus a chat panel. Claude writes only JSON. This program turns that JSON into HTML with no model call, so the HTML costs nothing to generate, looks the same every time, and cannot drift from the approved designs.

```
 user message ──► Claude (API) ──► response spec (JSON) ──► diagnosis_html.validate ──► errors? → back to Claude once
                  rules 06                 │                                    │
                  + block catalogue        ├── chat: text, note, points,        └──► diagnosis_html.render ──► canvas HTML
                                           │   question, 3 prompts ──► app chat UI       (desktop + mobile in one file)
                                           └── canvas: blocks + slot values
```

## What is where

| Path | What it is |
|---|---|
| `PROJECT-CONTEXT.md` | **Start here in a new chat.** What the project is, where each file lives, what is done, what is open, and which referenced files are still missing. |
| `LANDING-PAGES.md` | **Tab landing pages:** the rules (midnight refresh, Refresh now, first-visit state, the three buttons), the 12 samples, and how to build them. |
| `solutions-html-generator/solutions_html.py`, `registry.json`, `assets/solutions.css`, `check.py` | The Solutions generator. `python3 solutions_html.py build` validates and draws every spec in `examples/solutions/`; `check.py` measures them in a browser; `prompt` prints the Solutions system-prompt section. |
| `examples/solutions/` | Ten Solutions turns (so-00 to so-09), as the Claude API returns them. |
| `landing-common/landing-elements.json`, `build_library.py` | The 20 landing-page elements and 3 shared parts, and the builder for the full block library (`python3 build_library.py`). |
| `landing-common/` | Parts every tab landing page shares (stamp, three buttons, chat panel, shell, design-canvas export), plus `build_landing.py` and `measure.py`. |
| `solutions-html-generator/`, `automations-html-generator/`, `processes-html-generator/` | Each tab's own generator. Today each holds its landing-page samples (`landing.py`). `diagnosis-html-generator/landing.py` holds the Diagnosis ones. |
| `rules/05-universal-answering-method.md` | The general, industry-free answering method. Kept for reference: 06 and 07 (v2) fold in everything they need from it and stand on their own. |
| `references/discharge-process.md` | **Domain reference for Discharge.** Dependencies (§7.2), sizing (§7.3), the solution parts (§7.4.1–7.4.4) and the 16 measures (§8). Expanders are filled from here (F8, F9). |
| `references/discharge-process-conversation-playbook.md` | **The worked conversation arc** for Discharge: dependency checks, sizing, diagnosis, the five-part fix, deep-dives, pushback, real data, next steps. The Diagnosis-tab turns dp-01 to dp-12 follow it. |
| `rules/06-html-response-rules.md` | **Universal response rules.** Who writes what, turn types, the chat-panel components (note, @points, the 3 prompts), how blocks are chosen, the one-screen budget, evidence on the canvas, and the review loop. |
| `rules/07-html-block-design-rules.md` | **Block design rules.** The Version 3 look, type, two layouts per block, visual grammar, interaction, accessibility, and how to add a block. |
| `DIAGNOSIS-TAB.md` | **Handover:** what the Diagnosis tab has, what is approved, and what carries over to the next tabs. |
| `blocks/registry.json` | **The block database** (26 templates: 23 approved, 3 draft). Each block's purpose, when to use and avoid it, slots with word limits, mobile behaviour, height cost, **status** and **feedback log**. The generator validates against it. |
| `blocks/samples.json` | Sample slot values for every block, used by the gallery. |
| `schema/tojo-response.schema.json` | The JSON contract Claude must return. |
| `prompts/tojo-api-system-prompt.md` | The output-contract section of the API system prompt. `diagnosis_html.py prompt` fills in the live rules and catalogue. |
| `diagnosis-html-generator/diagnosis_html.py` | CLI: `render`, `validate`, `gallery`, `catalog`, `prompt`, `feedback`. Standard library only, Python 3.8+. |
| `diagnosis-html-generator/preview.py` | App-chrome preview shells (desktop and mobile), for reviewing a whole turn. |
| `diagnosis-html-generator/assets/tojo.css`, `tojo.js` | Design tokens, both layouts per block (container queries), and the small runtime: expanders, stop picking, calculators, point highlighting. |
| `diagnosis-html-generator/api_example.py` | A minimal Claude → validate → render loop with one repair retry (tested with a stand-in Claude). |
| `diagnosis-html-generator/server.py` | Optional HTTP service: `POST /render`, `POST /validate`, `GET /health`. |
| `diagnosis-html-generator/dc_export.py` | Exports an approved turn as design-canvas artboards (`SPEC --view desktop|mobile`), or the whole approved template library (`library WIDTH OUT TITLE`). |
| `diagnosis-html-generator/assets/fonts/` | Bebas Neue, Poppins, Caveat (open font licence), embedded so pages work fully offline. `TOJO_FONTS=google` or `none` switches this. |
| `tests/check_turns.py` | Browser test for each turn: plain English, real canvas height against the budget, no sideways scroll, every @Point, prompt, expander, stop and sum. |
| `tests/calibrate.py` | Re-fits the height estimates in the registry from real renders. Run it after changing CSS or adding blocks. |
| `examples/archive/` | Samples you did not pick, kept for reference, not shown. |
| `examples/*.json` | Worked specs: turn dp-01 (walk the chain) and dp-02 (price the wait). |
| `out/` | Built files: `gallery.html` and each example as canvas, desktop and mobile previews. |

## Quick start

```bash
cd diagnosis-html-generator
python3 diagnosis_html.py validate ../examples/turn-02-price-the-wait.json
python3 diagnosis_html.py render   ../examples/turn-02-price-the-wait.json -o ../out/t2.html            # canvas only
python3 diagnosis_html.py render   ../examples/turn-02-price-the-wait.json --view desktop -o ../out/t2d.html
python3 diagnosis_html.py render   ../examples/turn-02-price-the-wait.json --view mobile  -o ../out/t2m.html
python3 diagnosis_html.py gallery  -o ../out/gallery.html                                                 # review every block
python3 diagnosis_html.py blocks time-window phases -o ../out/some.html                                    # review chosen blocks only
python3 diagnosis_html.py prompt   > ../out/system-section.md                                             # paste into the API system prompt
```

## Technologies used

| Part | Technology | Needed in production? |
|---|---|---|
| Generator, validator, command line | **Python 3.8+, standard library only** (json, re, html, ast, argparse, base64, os). No packages to install. | Yes |
| Web service (`server.py`) | Python standard library `http.server` (threaded). Stateless JSON in, JSON out. | Optional: only if your backend is not Python |
| Block database, rules, contract | **JSON**: `registry.json`, `samples.json`, and `tojo-response.schema.json` (JSON Schema 2020-12). | Yes |
| Page styling | **CSS**, one file: custom properties for colours and shades; **container queries** switch the desktop and mobile layouts. | Yes |
| Interaction | **Plain JavaScript**, one small file, no frameworks: stop picking, live sums, point highlighting. Expanders are native HTML `<details>`, so they work with no script. | Yes |
| Fonts | Bebas Neue, Poppins and Caveat as **WOFF2** files (open font licence), embedded by default. `fonts: none` if your app loads them itself. | Yes, or loaded by your app |
| Sums inside calculators | A safe formula reader using Python's `ast` module: numbers, + − × ÷, min, max and round only. It never runs code. | Yes |
| Browser tests and height calibration | **Playwright + Chromium** (`tests/`). | No: development and QA only |
| API loop example | **Anthropic Python SDK** (`api_example.py`). | Only where you call Claude |
| Design-canvas export | `dc_export.py` (standard library). | No: design review only |

Browsers must support container queries: Chrome and Edge 105+, Safari 16+, Firefox 110+ (all from 2022–23).

## Running it on the agent backend

Yes: the generator is built to sit on the backend between Claude and the app.

1. Your agent calls Claude through the API with the system prompt (`diagnosis_html.py prompt`), and receives one JSON spec.
2. The backend hands the spec to the generator:
   - **Python backend:** `errs, warns = diagnosis_html.validate(spec)`, then `html = diagnosis_html.render_page(spec, 'canvas')`. About 8 ms per turn, measured.
   - **Any other language:** run `python3 server.py` and `POST /render` with `{"spec": …}`. About 10–20 ms, measured.
3. If there are errors (HTTP 422 from the service), send them back to Claude once and ask for the whole JSON again (`api_example.py` shows this).
4. Send the HTML to the canvas pane, and `spec.chat` (text, note, points, prompts) to your own chat interface.

**What makes it safe to run unattended**
- Every piece of text from Claude is escaped before it goes into the page.
- Formulas are read, never executed.
- Unknown blocks, broken slots, jargon and blocks marked "changes requested" are all refused.
- The service re-reads the registry on every request, so an approval takes effect without a restart.
- The service has no memory between requests, so it scales by running more copies.

**What it does not do**
- It does not call Claude.
- It does not store conversations; keep earlier turns' specs yourself for revisions.
- It does not measure the real height in production: the estimate is calibrated, and the browser test is a QA step.

## Wiring it into the Tojo agent

1. **System prompt** = your persona and scope file + the retrieved domain chunks + the output of `diagnosis_html.py prompt` (which carries 06 in full). The catalogue in that output is generated from the registry, so approvals and retirements reach Claude automatically.
2. **Claude returns one JSON spec.** Run `validate`. If there are errors, send them back once, as `api_example.py` does. Warnings, such as draft blocks or going over budget, are logged but not blocking.
3. **Render the canvas** with `render_page(spec, 'canvas')` and put it in the canvas pane. On desktop the pane sits beside the chat; on mobile it is inserted in the message stream above the chat part of the answer. It is the same file either way: the layout switches at a 700px canvas width.
4. **Render the chat parts in your own UI** from `spec.chat`: the text, Tojo’s Note (gold handwriting, larger, no marker), the question options as buttons, the points as selectable rows, and the three prompts.
   - When points are selected, prefill the input with `@Point1 @Point3 `.
   - Call `tojoCanvas.lightPoints(canvasEl, [1, 3])` so the linked canvas items light up.
   - Send the next message with `turn.user_tag`.
5. **History:** keep earlier canvases as one-line stubs (`[dp-01 · route-map · discharge chain]`) plus their specs. To revise one, have Claude re-emit the spec rather than editing HTML.

## The review loop (how approvals change things)

You review blocks in `out/gallery.html` and sample turns in the canvas, then tell me by block id what to approve or change. Each round:

```bash
python3 diagnosis_html.py feedback chain approved "Keep/change badges read clearly"
python3 diagnosis_html.py feedback two-flow changes_requested "Row labels too faint; add times row"
```

- **Feedback log:** every verdict is appended to that block's `feedback` log, and its status changes. `changes_requested` blocks are refused by the validator until revised.
- **General feedback** becomes a numbered row (F1, F2, …) in `06` §0 and is enforced where it lives: a word limit, a budget, a style token.
- **Revised blocks** get `version + 1` and go back to `draft` for the next review.
- **`block_requests`** that Claude logs in real turns are the queue for new blocks.
- **`CHANGELOG.md`** records every change.

## Colour is a rule

Nothing stored carries a colour. The generator picks the shade from the turn number, in sets of three:
- turns 1–3: sage
- turns 4–6: mist
- then the rotation repeats, as set in `tones` in the registry.

To add or change a shade, edit the `tones` list and the matching `[data-tone]` block in `tojo.css`. No template or turn changes.

## Plain English is enforced

The registry holds a `plain_english` list: abbreviations (ALOS, TPA, RMO, OT…), jargon words (derived, provisional, stock-take, bed-days…) and shorthand (“~”, “5 h”, “Cr”), each with its plain alternative. The validator **refuses** a spec that uses any of them, in the chat or on the canvas, unless the user used the word first (`turn.user_words`). Add words to the list as reviews find them.

## Honest limits

- Height estimates are calibrated from real renders and land within about 3% on most turns, but they can run up to 12% high on unusual content. `tests/check_turns.py` measures the real height and has the final word.
- The `night` theme is draft, so theme alternation (02 §5) is off until it is reviewed.
- Blocks still `draft`: two-flow, compare-table, agenda-grid, role-cards, fill-blank, fork. They work, but haven't had your review yet.
