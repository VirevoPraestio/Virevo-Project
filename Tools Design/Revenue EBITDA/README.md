# Revenue & EBITDA

The fifth Tojo tool, and the second **Financial Tool** (after Supply Chain and Procurement). It uses the Financial look approved for Supply Chain and Procurement (the V skin in `../Supply Chain Procurement/skins.py`: Virevo type unchanged, flat frame, report sheet, ledger paper and receipt) and changes only its colours.

There is no domain reference file yet. Every figure is made up for an example 250-bed hospital and marked Example only or Tojo's guess: money in about ₹18 crore a month; costs (staff ₹7.6 crore, medicines and supplies ₹4.9 crore, doctors' fees ₹2.2 crore, rent, power and upkeep ₹1 crore); about ₹2.3 crore left, about 13 of every 100 rupees; goal 18; about ₹90 lakh a month short.

## Status (8 Oct 2026)
**All five landing pages approved** (home: A, the cheque book; the four places in `places.py`). **In the block library (version 12)** under Financial Tools, added by `rev_library.py` (also called by `build_block_library.py` after `scp_library.py`).

| Page | Drawing | Colours (ground · ink · highlight) |
|---|---|---|
| Home | **The cheque book** (approved A) | Banknote green `#E4ECE3` · bottle green `#0C2E26` · marigold `#F2B233` |
| Diagnosis | **The bank statement**: ₹1,000 of bills followed to the bank, each step a statement line (day, lost, left), its box beside the statement; the ₹90 lakh gap split four ways on a ring | Peach `#F7E6DC` · deep plum `#3A1430` · electric blue `#5B8CFF` |
| Solutions | **The payback sheet**: one ruled entry per fix, its four stops, cost to start, money back a month, a 12-month strip marking the month it pays for itself; double-ruled total | Pale olive `#ECEED9` · deep teal `#0E3B3A` · tangerine `#FF9A2E` |
| Automations | **The bill's road**: patient leaves → bill closed → claim sent → insurer pays → money in the bank → next morning → month end, each helper hung at its stop; one card per helper with the note it would send | Ice blue `#E1ECF7` · navy `#0D2240` · hot pink `#FF5C93` |
| Processes | **The money rhythm**: daily, weekly, monthly and new-role lanes with the changes in them and a two-month trial; who owns each line of the profit and loss; the numbers we watch, now → plan | Orchid pink `#F2E6F0` · aubergine `#2E1A2C` · sea green `#2EC4A6` |

All 20 pages pass `qa.py`; every text pair clears 4.5:1. The rail carries each place's ground on every page.

### Round one: the home page in three looks (`rev_landing.py`)

| Look | The month's money | The four parts of the work | Colours (ground · ink · highlight) |
|---|---|---|---|
| **A · The cheque book** | Profit and loss on ledger paper, double-ruled line for what is left | One cheque per part, made out for what it brings back; a counterfoil ticks its steps; a signature line for when it is agreed | Banknote green `#E4ECE3` · bottle green `#0C2E26` · marigold `#F2B233` |
| **B · The results board** | Twelve months of what is left from every 100 rupees, against a dashed goal line | One results card per part: a ring of steps done, a step bar, the gap found or what it could bring back | Periwinkle `#E8EBF6` · midnight `#121A3A` · growth green `#35D088` |
| **C · The coin stacks** | A bridge from money in, cost by cost, to what is left | One stack of coins per part, one coin per step | Blush cream `#F4ECE6` · aubergine `#2A1B37` · teal `#22C1B0` |

All 12 pages pass `qa.py` (sideways scroll, the word "tab", text outside its box, script errors, phone picks stacked, picking, height). Plain English checked by `sc_common.plain_check` (EBITDA is the tool's own name and is explained once in the deck).

## What is where
| Path | What it is |
|---|---|
| `rev_landing.py` | Round one: the home page words and the three drawings A, B, C (A approved). Named so it does not clash with `../Supply Chain Procurement/landing.py`. Loads `sc_common`, `skins`, `landing2`, `landing3` from there. |
| `places.py` | The five landing pages: home (A) and the four places. Review page `out/landing/revenue-ebitda-landing-pages.html`; pages `rev-<home\|diagnosis\|solutions\|automations\|processes>.<desktop\|mobile>.<filled\|empty>.html`. |
| `rev_library.py` | Adds this tool's section to the block library under Financial Tools (`python3 rev_library.py LIB OUT`); needs the Supply Chain and Procurement section there first. |
| `qa.py` | Browser check (Playwright). |
| `out/landing/` | `revenue-ebitda-home-samples.html` (review page) and each page as `rev-home-<a|b|c>.<desktop|mobile>.<filled|empty>.html`. |

## Build
```bash
python3 rev_landing.py   # round one samples
python3 places.py        # the five landing pages
python3 qa.py
```
Needs `../Supply Chain Procurement`, `../Bed Management` and `../Common Elements` beside this folder.
