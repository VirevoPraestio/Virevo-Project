"""bm-dg-01 (transcript Turn 7, the case reveal), three samples. Writes bm-dg-01-A.json, -B.json, -C.json.
Same chat in all three; only the drawing changes. Each drawing is an approved library block (scope all)
with the Bed Management layer: the four moments as sheets, each with an "Add yours" entry, and one more entry
for anything else about the hospital's setup (the turn's own question)."""
import copy, json, os
HERE = os.path.dirname(os.path.abspath(__file__))

SAID = ('Beds it is — and what you’ve described lines up closely with a hospital we worked with. Let me show you their day rather than describe it. '
        'One thing to watch as you read it: that bed stopped earning hours before it was empty. Does that look like your day? '
        'And is there anything about your own setup you’d add to what’s there?')

SHEETS = [
 {'key': 'a', 'when': 'Late morning', 'title': 'Final bill closed', 'bed': 'leaving', 'bill': 'off',
  'text': 'The leaving patient’s final bill is closed and sent for insurance approval. From here nothing more is charged to this bed.',
  'bed_line': 'Patient still in it', 'bill_line': 'Closed. Nothing more charged',
  'entry': 'When does the final bill close at your hospital?', 'entry_hint': 'For example: nearer 1 PM, after the pharmacy check'},
 {'key': 'b', 'when': 'Afternoon', 'title': 'Approval, payment, family briefing', 'bed': 'leaving', 'bill': 'off',
  'text': 'The insurer approves, the family pays and is told what happens at home. All this time the patient is still in the bed.',
  'bed_line': 'Patient still in it', 'bill_line': 'Nothing billing',
  'entry': 'What happens in your afternoon?', 'entry_hint': 'For example: approval takes 3 hours for some insurers'},
 {'key': 'c', 'when': 'Evening', 'title': 'Patient leaves, bed made ready', 'bed': 'empty', 'bill': 'off',
  'text': 'The patient finally leaves. Housekeeping cleans the bed and gets it ready for the next patient.',
  'bed_line': 'Empty, being cleaned', 'bill_line': 'Nothing billing',
  'entry': 'Who readies the bed, and how long does it take?', 'entry_hint': 'For example: housekeeping, about 45 minutes'},
 {'key': 'd', 'when': 'Later still', 'title': 'Next patient admitted', 'bed': 'next', 'bill': 'new',
  'text': 'The next patient is admitted. Only now does a new bill open against this bed, and the bed starts earning again.',
  'bed_line': 'Next patient in', 'bill_line': 'New bill opens',
  'entry': 'When does your next patient usually reach the bed?', 'entry_hint': 'For example: around 5 PM, later on busy days'}]
ASK = {'label': 'Anything about your own setup you’d add?', 'hint': 'For example: our ICU works differently'}

BASE = {
 'turn': {'id': 'bm-dg-01', 'type': 'reveal', 'tool': 'Bed Management', 'tab': 'Diagnosis', 'register': 'guided',
          'user_message': 'Beds. That’s the problem I want to work on.',
          'transcript': {'label': 'Transcript turn 7 · the case reveal', 'said': SAID,
                         'note': 'The user’s line is paraphrased in the transcript (“commits to the bed problem”).'}},
 'chat': {
  'text': ['Beds it is. What you’ve described lines up closely with a hospital we worked with.',
           'Let me show you their day rather than describe it. One thing to watch: that bed stopped earning hours before it was empty.',
           'Does that look like your day? If yours is different anywhere, add it on the drawing and it comes into your message.'],
  'note': 'The bed stops earning long before it is empty.',
  'points': [{'n': 1, 'label': 'Late morning, final bill closed', 'canvas': True}, {'n': 2, 'label': 'Afternoon, approval and payment', 'canvas': True},
             {'n': 3, 'label': 'Evening, patient leaves', 'canvas': True}, {'n': 4, 'label': 'Later still, next patient in', 'canvas': True}],
  'prompts': ['Yes, that looks like our day', 'Ours is sometimes even longer', 'What happens next?']},
}
HEAD = {'type': 'heading', 'eyebrow': 'A hospital much like yours', 'title': 'The bed that stopped earning',
        'deck': 'One bed through one day. Watch where the bill stops, and how long it stays stopped.'}
EFFECT = {'type': 'effect', 'label': 'Dead bed time', 'value': 'Last bill closed to next bill opened', 'state': 'outcome',
          'sub': 'Often half a day or more on one bed. Most hospitals have never measured it on its own.'}
CAPTION = 'Nothing bills on this bed across this whole stretch. That includes pharmacy, tests, scans and procedures.'

A = copy.deepcopy(BASE); A['turn']['sample'] = {'letter': 'A', 'name': 'The day on one line',
  'what': 'The library’s time-window: one bed’s day on a single line, the stretch with no bill shaded in red. Tap a moment on the line for its sheet: what the bed and the bill are doing, and Add yours.'}
A['canvas'] = {'blocks': [HEAD, {'type': 'time-window', 'label': 'One bed, one day', 'axis_from': 8, 'axis_to': 24, 'tick': 2,
  'events': [{'time': 11, 'label': 'Bill closed', 'state': 'start', 'point': 1}, {'time': 14, 'label': 'Approval, payment', 'state': 'target', 'point': 2},
             {'time': 19, 'label': 'Patient leaves', 'point': 3}, {'time': 22, 'label': 'Next patient in', 'state': 'outcome', 'point': 4}],
  'window': {'start': 11, 'end': 22, 'label': 'Nothing bills here', 'note': 'The patient is still in the bed for most of it.'},
  'share': {'value': 'Half a day', 'label': 'on one bed, with no bill running'},
  'caption': CAPTION, 'sheets': SHEETS, 'ask_more': ASK}, EFFECT]}

B = copy.deepcopy(BASE); B['turn']['sample'] = {'letter': 'B', 'name': 'Four stops, one bed',
  'what': 'The library’s chain, as the approved transcript drew it: four boxes, the last one red. Each box carries the bed mark and whether anything is billing. Tap a box for its sheet and Add yours.'}
B['canvas'] = {'blocks': [HEAD, {'type': 'chain', 'label': 'One bed, one day',
  'steps': [{'title': 'Final bill closed', 'value': 'Late morning', 'state': 'start', 'point': 1},
            {'title': 'Approval, payment, family briefing', 'value': 'Afternoon', 'state': 'target', 'flag': 'Still in bed', 'point': 2},
            {'title': 'Patient leaves, bed made ready', 'value': 'Evening', 'point': 3},
            {'title': 'Next patient admitted', 'value': 'Later still', 'state': 'outcome', 'point': 4}],
  'caption': CAPTION, 'sheets': SHEETS, 'ask_more': ASK}, EFFECT]}

C = copy.deepcopy(BASE); C['turn']['sample'] = {'letter': 'C', 'name': 'The bed and the bill',
  'what': 'The library’s two-flow: what the bed is doing beside what the bill is doing, row by row. The gap shows in the right column, while the left still has a patient in it. Tap a time of day for its sheet and Add yours.'}
C['canvas'] = {'blocks': [HEAD, {'type': 'two-flow', 'left_title': 'The bed', 'right_title': 'The bill',
  'rows': [{'label': 'Late morning', 'left': 'Patient still in it', 'right': 'Final bill closed, sent for approval', 'right_state': 'start', 'point': 1},
           {'label': 'Afternoon', 'left': 'Patient still in it', 'flag': 'Still in bed', 'right': 'Nothing billing', 'right_state': 'target', 'point': 2},
           {'label': 'Evening', 'left': 'Empty, being cleaned', 'right': 'Nothing billing', 'right_state': 'target', 'point': 3},
           {'label': 'Later still', 'left': 'Next patient in', 'right': 'New bill opens', 'right_state': 'outcome', 'point': 4}],
  'caption': CAPTION, 'sheets': SHEETS, 'ask_more': ASK}, EFFECT]}

A['review'] = {'status': 'approved', 'date': '2026-09-30', 'note': 'Sample A approved by Avishek: the day on one line.'}
B['review'] = {'status': 'not chosen', 'date': '2026-09-30', 'note': 'Kept as a variation: the chain with the Bed Management layer.'}
C['review'] = {'status': 'not chosen', 'date': '2026-09-30', 'note': 'Kept as a variation: the two-flow with the Bed Management layer.'}
for s in (A, B, C):
    fn = os.path.join(HERE, 'bm-dg-01-%s.json' % s['turn']['sample']['letter'])
    json.dump(s, open(fn, 'w', encoding='utf-8'), ensure_ascii=False, indent=1); print('wrote', os.path.basename(fn))
