# 08 — Shared turn rules (every tool)

Rules settled in the Bed Management review, 30 Sep 2026. They add to 06 (response) and 07 (block design) and apply to every tool from now on. Where they differ from an older line in 06 or 07, this file wins.

## 1. How a turn is made
- **Through the generator only.** Claude writes one JSON spec per turn. The tool's generator validates it and draws it. Nobody writes or edits turn HTML by hand.
- **The spec records the conversation:** `turn.user_message` (the user's message), the chat parts (text, Tojo's Note, @points, one question with its options, the three prompts), and the canvas blocks with their words. `turn.transcript` keeps the source wording when a turn comes from a worked transcript.
- **Draw from the block library.** Use the approved universal patterns first (scope `all`), redrawn in the tool's colours through the library's colour variables. A tool writes a new block only when no library block can carry the content, and adds it to the library as `draft`.
- **One turn at a time.** Show a turn in three samples; the user picks one; then the next turn.

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

## 6. Entries (the common tool layer)
- Where a turn asks for data, the user types it **in the drawing**: a placeholder or an "Add yours" button opens a field right there.
- Each entry is written into the chat message with the place it came from, under "Added on the drawing:".
- **Every entry is added; none replaces another.** A prompt or an option sets the first line of the message and keeps the entries.
- A field shows "In your message" once its entry is in.

## 7. The block library
- **One library for every tool** (`Common Elements/library/build_block_library.py`).
- **Blocks only.** Each template is drawn inline as its canvas, at the desktop canvas width (864px) and the phone width (362px). Never the app interface (rail, header, chat panel), never frames, never whole pages.
- Why: the Discharge library published as blocks only stayed shareable. The version that added twenty framed whole-interface pages (6.6 MB, each a full page inside a frame) stopped opening for anyone but its owner. Restoring the blocks-only version fixed it at once.
- Each template carries its badge (universal pattern, or one place or tool only), its status (approved, variation, draft), when to use it and when to avoid it.
