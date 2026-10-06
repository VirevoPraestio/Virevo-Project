"""Writes the Discharge Process Solutions turns (dp-so-01 to 07) and turns.json. Redone 5 Oct 2026 with the latest generators.

From the approved Discharge templates: turn-04 (the overview, from the sample conversation) and so-01 to so-06 (the Solutions place),
250-bed hospital in Bhubaneswar, put into plain, simple English. One main drawing per turn, the tool layer and the three buttons.
Draw with: python3 ../../solutions-html-generator/dp_solutions_html.py build"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
JUMP = {'tab': 'Automations', 'detail': 'What runs by itself, night and day', 'say': 'Take me to Automations'}
def acts(go, go_say, add, add_say): return {'go': {'detail': go, 'say': go_say}, 'add': {'detail': add, 'say': add_say}, 'jump': dict(JUMP)}
def P(*labels): return [{'n': i + 1, 'label': x, 'canvas': True} for i, x in enumerate(labels)]
def S(key, when, title, text, lines=(), entry=None, hint=None, ask=None):
    s = {'key': key, 'when': when, 'title': title, 'text': text}
    if lines: s['lines'] = [dict(zip(('label', 'value', 'state'), l)) for l in lines]
    if entry: s['entry'] = entry
    if hint: s['entry_hint'] = hint
    if ask: s['ask'] = {'label': ask[0], 'say': ask[1]}
    return s
def T(n, typ, msg, was, context, label):
    return {'id': 'dp-so-%02d' % n, 'type': typ, 'tool': 'Discharge Process', 'tab': 'Solutions', 'register': 'advisory', 'user_message': msg, 'was': was,
            'context': context, 'transcript': {'label': label}}
def H(eyebrow, title, deck, plate=None):
    h = {'type': 'heading', 'eyebrow': eyebrow, 'title': title, 'deck': deck}
    if plate: h['plate'] = {'part': plate[0], 'of': 5, 'name': plate[1], 'stage': plate[2]}
    return h

SPECS = []
# ---------------------------------------------------------------------------------------------- 01 · the fix, as five doors (doors)
SPECS.append({
    'turn': T(1, 'overview', 'Yes, that’s exactly it. Show me how to fix it.', 'turn-04 (dp-04), cards + handnote + stat-strip',
              'Discharge sample conversation, turn 4 (playbook §3: a short intro, the five parts as options, one overview drawing).', 'Sample conversation · turn 4 · the fix'),
    'chat': {'text': ['Here is what the fix is made of. It has five parts.', 'None of them needs a new hospital system on day one. They sit on top of how you work today.'],
             'invite': 'Open any door to see what is behind it. Or tell me which part worries you most.',
             'note': 'Five parts, one aim: put the evening to work.',
             'points': P('Automatic paperwork', 'Changes on the wards', 'People who must agree', 'Who is in charge', 'How we will know it worked'),
             'prompts': ['Start with the automatic paperwork', 'Which part saves the most time?', 'Do we need to hire anyone?'], 'pointer': 'Five doors off one corridor. Open any one to see what it answers.'},
    'canvas': {'blocks': [
        H('The fix', 'What the fix is made of', 'Five parts. Each door says the question its part answers.'),
        {'type': 'doors', 'default': 1, 'corridor': 'One corridor. Open the doors in any order.',
         'doors': [{'n': 1, 'title': 'Automatic paperwork', 'question': 'What the software does, so nobody does the work twice', 'state': 'closed', 'tag': 'Start', 'point': 1},
                   {'n': 2, 'title': 'Changes on the wards', 'question': 'What each team does differently, and when it starts', 'state': 'closed', 'point': 2},
                   {'n': 3, 'title': 'People who must agree', 'question': 'Who has to say yes, and who gives up the most', 'state': 'closed', 'point': 3},
                   {'n': 4, 'title': 'Who is in charge', 'question': 'Whether you need anyone new, sized on your own numbers', 'state': 'closed', 'point': 4},
                   {'n': 5, 'title': 'How we will know', 'question': 'The few numbers we watch, week by week', 'state': 'closed', 'point': 5}],
         'sheets': [S('p1', 'Part 1', 'Automatic paperwork', 'The papers and the bill start on the evening round, by themselves. Other hospitals saved 6 to 8 hours for each patient. Not yet measured here.',
                      [('It answers', 'Hours nobody uses overnight'), ('Other hospitals', '6 to 8 hours saved', 'target')], 'Which paperwork takes longest on your wards?', None, ('Open part 1', 'Start with the automatic paperwork')),
                    S('p2', 'Part 2', 'Changes on the wards', 'Most of the work stays the same. What changes is when it starts, and who writes it.',
                      [('It answers', 'Hours nobody uses overnight')], 'What would you most like to change on the ward?', None, ('Open part 2', 'Show me the changes on the wards')),
                    S('p3', 'Part 3', 'People who must agree', 'Several teams touch discharge, but only a few change much. One person has to approve the new order.',
                      [('It answers', 'Nobody in charge of the whole discharge')], 'Who would push back hardest?', None, ('Open part 3', 'Show me the people who must agree')),
                    S('p4', 'Part 4', 'Who is in charge', 'One person owns discharge, with helpers for the busy hours. Sized on your numbers, not a rule of thumb.',
                      [('It answers', 'Nobody in charge of the whole discharge')], 'Who owns discharge today, if anyone?', None, ('Open part 4', 'Show me who is in charge')),
                    S('p5', 'Part 5', 'How we will know', 'A short list of numbers, watched week by week, starting from your own.',
                      [('It answers', 'Whether any of it is working')], 'Which numbers do you look at each week now?', None, ('Open part 5', 'Show me how we’ll know it worked'))]},
        {'type': 'effect', 'label': 'The aim of all five', 'value': 'Put the evening to work', 'state': 'target',
         'sub': 'Your doctors sign in the morning what they already decided the night before.'}],
        'actions': acts('Next: start with the automatic paperwork', 'Start with the automatic paperwork', 'Tell me which part worries you', 'The part that worries me most is: ')}})

# ---------------------------------------------------------------------------------------------- 02 · five parts, locked together (jigsaw)
PCS = [('Through the night', 'Automations', 'Papers and the bill start on the evening round, by themselves.', [2, 3], 'Hours nobody uses overnight', 'Your IT team lets Tojo read your records', 'The summary is drafted from notes already in your files. The bill stays up to date through the stay.', 'What would your IT team say to read-only access?'),
       ('The evening before', 'Changes on the wards', 'The going-home work moves to the night before the patient leaves.', [3, 4], 'Hours nobody uses overnight', 'A two-week trial on one ward', 'Nurses start the checklist after the evening round. Families hear that same evening.', 'Which ward would try it first?'),
       ('Before day 1', 'People who must agree', 'Who has to say yes, and what each group gives up.', [], 'Nobody in charge of the whole discharge', 'A yes from your Head of Operations', 'Typists check drafts instead of typing them. Doctors sign an early summary, as they do for cash patients.', 'Who has to say yes first?'),
       ('Every day', 'Team and roles', 'One person owns every discharge, with helpers for the two busy times.', [3], 'Nobody in charge of the whole discharge', 'The trial shows your two busy times', 'A Discharge Manager owns each discharge from start to end. One helper for each busy time.', 'Who could own discharge here?'),
       ('Week by week', 'Measures we watch', 'The numbers that tell us, week by week, if it is working.', [1, 2], 'Both causes', 'Real times from one normal week', 'Hours from ready to home. Patients home before noon. Minutes a bed stays empty.', 'Which number would you trust most?')]
SPECS.append({
    'turn': T(2, 'overview', 'Show me the five parts', 'so-01 (puzzle)', 'Solutions place, turn 1 (playbook §3: the five parts, and how they lean on each other).', 'Solutions · the five parts'),
    'chat': {'text': ['Here is the answer. It has five parts, and they only work together.', 'None of them needs a new hospital system on day one.'],
             'invite': 'Choose a part to start with. You can take them in any order.',
             'note': 'Five parts, one picture. Take one away and there is a hole.',
             'points': P(*[p[1] for p in PCS]),
             'prompts': ['Start with the automations', 'Which part saves the most time?', 'Do we need to hire anyone?'], 'pointer': 'Pick a piece. It lifts, and the pieces it leans on are outlined.'},
    'canvas': {'blocks': [
        H('The answer · all five parts', 'Five parts, one picture', 'Each part answers a cause Diagnosis found. Each one also leans on the others.'),
        {'type': 'jigsaw', 'pieces': [{'when': w, 'title': n, 'line': l, 'relies_on': r, 'point': i + 1} for i, (w, n, l, r, a, f, c, q) in enumerate(PCS)],
         'condition': 'Take any piece away and the evening goes unused again.',
         'sheets': [S('j%d' % (i + 1), 'Part %d of 5' % (i + 1), n, c, [('It answers', a), ('Needs first', f, 'target')], q, None, ('Open this part', 'Tell me about the %s' % n.lower()))
                    for i, (w, n, l, r, a, f, c, q) in enumerate(PCS)]}],
        'actions': acts('Next: start with the automations', 'Start with the automations', 'Tell me which part to start with', 'I would like to start with: ')}})

# ---------------------------------------------------------------------------------------------- 03 · the automations part (circuit)
SPECS.append({
    'turn': T(3, 'part', 'Start with the automations', 'so-02 (untangle)', 'Solutions place, turn 2 (playbook §4: this hospital’s own hold-ups, not the generic list).', 'Solutions · part 1, the automations'),
    'chat': {'text': ['Automations are the part that puts the unused night hours to work.'],
             'bullets': ['The decision is already made on the evening round. Today nothing moves until the morning signature.',
                         'Your staff write the same facts twice. Once in the notes, then again in the summary and the bill.',
                         'An early insurance request stops the insurer from setting the time a patient leaves.'],
             'invite': 'Next is the changes on the wards. This part leans on them.',
             'note': 'The work is not slow. It just waits all night.',
             'points': P('The doctor’s word on the round', 'The discharge summary', 'The final bill', 'The insurance request', 'Medicines to take home', 'The morning signature'),
             'prompts': ['Our doctors don’t use voice notes', 'What does our IT team have to do?', 'Next, the changes on the wards'], 'pointer': 'Pick a switch. The current runs to it, and the bulb lights at the last one.'},
    'canvas': {'blocks': [
        H('Part 1 · Automations', 'Six switches, one going home', 'The automation part, from the evening round to the morning signature. The patient is home early only when every switch is on.', (1, 'Automations', 'Shaped')),
        {'type': 'circuit', 'source': {'label': 'The evening round', 'line': 'Where the decision is already made'}, 'goal': {'label': 'Home by noon', 'line': 'A goal, set against today’s 3:15 PM'},
         'steps': [{'when': '7 PM round', 'title': 'The doctor’s word recorded', 'line': 'One tap on the ward phone says who can likely go.', 'state': 'start', 'point': 1},
                   {'when': '7:30 PM', 'title': 'Summary drafted', 'line': 'Drafted from notes already in your files, ready to check.', 'point': 2},
                   {'when': 'All evening', 'title': 'Bill kept up to date', 'line': 'Each charge is added as it happens. No count first.', 'point': 3},
                   {'when': 'Overnight', 'title': 'Insurance asked early', 'line': 'An early request goes with the expected bill.', 'point': 4},
                   {'when': 'Before morning', 'title': 'Medicines listed and packed', 'line': 'The pharmacy gets the list the evening before.', 'point': 5},
                   {'when': 'Morning round', 'title': 'Doctor checks and signs', 'line': 'A draft to check, not a page to write.', 'point': 6}],
         'readout': 'Take any switch away and the patient waits for the morning again.',
         'sheets': [S('word', '7 PM round', 'The doctor’s word recorded', 'Your doctors already decide on the evening round. Today it is said, not written down. One tap makes it the start of everything else.',
                      [('Today', 'Said, not recorded'), ('Asks of doctors', 'One tap, nothing new to learn', 'start')], 'Who is on your evening round?'),
                    S('sum', '7:30 PM', 'Summary drafted', 'Tojo drafts the summary from notes, reports and medicines already in your files. The morning typing queue goes.',
                      [('Today', 'Typed next morning by a typist'), ('Needs', 'Your IT team lets Tojo read your records', 'target')], 'How many summaries does one typist do a day?'),
                    S('bill', 'All evening', 'Bill kept up to date', 'Each charge goes on the bill as it happens. Billing stops waiting for nurses to count supplies.',
                      [('Today', 'Drawn up after the signature, 1:30 PM'), ('Needs', 'Billing agrees to check, not build', 'target')], 'How long does billing take after signing?'),
                    S('ins', 'Overnight', 'Insurance asked early', 'An early request goes with the expected bill, the evening before. The insurer stops setting the leaving time.',
                      [('Today', 'Asked once the bill is final'), ('Needs', 'Your insurers accept an early request', 'target')], 'Which insurers take longest to approve?'),
                    S('med', 'Before morning', 'Medicines listed and packed', 'The pharmacy gets the list of medicines to take home that evening. The rush after the signature goes.',
                      [('Today', 'Listed after the signature, then packed')], 'When does the pharmacy hear today?'),
                    S('sign', 'Morning round', 'Doctor checks and signs', 'The doctor checks a ready draft on the morning round and signs. Nothing is written from the start.',
                      [('Today', 'Signs about 11 AM, then the work starts'), ('With this', 'Signs a ready draft', 'start')], 'Would your consultants sign on a phone?')]}],
        'actions': acts('Next: the changes on the wards', 'Next, the changes on the wards', 'Tell me what our doctors do now', 'On our evening round, the doctors: ')}})

# ---------------------------------------------------------------------------------------------- 04 · a correction (maze)
SPECS.append({
    'turn': T(4, 'challenge', 'Our doctors don’t use voice notes, and we don’t record half these details today.', 'so-03 (maze)',
              'Solutions place, turn 3 (playbook §5: a factual correction is new information. Reframe the capability as a new layer).', 'Solutions · a correction'),
    'chat': {'text': ['Fair challenge. I described your rounds as if each decision was already recorded. It isn’t, and it doesn’t need to be.',
                      'Tojo adds the recording as a new layer. Your hospital only shares what it already keeps.'],
             'invite': 'Or we can look at which part saves the most time.',
             'note': 'Tojo adds the recording. Your hospital only shares what it already keeps.',
             'points': P('Voice notes on the round', 'Typing every summary at night', 'Waiting for new software', 'The one-tap form'),
             'prompts': ['What if some notes are on paper?', 'What does our IT team have to do?', 'Which part saves the most time?'], 'pointer': 'Pick a route through the maze. Three hit a wall. One gets through.'},
    'canvas': {'blocks': [
        H('Part 1 · a correction', 'A new layer, not a new habit', 'Four ways to record each decision on the evening round. Three hit a wall. One gets through with what you already have.', (1, 'Automations', 'Shaped')),
        {'type': 'maze', 'start': 'Record each decision on the evening round', 'goal': 'Every decision recorded, nothing new to learn',
         'routes': [{'kind': 'dead', 'name': 'Voice notes on the round', 'why': 'Your doctors don’t use them. Asking for them adds work to a busy round.', 'point': 1},
                    {'kind': 'dead', 'name': 'Type every summary at night', 'why': 'Your typists work in the morning. The queue moves to the night, but the work stays.', 'point': 2},
                    {'kind': 'dead', 'name': 'Wait for new hospital software', 'why': 'It takes months. The two-week trial does not need it.', 'point': 3},
                    {'kind': 'way', 'name': 'A one-tap form, and notes you keep', 'why': 'The doctor taps once on the ward phone for each decision. Tojo drafts the rest from your files.',
                     'needs': ['Doctors deciding on the evening round, as today', 'Notes and reports kept in your software', 'Your IT team lets Tojo read your records'], 'point': 4}],
         'sheets': [S('voice', 'Ruled out', 'Voice notes on the round', 'You told me your doctors don’t use voice notes. A new habit on a busy round would not last.', [('Why it fails', 'Adds work to the round', 'outcome')]),
                    S('night', 'Ruled out', 'Type every summary at night', 'Moving the typing to the night only moves the queue. Somebody still types every summary.', [('Why it fails', 'The work stays the same', 'outcome')]),
                    S('wait', 'Ruled out', 'Wait for new hospital software', 'New software takes months to choose and set up. The trial can start in weeks without it.', [('Why it fails', 'Months before anything changes', 'outcome')]),
                    S('tap', 'The way through', 'A one-tap form, and notes you keep', 'One tap on the ward phone for each decision. Everything else is drafted from what your software already holds.',
                      [('Asks of doctors', 'One tap a patient', 'start'), ('Asks of IT', 'Read-only access', 'target')], 'Which details are not recorded anywhere today?', 'For example: why a test was ordered')]}],
        'actions': acts('Next: which part saves the most time', 'Which part saves the most time?', 'Tell me what you record today', 'Today we record these on the ward: ')}})

# ---------------------------------------------------------------------------------------------- 05 · five knots in one wait (gap-knots)
SPECS.append({
    'turn': T(5, 'part', 'Which part saves the most time?', 'so-04 (knots)', 'Solutions place, turn 4 (the wait as knots, each held by one or two parts).', 'Solutions · which part saves most'),
    'chat': {'text': ['No single part. The wait is five knots, and most need two parts to undo them.',
                      'Parts 1 and 2 together undo three of the five. Add parts 3 and 4, and the last two come undone.'],
             'note': 'No part works alone. Most knots need two hands.',
             'points': P('Waiting for the summary', 'Waiting for the bill', 'Waiting for insurance', 'Final checks and the family', 'The empty bed'),
             'prompts': ['Is it worth what it costs?', 'Tell me more about the automations', 'What changes on the wards?'], 'pointer': 'Pick a knot to see which parts undo it. Switch to see them all come undone.'},
    'canvas': {'blocks': [
        H('The answer · which part saves most', 'Five knots in one wait', 'Your real times, from ready to leaving and the empty bed after. Each knot sits between two steps.'),
        {'type': 'gap-knots', 'steps': [{'title': 'Patient ready', 'line': '10 AM'}, {'title': 'Summary signed', 'line': 'About noon'}, {'title': 'Bill final', 'line': '1:30 PM'},
                                        {'title': 'Insurance approves', 'line': '2:30 PM'}, {'title': 'Patient leaves', 'line': '3:15 PM'}, {'title': 'Bed ready again', 'line': '4:30 PM'}],
         'gaps': [{'title': 'Waiting for the summary', 'point': 1}, {'title': 'Waiting for the bill', 'point': 2}, {'title': 'Waiting for insurance', 'point': 3},
                  {'title': 'Final checks, the family', 'point': 4}, {'title': 'The empty bed', 'point': 5}],
         'switch': {'today': 'Today', 'owner': 'With all five', 'cap_today': 'Five knots, one after another. The patient leaves at 3:15 PM.', 'cap_owner': 'Each knot is undone by the parts that hold it.'},
         'caption': 'Times from your normal Tuesday. The summary wait is my estimate.',
         'sheets': [S('k1', 'Knot 1 · about 2 hours', 'Waiting for the summary', 'The summary is typed next morning, then waits for the doctor to sign.', [('Undone by', 'Parts 1 and 2', 'start'), ('How', 'Drafted overnight, signed on the round')], 'How long do summaries wait to be signed?'),
                    S('k2', 'Knot 2 · 90 minutes', 'Waiting for the bill', 'The bill is drawn up only after the signature.', [('Undone by', 'Parts 1 and 3', 'start'), ('How', 'Kept up to date, billing checks it')], 'What holds the bill up most?'),
                    S('k3', 'Knot 3 · 1 hour', 'Waiting for insurance', 'The insurer is asked only once the bill is final.', [('Undone by', 'Part 1', 'start'), ('How', 'An early request the evening before')], 'Which insurer is slowest?'),
                    S('k4', 'Knot 4 · 45 minutes', 'Final checks, the family', 'Medicines are packed and the family called only at the end.', [('Undone by', 'Part 2', 'start'), ('How', 'Told on the evening round')], 'When does the family hear today?'),
                    S('k5', 'Knot 5 · 75 minutes', 'The empty bed', 'Housekeeping hears late, so the bed stays empty 75 minutes.', [('Undone by', 'Parts 2 and 4', 'start'), ('How', 'Housekeeping hears at once, one owner')], 'How does housekeeping hear a bed is free?')]}],
        'actions': acts('Next: is it worth what it costs', 'Is it worth what it costs?', 'Tell me about one of the knots', 'About one of the knots: ')}})

# ---------------------------------------------------------------------------------------------- 06 · worth it (pair + effect)
SPECS.append({
    'turn': T(6, 'recommendation', 'Is it worth what it costs?', 'so-05 (stake)', 'Solutions place, turn 5 (playbook §7: cost against what is at stake, a threshold already met).', 'Solutions · cost against the wait'),
    'chat': {'text': ['Yes. Put one Discharge Manager in place now, and start the two-week trial.', 'At 40 to 45 discharges a day, this is not a maybe-someday. You are already there.',
                      'The team costs a small part of what the wait costs, even if the trial wins back very little.'],
             'note': 'The team costs about a hundredth of what the wait does.',
             'points': P('What the wait costs', 'What the team costs', 'Your discharges a day'),
             'prompts': ['What would we do first?', 'Why the Manager before the trial?', 'Can we start with one person?'], 'pointer': 'The two figures read against each other. Ask about either one.'},
    'canvas': {'blocks': [
        H('Cost against what is at stake', 'A small team against a large wait', 'What the wait costs a year, against what the team that owns it costs.'),
        {'type': 'pair', 'label': 'Read one against the other', 'between': 'against',
         'items': [{'label': 'Yearly cost of the wait', 'value': 'Up to ₹10.9 crore', 'state': 'outcome', 'point': 1, 'sub': 'Worked out from your real times: 5 hours 15 minutes a patient. The most it could be.',
                    'ask': {'label': 'Ask how it is worked out', 'say': 'How did you work out the ₹10.9 crore?'}},
                   {'label': 'One manager, two helpers', 'value': '₹10 to 11.5 lakh', 'state': 'start', 'point': 2, 'sub': 'A year, at the top of the range. One Discharge Manager and two Discharge Executives.',
                    'ask': {'label': 'Ask about the team', 'say': 'Why one manager and two helpers?'}}],
         'caption': 'If the trial wins back just one hour in a hundred of the wait, the team pays for itself.'},
        {'type': 'effect', 'label': 'Your discharges a day', 'value': '40 to 45', 'state': 'target', 'sub': 'Past the line of 40 where one person in charge is needed. Your own number, so this is not a maybe-someday.'}],
        'actions': acts('Next: what we would do first', 'What would we do first?', 'Tell me about your budget', 'About the budget for this: ')}})

# ---------------------------------------------------------------------------------------------- 07 · first steps (route)
SPECS.append({
    'turn': T(7, 'recommendation', 'What would we do first?', 'so-06 (route)', 'Solutions place, turn 6 (playbook §7: a low-commitment trial first, then a choice).', 'Solutions · next steps'),
    'chat': {'text': ['Start with a two-week trial on one ward. Begin with the consultants who decide latest, because they gain the most.',
                      'It needs no new staff and no new system. It turns our biggest guess into a measured fact.'],
             'invite': 'Which would you like to go into first?',
             'note': 'Prove it on one ward, then decide on the rest.',
             'points': P('The two-week trial', 'The person in charge', 'Linking the hospital software'),
             'prompts': ['Walk me through the daily automation', 'Scope the two-week trial', 'I’d need to check with my team'], 'pointer': 'Three steps on one path. At the end, pick a door.'},
    'canvas': {'blocks': [
        H('Next steps', 'Try it on one ward first', 'Three steps in order. The first needs nothing new from you.'),
        {'type': 'route', 'hint': 'Pick a step to open it. Then choose a door.',
         'steps': [{'title': 'Two-week trial on one ward', 'what': 'Night work starts for the consultants who decide latest.', 'point': 1},
                   {'title': 'Put one person in charge', 'what': 'One Discharge Manager now. Two helpers after the trial.', 'point': 2},
                   {'title': 'Link the hospital software', 'what': 'Your IT team lets Tojo read your records, so drafting can start.', 'point': 3}],
         'sheets': [S('r1', 'Two weeks', 'Two-week trial on one ward', 'The new order of work runs by hand on one ward. No new staff and no new system.',
                      [('Needs', 'No new staff, no new system', 'start'), ('We measure', 'Hours from ready to home')], 'Which ward has the latest deciders?'),
                    S('r2', 'During the trial', 'Put one person in charge', 'One Discharge Manager now, to run the trial. Two helpers once the trial shows your busy hours.',
                      [('Needs', 'A yes from your Head of Operations', 'target'), ('We measure', 'Patients home by noon')], 'Who could run the trial here?'),
                    S('r3', 'After the trial', 'Link the hospital software', 'Your IT team lets Tojo read your records. Then drafting and the running bill can start.',
                      [('Needs', 'One person in your IT team', 'target'), ('We measure', 'Summaries ready before the round ends')], 'Who looks after your hospital software?')],
         'fork': {'question': 'Which do you want to go into first?',
                  'options': [{'tab': 'Automations', 'label': 'The daily automation', 'what': 'What runs by itself, from the evening round to going home', 'say': 'Walk me through the daily automation'},
                              {'tab': 'Processes', 'label': 'Scoping the trial', 'what': 'Which ward, who records the times, what we measure', 'say': 'Scope the two-week trial'}]}}],
        'actions': acts('Next: the daily automation', 'Walk me through the daily automation', 'Tell me what your team thinks', 'My team’s view is: ')}})

NOTES = {'dp-so-01': 'Was turn-04 (sample conversation). The five parts as doors off one corridor.',
         'dp-so-02': 'Was so-01. The five parts as jigsaw pieces: pick one and see what it leans on.',
         'dp-so-03': 'Was so-02. The automation part as six switches on one wire to going home.',
         'dp-so-04': 'Was so-03. The correction: three routes hit a wall, one gets through.',
         'dp-so-05': 'Was so-04. Five knots in one wait, each undone by the parts that hold it. The tracing-paper background starts here.',
         'dp-so-06': 'Was so-05. What the wait costs against what the team costs.',
         'dp-so-07': 'Was so-06. Three steps on one path, then a door to Automations or Processes.'}
man = {'place': 'Solutions', 'tool': 'Discharge Process', 'turns': []}
for s in SPECS:
    s['review'] = {'status': 'approved', 'date': '2026-10-06', 'note': 'Approved 6 Oct with the regenerated Discharge turns.'}
    fn = s['turn']['id'] + '.json'
    json.dump(s, open(os.path.join(HERE, fn), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    man['turns'].append({'file': fn, 'note': NOTES[s['turn']['id']]})
json.dump(man, open(os.path.join(HERE, 'turns.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('wrote', len(SPECS), 'specs and turns.json')
