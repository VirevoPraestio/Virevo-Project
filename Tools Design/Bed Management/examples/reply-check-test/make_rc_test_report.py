"""Tojo's end-of-day report for the reply-check test chat (rule 09 §10), checked against the report schema."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
SCHEMA = os.path.join(REPO, 'tojo-v2 - Regular Chat', 'schema', 'reply-check-report.schema.json')
PB = 'tojo-v2 - Regular Chat/skill/virevo-hospital-ops/references/bed-management-conversation-playbook.md'
T = {k: json.load(open(os.path.join(HERE, k + '.json'), encoding='utf-8')) for k in ('rc-01', 'rc-02', 'rc-03', 'rc-10', 'rc-20')}

def entry(k, recovered=None, said=None):
    s, r = T[k], T[k]['reply_check']; lr = r['last_reply']
    x = {'chat_id': r['chat_id'], 'turn_id': k, 'counted_turn': r['counted_turn'], 'user_ref': r['user_ref'],
         'tojo_said': said or '%s turn: %s' % (s['turn']['type'], s['canvas']['blocks'][0]['title']),
         'user_reply': s['turn']['user_message'], 'reply_class': lr['class'], 'action': r['action'], 'sources': r['sources']}
    if r.get('ask'): x['tojo_asked'] = r['ask']['text']
    if lr['class'].startswith('rating_'): x['rating'] = lr['class'].split('_')[1]
    if r.get('recheck'): x['recheck_found'] = r['recheck']['playbook']
    if recovered is not None: x['recovered'] = recovered
    return x

report = {
 'report_id': 'rc-2026-10-06-test-nagpur-300', 'day': '2026-10-06', 'deployment': 'test-nagpur-300', 'written_at': '2026-10-07T00:02:00+05:30',
 'files_read': [{'file': 'tojo-v2 - Regular Chat/rules/always-on/00-core.md', 'version': 'v2'},
                {'file': 'tojo-v2 - Regular Chat/rules/always-on/09-reply-check-rules.md', 'version': 'v1 2026-10-06'},
                {'file': 'Tools Design/Common Elements/rules/06-html-response-rules.md', 'version': 'v2 with F12, 2026-10-06'},
                {'file': 'Tools Design/Common Elements/rules/08-shared-turn-rules.md', 'version': '2026-10-06'},
                {'file': PB, 'version': '2026-10-01'},
                {'file': 'tojo-v2 - Regular Chat/skill/virevo-hospital-ops/references/bed-management.md', 'version': '2026-09-09'}],
 'totals': {'chats': 1, 'counted_turns': 20, 'ratings': {'good': 1, 'fine': 1, 'bad': 0, 'skipped': 0},
            'misses': {'ignored': 0, 'not_understood': 1, 'changed_subject': 1, 'rating_fine': 1, 'rating_bad': 0, 'unsure': 0},
            'resets': 2, 'reworks_recovered': 2, 'ask_directly': 0, 'findings': {'high': 1, 'medium': 1, 'low': 0},
            'by_tool': [{'tool': 'Bed Management', 'place': 'diagnosis', 'counted_turns': 20, 'misses': 3, 'resets': 2}]},
 'findings': [
  {'finding_id': 'f-2026-10-06-01', 'priority': 'high', 'cause': 'off_playbook', 'tool': 'Bed Management', 'place': 'diagnosis',
   'section_at_fault': PB.split('/')[-1] + ' §1, stage 2',
   'title': 'Kept to the question agenda when the user wanted the cause first',
   'what_happened': 'After the case reveal the user jumped to software, then said plainly Tojo was not getting it: they wanted to know why beds sit empty. Tojo had gone straight into the five areas of questions. The rework named the four usual reasons first, and the user then answered.',
   'chats': 1, 'misses': 2,
   'history': [entry('rc-02'), entry('rc-03', recovered=True)],
   'suggested_changes': [{'change_id': 'ch-2026-10-06-01', 'file': PB, 'file_version': '2026-10-01', 'section': '§1, stage 2', 'kind': 'add',
     'words_today': '2. **Dependency verification** (`bed-management.md` §7.2) — five areas, agenda shown as a graphic, questions put one at a time.',
     'words_suggested': '   If the hospital asks why its beds sit empty before the five areas are done, answer that first. Show the usual reasons from `bed-management.md` §6, marked as not yet checked against theirs. Then ask which one fits, and come back to the five areas from there.',
     'reason': 'off_playbook. The playbook gives no move for a user who wants the cause before the questions, so Tojo kept to the agenda twice. With this line he would have shown the four reasons at the first sign, one turn earlier, and kept the user.',
     'reach': 'this_subject', 'confidence': 'medium'}]},
  {'finding_id': 'f-2026-10-06-02', 'priority': 'medium', 'cause': 'too_long', 'tool': 'Bed Management', 'place': 'diagnosis',
   'section_at_fault': '06 §5.1',
   'title': 'Rated Fine after three long turns in a row',
   'what_happened': 'The rating at the 20th turn came back Fine. The three turns before it ran over 150 words each, with three drawings under the heading. The rework was two short paragraphs and the five parts only, and the user picked a part.',
   'chats': 1, 'misses': 1,
   'history': [entry('rc-20', recovered=True)],
   'no_change_reason': '06 §5.1 already says most turns stay under about 150 words. The rule was right; Tojo broke it. No change suggested; watch for repeats.'}],
 'user_notes': [{'user_ref': 'u-test', 'note': 'Wants the reason first, then the questions.', 'turns': ['rc-02', 'rc-03'], 'priority': 'low'}],
 'repeats': []}

try:
    from jsonschema import Draft202012Validator
    Draft202012Validator(json.load(open(SCHEMA, encoding='utf-8'))).validate(report); print('report valid against the schema')
except ImportError:
    print('jsonschema not installed; report written without the schema check')
json.dump(report, open(os.path.join(HERE, 'rc-test-report.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print('wrote rc-test-report.json')
