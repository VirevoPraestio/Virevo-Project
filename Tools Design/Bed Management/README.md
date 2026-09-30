# Bed Management

The second Tojo tool. Hospital for every turn: **the 300-bed super-specialty hospital in Nagpur** from the approved practice conversation (`references/bed-management-sample-chat-transcript.md`). Shared rules, generators and the one block library live in `../Common Elements`; this folder holds only what is Bed Management's own.

## What is where

| Path | What it is |
|---|---|
| `bm_common.py` | The Bed Management app shell, stamp, buttons, bed mark and v3 selection. Points at `../Common Elements`. |
| `home/home.py`, `diagnosis/`, `solutions/`, `automations/`, `processes/` | Each page's look and data. `home_v1_samples.py` and the A/B/C drawings are the samples not chosen. |
| `v3.py` | Draws the five approved landing pages (home B ward plan, Diagnosis B morning count, Solutions B corridor of fixes, Automations C station panel, Processes B trial ward). `qa_v3.py` checks them. |
| `diagnosis-html-generator/bm_diagnosis_html.py` | The Diagnosis turn generator. Draws with the universal blocks in Bed Management colours, plus the common tool layer. `registry.json` lists what it may use; `check.py` is the browser check. |
| `examples/diagnosis/` | Turn specs. `turns.json` lists the approved turns. `make_bm_dg_01.py` writes the three samples of turn 1. |
| `references/` | The approved transcript (turns 1–31). |
| `out/` | Built files: `landing/approved/` (the five pages), `diagnosis/bm-dg-01-samples.html`. |
| `archive/` | The rejected first Diagnosis generator and its 11 turns, and older scripts. Do not reuse. |

## Build

```bash
python3 v3.py                                                   # landing pages
cd diagnosis-html-generator
python3 bm_diagnosis_html.py samples ../examples/diagnosis/bm-dg-01-{A,B,C}.json -o ../out/diagnosis/bm-dg-01-samples.html --pages ../out/diagnosis/pages
python3 check.py ../out/diagnosis/pages
cd "../../Common Elements/library" && python3 build_block_library.py   # the one library
```

## Where it stands (30 Sep 2026)
- Landing pages: all five approved.
- Diagnosis turns: **bm-dg-01 approved, Sample A (the day on one line)**, from transcript turn 7. B and C are kept as variations.
- Next: transcript turn 8 (the five areas and the first question), in three samples. Then 9 to 16, and the missing diagnosis turn from the playbook §2.
- Landing pages still carry the Bhubaneswar example figures; to be moved to Nagpur.
