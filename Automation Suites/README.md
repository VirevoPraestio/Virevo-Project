# Automation Suites: approved landing pages

This folder is the only home for the Automation Suite landing pages. Example figures are for a 250-bed hospital in Bhubaneswar.

## Approved landing pages
| Suite | Look | File | Live link |
|---|---|---|---|
| Discharge Summary | Hospital diorama, sky and lawn | `discharge-summary-suite-landing.html` | https://claude.ai/artifact/JyiLZP8oWPTHHKjgB1dUCt |
| Billing & Insurance | Olive and marigold sorting floor | `billing-insurance-suite-landing.html` | https://claude.ai/artifact/NUN3UWHiMj6kaTAcgshq4N |
| Admission Process | Indigo and sunflower radar | `admission-process-suite-landing.html` | https://claude.ai/artifact/BdnarE4WMGZXKvxCyuBcrv |
| Diagnostic Scheduling | Magenta and sky day board | `diagnostic-scheduling-suite-landing.html` | https://claude.ai/artifact/7peTH3nuvhGt4YF8PAhmME |
| Procurement | Teal and coral supply lines | `procurement-suite-landing.html` | https://claude.ai/artifact/5GQMkTzw16cG8YWe6DcBBS |
| Financial Health | Graphite and lime: expected EBITDA stepped to actual, one step per cause; overview frozen at the top | `financial-health-suite-landing.html` | https://claude.ai/artifact/A6hduzPB5K5GhXeBogwijz |

For the development team:
- `approved-suite-landings.html`: every approved suite landing, one picker. Live: https://claude.ai/artifact/W6vtiboihseN1RfQnhgfPM
- `suite-block-library.html`: every block of every suite (8 per suite), colours, how each is drawn and used, data model, index. Live: https://claude.ai/artifact/QWLcjF3a8GSKL9YfqBHHUK

All six Healthcare suites are approved. The files here open on their own (double-click); the live links are the same pages.

## Building the pages (`landing-src`)
One runtime builds every page: `python3 build.py [discharge|billing|admission|diagnostic|procurement|financial|approved|library]` writes `out/<name>.html` (for publishing), `out/standalone/<name>.html` (the files in this folder) and a `.preview.html` with local fonts (set `FONTS` in `build.py` to your font folder).

- `00-head.html`: page shell, hover peek, detail panel, chat (the tools' chat look)
- Data, one file per suite: `10-data.js` Discharge Summary, `12-data-billing.js`, `13-data-admission.js`, `14-data-diagnostic.js`, `18-data-procurement.js`, `19-data-financial.js`
- Runtime: `15-helpers.js` (suite switching, units), `16-ticker.js` (live counters), `20-shared.js` (details, Ask Tojo, chat replies), `25-fh.js` (Financial Health: day and since-start checks, the two chosen measures, causes, recovery steps, CEO Approve/Hold), `90-init.js` (page modes and the approved list), `91-library.js` (block library)
- Approved looks: `33-diorama.js`, `38-sorter.js`, `40-radar.js`, `41-dayboard.js`, `44-lines.js`, `47-bridge.js`
- `unchosen-options/`: the options that were reviewed and not chosen, kept for reference only; no build uses them.

To add a suite: write its data file and look file, add both to `build.py`, add the pair to `APPROVED` in `90-init.js`, and add its colour chips (`tok`) and `DRAWN` lines in `91-library.js`.

## Rules every suite follows
- Financial Health adds a Recovery section after KPIs, and its header (section bar, title, pulse strip, watch list, next go-live) stays frozen at the top, tightening into one band once the page scrolls.
- One layout: section bar, title with four pulse readings, watch list and next go-live, Integrations drawing, KPIs, Taskboards (Today / This week), Project Status. Resources and Chat open as panels.
- One look per suite, never shared with another suite or a tool. The Virevo type scale: Bebas Neue, Poppins, Caveat.
- The drawing is never named on the page; headings are just KPIs, Taskboards, Project Status.
- Every hover peek and detail panel carries **Ask Tojo about this** beside ×. It opens the chat with the item attached and writes: "Tell me more about [the point]: where this stands, whether there is any delay or overrun on it, who or what is responsible for it, whether we have any way to recover, and how we are planning to recover." Sending closes the popup and keeps the chat open; the prompt can be edited or cleared.
