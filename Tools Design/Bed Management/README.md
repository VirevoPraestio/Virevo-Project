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
cd "../../Common Elements/library" && python3 build_block_library.py   # the one library
```

## Where it stands (1 Oct 2026)
- Landing pages: all five approved.
- **Diagnosis: all twelve turns approved.** bm-dg-01 Sample A (the day on one line), from transcript turn 7; B and C kept as variations. bm-dg-02 to bm-dg-12 approved 1 Oct: transcript turns 8 to 17, plus bm-dg-11 from the playbook §2. Each turn has a different main drawing; dg-05 and dg-07 are the filled redraws of dg-04 and dg-06.
- Every turn passes `check.py`: no sideways scroll, no word "tab", phone order, picks stacked on a phone, no text outside its box, two entries both reach the message.
- The one block library is rebuilt with these turns and the 11 drawings (republished 1 Oct).
- **Where Diagnosis ends:** naming the five parts (bm-dg-12, transcript 17) stays in Diagnosis. Solutions starts when one part is taken up (transcript 18, the automations part).
- Next: Solutions, from transcript turn 18, one turn at a time with three samples.
- Landing pages still carry the Bhubaneswar example figures; to be moved to Nagpur.
