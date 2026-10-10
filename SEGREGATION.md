# Segregating AB's deliveries

*Started 29 Sep 2026. AB's packages land in this repository as delivered. On every update the files are split three ways, by this map. Nothing AB wrote is edited in the process; only file names and front matter are added where the vault needs them.*

## The rule

Every file in an AB package falls into one of three buckets. The test is a question about the file, not about who wrote it.

| bucket | the question | where it goes |
|---|---|---|
| **vault** | Does any of this text enter an API request, at any stage — the cached prefix, the router, retrieval, a tool definition? | `vault/…` in this repo (publish-ready), then `D:\Git_Virevo\skills-live` for local IIS, then S3 through `Utility/Virevo.Utility.SkillsPublisher.Cli` for the dev box, when KT says |
| **code** | Does our code read it at build, run or test time — a template to port, CSS or JS to inline, a registry, fonts, a fixture an automated test compares against? | the project folders in `VirevoService_Dev` and `VirevoUI_Dev`, named below |
| **left** | Neither: written for people, or tooling AB runs on AB's side. | stays only in AB's folder here; never copied anywhere |

A file can be in two buckets (the block registry feeds the prompt and the validator). A file in *left* is not unimportant; it is simply not an input to anything we run.

## Layout of this repository

```
Virevo-Project/
  tojo-v2 - Regular Chat/        AB's regular-chat package, as delivered; AB updates here
  <tojo-html - Discharge Tool>/  AB's tool package, when it lands here (strip its nested .git first)
  vault/
    chat/                        publish-ready regular-chat files: exactly what skills-live and S3 hold
    tools/                       the tool request files; the publisher carries the whole folder (except README.md) since 1 Oct 2026
  SEGREGATION.md, SEGREGATION.json   this map, and the same map for tooling
```

`vault/chat/` was seeded on 29 Sep 2026 from `skills-live` (23 files, identical apart from `backup/`).

**`D:\Git_Virevo\skills-live` is the live folder.** The local application reads it and KT works from it, so it is never allowed to fall behind: every change to `vault/chat/` is written to `skills-live` in the same step, and the two are checked identical (apart from `skills-live\backup/`) at the end of every drop. `vault/chat/` is the git-tracked twin that gives history and diffs; if `skills-live` is ever edited directly, that change is pulled into `vault/chat/` first, so nothing is lost when the next drop is applied. `tools\sync-skills-live.ps1` does the check (default) and the copy in either direction (`-Apply` vault → live, `-Pull` live → vault); it never deletes anything.

## Map — regular chat package (`tojo-v2 - Regular Chat/`)

This is how the package was split when the vault was built, recorded so the next update follows the same lines. Vault files carry front matter (`id`, `title`, `description`, `keywords`, `kind`, `version`, `source_file`, `source_author`); the body is AB's, unchanged.

| AB's file | bucket | destination | note |
|---|---|---|---|
| `rules/always-on/00-core.md` | vault | `vault/chat/_rules-00-core.md`, `kind: rules` | persona and the SVG drawing rules; in the regular chat's prefix |
| `rules/on-demand/01-response-rules.md` | vault | `vault/chat/_rules-01-response.md`, `kind: rules` | |
| `rules/on-demand/02-image-creation-rules.md` | vault | `vault/chat/_rules-02-image.md`, `kind: rules` | |
| `rules/on-demand/04-layout-patterns.md` | vault | `vault/chat/_rules-04-layout.md`, `kind: rules` | |
| `skill/virevo-hospital-ops/references/discharge-process.md`, `discharge-process-conversation-playbook.md`, `bed-management.md`, `opd-diagnostic-leakage.md` | vault | `vault/chat/<same name>`, `kind: topic` | retrieved by chunk; the tool path uses the same copies |
| `skill/virevo-hospital-ops/references/common-elements.md` | vault | `vault/chat/common-elements.md`, `kind: shared` | |
| `skill/virevo-hospital-ops/index/GROUP-CATALOGUE.md` + the five `*.card.md` | vault | assembled into `vault/chat/_index.md`, `kind: index` | one file built from six; resident on every call |
| `skill/virevo-hospital-ops/index/POINT-INDEX.md` | vault | `vault/chat/index/POINT-INDEX.md` | searched by the retriever, never in the prompt |
| `skill/virevo-hospital-ops/index/points/*.points.md` | vault | `vault/chat/index/points/` | |
| `skill/virevo-hospital-ops/SKILL.md` | vault (tools) | `vault/tools/SKILL.md` | not published for the regular chat (the index plays its part there); from 29 Sep it opens every tool's prefix, one shared copy |
| `image/DESIGN-TOKENS.md`, `image/templates/*.py` (17 files) | code, ported | `Chat/Virevo.Chat.Business/FigureRenderer.cs` | AB's Python figure templates live on as C#; a change here is a code change and a release, never a copy |
| `image/samples/*.svg`, `*.png` (56 files) | left | — | what the figures should look like; compare by eye when the renderer changes |
| `publish/lint_chunks.py`, `publish/lint_points.py` | left | — | AB's checks; the publisher CLI validates instead. When they change, the publisher's validation may need the same change |
| `README.md`, `IMPLEMENTATION-GUIDE.md`, `CHUNKING-SPEC.md`, `FIGURE-STUBBING-SPEC.md` | left | — | the specs our code follows; a change is a code change |

Vault files with no source in this package: `_rules-00a-register-sales.md`, `_rules-00b-register-advisor.md`, `_rules-20-scripted-flow.md`, `_rules-30-pricing.md` (AB, earlier deliveries), `_rules-03b-svg-grammar.md`, `_rules-90-referral.md`, `_router.md` (ours). They live only in `vault/chat/`.

## Map — discharge tool package (`tojo-html`, AB v5 of 28 Sep 2026)

Until AB's folder is in this repository the source is `D:\Git_Virevo\FROM AB\Discharge_Tool_-_Documents - 3\tojo-html\tojo-html\tojo-html`. **The code bucket was copied on 30 Sep 2026** when the tool path was built (`D:\Git_Virevo\docs\tools-backend-plan.md`); the destinations below are the real ones. Since 1 Oct 2026 the publisher carries `vault/tools/` into the bucket as `tool_files` in the manifest, and the live tool engine reads SKILL.md, the prompt template, 06 and the response schema through the vault in both modes (embedded copies only until the first publish that carries them); registry.json, tojo.css and tojo.js still ride along for reference while the generator keeps its embedded copies.

| AB's file | bucket | destination | note |
|---|---|---|---|
| `prompts/tojo-api-system-prompt.md` | vault | `vault/tools/discharge/` → `skills-live/tools/discharge/` (staged 30 Sep 2026, byte-identical, no front matter) | the output contract; the generator's `prompt` command fills `{{RULES_06}}` and `{{CATALOG}}` into it |
| `rules/06-html-response-rules.md` | vault | `vault/tools/discharge/` → `skills-live/tools/discharge/` (staged 30 Sep 2026) | the only rule file the model reads on a tool turn |
| `blocks/registry.json` | vault, and read by the generator | `vault/tools/discharge/` | the catalogue in the prefix is built from it; the generator validates against the same copy, so they cannot drift |
| `schema/tojo-response.schema.json` | vault | `vault/tools/discharge/` → `skills-live/tools/discharge/` (staged 30 Sep 2026) | sent in every tool request as the `tojo_turn` input schema |
| (from the chat package) `SKILL.md` | vault | `vault/tools/SKILL.md` → `skills-live/tools/SKILL.md` (staged 30 Sep 2026) | opens the tool prefix |
| `blocks/registry.json`, `landing-common/landing-registry.json`, `diagnosis-html-generator/assets/tojo.css`, `tojo.js` (vault copies) | vault, as well as code | `vault/tools/discharge/` → `skills-live/tools/discharge/` (staged 30 Sep 2026); `vault/tools/bundle.json` records sources and hashes | the runtime data KT put in the vault bucket on 29 Sep; the API embeds identical copies until the loader can carry JSON and CSS |
| `references/discharge-process.md`, `…-conversation-playbook.md` | vault, already | `vault/chat/` | byte-identical to the chat copies; if a drop makes them differ, the chat copy is the one retrieval uses, and the difference goes back to AB |
| `diagnosis-html-generator/diagnosis_html.py` | code, ported | `VirevoService_Dev/Chat/Virevo.Chat.Canvas/` (`CanvasRenderer.cs`, `SpecValidator.cs`, `PageBuilder.cs`, `Catalog.cs`, `Py.cs`, `FormulaEvaluator.cs`) | ported 30 Sep 2026; AB's Python is the reference; the replay test renders AB's twelve turns byte for byte |
| `landing-common/landing_common.py` (shared zones, `LP_BASE_CSS`); `diagnosis-html-generator/landing.py` (sample C and its CSS) | code, ported | `Chat/Virevo.Chat.Canvas/LandingRenderer.cs`; the two CSS strings extracted unchanged into `Chat/Virevo.Chat.Canvas/assets/landing-base.css`, `landing-diagnosis.css` | the approved Diagnosis landing, proven against `out/landing/diagnosis-c.desktop.{filled,empty}.html` |
| `solutions-`, `automations-`, `processes-html-generator/landing.py` | code, ported (9 Oct 2026) | `Chat/Virevo.Chat.Canvas/LandingRenderer.Tabs.cs` (Solutions B, Automations B, Processes A); the three CSS strings extracted unchanged into `assets/landing-{solutions,automations,processes}.css`; each `DATA` as `Tests/Virevo.Chat.Canvas.Tests/fixtures/landing/{tab}.data.json`; the `empty` halves as `assets/landing-empty/dp-{tab}.json` (the first-visit page) | proven against the v5 previews (`Discharge Process/tojo-html/out/landing/`) and, for Processes A, against `Common Elements/out/block-library.html` (the v5 preview predates `roles_cost`) |
| `diagnosis-html-generator/assets/tojo.css`, `tojo.js` | code | `Chat/Virevo.Chat.Canvas/assets/` (embedded resources) | inlined into every canvas; copied unchanged |
| `blocks/registry.json` | code, as well as vault | `Chat/Virevo.Chat.Canvas/blocks/registry.json` (embedded) | travels with the renderers on purpose: a new block needs both; the replay test asserts it equals the fixture copy |
| `diagnosis-html-generator/assets/fonts/*.woff2` (8 files) | code | `Chat/Virevo.Chat.Canvas/assets/fonts/` (embedded; served or inlined by the API) and, still to do, `VirevoUI_Dev/src/assets/fonts/` | the API embeds them until `Tools:FontsHref` names a stylesheet the UI serves; `BebasNeue-Regular.ttf` in the UI is then replaced by the woff2 set |
| `landing-common/landing-registry.json` | code, not copied | — | the approved picks are in code: all four templates ported (`LandingRenderer.cs`, `LandingRenderer.Tabs.cs`, 9 Oct 2026) |
| `examples/turn-01…12.json` | code | `Tests/Virevo.Chat.Canvas.Tests/fixtures/ab-v5/examples/` | the replay oracle of the universal generator only; since 9 Oct 2026 the scripted engine replays the Tools Design templates tab by tab (`Chat/Virevo.Chat.Business/Tools/script/{discharge,bed}/{tab}/`), and the retired twelve and our `summaries.json` left `Tools/script/` |
| `out/turn-*.canvas.html`, `out/landing/diagnosis-c.desktop.*.html`, `out/system-section.md` | code | `Tests/Virevo.Chat.Canvas.Tests/fixtures/ab-v5/out/` | the replay oracle; AB's canvas files carry an older tojo.css and the label `tojo_html 1.0`, the only two things the test normalises. The `.desktop.html`/`.mobile.html` previews and the other landing samples were not copied |
| `prompts/tojo-api-system-prompt.md`, `rules/06-html-response-rules.md`, `blocks/samples.json` | code (fixtures), as well as vault for the first two | `Tests/Virevo.Chat.Canvas.Tests/fixtures/ab-v5/` | the prompt-section test builds AB's `system-section.md` from them; `samples.json` is copied but unused (a block gallery would use it) |
| `examples/archive/`, `out/gallery.html`, `out/design-canvas/` | left | — | |
| `diagnosis-html-generator/server.py`, `api_example.py`, `preview.py`, `dc_export.py`; `landing-common/build_landing.py`, `measure.py`; `tests/check_turns.py`, `calibrate.py` | left | — | AB's Python tooling; the port replaces `server.py`, AB's QA scripts run on AB's side |
| `rules/05-universal-answering-method.md`, `rules/07-html-block-design-rules.md` | left | — | 05 is the method 06 was distilled from; 07 governs the templates and therefore the port, but never enters a request |
| `README.md`, `CHANGELOG.md`, `DIAGNOSIS-TAB.md`, `LANDING-PAGES.md`, `PROJECT-CONTEXT.md` | left | — | the CHANGELOG is what to read first on every drop |
| `tojo-project-knowledge/` | left | — | a flattened copy for a Claude Project; ignore |
| `.git/` inside the package | strip on intake | — | or git treats AB's folder as a nested repository |

## Before tool files can be published (as it stood on 30 Sep 2026; done on 1 Oct: the publisher carries `vault/tools/**` as `tool_files`, JSON included, and the loaders read them by path)

The vault today accepts flat `*.md` files with `kind` in {topic, router, rules, rules-ondemand, shared, index} plus the point index, and the publisher enumerates `*.md` only. Tool request files need three small additions before the live engine (Phase 2): a kind of their own for prefix parts (so they are never swept into the regular chat's prefix, where every `kind: rules` file goes today), JSON objects in the manifest (the registry and the schema), and a per-tool key prefix (`tools/discharge/…`). Until then `vault/tools/` is staging only.

**Where the staging lives (30 Sep 2026).** `vault/tools/` is mirrored to `D:\Git_Virevo\skills-live\tools\` so that folder shows AB's whole current delivery, as KT expects. This is safe because both the loader (`LocalFolderSkillVault`) and the publisher enumerate top-level `*.md` only: a subfolder is invisible to the regular chat and to a publish. The files are AB's bytes with no front matter added; `vault/tools/bundle.json` carries the sources, sizes and hashes instead, and `tools\sync-skills-live.ps1` checks this pair as well as the chat one.

## Map — Tools Design (AB's repository folder, from the 8 Oct 2026 pull)

Since 8 Oct 2026 AB's deliveries arrive by `git pull` from `VirevoPraestio/Virevo-Project` (the 8 Oct merge brought his commits of 30 Sep to 7 Oct: "block library update and new rule", "shifted Reply check rules to common elements"). The source is no longer a copied `tojo-html` folder but `Tools Design/`, in three parts: `Common Elements/` (the shared rules 05–08, the one block registry, the schema, the prompt template, the four tab generators, the tool layer, the block library), `Discharge Process/` (the 32 regenerated Discharge turns with per-place generators, and the old `tojo-html/` copy left as it was) and `Bed Management/` (the second tool, whole). `Backend Agent/` holds AB's back-end agent for the reply-check reports. `git diff --name-status <before> HEAD` on those folders is the work list.

**The 9 Oct 2026 merge** (KT, 13:13) brought AB's commit `800634d` of 8 Oct 19:13, "updated block library": four new tools in their own folders, each with its five approved landing pages (home and the four places) and no turn generators yet - `Supply Chain Procurement/` (the first Financial tool and the Financial look, the V skin), `Revenue EBITDA/`, `Length of Stay/` (Financial, the same look in their own colours) and `OPD Diagnostic Leak/` (Operations, the Bed Management parts in its own colours); the block library at version 14 (grouped by domain, every template with a How to use card); rule 07 (one domain, one identity) and rule 08 (§12 domains, §13 every template open to every tool); and five review pages in `Claude outputs/` (left). No turn generator, registry, schema or prompt file changed.

| AB's file | bucket | destination | note |
|---|---|---|---|
| `Common Elements/prompts/tojo-api-system-prompt.md` | vault | `vault/tools/discharge/` → `skills-live/tools/discharge/` (8 Oct 2026, AB's bytes, CRLF) | step 0, the reply check, added |
| `Common Elements/rules/06-html-response-rules.md` | vault | `vault/tools/discharge/` → `skills-live/tools/discharge/` (8 Oct 2026) | rule 09 in the read-with list; F11 extended (the three buttons close every turn); F12 added (the reply check); the other tabs' rows; patterns cross tabs; `chat.moves` when a conversation moves tab (not in the schema yet, so the model cannot send it) |
| `Common Elements/schema/tojo-response.schema.json` | vault | `vault/tools/discharge/` → `skills-live/tools/discharge/` (8 Oct 2026) | `reply_check` added as a `$ref` into the regular chat's reply-check schema; the API cannot follow it, so `ToolPromptBuilder` inlines `$defs.turn_record` at request time. `canvas.actions` is still missing from AB's schema; the builder adds it (rules/08 §8) |
| `Common Elements/blocks/registry.json` | vault, and code | `vault/tools/discharge/`, `Chat/Virevo.Chat.Canvas/blocks/registry.json`, `Tests/Virevo.Chat.Canvas.Tests/fixtures/ab-v5/blocks/registry.json` | each block gained `scope`; nothing else changed, so the replay oracle still holds |
| `Common Elements/landing-common/landing-registry.json`, `diagnosis-html-generator/assets/tojo.css`, `tojo.js` | vault | `vault/tools/discharge/` (8 Oct 2026) | line endings only; the generator's embedded copies are content-identical and untouched |
| `Common Elements/rules/08-shared-turn-rules.md` | vault (reference) | `vault/tools/08-shared-turn-rules.md` (refreshed 9 Oct 2026 with §12 domains and §13 every template open to every tool; AB's bytes; `bundle.json` updated; skills-live identical) | for the generators, never in a request (AB assembles the prompt from 06 and the catalogue only); §8 and §11 are what the code carries out |
| `Common Elements/tool-layer/reply_check.py` | code, ported | `Chat/Virevo.Chat.Business/Tools/ReplyCheck.cs` | the checks on the record, the three fixed lines read from rule 09, the record's schema inlined |
| `Common Elements/tool-layer/tojo_layer.py`, `Bed Management/{diagnosis,solutions,automations,processes}-html-generator/bm_*.py`, `Discharge Process/<place>-html-generator/dp_*.py` + `dp_common.py` | code, ported (8–9 Oct 2026) | `Chat/Virevo.Chat.Canvas/Places/` (`PlaceRegistry`, `PlaceGenerator`, `ToolLayer`, the four renderers and validators); the CSS/JS/registry assets extracted unchanged into `assets/places/` | the eight places (two tools × four tabs); proven byte for byte against AB's 79 rendered turns (`Tests/.../fixtures/places/`) |
| `Discharge Process/<place>/examples/dp-*.json`, `Bed Management/examples/<place>/bm-*.json` (the turn templates, with each place's `turns.json` naming the first turn's variant) | code | `Tests/Virevo.Chat.Canvas.Tests/fixtures/places/{dp,bm}-{tab}/` (replay) and `Chat/Virevo.Chat.Business/Tools/script/{discharge,bed}/{tab}/` (embedded; the scripted engine's script, 9 Oct 2026) | the sequence is `turns.json`'s: bm-au-01-B, bm-so-01-A, bm-dg-01-A for the first turns |
| `Bed Management/v3.py`, `bm_common.py`, `{diagnosis,solutions,automations,processes}/*.py` (the approved pages: Diagnosis B, Solutions B, Automations C, Processes B), `out/landing/approved/bed-management-approved-pages-v3.html` | code, ported (9 Oct 2026) | `Chat/Virevo.Chat.Canvas/BedLandingRenderer.cs`; the page stylesheets and `SEL_JS` extracted unchanged from the approved pages into `assets/landing-bm-{tab}.css`, `assets/landing-bm.js`; each page's `DATA` as `Tests/.../fixtures/landing/bm-{tab}.data.json`, the `empty` halves as `assets/landing-empty/bm-{tab}.json` | proven byte for byte against the approved pages (`BedLandingTests`); the home page (ward plan) is not drawn - our worksheet is the tool's front |
| `Common Elements/library/`, `landing-common/*.py` (shared zones, already ported), `Bed Management/home/`, `Bed Management/archive/`, `qa_v3.py`, `*/check.py` | left | — | the block library and the QA scripts are AB's side; the shared landing zones were ported on 30 Sep |
| `Common Elements/examples/`, `reply-check-test/`, `out/`, `tests/`, `README*.md`, `ARTIFACTS.md`, `LANDING-PAGES.md`, `rules/05`, `rules/07`, `blocks/samples.json`, `Discharge Process/tojo-html/` | left | — | |
| `Supply Chain Procurement/landing3.py`, `Revenue EBITDA/places.py`, `Length of Stay/places.py`, `OPD Diagnostic Leak/landing.py` (+ `sc_common.py`, `odl_common.py`) | code, ported (9 Oct 2026) | `Chat/Virevo.Chat.Canvas/SupplyChainLandingRenderer.cs`, `RevenueLandingRenderer.cs`, `LengthOfStayLandingRenderer.cs`, `OpdLeakLandingRenderer.cs`, on bm_common's parts (`LandingParts.cs`, which Bed Management now shares); each page's stylesheet taken unchanged from AB's render into `assets/landing-{scp,rev,los,odl}-{tab}.css`; registered in `ToolLandingFamilies` | the 16 place pages, byte for byte against AB's renders (`NewToolLandingTests`, 32 pages). The figures AB's code prints from literals (totals, trial lengths, the statement title, the 1,300 extra days, the pad's date) are read from the data; his fixtures carry them under `_literals`. **Not wired to a tool of the app**: the app's list (OPD Scheduling, Clinical Notes, Supply Chain) is not AB's (OPD Diagnostic Leak, Revenue & EBITDA, Length of Stay), and these pages read fields our summary contract does not carry yet. The home pages are not drawn |
| `{Supply Chain Procurement,Revenue EBITDA,Length of Stay,OPD Diagnostic Leak}/out/landing/{scp,rev,los,odl}-{diagnosis,solutions,automations,processes}.desktop.{filled,empty}.html` | code | `Tests/Virevo.Chat.Canvas.Tests/fixtures/landing/` (the canvas inside `<main>`), with each page's DATA as `{tool}-{tab}.data.json` and its empty half as `Chat/Virevo.Chat.Canvas/assets/landing-empty/{tool}-{tab}.json` | the replay oracles |
| `skins.py`, `landing2.py`, `landing.py` (SCP), `rev_landing.py`, `los_landing.py`, `*_library.py`, `qa.py`, `shot.py`, `review_template.html`, `fonts/`, the home renders and review pages; `Claude outputs/*.html` | left | — | the home pages' samples and AB's tooling; `fonts/` are the set-aside looks' (the Financial look keeps the Virevo type) |
| `Common Elements/library/template_uses.json`, `reorganise.py` | left | — | the library's How to use cards (195, keyed by the registry's block names: what a template shows, key uses, best for). A candidate for the model's catalogue if AB puts it in a request; until then it is not one |
| `Common Elements/rules/07-html-block-design-rules.md` (8 Oct: one domain, one identity) | left | — | governs the templates; never in a request |
| `Backend Agent/**` | left | — | AB's agent that reads the end-of-day reports; nothing runs here yet |

**The regular chat package on 8 Oct 2026:**

| AB's file | bucket | destination | note |
|---|---|---|---|
| `rules/always-on/09-reply-check-rules.md` | vault | `vault/chat/_rules-09-reply-check.md`, id `_rules-reply-check`, `kind: rules-ondemand`, `version: 2026-10-06` | one copy for the chat and every tool, as AB keeps it. On-demand so a prefix carries it only where the code asks by id: the tool path (`ToolBundleSource`, beside SKILL.md) and, since the same evening, the regular chat (`ChatOrchestrator`, beside the rules) |
| `schema/reply-check-report.schema.json` | vault | `vault/tools/reply-check-report.schema.json` | `$defs.turn_record` into the tool schema and the record checks; the report root waits for the midnight job |
| `schema/reply-check-report.sample.json` | left | — | |
| `skill/virevo-hospital-ops/references/bed-management-conversation-playbook.md` | **held** | — | its own header says it is a reference behind `claude/06-bed-management-answering-rules.md` (not delivered) and "should not be chunked into the skill package"; no index card or point names it. Back to AB: which file is the runtime one |
| `README.md`, `IMPLEMENTATION-GUIDE.md` (§2a: the reply check around the model) | left | — | the spec the code follows |

**What the reply check needs from the app, and where it stands (8 Oct 2026).** Rule 09 asks three things of the app (IMPLEMENTATION-GUIDE §2a): show the three fixed lines (opening, rating, reset) as the app's own messages when the record names them; store every `reply_check` record and never show it; write the end-of-day report at midnight and hand it to the back-end agent. On the tool path the first two are built: the fixed lines come from the rule's text, the rating is a stored turn of type `rating` that holds the message, the record is checked as `reply_check.py` checks it and stored in `chat.tool_turns.reply_check` (schema 012). The report job is not built. The regular chat got the same the same evening: rule 09 by id beside the rules, the record as a JSON string on the `deliver_answer` tool (an object made the strict tool's grammar too large for the API), the rating and the fixed lines, storage on `message_turn_detail.reply_check` (schema 013, functions 120). Not built on either path: the midnight report.

## The procedure, every drop

1. AB updates their folder here (since 8 Oct 2026 by `git pull` from `VirevoPraestio/Virevo-Project`; before that a drop was copied in, with its nested `.git` removed). Read the CHANGELOG or README first.
2. `git diff --stat` on AB's folder: the list of changed, new and deleted files is the work list.
3. Look each file up in `SEGREGATION.json`. A new file with no entry is placed by the question in the rule above, and the map is extended in the same change. `node tools/check-map.js <commit-before-the-merge>` lists every changed file of the Tools Design package under the entry that places it (UNMATCHED = still to place).
4. **Vault files:** first run `tools\sync-skills-live.ps1` and pull anything edited directly in `skills-live` into `vault/chat/`. Then copy the drop's files to `vault/…` under the vault name; add or refresh the front matter (`version` = AB's date, `source_file` = AB's path); body untouched. Run the publisher's `validate` on the folder. Write `vault/chat/` to `skills-live` in the same step (`-Apply`) and confirm the check is clean; the local application picks the files up from there. Publish to S3 only when KT says.
5. **Code files:** copy content files to their project home. A changed template, generator source or spec is a code change: port it, run the replay test against AB's rendered files of the same drop, and it ships with the next release.
6. **Left files:** nothing to do.
7. Report: what moved where, that `skills-live` matches, what needs a build, what waits on a decision. Commit only when asked.
