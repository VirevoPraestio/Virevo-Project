"""Writes the three samples of bm-au-01, the first Bed Management Automations turn.

The approved transcript stops at turn 31 (the first step), whose prompt "How would the build work?" opens Automations
(Avishek, 1 Oct: Automations starts when the build itself is detailed). The record holds no Automations turn, so the
content is taken from the Bed Management reference file (bed-management.md §7.4.1 the engine and its daily cadence,
§7.2 the records it needs, §7.4.2 the prerequisites) and from the hospital's own facts in the transcript (turns 19, 20, 31).
Nothing here is a new figure. Draw with ../../automations-html-generator/bm_automations_html.py samples."""
import copy, json, os
HERE = os.path.dirname(os.path.abspath(__file__))

def S(key, when, title, text, lines=(), entry=None, hint=None, hand=None, ask=None):
    s = {'key': key, 'when': when, 'title': title, 'text': text}
    if lines: s['lines'] = [dict(zip(('label', 'value', 'state'), l)) for l in lines]
    if entry: s['entry'] = entry
    if hint: s['entry_hint'] = hint
    if hand: s['hand'] = {'who': hand[0], 'does': hand[1]}
    if ask: s['ask'] = {'label': ask[0], 'say': ask[1]}
    return s

BASE = {
    'turn': {'id': 'bm-au-01', 'tab': 'Automations', 'type': 'part', 'register': 'advisory', 'tool': 'Bed Management', 'user_message': 'How would the build work?',
             'context': 'The first Automations turn: how the build works. From bed-management.md §7.4.1 (the engine, a to e, and the 2 PM and 6 PM passes), §7.2 (the records) and §7.4.2 (discharge first, read access), with the transcript’s own facts.',
             'transcript': {'label': 'After transcript turn 31 · “How would the build work?” (the record stops at 31)'}},
    'chat': {
        'text': ['Here is the build, in the order it happens.'],
        'bullets': ['First, read access. Your IT team links the systems that already hold admissions, discharges, inpatient notes and billing. We write nothing back.',
                    'Second, discharge. The bed plan runs on discharge times, so discharge is built and linked before the bed mapping.',
                    'Then one engine does five jobs. It maps tomorrow’s beds and ICU beds, checks discharge times, holds emergency beds back and sets call-in times.'],
        'invite': 'Pick any part to see what it reads and what it makes. Or tell me which systems your hospital runs.',
        'note': 'Read access and discharge first. The engine comes after.',
        'points': [{'n': i + 1, 'label': x, 'canvas': True} for i, x in enumerate(['Read access', 'Discharge first', 'Tomorrow’s bed map', 'Emergency beds', 'Call-in times'])],
        'prompts': ['What exactly would our IT team do?', 'Why must discharge be built first?', 'What if some records are on paper?']},
}
ACTIONS = {'go': {'detail': 'Next: what your IT team would do', 'say': 'What exactly would our IT team do?'},
           'add': {'detail': 'Tell me about your systems', 'say': 'Here is what we run today: '},
           'jump': {'tab': 'Processes', 'detail': 'How the day changes on the wards', 'say': 'Take me to Processes'}}
PLATE = {'tag': 'Automations', 'name': 'The bed engine', 'stage': 'Idea'}
EFFECT = {'type': 'effect', 'label': 'Your IT team’s part', 'value': 'Read access, once', 'state': 'target',
          'sub': 'About two weeks. We read the records you already hold, and we write nothing back.'}

def sample(letter, name, what, pointer, heading, block):
    s = copy.deepcopy(BASE)
    s['turn']['sample'] = {'letter': letter, 'name': name, 'what': what}
    s['chat']['pointer'] = pointer
    s['review'] = {'status': 'approved', 'date': '2026-10-01', 'note': ('Approved 1 Oct: the turn (Avishek’s preference).' if letter == 'B' else 'Approved 1 Oct as a template; Sample B is the turn.')}
    s['canvas'] = {'blocks': [dict({'type': 'heading', 'eyebrow': 'Automations · how it is built', 'plate': PLATE}, **heading), block, copy.deepcopy(EFFECT)],
                   'actions': copy.deepcopy(ACTIONS)}
    return s

# ---------------------------------------------------------------------------------------------- A · the switchboard
A = sample('A', 'Link the records, light the lamps',
    'The library switchboard (sources), layered. Records are switches, discharge is the main switch from the landing page, and each automation is a lamp that lights only when every record it needs is linked.',
    'Flip the switches to link each record. A lamp lights when everything it needs is on. Pick a record to see what your IT team gives.',
    {'title': 'Link the records, light the lamps', 'deck': 'Each automation lights only when every record it needs is linked. Discharge is the main switch.'},
    {'type': 'sources', 'src_label': 'Where the records come from', 'auto_label': 'Automations that can switch on',
     'main': {'id': 'dis', 'tag': 'Main switch', 'name': 'Discharge, automated', 'short': 'discharge', 'point': 2,
              'line': 'The bed plan runs on real discharge times, not reported ones'},
     'sources': [{'id': 'adt', 'name': 'Admissions and discharges', 'short': 'admissions', 'holds': 'Who came in, who left, which bed, and when', 'link': 'waiting', 'point': 1},
                 {'id': 'ip', 'name': 'Inpatient records', 'short': 'inpatient notes', 'holds': 'The stay so far, for each patient and procedure', 'link': 'waiting', 'point': 1},
                 {'id': 'bed', 'name': 'Bed board', 'short': 'bed board', 'holds': 'Which beds are empty, being cleaned or ready', 'link': 'waiting', 'point': 1},
                 {'id': 'bill', 'name': 'Billing', 'short': 'billing', 'holds': 'When each bill closes and the next opens, bed by bed', 'link': 'waiting', 'point': 1},
                 {'id': 'opd', 'name': 'OPD prescriptions', 'short': 'OPD advice', 'holds': 'The advice to admit, the procedure and the date', 'link': 'ours'},
                 {'id': 'voice', 'name': 'Voice notes on rounds', 'short': 'round notes', 'holds': 'The doctor’s spoken note and the confirmed date', 'link': 'ours'}],
     'automations': [{'name': 'Tomorrow’s bed map', 'needs': ['dis', 'adt', 'opd', 'ip'], 'point': 3},
                     {'name': 'ICU bed map', 'needs': ['adt', 'ip', 'voice']},
                     {'name': 'Discharge times checked', 'needs': ['dis', 'adt', 'bed']},
                     {'name': 'Emergency beds held back', 'needs': ['adt'], 'point': 4},
                     {'name': 'Call-in times, bed by bed', 'needs': ['dis', 'adt', 'bed', 'opd'], 'point': 5},
                     {'name': 'Dead bed time, measured', 'needs': ['bill', 'adt']}],
     'default_on': ['opd', 'voice'],
     'presets': [{'label': 'Only what we bring', 'on': ['opd', 'voice']}, {'label': 'Add your IT links', 'on': ['opd', 'voice', 'adt', 'ip', 'bed', 'bill']},
                 {'label': 'Everything, discharge too', 'on': ['opd', 'voice', 'adt', 'ip', 'bed', 'bill', 'dis']}],
     'condition': 'Discharge is the main switch. Three of the six lamps stay dark until discharge is automated.',
     'sheets': [S('adt', 'Read access · your IT team', 'Admissions and discharges', 'The engine reads who came in, who left, which bed and when. It writes nothing back to your system.',
                  [('Who gives it', 'Your IT team, once'), ('Used by', 'Five of the six automations', 'start')], 'Which system holds admissions today?', 'For example, the hospital system'),
                S('ip', 'Read access · your IT team', 'Inpatient records', 'The stay so far for each patient. It lets the engine see who is near the usual stay for their procedure.',
                  [('Who gives it', 'Your IT team, once'), ('Used by', 'The bed map and the ICU map')], 'Are inpatient notes kept on a system?'),
                S('bed', 'Read access · your IT team', 'Bed board', 'Which beds are empty, being cleaned or ready. The engine checks it against what the wards report.',
                  [('Who gives it', 'Your IT team, once'), ('Used by', 'Discharge checks and call-in times')], 'How does your desk see bed status today?'),
                S('bill', 'Read access · your IT team', 'Billing', 'Both times already sit in your billing system. One report joins them against the same bed. That gives dead bed time.',
                  [('Who gives it', 'Billing, with IT'), ('It is', 'A report, not new records')], 'Which billing system do you run?'),
                S('opd', 'We bring this', 'OPD prescriptions', 'The advice to admit is read from the prescription as it is written. Nobody fills in a form.',
                  [('Who does it', 'We do'), ('Used by', 'The bed map and call-in times')], 'Are OPD prescriptions on paper or on a system?'),
                S('voice', 'We bring this', 'Voice notes on rounds', 'The doctor speaks on the round they already do. Our recorder turns it into a note and a confirmed date.',
                  [('Who does it', 'We do'), ('Used by', 'The ICU map and the 5 PM round')], 'Do your doctors record notes on rounds?',
                  hand=('the treating doctor', 'Speaks the note and confirms the date with a tap.'))]})

# ---------------------------------------------------------------------------------------------- B · the brain, over one day
B = sample('B', 'One engine, read through the day',
    'The library brain, layered: one day instead of one stay. Pick a time of day or play it, and watch the records flow in and the engine’s answers fill by the 6 PM freeze.',
    'Pick a time of day, or play the day. The records light as they arrive and the answers fill by 6 PM.',
    {'title': 'One engine, read through the day', 'deck': 'What the engine reads at each pass, and what it has made by the 6 PM freeze.'},
    {'type': 'brain', 'passes_label': 'Time of day', 'play': 'Play the day', 'in_label': 'What the engine reads', 'out_label': 'What it makes, filling in',
     'count_label': 'records read, none typed again',
     'kinds': [{'k': 'opd', 'name': 'OPD advice', 'example': 'Who is coming in, for which procedure'},
               {'k': 'stay', 'name': 'Expected stays', 'example': 'Patients near the usual stay for their procedure'},
               {'k': 'icu', 'name': 'ICU step-down signals', 'example': 'Given by 1 PM'},
               {'k': 'round', 'name': '5 PM round answers', 'example': 'Doctors confirm or correct the date'},
               {'k': 'trend', 'name': 'Emergency trend', 'example': 'Two to three years of emergency admissions', 'point': 4},
               {'k': 'dis', 'name': 'Discharge times', 'example': 'Real times from the discharge side', 'point': 2}],
     'outputs': [{'name': 'Tomorrow’s bed map', 'from': ['opd', 'stay', 'dis', 'round'], 'point': 3},
                 {'name': 'ICU bed map', 'from': ['icu', 'stay']},
                 {'name': 'Beds held for emergencies', 'from': ['trend'], 'point': 4},
                 {'name': 'Admissions still without a bed', 'from': ['opd', 'stay', 'round']},
                 {'name': 'Call-in times, bed by bed', 'from': ['round', 'dis'], 'point': 5}],
     'passes': [{'label': 'All day', 'what': 'OPD advice comes in', 'brings': ['opd', 'opd', 'trend']},
                {'label': '1 PM', 'what': 'ICU signals due', 'brings': ['icu', 'stay']},
                {'label': '2 PM', 'what': 'First mapping pass', 'brings': ['stay', 'dis']},
                {'label': '5 PM', 'what': 'Rounds confirm', 'brings': ['round', 'round']},
                {'label': '6 PM', 'what': 'Final freeze', 'brings': ['dis', 'round']}],
     'condition': 'The 2 PM pass is a first picture. Only the 6 PM freeze sends call-in times out.',
     'sheets': [S('day', 'All day', 'OPD advice comes in', 'Each advice to admit is read as it is written, with the procedure and the date. The emergency trend is read from your past admissions.',
                  [('Reads', 'OPD prescriptions, past admissions'), ('Makes', 'Tomorrow’s list of planned admissions')], 'How many planned admissions do you have on a usual day?'),
                S('one', '1 PM', 'ICU signals due', 'ICU patients need their step-down signal by 1 PM. The engine adds patients near the usual ICU stay for their procedure.',
                  [('Reads', 'ICU signals, inpatient records'), ('Makes', 'The ICU bed map')], 'Who gives the step-down signal in your ICU?'),
                S('two', '2 PM', 'First mapping pass', 'Tomorrow’s planned admissions are set against empty beds and beds likely to free up. The teams are told what to confirm.',
                  [('Reads', 'Admissions, stays, discharge times'), ('Tells', 'The discharge team and Medical Supervisory')], 'Who should hear about the 2 PM pass first?'),
                S('five', '5 PM', 'Rounds confirm', 'On the evening round each predicted date is confirmed or corrected. The engine takes in every answer.',
                  [('Reads', 'Round answers, voice notes')], 'At what time do your evening rounds end?',
                  hand=('the treating doctor', 'Confirms or corrects each predicted date.')),
                S('six', '6 PM', 'Final freeze', 'Tomorrow’s plan is frozen. Each patient coming in has one bed and a call-in time. What is still unmapped is shared with everyone.',
                  [('Makes', 'Call-in times, bed by bed', 'start'), ('Also makes', 'The list still without a bed')], 'What usually changes after 6 PM?',
                  hand=('the Bed Manager', 'Checks the freeze before the call-in times go out.'))]})

# ---------------------------------------------------------------------------------------------- C · the station panel, through the build
C = sample('C', 'The build, step by step',
    'The station panel from the Automations landing page. Two main switches on top, one row of four lamps for each automation. Step through the four steps of the build and the lamps light in order.',
    'Step through the build. The lamps light as each automation moves from idea to switched on. Pick a row to open it.',
    {'title': 'The build, step by step', 'deck': 'Four steps, in order. Watch each automation move from idea to switched on.'},
    {'type': 'panel', 'phases_label': 'The four steps', 'rows_label': 'Automation', 'foot': 'Nurses’ station · build panel',
     'phases': [{'when': 'About two weeks', 'name': 'Read access'}, {'when': 'Four weeks', 'name': 'Measure what happens now'},
                {'when': 'Step 3', 'name': 'The day changes'}, {'when': 'Step 4', 'name': 'The build: discharge, then beds'}],
     'mains': [{'tag': 'Main switch 1', 'name': 'Read access from IT', 'line': 'The systems you already run', 'on_at': 0},
               {'tag': 'Main switch 2', 'name': 'Discharge, automated', 'line': 'The bed plan runs on its times', 'on_at': 3}],
     'automations': [{'name': 'Admission steps timed', 'line': 'Five steps stamped as they happen', 'stages': [0, 3, 3, 3], 'point': 1},
                     {'name': 'Dead bed time, measured', 'line': 'Bill close and open, against the bed', 'stages': [0, 3, 3, 3]},
                     {'name': 'Call-in times, bed by bed', 'line': 'When to call each patient in', 'stages': [0, 0, 2, 3], 'point': 5},
                     {'name': 'Discharge times checked', 'line': 'Real times, not reported ones', 'stages': [0, 0, 1, 3], 'point': 2},
                     {'name': 'Tomorrow’s bed map', 'line': 'A 2 PM pass and a 6 PM freeze', 'stages': [0, 0, 1, 3], 'point': 3},
                     {'name': 'ICU bed map', 'line': 'Step-downs by 1 PM', 'stages': [0, 0, 0, 3]},
                     {'name': 'Emergency beds held back', 'line': 'From two to three years of trend', 'stages': [0, 1, 1, 3], 'point': 4}],
     'sheets': [S('steps', 'Switched on in step 2', 'Admission steps timed', 'Each of the five admission steps is stamped as it happens. That shows paperwork apart from waiting.',
                  [('Reads', 'The admission desk’s own steps'), ('Makes', 'Your real admission times', 'start')], 'Do you time any admission steps today?'),
                S('dbt', 'Switched on in step 2', 'Dead bed time, measured', 'One report joins bill close and bill open against the same bed. Your own number, before anything else changes.',
                  [('Reads', 'Billing'), ('Makes', 'Dead bed time, bed by bed', 'start')], 'Has anyone measured this at your hospital?'),
                S('call', 'Testing in step 3', 'Call-in times, bed by bed', 'Tested while the two jobs start running together. Switched on once the discharge times it uses are real.',
                  [('Reads', 'The bed map and discharge times'), ('Makes', 'One call-in time per bed')], 'Who calls patients in today?',
                  hand=('the admissions desk', 'Calls each patient at their time.')),
                S('dis', 'Built in step 4', 'Discharge times checked', 'Discharge is built first in step 4. The engine checks its times against the beds as they free.',
                  [('Reads', 'Discharge, admissions, bed board'), ('Why first', 'The bed plan runs on these times', 'target')], 'Who records discharge times today?'),
                S('map', 'Built in step 4', 'Tomorrow’s bed map', 'Built on top of discharge. A first pass at 2 PM and a final freeze at 6 PM, every day.',
                  [('Reads', 'OPD advice, stays, discharge times'), ('Makes', 'One bed for each planned admission')], 'How many planned admissions on a usual day?',
                  hand=('the Bed Manager', 'Checks the 6 PM freeze before it goes out.')),
                S('icu', 'Built in step 4', 'ICU bed map', 'The same mapping for ICU beds, using step-down signals given by 1 PM.',
                  [('Reads', 'ICU signals, inpatient records')], 'How many ICU beds do you run?'),
                S('er', 'Switched on in step 4', 'Emergency beds held back', 'A number of beds is kept for emergencies, worked out from two to three years of your own admissions.',
                  [('Reads', 'Past admissions'), ('Makes', 'Beds kept out of the planned map')], 'How many emergencies do you admit on a usual day?')]})

for s in (A, B, C):
    json.dump(s, open(os.path.join(HERE, 'bm-au-01-%s.json' % s['turn']['sample']['letter']), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('wrote bm-au-01-A/B/C.json')
