# Reply-check review pack · 6 October 2026

**TEST RUN.** Built from the test report `rc-2026-10-06-test-nagpur-300` (Bed Management, practice hospital). Nothing here comes from a live hospital. Decide as you would on a real pack, so the loop can be checked end to end.

Prepared by the back-end agent with `Backend Agent/skills/reply-check-review`. Ready for 9 AM, 7 October.

---

## 1. The day in five lines

- **1 chat, 20 counted turns,** all in Bed Management Diagnosis.
- **Ratings:** 1 Good, 1 Fine, 0 Bad, none skipped.
- **3 misses** (1 changed the subject, 1 not understood, 1 Fine). **2 resets, and both reworks recovered.**
- **Findings:** 1 high, 1 medium. I add 2 suggestions of my own and 1 request.
- **The report itself:** it passes the schema and holds no details about any person. One version label is wrong (see L-1).

## 2. Approved changes being watched

None yet. This is the first pack.

---

## 3. High

### [H-1] High · Bed Management · Diagnosis · off_playbook
`f-2026-10-06-01` · `ch-2026-10-06-01`

**What went wrong:** The user wanted to know why beds sit empty. Tojo kept to his list of questions, and the user said so plainly. Once Tojo named the usual reasons, the user answered.

**Seen in:** 1 chat, 1 user, 2 misses in a row (changed the subject, then not understood).

**Evidence:**
- Turn 2: *"We have 300 beds and they are always full. Which bed management software would you recommend?"* Tojo answered with the five areas of questions.
- Turn 3: *"No, you are not getting it. I don't need a questionnaire. I need to know why our beds sit empty for hours."* The reset followed, then the rework showed the four reasons and asked one question. The next reply answered it.

**Tojo suggests:** `bed-management-conversation-playbook.md` §1, stage 2 · add
- Today: "2. **Dependency verification** (`bed-management.md` §7.2) — five areas, agenda shown as a graphic, questions put one at a time."
- Suggested: "If the hospital asks why its beds sit empty before the five areas are done, answer that first. Show the usual reasons from `bed-management.md` §6, marked as not yet checked against theirs. Then ask which one fits, and come back to the five areas from there."

**My view: agree_reworded.** The gap is real. The playbook has no move for a user who wants the cause before the questions, so Tojo had nothing to fall back on. Two things need adding to the wording:
- Tojo must give **no verdict on their own answers** at this point, or the line clashes with 06 §3.3 ("Do not interpret while collecting").
- It must say that **none of the five areas is skipped.** Otherwise the shortcut becomes the habit.

**Final wording**, added as a new indented line under stage 2:
> If the hospital asks why its beds sit empty before the five areas are done, answer that first, in one turn. Show the usual reasons from `bed-management.md` §6 as reasons seen in other hospitals, not yet checked against theirs, and give no verdict on their own answers. Then ask which one fits, and go back to the five areas from there. None of the five is skipped.

**Also changes:**
- 06 §3.3, so the rules agree with the playbook (H-2).
- The playbook is cut into chunks, so run `publish/lint_chunks.py` and `publish/lint_points.py` after the edit. The chunk's front matter does not change.

**One flag:** the history has one user only. Under my skill (§2 step 3) that would make this a note about one user, not a rule change. I am putting it forward anyway. The miss comes from a move missing from the file, not from one person's taste, and it was a high "not understood". M-2 suggests making that exception part of the skill.

**Risk:** Tojo may jump to reasons too early with users who did not ask. The words "if the hospital asks" limit that. Watch `off_playbook` misses in Diagnosis for 14 days.

**Touches a standing rule:** no.

**Decide:** Approve · Reject · Rework (with a note)

### [H-2] High · every tool · wrong_register · my own (`source: back_end`)
Linked to `f-2026-10-06-01`.

**What it fixes:** Without this, H-1 puts a playbook in conflict with the rules every tool follows. A future Tojo reading 06 §3.3 alone would hold back the reasons again.

**Suggested:** `Tools Design/Common Elements/rules/06-html-response-rules.md` §3.3 · add, after the line below
- Today: "- **Do not interpret while collecting.** Acknowledge an answer and ask the next thing. What the answers mean waits for the diagnosis. Arithmetic on their own numbers (a total, a span) may be shown at any point; what the total means may not."
- Suggested: "- **If the person asks why before the facts are in, answer the why.** Show the usual reasons from the domain reference file, marked as seen in other hospitals and not yet checked against theirs. Give no verdict on their own answers, then go back to collecting."

**Reach:** every tool. The Discharge playbook has the same verification stage, so the same miss could happen there.

**Also changes:** nothing else. 06 is folded into each tool's system section, so rebuild those after the edit.

**Risk:** low. It opens a door only when the user asks for it.

**Touches a standing rule:** no. §3.3 is not one of the F rows.

**Decide:** Approve · Reject · Rework (with a note)

---

## 4. Medium

### [M-1] Medium · Bed Management · Diagnosis · too_long
`f-2026-10-06-02`

**What went wrong:** A Fine rating at turn 20, after three turns that each ran over 150 words with three drawings. The shorter rework recovered.

**Tojo suggests:** no change. 06 §5.1 already sets "most turns stay under about 150 words". The rule was right; Tojo broke it.

**My view: agree.** No file change. I will count `too_long` misses from here on. If the cause comes back in three or more chats within 14 days, I will bring a firmer wording for 06 §5.1.

**Decide:** Confirm no change · Ask for a change anyway

### [M-2] Medium · the back-end skill itself · my own (`source: back_end`)

**What it fixes:** My skill (§2 step 3) treats any finding seen with one user as a note about that user, unless the cause is a wrong fact or figure, or the wrong register. H-1 shows the gap. A high "not understood" that exposes a move missing from a file is a fault in the file, even if only one user has hit it so far.

**Suggested:** `Backend Agent/skills/reply-check-review/SKILL.md` §2 step 3 · replace
- Today: "If only one `user_ref` appears in the history, it is a user note unless the cause is `misread_reference`, `invented_figure` or `wrong_register`."
- Suggested: "If only one `user_ref` appears in the history, it is a user note unless the cause is `misread_reference`, `invented_figure` or `wrong_register`, or the finding is high and shows that a file has no move at all for what happened. Then put it to the team and say that only one user has hit it so far."

**Touches the reply-check rule or skill:** yes, the skill (09 §10 and skill §4.4). It needs your approval like any other change.

**Decide:** Approve · Reject · Rework (with a note)

---

## 5. Low

### [L-1] Low · request for the app

**What I found:** The report gives the Bed Management playbook's version as "2026-10-01". The file was last changed on 30 September. The wording Tojo quoted still matches the file exactly, so no harm was done this time. A wrong label could one day hide a stale suggestion, though.

**Request:** The app should fill `files_read` from each file's real date or content hash at the start of the day, instead of Tojo writing it. This is a change to the report job (`IMPLEMENTATION-GUIDE.md` §2a step 3), not to a rule.

**Decide:** Pass to the app team · Reject

---

## 6. Notes about one user

### [U-1] u-test
**Note:** Wants the reason first, then the questions.
**Seen in:** turns rc-02 and rc-03.
**My view: accept.** If approved, I write it to `review/user-profiles/u-test.md`, and Tojo reads it for this user from the next day.
**Decide:** Approve · Reject

---

## What happens after you decide

- **Approved:** I apply the final wording exactly, run the lints and rebuild the system sections, and add a line to each changed folder's changelog. The changes go live at midnight. Each one then goes on the 14-day watch.
- **Rework:** I revise the item and bring it back as `H-1-r1`, and so on.
- **Rejected:** I log your reason, so the same suggestion is not brought back without new evidence.
