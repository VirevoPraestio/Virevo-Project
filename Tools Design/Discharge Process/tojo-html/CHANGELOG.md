# Changelog

## 2026-09-29 — the Automations generator and its first nine turns
- **New `automations-html-generator/automations_html.py`**, built like the Solutions generator: validate, render, sample, build (one review file per turn and the tab book), prompt and catalog. Same simple-English rules, plus plain words for system terms (records, link, screen, as it happens). `check.py` measures every turn in the browser.
- **New `automations-html-generator/registry.json`:** `heading` and `landing` (Automations B, the overnight arc, now drawn from data) approved, and six draft blocks, all Automations only:
  - `nightshift`: the invisible digital factory. Eight stations on one moving line from the evening round to going home. Play the night or move the clock; a gold hand marks where a person approves.
  - `brain`: a digital brain and glowing network on a charcoal screen. Pick a day of the stay; facts flow in and the summary fills.
  - `agent`: the autonomous thinker. A holographic figure inside its loop (notice, gather, check, draft, ask); step through, with the hand-offs to people and what Tojo never does.
  - `sources`: drawn switches for where each record comes from; lamps light when an automation has every source it needs. Presets for no IT work, one link, all links.
  - `helper`: the friendly desk helper, with the IT list in plain words or with the detail.
  - `relay`: the hand-over from discharge to the bed desk on two lanes, each side checking the other, against the 30-minute line.
- **Turns (`examples/automations/`):** au-00 landing (first visit), au-01 the night shift (playbook §4), au-02 to au-04 the three "tell me more" steps (playbook §5), au-05 one plain question about their systems (playbook §7), au-06 their answer, au-07 the hand-over to the bed desk (beyond the playbook, from the discharge reference's Bed Management notes), au-08 landing the next morning.
- **Rules:** 07 §1.4 adds charcoal screens (light teal glow means Tojo is at work, never "switched on") and the machine motifs. 06 §1 lists the new blocks.
- **Solutions:** fixed a validator slip where block checks ran only on the last block.
- **Not supplied:** `bed-management.md`. au-07 uses only what the discharge reference says about Bed Management.

## 2026-09-29 — so-02 and so-03 back in Solutions; the move rule narrowed
- **The rule (06 §1), narrowed:** naming the automations or the process changes and saying briefly what each does stays in Solutions. The conversation moves to Automations only for the working detail: how things are automated, which records are tracked as they happen, what is read from which system, what the IT team sets up. The same holds for Processes.
- **Restored:** so-02 (what the automations do, on real times, `untangle`) and so-03 (the voice-notes correction, `maze`). Their prompts about the IT team and paper notes now carry a move to Automations; "Next, the changes on the wards" carries a move to Processes.
- **Renumbered:** the knots, stake and route turns are now so-04, so-05 and so-06; the next-morning landing page is so-07.

## 2026-09-29 — Solutions tab complete to the move into Automations and Processes
- **The rule (06 §1):** Solutions holds the answer as a whole. As soon as the conversation goes into the detail of one part, the next turn is drawn in that part's tab. Automations takes any elaboration of what runs by itself, including automations for Bed Management or other areas the reference calls on. Processes takes the people who must agree, team and role changes, changes on the wards and the measures. A passing mention is not a move.
- **`chat.moves`:** a spec marks the prompts that start a move, with the tab. The chat shows "Opens Automations" or "Opens Processes" on them. The validator checks each move names a real prompt and a real tab.
- **Moved out of Solutions:** the earlier so-02 (Automations on real times, `untangle`) and so-03 (the voice-notes correction, `maze`) go into the automation detail, so they belong to the Automations tab. They are kept in `examples/solutions/archive-for-automations/`, to be redrawn in the Automations look.
- **New turns (playbook §6 and §7):**
  - `so-02` (findings): "Which part saves the most time?" New draft block `knots`: the wait as one rope on real times, five knots. Pick parts; a knot comes undone only when every part it needs is picked. No part works alone.
  - `so-03` (recommendation): "Is it worth what it costs?" The threshold ("not a maybe-someday, you are already there") and cost against what is at stake. New draft block `stake`: a drafting balance and bars to one scale, with a slider for the share of the wait the trial wins back.
  - `so-04` (recommendation): "What would we do first?" New draft block `route`: three steps on one trail, ending at a bulb and two doors. One opens Automations, one opens Processes. This is the last Solutions turn.
  - `so-05` (landing): the tab's landing page the next morning, after the midnight refresh.
- **so-01:** its prompts "Start with the automations" and "Do we need to hire anyone?" now carry their moves.
- **Checks:** all six turns validate. Desktop canvases 552 to 794px; phone 934 to 1,437px. No sideways scroll, no script errors.

## 2026-09-29 — Solutions so-02 and so-03; so-01 approved
- **so-01 and the `puzzle` block approved.** Review pages: the "ResizeObserver loop" error is fixed. The pages now refit only when the width changes.
- **so-02 (part, playbook §4): Automations on this hospital's real times.** New draft block `untangle`, Solutions only. Five threads of going-home work run from 6 PM to 4 PM. Today they hang slack through the hours nobody uses and knot at the morning signature; the patient leaves at about 3:15 PM. The switch "With the automations" pulls each thread straight from the evening round. Pick a thread name to light it and open its sheet. Every end time carries its source.
- **so-03 (challenge, playbook §5): "Our doctors don't use voice notes".** New draft block `maze`, Solutions only, redrawn as a real labyrinth. Three routes end at walls. The one-tap form gets through and lights the bulb, with what the hospital must already have. Pick a route to walk it.
- **Recipes:** `part` starts with `untangle`; `challenge` starts with `maze`.

## 2026-09-29 — Solutions tab restarted after its landing page
- **Why:** the first drafts of so-01 to so-11 did not follow the playbook, their drawings did not work, and nothing on them could be used. They are kept in `examples/solutions/archive-2026-09-29/` and are no longer built.
- **Turn list:** `examples/solutions/turns.json` now names the turns to build, in order. Today: so-00 (landing, first visit) and so-01 (the five parts).
- **so-00:** now speaks of the playbook's five parts (Automations, Changes on the wards, People who must agree, Team and roles, Measures we will watch) instead of five solutions.
- **so-01 (overview, playbook §3):** the answer as one jigsaw picture. New draft block `puzzle`, Solutions only: the idea as the lit centre piece, five parts locked around it. Pick a piece to lift it, outline what it relies on, and open its sheet. "Ask Tojo about this part" writes the message into the chat box with its point attached.
- **Removed:** the draft blocks `maze`, `tangle` and `jigsaw`.
- **Delivery, from now on:**
  - `solutions_html.py build` writes one review file per turn to `out/solutions/turns/` (desktop 1440 × 900 and phone 390 wide, side by side, both live) and the tab book `out/solutions/solutions-tab.html` with every turn. `solutions-tab.artifact.html` is the same book, ready to publish as an artifact.
  - `solutions_html.py sample SPEC -o FILE` writes the review file for one spec.
  - The review pages are drawn by the new shared `landing-common/review_page.py`, so every tab's generator can write them the same way.
  - No PNGs. `check.py` measures in the browser and writes screenshots only when asked (`SHOTS=1`), to a scratch folder.
- **Simple English, stricter:** the Solutions validator now refuses sentences over 20 words, a dash or semicolon joining two thoughts, and a further list of long words (via, ensure, require, implement and others).
- **Scope:** every block in `solutions-html-generator/registry.json` now says `scope`: `all` or `Solutions`. The block library will show it when it is next rebuilt.

## 2026-09-29 — Solutions: two new turns and three "thinking" blocks
- **Direction:** the Solutions tab must look clearly unlike Diagnosis and show the thinking behind each solution. 07 §1.3 now names the motifs: lightbulb, maze, tangled and untangled wires, jigsaw.
- **New draft blocks in `solutions-html-generator/registry.json`:**
  - `maze`: a walled corridor from the problem to a lit bulb. Ruled-out routes are dead ends with a red ✕ and the reason. The validator needs at least one step and one dead end, and a reason on every dead end.
  - `tangle`: the same tasks knotted through one point today, then in straight lanes after. The validator checks every thread's lane exists and every lane has a thread.
  - `jigsaw`: the solutions as pieces of one picture. Agreed pieces lock in, open ones sit loose, the piece that just fitted is gold and snaps in (no motion when reduced motion is set). Only one piece can have just fitted, and it must be agreed.
  - Recipes updated so each can be used in the right turn types.
- **New turns:**
  - `so-10` (question): "Let’s settle the insurance desk question", the landing page's next step. A `maze` of routes to earlier insurance approval, and one structured question.
  - `so-11` (data-back): the answer ("two main insurers accept an early request"). A `tangle` from one knot to two lanes, and a `jigsaw` with Solution 1 just fitted.
- **so-08 and so-09 brought into line:** Solution 1 was shown as agreed while the insurance desk was still open. It is now "Tested with you", 4 of 5, until so-11 settles it. so-08's title is now "One agreed, one answer away". so-09 shows Solution 3 at 3 of 3.
- **Checks:** all twelve validate. so-10 is 659px desktop and 910px mobile; so-11 is 687px and 1,438px.

## 2026-09-29 — Solutions review, first pass fixed
- **`scales`:** when a line is under 6% of the scale it now carries a pointer and label, so the ₹10–11.5 lakh team line no longer reads as a letter "H". Mobile puts the label on its own line.
- **`register` validator:** "agreed" now needs every area settled, and the areas listed must match the "of N" count.
- **so-06:** chat now says one Discharge Manager now, two Discharge Executives after the trial confirms the busy hours (matches so-07 and the handover). Awkward "maybe-someday" line removed; first prompt now "Why the Manager before the trial?".
- **so-02:** third bullet softened to "works less well where evening decisions come late", matching Timing as "still open".
- **so-08:** solution 1 is 5 of 5 settled; solution 2 lists Cost · People · Systems; solution 3 lists Cost · People · Timing and is 3 of 3.
- **Checks:** all ten still validate; every desktop canvas fits; so-06 is 579px desktop, 806px mobile. `out/solutions/system-section.md` rebuilt.

## 2026-09-29 — the Solutions generator and the first ten Solutions turns
- **New `solutions-html-generator/solutions_html.py`.** It validates a Claude spec against `solutions-html-generator/registry.json` and draws the canvas offline in the Solutions look, inside the app shell.
  - Commands: `validate`, `render`, `build`, `prompt` and `catalog`.
  - It reuses the Diagnosis slot checks, the plain-English list and the chat rules, so every tab is held to the same rules.
- **New `solutions-html-generator/registry.json` with 11 blocks:**
  - **approved:** `heading`, `tracks` and `landing`, the last drawing the approved landing template from data;
  - **draft, promoted from landing variations:** `sheets`, `revisions` and `register`;
  - **draft, new:** `weigh` (a solution as a beam, each consideration a support), `signoff` (who has to agree, with a meter for what each gives up and the approver's stamp), `split` (what Tojo adds against what must already be there), `scales` (cost and what is at stake drawn to one scale), and `plan` (steps ending in a fork).
- **New `examples/solutions/`:** ten specs, as the Claude API would return them, following the conversation arc for the solution stage.
  - `so-00` is the landing page on arrival.
  - `so-01` to `so-08` are the overview, weighing solution 1, a correction, who has to agree, the redraw with real times, cost against what is at stake, next steps, and what is left.
  - `so-09` is the landing page after the midnight refresh.
- **Checks:** all ten validate. Built pages are in `out/solutions/`. `check.py` measures them in a browser: every canvas fits the desktop budget, and none scrolls sideways. `so-09` on mobile is 1,539px against the 1,500px guide, which is accepted for a landing page and logged here.
- **New `out/solutions/system-section.md`:** the Solutions system-prompt section.
- **Landing template:** now knows the `idea` and `parked` statuses.

## 2026-09-29 — landing elements added to the block library
- **New `landing-common/landing-elements.json`** lists 20 elements cut from all 12 landing samples: 7 approved, as part of an approved landing page, and 13 variations from the samples not chosen. It also lists 3 shared parts (the update stamp, the three buttons, and What Tojo still has to do). Each entry has a purpose and where it can be reused.
- **New `landing-common/build_library.py`** builds the full library: the Diagnosis blocks and sample turns, then the approved landing pages, the shared parts in all four looks, and every element at desktop and mobile width, each with its first-visit state behind an expander. Elements are cut from the rendered samples, so they always match the templates.
- **06 §1:** patterns may cross tabs; looks never do.
- **07 §9:** a borrowed structure is redrawn in the new tab's look.

## 2026-09-28 — 06 and 07 v2, complete on their own
- **06 v2.** 06 no longer points to 01, 02, 04 or 05.
  - **Folded in:** the two registers, the order of work, how to ask, the full evidence rules, what the canvas must carry, multi-part reveals and dependencies, and the interaction rules.
  - **Added:** tabs and their generators (§1), the `landing` turn type, landing pages (§11), and F11.
  - **Fixed:** the example spec no longer carries a colour, and the example measure reads "average stay", not ALOS.
- **07 v2.**
  - **Added:** the look of every tab with its colour values (§1), the landing-page zones and approved templates (§3), and build discipline (§8).
  - **Folded in:** the visual grammar that 02 used to hold (§5: fill types, muted boxes, tags, badges, dividers, arrows).
  - **Mapped:** the state meanings onto each tab's palette.
- **Contrast fix.** The waiting amber in Solutions, Automations and Processes darkened from `#A86B12` to `#8A5608` (it was 4.2:1; now at least 4.9:1). The Processes empty readout dash now uses muted text instead of grey. All samples and canvas artboards were rebuilt.
- **Rebuilt `out/system-section.md`** from the new 06. All 12 Diagnosis turns still validate.

## 2026-09-28 — landing pages approved
- **Approved:** Diagnosis C (Under the glass), Solutions B (Iteration tracks), Automations B (Overnight arc) and Processes A (Ward board).
- **Kept for reference:** the other eight, marked "not chosen".
- **New file:** `landing-common/landing-registry.json` holds the picks and their feedback log.
- **Build option:** `APPROVED=1` in `build_landing.py` builds only the approved templates.
- **Design canvas:** approved artboards are titled "approved", with a green note on each row.

## 2026-09-28 — tab landing pages, one generator per tab
- **Renamed** `generator/` to `diagnosis-html-generator/` and `tojo_html.py` to `diagnosis_html.py`. All imports, tests and docs are updated, and all 12 Diagnosis turns still validate.
- **New generator folders:** `solutions-html-generator/`, `automations-html-generator/` and `processes-html-generator/`. They share the typography; each has its own look.
- **New `landing-common/`:** the shared landing-page parts, the build script and the QA measure script.
- **12 landing-page samples:** three per tab, each in desktop and mobile and in both states (in progress and first visit), all inside one-screen desktop budget. Rules are in `LANDING-PAGES.md`.
- **Design canvas "Tojo — Tab Landing Pages":** 24 interactive artboards.
- **Preview shell fix:** the current tab is marked in the rail and in the mobile tab bar.

## 2026-09-28 — project files gathered for the Solutions tab
- **Added** `rules/05-universal-answering-method.md`, `references/discharge-process.md` and `references/discharge-process-conversation-playbook.md`. 06 and the F8/F9 feedback already depended on them; they now sit in the project.
- **Added** `PROJECT-CONTEXT.md`, a primer for starting a new chat on this project.
- **README** and **DIAGNOSIS-TAB.md** point at the new files.
- No generator, registry, block or example changes. All 12 example turns still validate.

## 2026-09-26 — v4 final: Diagnosis tab closed (registry v4)
- **All ten playbook templates approved:** time-window, hour-load, was-now, scorecard, narrow-claim, converge, bands, shared-flow, zoom-trail, phases. 23 templates are now approved; agenda-grid, fill-blank and fork are still draft.
- **Rules 06:** the turn-type recipes and the block-choice guide now name the new templates. There is a new turn type, `data-back`, for when real numbers arrive.
- **Rules 07:** the desktop and mobile layout table covers all templates.
- **Height costs** re-calibrated from real renders.
- **Design canvas:** a template-library row (desktop and mobile canvas widths), generated by `dc_export.py library`.
- **`DIAGNOSIS-TAB.md`:** a handover note.

## 2026-09-26 — v4 draft (registry: 26 blocks)

**Ten new templates** from the conversation playbook, all draft and awaiting review: time-window, hour-load, was-now, scorecard, narrow-claim, converge, bands, shared-flow, zoom-trail, phases. Each has a desktop and a mobile layout, sample content, and a plain-English check. Review them with `tojo_html.py blocks …`.

**Fix: shell classes renamed with an `sh-` prefix.** The preview shell's short class names (`.m`, `.bar`, `.row`, `.opt`, `.ph`, `.lab`) were leaking into blocks with the same names. For example, comparison-table cards on mobile previews were being restyled as pills. Shell and blocks can no longer collide. All 12 turns re-tested.

## 2026-09-26 — v3.2 (registry v3)

**Approved**
- Turns dp-07 to dp-10.
- The role-cards and compare-table blocks.
- All four turns were added to the design canvas.

**New turns for review**
- dp-11: plan the trial and ask for the hospital's times on a blank timeline.
- dp-12: the same timeline filled with their real times. It states plainly what changed: decisions happen from 6 to 9 PM, not at a fixed 7 PM; the wait is 5 hours 15 minutes, not 5; the yearly cost is ₹10.9 crore, not ₹10.3 crore. It also names one new finding: the bed sits empty for 75 minutes after the patient leaves.
- Both were built strictly by the generator from their JSON inputs.

**Fixes found by these turns** (in the generator, so they apply to every future turn)
- fill-blank now wraps evenly when it has more than five steps.
- Filled boxes are exactly as tall as blank ones, so the answered redraw lands on the same spots on desktop and on phones. The test checks this.

## 2026-09-25 — v3.1
- **New turns for review:** dp-09 (knowing it worked: six measures curated from discharge-process.md §8, marked Yours, Goal or New) and dp-10 (the plan: a two-week trial first, the manager hire the numbers already call for, and cost against what's at stake). Both were built strictly by the generator from their JSON inputs, with no hand edits.
- **`server.py`:** an HTTP service for backends that are not written in Python. Measured at 10–20 ms per render. A bad spec returns HTTP 422 with the errors to send back to Claude.
- **README:** a technologies list and a guide to running it on the agent backend.

## 2026-09-25 — v3 (registry v3)

**Approved**
- Turns dp-05 (automatic paperwork) and dp-06 (changes on the wards).
- Shade B, **mist**, a shade lighter than sage. The darker "deep" shade was not chosen.
- The two-flow block.

**Colour is a rule, not stored content (F10)**
- Templates, layouts and turns are saved without colour. The generator picks the shade from the turn number, in sets of three: 1–3 sage, 4–6 mist, 7–9 sage, and so on.
- Claude never sets a colour. `canvas.tone` is allowed only on a fill-in-the-blank redraw, and the validator warns when it is set.
- Older turns were not re-coloured by hand; re-rendering applies the rule. The dark "night" theme is retired.

**Blocks**
- two-flow v2: a row can carry a flag, for example "Biggest hold-up", on the today side.
- On mobile, the two sides of each row now sit next to each other, which halves the height.
- Chains longer than five steps wrap evenly.
- role-cards: the approver box can be linked to a chat point.
- compare-table: rows can be linked to chat points.
- stat-strip values can show a range, for example "₹10 to 11.5 lakh".

**New turns for review**
- dp-07: people who must agree.
- dp-08: who is in charge. This includes the staffing check against the hospital's two busy times of day, from discharge-process.md §7.4.4.

## 2026-09-25 — v2 (registry v2)

**Approved:** turn dp-03 (diagnosis, sample 3A) and turn dp-04 (five-part fix, sample 4B). The other four samples moved to `examples/archive/`. Blocks chain, stat-strip and cards are now approved.

**Feedback F7: simple, plain English only.**
- The registry has a `plain_english` list, and the validator refuses abbreviations, jargon and shorthand.
- Built-in labels are plain: "From your numbers", "Tojo’s guess", "Need from you", "What people usually say".
- Number formats write units in full: 5 hours, ₹10.3 crore, ₹4.5 lakh.
- All four example turns were rewritten; for example, "Wait, fit to leaving" became "Hours each patient waits to leave".

**Feedback F8/F9: expanders hold real detail from the reference file.**
- Expanders are now native `<details>`, which work with no scripts.
- The button says what is inside, and it opens to 2–6 points (`more_label`, `more_points`).
- The five solution parts are filled from discharge-process.md §7.4.1–7.4.4 and §8.

**Fixes found by testing**
- Budget set to the real visible canvas: 824px, not 780.
- Height estimates calibrated from real renders (`tests/calibrate.py`).
- A long source tag made the mobile screen scroll sideways.
- Opening one card stretched its whole row.
- The "waiting" line showed on finished sums.
- Rounding differed between the build and the browser (212 vs 213).

**New**
- `tests/check_turns.py` browser test.
- `dc_export.py` for the design canvas.
- Embedded fonts for fully offline pages.
- A stand-in-Claude test of the API repair loop.

## 2026-09-25 — v1 (registry v1, generator 1.0)

**From review of the three chat-interface versions**
- Version 3 (route map on sage) adopted as the house style. Blocks derived from it are marked `approved`: heading, route-map, calculator, threshold-gauges, balance, progress-trail and handnote.
- Standing feedback recorded in 06 §0:
  - F1: one screen on desktop.
  - F2: cleaner depiction.
  - F3: less text.
  - F4: Tojo's Note highlighted by colour and size only.
  - F5: Version 3 is the house style.
  - F6: mobile reflows and never shrinks.
- Tojo's Note is now gold Caveat at about 31px with no marker highlight. This also changes all three versions on the design canvas.

**From 05-universal-answering-method**
- calculator v2: no invented defaults. A figure the user hasn't given is `source: "needed"`, and results wait for it. The condition is mandatory.
- Thresholds and cost/return are recommendations, so `threshold-gauges` and `balance` are refused in question and data-ask turns.
- Turn dp-02 was rebuilt accordingly. It is now a data-ask that prices the wait from the user's own figures. The earlier ₹30,000 revenue-per-bed estimate and the Discharge Manager triggers are gone from this turn.

**New**
- 16-block registry: 7 approved and 9 draft.
- Offline generator with validation, word limits, a one-screen budget estimate, and a rule that the chat pointer never gives a direction.
- Gallery, preview shells, API system-prompt assembly, and an API loop example.
