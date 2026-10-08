"""Writes the Discharge Process Automations turns (dp-au-01 to 08) and turns.json. Redone 5 Oct 2026 with the latest generators.

From the approved Discharge templates: turn-05 (the automatic paperwork, from the sample conversation) and au-01 to au-07 (the
Automations place), 250-bed hospital in Bhubaneswar, put into plain, simple English. One main drawing per turn, the tool layer and
the three buttons. Draw with: python3 ../../automations-html-generator/dp_automations_html.py build"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
JUMP = {'tab': 'Processes', 'detail': 'How the day changes on the wards', 'say': 'Take me to Processes'}
def acts(go, go_say, add, add_say): return {'go': {'detail': go, 'say': go_say}, 'add': {'detail': add, 'say': add_say}, 'jump': dict(JUMP)}
def P(*labels): return [{'n': i + 1, 'label': x, 'canvas': True} for i, x in enumerate(labels)]
def S(key, when, title, text, lines=(), entry=None, hint=None, hand=None, ask=None):
    s = {'key': key, 'when': when, 'title': title, 'text': text}
    if lines: s['lines'] = [dict(zip(('label', 'value', 'state'), l)) for l in lines]
    if entry: s['entry'] = entry
    if hint: s['entry_hint'] = hint
    if hand: s['hand'] = {'who': hand[0], 'does': hand[1]}
    if ask: s['ask'] = {'label': ask[0], 'say': ask[1]}
    return s
def T(n, typ, msg, was, context, label):
    return {'id': 'dp-au-%02d' % n, 'type': typ, 'tool': 'Discharge Process', 'tab': 'Automations', 'register': 'advisory', 'user_message': msg, 'was': was,
            'context': context, 'transcript': {'label': label}}
def H(eyebrow, title, deck, name, stage='Idea'):
    return {'type': 'heading', 'eyebrow': eyebrow, 'title': title, 'deck': deck, 'plate': {'tag': 'Automations', 'name': name, 'stage': stage}}

def CLK(t):
    h, m = [int(x) for x in t.split(':')]
    return 'Noon' if (h, m) == (12, 0) else '%d%s %s' % (h % 12 or 12, (':%02d' % m) if m else '', 'AM' if h < 12 else 'PM')

SPECS = []
# ---------------------------------------------------------------------------------------------- 01 · the going-home file (file)
SPECS.append({
    'turn': T(1, 'part', 'Start with the automatic paperwork', 'turn-05 (dp-05), chain + cards + stat-strip',
              'Discharge sample conversation, turn 5 (playbook §4: the automation part in this hospital’s own hold-ups).', 'Sample conversation · turn 5 · the automatic paperwork'),
    'chat': {'text': ['Here is what the software does at your hospital, from the 7 PM round to the patient going home. Why each piece matters:'],
             'bullets': ['It starts at the evening round, because your doctors already decide then. Nothing new is asked of them.',
                         'It keeps the bill up to date all day, so billing stops waiting for the nurses to count supplies.',
                         'It sends the first bill to insurance overnight, so the morning is not spent waiting for approval.'],
             'invite': 'Next is the changes on the wards: what each team does differently.',
             'note': 'The papers are ready before the doctor signs.',
             'points': P('The discharge summary', 'The running bill', 'The insurance request', 'Medicines to take home', 'What your IT team must do first'),
             'prompts': ['Show me the changes on the wards', 'Our doctors don’t use voice notes', 'What does our IT team need to do?'], 'pointer': 'Switch between today and with the automation. Pick a paper to open it.'},
    'canvas': {'blocks': [
        H('Part 1 of 5 · Automatic paperwork', 'Papers ready before the doctor signs', 'Every paper a patient needs to leave. Today each one starts after the 11 AM signature.', 'The going-home file'),
        {'type': 'file', 'label': 'The going-home file, one patient', 'hand_key': 'A person says yes',
         'switch': {'today': 'Today', 'with': 'With the automation', 'cap_today': 'Every paper waits for the 11 AM signature. The patient leaves about 3 PM.',
                    'cap_with': 'Each paper fills in from the evening round. Staff check and say yes.'},
         'docs': [{'title': 'Discharge summary', 'at_today': 'After 11 AM', 'today': 'Typed from the doctor’s notes', 'at_with': '7:30 PM', 'with': 'Drafted from notes in your files', 'hand': True, 'point': 1},
                  {'title': 'The running bill', 'at_today': 'After 11 AM', 'today': 'Built once supplies are counted', 'at_with': 'All day', 'with': 'Each charge added as it happens', 'hand': True, 'point': 2},
                  {'title': 'Insurance request', 'at_today': 'After the bill', 'today': 'Sent once the bill is final', 'at_with': 'Overnight', 'with': 'A first bill sent the evening before', 'point': 3},
                  {'title': 'Medicines to take home', 'at_today': 'After 11 AM', 'today': 'Listed after the signature', 'at_with': 'Evening', 'with': 'Listed for the pharmacy on the round', 'point': 4},
                  {'title': 'Supplies going back', 'at_today': 'At noon', 'today': 'Counted by the nurses first', 'at_with': 'Evening', 'with': 'Worked out from what was used'}],
         'condition': 'What must happen first: your IT team lets Tojo read your records. Without that link, none of these papers fill in.',
         'sheets': [S('sum', 'Paper 1 · the summary', 'Discharge summary', 'Drafted from notes, tests and medicines already in your files. The doctor checks and signs on the morning round.',
                      [('Today', 'Typed after 11 AM'), ('With it', 'Ready to sign at 7:30 PM', 'start')], 'Who types your summaries today?', None, ('the doctor', 'Checks the draft and signs it on a phone.')),
                    S('bill', 'Paper 2 · the bill', 'The running bill', 'Each charge goes on the bill as it happens, so it is ready when the doctor signs.',
                      [('Today', 'Built after the supply count'), ('With it', 'Up to date all day', 'start')], 'How long does your final bill take?', None, ('billing', 'Checks the bill before it goes out.')),
                    S('ins', 'Paper 3 · insurance', 'Insurance request', 'A first bill goes to the insurer the evening before, so approval is not waited for in the morning.',
                      [('Today', 'Sent after the final bill'), ('With it', 'Sent overnight', 'start')], 'Which insurers do most of your patients use?'),
                    S('med', 'Paper 4 · medicines', 'Medicines to take home', 'The list goes to the pharmacy on the evening round, so the medicines are packed by morning.',
                      [('Today', 'Listed after the signature'), ('With it', 'Packed by morning', 'start')], 'When does the pharmacy pack medicines now?'),
                    S('sup', 'Paper 5 · supplies', 'Supplies going back', 'What was given, used and left over is worked out from the records. Nurses check it, instead of counting first.',
                      [('Today', 'Counted by hand before billing'), ('With it', 'Worked out, nurses check', 'start')], 'Who counts the used supplies today?')]},
        {'type': 'effect', 'label': 'Hours each patient waits today', 'value': '5 hours', 'state': 'start', 'sub': 'Your own figure. This part is aimed at those hours. How many it removes here, a short trial will show.'}],
        'actions': acts('Next: walk through one night', 'Walk me through the daily automation', 'Tell me which paper is slowest', 'The slowest paper here is: ')}})

# ---------------------------------------------------------------------------------------------- 02 · the night shift (nightshift)
ST = [('19:30', 'Summary drafted', 'A draft summary to sign', True, 1, 'The doctor marks on the round that the patient can likely go. Tojo drafts the summary from notes already in your files.', 'Notes, reports and medicines', ('the doctor', 'Reads the early summary on the ward phone and signs it.'), 'Who is on your evening round?'),
      ('20:00', 'Bill and supplies brought up to date', 'The expected bill and the return list', False, 2, 'Every charge is already on the bill. Tojo adds what the patient will use, and works out what goes back to the pharmacy.', 'Billing records, medicines and supplies', None, 'Who counts returns today?'),
      ('21:00', 'Early insurance request', 'An early request to the insurer', False, 3, 'The expected bill goes to the insurance desk that evening, for first approval.', 'The expected bill and the summary', None, 'Which insurers would take an early request?'),
      ('21:30', 'Family and pharmacy told', 'A likely leaving time for the family', False, None, 'The family gets a likely time to leave. The pharmacy gets the list of medicines to pack.', 'The draft summary', None, 'How do you reach families today?'),
      ('08:30', 'Morning sign-off', 'The signed final summary', True, 4, 'The final summary is on the doctor’s phone on the morning round.', 'The overnight notes', ('the doctor', 'Confirms the discharge and signs in one tap.'), 'When does your morning round start?'),
      ('09:00', 'Final bill and insurance', 'The final bill, sent', True, None, 'The signed summary sends the final bill and the reports to the insurance desk by itself.', 'The signed summary', ('billing', 'Checks the final bill before it goes out.'), 'Who checks the final bill today?'),
      ('12:00', 'Empty bed alert', 'A cleaning alert with the bed number', False, 5, 'The moment the patient leaves, housekeeping and the bed desk hear, with the bed number.', 'The leaving time on the ward', None, 'How does housekeeping hear today?')]
SPECS.append({
    'turn': T(2, 'part', 'Walk me through the daily automation', 'au-01 (nightshift)', 'Automations place, turn 1 (one night on one ward, from the evening round to going home).', 'Automations · one night'),
    'chat': {'text': ['Here is one night on one ward, from the evening round to the patient going home.', 'Seven stations run by themselves. A person steps in at three of them, only to say yes.'],
             'invite': 'Pick any station to go deeper. The summary is the best place to start.',
             'note': 'The machines work all night. People only say yes.',
             'points': P('The summary on the evening round', 'The running bill', 'The early insurance request', 'The morning sign-off', 'The empty bed alert'),
             'prompts': ['How is the summary drafted all through the stay?', 'What does the doctor have to do?', 'Which reports come in late?'], 'pointer': 'Play the night, or move the clock. Pick a station to open it.'},
    'canvas': {'blocks': [
        H('Automations · one night', 'One night, seven stations', 'What runs between the evening round and the patient going home. A hand marks where a person says yes.', 'The night shift', 'Built'),
        {'type': 'nightshift', 'from': '18:00', 'to': '15:00', 'start_at': '18:00', 'play': 'Play the night', 'ready_label': 'Ready by',
         'clock': ['18:00', '20:00', '21:30', '02:00', '08:30', '09:00', '12:00'], 'night': {'from': '22:00', 'to': '07:30', 'label': 'Nothing waits now'},
         'goal': {'at': '12:00', 'label': 'Home by', 'source': 'target'},
         'stations': [dict({'at': a, 'title': t, 'makes': m}, **({'hand': True} if h else {}), **({'point': p} if p else {})) for a, t, m, h, p, d, r, hd, q in ST],
         'condition': 'Every station is designed, not switched on. The times are goals, not yet measured here.',
         'sheets': [S('s%d' % (i + 1), CLK(a), t, d, [('Reads', r), ('Makes', m, 'start')], q, None, hd) for i, (a, t, m, h, p, d, r, hd, q) in enumerate(ST)]}],
        'actions': acts('Next: how the summary is drafted', 'How is the summary drafted all through the stay?', 'Tell me about your nights', 'On a usual night on our wards: ')}})

# ---------------------------------------------------------------------------------------------- 03 · the summary writes itself (brain)
DAYS = [('Day 1', 'Admitted', ['a', 'b', 'd', 'g'], 'Chest pain, admitted through Emergency. Blood tests and a heart tracing. Three medicines started.', 'What is recorded on arrival at your hospital?'),
        ('Day 2', 'Tests', ['b', 'f', 'd', 'e', 'g'], 'A heart scan shows a narrowed vessel. One medicine changed. A drip set and syringes used.', 'Where do test results land today?'),
        ('Day 3', 'Procedure', ['c', 'e', 'd', 'f', 'g'], 'A stent is placed in the narrowed vessel. A blood thinner is started. Stable after the procedure.', 'How are procedure notes kept?'),
        ('Day 4', 'Evening round', ['f', 'd', 'b', 'f'], 'The doctor says the patient can go tomorrow. Two strips of one medicine are left over.', 'What does the doctor note on this round?')]
SPECS.append({
    'turn': T(3, 'deeper', 'How is the summary drafted all through the stay?', 'au-02 (brain)', 'Automations place, turn 2 (playbook §5: tell me more, one level further down).', 'Automations · the summary writes itself'),
    'chat': {'text': ['The night showed the summary appear on the evening round. It can, because it has been writing itself since admission.',
                      'Each day, Tojo records what happens to the patient. By the evening round, most of the summary is already there.'],
             'note': 'The summary is written a little each day, not all at once.',
             'points': P('What is recorded on arrival', 'Tests and what they showed', 'Medicines, counted in strips', 'The doctor’s daily notes'),
             'prompts': ['Explain the first three steps on the round', 'Won’t this take our nurses’ time?', 'What if a report comes in late?'], 'pointer': 'Pick a day, or play the stay. The summary fills in, day by day.'},
    'canvas': {'blocks': [
        H('Automations · the summary', 'The summary that writes itself', 'One patient’s four days. Each day adds to the summary, so it is mostly written by the evening round.', 'The running summary', 'Built'),
        {'type': 'brain', 'passes_label': 'Day of the stay', 'play': 'Play the stay', 'in_label': 'What is recorded', 'out_label': 'The summary, filling in', 'count_label': 'facts recorded, none typed twice',
         'kinds': [{'k': 'a', 'name': 'On arrival', 'example': 'History, symptoms and what doctors found', 'point': 1}, {'k': 'b', 'name': 'Tests and findings', 'example': 'Each result, anything unusual marked', 'point': 2},
                   {'k': 'c', 'name': 'Procedures', 'example': 'Each procedure, with its notes'}, {'k': 'd', 'name': 'Medicines', 'example': 'Given, changed and left over, in strips', 'point': 3},
                   {'k': 'e', 'name': 'Supplies', 'example': 'Used and left over, in whole units'}, {'k': 'f', 'name': 'Daily progress', 'example': 'The doctor’s notes on each round', 'point': 4},
                   {'k': 'g', 'name': 'Reasons and outcomes', 'example': 'Why each step was taken, and what happened'}],
         'outputs': [{'name': 'Reason for admission', 'from': ['a']}, {'name': 'Tests and what they showed', 'from': ['b']}, {'name': 'Treatment given', 'from': ['c', 'g']},
                     {'name': 'Medicines to take home', 'from': ['d']}, {'name': 'Supplies to return', 'from': ['e']}, {'name': 'How the stay went', 'from': ['f']}],
         'passes': [{'label': d, 'what': w, 'brings': k} for d, w, k, t, q in DAYS],
         'condition': 'The patient here is an example only. Your records would fill the summary the same way.',
         'sheets': [S('d%d' % (i + 1), d, w, t, [('Adds to the summary', '%d facts' % len(k), 'start')], q) for i, (d, w, k, t, q) in enumerate(DAYS)]}],
        'actions': acts('Next: the three steps on the round', 'Explain the first three steps on the round', 'Tell me how notes are kept', 'Our doctors keep their notes like this: ')}})

# ---------------------------------------------------------------------------------------------- 04 · three steps on the round (agent)
SPECS.append({
    'turn': T(4, 'deeper', 'Explain the first three steps on the round', 'au-03 (agent)', 'Automations place, turn 3 (the loop on the evening round, and who says yes).', 'Automations · three steps on the round'),
    'chat': {'text': ['The summary was already filling in. Here are the three steps on the evening round, and who says yes at each.', 'Tojo gathers, checks and drafts. People make every decision.'],
             'note': 'Tojo drafts. The doctor decides.',
             'points': P('Hearing the decision', 'Putting the draft together', 'The doctor’s yes'),
             'prompts': ['How would you record each decision?', 'What if the doctor changes their mind?', 'Does it work for insured patients?'], 'pointer': 'Pick a step. The loop lights where Tojo is.'},
    'canvas': {'blocks': [
        H('Automations · on the round', 'Three steps, one yes each', 'What happens between the doctor’s word and the draft on their phone.', 'The evening round', 'Built'),
        {'type': 'agent', 'hint': 'Pick a step. The loop lights where Tojo is, and its sheet opens.',
         'loop': [{'id': 'n', 'name': 'Notice'}, {'id': 'g', 'name': 'Gather'}, {'id': 'c', 'name': 'Check'}, {'id': 'd', 'name': 'Draft'}, {'id': 'a', 'name': 'Ask'}],
         'steps': [{'when': 'On the evening round', 'title': 'Hear the decision', 'stages': ['n', 'c'], 'point': 1},
                   {'when': 'Within minutes', 'title': 'Put the draft together', 'stages': ['g', 'c', 'd'], 'point': 2},
                   {'when': 'Before the round ends', 'title': 'Ask for the yes', 'stages': ['a'], 'point': 3}],
         'caption': 'Tojo’s loop: it notices, gathers, checks, drafts, then asks a person.', 'steps_label': 'On the evening round',
         'never_label': 'What it never does', 'never': ['It never decides who goes home.', 'It never signs for a doctor.', 'It never guesses a missing result.', 'It never changes a patient’s record.'],
         'sheets': [S('hear', 'On the evening round', 'Hear the decision', 'The doctor taps once on the ward phone to say the patient can likely go tomorrow. Tojo takes that as its signal.',
                      [('Checks first', 'It is the patient’s own doctor'), ('And', 'The patient is not waiting on a test')], 'What would stop a patient going tomorrow?', None, ('the doctor', 'Taps once to say the patient can likely go.')),
                    S('draft', 'Within minutes', 'Put the draft together', 'Tojo gathers the facts recorded since admission. It writes the draft summary, the expected bill and the medicines to take home.',
                      [('Checks first', 'Every test result is in'), ('And', 'The bill matches what was used')], 'Which part of the summary is hardest to write?'),
                    S('yes', 'Before the round ends', 'Ask for the yes', 'The draft is on the doctor’s phone. Anything missing or unclear is marked for the doctor to look at.',
                      [('Checks first', 'Late reports are named, never guessed')], 'Who else should see the draft?', None, ('the doctor', 'Reads the early summary, then signs or corrects it.'))]}],
        'actions': acts('Next: how each decision is recorded', 'How would you record each decision?', 'Tell me about your rounds', 'On our evening round: ')}})

# ---------------------------------------------------------------------------------------------- 05 · where the facts come from (sources) · the night background starts
SRC = [('h', 'Hospital software: billing and notes', 'the hospital software', 'Charges, doctors’ notes and medicines given', 'waiting', 2, 'Charges, the doctor’s daily notes, medicines given and supplies used. One read-only link.', 'Which software holds your bills and notes?'),
       ('r', 'The scan and lab report system', 'the report system', 'Every test result and report', 'waiting', 3, 'Every test result and scan report, the moment it is signed off. So the summary never waits for a report.', 'Do reports come from a separate system?'),
       ('p', 'The pharmacy stock list', 'the pharmacy list', 'What was issued, and what is left', 'needed', 4, 'Strips and bottles issued and returned. Needed only for the supply count.', 'Is the pharmacy stock kept on a system?')]
AUTOS = [{'name': 'Family and pharmacy told that evening', 'needs': ['f']}, {'name': 'Running bill kept up to date', 'needs': ['h']}, {'name': 'Early insurance request', 'needs': ['f', 'h']},
         {'name': 'Summary drafted on the evening round', 'needs': ['f', 'h', 'r']}, {'name': 'Final summary signed on a phone', 'needs': ['f', 'h', 'r']}, {'name': 'Supply count for the nurses', 'needs': ['h', 'p']}]
SPECS.append({
    'turn': T(5, 'deeper', 'How would you record each decision?', 'au-04 (sources)', 'Automations place, turn 4 (where each fact comes from, and what needs no IT work).', 'Automations · where the facts come from'),
    'chat': {'text': ['Each fact comes from a place your hospital already keeps it. Here are those places, and what each one holds.', 'One of them needs no IT work at all. That is the one-tap form on the ward phone.'],
             'note': 'Start with what needs no link. Add the links one at a time.',
             'points': P('The one-tap form', 'Billing and clinical notes', 'Scan and lab reports', 'The pharmacy list'),
             'prompts': ['What exactly does our IT team need?', 'Can we test one without the link?', 'What if some notes are on paper?'], 'pointer': 'Try a setting, or flip the switches. Each lamp lights when everything it needs is linked.'},
    'canvas': {'blocks': [
        H('Automations · where facts come from', 'Four places, one at a time', 'Each automation lights only when every place it reads from is linked. The form needs no IT work.', 'The switchboard', 'Built'),
        {'type': 'sources', 'src_label': 'Where the facts are kept', 'auto_label': 'What can switch on', 'hint': 'Try a setting or flip a switch. Pick a place to see what it holds.',
         'main': {'id': 'f', 'tag': 'Start here', 'name': 'One-tap form on the ward phone', 'short': 'the form', 'line': 'Needs no IT work. Each decision from the round', 'point': 1},
         'sources': [{'id': i, 'name': n, 'short': sh, 'holds': h, 'link': l, 'point': p} for i, n, sh, h, l, p, t, q in SRC],
         'automations': AUTOS, 'default_on': ['f'],
         'presets': [{'label': 'No IT work', 'on': ['f']}, {'label': 'Link the hospital software', 'on': ['f', 'h']}, {'label': 'Add the reports', 'on': ['f', 'h', 'r']}, {'label': 'Everything', 'on': ['f', 'h', 'r', 'p']}],
         'condition': 'Which systems your hospital uses is still to be checked. These are the usual ones.',
         'sheets': [S(i, 'Read-only link', n, t, [('Holds', h)], q) for i, n, sh, h, l, p, t, q in SRC]}],
        'actions': acts('Next: what your IT team needs', 'What exactly does our IT team need?', 'Tell me which systems you run', 'Our hospital runs these systems: ')}})

# ---------------------------------------------------------------------------------------------- 06 · one question for IT (helper)
ASKS = [('Read-only access to billing and notes', 'Your IT team, once', 'Needed', 'needed', 'Tojo only reads. Nothing can be changed or deleted.', 'Who could give read-only access?'),
        ('Each report, as it is signed', 'Your IT team, with the lab', 'Needed', 'needed', 'So the summary never waits for a report.', 'How do reports reach doctors today?'),
        ('The list of charges and their prices', 'Billing, with IT', 'A list', 'waiting', 'So the bill can be kept up to date, charge by charge.', 'Where is your price list kept?'),
        ('A test copy of one ward’s records', 'Your IT team, once', 'For testing', 'waiting', 'With the patient names hidden. So we can try it before any real patient.', 'Which ward could we copy?'),
        ('One named person in your IT team', 'Your Head of IT', 'One person', 'ours', 'One contact, so questions do not wait.', 'Who looks after your hospital software?')]
SPECS.append({
    'turn': T(6, 'question', 'What exactly does our IT team need?', 'au-05 (helper)', 'Automations place, turn 5 (playbook §7: one plain question first, the technical detail only if asked).', 'Automations · one question for IT'),
    'chat': {'text': ['One question first, before any list. The answer decides what your IT team has to link.', 'Are your billing and your doctors’ notes in one system, or in separate ones?'],
             'invite': 'Anything more technical can wait. Say so, and I will park it until you are ready.',
             'note': 'One question now. The rest can wait.',
             'points': P('Read-only access', 'Reports as they are signed', 'A test copy first'),
             'prompts': ['Yes, one system. Reports are separate.', 'This is too technical for now', 'I’d need to check with our IT team'], 'pointer': 'Pick an ask to see why it is needed and who does it.'},
    'canvas': {'blocks': [
        H('Automations · your IT team', 'Five asks, nothing changed', 'Each ask only reads, or is a one-off. Your IT team changes nothing in your systems.', 'The IT links'),
        {'type': 'helper', 'says': 'One question for you first. Then these five things for your IT team. None of it is needed today.', 'label': 'What I would ask IT',
         'asks': [{'title': t, 'who': w, 'tag': g, 'tag_state': st, **({'point': [1, 2, None, 3, None][i]} if [1, 2, None, 3, None][i] else {})} for i, (t, w, g, st, y, q) in enumerate(ASKS)],
         'park': 'Anything more technical can wait. Say so, and Tojo will park it until you are ready.',
         'sheets': [S('a%d' % (i + 1), 'Ask %d of 5' % (i + 1), t, y, [('Who does it', w)], q) for i, (t, w, g, st, y, q) in enumerate(ASKS)]},
        {'type': 'effect', 'label': 'Changed in your systems', 'value': 'Nothing', 'state': 'start', 'sub': 'Every link only reads. Your records stay as they are, and your teams keep working in them.'}],
        'actions': acts('Next: answer the one question', 'Yes, one system. Reports are separate.', 'Tell me about your systems', 'Our billing and notes are kept like this: ')}})

# ---------------------------------------------------------------------------------------------- 07 · the order of switching on (panel)
ROWS = [('Family and pharmacy told', 'Works from the form alone', [3, 3, 3, 3], 1, 'The family gets a likely leaving time, the pharmacy its list. Needs only the form.', 'How do families hear today?'),
        ('Running bill kept up to date', 'Needs the hospital software', [0, 3, 3, 3], 2, 'Each charge is added as it happens. The first link lights it.', 'Who builds the bill today?'),
        ('Early insurance request', 'The form and the software', [0, 3, 3, 3], None, 'The expected bill goes to the insurer the evening before.', 'Which insurers take early requests?'),
        ('Summary drafted on the round', 'Needs the reports too', [0, 1, 3, 3], 3, 'Drafted from notes and reports. Built after link 1, switched on with link 2.', 'Which reports come in late?'),
        ('Final summary signed on a phone', 'Needs the reports too', [0, 1, 3, 3], None, 'The doctor signs the final summary on the morning round.', 'Would your consultants sign on a phone?'),
        ('Supply count for the nurses', 'Waits on the pharmacy list', [0, 1, 1, 3], 4, 'Works out what goes back. Waits for the pharmacy stock list.', 'Is the pharmacy stock on a system?')]
SPECS.append({
    'turn': T(7, 'findings', 'Yes, one system. Reports are separate.', 'au-06 (sources, redrawn)', 'Automations place, turn 6 (the answer sets the order: the form, then one link, then the reports).', 'Automations · the order of switching on'),
    'chat': {'text': ['That helps. One link to the hospital software lights most of the board. The reports are a second, smaller link.', 'So the order is simple. The form first, then the hospital software, then the reports.'],
             'note': 'Notes and bills in one place. Most of the work is one link.',
             'points': P('The form, with no IT work', 'The first link', 'The report link', 'What waits on the pharmacy'),
             'prompts': ['What about the bed after the patient leaves?', 'This is getting too technical', 'Scope the two-week trial'], 'pointer': 'Step through the links. The lamps light as each automation can switch on.'},
    'canvas': {'blocks': [
        H('Automations · the order', 'The form first, then two links', 'Your answer sets the order. Step through it and watch which automations light.', 'The build panel', 'Built'),
        {'type': 'panel', 'phases_label': 'The order', 'rows_label': 'Automation', 'foot': 'Discharge desk · build panel', 'hint': 'Step through the order. Pick a row to see when it switches on.',
         'phases': [{'when': 'Day 1', 'name': 'The form, no IT work'}, {'when': 'Link 1', 'name': 'Billing and notes'}, {'when': 'Link 2', 'name': 'The reports'}, {'when': 'Later', 'name': 'The pharmacy list'}],
         'mains': [{'tag': 'Main switch 1', 'name': 'The one-tap form', 'line': 'On the ward phone, from day 1', 'on_at': 0},
                   {'tag': 'Main switch 2', 'name': 'The hospital software link', 'line': 'Billing and notes, in one system', 'on_at': 1}],
         'automations': [dict({'name': n, 'line': l, 'stages': st}, **({'point': p} if p else {})) for n, l, st, p, t, q in ROWS],
         'sheets': [S('r%d' % (i + 1), ['On from day 1', 'On with link 1', 'On with link 1', 'On with link 2', 'On with link 2', 'On last'][i], n, t, [('Needs', l)], q) for i, (n, l, st, p, t, q) in enumerate(ROWS)]},
        {'type': 'effect', 'label': 'Lit by the first link', 'value': '4 of 6', 'state': 'outcome', 'sub': 'With the form and the hospital software link, four of the six automations can switch on.'}],
        'actions': acts('Next: the bed after the patient leaves', 'What about the bed after the patient leaves?', 'Tell me about your reports', 'Our reports reach the doctors like this: ')}})

# ---------------------------------------------------------------------------------------------- 08 · the bed after leaving (relay)
LEGS = [('dis', 'The ward', 'Patient leaves the ward', 'About 3:15 PM', 'Recorded as it happens', False, 1, 'The ward marks the leaving time on the phone. Tojo passes it on at once.', 'Who records the leaving time today?'),
        ('dis', 'Tojo', 'Housekeeping hears', 'When someone calls', 'At once, with the bed', True, 2, 'Housekeeping gets an alert with the bed number and the time.', 'How does housekeeping hear today?'),
        ('bed', 'Housekeeping', 'Bed cleaned and made', 'Starts late', 'Starts within minutes', False, None, 'Housekeeping marks the bed clean on their phone when it is done.', 'How long does a clean take?'),
        ('bed', 'The bed desk', 'Bed shown as ready', 'About 4:30 PM', 'The minute it is clean', True, 3, 'The bed desk sees the bed turn ready, without a phone call.', 'How does the bed desk see a ready bed?'),
        ('bed', 'The bed desk', 'Next patient in the bed', 'Not recorded today', 'Recorded and checked', True, 4, 'The time the next patient arrives is recorded. Both sides check each other’s times.', 'When does the next patient usually arrive?')]
SPECS.append({
    'turn': T(8, 'deeper', 'What about the bed after the patient leaves?', 'au-07 (relay)', 'Automations place, turn 7 (the hand-over to the bed, each side checking the other).', 'Automations · the bed after leaving'),
    'chat': {'text': ['The discharge does not end at the door. Today the bed stays empty 75 minutes before the next patient can use it.'],
             'bullets': ['Housekeeping hears late, so cleaning starts late.', 'The bed desk learns a bed is free only when someone calls.',
                         'Nobody checks the other side’s times. So a late discharge can be written down as an early one.'],
             'invite': 'Next, we can look at how the day changes on the wards.',
             'note': 'A discharge ends when the next patient is in the bed.',
             'points': P('The patient leaves', 'The housekeeping alert', 'The bed shown as ready', 'The next patient in'),
             'prompts': ['Who at the bed desk would see this?', 'Where do the automations stand now?', 'This is getting too technical'], 'pointer': 'Switch between today and both sides linked. Pick a step to open it.'},
    'canvas': {'blocks': [
        H('Automations · after the door', 'The bed is the last step', 'From the patient leaving to the next patient in the bed, on both sides.', 'The bed hand-over'),
        {'type': 'relay', 'with_label': 'Both sides linked', 'lane_dis': 'The discharge side', 'lane_bed': 'The bed side', 'hint': 'Pick a step of the hand-over. Switch to see it with both sides linked.',
         'gap': {'label': 'Time the bed stands empty', 'today': '75 minutes, yours', 'with': 'Under 30 minutes, a goal'},
         'legs': [dict({'side': sd, 'who': w, 'name': n, 'today': td, 'with': wi}, **({'checked': True} if c else {}), **({'point': p} if p else {})) for sd, w, n, td, wi, c, p, t, q in LEGS],
         'condition': 'Past 30 minutes, the hand-over is slow, or a time is not what really happened. This check needs the bed desk’s own times.',
         'sheets': [S('l%d' % (i + 1), {'dis': 'The discharge side', 'bed': 'The bed side'}[sd], n, t, [('Today', td), ('Linked', wi, 'start')], q) for i, (sd, w, n, td, wi, c, p, t, q) in enumerate(LEGS)]},
        {'type': 'effect', 'label': 'Bed empty after leaving', 'value': '75 minutes', 'state': 'outcome', 'sub': 'Your own number. The goal is under 30 minutes, checked by both sides.'}],
        'actions': acts('Next: how the day changes on the wards', 'Show me the changes on the wards', 'Tell me about your bed desk', 'Our bed desk works like this: ')}})

NOTES = {'dp-au-01': 'Was turn-05 (sample conversation). The going-home file, paper by paper, today and with the automation.',
         'dp-au-02': 'Was au-01. One night on one ward: seven stations, a hand where a person says yes.',
         'dp-au-03': 'Was au-02. The summary written a little each day, on the engine’s screen.',
         'dp-au-04': 'Was au-03. The loop on the evening round, and what it never does.',
         'dp-au-05': 'Was au-04. The places facts are kept, as switches. The night-shift background starts here.',
         'dp-au-06': 'Was au-05. Tojo at the desk: one question, then five asks for IT.',
         'dp-au-07': 'Was au-06 (the switchboard again). Now the build panel: the order of switching on.',
         'dp-au-08': 'Was au-07. The hand-over from the patient leaving to the next patient in the bed.'}
man = {'place': 'Automations', 'tool': 'Discharge Process', 'turns': []}
for s in SPECS:
    s['review'] = {'status': 'approved', 'date': '2026-10-06', 'note': 'Approved 6 Oct with the regenerated Discharge turns.'}
    fn = s['turn']['id'] + '.json'
    json.dump(s, open(os.path.join(HERE, fn), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    man['turns'].append({'file': fn, 'note': NOTES[s['turn']['id']]})
json.dump(man, open(os.path.join(HERE, 'turns.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('wrote', len(SPECS), 'specs and turns.json')
