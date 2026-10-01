# Common Elements

Everything every Tojo tool shares: the rules, the generators, the tool layer and **the one block library**. Each tool's own folder (Discharge Process, Bed Management, and the tools to come) holds only what is that tool's: its look, its landing pages, its turns and its generator settings.

Set up 30 Sep 2026 from the Discharge Process repo (`Tools Design/Discharge Process/tojo-html`). The generators and rules here are the same files, moved here to be shared; Discharge Process still has its own copies and they have not changed.

## What is where

| Path | What it is |
|---|---|
| `rules/05-universal-answering-method.md` | The general answering method (reference). |
| `rules/06-html-response-rules.md` | Response rules: turn types, the chat panel, choosing blocks, evidence, reviews. |
| `rules/07-html-block-design-rules.md` | Block design rules: looks, type, two layouts, visual grammar, interaction, adding a block. |
| `rules/08-shared-turn-rules.md` | **New.** Rules from the Bed Management review that apply to every tool: generator only, every turn looks different, background every four turns, the phone order, picking, entries, the blocks-only library. |
| `blocks/registry.json`, `blocks/samples.json` | The universal block database (26 blocks) and their sample words. |
| `diagnosis-html-generator/` | `diagnosis_html.py` (the universal block renderers, validator and fonts), `assets/tojo.css` and `tojo.js`, `preview.py` (app shell), fonts. |
| `solutions-html-generator/`, `automations-html-generator/`, `processes-html-generator/` | The Discharge place generators and their blocks. |
| `landing-common/` | Shared landing-page parts (stamp, three buttons, chat panel, shell) and the old library's builder `build_library.py`. |
| `tool-layer/tojo_layer.py` | **New.** Picking (first item raised, sheet open, phone sheet under its item) and entries (typed in the drawing, added to the chat message, never replaced). Any tool can use it. |
| `library/build_block_library.py` | **New. The one block library** for every tool. |
| `schema/`, `prompts/`, `tests/`, `examples/` | The response contract, the API prompt template, browser tests, and the Discharge turn specs the library draws from. |
| `out/block-library.html` | The built library. `out/block-library.artifact.html` is the same page ready to publish. |

## The one block library

```bash
cd library && python3 build_block_library.py
```

It draws, in this order: how to use the library (which block when, how a turn is built, which generator draws which place); the universal patterns and every Discharge Process template, drawn by the old library's own code, unchanged; then Bed Management (its look, its five approved landing pages with their first-visit state, its twelve approved Diagnosis turn templates with the samples not chosen as variations, its 11 own drawings with the turn each first appears in, and the tool layer).

**Library updated only on request.** New turns are delivered first; the library is rebuilt only after they are approved and the user asks.

**Blocks only.** Every template is drawn inline as its canvas at 864px and 362px. No app interface, no frames, no whole pages. The Bed Management page CSS is scoped under `.bmx` so it cannot change any other template. This is what fixes the earlier failure: the library stopped opening for anyone but its owner only when twenty framed whole-interface pages (6.6 MB) were added; the blocks-only version always opened. See `rules/08` §7.

Published as **Tojo Block Library** (see `ARTIFACTS.md`). The earlier Discharge library artifact is left as it was until this one is confirmed to open for everyone.

## Adding a tool
1. Make its folder beside this one. Point its generator at `Common Elements` (see `Bed Management/bm_common.py`).
2. Give it its own colours through the library's colour variables; use universal patterns first.
3. Add a section for it in `library/build_block_library.py`, drawing blocks only.
