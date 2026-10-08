# OPD Diagnostic Leak

The third Tojo tool. Domain reference: `tojo-v2 - Regular Chat/skill/virevo-hospital-ops/references/opd-diagnostic-leakage.md`.
Example hospital for now: the case study in that file's §0 (40 new and 400 returning outpatients a day; 1 in 10 new and 2 in 10 returning patients finish their tests here; about ₹1.5 lakh lost a day; about 5% of profit). Every other figure on the pages is marked Example only or Tojo's guess.

## Status (8 Oct 2026)
Landing pages drawn for review: the tool's home page and the four place pages. **Not approved yet. Not in the block library yet.**

## What is where
| Path | What it is |
|---|---|
| `odl_common.py` | Loads the Bed Management page parts (`../Bed Management/bm_common.py`) as a private copy and points them at this tool: name, hospital, colours, the plain-English check. |
| `landing.py` | Data and drawing for the five landing pages. |
| `qa.py` | Browser check: sideways scroll, the word "tab", text outside its box, script errors, phone picks side by side, picking. |
| `review_template.html` | The review page shell (desktop and phone side by side, both states). |
| `out/landing/` | `opd-diagnostic-leak-landing-pages.html` (review page) and each page as `odl-<page>.<desktop|mobile>.<filled|empty>.html`. |

## The five pages
| Page | Drawing | Colours (ground · ink · highlight) |
|---|---|---|
| Home | **The leak line**: a split top (the claim on the left, the leak meter on the right), then one pipe from the clinic to the test rooms, a valve for each part of the work that turns shut as it is done, and drops where tests still leave | Saffron `#F1E3B9` · warm black `#2B1E05` · vermilion `#E0502A` |
| Diagnosis | **The sieve**: 100 tests written, how many are left at each step and why each group drops out; the four possible main causes weighed below | Khaki `#E3E5C3` · olive black `#262B07` · magenta `#C92A6A` |
| Solutions | **The prescription pad**: one line per fix, its four stops as tick boxes, its by-hand and automatic versions side by side (opd §7.4 standing requirement) | Rose `#F3D9DE` · raspberry `#45102A` · turquoise `#0E8F89` |
| Automations | **One patient's visit**: the four helpers (opd §7.4.2) placed over the stations of a visit where they act | Apricot `#F7DCC2` · burnt umber `#3A1904` · cobalt `#2C57CC` |
| Processes | **The busy-hours board**: bills per hour against what the desk can make (peak-load method, opd §7.1 point 3), changes pinned under their hours, the numbers we watch, team and roles | Lagoon `#CDEBEB` · deep sea `#06323A` · orange `#E07F0C` |

The highlight takes the place of the shared gold in the other tools (raised edge, first button bar, emblem, rail). Same behaviour as Bed Management v3: chat one screen tall with its own scroll, header fixed, first element raised with its box open, phone boxes under each element, picks stacked, three buttons in order.

## Build
```bash
python3 landing.py      # writes out/landing/
python3 qa.py           # browser check (Playwright)
```
Needs `../Bed Management` and `../Common Elements` beside this folder.
