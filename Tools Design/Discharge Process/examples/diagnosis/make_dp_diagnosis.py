"""Writes the Discharge Process Diagnosis turns (dp-dg-01 to 03) and turns.json. Redone 5 Oct 2026 with the latest generators.

The content is the approved Discharge sample conversation (Common Elements/examples/turn-01 to turn-03, 250-bed hospital in
Bhubaneswar), put into plain, simple English. Each turn has its own drawing, the tool layer (entries typed in the drawing go into
the message) and the three buttons. Draw with: python3 ../../diagnosis-html-generator/dp_diagnosis_html.py build"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
JUMP = {'tab': 'Solutions', 'detail': 'How the wait could be fixed', 'say': 'Take me to Solutions'}
def acts(go, go_say, add, add_say): return {'go': {'detail': go, 'say': go_say}, 'add': {'detail': add, 'say': add_say}, 'jump': dict(JUMP)}
def P(*labels): return [{'n': i + 1, 'label': x, 'canvas': True} for i, x in enumerate(labels)]
def S(key, when, title, text, lines=(), entry=None, hint=None):
    s = {'key': key, 'when': when, 'title': title, 'text': text}
    if lines: s['lines'] = [dict(zip(('label', 'value', 'state'), l)) for l in lines]
    if entry: s['entry'] = entry
    if hint: s['entry_hint'] = hint
    return s
def T(n, typ, msg, was, context, label, user_tag=None):
    t = {'id': 'dp-dg-%02d' % n, 'type': typ, 'tool': 'Discharge Process', 'tab': 'Diagnosis', 'register': 'advisory', 'user_message': msg, 'was': was,
         'context': context, 'transcript': {'label': label}}
    if user_tag: t['user_tag'] = user_tag
    return t

SPECS = []
# ---------------------------------------------------------------------------------------------- 01 · the road to going home (ward-map)
STOPS = [('The doctors', 'now', '“Discharges are just slow”', 'The summary is drafted, checked and signed by different people. The round decides when any of it can start.', 'Who writes, checks and signs the summary?', 1),
         ('Supply count', 'next', '“Billing is slow”', 'The bill cannot be finished until nurses count the used supplies. They count only when they are free.', 'How long after signing do nurses start counting?', 2),
         ('Pharmacy returns', 'later', '“Still waiting on pharmacy”', 'What was given, what was used and what goes back. Counted by hand, it means a second pass on the bill.', 'Who works out the medicines going back?', 3),
         ('Billing', 'later', '“Bills changed at the counter”', 'A charge that arrives after the bill is closed opens it again.', 'How many bills were reopened last month?', 4),
         ('Insurance desk', 'later', None, 'The insurer’s approval sits inside the family’s wait.', 'Does your discharge time include the insurance wait?', None),
         ('Bed desk', 'later', None, 'Discharge times can only be checked against when beds were given out.', 'Can the bed desk say when beds were given?', None),
         ('Housekeeping', 'later', None, 'A bed is cleaned from when housekeeping hears, not from when the patient left.', 'How long until housekeeping hears a bed is free?', None),
         ('Transport', 'later', None, 'Porters are shared with admissions and scans, at the same busy hour.', 'How many porters work at the busy hour?', None),
         ('Operating theatre', 'later', None, 'A bed freed late cannot be used for an operation that same day.', 'What is the latest a freed bed helps?', None),
         ('Last checks', 'later', None, 'The dietitian, the pharmacist and the nurse must each see the patient, in no set order.', 'Who must see the patient before they leave?', None),
         ('Cash counter', 'later', None, 'Every patient going home meets one counter, in the same two hours.', 'Who can let a patient go with money owed?', None)]
SPECS.append({
    'turn': T(1, 'question', 'Discharge delays. Our patients are medically fit by mid-morning but most don’t leave till late afternoon.', 'turn-01 (dp-01), route-map',
              'Discharge sample conversation, turn 1 (playbook §1: check how the work really runs before proposing anything).', 'Sample conversation · turn 1 · walk the road'),
    'chat': {'text': ['Before I suggest anything, I want to see how discharge really runs at your hospital. Most delays that look like discharge problems start further up the road.',
                      'First stop, the doctors. Who writes the discharge summary, who checks it, and who signs it? And when do rounds finish on your busiest wards?'],
             'pointer': 'The whole road is drawn as rooms on one path. Tap any room to see what I will ask there.',
             'note': 'Most delays start long before the billing desk.',
             'points': P('The doctors: who writes, checks and signs', 'Nurses: when they count used supplies', 'Pharmacy: medicines going back', 'Billing: bills opened again'),
             'prompts': ['Rounds finish around 11 AM', 'A junior doctor writes it, the consultant signs', 'Why start with the doctors?']},
    'canvas': {'blocks': [
        {'type': 'heading', 'eyebrow': 'The road home · stop 1 of 11', 'title': 'The road to going home', 'deck': 'Eleven stops, each run by a different team. We walk them one at a time.'},
        {'type': 'ward-map', 'start_label': 'Doctor decides', 'end_label': 'Bed ready',
         'stops': [dict({'name': n, 'status': st, 'tag': chr(65 + i)}, **({'heard': h} if h else {}), **({'point': p} if p else {})) for i, (n, st, h, _, _, p) in enumerate(STOPS)],
         'sheets': [S(chr(97 + i), 'Stop %d of 11' % (i + 1), n, txt, ([('What we often hear', h.strip('“”'))] if h else []), q, 'Type a rough answer. It goes into your message.')
                    for i, (n, st, h, txt, q, p) in enumerate(STOPS)],
         'caption': 'Each stop is a team. The question in each room is the one I will ask when we get there.'}],
        'actions': acts('Next: answer the first stop', 'Rounds finish around 11 AM', 'Tell me about your doctors', 'About our doctors and the summary: ')}})

# ---------------------------------------------------------------------------------------------- 02 · price the wait (receipt + stat-strip)
SPECS.append({
    'turn': T(2, 'data-ask', 'Consultants finish rounds by about 11. The RMO drafts the summary, the consultant signs, and a transcriptionist types it up. We’re 250 beds, around 88% full, 40–45 discharges a day.',
              'turn-02 (dp-02), progress-trail + stat-strip + calculator', 'Discharge sample conversation, turn 2 (playbook §1.2: put a price on the wait before the diagnosis).', 'Sample conversation · turn 2 · price the wait', '@Point1'),
    'chat': {'text': ['Thank you. That is the first stop done. Three people handle every summary, and none of it starts before 11.',
                      'To put a price on the wait, I need three figures. They are on the bill in the drawing.'],
             'pointer': 'Type each figure straight onto the bill. Each one goes into your message.',
             'note': 'A delay only moves people once it has a price.',
             'points': P('What one bed earns in a day', 'Hours each patient waits to leave', 'When doctors decide who goes home', 'Your 250 beds, 88% in use'),
             'prompts': ['One bed earns about ₹35,000 a day', 'Where do I find the wait time?', 'I’d need to check with finance']},
    'canvas': {'blocks': [
        {'type': 'heading', 'eyebrow': 'Pricing the wait', 'title': 'What is the wait costing you?', 'deck': 'Your numbers are in. Three more and the wait has a price.'},
        {'type': 'receipt', 'title': 'Figures for Tojo', 'subtitle': 'Your hospital · the price of the wait',
         'lines': [{'label': 'What one bed earns', 'unit': 'a day, in rupees', 'placeholder': 'Type it here', 'point': 1},
                   {'label': 'Hours each patient waits to leave', 'unit': 'from ready to leaving', 'placeholder': 'Type it here', 'point': 2},
                   {'label': 'When doctors decide who goes home', 'unit': 'a clock time', 'placeholder': 'Type it here', 'point': 3}],
         'total_label': 'Yearly cost of the wait', 'waiting': 'Waiting on your figures', 'done': 'All three in. Send to Tojo.',
         'hint': 'Type each figure on its line. Tap a line to see what it is for.',
         'caption': 'Nothing here is my guess. Every figure comes from you.',
         'sheets': [S('rate', 'Figure 1 of 3', 'What one bed earns', 'Turns each hour a bed waits into rupees.'),
                    S('wait', 'Figure 2 of 3', 'Hours each patient waits to leave', 'From the doctor saying the patient can go, to the patient leaving. A rough number is fine.'),
                    S('decide', 'Figure 3 of 3', 'When doctors decide who goes home', 'Tells us when the going-home work could start, if anyone used that time.')]},
        {'type': 'stat-strip', 'stats': [{'label': 'Beds', 'value': '250', 'source': 'yours', 'point': 4}, {'label': 'Beds in use', 'value': '88%', 'source': 'yours', 'point': 4},
                                         {'label': 'Patients going home each day', 'value': '40–45', 'source': 'yours'}, {'label': 'Summary can start', 'value': 'About 11 AM', 'source': 'yours'}],
         'caption': 'What you have told me so far.'}],
        'actions': acts('Next: send the three figures', 'One bed earns about ₹35,000 a day', 'Send the figures you have', 'Here are the figures I have: ')}})

# ---------------------------------------------------------------------------------------------- 03 · the diagnosis (time-window + threshold-gauges + effect)
SPECS.append({
    'turn': T(3, 'diagnosis', 'One bed earns about ₹32,000 a day. Most patients are ready by 10 and leave around 3, so they wait about 5 hours. The doctors usually decide who’s going home on the 7 PM round, but they don’t sign till morning.',
              'turn-03 (dp-03), chain + threshold-gauges + calculator', 'Discharge sample conversation, turn 3 (playbook §2: name the dead window and the missing owner).', 'Sample conversation · turn 3 · the diagnosis', '@Point1 @Point2'),
    'chat': {'text': ['Your real problem is not slow discharge. It is time nobody uses, and nobody being in charge.',
                      'Your doctors already decide in the evening. But nothing happens until they sign the next morning. Most of the going-home work could be done overnight. Nobody does it today because:'],
             'bullets': ['Nothing is automatic, so starting early means doing the work twice.', 'No team moves until the doctor signs.', 'Nobody has ever been asked to use the evening.'],
             'invite': 'The second reason: your own numbers show you now need one person in charge of discharge. Does this match what you see on the wards?',
             'note': 'The time is already there. Nobody uses it.',
             'points': P('The hours nobody uses overnight', 'The doctor signs next morning', 'Needing one person in charge', 'What the waiting costs'),
             'prompts': ['Yes, show me how to fix it', 'Why doesn’t anyone use the evening now?', 'Our doctors won’t sign at night']},
    'canvas': {'blocks': [
        {'type': 'heading', 'eyebrow': 'What is really wrong', 'title': 'Unused hours, and nobody in charge', 'deck': 'One patient’s night and morning, on your own times.'},
        {'type': 'time-window', 'label': 'From the evening round to going home', 'axis_from': 18, 'axis_to': 40, 'tick': 4,
         'events': [{'time': 19, 'label': 'Doctor decides', 'state': 'start'}, {'time': 34, 'label': 'Patient ready', 'state': 'target'},
                    {'time': 35, 'label': 'Doctor signs', 'point': 2}, {'time': 39, 'label': 'Patient goes home', 'state': 'outcome'}],
         'window': {'start': 19, 'end': 35, 'label': 'Nothing happens', 'note': 'The decision is made. The work waits for the signature.', 'point': 1},
         'share': {'value': 'Most', 'label': 'of the going-home work could be done in these hours'},
         'caption': 'Ready by 10 AM, home by 3 PM: about 5 hours of waiting. All the times are yours.',
         'sheets': [S('dec', '7 PM round', 'Doctor decides', 'The doctor already knows who can go home tomorrow. Today that decision is not written down anywhere.', [('Today', 'Said, not recorded')], 'Who hears the decision on the round?', 'For example: only the ward nurse'),
                    S('ready', '10 AM', 'Patient ready to go', 'The patient is fit to leave. Nothing they need is ready yet.', [('Waiting from here', 'About 5 hours', 'target')], 'When are most of your patients ready?'),
                    S('sign', '11 AM', 'Doctor signs', 'Only now do the papers and the bill start. Three people handle every summary.', [('Starts after this', 'Papers and the bill')], 'What happens first after the signature?'),
                    S('home', 'About 3 PM', 'Patient goes home', 'Four hours after the signature, the patient leaves and the bed frees.', [('Ready to home', 'About 5 hours', 'outcome')], 'What usually holds up the last hour?')]},
        {'type': 'threshold-gauges', 'gauges': [
            {'label': 'Beds in use', 'caption': 'Over 80% needs one person in charge', 'min': 0, 'max': 100, 'value': 88, 'value_label': 'You: 88%', 'line': 80, 'line_label': '80%', 'point': 3},
            {'label': 'Patients going home a day', 'caption': 'Over 40 a day needs the same', 'min': 0, 'max': 60, 'value': 42.5, 'value_label': '40 to 45', 'band_low': 40, 'band_high': 45, 'line': 40, 'line_label': '40', 'point': 3}]},
        {'type': 'effect', 'label': 'What the waiting costs a year', 'value': 'Up to ₹10.3 crore', 'state': 'outcome',
         'sub': 'Worked out from your figures: 42.5 patients a day, 5 hours each, ₹32,000 a bed. True only if each freed bed fills that day.'}],
        'actions': acts('Next: how to fix it', 'Yes, show me how to fix it', 'Tell me what I missed', 'One more thing about our discharges: ')}})

NOTES = {'dp-dg-01': 'Was turn-01. The eleven stops as rooms on one path: the agenda, walked one stop at a time.',
         'dp-dg-02': 'Was turn-02. The three figures as lines on a bill, typed in place, with what is already known.',
         'dp-dg-03': 'Was turn-03. The unused hours on one line, the two lines for an owner, and the cost.'}
man = {'place': 'Diagnosis', 'tool': 'Discharge Process', 'turns': []}
for s in SPECS:
    s['review'] = {'status': 'approved', 'date': '2026-10-06', 'note': 'Approved 6 Oct with the regenerated Discharge turns.'}
    fn = s['turn']['id'] + '.json'
    json.dump(s, open(os.path.join(HERE, fn), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    man['turns'].append({'file': fn, 'note': NOTES[s['turn']['id']]})
json.dump(man, open(os.path.join(HERE, 'turns.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('wrote', len(SPECS), 'specs and turns.json')
