# Length of Stay

The sixth Tojo tool, and the third and last **Financial Tool** (after Supply Chain and Procurement and Revenue & EBITDA). It covers every kind of stay: the wait in Emergency for a bed, days in the ICU, in step-down and on the wards, and the hospital as a whole. It sits in the Financial domain because every extra day is a bed someone else waits for and a day the hospital pays for, often inside a fixed-price package.

It uses the Financial look approved for Supply Chain and Procurement (the V skin in `../Supply Chain Procurement/skins.py`: Virevo type unchanged, flat frame, report sheet, ledger paper, receipt) and changes only its colours.

No domain reference file yet. Every figure is made up for an example 250-bed hospital and marked Example only or Tojo's guess:

| Area | Now | Goal | Extra a month | Cost of the extra |
|---|---|---|---|---|
| Emergency, wait for a bed | 5 hours 10 minutes | 4 hours | about 14 patients a day wait longer | — |
| ICU | 4.8 days | 3.5 | about 180 days (₹45,000 a day) | ₹81 lakh |
| Step-down | 2.9 days | 2 | about 220 days (₹22,000 a day) | ₹48 lakh |
| Wards | 4.1 days | 3.5 | about 900 days (₹9,000 a day) | ₹81 lakh |
| Whole hospital | 4.6 days | 3.9 | about 1,300 days | about ₹2.1 crore |

About 43 beds a day are held by patients ready to go home.

## Status (8 Oct 2026)
**Home page approved: A, the patient's path.** The four place pages (`places.py`), using ideas from the samples not chosen (B the bed board, C the stay chart and monitors). Review page `out/landing/length-of-stay-landing-pages.html`. **All five approved (8 Oct). In the block library (version 13)** under Financial Tools, added by `los_library.py` (also called by `build_block_library.py` after `rev_library.py`).

| Page | Drawing | Colours (ground · ink · highlight) |
|---|---|---|
| Home | **The patient's path** (approved A) | Aqua `#DFEFEE` · petrol `#0B2F3A` · coral red `#FF6F61` |
| Diagnosis | **One patient's chart**: one typical stay (9 days, the care needed 7) as a strip of days by area with the extra hatched, then each step as a chart line (when, where, what happened, the extra), its box beside the chart; the 1,300 extra days split by cause, one square per 13 days | Pale rose `#F7E4E1` · deep cobalt `#14246B` · spring green `#5EE08A` |
| Solutions | **The beds we get back**: one ruled entry per fix, its four stops, days freed a month, the beds that gives back every day drawn as beds; double-ruled total (about 600 days, about 20 beds, about ₹1 crore a month) | Pale lemon `#F6F3D4` · graphite `#20242B` · magenta `#F06BD0` |
| Automations | **The hospital's day**: a 24-hour clock face, night shaded, each helper at its hour; one bedside monitor per helper showing what it would put up | Pale butter `#F4EFD9` · ox-blood `#3A1016` · monitor yellow `#FFD43B` |
| Processes | **The week on the bed board**: a whiteboard week with each change as a magnet on its days, the new role (Patient Flow Lead) and a two-month trial; who owns the flow in each area, Emergency to home; the numbers we watch, now and plan | Whiteboard `#EFEDE6` · indigo `#1C1E4F` · marker cyan `#39C6EC` |

All 20 pages pass `qa.py`; every text pair clears 4.5:1. The rail carries each place's ground on every page.

### Round one: the home page in three looks (`los_landing.py`)
Review page `out/landing/length-of-stay-home-samples.html`.

| Look | The stay | The four parts of the work | Colours (ground · ink · highlight) |
|---|---|---|---|
| **A · The patient's path** | The stay as a route through the hospital: Emergency → ICU → step-down → wards → home; each stop with its days now against the goal, the extra days and what they cost; double-ruled total | One patient wristband per part: snap, label, one day box per step, status, barcode | Aqua `#DFEFEE` · petrol `#0B2F3A` · coral red `#FF6F61` |
| **B · The bed board** | Today's 250 beds as a grid, area by area: in use, held by patients ready to go home, Emergency patients waiting, free | One bed per part on the ward's bed board: bed number, day of stay as steps done, plan | Whiteboard `#EFEDE6` · indigo `#1C1E4F` · marker cyan `#39C6EC` |
| **C · The stay chart** | One average stay as days needed (ink) and extra (highlight), area by area, the Emergency wait beneath | One bedside monitor per part: reading = steps done, a trace climbing one step per step done, a dot where the work is now; screen off when not started | Pale butter `#F4EFD9` · ox-blood `#3A1016` · monitor yellow `#FFD43B` |

All 12 pages pass `qa.py`; every text pair clears 4.5:1; plain English checked by `sc_common.plain_check` (no "bed-days", "ALOS" and the like).

## What is where
| Path | What it is |
|---|---|
| `los_landing.py` | The home page words (one set for every look) and the three drawings A, B, C. Loads `sc_common`, `skins`, `landing2`, `landing3` from `../Supply Chain Procurement`. |
| `places.py` | The five landing pages: home (A) and the four places. Pages `los-<home\|diagnosis\|solutions\|automations\|processes>.<desktop\|mobile>.<filled\|empty>.html`. |
| `los_library.py` | Adds this tool's section to the block library under Financial Tools (`python3 los_library.py LIB OUT`); needs the Revenue & EBITDA section there first. |
| `qa.py` | Browser check (Playwright), `QA_GLOB` default `los-*.html`. |
| `shot.py` | Screenshots of whole canvases for review. |
| `out/landing/` | The review page and each page as `los-home-<a\|b\|c>.<desktop\|mobile>.<filled\|empty>.html`. |

## Build
```bash
python3 los_landing.py   # round one samples
python3 places.py        # the five landing pages
python3 qa.py
```
Needs `../Supply Chain Procurement`, `../Bed Management` and `../Common Elements` beside this folder.
