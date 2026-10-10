# vault/tools — the tool request bundle

What a tool turn puts in front of the model (Phase 2 of `D:\Git_Virevo\docs\tools-backend-plan.md`,
live since 30 Sep 2026), copied byte for byte from AB's `Tools Design/Common Elements` (the 8 Oct 2026
drop, AB's commits of 6 Oct) and from the regular-chat package. `bundle.json` records each file's
source and hash.

```
tools/
  SKILL.md                         opens every tool's prefix (KT, 29 Sep 2026) — AB's 15 Sep v2, shared by all tools
  08-shared-turn-rules.md          AB's shared turn rules for the generators (6 Oct): §8 the three buttons on every turn,
                                   §11 how a tool carries the reply check. Never in a request; here so the folder shows AB's delivery
  reply-check-report.schema.json   rule 09's record ($defs.turn_record) and end-of-day report; read on every tool turn
  bundle.json                      sources, sizes, hashes, and what reads the files
  discharge/
    tojo-api-system-prompt.md      the output contract (step 0 since 8 Oct: the reply check); {{RULES_06}} and {{CATALOG}} filled at request time
    06-html-response-rules.md      the rule file the model reads on a tool turn (F11 and F12 since 8 Oct)
    registry.json                  the block catalogue in the prefix; the generator validates against the same file (scope per block since 8 Oct)
    tojo-response.schema.json      the tojo_turn input schema (reply_check since 8 Oct, by $ref; inlined at request time)
    landing-registry.json          which landing template is approved per tab
    tojo.css, tojo.js              inlined into every canvas page
```

**Rule 09, the reply check, is not in this folder.** AB keeps one copy for the regular chat and every
tool (`tojo-v2 - Regular Chat/rules/always-on/09-reply-check-rules.md`, rules/08 §11), so the vault
keeps one too: `vault/chat/_rules-09-reply-check.md`, id `_rules-reply-check`, kind `rules-ondemand`.
That kind means it is published with the chat skills but enters a prompt only where the code asks for
it by id: the tool path does since 8 Oct 2026 (it rides beside SKILL.md, as it rides beside 00-core in
AB's chat prefix), and so does the regular chat since the same evening (beside the rules block;
the record travels as a JSON string on the deliver_answer tool). One file serves both.

**Who reads this folder (8 Oct 2026).** The live tool engine reads `SKILL.md`,
`<tool>/tojo-api-system-prompt.md`, `<tool>/06-html-response-rules.md`,
`<tool>/tojo-response.schema.json` and `reply-check-report.schema.json` through the vault on every
turn (`ToolBundleSource`), and rule 09 by its id: on a box whose vault is a local folder (this
machine's IIS pool reads `D:\Git_Virevo\skills-live`) straight from here, so an edit of AB's files
reaches the next turn without a deploy; on a box that reads its vault from S3 (the dev box) from the
published copies - the publisher carries this whole folder, README.md excepted, as `tool_files` in the
manifest, so a publish is what moves an edit there. The chat log says "Tool request files come from …"
the first time, and names which of the two reply-check files came from the embedded copies when the
vault lacks them. A tool without its own folder borrows `discharge/`. The copies embedded in
`VirevoService_Dev/Chat/Virevo.Chat.Business/Tools/prompt/` serve only while a vault has no
`tool_files` or no rule 09 (a manifest published before 8 Oct 2026), and must still be refreshed on
every drop. The regular chat never sees this subfolder: the skill loaders enumerate top-level `*.md`
only. `registry.json`, `tojo.css` and `tojo.js` stay embedded with the generator
(`Virevo.Chat.Canvas`), content-identical to these (AB's 8 Oct copies of the css, the js and the
landing registry differ from the generator's only in line endings).

**Rules, as for `vault/chat`:** AB's bodies are never edited here; a new drop replaces the files and
`bundle.json`; `D:\Git_Virevo\skills-live\tools` is the live twin and is written in the same step
(`tools\sync-skills-live.ps1` checks both pairs). The eight font files stay in code
(`Chat/Virevo.Chat.Canvas/assets/fonts`), to be served by the UI; the worked turns and rendered
outputs are test fixtures, not vault content.
