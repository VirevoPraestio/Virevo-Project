"""Writes the Bed Management Processes turns (bm-pr-01 to bm-pr-11) and turns.json. 6 Oct 2026, approved by Avishek the same day.

The record stops at transcript turn 31, so these turns follow the prompts of the turn before, starting from bm-au-07's
"How does the day change on the wards?". Content comes only from bed-management.md §7.4.2 (the process changes: allocate
forward and run admissions alongside discharges, the 24-hour and 1 PM signals, OPD prescriptions as the intake, the 5 PM
round, stage times, the bill-close and bill-open join, the desk link), §7.4.3 (who must agree, the Head of Operations,
where the resistance sits), §7.4.4 (the two managers and the Admissions Executives), §8 and transcript turns 22 to 31
(the eight weekly measures, the first step, the four missing numbers). Nagpur figures are the hospital's own; examples
and goals are labelled. Simple English throughout. Draw with: python3 ../../processes-html-generator/bm_processes_html.py build"""
import copy, json, os
HERE = os.path.dirname(os.path.abspath(__file__))

def S(key, when, title, text, lines=(), entry=None, hint=None, ask=None):
    s = {'key': key, 'when': when, 'title': title, 'text': text}
    if lines: s['lines'] = [dict(zip(('label', 'value', 'state'), l)) for l in lines]
    if entry: s['entry'] = entry
    if hint: s['entry_hint'] = hint
    if ask: s['ask'] = {'label': ask[0], 'say': ask[1]}
    return s

JUMP = {'tab': 'Diagnosis', 'detail': 'Back to what is really wrong', 'say': 'Take me to Diagnosis'}
def P(*labels): return [{'n': i + 1, 'label': x, 'canvas': True} for i, x in enumerate(labels)]
def H(eyebrow, title, deck, column, name):
    return {'type': 'heading', 'eyebrow': eyebrow, 'title': title, 'deck': deck, 'plate': {'column': column, 'name': name}}
def turn(n, msg, context, chat, blocks, go, add, note=None):
    s = {'turn': {'id': 'bm-pr-%02d' % n, 'tab': 'Processes', 'type': 'part', 'register': 'advisory', 'tool': 'Bed Management', 'user_message': msg,
                  'context': context, 'transcript': {'label': 'After transcript turn 31 · Processes, turn %d (the record stops at 31)' % n}},
         'chat': chat, 'canvas': {'blocks': blocks, 'actions': {'go': {'detail': go[0], 'say': go[1]}, 'add': {'detail': add[0], 'say': add[1]}, 'jump': copy.deepcopy(JUMP)}}}
    return s
def E(label, value, sub, state='start', look='plate'): return {'type': 'effect', 'label': label, 'value': value, 'sub': sub, 'state': state, 'look': look}

T = []
# ---------------------------------------------------------------------------------------------- 01 · the ward's day on a clock (day-dial)
TIMES = [('09:00', 'Admissions start with discharges', 'Admissions desk', True, 1,
          'The desk starts admitting while the morning discharges run. It admits into beds that will be free, not beds already free.',
          [('Today', 'Admissions start after 1 PM'), ('New', 'From 9 AM', 'start')], 'Who works the desk at 9 AM today?'),
         ('10:00', 'Dates checked on the round', 'Doctors', True, None,
          'On the morning round the doctor sees a likely discharge date for each patient. They confirm it or change it, a day ahead.',
          [('Asked of doctors', 'Check a date, by voice'), ('Extra time', 'None, the round already happens', 'start')], 'When does your morning round end?'),
         ('12:00', 'Admissions done', 'Admissions desk', True, 2,
          'Patients called in for a set time are in bed by about noon. The bill on their bed opens hours earlier.',
          [('Today', 'In bed 4:30 PM, up to 8 PM', 'outcome'), ('Goal', 'In bed by about noon', 'target')], 'What time do most patients reach a bed today?'),
         ('13:00', 'ICU step-down signal', 'ICU doctors', True, 3,
          'ICU patients likely to move to a ward are named by 1 PM. That lets the 2 PM plan count their ICU beds.',
          [('Who', 'ICU in-charge and the treating doctor'), ('Feeds', 'The 2 PM plan')], 'Who decides step-downs in your ICU today?'),
         ('14:00', 'First bed plan', 'Tojo and the Bed Manager', True, 4,
          'The first pass matches tomorrow’s planned patients to beds. Teams are told at once what still has no bed.',
          [('Made by', 'Tojo, checked by the Bed Manager'), ('Goes to', 'Discharge team, Medical Supervisory')], 'How many planned admissions on a usual day?'),
         ('17:00', 'The 5 PM round', 'Medical Supervisory team', True, 5,
          'One round of the beds likely to free tomorrow. Each date is confirmed or corrected by 5 PM.',
          [('Who', 'Medical Supervisory team'), ('Feeds', 'The 6 PM freeze')], 'Who does evening rounds today?'),
         ('18:00', 'Bed plan frozen', 'Bed Manager', True, 6,
          'Tomorrow’s plan is frozen and sent to everyone. Each planned patient gets a call-in time for their bed.',
          [('Goes to', 'Every ward, the desk, Billing'), ('Gives', 'A call-in time per bed', 'start')], 'Who should get the 6 PM plan?')]
T.append(turn(1, 'How does the day change on the wards?',
    'Prompt 1 of bm-au-07. bed-management.md §7.4.2 (allocate forward, admissions alongside discharges, 24-hour signal, 1 PM ICU signal, 5 PM round) and §7.4.1 (2 PM pass, 6 PM freeze, call-in times). Nagpur times from transcript 9 to 13.',
    {'text': ['The work stays the same. What changes is when things are decided, so a bed is given before it is free.'],
     'bullets': ['Today a bed is given out only once it is clean. Your patients reach a bed between 4:30 and 8 PM.',
                 'In the new day, admissions run alongside the morning discharges. Each patient is called in for a set time.',
                 'Six times are fixed each day. They fix when a decision is made, never what the doctor decides.'],
     'invite': 'Next, we can see where on the ward each change happens.',
     'note': 'Same people, same beds. A different order.',
     'points': P('Admissions start at 9 AM', 'Admissions done by noon', 'ICU signal by 1 PM', 'First bed plan, 2 PM', 'The 5 PM round', 'The 6 PM freeze'),
     'prompts': ['Where on the ward does each change happen?', 'Why do our patients still get in so late?', 'What does a doctor have to do?'],
     'pointer': 'Switch between today and the new day. Pick a time to move the clock hand.'},
    [H('Processes · the ward’s day', 'Same work, a different clock', 'The ward’s day from 8 AM to 8 PM. Switch to set today’s admissions against the new ones.', 'Changes', 'The ward’s day'),
     {'type': 'day-dial', 'switch': {'today': 'Today', 'with': 'The new day', 'cap_today': 'Bills close by noon. Patients arrive at 1 PM and reach a bed from 4:30 PM.',
                                     'cap_with': 'Admissions run with the morning discharges. Patients reach a bed by about noon.'},
      'windows': [{'side': 'today', 'from': '09:00', 'to': '12:30', 'label': 'Discharges', 'state': 'plain', 'inner': True},
                  {'side': 'today', 'from': '13:00', 'to': '20:00', 'label': 'Admissions', 'state': 'outcome'},
                  {'side': 'with', 'from': '09:00', 'to': '12:30', 'label': 'Discharges', 'state': 'plain', 'inner': True},
                  {'side': 'with', 'from': '09:00', 'to': '12:00', 'label': 'Admissions', 'state': 'start'}],
      'times_label': 'Fixed times of the new day',
      'times': [dict({'at': a, 'name': n, 'who': w, 'new': nw}, **({'point': p} if p else {})) for a, n, w, nw, p, t, l, q in TIMES],
      'caption': 'Arrival at 1 PM and a bed from 4:30 PM are your times. The new times are the plan, not yet tried.',
      'sheets': [S('t%d' % (i + 1), 'At ' + {'09:00': '9 AM', '10:00': '10 AM', '12:00': 'noon', '13:00': '1 PM', '14:00': '2 PM', '17:00': '5 PM', '18:00': '6 PM'}[x[0]],
                   x[1], x[5], x[6], x[7]) for i, x in enumerate(TIMES)]},
     E('Patient in bed', 'From 4:30 PM to noon', 'Each bed starts earning about four hours earlier. Nothing else about the stay changes.', 'start', 'stamp')],
    ('Next: where each change happens', 'Where on the ward does each change happen?'), ('Tell me how your day runs', 'On our wards today: ')))

# ---------------------------------------------------------------------------------------------- 02 · where each change happens (ward-pins)
ROOMS = [{'area': 'bay', 'name': 'Patient beds', 'kind': 'beds', 'beds': 8}, {'area': 'stn', 'name': 'Nurses’ station', 'kind': 'desk'},
         {'area': 'opd', 'name': 'OPD room', 'kind': 'room'}, {'area': 'adm', 'name': 'Admissions desk', 'kind': 'desk'},
         {'area': 'bil', 'name': 'Billing office', 'kind': 'office'}, {'area': 'icu', 'name': 'ICU', 'kind': 'room'}]
CH = [('Date checked on the round', 1, 'Doctors', 1, 'The doctor sees a likely date for each patient, a day ahead, and confirms or changes it by voice.',
       [('Today', 'Said in passing, not written'), ('New', 'Confirmed 24 hours ahead', 'start')], 'Do doctors mention discharge dates on rounds today?'),
      ('The 5 PM round', 2, 'Medical Supervisory team', 2, 'One fixed round of the beds likely to free tomorrow. It is what lets the plan freeze at 6 PM.',
       [('Today', 'No fixed evening check'), ('New', 'Every day by 5 PM', 'start')], 'Who could do this round on your wards?'),
      ('Admissions written down in OPD', 3, 'OPD doctors', 3, 'When a doctor advises admission, the date, the procedure and the likely stay are written down once.',
       [('Today', 'Stays on paper in OPD'), ('New', 'Feeds the bed plan', 'start')], 'How are planned admissions booked today?'),
      ('Patients called in on time', 4, 'Desk staff', 4, 'The desk calls each patient for the time their bed will be free. It also confirms dates back into the plan.',
       [('Today', 'Told to come at 1 PM'), ('New', 'A time for each bed', 'start')], 'Who calls patients in today?'),
      ('Bill close and open joined', 5, 'Billing', 5, 'One report puts the last bill of one patient and the first bill of the next on the same bed.',
       [('Today', 'Both times exist, never joined'), ('New', 'Dead bed time, every week', 'start')], 'Who runs billing reports today?'),
      ('Step-down named by 1 PM', 6, 'ICU doctors', None, 'ICU patients likely to move to a ward are named by 1 PM, in time for the 2 PM plan.',
       [('Today', 'Decided when a bed is found'), ('New', 'Named by 1 PM', 'start')], 'How many ICU beds do you run?')]
T.append(turn(2, 'Where on the ward does each change happen?',
    'Prompt 1 of bm-pr-01. bed-management.md §7.4.2: the 24-hour signal, the 5 PM round, OPD prescriptions as intake, stage times and the desk link, the bill-close and bill-open join, the 1 PM ICU signal. The drawing comes from the approved Processes landing page B, the trial ward.',
    {'text': ['Six small changes, each in a room you already have. None of them is a new job.'],
     'bullets': ['On the round, the doctor checks a date instead of giving one. That is the change people will feel most.',
                 'At the desk, patients are called in for a time. At billing, one report is added.',
                 'The other three are a time written down, in OPD, at the ICU and at the 5 PM round.'],
     'invite': 'Next, we can see why your patients still get in so late.',
     'points': P('The round', 'The 5 PM round', 'OPD', 'The admissions desk', 'Billing'),
     'prompts': ['Why do our patients still get in so late?', 'What does a doctor have to do?', 'Who needs to agree to this?'],
     'pointer': 'Pick a change to see its pin on the ward.'},
    [H('Processes · where it happens', 'Six pins on one ward', 'Your trial ward seen from above. Each change is pinned in the room where it happens.', 'Changes', 'The trial ward'),
     {'type': 'ward-pins', 'layout': ['bay bay bay stn', 'c c c c', 'opd adm bil icu'], 'rooms': ROOMS, 'corridor': 'Corridor',
      'plan_label': 'A ward drawn as an example. Every ward in your hospital has these rooms.', 'changes_label': 'Six small changes',
      'changes': [dict({'name': n, 'room': r, 'who': w}, **({'point': p} if p else {})) for n, r, w, p, t, l, q in CH],
      'rule': 'Each change is a time, or a thing written down, inside work people already do. Nobody gets a new job.',
      'sheets': [S('c%d' % (i + 1), x[2], x[0], x[4], x[5], x[6]) for i, x in enumerate(CH)]}],
    ('Next: why patients still get in late', 'Why do our patients still get in so late?'), ('Tell me how a ward runs here', 'On our wards: ')))

# ---------------------------------------------------------------------------------------------- 03 · why patients still get in late (swap)
ROWS = [('Bed given out', 'Admissions desk', 'When it is clean and ready', '3 to 4 PM', 'When it will be free', 'By 10 AM', 'The big one', 1,
         'This one rule causes the late afternoon. A bed is only given once it is ready, so every step after it waits.',
         [('Today', 'Given when ready'), ('New', 'Given against its free time', 'start')], 'Who decides a bed is ready today?'),
        ('Patient called in', 'Admissions desk', 'Told to come at 1 PM', None, 'Given a time for their bed', '9 to 11 AM', None, 2,
         'Today every patient is told the same time. With a free time for each bed, each patient gets their own.',
         [('Today', 'One time for all'), ('New', 'One time per bed', 'start')], 'What time are patients told to come today?'),
        ('Admission papers', 'Admissions desk', 'Done once the bed is ready', None, 'Done before the bed is free', None, None, 3,
         'Papers take about an hour of your 3½ hours. Done while the bed is still being cleaned, they stop adding to the wait.',
         [('Paperwork today', 'About 1 hour of 3½'), ('New', 'Done while the bed is cleaned', 'start')], 'Which paper takes longest at your desk?'),
        ('Bed cleaned', 'Housekeeping', 'When someone calls them', None, 'Told when the patient leaves', None, None, None,
         'Housekeeping hears the leaving time from the plan. They are at the bed when it empties.',
         [('Today', 'Called when someone notices'), ('New', 'Told from the plan', 'start')], 'How does housekeeping hear a bed is empty?'),
        ('First bill on bed', 'Billing', 'Opened from 5 PM', None, 'Opened by about noon', None, None, 4,
         'The bed earns again only when the new bill opens. Bringing it to noon is the money in this whole change.',
         [('Today', 'From 5 PM, up to 8 PM', 'outcome'), ('Goal', 'By about noon', 'target')], 'When does the first charge go on today?')]
T.append(turn(3, 'Why do our patients still get in so late?',
    'Prompt 1 of bm-pr-02. Transcript 9 (one team, both jobs at once), 11 (the filled chain) and 22 (allocate forward). bed-management.md §7.2 question 8: a claimed overlap tested against the clock, and the rule that beds are not given until ready.',
    {'text': ['You already run discharges and admissions together. The wait comes from one rule: a bed is given only once it is ready.'],
     'bullets': ['Every step after that rule waits for it. So patients reach a bed between 4:30 and 8 PM.',
                 'Give the bed against the time it will be free. The papers and the call-in can then happen first.',
                 'The same team, beds and patients give a different day. It costs nothing but the new order.'],
     'invite': 'Next, we can look at what a doctor is asked to do.',
     'points': P('Bed given out', 'Patient called in', 'Admission papers', 'First bill on the bed'),
     'prompts': ['What does a doctor have to do?', 'What if a bed is not free in time?', 'Who needs to agree to this?'],
     'pointer': 'Move each magnet, or switch to move them all.'},
    [H('Processes · the one rule', 'One rule keeps the day late', 'Each step of an admission, today and with the change. Move a magnet to see what changes.', 'Changes', 'The admission'),
     {'type': 'swap', 'with_label': 'With the change',
      'rows': [dict({'name': n, 'who': w, 'today': t, 'with': wi}, **({'today_at': ta} if ta else {}), **({'with_at': wa} if wa else {}), **({'flag': f} if f else {}), **({'point': p} if p else {}))
               for n, w, t, ta, wi, wa, f, p, tx, l, q in ROWS],
      'keeps': 'The same team, the same beds and the same patients. Only the order changes, and the new order costs nothing.',
      'condition': 'Arrive 1 PM, in bed 4:30 PM, first bill 5 PM are your times. The new times are the plan.',
      'sheets': [S('r%d' % (i + 1), x[1], x[0], x[8], x[9], x[10]) for i, x in enumerate(ROWS)]},
     E('What it costs', 'Nothing but the new order', 'No hire and no system. The loss it removes comes from a rule, so changing the rule removes it.', 'start', 'banner')],
    ('Next: what a doctor does', 'What does a doctor have to do?'), ('Tell me about your bed rule', 'Our rule for giving a bed is: ')))

# ---------------------------------------------------------------------------------------------- 04 · the doctor's round (round-cards)
PTS = [('3-12', 'Knee replacement', 'Orthopaedics team', 4, 5, 'Tomorrow, 11 AM', 'Knee patients here stay about 5 days', 1,
        'The date comes from your own past knee patients and this patient’s notes. The doctor only checks it.', [('Based on', 'Past stays, today’s notes')], 'Is this how your knee patients go?'),
       ('3-14', 'Gall bladder removal', 'Surgery team', 2, 3, 'Tomorrow, 10 AM', 'Usual stay 3 days, notes normal', 2,
        'A short, regular stay. These are the dates most often confirmed with one word.', [('Based on', 'Past stays, today’s notes')], 'Which stays are most regular for you?'),
       ('3-03', 'Chest infection', 'Medicine team', 5, 7, 'In two days', 'No fever for one day', None,
        'Medical stays move more. A date that is changed is still useful. It goes into the next plan.', [('Often', 'Changed once, then confirmed')], 'Which wards have the longest stays?'),
       ('3-08', 'Angioplasty', 'Cardiology team', 2, 3, 'Tomorrow, noon', 'Usual stay 3 days after the procedure', None,
        'Planned procedures give the steadiest dates. They are where the plan gets most of its beds.', [('Based on', 'Past stays, today’s notes')], 'How many angioplasties in a usual week?'),
       ('3-17', 'Hip fracture', 'Orthopaedics team', 6, 8, 'In two days', 'Walking check due tomorrow', 3,
        'If the walking check is not passed, the doctor changes the date. The bed plan moves with it.', [('If changed', 'The plan runs again', 'start')], 'Who does the walking check?'),
       ('3-05', 'Diabetes control', 'Medicine team', 3, 4, 'Tomorrow, 4 PM', 'Sugar steady for two days', None,
        'A late date still helps. The bed can be planned for an evening patient instead of left to chance.', [('Based on', 'Readings and past stays')], 'Are evening admissions common here?')]
T.append(turn(4, 'What does a doctor have to do?',
    'Prompt 2 of bm-pr-03. bed-management.md §7.4.3: doctors speak on the round, and the agent shows a predicted date and summary for each patient. Transcript 23 and 27: show a date to confirm or correct, never ask for one.',
    {'text': ['On the round the doctor speaks as usual. Tojo writes it down and shows a likely date for each patient.'],
     'bullets': ['The doctor confirms the date or changes it. Checking a date is quick. Making one up a day early is not.',
                 'A changed date is fine. It is not a rule broken, it just goes into the next plan.',
                 'If the round gets longer, something is wrong, and we change it.'],
     'invite': 'Next, we can see what happens when a doctor will not confirm.',
     'note': 'Ask a doctor to check a date, never to make one up.',
     'points': P('A knee patient', 'A short surgical stay', 'A stay that may change'),
     'prompts': ['What if a doctor will not confirm a date?', 'Where do planned admissions come from?', 'Will this slow the round?'],
     'pointer': 'Confirm a date, or change it and type the new one. Pick a patient to see where the date comes from.'},
    [H('Processes · the doctor’s round', 'Check a date, do not make one', 'One round, six patients. Each card shows the likely date. The doctor confirms or changes it.', 'People', 'The doctor’s round'),
     {'type': 'round-cards', 'round_label': 'Speak on the round.', 'round_line': 'Tojo writes it down. The doctor only checks each date.',
      'predicted_label': 'Likely home', 'confirm': 'Confirm', 'change': 'Change', 'stamp': 'Confirmed',
      'patients': [dict({'bed': b, 'what': w, 'doctor': d, 'day': dy, 'of': of, 'predicted': pr, 'basis': ba}, **({'point': p} if p else {})) for b, w, d, dy, of, pr, ba, p, t, l, q in PTS],
      'rule': 'The clinical call stays with the treating doctor. A changed date is logged, not a rule broken.',
      'caption': 'Example patients, to show the round. Your own patients show once read access is in.',
      'sheets': [S('p%d' % (i + 1), 'Bed ' + x[0], x[1], x[8], x[9], x[10]) for i, x in enumerate(PTS)]},
     E('Extra time on the round', 'None', 'The round already happens. If it takes longer, that is a fault to fix, not a cost to accept.', 'start', 'ticket')],
    ('Next: when a doctor will not confirm', 'What if a doctor will not confirm a date?'), ('Tell me how your rounds run', 'Our rounds run like this: ')))

# ---------------------------------------------------------------------------------------------- 05 · when a doctor will not confirm (loop)
LOOP = [('No date given', 'Doctor, morning round', 1, 'The doctor is busy or unsure. Nothing breaks. The patient simply has no confirmed date yet.', [('Happens', 'Often, at the start')], 'Which teams would confirm least at first?'),
        ('Likely date used', 'Tojo', 2, 'Tojo uses the usual stay for this kind of patient. The bed is planned as likely, not confirmed.', [('Marked', 'Likely, not confirmed', 'target')], 'Do you track usual stays by procedure?'),
        ('Checked at 5 PM', 'Medical Supervisory team', 3, 'The 5 PM round asks the doctor once more. Most dates are settled here, before the freeze.', [('By', '5 PM, every day')], 'Who would ask the doctor at 5 PM?'),
        ('Planned as confirmed', 'Bed Manager', None, 'The bed goes into the 6 PM plan with a call-in time for the next patient.', [('Gives', 'A call-in time', 'start')], 'Who sends call-in times today?'),
        ('Likely, asked again', 'Bed Manager and doctor', 4, 'The bed stays in the plan as likely. No patient is called in for it until the doctor confirms next morning.', [('Patient called', 'Only once confirmed', 'target')], 'How often would a likely bed be wrong?')]
T.append(turn(5, 'What if a doctor will not confirm a date?',
    'Prompt 1 of bm-pr-04. Transcript 23: what is fixed is when a decision is made, not what is decided; a step-down that slips is an input to the next pass. bed-management.md §7.4.2: the 5 PM round confirms or corrects predictions. The evening background starts here.',
    {'text': ['Then the bed is planned as likely, not confirmed. Nobody is called in for it until a doctor says yes.'],
     'bullets': ['Tojo uses the usual stay for that kind of patient, from your own past patients.',
                 'The 5 PM round asks once more. Most dates are settled there, before the 6 PM freeze.',
                 'If it is still open, it is asked again next morning. A missed date is logged, not punished.'],
     'invite': 'Next, we can see where the planned admissions come from.',
     'points': P('No date on the round', 'A likely date', 'The 5 PM check', 'Asked again'),
     'prompts': ['Where do planned admissions come from?', 'Who needs to agree to this?', 'How often will a likely bed be wrong?'],
     'pointer': 'Step round the loop. At the 5 PM check, pick an answer to see where it goes.'},
    [H('Processes · a date not given', 'No date is not a breakdown', 'What happens to one bed when the doctor does not confirm. Step round it.', 'Changes', 'A date not given'),
     {'type': 'loop', 'at': 0, 'sub': 'Every day, before 6 PM',
      'steps': [dict({'name': n, 'who': w}, **({'point': p} if p else {})) for n, w, p, t, l, q in LOOP],
      'gate': {'at': 2, 'question': 'Did the doctor confirm by 5 PM?', 'yes': 'Yes, confirmed', 'no': 'Not yet', 'yes_to': 3, 'no_to': 4, 'retry_to': 0},
      'sheets': [S('s%d' % (i + 1), 'Step %d of 5' % (i + 1), x[0], x[3], x[4], x[5]) for i, x in enumerate(LOOP)]},
     {'type': 'notes', 'label': 'Two things this keeps apart',
      'items': [{'tag': 'Stays fixed', 'title': 'When a decision is made', 'text': 'The 1 PM, 2 PM, 5 PM and 6 PM times stay the same every day.', 'state': 'plain'},
                {'tag': 'Never fixed', 'title': 'What the doctor decides', 'text': 'Who is fit to go home, and when, stays with the treating doctor.', 'state': 'muted'}],
      'sheets': [S('n1', 'Stays fixed', 'When a decision is made', 'The plan needs its answers by set times. The times stay the same, busy day or quiet day.', [('Times', '1 PM, 2 PM, 5 PM, 6 PM')], 'Which of these times would be hardest here?'),
                 S('n2', 'Never fixed', 'What the doctor decides', 'The plan never decides who goes home. It only asks by when the doctor will say.', [('Decides', 'The treating doctor')], 'Where do you expect pushback?')]}],
    ('Next: where planned admissions come from', 'Where do planned admissions come from?'), ('Tell me how often dates change', 'Discharge dates here change because: ')))

# ---------------------------------------------------------------------------------------------- 06 · the OPD slip (slip)
FIELDS = [('Procedure', 'Knee replacement', 'Which kind of bed', 1, 'The procedure tells the plan which ward and which kind of bed.', [('Feeds', 'Ward and bed type')], 'Which procedures fill most of your beds?'),
          ('Admit on', 'Thursday, 10 AM', 'Which day', 2, 'The day lets the bed be held days ahead, not found on the morning.', [('Today', 'Found on the day'), ('New', 'Held days ahead', 'start')], 'How far ahead are admissions booked?'),
          ('Likely stay', '5 days', 'When the bed frees again', 3, 'The likely stay tells the plan when this bed will be free for the next patient.', [('Feeds', 'The next free time')], 'Do OPD doctors write a likely stay today?'),
          ('Operation theatre', 'Friday morning', 'Theatre slot held', None, 'A theatre slot booked with the bed, so the stay does not start with a wait.', [('Feeds', 'The theatre list')], 'Who books theatre slots today?'),
          ('ICU after?', 'No', 'ICU bed or not', 4, 'If an ICU bed is needed after the procedure, it is planned with the ward bed.', [('Feeds', 'The ICU plan')], 'How often do planned patients need ICU?'),
          ('Paid by', 'Insurance', 'Approval started early', None, 'Insurance approval can start before the patient arrives, not on the day.', [('Feeds', 'The insurance desk')], 'How long do approvals take here?')]
T.append(turn(6, 'Where do planned admissions come from?',
    'Prompt 2 of bm-pr-04 and bm-pr-05. bed-management.md §7.4.2: OPD prescriptions become the intake point for planned-admission data (date, procedure, likely stay, theatre need); the desk confirms back with a tentative bed. The slip is an example.',
    {'text': ['From the OPD slip. When a doctor advises admission, the slip already holds most of what the bed plan needs.'],
     'bullets': ['Today those details stay on paper in OPD. The bed is found on the day the patient comes.',
                 'Written down once, they let the plan hold a bed days ahead. The theatre and insurance can start early too.',
                 'When the patient books at the desk, the date is confirmed back. A bed number is attached at once.'],
     'invite': 'Next, we can see who needs to agree to all this.',
     'points': P('The procedure', 'The admission day', 'The likely stay', 'ICU after or not'),
     'prompts': ['Who needs to agree to this?', 'Who would write this down in OPD?', 'What if the patient does not come?'],
     'pointer': 'Pick a line of the slip to see what it feeds. Then pull the slip into the bed plan.'},
    [H('Processes · where it starts', 'The bed plan starts in OPD', 'One OPD slip, and what each line gives the bed plan. Pull it across to see.', 'Changes', 'The OPD slip'),
     {'type': 'slip', 'slip_title': 'OPD prescription · Orthopaedics', 'slip_sub': 'An example slip, written in OPD on Tuesday', 'slip_foot': 'OPD doctor', 'pull': 'Pull into the bed plan',
      'fields': [dict({'label': l, 'value': v, 'feeds': f}, **({'point': p} if p else {})) for l, v, f, p, t, li, q in FIELDS],
      'plan': {'label': 'Bed plan · Thursday', 'title': 'One planned admission', 'bed_label': 'Bed held', 'bed': '3-12', 'bed_note': 'Held for now. Confirmed when the patient books in.'},
      'rule': 'The details are written once, in OPD. The plan, the theatre and the insurance desk all read the same slip.',
      'sheets': [S('f%d' % (i + 1), 'Line %d' % (i + 1), x[0], x[4], x[5], x[6]) for i, x in enumerate(FIELDS)]},
     E('Planned admissions with a slip', 'Measured from day one', 'Nobody counts this today. Without it, the bed plan has nothing to plan from.', 'target', 'meter')],
    ('Next: who needs to agree', 'Who needs to agree to this?'), ('Tell me how OPD books admissions', 'In our OPD, admissions are booked like this: ')))

# ---------------------------------------------------------------------------------------------- 07 · who must agree (badges)
PPL = [('Head of Operations', 'Signs off', 'to_ask', False, 1, 'Approves the new order of the day. Without that sign-off, the old order comes back on the first busy day.',
        [('Asked', 'Approve the new order'), ('Daily work', 'None', 'start')], 'Who is your Head of Operations?'),
       ('Doctors', 'On the wards', 'worried', True, 2, 'The pushback sits here. Naming a date a day early is a clinical call. A date to check is easier than one to make.',
        [('Asked', 'Check a date on the round'), ('Worry', 'Being held to a date', 'target')], 'Which doctors would agree first?'),
       ('Medical Supervisory team', 'On the wards', 'to_ask', True, 3, 'One round at 5 PM of the beds likely to free tomorrow. That is the new part of their day.',
        [('Asked', 'The 5 PM round')], 'Who leads Medical Supervisory today?'),
       ('ICU doctors', 'On the wards', 'to_ask', False, None, 'Name the ICU patients likely to move to a ward, by 1 PM.', [('Asked', 'A name by 1 PM')], 'Who runs your ICU?'),
       ('Admissions desk', 'At the desks', 'to_ask', True, 4, 'Calls each patient in for a time. Confirms dates back into the plan.', [('Asked', 'Call in by the plan')], 'How many people work the desk?'),
       ('Discharge team', 'At the desks', 'to_ask', True, None, 'Gets a time to have each bed ready, instead of a surprise.', [('Gets', 'A release time per bed', 'start')], 'Who runs discharges on the wards?'),
       ('Billing', 'At the desks', 'to_ask', False, None, 'Runs one new report: last bill and first bill against the same bed.', [('Asked', 'One report')], 'Who runs billing reports?'),
       ('OPD doctors', 'Behind the scenes', 'to_ask', False, None, 'Write the date, the procedure and the likely stay on the slip.', [('Asked', 'Three lines on a slip')], 'Which OPD books most admissions?'),
       ('IT team', 'Behind the scenes', 'to_ask', False, 5, 'Gives read access, about two weeks of work. Then nothing daily.', [('Asked', 'Read access, once')], 'Who looks after your systems?')]
T.append(turn(7, 'Who needs to agree to this?',
    'Prompt 2 of bm-au-07, again in bm-pr-02, 03, 05 and 06. bed-management.md §7.4.3 (the teams, the Head of Operations approves the flows, resistance concentrates with doctors). Transcript 27 (Key people, rebuilt for both sides).',
    {'text': ['Nine groups touch this. Nobody gets a new job. Each confirms something the plan has already worked out.'],
     'bullets': ['The pushback sits with the doctors. Not the speaking, but naming a date a day early.',
                 'The Head of Operations signs off the new order. Without that, it will not survive the first busy day.',
                 'Four groups are in the trial on one ward. The rest join when it spreads.'],
     'invite': 'Next, we can look at whether you need to hire anyone.',
     'points': P('Head of Operations', 'Doctors', 'Medical Supervisory', 'Admissions desk', 'IT team'),
     'prompts': ['Do we need to hire anyone?', 'What if the doctors still refuse?', 'How would we know it is working?'],
     'pointer': 'Pick a name badge to see what changes for that person.'},
    [H('Processes · who says yes', 'Nine groups, one signature', 'Everyone this touches, grouped by where they work. Filter to see who is in the trial.', 'People', 'Who says yes'),
     {'type': 'badges', 'people': [dict({'name': n, 'group': g, 'status': s, 'trial': tr}, **({'point': p} if p else {})) for n, g, s, tr, p, t, l, q in PPL],
      'rule': 'Nobody gets a new job. What changes is when they confirm something. The Head of Operations signs off the new order.',
      'sheets': [S('b%d' % (i + 1), x[1], x[0], x[5], x[6], x[7]) for i, x in enumerate(PPL)]},
     E('Where the pushback sits', 'A date named a day early', 'Not the speaking on the round. Show a date to check and it holds. Ask for one and it will not.', 'target', 'plate')],
    ('Next: do we need to hire anyone', 'Do we need to hire anyone?'), ('Tell me who would push back', 'The people who would push back here are: ')))

# ---------------------------------------------------------------------------------------------- 08 · the roles (seats)
T.append(turn(8, 'Do we need to hire anyone?',
    'Prompt 1 of bm-pr-07 (and bm-so-04). bed-management.md §7.4.4: the Bed Manager on any one of three triggers (₹4 to 4.5 lakh), Admissions Executives sized by the peak hour (₹3 to 3.5 lakh each), scope added for everyone else. Transcript 22 and 28: two managers as peers, three on the afternoon desk, ₹17 to 19.5 lakh, Discharge Executives not yet sized.',
    {'text': ['Two managers, and three people on the afternoon desk. The discharge desk is sized once we have your times.'],
     'bullets': ['A Bed Manager owns the plan from the OPD slip to the bed. Two of the three triggers are met on your numbers.',
                 'A Discharge Manager owns each discharge, so the plan runs on real times. Neither manager reports to the other.',
                 'Three Admissions Executives cover your afternoon peak. One person handles about 5 admissions an hour.'],
     'invite': 'Next, we can see how you would know it is working.',
     'points': P('The Bed Manager', 'Its triggers', 'The Discharge Manager', 'Admissions Executives'),
     'prompts': ['How would we know it is working?', 'Can someone we already have do this?', 'Why not one manager for both?'],
     'pointer': 'Pick a role to open it. Its lamps show which triggers your numbers meet.'},
    [H('Processes · the roles', 'Two managers, one desk sized', 'The new roles as chairs at the station. Lamps show which triggers your own numbers meet.', 'Roles', 'Who runs it'),
     {'type': 'seats', 'hint': 'Pick a role to open it. The lamps show which triggers your numbers meet.', 'reports_to': {'name': 'Head of Operations', 'does': 'Both managers report here, as peers.'},
      'roles': [{'name': 'Bed Manager', 'seats': 1, 'cost_low': 4, 'cost_high': 4.5, 'state': 'needed', 'does': 'Owns the bed plan, from OPD slip to bed. Runs the 2 PM and 6 PM plans.', 'rule': 'Any one is enough', 'point': 1,
                 'triggers': [{'label': 'More admissions than empty beds', 'value': '41 to about 33', 'state': 'met', 'source': 'derived', 'point': 2},
                              {'label': 'Beds more than 80% full', 'value': '89%', 'state': 'met', 'source': 'yours'},
                              {'label': 'Over half of admissions run late', 'state': 'unknown', 'source': 'needed'}]},
                {'name': 'Discharge Manager', 'seats': 1, 'cost_low': 4, 'cost_high': 4.5, 'state': 'needed', 'does': 'Owns each discharge, so the bed plan runs on real times, not guesses.', 'rule': 'Any one is enough', 'point': 3,
                 'triggers': [{'label': 'More than 40 discharges a day', 'value': 'About 41', 'state': 'met', 'source': 'derived'},
                              {'label': 'Beds more than 80% full', 'value': '89%', 'state': 'met', 'source': 'yours'}]},
                {'name': 'Admissions Executives', 'seats': 3, 'cost_low': 3, 'cost_high': 3.5, 'each': True, 'state': 'needed', 'does': 'Run the desk through the afternoon peak. One person handles about 5 an hour.',
                 'note': 'Sized on your busiest hour, not the minimum cover.', 'point': 4},
                {'name': 'Discharge Executives', 'seats': 2, 'cost_low': 3, 'cost_high': 3.5, 'each': True, 'state': 'check', 'does': 'Sized once we know when your discharges happen through the day.',
                 'note': 'Not in the cost yet, on purpose.'}],
      'others': 'OPD, Medical Supervisory, the desk and Billing each record a little more. That is a wider job, not a new one.',
      'sheets': [S('bm', 'Needed now', 'Bed Manager', 'Owns the whole bed plan, end to end. Any one trigger is enough, and two are met on your numbers.',
                   [('Cost', 'About ₹4 to 4.5 lakh a year'), ('Triggers met', 'Two of three', 'start')], 'Could someone you have take this role?'),
                 S('dm', 'Needed now', 'Discharge Manager', 'Makes discharge times something the bed plan can trust. A peer of the Bed Manager, not under it.',
                   [('Cost', 'About ₹4 to 4.5 lakh a year'), ('Reports to', 'Head of Operations')], 'Who runs discharges today?'),
                 S('ae', 'Needed now', 'Admissions Executives', 'About 41 admissions a day, arriving over a short window. The busiest hour needs three people at 5 an hour each.',
                   [('Cost', 'About ₹3 to 3.5 lakh each a year'), ('Sized by', 'Your busiest hour')], 'How many people are on the desk at 2 PM?'),
                 S('de', 'Needs your numbers', 'Discharge Executives', 'The usual rule says one for every 15 discharges a day. At another hospital the real answer was lower, once its busy hours were known.',
                   [('Need from you', 'When discharges happen in a day', 'target')], 'When do most discharges happen here?')]},
     E('Cost of the new roles', '₹17 to 19.5 lakh yearly', 'Two managers and three Admissions Executives. This is the full cost, not the extra cost, until we know who is on each desk today.', 'target', 'ticket')],
    ('Next: how we would know it works', 'How would we know it is working?'), ('Tell me who is on the desk now', 'On our desk today we have: ')))

# ---------------------------------------------------------------------------------------------- 09 · the measures (readouts)
MS = [('Dead bed time, bill to bill', None, 'new', 'new', 'trial', 1, 'From the last bill of one patient to the first bill of the next, on the same bed. The one number that moves when the others improve.',
       [('Today', 'Nobody measures it'), ('Your guess', '4 to 5 hours, up to 8')], 'Has billing ever looked at this?'),
      ('Admission time, step by step', None, 'new', 'new', 'trial', None, 'Your 3½ hours, split into its five steps. It shows paperwork apart from waiting.',
       [('Your guess', 'About 3½ hours, 1 hour papers')], 'Which step do you think is slowest?'),
      ('Beds planned by 6 PM', None, 'new', 'new', 'trial', 2, 'How many of tomorrow’s planned patients have a bed by 6 PM. An early warning if it slips.',
       [('Read', 'Every evening')], 'How many planned admissions in a usual day?'),
      ('Discharge dates given a day ahead', None, 'new', 'new', 'trial', 3, 'How many discharges had a confirmed date 24 hours before. Shows if the round is working.',
       [('Read', 'Every morning')], 'How many discharges have a date today?'),
      ('Admissions finished by noon', None, 'new', 'new', 'trial', 4, 'The share of planned patients in bed by about noon. Shows if the new order is holding.',
       [('Today', 'In bed 4:30 PM, up to 8', 'outcome')], 'How many patients are in bed by noon today?'),
      ('Likely stay against real stay', None, 'new', 'new', 'later', None, 'How close the likely dates were to the real ones, by procedure. Keeps the predictions honest.',
       [('Read', 'Every month, after the trial')], 'Which procedures vary most?'),
      ('Bed occupancy', '89%', 'confirmed', 'yours', 'later', 5, 'Tracked as it is today. Not expected to rise much. That is not what this work does.',
       [('Your number', '89%, ICU 94%')], 'Who reports occupancy today?'),
      ('Average length of stay', '6.5 days', 'confirmed', 'yours', 'later', None, 'Tracked as it is today. It may fall a little. That gain is already counted once in the money.',
       [('Your number', '6.5 days')], 'Is length of stay tracked by ward?')]
T.append(turn(9, 'How would we know it is working?',
    'Prompt 3 of bm-au-07 and bm-pr-07. Transcript 29 (eight numbers, checked weekly, six new; occupancy and stay tracked, not promised) and bed-management.md §8 (with dead bed time and stage times added, as agreed). The day background returns here.',
    {'text': ['Eight numbers, read every week. Six of them nobody measures today.'],
     'bullets': ['Start with dead bed time. It moves when any of the others improve, and both halves sit in your billing system.',
                 'Three numbers check people are doing the new thing. If they slip, the rest follows within a fortnight.',
                 'Occupancy and length of stay are tracked, not promised. This work moves time and billing.'],
     'invite': 'Next, we can plan a trial on one ward.',
     'points': P('Dead bed time', 'Beds planned by 6 PM', 'Dates a day ahead', 'Admissions by noon', 'Occupancy'),
     'prompts': ['Can we try it on one ward first?', 'Who would read these each week?', 'Why weekly, not monthly?'],
     'pointer': 'Pick a window to see how it is measured. Switch to see which are read in the trial.'},
    [H('Processes · the measures', 'Eight windows, read weekly', 'Each measure as a window on the station wall. Six are new and start with no number.', 'Measures', 'What we read'),
     {'type': 'readouts', 'measures': [dict({'name': n, 'state': st, 'source': so, 'when': w}, **({'value': v} if v else {}), **({'point': p} if p else {})) for n, v, st, so, w, p, t, l, q in MS],
      'condition': 'Read every week, not every month. A month hides a bad week.',
      'sheets': [S('m%d' % (i + 1), 'In the trial' if x[4] == 'trial' else 'After the trial', x[0], x[6], x[7], x[8]) for i, x in enumerate(MS)]},
     E('Expected to change', 'Time and billing, not occupancy', 'Occupancy will not go up. Patients reach a bed earlier, and each bed earns for more of the day.', 'outcome', 'banner')],
    ('Next: a trial on one ward', 'Can we try it on one ward first?'), ('Tell me what you track now', 'We already track these: ')))

# ---------------------------------------------------------------------------------------------- 10 · the trial (trial)
PH = [(1, 3, 'Record the day as it runs', 'Ward nurse in charge', 2, 'Nothing changes yet. The ward records when each bed frees and when each patient reaches a bed.',
       [('Recorded', 'Bed free, patient in bed, bills')], 'What would get in the way on these days?'),
      (4, 7, 'Dates checked on the round', 'Doctors, Medical Supervisory', 3, 'Doctors check likely dates on the round. The 5 PM round starts. The plan is made but nobody is called in by it yet.',
       [('Watch', 'Dates given a day ahead')], 'Which doctor would start this best?'),
      (8, 11, 'Patients called in by the plan', 'Admissions desk', 4, 'The desk calls planned patients in for their bed’s time. This is where the day changes.',
       [('Watch', 'Admissions finished by noon', 'target')], 'Who on the desk would run this?'),
      (12, 14, 'Read the numbers', 'You, the ward and Tojo', None, 'Dead bed time and admission times, before and after. Then you decide whether it spreads.',
       [('Read', 'Your own before and after', 'start')], 'Who should see the result?')]
T.append(turn(10, 'Can we try it on one ward first?',
    'Prompt 1 of bm-pr-09. Transcript 31: step 3 is where the day changes, after read access and four weeks of measuring. The trial is that step on one ward; goals are set from the ward’s own first days.',
    {'text': ['Yes. Two weeks on one ward, once read access is in and your four weeks of numbers are measured.'],
     'bullets': ['The first three days only record the day as it runs. Nothing changes for anyone.',
                 'Then dates are checked on the round, and after that the desk calls patients in by the plan.',
                 'On day 14 you read dead bed time and admission times, before and after.'],
     'invite': 'Last, we can list what we need from you to start.',
     'points': P('The trial ward', 'Recording the day', 'Dates on the round', 'Calling in by the plan'),
     'prompts': ['What do you need from us to start?', 'Which ward should we pick?', 'What if the trial goes badly?'],
     'pointer': 'Play the two weeks, or pick a part of the trial.'},
    [H('Processes · the trial', 'Two weeks on one ward', 'The trial as a strip of days. Play it to see each part start.', 'The trial', 'One ward first'),
     {'type': 'trial', 'days': 14,
      'ward': {'label': 'The ward with most planned admissions', 'status': 'needed', 'note': 'Most planned patients means the change shows fastest. You pick the ward.', 'ask': 'Which ward would you start on?', 'ask_hint': 'Type the ward’s name', 'point': 1},
      'needs': ['Read access already in', 'Four weeks of your numbers', 'One name to own it', 'No new staff for the trial'],
      'phases': [dict({'from': a, 'to': b, 'title': t, 'who': w}, **({'point': p} if p else {})) for a, b, t, w, p, tx, l, q in PH],
      'condition': 'Goals are set on day 3 from the ward’s own times. None are guessed now.',
      'sheets': [S('p%d' % (i + 1), ('Days %d to %d' % (x[0], x[1])), x[2], x[5], x[6], x[7]) for i, x in enumerate(PH)]}],
    ('Next: what you need from us', 'What do you need from us to start?'), ('Tell me about our wards', 'The ward I would start on is: ')))

# ---------------------------------------------------------------------------------------------- 11 · what we need (clipboard)
ASKS = [('One name to own this', 'Until the managers join', 'Name and role', 1, 'Someone has to own the plan until the managers join. It can be a person you already have.', [('Needed for', 'Step 1')], None),
        ('Who in IT gives read access', 'Step 1, about two weeks', 'Name in IT', 2, 'Read access to admissions, discharges, billing and the bed board. Nothing is changed in your systems.', [('Needed for', 'Step 1')], None),
        ('Desk roster on each shift', 'Admissions and discharge desks', 'Like 2 morning, 3 afternoon', 3, 'Turns the cost from a total into a difference. Today we count every seat as new.', [('Changes', 'The cost of the roles', 'target')], None),
        ('When patients arrive, by hour', 'A normal weekday', 'Busiest hours', None, 'Checks the three Admissions Executives against your real busiest hour.', [('Changes', 'The desk size')], None),
        ('Bed moves inside the hospital', 'Transfers on a normal day', 'About how many a day', None, 'The desk also handles moves between wards. They count in the busiest hour.', [('Changes', 'The desk size')], None),
        ('When discharges happen', 'Through a normal day', 'Busiest hours', 4, 'Sizes the discharge desk. The usual rule may give too many, so we wait for your times.', [('Changes', 'Discharge Executives', 'target')], None)]
T.append(turn(11, 'What do you need from us to start?',
    'Prompt 1 of bm-pr-10. Transcript 31 (to start: read access from IT and one name to own this) and the four numbers still missing in the record (desk roster per shift, hour-by-hour arrivals, internal transfers, the discharge pattern). The last Processes turn; the jump goes back to Diagnosis.',
    {'text': ['Two things to start, and four numbers to finish the picture. Type them straight into the clipboard.'],
     'bullets': ['To start: one name to own this, and who in IT gives read access.',
                 'The four numbers turn the cost into a difference and size both desks on your real hours.',
                 'At the end of step 2 you have your own dead bed time. If it is smaller than we said, you will know first.'],
     'invite': 'Send what you have. Rough answers are fine.',
     'points': P('An owner', 'Read access', 'The desk roster', 'Discharge times'),
     'prompts': ['Here are our answers', 'Who else should see this plan?', 'Can we start step 1 now?'],
     'pointer': 'Type on each line of the clipboard. Every line you fill is added to your message.'},
    [H('Processes · to start', 'What we need from you', 'Six lines on a clipboard. Each one you fill goes into your message.', 'The trial', 'To start'),
     {'type': 'clipboard', 'title': 'What we need to start', 'sub': 'Rough answers are fine. Leave a line empty if you do not know yet.',
      'asks': [dict({'title': t, 'who': w, 'placeholder': ph}, **({'point': p} if p else {})) for t, w, ph, p, tx, l, q in ASKS],
      'count_label': 'Lines filled', 'waiting': 'None filled yet', 'done': 'All in. Send to Tojo.',
      'have_label': 'Already given in this chat', 'have': ['Your admission times', 'When billing stops and starts', 'What a bed earns a day', 'Beds, occupancy and stay'],
      'sheets': [S('a%d' % (i + 1), x[1], x[0], x[4], x[5]) for i, x in enumerate(ASKS)]},
     E('After step 2', 'Your own dead bed time', 'Measured, not guessed. If it is smaller than we said, you know before spending anything on people or process.', 'start', 'stamp')],
    ('Send what we have', 'Here are our answers'), ('Add something else we should know', 'Something else you should know: ')))

for s in T:
    s['review'] = {'status': 'approved', 'date': '2026-10-06', 'note': 'Approved 6 Oct with the Bed Management Processes turns.'}
    json.dump(s, open(os.path.join(HERE, s['turn']['id'] + '.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

NOTES = {'bm-pr-01.json': 'Prompt 1 of bm-au-07. New drawing: the day-dial, the ward’s day on a wall clock. Today against the new day.',
         'bm-pr-02.json': 'New drawing: ward-pins, from the approved Processes landing page B (the trial ward from above).',
         'bm-pr-03.json': 'The library swap (magnets): the one rule that keeps the day late, and the new order.',
         'bm-pr-04.json': 'New drawing: round-cards. Confirm or change a likely date; a changed date is typed in and added to the message.',
         'bm-pr-05.json': 'The library loop with a yes-or-no check: a date not given. The evening background starts here.',
         'bm-pr-06.json': 'New drawing: the OPD slip, pulled into the bed plan.',
         'bm-pr-07.json': 'The library name badges: everyone this touches, grouped and filtered.',
         'bm-pr-08.json': 'The library chairs and lamps: the two managers and the desks, with the triggers your numbers meet.',
         'bm-pr-09.json': 'The library instrument windows: the eight weekly measures. The day background returns.',
         'bm-pr-10.json': 'The library trial strip: two weeks on one ward, playable.',
         'bm-pr-11.json': 'New drawing: the clipboard, typed into. The last Processes turn; the jump goes back to Diagnosis.'}
json.dump({'place': 'Processes', 'turns': [{'file': f, 'note': n} for f, n in NOTES.items()]}, open(os.path.join(HERE, 'turns.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('wrote bm-pr-01 to bm-pr-11 and turns.json')
