# Backend Agent

The agent that sits between Tojo, the front-end chat agent, and the Virevo development team. Tojo never sees this folder.

## Skills
| Skill | What it does |
|---|---|
| `skills/reply-check-review/` | Reads Tojo's end-of-day reply-check report, judges every finding and suggested change, writes the daily review pack for the team, applies only what the team approves from the next midnight, and checks over 14 days that each change worked. |

## What it reads from elsewhere
- `tojo-v2 - Regular Chat/rules/always-on/09-reply-check-rules.md`: the rule Tojo follows.
- `tojo-v2 - Regular Chat/schema/reply-check-report.schema.json`: the report format. One copy only, kept beside the rule, so the two agents can never drift apart.

## Its own working folder
`review/` is created on first run: `decisions.jsonl` (every decision, append-only), `watch.json` (approved changes being checked), `user-profiles/` (accepted notes about one user's way of working).
