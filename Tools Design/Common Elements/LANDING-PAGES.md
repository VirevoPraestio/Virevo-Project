# Tab landing pages — rules and samples (28 Sep 2026)

## What a landing page is
Every tab (Diagnosis, Solutions, Automations, Processes) has its own landing page: a summary of the progress so far in that tab and what Tojo still has to do.
Processes covers three things: process changes, the measures we watch (KPI monitoring), and team and role changes.

The Discharge Process tool's own landing page is the first page already built. On first load it shows exactly as it is now and is not generated. On later visits it fills in with what has happened so far.

## When it shows
- **Clicking a tab** shows that tab's landing page. On a first visit it is the first thing in the tab. If the tab has been used before, it comes after the last response in that tab.
- **Automatic refresh:** every page is brought up to date every night at midnight.
- **Refresh now:** every page has this button, so the user can pull in conversations since the last update without waiting for midnight.
- **Filling in from other tabs:** a page fills in from conversations in any tab, not only its own. For example, Solutions fills in as Diagnosis progresses.
- **First visit:** the page is unfilled. Each zone shows an empty outline of what will appear there, and says what fills it.

## What every page carries, in this order
1. **Masthead:** the tab's emblem and name, and the update stamp. The stamp says when the page was last brought up to date and how many conversations since then are not in yet. It also holds the Refresh now button.
2. **Where this stands:** one plain sentence.
3. **Progress so far:** the tab's own drawing.
4. **What Tojo still has to do:** items that need a figure or an answer from the user are marked.
5. **Three buttons, always in this order:**
   - Proceed with next step (it names the step)
   - Add more
   - Jump to the next tab. The order is Diagnosis → Solutions → Automations → Processes, and Processes jumps back to Diagnosis.

## What stays the same, and what differs
- **The chat panel is unchanged:** text, pointer, Tojo's Note, @Points and three predictive prompts. @Points light up the matching items on the page.
- **Same everywhere:** the typography (Bebas Neue, Poppins, Caveat), plain English (F7), the one-screen desktop budget (824px of canvas), and mobile reflowing rather than shrinking (F6).
- **Different per tab:** each tab has its own generator folder with its own look, elements and templates.
  - `diagnosis-html-generator/` keeps the current house style: sage, uppercase labels.
  - `solutions-html-generator/` is a blueprint: grid, navy, revision triangles.
  - `automations-html-generator/` is a switch room: steel, charcoal, teal switches.
  - `processes-html-generator/` is a ward board: heather, aubergine, readouts, seats.
- **Shared parts:** `landing-common/` holds the parts every page shares: the stamp, the three buttons, the chat panel, the shell, and the design-canvas export.

## Samples for review
| Tab | A | B | C |
|---|---|---|---|
| Diagnosis | Route walked | Case sheet (pulse line) | Under the glass (lens) |
| Solutions | Drawing sheets | Iteration tracks | Revision log |
| Automations | Switchboard | Overnight arc | Signal bars |
| Processes | Ward board | Readouts and seats | The loop |

Build and check:
```bash
cd landing-common
python3 build_landing.py            # plain previews in out/landing/ (both states, desktop and mobile)
python3 measure.py                  # QA: page heights, sideways scroll, screenshots in out/landing/shots/
DC=1 python3 build_landing.py       # design-canvas artboards in out/landing/design-canvas/
```

All 12 fit the desktop budget. None scroll sideways at 390px.

The design canvas "Tojo — Tab Landing Pages" has all 24 artboards. Each artboard has a **state** switch (In progress / First visit) in its Tweaks, a working Refresh now button, @Points, and prompts that fill the input.

## Approved (28 Sep 2026)
| Tab | Approved template | Kept for reference |
|---|---|---|
| Diagnosis | **C, Under the glass**: the diagnosis inside a lens, the stages as its rim, evidence pinned beside it | A, B |
| Solutions | **B, Iteration tracks**: each solution travels idea, shaped, tested with you, agreed; revision marks and what-it-depends-on dots | A, C |
| Automations | **B, Overnight arc**: each automation placed at the hour it runs, 6 PM to going home, behind the software link | A, C |
| Processes | **A, Ward board**: changes, measures and roles in three columns, the trial strip across the bottom | B, C |

- **Where the picks are recorded:** `landing-common/landing-registry.json` records the picks and their feedback log.
- **What gets built:** `APPROVED=1 python3 build_landing.py` builds only the approved ones.
- **Changing a template:** a change to an approved template raises its version and goes back for review, the same loop as the blocks (07 §7).
