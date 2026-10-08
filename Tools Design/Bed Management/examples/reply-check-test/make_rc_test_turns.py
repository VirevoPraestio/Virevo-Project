"""
make_rc_test_turns — test turns for rule 09, the reply check (6 Oct 2026).

One practice chat in Bed Management Diagnosis (300-bed hospital, Nagpur), showing every move of the rule:
  rc-01  first message of a new chat: the opening line, then the case reveal
  rc-02  one miss (the user changes the subject): noted, run 1, Tojo carries on and answers it
  rc-03  second miss in a row (the user says Tojo has not understood): reset line, recheck, rework
  rc-10  the 10th counted turn: rating asked first, user says Good, Tojo answers the held message
  rc-20  the 20th counted turn: rating asked first, user says Fine: reset line, recheck, rework
Every canvas is drawn by the Bed Management Diagnosis generator. Specs only; no HTML by hand.
"""
import copy, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
DG = os.path.join(os.path.dirname(HERE), 'diagnosis')
load = lambda f: json.load(open(os.path.join(DG, f), encoding='utf-8'))
PB = 'bed-management-conversation-playbook.md'
REF = 'bed-management.md'

def rc(turn_id, n, run, action, last, ask=None, say=None, sources=None, recheck=None):
    r = {'chat_id': 'test-chat-1', 'turn_id': turn_id, 'user_ref': 'u-test', 'tool': 'Bed Management', 'place': 'diagnosis',
         'counted_turn': n, 'run': run, 'action': action, 'last_reply': last}
    if say: r['say'] = say
    if ask: r['ask'] = ask
    if sources: r['sources'] = sources
    if recheck: r['recheck'] = recheck
    return r

specs = {}

# ---------------------------------------------------------------- rc-01: new chat, opening line, the case reveal
s = load('bm-dg-01-B.json'); s['turn'].pop('sample', None); s['turn'].pop('transcript', None)
s['turn'].update({'id': 'rc-01', 'note_for_review': 'First message of a new chat. The app shows the opening line as its own message, then the case reveal (approved bm-dg-01, Sample B).'})
s['reply_check'] = rc('rc-01', 1, 0, 'answer', {'class': 'no_ask', 'why': 'First message of the chat; there is no earlier turn.'},
    ask={'kind': 'direct_question', 'text': 'Does that look like your day?'}, say='opening',
    sources={'rules': ['09 §2', '06 §6', '08 §8'], 'playbook_step': PB + ' §1, stage 1: case reveal', 'references': [REF + ' §6']})
specs['rc-01'] = s

# ---------------------------------------------------------------- rc-02: one miss, carry on
s = load('bm-dg-02.json'); s['turn'].pop('transcript', None)
s['turn'].update({'id': 'rc-02', 'type': 'question',
    'user_message': 'We have 300 beds and they are always full. Which bed management software would you recommend?',
    'note_for_review': 'Miss 1: the user skips the question and changes the subject to software. Run 1, medium. Tojo does not say so. He answers the software question in one line and carries on with the agenda.'})
s['chat']['text'] = [
    'Software is part of the answer, and we will come to it. Which one fits depends on how your beds move today, so I need that first.',
    'The five areas are under the glass, so you can see where this is going. I’ll take them one at a time.',
    'First one: does the same team handle both your discharges and your admissions, or are those two separate teams?']
s['chat']['prompts'] = ['One team does both', 'Why not start with the software?', 'Two separate teams']
s['reply_check'] = rc('rc-02', 2, 1, 'answer',
    {'class': 'changed_subject', 'quote': 'We have 300 beds and they are always full. Which bed management software would you recommend?',
     'why': 'Skips “does that look like your day” and starts on software.', 'cause': 'missed_the_ask', 'priority': 'medium'},
    ask={'kind': 'question', 'text': 'Does the same team handle both your discharges and your admissions?'},
    sources={'rules': ['06 §3.3', '06 §6 question'], 'playbook_step': PB + ' §1, stage 2: dependency verification', 'references': [REF + ' §7.2']})
specs['rc-02'] = s

# ---------------------------------------------------------------- rc-03: second miss in a row: reset, recheck, rework
r1 = load('bm-dg-01-B.json')['canvas']['actions']
specs['rc-03'] = {
 'turn': {'id': 'rc-03', 'type': 'diagnosis', 'tool': 'Bed Management', 'tab': 'Diagnosis', 'register': 'advisory',
          'user_message': 'No, you are not getting it. I don’t need a questionnaire. I need to know why our beds sit empty for hours.',
          'note_for_review': 'Miss 2 in a row (not understood, high). The app shows the reset line. Tojo rechecks, then answers what was asked: why beds earn nothing for hours. One question only, with Something else.'},
 'chat': {
   'text': ['Then let’s start with the why. In most hospitals your size, the bed stops earning long before it is empty, for four usual reasons.',
            'They feed each other. One of them is usually a rule nobody wrote down: a bed is given only once it is ready. So nobody is called in until late, and the late arrival seems to prove the rule.',
            'Which of the four sounds most like your hospital?'],
   'pointer': 'Tap each reason to see how it keeps a bed from earning.',
   'note': 'The bed stops earning when the bill closes, not when it empties.',
   'question': {'text': 'Which sounds most like you?', 'options': ['A bed is given only once it is ready', 'One team does discharges and admissions', 'Patients stay in bed long after the bill', 'Cleaning starts late', 'Something else']},
   'points': [{'n': 1, 'label': 'Bed given only once ready', 'canvas': True}, {'n': 2, 'label': 'One team for both jobs', 'canvas': True},
              {'n': 3, 'label': 'Bill closed, patient still in bed', 'canvas': True}, {'n': 4, 'label': 'Cleaning told late', 'canvas': True}],
   'prompts': ['A bed is given only once it is ready', 'All four, honestly', 'How much is this costing us?']},
 'canvas': {'blocks': [
   {'type': 'heading', 'eyebrow': 'Why a bed earns nothing for hours', 'title': 'Four reasons, one loop', 'deck': 'The usual reasons in hospitals your size. Not yet checked against yours.'},
   {'type': 'cards', 'label': 'What usually keeps a bed from earning', 'items': [
      {'title': 'Bed given only once ready', 'text': 'Nobody can be called in against a bed until it is nearly free. So arrivals drift to the afternoon.', 'tag': 'Most common', 'point': 1,
       'more_label': 'See how it plays out', 'more_points': ['The bed is put against a name only after the ward says it is ready.', 'So the next patient is called late.', 'The late arrival then seems to prove beds were never free earlier.']},
      {'title': 'One team for both jobs', 'text': 'The same team does discharges in the morning and admissions after. The job with a deadline wins.', 'point': 2,
       'more_label': 'See how it plays out', 'more_points': ['Discharges take the morning, until about noon to 2 PM.', 'Admissions are then booked for later in the day.', 'Two jobs that should overlap run one after the other.']},
      {'title': 'Bill closed, patient still in bed', 'text': 'Billing stops when the final bill closes, late morning. The patient often stays until evening.', 'point': 3,
       'more_label': 'See how it plays out', 'more_points': ['Insurance approval, payment and the family briefing all happen with the patient in the bed.', 'Nothing is charged to that bed all this time.']},
      {'title': 'Cleaning told late', 'text': 'Housekeeping hears only once the patient has left, and may be short at the busy hour.', 'point': 4,
       'more_label': 'See how it plays out', 'more_points': ['The clock for cleaning starts when someone tells housekeeping, not when the patient leaves.', 'Nobody has usually worked out how many beds they can ready at the busiest hour.']}]},
   {'type': 'effect', 'label': 'Dead bed time', 'value': 'Last bill closed to next bill opened', 'state': 'outcome', 'sub': 'Often half a day or more on one bed. Most hospitals have never measured it on its own.'}],
  'actions': {'go': {'detail': 'Next: which reason fits your hospital', 'say': 'The one that fits us best is: '},
              'add': {'detail': 'Tell me what happens with your beds', 'say': 'With our beds, what happens is: '},
              'jump': {'tab': 'Solutions', 'detail': 'How the bed problem could be fixed', 'say': 'Take me to Solutions'}}},
 'reply_check': rc('rc-03', 3, 2, 'reset',
    {'class': 'not_understood', 'quote': 'No, you are not getting it. I don’t need a questionnaire. I need to know why our beds sit empty for hours.',
     'why': 'Says plainly Tojo has missed the point.', 'cause': 'off_playbook', 'priority': 'high'},
    ask={'kind': 'question', 'text': 'Which of the four sounds most like your hospital?'}, say='reset',
    sources={'rules': ['09 §5', '09 §6', '06 §6 diagnosis', '08 §2'], 'playbook_step': PB + ' §2: the diagnosis as its own turn', 'references': [REF + ' §6']},
    recheck={'user_wants': 'To understand why beds earn nothing for hours, before answering more questions.',
             'playbook': 'Tojo kept to the verification agenda after the user asked twice for the cause. Playbook §2 says the mechanism is its own turn and the bill-to-bill loss is the point to make.',
             'reference': 'bed-management.md §6 gives the four usual reasons and says the loss starts when the bill closes, not when the bed empties.',
             'rules': 'The agenda turn answered nothing the user asked. One question at a time still holds; the rework asks one, with Something else.',
             'cause': 'off_playbook',
             'fix_in_chat': 'Name the four usual reasons and the dead bed time first, marked as not yet checked, then ask which fits.'})}

# ---------------------------------------------------------------- rc-10: rating Good, then the held message
s = load('bm-dg-05.json'); s['turn'].pop('transcript', None); s['turn'].pop('redraw_of', None); s['canvas'].pop('tone', None)
s['turn'].update({'id': 'rc-10', 'note_for_review': 'The 10th counted turn. The rating is asked first and the user’s message is held. Good: one short line, then the answer (approved bm-dg-05).'})
t = s['chat']['text']; s['chat']['text'] = ['Thank you. ' + t[0]] + t[1:]
s['reply_check'] = rc('rc-10', 10, 0, 'answer', {'class': 'rating_good', 'quote': 'Good'},
    ask={'kind': 'question', 'text': 'Is there a set way to match tomorrow’s planned admissions against the beds you expect to free up?'},
    sources={'rules': ['09 §4', '06 §4', '06 §6 data-back'], 'playbook_step': PB + ' §1, stage 2: dependency verification', 'references': [REF + ' §7.1', REF + ' §7.2']})
specs['rc-10'] = s

# ---------------------------------------------------------------- rc-20: rating Fine: reset, recheck, rework
s = load('bm-dg-12.json'); s['turn'].pop('transcript', None)
s['turn'].update({'id': 'rc-20', 'type': 'overview', 'register': 'advisory', 'user_message': 'Okay. So what do we actually do about it?',
    'note_for_review': 'The 20th counted turn. Rating first; the user says Fine, so the app shows the reset line. Recheck: the user wants the fix; the last turns ran long. Rework: shorter, the five parts named, nothing else to read.'})
s['chat']['text'] = ['Here is what I’d build. Five parts, and the full design, because your admissions run ahead of the beds that free up overnight.',
                     'Pick the part you care about most, and I’ll take you through just that one.']
s['canvas']['blocks'] = [b for b in s['canvas']['blocks'] if b['type'] != 'scale']
s['canvas']['blocks'] = [b for b in s['canvas']['blocks'] if not (b['type'] == 'effect' and b['label'].startswith('Not an'))]
s['reply_check'] = rc('rc-20', 20, 1, 'reset', {'class': 'rating_fine', 'quote': 'Fine', 'cause': 'too_long', 'priority': 'medium'},
    ask={'kind': 'question', 'text': 'Which part first?'}, say='reset',
    sources={'rules': ['09 §4.3', '09 §6', '06 §10.1'], 'playbook_step': PB + ' §3: five-part solution overview', 'references': [REF + ' §7.4']},
    recheck={'user_wants': 'To move from what is wrong to what to do about it.',
             'playbook': 'The diagnosis is done; playbook §3 says the next turn is the five-part overview, one part per turn after.',
             'reference': 'bed-management.md §7.4: the full design applies; nothing to correct.',
             'rules': 'The last three turns ran over 150 words each, with three blocks under the heading. 06 §5.1 says most turns stay under about 150.',
             'cause': 'too_long',
             'fix_in_chat': 'Two short paragraphs, the five parts and what they are worth, then let the user pick.'})
specs['rc-20'] = s

order = []
for k, v in specs.items():
    json.dump(v, open(os.path.join(HERE, k + '.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    order.append({'file': k + '.json', 'note': v['turn']['note_for_review']})
json.dump({'note': 'Test turns for rule 09, the reply check. One practice chat, Bed Management Diagnosis.', 'turns': order},
          open(os.path.join(HERE, 'turns.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print('wrote', ', '.join(specs))
