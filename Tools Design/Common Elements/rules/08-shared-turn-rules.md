# 08 — Shared turn rules (every tool)

Rules settled in the Bed Management review, 30 Sep 2026, and added to since. They add to 06 (response) and 07 (block design) and apply to every tool from now on. Where they differ from an older line in 06 or 07, this file wins.

## 1. How a turn is made
- **Through the generator only.** Claude writes one JSON spec per turn. The tool's generator validates it and draws it. Nobody writes or edits turn HTML by hand.
- **The spec records the conversation:** `turn.user_message` (the user's message), the chat parts (text, Tojo's Note, @points, one question with its options, the three prompts), and the canvas blocks with their words. `turn.transcript` keeps the source wording when a turn comes from a worked transcript.
- **Draw from the block library.** Use the approved universal patterns first (scope `all`), redrawn in the tool's colours through the library's colour variables. A tool writes a new block only when no library block can carry the content, and adds it to the library as `draft`.
- **One turn at a time.** Show a turn in three samples; the user picks one; then the next turn. Once a turn's look is set, the rest of a place may be delivered together, all through the generator.
- **Variety beats boxes.** A turn of cards and strips only is not enough; each turn needs a drawing that pictures its idea (a route, a scale, a loop, a receipt).

## 2. Every turn looks different
- A place's main block (the first after the heading) is used by one turn only.
- No block except heading and the effect box appears in two turns in a row.
- The one exception: a fill-in-the-blank and its answered redraw share one block (06 §10.2), and the redraw adds at least one block of its own.

## 3. Background theme every four turns
- Turns 1–4 use the place's base theme, 5–8 its second theme, 9–12 the base again, and so on. The generator sets it from the turn number; specs store no colour.
- A redraw keeps the theme of the turn it redraws (`turn.redraw_of` plus `canvas.tone`).
- Landing pages always use the base theme.

## 4. The screen
- **Roomy pages.** A desktop page may run to 1.5–2 screens.
- **Desktop:** the chat panel is one screen tall with its own scroll; only the page area scrolls. On landing pages the header stays fixed down to the line under Refresh now.
- **Phone, a turn:** one feed, in this order: the user's message, Tojo's text, the drawing, then Tojo's Note, the question, the points and the prompts. The message box stays at the foot.

## 5. Picking (the common tool layer)
- The first item of a drawing loads **raised**: lifted, gold edge, a solid and a soft shadow, a colour change, with its sheet open.
- Tapping another item raises it and opens its sheet; the rest drop back and close.
- **Desktop:** one shared sheet under the drawing. **Phone:** each sheet opens right under its item, with a small pointer.
- **Phone: pickable items are always stacked one above the other, never side by side**, whatever the drawing does on a desktop.
- **No text may run outside its box** on either layout (picks, sheets, cards, callouts). Long words wrap. The browser check fails a turn that breaks this.

## 6. Entries (the common tool layer)
- Where a turn asks for data, the user types it **in the drawing**: a placeholder or an "Add yours" button opens a field right there.
- Each entry is written into the chat message with the place it came from, under "Added on the drawing:".
- **Every entry is added; none replaces another.** A prompt or an option sets the first line of the message and keeps the entries.
- A field shows "In your message" once its entry is in.

## 7. The block library
- **One library for every tool** (`Common Elements/library/build_block_library.py`).
- **Blocks only.** Each template is drawn inline as its canvas, at the desktop canvas width (864px) and the phone width (362px). Never the app interface (rail, header, chat panel), never frames, never whole pages.
- Why: the Discharge library published as blocks only stayed shareable. The version that added twenty framed whole-interface pages (6.6 MB, each a full page inside a frame) stopped opening for anyone but its owner. Restoring the blocks-only version fixed it at once.
- **Updated only when asked.** Turns are delivered and approved first; the library is rebuilt only when the user asks for it.
- A tool's own drawings go in the library with the turn each first appears in.
- Each template carries its badge (universal pattern, or one place or tool only), its status (approved, variation, draft), when to use it and when to avoid it.

## 8. The three buttons, on every turn (1 Oct 2026)
- **Every turn ends with the three buttons**, not only landing pages: Proceed with next step (naming the step), Add more, Jump to the next place. Same order and look as the landing page (06 §11.2 point 5, 07 §3.2).
- Why this is written down: 06 F11 and §11.2 put the three buttons only on landing pages, so no generator asked for them on turns, and the Bed Management Diagnosis turns and bm-so-01 went out without them. Avishek’s rule is that they belong on every turn.
- The generator refuses a turn spec without `canvas.actions`. Each button writes its line into the chat message like a prompt and keeps the entries.
- Solutions jumps to Automations. The order is Diagnosis → Solutions → Automations → Processes, and Processes jumps back to Diagnosis.

## 9. Lessons from the Bed Management Solutions review (1 Oct 2026)
- **Where a place ends is set by the content, not by a mention.** Mentioning or listing what the automations will be stays in Solutions. The conversation moves to Automations only when the build itself is detailed (how it runs, the systems, the IT work). Avishek kept transcript turns 19–20 in Solutions on that rule.
- **A turn the record marks as superseded is not drawn.** Bed Management transcript turns 24 and 25 were replaced by 27 and 28; only the versions of record become turns.
- **Samples:** a first turn in a new place gets three samples; once its look is set, the rest of the place may come as one set, one drawing per turn.
- **A figure Tojo supplies is labelled.** A slider default, a goal or a measure taken from the reference file and not from the conversation carries its source (Tojo’s guess, Goal, worked out from your figures).
- **One entry per question.** The same missing number is asked for in one place on a turn, never twice.

## 10. One set of latest generators for every tool (5 Oct 2026)
- Every tool draws its turns with the latest generators (today: the Bed Management ones). A tool loads that generator as its own copy and points
  it at its own registry, colours, shell and drawings (see `Discharge Process/dp_common.py`). Fixing a generator fixes every tool.
- Discharge Process was regenerated this way: all 32 turn templates, the three buttons on every turn, entries in the drawing, a background every
  four turns, one main drawing per turn. The old Discharge turn templates are retired from the library.
- The library shows each template as its canvas only, and each template's picking groups are its own, so picking in one never opens a sheet in another.

## 11. The reply check, in every tool (6 Oct 2026)
- **The rule itself is not here.** It is `tojo-v2 - Regular Chat/rules/always-on/09-reply-check-rules.md`, always on, for the regular chat and every tool. There is one copy only, so the chat and the tools can never drift apart. This section says only how a tool carries it out.
- **Every turn spec carries `reply_check`:** the record of 09 §9, with the fields in `tojo-v2 - Regular Chat/schema/reply-check-report.schema.json` (`$defs.turn_record`). The generators check it through `tool-layer/reply_check.py`. A record that is wrong refuses the turn. A missing record is a warning, because the approved templates were made before the rule; a live turn always has one.
- **The three fixed lines are never written into a spec.** Tojo sets `reply_check.say` (`opening` or `reset`) and the app shows the line word for word, read from rule 09. The page shows it as Tojo's own message, between the user's message and the answer.
- **The rating question is not a generator turn.** It is a short, text-only message the app shows before the 10th, 20th, 30th… counted turn. The turn that follows records the answer as `last_reply.class` (`rating_good`, `rating_fine`, `rating_bad` or `rating_skipped`), and its page shows the question and the answer before the reply.
- **A rework after a reset is a normal turn of the place,** through the generator, with the three buttons. Its main block is never the main block of the turn that was missed (§2), and it never shows the same drawing again (09 §5.3).
- **Landing pages, the opening line, the rating question and the reset line are not counted turns** (09 §1).

## 12. Domains (8 Oct 2026)
- **Two groups of tools.** Operations Tools: Discharge Process, Bed Management, OPD Diagnostic Leak. Financial Tools: Supply Chain and Procurement, Revenue & EBITDA, Length of Stay. New tools join a group, or start a new one.
- **A domain has its own identity, never only its own colours** (07 §1.1): shapes, paper, frame dress, marks, the raised state and the kind of drawing. The Virevo type and type scale never change.
- **The response templates are shared by every tool in every domain.** A tool redraws a universal pattern in its own look; it never copies another domain's look.
- **The block library:** see §13 for the layout from version 14.

## 13. Every template is open to every tool (Avishek, 8 Oct 2026)
- **No template belongs to one tool.** Every response template (universal patterns, landing elements and shared parts, worked turns, drawing blocks) is open to every tool and every place. A tool redraws it in its own look and colours, with its own words. Example words in a template come from the tool it was first drawn for; they are not a limit.
- **Only landing pages are tool-specific:** by tool and by place (home, Diagnosis, Solutions, Automations, Processes).
- **Templates are grouped by what they show:** Logical (sides of an argument), Process flow, Time flows, Selection (pick one or a few), Financial (money effects), Numbers and measures, People and ownership, Universal elements. A template may name a second group ("also useful here").
- **Every template has a "How to use this template" card** (`library/template_uses.json`): what it shows, key uses in order, the logic it can show, the responses it is best for, and, when its drawing carries a picture (beds, clocks, timelines, money, people, routes), a note to use it whenever the response is about that thing.
- **A new template is not added without its card.** `library/reorganise.py` stops if one is missing.
- **Layout:** `out/block-library.source.html` keeps the build order (tool injectors write to it); `library/reorganise.py` lays it out as the published library (`out/block-library.artifact.html`), which is always published to the original link.

