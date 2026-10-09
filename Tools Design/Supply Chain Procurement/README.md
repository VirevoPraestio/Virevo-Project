# Supply Chain and Procurement

The fourth Tojo tool, and **the first tool of the Financial domain**. Discharge Process, Bed Management and OPD Diagnostic Leak are Hospital Operations tools.
There is no domain reference file yet. Example hospital for now: an example 250-bed hospital buying about ₹3 crore of supplies a month and losing about ₹20 lakh of it (paid above the best price ₹8 lakh, rushed buys ₹5 lakh, used but never billed ₹4 lakh, expired ₹3 lakh). Every figure is marked Example only or Tojo's guess.

## Status (8 Oct 2026)
**All five landing pages approved** (home: F, the notebook; the four places in `landing3.py`). **In the block library (version 11)** under Financial Tools, added by `scp_library.py`, which also groups the library into Response templates, Operations Tools and Financial Tools.

## The five landing pages (8 Oct 2026, for review): `landing3.py`
Avishek approved **F, the notebook, as the tool's home page**, and asked for the four place pages to use ideas from the other samples, each place different in colour and in elements. All five use the V skin (Virevo type, flat frame). Review page: `out/landing/supply-chain-landing-pages.html`; pages `scp-<home|diagnosis|solutions|automations|processes>.<desktop|mobile>.<filled|empty>.html`. All 20 pass `qa.py`; every text pair clears 4.5:1.

| Page | Drawing | Elements from | Colours (ground · ink · highlight) |
|---|---|---|---|
| Home | **The notebook** (approved F): receipt stapled on; parts on the left page, the open part on the right | F | Report white `#EEEEE9` · black `#0F1012` · lime `#C6E43F` |
| Diagnosis | **The item's receipt**: 100 IV cannulas followed from request to bill, each loss a printed line, the line's box beside it; the four causes as report bars | B, C | Steel `#E3E9F0` · navy `#0E1A2B` · signal orange `#FF8A3D` |
| Solutions | **The ledger of fixes**: one ruled entry per fix, its four stops ticked, what it brings back, a double-ruled total; by hand and automatic side by side | A, C | Lilac `#ECE7F7` · deep violet `#1D1736` · violet `#A48EFF` |
| Automations | **The helpers' day**: a flat 24-hour bar with each helper at its hour; one card per helper with its lamps and the slip it would print | C, B | Mint `#E0EFE8` · deep green `#08271D` · coral `#FF6F91` |
| Processes | **The week planner**: a ruled notebook week with the changes pinned on their days and a trial strip; a signature register; the numbers we watch, now against goal | A, F, C | Sand `#F2EBDC` · deep brown `#23190A` · sky blue `#4FA3F0` |

The rail now carries each place's own ground, on every page including home.

**After approval (Avishek, 8 Oct): update the block library.** Group the tools by domain: Discharge Process, Bed Management and OPD Diagnostic Leak under **Operations Tools**; Supply Chain and Procurement under **Financial Tools**. The response templates (turn blocks, universal patterns) stay open to every tool in every domain.

## Round two (8 Oct 2026): D, E, F
Avishek's feedback on A, B, C: keep C's clean design and colours, A's notebook and B's receipt, and **do not change the Virevo type at all**. So the domain identity can no longer use fonts: it lives in shapes, paper, marks, frame dress and drawings. `landing2.py` draws three looks with the **V skin** in `skins.py` (Bebas Neue, Poppins, Caveat at the 07 §2 sizes; C's flat frame and colours: report white `#EEEEE9`, black `#0F1012`, lime `#C6E43F`). The Financial paper vocabulary: report sheet (flat planes, heavy rules, numbered sections, hard lime block when raised), ledger paper (ruled lines, double margin, double rules under totals), receipt (torn zigzag edges, dashed tear lines, dotted leaders).

| Look | The month's money | The work |
|---|---|---|
| **D · The clean ledger** | Till receipt, total marked in lime | Ledger book: one ruled line per part, step bar as its entries; the pending list on ruled paper |
| **E · Receipts on the rail** | Ledger account, double-ruled total | Four receipts clipped to a black rail, step bar and big count on each; the open part prints as a docket |
| **F · The notebook** | Till receipt, stapled on | Open spiral notebook: parts on the left page, the open part's steps on the right, a hand note "We are here" |

Review page: `out/landing/supply-chain-home-round-2.html`. All 12 pages pass `qa.py`.

## The domain rule (Avishek, 8 Oct 2026)
Every domain has its own identity, and colour alone is not enough, because tools inside one domain already differ by colour.

| Stays the same in every domain (the layout) | Set by the domain (its identity) | Set by each tool inside the domain |
|---|---|---|
| Rail with Home and the five places, header bar, page, chat panel (desktop); top bar, feed, chat, message box, five icons (phone). The five landing zones in their order. Type scale and phone minimums (07 §2). Plain English. Picking, the three buttons, the stamp with Refresh now. Drawn, not software. | Type families. Shapes (corners, border weights, edges). Paper and texture. How the rail, header and chat panel are dressed. The marks for done, now, still to do, not started. How Tojo's Note is set. What "raised" looks like. The kind of drawing. | Its colours only: ground, card, ink, highlight. |

## The three looks
| Look | Type | Shapes and paper | Rail · chat · note | Raised | Drawing | Colours here |
|---|---|---|---|---|---|---|
| **A · The ledger** | Playfair Display + Source Serif 4 | Square corners, hairlines, double rules, a red double margin, ruled paper | Book thumb index · cloth-bound cover with a gilt line, ruled message card · italic serif | Printed offset shadow | The month's account (double-ruled total), then the accounts book: one ruled line per part, ticks as entries | Ledger buff `#ECE5CF` · navy ink `#1E2B45` · red ink `#B4321F` |
| **B · The till roll** | Space Mono + Space Grotesk | Paper slips with torn zigzag edges on a dotted counter, dashed tear lines, printed tick boxes | Tear-off tickets · the till printing slips · rubber stamp | Slip lifted and tilted | The month's till receipt, then four slips clipped to a rail, each stamped | Counter grey `#DAD6CC` · till ink `#26232E` · stamp violet `#6A3DBA` |
| **C · The annual report** | Inter Tight + Instrument Serif italic | Flat planes, no rounded corners, heavy rules, numbered sections, big figures | Flat numbered bars · flat black, editorial · serif italic pull quote | Hard block shadow | Where the money goes (one bar split four ways), then every step of the work in one bar, cut into its four parts | Report white `#EEEEE9` · black `#0F1012` · lime `#C6E43F` |

## What is where
| Path | What it is |
|---|---|
| `sc_common.py` | The domain layer: loads the Bed Management page parts as a private copy, the app frame (same markup and places as every tool), embedded fonts, chat panel, plain-English check (with this domain's own buying words). |
| `skins.py` | The three candidate identities A, B, C: fonts, frame dress, page-part dress, raised state. |
| `landing.py` | The home page words (one set for every look) and round one's drawings A, B, C. |
| `landing2.py` | Round two: D, E, F in Virevo type (F approved as home). |
| `landing3.py` | The five landing pages: home (F) and the four places. |
| `scp_library.py` | Adds this tool's section and the domain grouping to the block library (`python3 scp_library.py LIB OUT`); also called by `build_block_library.py`. |
| `qa.py` | Browser check: sideways scroll, the word "tab", text outside its box, script errors, phone picks side by side, picking, height. |
| `review_template.html` | The review page shell. |
| `fonts/` | The woff2 files (latin and latin-ext; the rupee sign is in latin-ext). SIL Open Font License. |
| `out/landing/` | `supply-chain-home-samples.html` (review page) and each page as `scp-home-<a|b|c>.<desktop|mobile>.<filled|empty>.html`. |

## Build
```bash
python3 landing.py      # writes out/landing/
python3 qa.py           # browser check (Playwright)
```
Needs `../Bed Management` and `../Common Elements` beside this folder.

## Checks on 8 Oct
All 12 pages pass `qa.py`. Desktop canvas heights 1,800–1,860px filled (OPD home 1,793). Every text pair clears 4.5:1; the lime of C is used for fills only on light ground.

## Open for Avishek
- Which of D, E, F becomes the Financial domain identity (A, B, C are set aside: fonts stay Virevo).
- Whether the chat panel may be dressed by the domain (all three do), or should stay forest for every domain.
- Example hospital figures for this tool.
- Rules 07 §1.1 and §2 say type and the chat panel are shared everywhere. Once a look is picked, they need a line saying these are now shared per domain.
