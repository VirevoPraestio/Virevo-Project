"""Writes the Discharge Process Processes turns (dp-pr-01 to 14) and turns.json. Redone 5 Oct 2026 with the latest generators.

From the approved Discharge templates: turn-06 to turn-12 (the sample conversation: the ward changes, the people, the team, the
measures, the plan, the trial times asked and given) and pr-01 to pr-07 (the Processes place), 250-bed hospital in Bhubaneswar,
put into plain, simple English. One main drawing per turn (the filled timesheet redraws the blank one), the tool layer and the
three buttons. Draw with: python3 ../../processes-html-generator/dp_processes_html.py build"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
JUMP = {'tab': 'Diagnosis', 'detail': 'Back to what is really wrong', 'say': 'Take me to Diagnosis'}
def acts(go, go_say, add, add_say): return {'go': {'detail': go, 'say': go_say}, 'add': {'detail': add, 'say': add_say}, 'jump': dict(JUMP)}
def P(*labels): return [{'n': i + 1, 'label': x, 'canvas': True} for i, x in enumerate(labels)]
def S(key, when, title, text, lines=(), entry=None, hint=None, ask=None):
    s = {'key': key, 'when': when, 'title': title, 'text': text}
    if lines: s['lines'] = [dict(zip(('label', 'value', 'state'), l)) for l in lines]
    if entry: s['entry'] = entry
    if hint: s['entry_hint'] = hint
    if ask: s['ask'] = {'label': ask[0], 'say': ask[1]}
    return s
def T(n, typ, msg, was, context, label, user_tag=None):
    t = {'id': 'dp-pr-%02d' % n, 'type': typ, 'tool': 'Discharge Process', 'tab': 'Processes', 'register': 'advisory', 'user_message': msg, 'was': was,
         'context': context, 'transcript': {'label': label}}
    if user_tag: t['user_tag'] = user_tag
    return t
def H(eyebrow, title, deck, column, name):
    return {'type': 'heading', 'eyebrow': eyebrow, 'title': title, 'deck': deck, 'plate': {'column': column, 'name': name}}

SPECS = []
# ---------------------------------------------------------------------------------------------- 01 · the ward changes, on one clock (night-lanes)
LANES = [('Evening round', 'Doctors', None, ('19:00', '19:45', 'Decided, not written down', 'plain'), ('19:00', '19:45', 'Decision recorded, papers start', 'start'), 1,
          'Doctors already decide on the 7 PM round. Today nothing is written down, so no team can start.', 'Who hears the decision on the round today?'),
         ('Discharge papers', 'Doctors, typists', 'Biggest hold-up', ('11:00', '12:30', 'Typed after the round', 'outcome'), ('19:30', '21:00', 'Drafted, signed on a phone', 'start'), 2,
          'The papers are the biggest hold-up today, so they change the most. A ready draft is checked and signed.', 'How long does one summary take to type?'),
         ('Bill and supplies', 'Nurses, billing', None, ('12:00', '13:30', 'Counted, then billed', 'plain'), ('19:00', '23:00', 'Kept up to date', 'start'), 3,
          'Today nurses count supplies before billing can start. With the change, the bill is kept up to date and nurses only check.', 'Who counts the supplies today?'),
         ('Insurance', 'Insurance desk', None, ('13:30', '14:30', 'Sent after the bill', 'plain'), ('21:00', '22:00', 'First bill sent that night', 'start'), 4,
          'Today the insurer is asked only once the bill is final. With the change, a first bill goes the evening before.', 'Which insurers take longest?'),
         ('Family and transport', 'Ward nurse', None, ('13:00', '15:00', 'Called on the day', 'plain'), ('20:00', '21:00', 'Told the night before', 'start'), 5,
          'Today the family is called late and arrives in the afternoon. With the change, they hear the leaving time that evening.', 'When does the family hear today?'),
         ('Admissions', 'The same team', 'Check this', ('12:00', '16:00', 'Wait behind discharges', 'target'), ('09:00', '12:00', 'Run at the same time', 'start'), None,
          'One team runs leaving and arriving, so admissions queue behind discharges. Split the team, or run both at once. It costs nothing but the new order.', 'Is it one team, or two?')]
SPECS.append({
    'turn': T(1, 'part', 'Show me the changes on the wards', 'turn-06 (dp-06), two-flow + cards', 'Discharge sample conversation, turn 6 (playbook §4: function by function, today against with Virevo).', 'Sample conversation · turn 6 · the changes on the wards'),
    'chat': {'text': ['Most of the work stays the same. What changes is when it starts, and who writes it. Why these changes:'],
             'bullets': ['Starting in the evening only works if each team knows it has started, so the software tells them.', 'Staff approve instead of writing, so nobody does the same work twice.',
                         'The discharge papers are the biggest hold-up today, so they change the most.'],
             'invite': 'Next is the people who must agree, and who has the most to give up.',
             'note': 'Same steps. They just start the night before.',
             'points': P('The evening round', 'Discharge papers, the biggest hold-up', 'The bill and the supply count', 'Insurance', 'Family and transport'),
             'prompts': ['Show me the people who must agree', 'Why are the papers the biggest hold-up?', 'One team does both discharges and admissions'], 'pointer': 'Switch between today and with the changes. Pick a job to open it.'},
    'canvas': {'blocks': [
        H('Part 2 · Changes on the wards', 'Same steps, started the night before', 'Each job on one clock, from the evening round to the next afternoon.', 'Changes', 'The ward’s day'),
        {'type': 'night-lanes', 'from': '18:00', 'to': '16:00', 'night': {'from': '23:00', 'to': '07:00', 'label': 'The night'},
         'switch': {'today': 'Today', 'with': 'With the changes', 'cap_today': 'Everything waits for the 11 AM signature. The patient leaves about 3 PM.', 'cap_with': 'Most of the work moves to the evening before. The morning only checks and signs.'},
         'lanes': [dict({'name': n, 'who': w, 'today': dict(zip(('from', 'to', 'label', 'state'), td)), 'with': dict(zip(('from', 'to', 'label', 'state'), wd))}, **({'flag': f} if f else {}), **({'point': p} if p else {}))
                   for n, w, f, td, wd, p, t, q in LANES],
         'caption': 'The 7 PM round and the 11 AM signature are your times. The other times are my estimate.',
         'sheets': [S('l%d' % (i + 1), w, n, t, [('Today', td[2]), ('With the change', wd[2], 'start')], q) for i, (n, w, f, td, wd, p, t, q) in enumerate(LANES)]}],
        'actions': acts('Next: the people who must agree', 'Show me the people who must agree', 'Tell me how your wards run', 'On our wards today: ')}})

# ---------------------------------------------------------------------------------------------- 02 · who must agree (people)
TEAMS = [('Doctors', 'Say who goes home at 7 PM. Sign on a phone next morning.', False, 1, 'They already decide at 7 PM, which is why they can agree. Nothing extra is asked of them.', [('Extra time', 'None, if no extra round or login', 'start')], 'Which doctors would you ask first?'),
         ('Typists', 'Check and correct a ready draft, instead of typing each one.', True, 2, 'Typists have the most to give up. They check drafts first, and nobody loses a job at the start.', [('At the start', 'Check drafts, no job cut', 'target')], 'How many typists work on summaries?'),
         ('Nurses', 'Check what the software writes, instead of counting supplies first.', False, None, 'The supply count before billing goes. Nurses check a list that is already made.', [('Saves', 'The count before billing', 'start')], 'Who counts supplies on your wards?'),
         ('Billing and insurance', 'Check bills that are already made.', False, 3, 'The bill is kept up to date through the stay. Billing checks it, instead of building it after the signature.', [('Saves', 'Building the bill at noon', 'start')], 'How long does billing take today?'),
         ('IT team', 'Link the software to records, bills, lab reports and scans.', False, 4, 'The software can only read what it is linked to. Your IT team gives read-only access, once.', [('Asks', 'Read-only access, once', 'target')], 'Who looks after your hospital software?'),
         ('Bed desk and wards', 'Act when the software says a bed or a patient is ready.', False, None, 'Each team is told when it is their turn. Nobody waits for a phone call.', [('Gets', 'A message when it is their turn')], 'How does the bed desk hear a bed is free?')]
SPECS.append({
    'turn': T(2, 'part', 'Show me the people who must agree', 'turn-07 (dp-07), role-cards + stat-strip', 'Discharge sample conversation, turn 7 (playbook §4: only the roles this conversation touched, and the one approver).', 'Sample conversation · turn 7 · who must agree'),
    'chat': {'text': ['Several teams touch discharge, but only a few are asked to change much. One person has to approve it. Why each matters:'],
             'bullets': ['Doctors are asked for no extra time. They already decide at 7 PM, which is why they can agree.', 'Typists have the most to give up, so they check drafts first, and nobody loses a job at the start.',
                         'The Head of Operations must approve the new order, or it will not last past the first busy morning.'],
             'invite': 'Next is who is in charge: whether you need anyone new.',
             'note': 'Help first. Fewer hands only once it is trusted.',
             'points': P('Doctors', 'Typists, who have the most to give up', 'Billing and the insurance desk', 'The IT team', 'Head of Operations'),
             'prompts': ['Show me who is in charge', 'Will anyone lose their job?', 'Our consultants won’t sign on a phone'], 'pointer': 'Pick a team to see what changes for them.'},
    'canvas': {'blocks': [
        H('Part 3 · People who must agree', 'Who has to say yes', 'Six teams touched, one approver. Each team’s room says what it is asked to do.', 'People', 'Who says yes'),
        {'type': 'people', 'teams_label': 'Six teams, and what each is asked', 'resist_tag': 'Most to give up',
         'teams': [dict({'title': n, 'gets': g}, **({'resist': True} if r else {}), **({'point': p} if p else {})) for n, g, r, p, t, l, q in TEAMS],
         'approver': {'tag': 'Sign-off', 'title': 'Head of Operations', 'line': 'Approves the new order of steps, and splitting discharges from admissions.'},
         'managers': [{'tag': 'New role', 'title': 'Discharge Manager', 'line': 'Owns every discharge'}, {'title': 'Bed desk manager', 'line': 'Owns the beds'}],
         'tree_note': 'Peers. Both report to the Head of Operations, who signs off the new order.',
         'sheets': [S('t%d' % (i + 1), n, n, t, l, q) for i, (n, g, r, p, t, l, q) in enumerate(TEAMS)]},
        {'type': 'effect', 'label': 'Jobs cut at the start', 'value': 'None', 'state': 'start', 'sub': 'The software helps each person first. It takes work away only once everyone trusts it.'}],
        'actions': acts('Next: who is in charge', 'Show me who is in charge', 'Tell me who would push back', 'The people who would push back here are: ')}})

# ---------------------------------------------------------------------------------------------- 03 · who is in charge (sizing)
SPECS.append({
    'turn': T(3, 'part', 'Show me who is in charge', 'turn-08 (dp-08), cards + compare-table + stat-strip', 'Discharge sample conversation, turn 8 (playbook §4: the peak-load check on this hospital’s own pattern).', 'Sample conversation · turn 8 · who is in charge'),
    'chat': {'text': ['You need one person to own discharge, and two people to run it day to day. Why:'],
             'bullets': ['Nobody owns the whole wait today, and your own numbers are past the lines where one owner is needed.',
                         'Two helpers, not three, because your work comes in two busy times of day, not spread across 24 hours.',
                         'Every other team only records and approves a little more. Their jobs do not change.'],
             'invite': 'Last part: how we will know it worked.',
             'note': 'One owner, two helpers, sized to your busy hours.',
             'points': P('The Discharge Manager', 'The Discharge Executives', 'Why two helpers, not three', 'What the roles cost'),
             'prompts': ['Show me how we’ll know it worked', 'Can one of our nurses become the manager?', 'Our busy hours change at weekends'], 'pointer': 'Pick a role to open it. The two chains show why two helpers, not three.'},
    'canvas': {'blocks': [
        H('Part 4 · Who is in charge', 'One owner, two helpers', 'The roles, then the two ways to size the helpers: the usual rule, and your busy hours.', 'Roles', 'Who is in charge'),
        {'type': 'sizing', 'roles_label': 'The roles', 'new_tag': 'New role',
         'roles': [{'title': 'Discharge Manager', 'line': 'Owns the whole process. About ₹4 to 4.5 lakh a year.', 'new': True, 'point': 1},
                   {'title': 'Discharge Executives', 'line': 'Look after each patient going home. About ₹3 to 3.5 lakh each.', 'new': True, 'point': 2},
                   {'title': 'Everyone else', 'tag': 'Team', 'line': 'Records and approves a little more. Same jobs.'}],
         'chains': [{'title': 'The usual rule', 'verdict': 'About 3', 'state': 'muted', 'steps': [{'title': 'One helper per 15 a day', 'line': 'A rule of thumb'}, {'title': '42.5 a day, divided by 15', 'line': 'The middle of your 40 to 45'},
                                                                                              {'title': 'About 3 helpers', 'line': '₹9 to 10.5 lakh a year'}]},
                    {'title': 'Your busy hours', 'verdict': 'Use this', 'state': 'outcome', 'steps': [{'title': 'Two busy times a day', 'line': 'The 7 PM round, then 11 AM to about 3 PM'}, {'title': 'One helper for each', 'line': 'Sized to the peak, not the day'},
                                                                                                {'title': '2 helpers', 'line': '₹6 to 7 lakh a year', 'state': 'outcome'}]}],
         'caption': 'My working from your times. Check it against your staff rota before hiring.',
         'sheets': [S('dm', 'New role', 'Discharge Manager', 'One person answers for every delay, instead of each team blaming the process. Works with the bed desk manager as an equal.',
                      [('Cost', 'About ₹4 to 4.5 lakh a year'), ('Needed because', 'Past 80% full and 40 a day', 'target')], 'Could someone you have take this role?'),
                    S('de', 'New role', 'Discharge Executives', 'They take over each patient from the evening round. They spot delays as they happen and chase the team holding things up.',
                      [('Cost', 'About ₹3 to 3.5 lakh each'), ('How many', 'Two, one for each busy time', 'start')], 'When are your two busiest times?'),
                    S('ev', 'Same jobs', 'Everyone else', 'Every other team only records and approves a little more. Their jobs do not change.',
                      [('Changes', 'A little more recording')], 'Which team would feel this most?')]},
        {'type': 'effect', 'label': 'New roles, cost a year', 'value': '₹10 to 11.5 lakh', 'state': 'target', 'sub': 'One manager and two helpers. About 1% of what the waiting costs a year, worked out from your figures.'}],
        'actions': acts('Next: how we will know it worked', 'Show me how we’ll know it worked', 'Tell me about your busy hours', 'Our busiest times for discharges are: ')}})

# ---------------------------------------------------------------------------------------------- 04 · how we will know (gauges)
MEAS = [('Hours from ready to home', 'Starting number 5 hours, from you', 'result', False, 0.5, 1, 'From the doctor saying the patient can go, to the patient leaving. Counted for every patient, reported every week, ward by ward.', [('Starting number', '5 hours, yours', 'start')], 'Who could record the leaving time?'),
        ('Home by 10 AM', 'Goal: 10 AM, insured patients by 1 PM', 'result', True, None, 2, 'The share of each day’s patients who have left by those times. The first week of the trial sets the starting number.', [('Starting number', 'None yet. The trial sets it', 'target')], 'How many leave before noon today?'),
        ('Decided on the evening round', 'Share of decisions made at 7 PM', 'lead', True, None, 3, 'The earlier the decision is recorded, the more of the night can be used. This warns early when it slips.', [('Starting number', 'None yet. The trial sets it', 'target')], 'Do any wards decide later than 7 PM?'),
        ('Insurance approval time', 'From the first bill to the yes', 'lead', True, None, 4, 'With the first bill sent the evening before, this should fall first. Read for insured patients only.', [('Starting number', 'None yet. The trial sets it', 'target')], 'How long do approvals take today?'),
        ('Money won back', 'Bed days freed, in rupees', 'result', True, None, 5, 'What the freed bed time earns, against the most it could be. Read after the trial.', [('The most it could be', '₹10.3 crore a year', 'outcome')], 'Who in finance would check it?'),
        ('Patients going home a day', '40 to 45 today, from you', 'lead', False, 0.71, None, 'Watched each month against the line for the Discharge Manager. No goal, only a watch.', [('Starting number', '40 to 45, yours', 'start')], 'Does this change by season?')]
SPECS.append({
    'turn': T(4, 'part', 'Show me how we’ll know it worked', 'turn-09 (dp-09), cards + stat-strip', 'Discharge sample conversation, turn 9 (playbook §4: only the measures with a number or a goal; new ones marked new).', 'Sample conversation · turn 9 · the measures'),
    'chat': {'text': ['We will watch a short list of numbers, week by week. Where you already gave me a number, that is where we start. Why these:'],
             'bullets': ['They measure the wait itself, not how busy people are, so a busy week cannot hide a slow one.', 'They start from your own numbers, so progress is measured against you, not other hospitals.',
                         'Nothing tracks some of them today. Those are marked new, and the trial’s first week gives their starting number.'],
             'invite': 'That is all five parts. Shall I put them into a plan, starting with a short trial?',
             'note': 'Measure the wait, not the effort.',
             'points': P('Hours from ready to home', 'Patients home by 10 AM', 'Decisions made on the evening round', 'Insurance approval time', 'Money won back'),
             'prompts': ['Yes, put it into a plan', 'Who reports these numbers each week?', 'What counts as a good result?'], 'pointer': 'Pick a dial to see how it is measured. Dashed dials have no number yet.'},
    'canvas': {'blocks': [
        H('Part 5 · Knowing it worked', 'The numbers we will watch', 'Six dials. Two already have your number. The rest get theirs from the trial’s first week.', 'Measures', 'The six dials'),
        {'type': 'gauges', 'filters': {'all': 'All six', 'lead': 'Early warnings', 'result': 'Results'}, 'key_line': 'Dashed dials: nobody measures these today.', 'new_tag': 'New', 'tracked_tag': 'Yours',
         'measures': [dict({'title': t, 'reading': r, 'kind': k, 'new': nw}, **({'needle': nd} if nd is not None else {}), **({'point': p} if p else {})) for t, r, k, nw, nd, p, tx, l, q in MEAS],
         'caption': 'A number nobody has measured is marked new, never guessed.',
         'sheets': [S('m%d' % (i + 1), ('Result' if k == 'result' else 'Early warning') + (' · new' if nw else ''), t, tx, l, q) for i, (t, r, k, nw, nd, p, tx, l, q) in enumerate(MEAS)]}],
        'actions': acts('Next: put it into a plan', 'Yes, put it into a plan', 'Tell me what you track today', 'Each week we already look at: ')}})

# ---------------------------------------------------------------------------------------------- 05 · the plan (circuit)
SPECS.append({
    'turn': T(5, 'recommendation', 'Yes — put it into a plan', 'turn-10 (dp-10), chain + cards + stat-strip', 'Discharge sample conversation, turn 10 (playbook §7: a low-commitment trial, a threshold already met, a choice).', 'Sample conversation · turn 10 · the plan'),
    'chat': {'text': ['Start with a two-week trial on one ward. It needs no new staff and no new system. It tells us how much of the 5 hours comes back.',
                      'Hire the Discharge Manager now, not after the trial. Your own numbers are past both lines, so this is not a maybe-someday. They can run the trial.'],
             'invite': 'Would you like me to plan the two-week trial, or first walk through what the full software does each day?',
             'note': 'Prove it on one ward, then grow it.',
             'points': P('The two-week trial', 'Hiring the Discharge Manager now', 'Linking the software', 'Cost against what is at stake'),
             'prompts': ['Let’s plan the two-week trial', 'Why hire the manager before the trial ends?', 'What will the trial cost us?'], 'pointer': 'Pick a switch. The current runs to it, and the bulb lights at the last one.'},
    'canvas': {'blocks': [
        H('The plan', 'Try it on one ward first', 'Four switches, in order. Patients go home sooner only when every one is on.', 'The trial', 'The plan'),
        {'type': 'circuit', 'source': {'label': 'Today', 'line': 'Ready at 10 AM, home at 3 PM'}, 'goal': {'label': 'Home hours sooner', 'line': 'How many hours, the trial will show'},
         'steps': [{'when': 'Week 1', 'title': 'Start the trial on one ward', 'line': 'The new order of steps, by hand. No new system.', 'state': 'start', 'point': 1},
                   {'when': 'Weeks 1 and 2', 'title': 'Measure the wait every day', 'line': 'One person writes down the times for each patient.', 'point': 1},
                   {'when': 'Week 3', 'title': 'Decide using the numbers', 'line': 'Spread it, or adjust and try again.'},
                   {'when': 'After that', 'title': 'Link the software, ward by ward', 'line': 'Your IT team gives read-only access.', 'point': 3}],
         'readout': 'The trial turns the biggest guess, how many hours come back, into a measured fact.',
         'sheets': [S('w1', 'Week 1', 'Start the trial on one ward', 'The trial runs the new order of steps by hand, so it needs no new system. One ward with a usual mix of patients.',
                      [('Needs', 'One ward, the doctors’ yes', 'target'), ('Cost', 'No new staff, no new system', 'start')], 'Which ward would you pick?'),
                    S('w2', 'Weeks 1 and 2', 'Measure the wait every day', 'Week 1 runs as usual and records the times. Week 2 runs the new order and records the same times.',
                      [('Who records', 'The Discharge Manager, or a nurse')], 'Who could write the times down?'),
                    S('w3', 'Week 3', 'Decide using the numbers', 'We read the two weeks side by side. If the hours fell, we spread it. If not, we adjust and try again.',
                      [('We read', 'Hours from ready to home')], 'Who should be in the room to decide?'),
                    S('it', 'After that', 'Link the software, ward by ward', 'Once the order works by hand, the software takes over the writing. Your IT team gives read-only access.',
                      [('Needs', 'One person in your IT team', 'target')], 'Who looks after your hospital software?')]},
        {'type': 'effect', 'label': 'Hire the manager now', 'value': 'Not a maybe-someday', 'state': 'target', 'sub': '88% of beds in use against a line of 80%. 40 to 45 a day against a line of 40. Both are your numbers.'}],
        'actions': acts('Next: plan the two-week trial', 'Let’s plan the two-week trial', 'Tell me what worries you', 'What worries me about the plan is: ')}})

# ---------------------------------------------------------------------------------------------- 06 · the trial times, asked (timesheet blank + notes)
STEPS = [('Doctor decides', 'time', 1), ('Doctor signs', 'time', 2), ('Papers ready', 'time', None), ('Bill final', 'time', 3), ('Insurance approves', 'time, if insured', 4), ('Patient leaves', 'time', None), ('Bed ready again', 'time', 5)]
WHY = ['The decision starts everything. If nobody writes it down, say so.', 'The morning signature. Today every paper waits for it.', 'When the summary is ready to hand over.',
       'When the final bill is closed.', 'For insured patients only. When the insurer says yes.', 'When the patient leaves the ward.', 'When the bed is clean and ready for the next patient.']
SPECS.append({
    'turn': T(6, 'data-ask', 'Let’s plan the two-week trial', 'turn-11 (dp-11), fill-blank + cards', 'Discharge sample conversation, turn 11 (playbook §6: the blank day to fill in, then redrawn with the real times).', 'Sample conversation · turn 11 · the trial times'),
    'chat': {'text': ['Before the trial starts, I need your real times for one normal weekday. They become the starting numbers the trial is measured against.', 'Rough times are fine. If nobody writes a step down today, just say so.'],
             'note': 'Rough times now beat perfect times never.',
             'points': P('When doctors decide', 'When doctors sign', 'When the bill is final', 'When insurance approves', 'When the bed is ready again'),
             'prompts': ['Here are the times for a normal Tuesday', 'We don’t write down when doctors decide', 'Can the Discharge Manager collect these?'], 'pointer': 'Type a rough time on each step. Each one goes into your message.'},
    'canvas': {'blocks': [
        H('The trial · your starting times', 'One normal day, step by step', 'Seven steps. Type a rough time on each one, straight into the drawing.', 'The trial', 'Your starting times'),
        {'type': 'timesheet', 'mode': 'blank', 'label': 'Times for Tojo', 'day': 'A normal weekday', 'count_label': 'Times typed in', 'waiting': 'None typed yet', 'done': 'All seven in. Send to Tojo.',
         'steps': [dict({'title': t, 'field': f}, **({'point': p} if p else {})) for t, f, p in STEPS],
         'caption': 'The trial ward on a normal weekday. Rough is fine. Leave a box empty if nobody records it.',
         'sheets': [S('s%d' % (i + 1), 'Step %d of 7' % (i + 1), t, WHY[i]) for i, (t, f, p) in enumerate(STEPS)]},
        {'type': 'notes', 'label': 'The trial, week by week', 'items': [{'tag': 'Week 1', 'title': 'Watch', 'text': 'Run discharge the usual way. Write down every time.', 'state': 'start'},
                                                                       {'tag': 'Week 2', 'title': 'The new order', 'text': 'Start the papers, the bill and insurance on the evening round.'},
                                                                       {'tag': 'Week 3', 'title': 'Decide', 'text': 'Compare the two weeks, then choose.', 'state': 'target'}],
         'sheets': [S('n1', 'Week 1', 'Watch', 'Nothing changes on the ward yet. The Discharge Manager, or a nurse you choose, writes down the times for each patient.', [('At the end', 'Your real starting numbers', 'start')]),
                    S('n2', 'Week 2', 'The new order', 'Doctors say who is going home on the evening round, as they already do. Papers and the bill start that evening.', [('Records', 'The same times, to compare')]),
                    S('n3', 'Week 3', 'Decide', 'We read the two weeks side by side and choose: spread it, or adjust and try again.', [('We read', 'Hours from ready to home')])]}],
        'actions': acts('Next: send the times', 'Here are the times for a normal Tuesday', 'Tell me what you do not record', 'Nobody records these steps today: ')}})

# ---------------------------------------------------------------------------------------------- 07 · the real times, back (timesheet filled + findings)
FILLED = [('Doctor decides', 'time', '6–9 PM', None, 'target', 1), ('Doctor signs', 'time', '11 AM', 'about 14 hours', 'plain', None), ('Papers ready', 'time', '12:30 PM', '1½ hours', 'plain', 3),
          ('Bill final', 'time', '1:30 PM', '1 hour', 'plain', None), ('Insurance approves', 'time, if insured', '2:30 PM', '1 hour', 'plain', None), ('Patient leaves', 'time', '3:15 PM', '45 minutes', 'outcome', 2),
          ('Bed ready again', 'time', '4:30 PM', '75 minutes', 'target', 4)]
SPECS.append({
    'turn': dict(T(7, 'findings', 'A normal Tuesday: doctors decide anywhere from 6 to 9 PM, depending on the consultant. They sign around 11. Papers ready 12:30, bill final 1:30, insurance approves around 2:30, patient leaves 3:15, bed ready 4:30.',
                   'turn-12 (dp-12), fill-blank filled + cards + stat-strip', 'Discharge sample conversation, turn 12 (playbook §6: say what shifted, recompute, name what holds).', 'Sample conversation · turn 12 · your real times'), redraw_of='dp-pr-06'),
    'chat': {'text': ['Your real times change the picture a little, and mostly in a useful way. Two of my guesses held up. One was wrong in a way that helps.',
                      'The decision time is not fixed. It moves with each consultant. So the trial should start with the consultants who decide latest, because their patients lose the most of the evening.'],
             'invite': 'Shall I update the trial plan with these times?',
             'note': 'The latest decisions lose the most time.',
             'points': P('When doctors decide', 'The wait from ready to home', 'Papers after signing', 'The bed after the patient leaves'),
             'prompts': ['Yes, update the trial plan', 'Why is the bed ready so late?', 'Can consultants decide earlier?'], 'pointer': 'Your normal Tuesday, on the same line. Pick a step or a finding to open it.'},
    'canvas': {'blocks': [
        H('The trial · your starting times', 'One normal day, step by step', 'Your normal Tuesday on the same line, with the time between each step.', 'The trial', 'Your starting times'),
        {'type': 'timesheet', 'mode': 'filled', 'label': 'Your times', 'day': 'A normal Tuesday',
         'steps': [dict({'title': t, 'field': f, 'value': v, 'state': st}, **({'gap': g} if g else {}), **({'point': p} if p else {})) for t, f, v, g, st, p in FILLED],
         'caption': 'All seven times are yours. The gaps are worked out from them.',
         'sheets': [S('s%d' % (i + 1), 'Step %d of 7' % (i + 1), t, WHY[i], [('Your time', v, st if st != 'plain' else 'start')] + ([('Since the step before', g)] if g else [])) for i, (t, f, v, g, st, p) in enumerate(FILLED)]},
        {'type': 'findings', 'label': 'What your times changed', 'items': [{'tag': 'Changed', 'value': 'Decided 6 to 9 PM', 'line': 'Not a fixed 7 PM. It depends on the consultant.', 'point': 1},
                                                                      {'tag': 'Confirmed', 'value': 'Papers take 1½ hours', 'line': 'Signed at 11 AM, ready at 12:30.', 'point': 3},
                                                                      {'tag': 'New', 'value': 'Bed ready 75 minutes later', 'line': 'The bed sits empty after the patient leaves.', 'point': 4}],
         'caption': 'Muted, because these are your facts. Nothing in this row is my proposal.',
         'sheets': [S('f1', 'Changed', 'Doctors decide 6 to 9 PM', 'The unused hours overnight are 14 to 17, not 16. Patients of late deciders get the least time, so the trial starts with those consultants.', [('Was', 'A fixed 7 PM, my guess')], 'Which consultants decide latest?'),
                    S('f2', 'Confirmed', 'Papers take 1½ hours', 'This is the typing step the software removes. It was the biggest hold-up I expected, and your times agree.', [('Held up', 'The biggest hold-up', 'start')]),
                    S('f3', 'New', 'Bed ready 75 minutes later', 'Part of this may be waiting for housekeeping to hear. We will check it in the trial.', [('Goal', 'Under 30 minutes', 'target')], 'How does housekeeping hear today?')]},
        {'type': 'effect', 'label': 'Hours each patient waits', 'value': '5 hours 15 minutes', 'state': 'outcome', 'sub': 'Your times. I had 5 hours. The yearly cost moves from ₹10.3 crore to ₹10.9 crore, the most it could be.'}],
        'actions': acts('Next: update the trial plan', 'Yes, update the trial plan', 'Tell me about one of the times', 'About one of our times: ')}})

# ---------------------------------------------------------------------------------------------- 08 · the two weeks (trial)
PHASES = [(1, 3, 'Record today’s times', 'Ward nurse in charge', 2, 'Nothing changes yet. The ward records when each patient is ready to go and when they leave.', ['Ready to go home', 'Left the ward', 'Bed ready again']),
          (4, 7, 'The evening round starts it', 'Doctors and the night nurse', 3, 'Doctors mark likely discharges on the evening round. The night nurse starts the papers and the bill.', ['Decided on the evening round', 'Papers ready by the morning round']),
          (8, 11, 'Insurance and family the night before', 'Insurance desk and ward nurse', None, 'The insurance desk sends its request the evening before. The family hears the leaving time that night.', ['Insurance approval time', 'Family told the night before']),
          (12, 14, 'Read the numbers', 'You, the ward and Tojo', 4, 'Compare the trial days with days 1 to 3. Then choose: adjust and try again, or spread to more wards.', ['Hours from ready to home', 'Patients home by 10 AM'])]
SPECS.append({
    'turn': T(8, 'part', 'Scope the two-week trial', 'pr-01 (trial)', 'Processes place, turn 1 (the trial, day by day: three quiet days first, then the changes in two steps).', 'Processes · the two weeks'),
    'chat': {'text': ['Here is the trial, day by day. Nothing changes for the first three days, so we get the ward’s own starting times.', 'Then the changes come in two steps. On days 12 to 14 we read the numbers together.'],
             'invite': 'Next, we can see who has to agree before day 1.',
             'note': 'Three quiet days first. Then we know what changed.',
             'points': P('The trial ward', 'Days 1 to 3, today’s times', 'The evening round', 'Reading the numbers'),
             'prompts': ['Who has to agree to this?', 'What changes on the ward, step by step?', 'Which ward should we start on?'], 'pointer': 'Play the two weeks, or pick a part of the trial to open it.'},
    'canvas': {'blocks': [
        H('Processes · the trial', 'Two weeks on one ward', 'Fourteen days, in four parts. Nothing changes in the first three.', 'The trial', 'The two weeks'),
        {'type': 'trial', 'ward': {'label': 'The ward whose consultants decide latest', 'status': 'needed', 'note': 'They gain the most, so the change shows fastest. You pick the ward.', 'ask': 'Which ward would you start on?', 'ask_hint': 'Type the ward’s name', 'point': 1},
         'needs': ['No new staff', 'No new system', 'The one-tap form on a ward phone', 'One person to record the times'],
         'phases': [dict({'from': a, 'to': z, 'title': t, 'who': w}, **({'point': p} if p else {})) for a, z, t, w, p, x, r in PHASES],
         'condition': 'Goals for each measure are set on day 3, from the ward’s own times. None are guessed now.',
         'sheets': [S('p%d' % (i + 1), 'Days %d to %d' % (a, z), t, x, [('Who acts', w)] + [('Recorded', ', '.join(r[:2]))], 'What would get in the way on these days?') for i, (a, z, t, w, p, x, r) in enumerate(PHASES)]}],
        'actions': acts('Next: who has to agree', 'Who has to agree to this?', 'Tell me which ward to start on', 'The ward we would start on is: ')}})

# ---------------------------------------------------------------------------------------------- 09 · who agrees (badges)
PEOPLE = [('Head of Operations', 'Approves the flow', 'to_ask', True, 1, 'Signs off the new order of work across departments. Takes no part in the daily tasks.', 'One Discharge Manager reports the numbers every week.', None),
          ('Doctors', 'Works on the trial ward', 'worried', True, 2, 'Mark likely discharges on the evening round with one tap. Sign the early summary.', 'The summary is ready to check, not to write.', '“Our doctors don’t use voice notes.” So the trial uses a tap.'),
          ('Nurses', 'Works on the trial ward', 'to_ask', True, None, 'Record the ready and leaving times. Start the papers after the evening round.', 'No rush for medicines and papers at noon.', None),
          ('Billing', 'Works on the trial ward', 'to_ask', True, 3, 'Checks a bill kept up to date all stay, instead of building it at the end.', 'No pile of bills at noon.', None),
          ('Insurance desk', 'Works on the trial ward', 'to_ask', True, None, 'Sends the early request the evening before.', 'Fewer calls chasing the insurer the next day.', None),
          ('Housekeeping', 'Watches for updates', 'to_ask', True, None, 'Hears the moment a patient leaves, with the bed number.', 'No waiting for a phone call.', None),
          ('Pharmacy and diet', 'Watches for updates', 'to_ask', True, None, 'Told that evening who goes home tomorrow.', 'Medicines packed before the morning rush.', None),
          ('Bed desk', 'Watches for updates', 'to_ask', False, None, 'Sees each bed turn ready without a call.', 'The next patient is placed sooner.', None),
          ('IT team', 'After the trial', 'to_ask', False, 4, 'Lets Tojo read the hospital software. Nothing can be changed or deleted.', 'One clear list, asked for once.', None)]
SPECS.append({
    'turn': T(9, 'part', 'Who has to agree to this?', 'pr-02 (people)', 'Processes place, turn 2 (who agrees, team by team, and the one approver of the flow).', 'Processes · who agrees'),
    'chat': {'text': ['Nine teams are touched, but only one approves the flow. Your Head of Operations signs off the new order of work, not the daily tasks.',
                      'Doctors matter most. You said they do not use voice notes, so the trial asks them for one tap, not a new habit.'],
             'invite': 'Next, we can walk through each change on the ward.',
             'note': 'Help with each job first. Fewer hours come later.',
             'points': P('Head of Operations', 'Doctors', 'Billing', 'The IT team'),
             'prompts': ['What changes on the ward, step by step?', 'How do we win over the doctors?', 'Do we need to hire anyone?'], 'pointer': 'Pick a name badge to see what changes for that person.'},
    'canvas': {'blocks': [
        H('Processes · who agrees', 'Nine badges, one approver', 'Each badge says where that person stands. Most are still to ask.', 'People', 'Who agrees'),
        {'type': 'badges', 'rule': 'Tojo comes in as help with each job, not a threat to it. Any fall in staff hours comes later, once it is trusted.',
         'people': [dict({'name': n, 'group': g, 'status': st}, **({'trial': True} if tr else {}), **({'point': p} if p else {})) for n, g, st, tr, p, c, ga, sd in PEOPLE],
         'sheets': [S('b%d' % (i + 1), g, n, c, [('What they gain', ga, 'start')] + ([('What you told us', sd)] if sd else []), 'What would %s say?' % n.lower().replace('it team', 'your IT team').replace('head of operations', 'your Head of Operations'))
                    for i, (n, g, st, tr, p, c, ga, sd) in enumerate(PEOPLE)]}],
        'actions': acts('Next: each change on the ward', 'What changes on the ward, step by step?', 'Tell me who has already agreed', 'These people have already agreed: ')}})

# ---------------------------------------------------------------------------------------------- 10 · the ward changes, step by step (swap)
ROWS = [('Evening round', 'Doctors', 'Discharges decided the next morning', None, 'Likely discharges marked with one tap', '6 to 9 PM', None, 1, 'Who marks discharges on your round?'),
        ('Discharge summary', 'Doctors, night nurse', 'Typed next morning, waits for a signature', '10 AM to noon', 'Drafted overnight, signed on the morning round', None, 'Biggest hold-up', 2, 'Who types summaries today?'),
        ('Supplies and bill', 'Nurses, billing', 'Counted and drawn up after signing', None, 'Kept up to date all through the stay', None, None, None, 'Who counts supplies today?'),
        ('Bill sign-off', 'Billing', 'Built from the start at the end', '90 minutes', 'Checked, not built', None, None, None, 'How long does sign-off take?'),
        ('Insurance', 'Insurance desk', 'Asked once the bill is final', 'About 1 hour', 'Early request sent the evening before', None, None, 3, 'Which insurers take longest?'),
        ('Family and transport', 'Ward nurse', 'Called at the end of the day', None, 'Told the leaving time the night before', None, None, None, 'When does the family hear today?'),
        ('The bed', 'Housekeeping', 'Hears late, so cleaning starts late', '75 minutes', 'Told the moment the patient leaves', None, None, 4, 'How does housekeeping hear today?')]
SPECS.append({
    'turn': T(10, 'part', 'What changes on the ward, step by step?', 'pr-03 (swap)', 'Processes place, turn 3 (seven changes, one for each step of the day).', 'Processes · the changes, step by step'),
    'chat': {'text': ['Seven changes, one for each step of the day. The work itself stays the same. Only its timing moves.', 'The biggest hold-up is the summary. Moving it to the evening round frees most of the morning.'],
             'invite': 'Next, we can size the team that keeps this running.',
             'note': 'Same work. Earlier in the day.',
             'points': P('The evening round', 'The summary, the biggest hold-up', 'Insurance the evening before', 'The empty bed'),
             'prompts': ['Do we need to hire anyone?', 'Who at the bed desk would see this?', 'Which measures show it worked?'], 'pointer': 'Move each magnet across, or move them all. Pick a step to open it.'},
    'canvas': {'blocks': [
        H('Processes · the changes', 'Seven magnets, moved across', 'Each step of the day. Move its magnet to see what it becomes.', 'Changes', 'Step by step'),
        {'type': 'swap', 'with_label': 'With the changes', 'keeps': 'The flow of work stays the same. The new timing sits on top of it, and costs nothing but order.',
         'rows': [dict({'name': n, 'who': w, 'today': t}, **({'today_at': ta} if ta else {}), **({'with': wi}), **({'with_at': wa} if wa else {}), **({'flag': f} if f else {}), **({'point': p} if p else {}))
                  for n, w, t, ta, wi, wa, f, p, q in ROWS],
         'sheets': [S('w%d' % (i + 1), w, n, 'Today: %s. With the change: %s.' % (t.lower(), wi.lower()), [('Today', t + (', ' + ta if ta else ''))] + [('With the change', wi + (', ' + wa if wa else ''), 'start')], q)
                    for i, (n, w, t, ta, wi, wa, f, p, q) in enumerate(ROWS)]}],
        'actions': acts('Next: do we need to hire anyone', 'Do we need to hire anyone?', 'Tell me which change worries you', 'The change that worries me is: ')}})

# ---------------------------------------------------------------------------------------------- 11 · who to hire (seats)
SPECS.append({
    'turn': T(11, 'recommendation', 'Do we need to hire anyone?', 'pr-04 (seats)', 'Processes place, turn 4 (the roles, their triggers, and the busy-hours check on your own pattern).', 'Processes · who to hire'),
    'chat': {'text': ['Yes. One Discharge Manager and two Discharge Executives.', 'The flat rule says three Executives. Your busy hours say two, one for each window.', 'At 40 to 45 discharges a day, the Manager is needed now. You are already there.'],
             'invite': 'Next, we can see how this joins up with the bed desk.',
             'note': 'Size the team to your busy hours, not your daily total.',
             'points': P('The Discharge Manager', 'More than 40 discharges a day', 'The two Discharge Executives', 'The busy-hours check'),
             'prompts': ['Why not one person for both jobs?', 'Who at the bed desk would see this?', 'Which measures show it worked?'], 'pointer': 'Move the slider and switch the rule. The chairs and the cost follow.'},
    'canvas': {'blocks': [
        H('Processes · who to hire', 'Three chairs, sized to your hours', 'The roles as chairs. Their triggers as lamps. The helpers sized to your busy hours.', 'Roles', 'Who to hire'),
        {'type': 'seats', 'others': 'Everyone else records and approves a little more. That is a wider job, not a new one.',
         'roles': [{'name': 'Discharge Manager', 'seats': 1, 'cost_low': 4, 'cost_high': 4.5, 'state': 'needed', 'does': 'Owns the whole discharge process. Works with the other departments. A peer of the Bed Manager.', 'rule': 'Any one is enough', 'point': 1,
                    'triggers': [{'label': 'More than 40 discharges a day', 'value': '40 to 45', 'state': 'met', 'source': 'yours', 'above': 40, 'point': 2},
                                 {'label': 'Beds more than 80% full', 'value': '88%', 'state': 'met', 'source': 'yours'},
                                 {'label': 'Discharges often run over time', 'state': 'unknown', 'source': 'needed'}]},
                   {'name': 'Discharge Executives', 'seats': 2, 'cost_low': 3, 'cost_high': 3.5, 'each': True, 'sized': True, 'state': 'needed', 'does': 'Own each discharge from the doctor’s first signal. Catch hold-ups as they happen.', 'point': 3}],
         'sizing': {'flat_label': 'Flat rule', 'busy_label': 'Your busy hours', 'slider_label': 'Discharges a day', 'min': 20, 'max': 60, 'default': 45, 'yours_low': 40, 'yours_high': 45, 'per_person': 15, 'start': 6, 'end': 24,
                    'windows': [{'from': 8, 'to': 11, 'label': 'Morning confirmations', 'clock': '8 to 11 AM'}, {'from': 18, 'to': 21, 'label': 'Evening round intake', 'clock': '6 to 9 PM'}],
                    'flat_text': '{n} a day at 15 each makes {k}. But the work comes in two windows, so most of the day they wait.',
                    'busy_text': 'Your work comes in two windows. One person anchored to each covers the peak. This is your own pattern.',
                    'recheck_text': 'Your busy hours were checked at 40 to 45 a day. At this number, run the check again with your times.',
                    'count_label': 'Discharge Executives', 'total_label': 'New roles, each year', 'point': 4},
         'sheets': [S('dm', 'Needed now', 'Discharge Manager', 'Owns the whole discharge process. Any one trigger is enough, and two of yours are met.', [('Cost', 'About ₹4 to 4.5 lakh a year'), ('Triggers met', 'Two of three, your numbers', 'start')], 'Could someone you have take this role?'),
                    S('de', 'Needed now', 'Discharge Executives', 'One person anchored to each busy window: the morning confirmations and the evening round.', [('Cost', 'About ₹3 to 3.5 lakh each'), ('How many', 'Two, for two windows', 'start')], 'Do your busy times change at weekends?')]}],
        'actions': acts('Next: how this joins the bed desk', 'Who at the bed desk would see this?', 'Tell me about your staff rota', 'Our discharge staff work these shifts: ')}})

# ---------------------------------------------------------------------------------------------- 12 · the bed desk (owners + notes)
SPECS.append({
    'turn': T(12, 'part', 'Who at the bed desk would see this?', 'pr-05 (seats, with what passes between)', 'Processes place, turn 5 (two peers under one head, and what passes between the two desks).', 'Processes · the bed desk'),
    'chat': {'text': ['The bed desk sees it through its own Bed Manager, a peer of the Discharge Manager. Both report to your Head of Operations.',
                      'Whether you need a Bed Manager depends on three numbers we do not have yet. So that chair stays open for now.'],
             'bullets': ['Likely discharges reach the bed desk a day ahead.', 'A 5 PM round confirms tomorrow’s leavers.', 'Each bill is held against the bed, so the empty time can be measured.'],
             'note': 'The bed desk plans from the discharge desk’s times.',
             'points': P('Head of Operations', 'The Bed Manager', 'A day ahead', 'One team doing both'),
             'prompts': ['One team does both', 'Two separate teams', 'Which measures show it worked?'], 'pointer': 'Pick a desk, or something that passes between them, to open it.'},
    'canvas': {'blocks': [
        H('Processes · the bed desk', 'Two desks, one head', 'The Discharge Manager and the Bed Manager as peers, and what passes between them.', 'Roles', 'The two desks'),
        {'type': 'owners', 'label': 'Two desks under the Head of Operations', 'link': 'Peers. Neither reports to the other.', 'line': 'The bed desk can only plan from times the discharge desk sends it.',
         'owners': [{'tag': 'Needed now', 'title': 'Discharge Manager', 'line': 'Owns discharges. Sends likely leavers to the bed desk a day ahead.', 'point': 1},
                    {'tag': 'Open chair', 'title': 'Bed Manager', 'line': 'Owns bed planning. Places each admission in a bed before it is free.', 'point': 2}],
         'sheets': [S('dm', 'Needed now', 'Discharge Manager', 'More than 40 discharges a day already calls for this role. Your number is 40 to 45.', [('Cost', 'About ₹4 to 4.5 lakh a year'), ('Reports to', 'The Head of Operations')], 'Who would the two managers report to?'),
                    S('bm', 'Needs your numbers', 'Bed Manager', 'Needed if any one of three is true. More admissions than free beds the night before. Beds over 80% full. Or more than half of admissions late.',
                      [('Cost', 'About ₹4 to 4.5 lakh a year'), ('Still needed', 'Three of your bed numbers', 'target')], 'How many admissions come in late?')]},
        {'type': 'notes', 'label': 'What passes between the two desks',
         'items': [{'tag': 'New', 'title': 'Likely leavers, a day ahead', 'text': 'Ward patients flagged 24 hours ahead, intensive care by 1 PM.', 'state': 'start', 'point': 3},
                   {'tag': 'New', 'title': 'A 5 PM round', 'text': 'Senior doctors check tomorrow’s leavers. The plan is fixed at 6 PM.'},
                   {'tag': 'Agreed', 'title': 'Bed ready, once clean', 'text': 'The bed desk sees it at once, with no phone call.'},
                   {'tag': 'Answer', 'title': 'One team, or two?', 'text': 'If one team does both, they must run side by side.', 'state': 'target', 'point': 4}],
         'sheets': [S('n1', 'New', 'Likely leavers, a day ahead', 'The bed desk maps tomorrow’s beds from this list. Without it, the plan is built on the day.', [('Sent by', 'The Discharge Manager')]),
                    S('n2', 'New', 'A 5 PM round', 'The senior doctors check tomorrow’s likely leavers by 5 PM. The bed desk then fixes its plan at 6 PM.', [('Fixed at', '6 PM')]),
                    S('n3', 'Agreed', 'Bed ready, once clean', 'Housekeeping marks the bed clean. The bed desk sees it at once.', [('Today', 'A phone call, when someone remembers')]),
                    S('n4', 'Needs your answer', 'One team, or two?', 'If one team runs discharges and admissions, the two must run side by side, not one after the other.', [('We need', 'Your answer', 'target')], 'Is it one team, or two?')]}],
        'actions': acts('Next: the measures that show it worked', 'Which measures show it worked?', 'Tell me about your bed desk', 'Our bed desk works like this: ')}})

# ---------------------------------------------------------------------------------------------- 13 · the measures (readouts)
RD = [('Hours from ready to home', '5 hours 15 min', 'confirmed', 'yours', 'trial', 1, 'From the doctor’s go-ahead to the patient leaving the ward.', 'Ward nurse', 'Set on day 3'),
      ('Patients home by 10 AM', None, 'new', 'new', 'trial', 2, 'Share of patients without insurance home by 10 AM. Insured patients by 1 PM.', 'Ward nurse', 'Set on day 3'),
      ('Decided on the evening round', None, 'new', 'new', 'trial', None, 'Share of discharges first marked on the evening round, not the same morning.', 'The one-tap form', 'Set on day 3'),
      ('Bed empty after leaving', '75 min', 'confirmed', 'yours', 'trial', 3, 'From the patient leaving to the bed ready for the next one.', 'Housekeeping', 'Under 30 minutes'),
      ('Time to finish the bill', '90 min', 'confirmed', 'yours', 'trial', None, 'From the doctor’s signature to the final bill.', 'Billing', 'Set on day 3'),
      ('Insurance approval time', 'About 1 hour', 'confirmed', 'yours', 'trial', None, 'From the request to the insurer’s yes, evening and morning apart.', 'Insurance desk', 'Set on day 3'),
      ('Family told before leaving', None, 'new', 'new', 'trial', 4, 'Share of patients whose family got diet, medicine and follow-up advice before leaving.', 'Ward nurse', 'Every patient'),
      ('Money won back', None, 'new', 'new', 'later', None, 'Revenue from freed bed days, against the most it could be.', 'Billing', 'Set after the trial'),
      ('Discharges a day', '40 to 45', 'confirmed', 'yours', 'later', None, 'Checked each month against the line for the Discharge Manager.', 'Discharge Manager', 'Watch, no goal')]
SPECS.append({
    'turn': T(13, 'part', 'Which measures show it worked?', 'pr-06 (readouts)', 'Processes place, turn 6 (nine measures, not all sixteen; new ones get no number until the trial records one).', 'Processes · the measures'),
    'chat': {'text': ['Nine measures, not all sixteen. Five already have your starting number.', 'The other four are new. They get no number until the trial records one, so none is made up.'],
             'invite': 'Next, we can see what happens after the two weeks.',
             'note': 'Measure what you already know first.',
             'points': P('Hours from ready to home', 'Patients home by 10 AM', 'The empty bed', 'Family told before leaving'),
             'prompts': ['What happens after the two weeks?', 'Who records the times?', 'Can we add a measure?'], 'pointer': 'Pick a window to see how it is measured. Flip to after the trial.'},
    'canvas': {'blocks': [
        H('Processes · the measures', 'Nine windows on the board', 'Five show your starting number. Four are new, and stay dashed until the trial reads them.', 'Measures', 'Nine windows'),
        {'type': 'readouts', 'condition': 'Goals are set on day 3 of the trial, from the ward’s own times.',
         'measures': [dict({'name': n, 'state': st, 'source': so, 'when': w}, **({'value': v} if v else {}), **({'point': p} if p else {})) for n, v, st, so, w, p, h, who, g in RD],
         'sheets': [S('r%d' % (i + 1), ('Read in the trial' if w == 'trial' else 'Read after the trial'), n, h, [('Who records it', who), ('Goal', g, 'target')], 'Who records this today, if anyone?') for i, (n, v, st, so, w, p, h, who, g) in enumerate(RD)]}],
        'actions': acts('Next: what happens after the two weeks', 'What happens after the two weeks?', 'Tell me a measure to add', 'One measure I would add is: ')}})

# ---------------------------------------------------------------------------------------------- 14 · after the trial (loop)
LOOP = [('Plan', 'You and Tojo', 1, 'Pick the ward. Name who records the times. Your Head of Operations says yes to the new order.'),
        ('Try on one ward', 'The trial ward', 2, 'Run the fourteen days. Three quiet days, then the changes in two steps.'),
        ('Measure', 'You, the ward and Tojo', 3, 'Read the nine windows. Compare the trial days with days 1 to 3.'),
        ('Adjust', 'Discharge Manager', None, 'Fix what did not work. Then run one more week on the same ward.'),
        ('Spread to more wards', 'Discharge Manager and IT', 4, 'Add one or two wards at a time. Link the hospital software once two wards run well.')]
SPECS.append({
    'turn': T(14, 'recommendation', 'What happens after the two weeks?', 'pr-07 (loop)', 'Processes place, turn 7 (read the numbers and choose: spread, or adjust and try again).', 'Processes · after the trial'),
    'chat': {'text': ['After two weeks we read the numbers and choose. If hours from ready to home fell, we spread it. If not, we adjust and try again.', 'Each new ward starts from the plan step. The software link comes in once two wards run well.'],
             'note': 'Spread only what worked.',
             'points': P('Plan', 'Try on one ward', 'Measure', 'Spread'),
             'prompts': ['Let’s pick the trial ward', 'What does spreading cost?', 'Where do the automations stand now?'], 'pointer': 'Step round the loop. At the check, the answer sends you on or back.'},
    'canvas': {'blocks': [
        H('Processes · after the trial', 'Spread only what worked', 'One ward at a time, round the same loop. The check after measuring decides where you go next.', 'The trial', 'After two weeks'),
        {'type': 'loop', 'at': 0, 'sub': 'One ward at a time',
         'steps': [dict({'name': n, 'who': w}, **({'point': p} if p else {})) for n, w, p, x in LOOP],
         'gate': {'at': 2, 'question': 'Did hours from ready to home fall?', 'yes': 'Yes, it fell', 'no': 'Not yet', 'yes_to': 4, 'no_to': 3, 'retry_to': 1},
         'sheets': [S('s%d' % (i + 1), 'Step %d of 5' % (i + 1), n, x, [('Who', w)], 'What would you need for this step?' if i in (0, 4) else None) for i, (n, w, p, x) in enumerate(LOOP)]}],
        'actions': acts('Next: pick the trial ward', 'Let’s pick the trial ward', 'Tell me what spreading needs', 'To spread this, we would need: ')}})

NOTES = {'dp-pr-01': 'Was turn-06 (sample conversation). Each job on one clock from the evening round, today and with the changes.',
         'dp-pr-02': 'Was turn-07. The six teams as rooms, the one approver and the two peers under them.',
         'dp-pr-03': 'Was turn-08. The roles, and the two ways to size the helpers: the usual rule and your busy hours.',
         'dp-pr-04': 'Was turn-09. The measures as six dials; the new ones dashed.',
         'dp-pr-05': 'Was turn-10. The plan as four switches to the bulb. The night-board background starts here.',
         'dp-pr-06': 'Was turn-11. The blank day: type each time straight into the drawing. The trial week by week.',
         'dp-pr-07': 'Was turn-12. The same day filled with the real times and the gaps (a redraw), and what they changed.',
         'dp-pr-08': 'Was pr-01. The two weeks: play the day strip, pick a part, type the ward.',
         'dp-pr-09': 'Was pr-02. Nine name badges, grouped by what each person does. The ward-board background is back.',
         'dp-pr-10': 'Was pr-03. Seven magnets moved from today to with the changes.',
         'dp-pr-11': 'Was pr-04. The chairs, their triggers and the busy-hours slider.',
         'dp-pr-12': 'Was pr-05. Two peers under one head, and what passes between the desks.',
         'dp-pr-13': 'Was pr-06. Nine instrument windows. The night-board background is back.',
         'dp-pr-14': 'Was pr-07. The loop after the trial, with the yes-or-no check.'}
man = {'place': 'Processes', 'tool': 'Discharge Process', 'turns': []}
for s in SPECS:
    s['review'] = {'status': 'approved', 'date': '2026-10-06', 'note': 'Approved 6 Oct with the regenerated Discharge turns.'}
    fn = s['turn']['id'] + '.json'
    json.dump(s, open(os.path.join(HERE, fn), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    man['turns'].append({'file': fn, 'note': NOTES[s['turn']['id']]})
json.dump(man, open(os.path.join(HERE, 'turns.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('wrote', len(SPECS), 'specs and turns.json')
