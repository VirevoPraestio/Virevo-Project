"""Writes the three samples of bm-so-01, the first Bed Management Solutions turn (transcript turn 18, Part 1: Automation).
Each sample is a full turn spec: the user's message, the chat (text, bullets, note, @points, three prompts) and the canvas.
Run, then draw with ../../solutions-html-generator/bm_solutions_html.py samples."""
import copy, json, os
HERE = os.path.dirname(os.path.abspath(__file__))

TRANSCRIPT = {
    'label': 'Transcript turn 18 · Part 1: Automation',
    'user': 'automations',
    'tojo': ['Automation first, then.',
             'The mapping doesn’t just count empty beds. It includes beds expected to free up — patients approaching the typical stay for their own procedure — which is what makes a next-day picture possible at all.',
             'The 5 PM round is what makes the 6 PM freeze worth anything. A prediction nobody confirmed with the treating doctor is a guess with a timestamp on it.',
             'And the last step is aimed squarely at your 1 PM arrivals: the desk is told when to call each patient in, per bed. It stops guessing, so patients stop arriving after the bed was already free.',
             'The full chain is in the graphic. Come back to me on any step — or pick another of the five.'],
    'graphic': 'Six-step chain: OPD prescription captured → 2 PM first mapping pass → teams notified → 5 PM rounds confirm → 6 PM final freeze → call-in times issued (red outcome). '
               'Desktop wraps three-and-three with an elbow connector. Effect box: ADMISSION TAT · under 30 minutes · documentation is the only step that cannot be compressed.'}

STEPS = [  # when, title, short line, sheet
    ('In OPD, all day', 'Admission advice recorded', 'The doctor’s advice to admit is recorded as it is written.',
     {'key': 'opd', 'text': 'Each time an OPD doctor advises admission, the advice is recorded with the procedure and the date. Tomorrow’s planned admissions are known when they are advised, not when the patient turns up.',
      'lines': [{'label': 'Reads from', 'value': 'The OPD prescription, as the doctor writes it'}, {'label': 'Who does the work', 'value': 'Nobody new. The advice is read, not typed again'}],
      'entry': 'How does admission advice reach your desk today?', 'entry_hint': 'For example, a slip the patient carries'}),
    ('2 PM', 'First mapping of tomorrow', 'Planned admissions set against empty beds and beds likely to free up.',
     {'key': 'map', 'text': 'At 2 PM the first pass sets tomorrow’s planned admissions against the beds. It counts empty beds, and beds likely to free up. Those are patients near the usual stay for their own procedure.',
      'lines': [{'label': 'Reads from', 'value': 'Admissions, discharges and each patient’s procedure'}, {'label': 'Gives', 'value': 'A first picture of tomorrow’s beds, ward by ward', 'state': 'start'}],
      'entry': 'Which wards are hardest to predict?', 'entry_hint': 'For example, the ICU or the surgical ward'}),
    ('After 2 PM', 'Teams told', 'Wards, housekeeping and the desk see which beds should free up.',
     {'key': 'tell', 'text': 'The wards, housekeeping and the admissions desk are told which beds should free up tomorrow. Each team sees the same list, so nobody works from an old one.',
      'lines': [{'label': 'Who sees it', 'value': 'Ward nurses, housekeeping and the admissions desk'}, {'label': 'Kept up to date', 'value': 'At each pass, 2 PM and 6 PM'}],
      'entry': 'Who should hear first at your hospital?', 'entry_hint': 'A role, for example the night ward in charge'}),
    ('5 PM', 'Evening round confirms', 'Treating doctors confirm who goes home tomorrow.',
     {'key': 'round', 'text': 'On the 5 PM round, the treating doctor confirms which patients will go home tomorrow. This is what makes the 6 PM freeze worth anything. A forecast no doctor has checked is only a guess.',
      'lines': [{'label': 'Who', 'value': 'The treating doctor, on the evening round'}, {'label': 'What changes', 'value': 'The forecast becomes a decision', 'state': 'target'}],
      'entry': 'Do your doctors round in the evening? At what time?', 'entry_hint': 'For example, about 5 PM on most wards'}),
    ('6 PM', 'Tomorrow’s plan frozen', 'Each patient coming in is matched to one bed.',
     {'key': 'freeze', 'text': 'At 6 PM tomorrow’s plan is frozen. Each patient coming in is matched to one bed, with the time it should be ready. A late change is handled on its own, not by redoing the plan.',
      'lines': [{'label': 'Gives', 'value': 'One plan for every bed tomorrow', 'state': 'start'}, {'label': 'Fixed at', 'value': '6 PM, the evening before'}],
      'entry': 'What usually changes the plan after 6 PM?', 'entry_hint': 'For example, an emergency admission'}),
    ('After 6 PM', 'Call-in times sent', 'The desk calls each patient for the time their bed is ready.',
     {'key': 'call', 'text': 'The desk is told when to call each patient in, bed by bed. It stops guessing, so patients come when their bed is ready. This step is aimed at your 1 PM arrivals.',
      'lines': [{'label': 'Today', 'value': 'Patients arrive about 1 PM, in a bed about 4:30 PM', 'state': 'outcome'},
                {'label': 'With this step', 'value': 'Each patient is called for their own bed’s time', 'state': 'start'}],
      'entry': 'Who calls patients in at your hospital today?', 'entry_hint': 'A role, for example the admissions desk'}),
]

def sheets():
    out = []
    for when, title, line, sh in STEPS:
        s = dict(sh); s.update({'when': when, 'title': title})
        s['ask'] = {'label': 'Ask about this step', 'say': 'Tell me more about this step: %s' % title[0].lower() + title[1:]}
        out.append(s)
    return out

POINTS = ['Admission advice recorded', 'The 2 PM mapping', 'Teams told', 'The 5 PM round', 'The 6 PM freeze', 'Call-in times']

BASE = {
    'turn': {'id': 'bm-so-01', 'tab': 'Solutions', 'type': 'part', 'register': 'advisory', 'tool': 'Bed Management', 'user_message': 'automations',
             'context': 'The first Solutions turn: one part (automations) taken up after the overview. Six steps, the mechanism in the bullets, the drawing holds the steps.',
             'transcript': TRANSCRIPT},
    'chat': {
        'text': ['Automation first, then.'],
        'bullets': ['The mapping counts more than empty beds. It also counts beds likely to free up: patients near the usual stay for their procedure. That is what makes a next-day picture possible.',
                    'The 5 PM round is what makes the 6 PM freeze worth anything. A forecast no treating doctor has checked is a guess with a time on it.',
                    'The last step is aimed at your 1 PM arrivals. The desk is told when to call each patient in, bed by bed. It stops guessing.'],
        'invite': 'Come back to me on any step, or pick another of the five parts.',
        'note': 'One plan for tomorrow’s beds, fixed at 6 PM.',
        'points': [{'n': i + 1, 'label': x, 'canvas': True} for i, x in enumerate(POINTS)],
        'prompts': ['How would all of this be done?', 'What if we don’t have such systems?', 'Take me to part 2, the process changes']},
}
PLATE = {'part': 1, 'of': 5, 'name': 'Automations', 'stage': 'Shaped'}
EFFECT = {'type': 'effect', 'label': 'Time to a bed', 'value': 'Under 30 minutes', 'state': 'outcome',
          'sub': 'From about 3½ hours today. Paperwork is the one step that cannot be made shorter.'}

def sample(letter, name, what, pointer, heading, block):
    s = copy.deepcopy(BASE)
    s['turn']['sample'] = {'letter': letter, 'name': name, 'what': what}
    s['chat']['pointer'] = pointer
    s['canvas'] = {'blocks': [dict({'type': 'heading', 'eyebrow': 'Part 1 · Automations', 'plate': PLATE}, **heading), block, copy.deepcopy(EFFECT)]}
    return s

A = sample('A', 'Six switches, one bulb',
           'The lightbulb motif. The six steps are switches on one wire, wrapped three and three with an elbow as the transcript asks. Pick a switch: the current runs from OPD to it, and the bulb lights only at the last one.',
           'The six steps are switches on one wire. Pick one to see what it does and what it reads from.',
           {'title': 'Six switches, one bulb', 'deck': 'The automation part, from the OPD to the call-in time. The bed is ready on time only when every switch is on.'},
           {'type': 'circuit', 'source': {'label': 'OPD', 'line': 'Where the advice to admit is written'},
            'goal': {'label': 'Bed ready as the patient arrives', 'line': 'Called in for their own bed’s time'},
            'steps': [{'when': w, 'title': t, 'line': l, 'point': i + 1} for i, (w, t, l, _) in enumerate(STEPS)],
            'readout': 'Take any switch away and the call-in time is a guess again.', 'sheets': sheets()})

B = sample('B', 'Six pieces that only fit together',
           'The jigsaw motif. The six steps are pieces locked together. Pick a piece: it lifts, and the pieces it relies on are outlined. The 6 PM freeze shows that it leans on the 5 PM round.',
           'The six steps are pieces of one jigsaw. Pick one to see what it relies on.',
           {'title': 'Six pieces that only fit together', 'deck': 'Each step leans on the ones before it. The 6 PM freeze leans on the 5 PM round most of all.'},
           {'type': 'jigsaw',
            'pieces': [{'when': w, 'title': t, 'line': l, 'point': i + 1, 'relies_on': r} for i, ((w, t, l, _), r) in enumerate(zip(STEPS, [[], [1], [2], [3], [2, 4], [5]]))],
            'condition': 'Take any piece away and the call-in time is a guess again.', 'sheets': sheets(), 'hint': 'Pick a piece. The pieces it relies on are outlined.'})

C = sample('C', 'From OPD to the bed, in six stops',
           'The library route. The six steps are stations on one trail through the day before. At the end, under the bulb, four doors open the other four parts.',
           'The six steps are stations on one route. Pick one to open it, or pick a door at the end.',
           {'title': 'From OPD to the bed, in six stops', 'deck': 'The automation part as one route through the day before. At the end, pick the part to open next.'},
           {'type': 'route', 'steps': [{'title': t, 'what': l, 'point': i + 1} for i, (w, t, l, _) in enumerate(STEPS)], 'sheets': sheets(),
            'fork': {'question': 'Come back to me on any stop, or pick another of the five parts.',
                     'options': [{'tag': 'Part 2', 'label': 'Process changes', 'what': 'What changes in how the day is run', 'say': 'Take me through part 2, the process changes'},
                                 {'tag': 'Part 3', 'label': 'People and buy-in', 'what': 'Whose help this needs, and who signs it off', 'say': 'Take me through part 3, the people and their buy-in'},
                                 {'tag': 'Part 4', 'label': 'Teams and roles', 'what': 'Whether you need to hire, and who', 'say': 'Take me through part 4, the teams and roles'},
                                 {'tag': 'Part 5', 'label': 'Measures and targets', 'what': 'How you will know it is working', 'say': 'Take me through part 5, the measures and targets'}]}})

for s in (A, B, C):
    json.dump(s, open(os.path.join(HERE, 'bm-so-01-%s.json' % s['turn']['sample']['letter']), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('wrote bm-so-01-A/B/C.json')
