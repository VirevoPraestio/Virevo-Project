# Discharge Process: the regenerated turns (5 Oct 2026)

All 32 Discharge Process turn templates, redone with the latest generators. The old repo (`tojo-html/`) is left as it was; its turn
templates are superseded by these and no longer appear in the block library.

## What changed
- **Latest generators.** Each place has a generator here that loads the Bed Management generator for that place as its own copy and points
  it at Discharge (`dp_common.py`): its own registry (colours, backgrounds, blocks, the three buttons), the Discharge app shell
  (250-bed hospital, Bhubaneswar) and, where needed, its own drawings. Nothing in Bed Management changes.
- **Every turn looks different.** One main drawing per turn, never repeated in a place (the filled timesheet, a redraw, is the one exception).
- **Plain, simple English** everywhere, checked by the generator (sentences under 21 words, no joining dashes, plain words).
- **The three buttons** on every turn: Proceed with next step, Add more, Jump to the next place (Diagnosis → Solutions → Automations →
  Processes → Diagnosis).
- **Interactivity in the HTML.** The first item is raised with its sheet open; on a phone every item is stacked with its sheet right under it;
  entries typed in the drawing are added to the chat message, never replacing one another.
- **Background every four turns**, by turn number within the place.

## The places
| Place | Generator | Look | Turns |
|---|---|---|---|
| Diagnosis | `diagnosis-html-generator/dp_diagnosis_html.py` | the case sheet: sage, forest ink; then the night round | dp-dg-01 to 03 |
| Solutions | `solutions-html-generator/dp_solutions_html.py` | the blueprint: blue-grey, navy, grid; then tracing paper | dp-so-01 to 07 |
| Automations | `automations-html-generator/dp_automations_html.py` | the switch room: steel, charcoal, teal; then the night shift | dp-au-01 to 08 |
| Processes | `processes-html-generator/dp_processes_html.py` | the ward board: heather, aubergine, plum; then the night board | dp-pr-01 to 14 |

Processes had no layered generator before. It is a copy of the Solutions generator pointed at Processes, drawing the library's Processes motifs
layered (`dp_pr_blocks.py`: ward-board heading, swap, trial, badges, seats, readouts, loop, and the new timesheet and night lanes) and the
layered Solutions drawings that fit process work (people, sizing, gauges, owners, findings, circuit, notes).

New Discharge drawings: `ward-map` (Diagnosis), `file` (Automations), and the nine Processes drawings above.

## Where each turn came from
Each spec records `turn.was`: the old template it replaces. Diagnosis = sample turns 1–3; Solutions = sample turn 4, then so-01 to so-06;
Automations = sample turn 5, then au-01 to au-07; Processes = sample turns 6–12, then pr-01 to pr-07.

## Build and check
```bash
cd examples/<place> && python3 make_dp_<place>.py                         # writes the specs and turns.json
cd ../../<place>-html-generator && python3 dp_<place>_html.py build        # out/<place>/<place>-turns.html and pages/
python3 check.py ../out/<place>/pages                                      # browser checks
```
Needs the `Bed Management` and `Common Elements` folders beside this one. Standard library only (Playwright for check.py).

All 32 turns are drafts awaiting review. They are in the one block library (Common Elements/ARTIFACTS.md), canvases only.
