# Bed Management

The second Tojo tool. Hospital for every turn: **the 300-bed super-specialty hospital in Nagpur** from the approved practice conversation (`references/bed-management-sample-chat-transcript.md`). Shared rules, generators and the one block library live in `../Common Elements`; this folder holds only what is Bed Management's own.

## What is where

| Path | What it is |
|---|---|
| `bm_common.py` | The Bed Management app shell, stamp, buttons, bed mark and v3 selection. Points at `../Common Elements`. |
| `home/home.py`, `diagnosis/`, `solutions/`, `automations/`, `processes/` | Each page's look and data. `home_v1_samples.py` and the A/B/C drawings are the samples not chosen. |
| `v3.py` | Draws the five approved landing pages (home B ward plan, Diagnosis B morning count, Solutions B corridor of fixes, Automations C station panel, Processes B trial ward). `qa_v3.py` checks them. |
| `diagnosis-html-generator/bm_diagnosis_html.py` | The Diagnosis turn generator. Draws with the universal blocks in Bed Management colours, plus the common tool layer. `registry.json` lists what it may use; `check.py` is the browser check. |
| `diagnosis-html-generator/bm_blocks.py` | Bed Management's own drawings (11, all approved 1 Oct): lens, day-strips, admission-route, stopwatch, bed-bills, receipt, bed-count, evidence-board, rule-loop, scale, corridor. Also in the one library. |
| `examples/diagnosis/` | Turn specs. `turns.json` lists the turns in order. `make_bm_dg_01.py` writes the three samples of turn 1; `make_diagnosis_turns.py` writes turns 2 to 12. |
| `solutions-html-generator/bm_solutions_html.py` | The Solutions turn generator: the library's Solutions renderers and motifs in the fit-out look, the common tool layer, and the three buttons on every turn. `bm_so_blocks.py` and `bm_so_blocks2.py` hold the 19 drawings, `registry.json` lists them, `check.py` is the browser check. |
| `examples/solutions/` | Turn specs. `make_bm_so_01.py` writes the three samples of turn 1 (all approved as templates; A is the turn); `make_solutions_turns.py` writes bm-so-02 to 12 and `turns.json`. |
| `processes-html-generator/bm_processes_html.py` | The Processes turn generator: a copy of the Solutions generator pointed at Processes, in the trial ward look (pale clay, deep brown, rust). Layers the library's Processes motifs (loaded from `../Discharge Process/processes-html-generator/dp_pr_blocks.py` as a private copy) and its own five drawings in `bm_pr_blocks.py`. `registry.json` lists them, `check.py` is the browser check. |
| `examples/processes/` | `make_processes_turns.py` writes bm-pr-01 to 11 and `turns.json`. |
| `references/` | The approved transcript (turns 1–31). |
| `out/` | Built files: `landing/approved/` (the five pages), `diagnosis/bm-dg-01-samples.html`, `diagnosis/diagnosis-turns.html` (all twelve turns stacked) and `diagnosis/pages/`. |
| `archive/` | The rejected first Diagnosis generator and its 11 turns, and older scripts. Do not reuse. |

## Build

```bash
python3 v3.py                                                   # landing pages
cd diagnosis-html-generator
python3 bm_diagnosis_html.py samples ../examples/diagnosis/bm-dg-01-{A,B,C}.json -o ../out/diagnosis/bm-dg-01-samples.html --pages ../out/diagnosis/pages
python3 bm_diagnosis_html.py build                            # turns 1-12 stacked
python3 check.py ../out/diagnosis/pages
cd ../solutions-html-generator && python3 bm_solutions_html.py build && python3 check.py ../out/solutions/pages
cd "../../Common Elements/library" && python3 build_block_library.py   # the one library
```

## Where it stands (1 Oct 2026)
- Landing pages: all five approved.
- **Diagnosis: all twelve turns approved** (bm-dg-01 to 12, transcript turns 7 to 17 plus the playbook's diagnosis turn). `out/diagnosis/diagnosis-turns.html`.
- **Solutions: all twelve turns approved, 1 Oct.** bm-so-01 (transcript 18): three samples approved as templates, Sample A (six switches, one bulb) is the turn. bm-so-02 to bm-so-12: transcript turns 19 to 23 and 26 to 31 (24 and 25 were superseded in the record by 27 and 28). `out/solutions/solutions-turns.html`.
- Turns 1–4 and 9–12 use the place's base background, 5–8 the second (count/lamp in Diagnosis, fit-out/plan paper in Solutions). No two turns share a main drawing; the generators check it.
- **Every Solutions turn ends with the three buttons** (Proceed with next step, Add more, Jump to Automations); rules/08 §8. The Diagnosis turns carry them too since 5 Oct 2026 (`examples/diagnosis/dg_actions.py`).
- **Where Solutions ends:** transcript turn 31, the first step. Automations starts when the build itself is detailed ("How would the build work?").
- The one block library holds every Bed Management landing page, Diagnosis, Solutions and Automations turn and drawing (republished 5 Oct, version 7). Discharge Process now draws its turns with these generators too (see `../Discharge Process/README.md`).
## Automations turns (approved 6 Oct 2026)
- Generator: `automations-html-generator/bm_automations_html.py` (library Automations renderers in the station-panel look, plus `bm_au_blocks.py` and `bm_au_blocks2.py`). `check.py` is the browser check. Build: `python bm_automations_html.py build`.
- bm-au-01 ("How would the build work?", after transcript 31): Sample B is the turn (the engine through one day); A (switchboard) and C (build panel) are approved templates.
- bm-au-02 to bm-au-07, one drawing each: helper (what IT does), relay (why discharge first), agent (how beds freeing are predicted), sources (records on paper; night background from turn 5), nightshift (after the 6 PM freeze), panel (what switches on first). Stacked in `out/automations/automations-turns.html`.
- **Where Automations ends:** bm-au-07. Process changes, people, team changes and KPIs are only named there (prompts and the jump); the move to Processes comes when one of them is detailed.
- Approved by Avishek on 6 Oct 2026, with all 32 regenerated Discharge turns; library version 8 marks them approved.
- Landing pages still carry the Bhubaneswar example figures; to be moved to Nagpur.

## Processes turns (approved 6 Oct 2026)
- Generator: `processes-html-generator/bm_processes_html.py`. Build: `python3 bm_processes_html.py build`, then `python3 check.py ../out/processes/pages`.
- The record stops at transcript 31, so the turns follow the prompts, from bm-au-07's "How does the day change on the wards?". Content only from bed-management.md §7.4.2 to §7.4.4 and §8, and transcript 22 to 31.
- One main drawing each, stacked in `out/processes/processes-turns.html`:
  bm-pr-01 day-dial (the ward's day on a wall clock, new) · 02 ward-pins (the trial ward from above, new) · 03 swap (the one rule that keeps the day late) ·
  04 round-cards (the doctor confirms or changes a likely date, new) · 05 loop (a date not given; evening background from here) · 06 slip (the OPD prescription pulled into the bed plan, new) ·
  07 badges (who must agree) · 08 seats (two managers, the desks, triggers as lamps) · 09 readouts (eight weekly measures; day background again) · 10 trial (two weeks on one ward) ·
  11 clipboard (what we need to start, typed in, new). The jump on every turn goes back to Diagnosis.
- Approved by Avishek on 6 Oct 2026 and added to the one block library (version 9), canvases only, with the five new drawings.
