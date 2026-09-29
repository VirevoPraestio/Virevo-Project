# 07 — Tojo HTML Block Design Rules (v2)

How canvas blocks and landing pages look and behave. This file is complete on its own.

These rules govern the **templates** in each tab's generator, not individual responses. A response only picks blocks and fills slots (06). Anyone adding or changing a block or a landing template follows this file.

**The block library** (`landing-common/build_library.py`) shows every Diagnosis block, the sample turns, the four approved landing pages, the shared landing parts in all four looks, and 20 landing-page elements, both approved and variations.

| Tab | Generator | Templates |
|---|---|---|
| Diagnosis | `diagnosis-html-generator/` | Blocks in `diagnosis_html.py` and `assets/tojo.css`/`tojo.js`, listed in `blocks/registry.json`. Landing page in `landing.py`. |
| Solutions | `solutions-html-generator/` | Landing page in `landing.py`. Turn blocks in `registry.json`, each with a `scope`; `puzzle` is Solutions only. |
| Automations | `automations-html-generator/` | Landing page in `landing.py`, drawn from data. Turn blocks in `registry.json` (nightshift, brain, agent, sources, helper, relay, all Automations only). |
| Processes | `processes-html-generator/` | Landing page in `landing.py`. Turn blocks to come. |

`landing-common/` holds what every landing page shares: the stamp, the three buttons, the chat panel, the app shell, and the design-canvas export.

---

## 1. The looks

### 1.1 Rules for every tab

**Not software.**
- No tables of rows with zebra stripes, no dashboards of widgets, no sidebars of filters, no chat bubbles on the canvas, and no grids of icon-and-shadow cards.
- Structures are **drawn**: lines with stops, gauges with a marked line, a balance, a chain of boxes, a track, a switch, a dial, a seat. If a block could be mistaken for a hospital software screen, it is wrong.

**One tab, one look.**
- Each tab has its own ground, ink, accent and drawn elements, so the user always knows which tab they are in.
- A tab's templates use only its own palette. They never borrow another tab's elements.

**Shared everywhere:**
- **The typography** (§2).
- **The chat panel.** It stays forest (`#10241a`) with cream and gold in every tab, and the canvas is always the lighter half of the screen.
- **Virevo gold `#d4a94f`** for "now", for the next step, and for selected and highlighted items.
- **Gold text on a light ground** uses a dark gold (`#6B4F16` or the tab's own), never the fill gold, for contrast.
- **The state meanings** (§5).

**Colour lives in variables.** Blocks are always written against the tab's colour variables, never fixed colours, so every shade works on every block.

### 1.2 Diagnosis: route map on sage (Version 3, approved 25 Sep 2026)

| Token | Value |
|---|---|
| Ground | sage `#DCE3DA` |
| Cards | `#F7F9F5`, with a 1.5–2px forest border |
| Ink | forest `#10241a` |
| Muted text | `#44544A` |
| Result red | `#8E2F1C` |
| Needs-attention amber | `#B8862B` (borders only) |
| Your-number green | `#2f7350` |

- **Shadows:** where a card is the subject, it gets a flat offset shadow (`8px 8px 0` at 12% ink). No blurred shadows.
- **Labels:** uppercase Poppins, weight 600, with +0.09em letter spacing.
- **Signature elements:** the route map with lettered stops, the magnifying lens, and the pulse line.
- **Shades** (F10):

  | Tone | Ground | Cards | Text | Borders | Status |
  |---|---|---|---|---|---|
  | sage (base) | `#DCE3DA` | `#F7F9F5` | forest `#10241a` | 2px forest | approved |
  | mist, a shade lighter | `#EEF2EC` | white | softer forest `#1C3A2B`; titles stay `#10241a` | 1.5px | approved (25 Sep) |
  | deep, a shade darker | `#C4CFC1` | cream `#F3F1EA` | forest `#10241a`, muted `#37473C` | 2px forest | not chosen, kept for reference |

### 1.3 Solutions: the drafting table

| Token | Value |
|---|---|
| Ground | pale blueprint `#E3EAF0`, with a faint 24px grid (7% navy) |
| Sheets | `#F8FAFC`, with a 1.5px navy border and corner marks |
| Ink | navy `#15304D` |
| Muted text | `#4A5D72` |
| Line blue | `#2E5E8E` |
| Waiting amber | `#8A5608` |
| Settled green | `#2F6B4F` |
| Rail tab | navy with pale gold text |

- **Corners:** square, or 2px at most.
- **Labels:** sentence case, Poppins 600.
- **Signature elements:**
  - **revision triangles** carrying the revision number, one for each time a solution is redrawn;
  - **iteration tracks** from idea to agreed;
  - **drawing sheets** with earlier revisions behind them;
  - **a title block** holding the update stamp.
- **Considerations** show as small circles: filled means settled, dashed amber means still open.
- **Show the thinking, and let the user handle it (29 Sep).** Solutions must look clearly unlike Diagnosis and let the user see how much thought went into the answer. Drawn motifs, in blueprint ink, never clip art: the **lightbulb** (an idea reached), the **jigsaw** (parts that only work together), and, still to be designed, the maze (routes ruled out) and tangled wires made straight (work separated).
  - **Every Solutions drawing is interactive.** The user picks, lifts, opens or compares something on it, and the drawing answers. A drawing that only sits there is not enough.
  - **The first one is `puzzle`** (the five-part overview): the idea as the lit centre piece, five parts locked around it. Picking a piece lifts it, outlines the pieces it relies on, and opens its sheet underneath; "Ask Tojo about this part" writes the message into the chat box with its point attached.
  - Also drawn so far, all Solutions only: `knots` (the wait as a rope; pick parts to undo knots), `stake` (a drafting balance; the user sets the share won back), `route` (steps on a trail to doors into the next tabs), and, for the Automations tab to redraw, `untangle` and `maze`.
  - The first drafts of `maze`, `tangle` and `jigsaw` were rejected on 29 Sep (look, flow and no interaction) and removed.
  - Every motif carries real content from the spec. A motif with nothing to say is decoration, and is left out.
- **Scope.** Each block in a tab registry says `scope`: `all` (the pattern may be used by any tab, redrawn in that tab's look) or a tab name (that tab only). The block library shows the scope, so any generator reading it knows which templates it may use.

### 1.4 Automations: the switch room

| Token | Value |
|---|---|
| Ground | pale steel `#E4E7EA` |
| Panels | `#F9FAFB` |
| Ink | charcoal `#1C2A33` |
| Muted text | `#4B5963` |
| Switched-on teal | `#0F6E6B` |
| Light teal | `#8FD3CD` (fills and text on charcoal only) |
| Not-built grey | `#8C98A0` (borders only) |
| Waiting amber | `#8A5608` |

- **Panels:** rounded, 10–16px corners.
- **Labels:** sentence case.
- **Signature elements:**
  - **drawn switches:** track and knob, off, testing or switched on;
  - **the main switch:** the one prerequisite every automation waits on;
  - **wires** from one bus;
  - **the overnight arc** from 6 PM to going home;
  - **signal bars** from idea to switched on.
- **Teal means switched on,** and nothing else, on steel panels.
- **Charcoal screens (29 Sep).** Where the drawing shows the machine at work, it sits on a charcoal screen (`#16222A`) and glows in light teal `#8FD3CD`. The glow means "Tojo is doing this", never "switched on".
- **The machine motifs (29 Sep).** Automations must look unlike Solutions and show the machine working with people. Drawn in the switch-room palette, never clip art, and each carrying real content:
  - **the helping hand:** a machine hand meeting a person's hand (gold) wherever a person approves (`nightshift`, `agent`);
  - **the invisible digital factory:** stations on one moving line through the night (`nightshift`);
  - **the digital brain and glowing network:** the facts of the stay flowing in and the summary filling (`brain`);
  - **the autonomous thinker and the holographic figure:** the agent's loop of notice, gather, check, draft and ask (`agent`);
  - **the friendly desk helper:** a small drawn bot for questions to the IT team (`helper`);
  - **drawn switches and lamps:** the records and where they come from (`sources`), and the relay to the bed desk (`relay`).
- **Every Automations drawing is interactive:** play, drag, flip, step through or pick, and the drawing answers.

### 1.5 Processes: the ward board

| Token | Value |
|---|---|
| Ground | pale heather `#ECE8EE` |
| Board | `#FCFBFD` |
| Ink | aubergine `#2A1E30` |
| Muted text | `#5A4D60` |
| Plum | `#6D4A77` |
| Light plum | `#E9C8F0` (rail text only) |
| Waiting amber | `#8A5608` |
| Measured green | `#2F6B4F` |

- **Buttons:** pill-shaped.
- **Board:** rounded, 14px.
- **Labels:** sentence case.
- **Signature elements:**
  - **magnet strips** on a white board;
  - **the three columns:** process changes, measures we watch, team and role changes;
  - **the trial strip** with week boxes;
  - **instrument readouts** for measures;
  - **seats** for roles, filled or empty;
  - **the loop:** plan, try on one ward, measure, adjust, spread.

### 1.6 Shades in the new tabs
- **Solutions, Automations and Processes each get a lighter shade** when their turn templates are designed. It is built the same way as mist: the same colours one step lighter, applied from the turn number.
- **Landing pages always use the tab's base shade.**

### 1.7 Contrast
- Every text pair in every tab and shade clears 4.5:1 for body text, and 3:1 for text 24px and larger. This is checked whenever a palette changes.
- **Colours for borders, rings and fills only.** The not-built greys (`#879689`, `#8C98A0`, `#9C92A1`) and the fill gold never carry text.

---

## 2. Type (the same in every tab)

| Use | Font | Rule |
|---|---|---|
| Titles, tab names, big numbers, stop letters | **Bebas Neue** | Turn title 60px desktop / 44px mobile. Landing tab name 48px / 42px. Landing claim 37–40px / 34px. Big values 44–48px desktop / 38px mobile in turns; 24–30px in landing pages. Never for sentences. |
| Everything else | **Poppins** | Body 15px (landing 14–14.5px). Labels 12–13px at weight 600. Question text 17–19px at 500. |
| Handwritten pointers and one-line notes | **Caveat** (700) | Only in `handnote`, "What people usually say" quotes, the `or` in a fork, and Tojo's Note in the chat. Never for data. |

- **Minimum sizes on mobile:** body 14px, labels 11px, small tags 10.5px. Content that does not fit reflows or collapses; **it never shrinks below these.**
- **Tojo's Note** (chat panel): Caveat 700, about 31px, gold `#d4a94f` on forest. No background, marker or underline (F4).
- **Fonts:** they load from Google Fonts with system fallbacks, and can be self-hosted. Previews embed the font files so they work offline.

---

## 3. Landing pages

### 3.1 Zones
Every landing page has the same five zones in the same order, whatever the tab:
1. **Masthead:** the emblem, the tab name, and the stamp with Refresh now.
2. **Where this stands:** the claim, with an optional one-line deck under it.
3. **Progress so far:** the tab's drawing.
4. **What Tojo still has to do.**
5. **The three buttons.**

Each tab draws the zones in its own look. The zones never change order, so a user moving between tabs always finds the same thing in the same place.

### 3.2 Shared parts (`landing-common/`)
- **The stamp:**
  - "Brought up to date at midnight, [date]";
  - how many conversations since then are not in yet;
  - a Refresh now button that at least 44px tall.

  After a refresh, it reads "Brought up to date just now, [time]". On a first visit it reads "Nothing to bring up to date yet".
- **The three buttons:**
  - They read Proceed with next step, Add more, and Jump to [tab], each with a one-line detail under it.
  - Proceed with next step is the filled, primary button. It carries a gold mark in every tab.
  - Each button is at least 52px tall.
- **Pending items:** a drawn marker, then the text. An item waiting on the user has a dashed amber marker and a short amber line saying what is needed.
- **First visit:**
  - The same zones, drawn as dashed outlines with a line saying what fills them.
  - Headline in muted ink.
  - Never a blank page.

### 3.3 The approved landing templates

| Tab | Template | Wide (desktop) | Narrow (mobile) |
|---|---|---|---|
| Diagnosis | C, Under the glass | 340px lens on the left, stages listed under it; evidence cards (2×2, gold pins) and pending items on the right; the three buttons in a row | 300px lens centred, stages under it; evidence 2 across; pending items; buttons stacked |
| Solutions | B, Iteration tracks | Title-block stamp; a sheet with one row per solution: name and latest revision, a 4-stop track, and dots for what it depends on; pending items and the buttons side by side | Each solution stacked: name, revision, then the track with its stop names shown, then the dots; the column headings hidden |
| Automations | B, Overnight arc | Arc on the left, marked 6 PM to 2 PM, overnight in charcoal and the day in grey; numbered markers at the hour each runs; the main-switch gate and the key on the right | Arc full width, then the gate, then the key |
| Processes | A, Ward board | One white board with three columns and a charcoal trial strip across the foot | Columns stacked; the trial strip without its week boxes |

The unchosen samples (Diagnosis A and B, Solutions A and C, Automations A and C, Processes B and C) are kept in the same `landing.py` files and are not built into production landing pages. Their elements are listed in `landing-common/landing-elements.json` and shown in the block library as **variations**, ready to be used as patterns in turns.

---

## 4. Two layouts, one markup

Each block and landing template has two layouts:
- **wide,** for a canvas at least 700px across;
- **narrow,** for a canvas under 700px across.

The switch is a CSS container query on the canvas itself. One HTML file serves both, and the same file can sit in a desktop pane or a phone column.

**The same components are reflowed, never shrunk** (F6). Mobile shows the same stops, boxes, gauges and tags, in the same order and the same visual language, rearranged for the width.

| Diagnosis block | Wide | Narrow |
|---|---|---|
| route-map | Serpentine line with 6 stops per row, and a detail panel under the map | Vertical line; the selected stop opens inline beneath itself |
| chain | Row, wrapping | Vertical stack; the arrows turn downward |
| two-flow | Label column plus two height-matched columns | Per row: the label, then both cells stacked, each tagged with its column name |
| compare-table | Grid, with options as columns | One card per option, with the same attributes |
| stat-strip | 1–4 across | 2 across |
| calculator | Inputs next to the working | Inputs above the working |
| gauges, cards, agenda | Across | Stacked |
| balance | 380px beam | 250px beam, same drawing |
| time-window | One line across the day, moments above, unused hours shaded | Vertical timeline; unused hours as a shaded block between two moments |
| hour-load | Vertical bars per hour, busy windows bracketed with their staff | Sideways bars, grouped under each busy window, then "Other hours" |
| was-now, scorecard | One row per figure or measure, in columns | One card per figure or measure |
| narrow-claim | Their words, then what changes and what stays side by side, then the ask | The same, stacked |
| converge | Sources in a row, one rail, one arrow to the result | Sources stacked on a rail down the left, arrow into the result |
| bands | What goes in → the engine → what comes out, in three columns | Stacked; the arrows turn downward |
| shared-flow | Chain with the one-flow step dashed and a bypass arc over it | Vertical; the one-flow step tagged, no arc |
| zoom-trail | Arrow-shaped steps across | Indented list, one level per line |
| phases | Bars on one week scale, with decision lines through every row | One row per phase with its own bar; week numbers only |

**Rules for both layouts:**
- **Vertical scroll only.** Nothing may cause sideways scroll at a 360px canvas width. The build check renders at 362px (390px for landing pages in the phone shell) and fails on overflow.
- **When a structure truly cannot reflow** (the serpentine map), the block renders two structures from the same data (`.tj-desk` and `.tj-mob`), and keeps their interaction state in sync.

---

## 5. Visual grammar (every tab)

The grammar is fixed and reused rather than reinvented. Before adding a colour, check whether an existing one already carries the meaning. Each tab maps these meanings onto its own palette (§1).

### 5.1 Border colour carries state. Only five states exist.

| State | Meaning | Diagnosis | Other tabs |
|---|---|---|---|
| `plain` | Confirmed or unchanged | Forest border | The tab's ink |
| `target` | A goal, not yet measured, or needs attention | Amber | Waiting amber |
| `outcome` | The headline result; its value turns red too | Red | Red, where a result is shown |
| `start` | Where to begin | Green | Gold "now" mark |
| `dashed` | Exists on only some paths, or not built yet | Dashed | Dashed |

**Every tab also shares these four markers:**
- **Now or next:** gold, in every tab.
- **Done, agreed or walked:** filled with the tab's ink.
- **Waiting on the user:** dashed amber, with words saying what is needed.
- **Not started or not built:** a dashed grey outline.

### 5.2 Fill says what kind of box it is
- **Process-step boxes share one fill.**
- **Effect boxes** (a figure, a result or a condition, anything that is not a step) take a visibly different light fill, a strong value colour and a dark label, so they read as a different kind of object at a glance.

### 5.3 A muted fill means present but not the subject
- Use it for items being listed rather than acted on.
- **Dim the text along with the box.** Dimming only the box does not work, because the text stays at full weight and the box still reads as lit.
- Drop the fill close to the ground, lighten the border, and step the text down with it.
- Then check the dimmed text still clears 4.5:1. Muted means receded, never hard to read.

### 5.4 Marks and dividers
- **Stop status** (route-map, progress-trail, lens rim, tracks):
  - `now`: gold fill;
  - `done`: ink fill;
  - `next`: ink ring with a gold halo;
  - `later`: pale ring;
  - `flag`: red ring.
- **Tags** carry a short state label on a box, such as where to begin or the biggest hold-up. A tag takes its box's state colour; a green tag on an amber box reads wrongly.
- **Source tags** on figures: *Your number* (solid green); *Worked out from yours*, *Tojo's guess*, *Example only* or *Goal* (dashed gold); *Need from you* (dashed red).
- **Status badges:** a tick or a cross per step, each with a short caption. They turn a process drawing into a keep-or-change verdict without a second visual language.
- **A dashed divider with an italic caption** holds the point that spans a whole structure rather than one step: the condition a number rests on, the benefit that is not a number, or the split between two phases.

### 5.5 Arrows and cards
- **Arrows only between things in sequence.** Cards for independent items never have arrows between them.
- **Nothing sits between an arrowhead and the thing it points at.** A label under an arrow makes the arrow point at the label, so labels go above the band they introduce.
- **Several inputs feeding one thing:** draw a rail across all the inputs and one arrow from its centre. Never draw an arrow rising from the gap between two boxes.

**Don't add a sixth state or a new colour** before checking that the existing ones cannot carry the meaning.

---

## 6. Interaction

- **Expanders** are native `<details>` and `<summary>` elements, so they work with no JavaScript: in the app, on the design canvas and in any preview.
  - Detail is collapsed by default, behind a pill button with a chevron.
  - Collapsed content does not count against the one-screen budget.
- **An expander button says what it opens:** "See what it does", "See the roles", "See what we'll track". It opens to 2–6 real points (`more_points`), optionally led by one line (`more`). A generic label like "More", or a button that opens to one thin line, is not allowed (F8).
- **Pickers.** In route-map, one stop is open at a time, and "now" is open by default. The picked stop gets a gold ring.
- **Calculators** recalculate on input. `needed` inputs are empty fields with a dashed red border. Until they are filled, results show "—" and a waiting line.
- **Point links.** Any item can carry `point: N`. When the user selects @PointN in the chat, the app calls `tojoCanvas.lightPoints(canvas, [N])` and the item gets a 4px gold outline. On landing pages the same link is the `data-pt` attribute.
- **Landing buttons:**
  - Refresh now updates the stamp in place.
  - The three buttons hand their action to the app.
  - In previews, the buttons fill the chat input instead.
- **Touch and keyboard.** Every interactive element is a real `<button>` or `<input>`, at least 40×40px (44px for Refresh now, 52px for the landing buttons), with a visible gold focus ring.
- **Offline-safe.** Blocks use plain CSS and a small vanilla JS runtime, with no frameworks and no network calls.

---

## 6b. Words inside blocks

- **Every built-in label is plain English** (F7).
- **Source tags** read *Your number*, *Worked out from yours*, *Tojo's guess*, *Example only*, *Goal* and *Need from you*.
- **Route stops** say *What people usually say*, not "Heard as".
- **Number formats write units in full:** *5 hours*, *₹32,000*, *₹10.3 crore*, *₹4.5 lakh*.
- **Landing labels** are the same in every tab: *What Tojo still has to do*, *Proceed with next step*, *Add more*, *Jump to [tab]*, *Refresh now*.
- **A new block or template may not introduce a label** that fails the registry's `plain_english` list.

---

## 7. Accessibility floor

- **Contrast:** text is at least 4.5:1 for body text and 3:1 for 24px and larger, in every tab and shade (§1.7).
- **Colour never carries meaning alone.**
  - Stop status has a text label in the detail, the legend or hidden text for screen readers.
  - Source tags carry words.
  - Switch and seat states have hidden text labels.
- **Drawings that carry meaning have text equivalents** in labels or `aria-label`. That includes the balance, gauges, the lens rim, the overnight arc, signal bars and seats.
- **Motion respects `prefers-reduced-motion`.** Nothing animates for users who turn motion off.

---

## 8. Build discipline

- **Render it and look at it before review, every time.** The browser checks measure real heights and sideways overflow at both widths, and take screenshots:
  - `tests/check_turns.py` for turns;
  - `landing-common/measure.py` for landing pages.

  An estimate is never the final word.
- **Size every container from its content, never from a fixed number.** The recurring failure is a fixed height meeting content that varies: a second value line, a wrapped caption, a tag.
- **Leave room for the real font.** A local render can use a narrower fallback font than the one that reaches the reader, so a line that just fits can still overflow. Allow a margin from the first draft, and check long single words against their box.
- **Regenerate from the generator, never from a delivered file.** Delivered HTML is an output, not a source. Change the template, then rebuild.
- **Stretch the size for dense content; never cut content** to hit a size.

---

## 9. Adding or changing a block or template

1. **Why?** A `block_request` from real turns, or feedback on an existing block.
2. **Add or update the registry entry:**
   - **Turn blocks:** in the tab's registry (for Diagnosis, `blocks/registry.json`) with `id`, `version`, `status: draft`, `category`, `purpose`, `use_when`, `avoid_when`, `slots` with word limits, `mobile` and `cost`.
   - **Landing templates:** in `landing-common/landing-registry.json`.
3. **Write the renderer in the tab's own generator,** using only that tab's palette (§1). A structure borrowed from another tab's element (for example the switchboard used in Processes) is redrawn in this tab's look, never copied with its colours. Include CSS for both layouts and any behaviour.
4. **Add sample content.** For Diagnosis it goes in `blocks/samples.json`; for landing templates, in the `DATA` of `landing.py`. Include a first-visit version of every landing template.
5. **Build it and check it at both widths:** no overflow, nothing below the minimum sizes, contrast checked, and nothing that reads as software.
   - Diagnosis: `python3 diagnosis_html.py gallery`.
   - Landing pages: `python3 build_landing.py`, then `python3 measure.py`.
6. **Submit it for review.** It stays `draft` until the user approves it (06 §13). Approved work goes to both the library page and the design canvas.
7. **Changing an approved block's slots is a new `version`.** Old specs must still validate, or the change needs a migration note in `CHANGELOG.md`.
