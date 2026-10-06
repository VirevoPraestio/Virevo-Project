"""Bed Management Diagnosis, turns bm-dg-02 to bm-dg-12 (Avishek, 30 Sep 2026: all the turns up to the point where the
conversation starts on one solution; naming the five parts stays in Diagnosis, the first part itself opens Solutions).

  bm-dg-02  transcript 8   the five areas, and the first question        lens
  bm-dg-03  transcript 9   one team: which of two days?                  day-strips
  bm-dg-04  transcript 10  admission time, five steps left blank         admission-route (blank; times typed in)
  bm-dg-05  transcript 11  the same five steps, your times               admission-route (redraw) + stopwatch
  bm-dg-06  transcript 12  when billing stops and starts again (blank)   bed-bills (blank; times typed in)
  bm-dg-07  transcript 13  your two times, and the gap                   bed-bills (redraw) + was-now + effect
  bm-dg-08  transcript 14  five figures that turn hours into money       receipt (figures typed on the bill)
  bm-dg-09  transcript 15  dead bed time, turned into money              bed-count + effect
  bm-dg-10  transcript 16  everything you told me, in one place          evidence-board
  bm-dg-11  playbook §2    the diagnosis: one rule and its loop          rule-loop
  bm-dg-12  transcript 17  the five parts, named                         scale + corridor + two effects
Every turn has its own drawing (rules/08 §2), redrawn 30 Sep 2026 after the box-heavy set was rejected.

Tojo's wording is the transcript's, in the plain English the rules require; the transcript's own words are kept in
turn.transcript.said. Run once; afterwards edit the JSON files.
"""
import dg_actions, copy, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = {'tool': 'Bed Management', 'tab': 'Diagnosis', 'register': 'guided'}

def turn(id_, type_, user, label, said, **kw):
    t = dict(BASE, id=id_, type=type_, user_message=user, transcript={'label': label, 'said': said}); t.update(kw); return t

SPECS = []

# ------------------------------------------------------------------------------------------ bm-dg-02 · Turn 8
AREAS = [
 ('who', 'Who runs what', 'Does one team handle both discharges and admissions, or are there two teams?', 'Asking now', 'start'),
 ('tat', 'How long an admission takes', 'The five steps of an admission, and a typical day’s clock time for each.', 'Later', 'plain'),
 ('map', 'Tomorrow’s bed picture', 'Is there a set way to match tomorrow’s planned admissions against the beds you expect to free up?', 'Later', 'plain'),
 ('bill', 'When billing stops and starts again', 'When the leaving patient’s final bill closes, and when the next patient’s first charge appears.', 'Later', 'plain'),
 ('turn', 'Who gets the bed ready again', 'Has anyone worked out how many beds housekeeping and transport can ready in the busiest hours?', 'Later', 'plain')]
SPECS.append({
 'turn': turn('bm-dg-02', 'question', 'Yes, that’s our day. Ours is sometimes even longer. What happens next?', 'Transcript turn 8 · the questions, and the first one',
   'That’s worth holding on to — and most hospitals can’t say how much longer, because nobody measures that stretch end to end. Now I need to pin down how your hospital actually runs it. The graphic has the whole list so you can see where this is going; I’ll take them one at a time rather than dump them on you. First one: does the same team handle both your discharges and your admissions, or are those two separate teams?',
   note_for_review='The user’s line is paraphrased in the transcript.'),
 'chat': {
  'text': ['That’s worth holding on to. Most hospitals can’t say how much longer, because nobody measures that stretch end to end.',
           'Now I need to pin down how your hospital runs it. The five areas are under the glass, so you can see where this is going. I’ll take them one at a time.',
           'First one: does the same team handle both your discharges and your admissions, or are those two separate teams?'],
  'note': 'Five areas. One question at a time.',
  'question': {'text': 'Pick the closest', 'options': ['One team does both', 'Two separate teams', 'It varies by ward. I’d need to check']},
  'points': [{'n': i + 1, 'label': a[1], 'canvas': True} for i, a in enumerate(AREAS)],
  'prompts': ['One team does both', 'Why does that matter?', 'Can I answer some of these later?']},
 'canvas': {'blocks': [
  {'type': 'heading', 'eyebrow': 'What I need to know', 'title': 'Five areas, one question at a time',
   'deck': 'This is where the questions are going, so nothing comes as a surprise. They are separate areas, not steps in a row.'},
  {'type': 'lens', 'centre': {'kicker': 'Under the glass', 'title': 'Five areas', 'sub': 'One question at a time'},
   'hint': 'Tap an area to see the question I’ll ask there.',
   'areas': [{'name': n, 'status': tg, 'state': 'now' if i == 0 else 'later', 'point': i + 1} for i, (k, n, q, tg, stt) in enumerate(AREAS)],
   'caption': 'Separate areas, not steps in a row. The order between them does not matter.',
   'sheets': [{'key': k, 'when': 'Area %d · %s' % (i + 1, tg), 'title': n, 'text': q,
               'lines': [{'label': 'When', 'value': 'I’m asking this one now.' if i == 0 else 'After the one before it is answered.', 'state': 'start' if i == 0 else 'plain'}]}
              for i, (k, n, q, tg, stt) in enumerate(AREAS)]}]}})

# ------------------------------------------------------------------------------------------ bm-dg-03 · Turn 9
ROWS = [('Morning', 'Discharges first, through the morning', 'Discharges and admissions worked together',
         'In A the team spends the morning on discharges. In B it is already lining up the day’s admissions.'),
        ('Midday', 'The team switches to admissions', 'Patients already called in for beds due to free',
         'In A the switch comes at midday. In B patients are called in for beds that will be free soon.'),
        ('Afternoon and evening', 'Admissions land late in the day', 'Admissions land across the day',
         'In A admissions pile up late. In B they are spread across the day.')]
SPECS.append({
 'turn': turn('bm-dg-03', 'question', 'one team does both', 'Transcript turn 9 · the follow-up to “one team”',
   'One team — that’s the more common of the two answers. So the follow-up matters: which of the two patterns in the graphic is closer to how that team’s day actually runs?'),
 'chat': {
  'text': ['One team. That’s the more common of the two answers.',
           'So the follow-up matters. Which of the two patterns is closer to how that team’s day really runs?'],
  'note': 'The same team can run two very different days.',
  'question': {'text': 'Which is closer?', 'options': ['Pattern A: one after the other', 'Pattern B: both at once', 'Somewhere between the two']},
  'prompts': ['Pattern B, both at once', 'It changes from day to day', 'Why does the order matter?']},
 'canvas': {'blocks': [
  {'type': 'heading', 'eyebrow': 'One team, two ways to run the day', 'title': 'Which day is closer to yours?',
   'deck': 'The same three moments of the day, run two ways. Read across each row.'},
  {'type': 'day-strips', 'slots': ['8 AM', '10 AM', 'Noon', '2 PM', '4 PM', '6 PM'], 'hint': 'Tap a pattern to read it, moment by moment.',
   'patterns': [{'name': 'Pattern A', 'tag': 'One after the other', 'cells': ['out', 'out', 'none', 'in', 'in', 'in']},
                {'name': 'Pattern B', 'tag': 'Both at once', 'cells': ['both', 'both', 'in', 'both', 'in', 'none']}],
   'caption': 'Two neutral patterns, so you can place your own day. Neither one is the answer I expect.',
   'sheets': [{'key': 'a', 'when': 'Pattern A', 'title': 'Discharges first, admissions later',
               'text': 'The team finishes one job before it starts the other. New patients wait for the switch.',
               'lines': [{'label': ROWS[i][0], 'value': ROWS[i][1]} for i in range(3)]},
              {'key': 'b', 'when': 'Pattern B', 'title': 'Both jobs side by side',
               'text': 'The team works both jobs together. New patients are called in before their bed is free.',
               'lines': [{'label': ROWS[i][0], 'value': ROWS[i][2]} for i in range(3)]}]}]}})

# ------------------------------------------------------------------------------------------ bm-dg-04 · Turn 10 (blank)
STAGES = [('arr', 'Patient arrives, or Emergency says admit', 'The clock starts when the patient arrives, or when Emergency decides to admit.'),
          ('doc', 'Paperwork done', 'Registration and admission papers are complete.'),
          ('bed', 'Bed given in the system', 'A bed is put against the patient’s name in your hospital software.'),
          ('rdy', 'Ward or ICU confirms bed ready', 'The ward or ICU says the bed is clean and ready to take the patient.'),
          ('in', 'Patient in the bed', 'The patient is physically in the bed. The clock stops here.')]
SHORT = ['Patient arrives', 'Paperwork done', 'Bed given', 'Bed confirmed ready', 'Patient in the bed']
SPECS.append({
 'turn': turn('bm-dg-04', 'data-ask', 'pattern b', 'Transcript turn 10 · admission time, as a blank chain',
   'Pattern B is the better of the two, and less common than you’d think. Which makes the next one worth getting precise, because it’s what shows the pattern is actually landing: every admission runs through five steps, and the gap between the first and the last is your Admission TAT. The graphic has that chain with the times left blank. Fill in a typical day’s clock times and we’ll see exactly where the time goes.'),
 'chat': {
  'text': ['Pattern B is the better of the two, and less common than you’d think.',
           'That makes the next one worth getting exact. It shows whether the pattern is really landing.',
           'Every admission runs through five steps. The gap between the first and the last is your admission time. Type a typical day’s clock times onto each stop. Then we’ll see where the time goes.'],
  'note': 'Clock times settle it.',
  'prompts': ['Arrival about 1 PM, in the bed by 4:30 PM', 'Our times change a lot from day to day', 'Do the times need to be exact?']},
 'canvas': {'blocks': [
  {'type': 'heading', 'eyebrow': 'How long an admission takes', 'title': 'Five steps, times left blank',
   'deck': 'A typical day’s clock times are enough. They do not have to be exact.'},
  {'type': 'admission-route', 'mode': 'blank', 'start_label': 'Arrival', 'end_label': 'In the bed', 'hint': 'Tap a step and type its time. Each one you add goes into your message.',
   'stops': [dict({'name': n, 'point': i + 1}, **({'outcome': True} if i == 4 else {})) for i, (k, n, w) in enumerate(STAGES)],
   'caption': 'The gap between the first step and the last is your admission time.',
   'sheets': [{'key': k, 'when': 'Step %d of 5' % (i + 1), 'title': n, 'text': w, 'entry': 'Your typical clock time for this step',
               'entry_hint': 'For example: around 2 PM, sometimes 3', 'entry_open': True, 'entry_label': 'Step %d, %s' % (i + 1, SHORT[i].lower())}
              for i, (k, n, w) in enumerate(STAGES)]}]}})

# ------------------------------------------------------------------------------------------ bm-dg-05 · Turn 11 (filled, redraw)
GAPS = ['1 hour', '1 hour', '1 hour', '30 minutes']
TIMES = [('1 PM', None), ('2 PM', '3 to 4 PM'), ('3 PM', 'Sometimes 4 PM, worst 4 to 5 PM'), ('4 PM', '5 to 6 PM'), ('4:30 PM', '6:30 PM, up to 7 to 8 PM')]
SPECS.append({
 'turn': turn('bm-dg-05', 'data-back',
   'Arrival around 1 PM. Documentation by 2 PM, worst 3–4 PM. Bed allocated by 3 PM, sometimes 4, worst 4–5 PM. Ward or ICU confirms ready by 4 PM, worst 5–6 PM. In the bed by 4:30 PM, worst 6:30 PM. This is the ideal situation, sometimes this can stretch to 7–8 PM. Generally we allocate only after we get confirmation that bed is ready or about to get readied.',
   'Transcript turn 11 · the filled chain, and the gap named',
   'Your own times are worth more than anything else we’ve covered — and they point somewhere slightly different from what you told me a moment ago. You said admissions and discharges run together through the day. The times you have just given put the patient arriving in the early afternoon and physically in the bed late afternoon to evening, which is an afternoon pattern rather than a spread one. I would take the numbers as the better guide — and two likely reasons for the gap: you allocate a bed only once it is confirmed ready, so there is nothing to call a patient in against until late in the day; and where one team carries both jobs, whichever job has a deadline in front of it takes the morning. Your times are in the chain below. Next: is there an actual mechanism that maps tomorrow’s planned admissions against the beds you expect to free up — or does the bed picture come together as the day goes?',
   redraw_of='bm-dg-04'),
 'chat': {
  'text': ['Your own times are worth more than anything else we’ve covered. They point somewhere slightly different from what you told me.',
           'You said admissions and discharges run together through the day. Your times put arrival in the early afternoon, and the bed late afternoon to evening. That is an afternoon pattern, not a spread one.',
           'I’d take the numbers as the better guide. There are two likely reasons. You give a bed only once it is confirmed ready, so nobody can be called in until late. And where one team carries both jobs, the job with a deadline takes the morning.'],
  'pointer': 'Your times are on the way from the door to the bed.',
  'invite': 'Next: is there a set way to match tomorrow’s planned admissions against the beds you expect to free up?',
  'note': 'Your numbers tell a different story from the claim.',
  'question': {'text': 'Pick the closest', 'options': ['Yes, a set way, done every day', 'It happens, but informally', 'No, the picture comes together as the day goes']},
  'prompts': ['It happens, but informally', 'We do call some patients in early', 'Why would the morning go to discharges?']},
 'canvas': {'tone': 'count', 'blocks': [
  {'type': 'heading', 'eyebrow': 'Admission time, from your own clock', 'title': 'Five steps, your times',
   'deck': 'A typical day at each stop, and the wait between stops. Tap a stop for its worst day.'},
  {'type': 'admission-route', 'mode': 'filled', 'start_label': 'Arrival', 'end_label': 'In the bed', 'hint': 'Tap a step to see its worst day.',
   'stops': [dict({'name': n, 'typical': TIMES[i][0], 'point': i + 1}, **({'gap': GAPS[i]} if i < 4 else {}), **({'outcome': True} if i == 4 else {})) for i, (k, n, w) in enumerate(STAGES)],
   'caption': 'About an hour of this is paperwork. The rest is waiting on the next step.',
   'sheets': [dict({'key': k, 'when': 'Step %d of 5' % (i + 1), 'title': n, 'text': w,
                    'lines': [{'label': 'Typical day', 'value': TIMES[i][0], 'state': 'start'}] + ([{'label': 'Worst day', 'value': TIMES[i][1], 'state': 'outcome' if i == 4 else 'target'}] if TIMES[i][1] else [])})
              for i, (k, n, w) in enumerate(STAGES)]},
  {'type': 'stopwatch', 'label': 'Where the 3½ hours go', 'value': '3½ hours', 'value_sub': 'on a good day', 'dial_hours': 4,
   'parts': [{'label': 'Paperwork', 'hours': 1, 'kind': 'work', 'text': 'From arrival at 1 PM to paperwork done by 2 PM.'},
             {'label': 'Waiting on the next step', 'hours': 2.5, 'kind': 'wait', 'text': 'For a bed to be given, then confirmed ready, then the move.'}],
   'worst': '5½ hours at worst, and up to 7 on the days it stretches to 8 PM.'}]}})

# ------------------------------------------------------------------------------------------ bm-dg-06 · Turn 12 (blank)
BILLS = [('out', 'Final bill closed', 'Patient going home', 'The leaving patient’s final bill is closed. From here nothing more is charged to this bed.', 'Final bill closed'),
         ('in', 'First charge for the next patient', 'Next patient, same bed', 'The first charge of any kind appears against the next patient in that same bed.', 'First charge for the next patient')]
SPECS.append({
 'turn': turn('bm-dg-06', 'data-ask', 'it happens but informally', 'Transcript turn 12 · when billing stops and starts again',
   'Informally is the most common of the three answers. Next one, and it is the one that puts a number on what all of this costs: what time does the outgoing patient’s final bill actually get closed, and what time does the first billable entry appear against the next patient in that same bed? Both are blank in the graphic below — same idea as the last one.'),
 'chat': {
  'text': ['Informally is the most common of the three answers.',
           'The next one puts a number on what all this costs. What time does the leaving patient’s final bill close? And when does the first charge appear against the next patient in that same bed?',
           'Both are blank on the two bill tags. Same idea as the last one: type them in.'],
  'note': 'Two times from your billing desk.',
  'prompts': ['The bill closes about 12 to 1 PM', 'I’d have to ask our billing team', 'Why the bill, and not the empty bed?']},
 'canvas': {'blocks': [
  {'type': 'heading', 'eyebrow': 'When billing stops and starts again', 'title': 'Two times on one bed',
   'deck': 'The leaving patient’s last bill, and the next patient’s first charge, on the same bed.'},
  {'type': 'bed-bills', 'mode': 'blank', 'gap_label': 'Nothing bills in between', 'hint': 'Tap a tag and type its time. Both go into your message.',
   'tags': [{'who': w, 'label': l} for (k, l, w, t, el) in BILLS],
   'caption': 'Everything between these two times bills nothing. That gap is the dead bed time.',
   'sheets': [{'key': k, 'when': w, 'title': l, 'text': t + ' Both times almost surely sit in your billing system already.',
               'entry': 'Your typical time for this', 'entry_hint': 'For example: 12 to 1 PM', 'entry_open': True, 'entry_label': el}
              for (k, l, w, t, el) in BILLS]}]},
})

# ------------------------------------------------------------------------------------------ bm-dg-07 · Turn 13 (filled, redraw)
SPECS.append({
 'turn': turn('bm-dg-07', 'data-back', 'Final bill closed typically 12–1 PM. First billable entry for the next patient: we try for 5 pm but could go up to 7–8 pm.',
   'Transcript turn 13 · dead bed time, worked out',
   'That is the number this whole conversation has been circling, and it is now yours rather than borrowed from anyone else. Both times are in the graphic, with the gap between them worked out. Last area, and it is a different kind of question: has anyone at the hospital ever actually calculated how many bed turnovers your housekeeping and transport staff can handle in the peak hours — or is that staffing assumed adequate because it has not caused a visible crisis?',
   redraw_of='bm-dg-06'),
 'chat': {
  'text': ['That is the number this whole conversation has been circling. It is now yours, not borrowed from anyone else.',
           'Both times are on the two bill tags, with the gap between them worked out.',
           'Last area, and a different kind of question. How many beds can your housekeeping and transport staff get ready in the busiest hours?'],
  'invite': 'Has anyone worked that out? Or is the staffing taken to be enough, because nothing has gone badly wrong?',
  'note': 'Four to five hours, every time a bed changes patient.',
  'question': {'text': 'Pick the closest', 'options': ['Yes, we have worked it out', 'No, it is taken to be enough', 'Not sure. I would need to check']},
  'prompts': ['Not sure, I’d need to check', 'Is 4 to 5 hours a lot?', 'That matches what our billing shows']},
 'canvas': {'blocks': [
  {'type': 'heading', 'eyebrow': 'When billing stops and starts again', 'title': 'Your two times, and the gap',
   'deck': 'Worked out from your own two times. One bed, one change of patient.'},
  {'type': 'bed-bills', 'mode': 'filled', 'gap_label': '4 to 5 hours unbilled', 'hint': 'Tap a tag to see it in full.',
   'tags': [{'who': 'Patient going home', 'label': 'Final bill closed', 'value': '12 to 1 PM'},
            {'who': 'Next patient, same bed', 'label': 'First charge for the next patient', 'value': '5 PM, the goal', 'worst': 'Worst 7 to 8 PM', 'outcome': True}],
   'sheets': [{'key': 'out', 'when': 'Patient going home', 'title': 'Final bill closed', 'text': BILLS[0][3], 'lines': [{'label': 'Your time', 'value': '12 to 1 PM', 'state': 'start'}]},
              {'key': 'in', 'when': 'Next patient, same bed', 'title': 'First charge for the next patient', 'text': BILLS[1][3],
               'lines': [{'label': 'Your goal', 'value': '5 PM'}, {'label': 'On the worst days', 'value': '7 to 8 PM', 'state': 'outcome'}]}]},
  {'type': 'was-now', 'rows': [{'label': 'Dead bed time on one bed', 'was': 'Half a day', 'now': '4 to 5 hours', 'change': 'Up to 8 hours',
                                 'direction': 'same', 'knock_on': 'The hospital like yours, set against your own two times.'}],
   'caption': 'Your number replaces the example from the hospital like yours.'},
  {'type': 'effect', 'label': 'Dead bed time', 'value': 'About 4 to 5 hours, every change of patient', 'state': 'outcome',
   'sub': 'Up to 8 hours on the days it stretches. Simple arithmetic on your own two times.'}]}})

# ------------------------------------------------------------------------------------------ bm-dg-08 · Turn 14
FIG = [('arpob', 'What one occupied bed earns', 'a day, in rupees', 'Turns each lost hour of bed time into rupees.', 'For example: ₹8,000 a day'),
       ('stay', 'Average stay in days', 'across the hospital', 'Tells us how often each bed changes patient.', 'For example: 6.5 days'),
       ('rev', 'Average daily revenue', 'for the whole hospital', 'Lets us check the bed figure against the whole hospital.', 'For example: ₹28 lakh a day'),
       ('occ', 'Beds full, ICU separately', 'as a share of beds', 'Tells us how many beds change patient each day, and where the pressure sits.', 'For example: 89%, ICU 94%'),
       ('ot', 'Operating theatre use and revenue', 'use, and rupees a day', 'Shows whether a late bed can cost you an operation.', 'For example: 75%, ₹5 lakh a day')]
SPECS.append({
 'turn': turn('bm-dg-08', 'data-ask', 'not sure', 'Transcript turn 14 · the money figures',
   '“Not sure” is itself the answer — if nobody has run it, nobody knows whether the people doing the physical turnaround can keep up at peak. I’ll come back to that. We now have hours. Hours on their own don’t move anyone, so before we go further I need the figures that turn them into money — they’re listed in the graphic. Once those are in, there’s one more staffing question, on the admissions desk itself.'),
 'chat': {
  'text': ['“Not sure” is itself the answer. If nobody has worked it out, nobody knows whether the people who ready beds keep up at peak. I’ll come back to that.',
           'We now have hours. Hours on their own don’t move anyone. Before we go further, I need the figures that turn them into money.',
           'Once those are in, there’s one more staffing question, on the admissions desk itself.'],
  'pointer': 'Type the five figures straight onto the bill. Each one goes into your message.',
  'note': 'Five figures turn hours into money.',
  'points': [{'n': i + 1, 'label': f[1], 'canvas': True} for i, f in enumerate(FIG)],
  'prompts': ['I’ll send all five now', 'I only have some of these', 'Why the ICU on its own?']},
 'canvas': {'blocks': [
  {'type': 'heading', 'eyebrow': 'Turning hours into money', 'title': 'Five figures I need from you',
   'deck': 'Each one turns something we already have into rupees.'},
  {'type': 'receipt', 'title': 'Figures for Tojo', 'subtitle': 'Your hospital · turning hours into rupees', 'hint': 'Type each figure on its line. Tap a line to see what it turns into.',
   'lines': [{'label': n, 'unit': u, 'placeholder': 'Type it here', 'point': i + 1} for i, (k, n, u, t, h) in enumerate(FIG)],
   'total_label': 'Dead bed time in rupees', 'waiting': 'Waiting on your figures', 'done': 'All five in. Send to Tojo.',
   'caption': 'Nothing here is my guess. Every figure comes from you.',
   'sheets': [{'key': k, 'when': 'Figure %d of 5' % (i + 1), 'title': n, 'text': t} for i, (k, n, u, t, h) in enumerate(FIG)]}]}})

# ------------------------------------------------------------------------------------------ bm-dg-09 · Turn 15
SPECS.append({
 'turn': turn('bm-dg-09', 'sizing', 'ARPOB ₹8,000/day. ALOS 6.5 days. Average daily revenue ₹28 lakhs. Bed occupancy 89%, ICU 94%. OT utilisation 75%, daily OT revenue ₹5 lakhs.',
   'Transcript turn 15 · dead bed time turned into money',
   'That’s everything I needed. The graphic below turns your dead bed time into a revenue number, step by step, so you can check every line of the arithmetic rather than take it from me. Two things I’ve deliberately left out of it: an ALOS gain on top, because that would be the same bed-days counted twice; and OT, which needs more from you before it can be sized honestly. Last question before we move on: has anyone worked out what your admissions desk can actually handle per hour at peak — counting internal bed transfers alongside admissions — or is that team sized by habit?',
   user_words=['ARPOB', 'ALOS', 'OT']),
 'chat': {
  'text': ['That’s everything I needed.',
           'The working turns your dead bed time into a revenue number, one line at a time. You can check every line rather than take it from me.',
           'Two things I’ve left out on purpose. A shorter stay on top, because that would count the same days twice. And the operating theatre, which needs more from you first.'],
  'invite': 'Last one before we move on. Has anyone worked out what your admissions desk can handle an hour at peak, bed transfers included?',
  'note': '₹1.5 to 2 crore a year, from your own figures.',
  'question': {'text': 'Pick the closest', 'options': ['Yes, we have worked it out', 'No, sized by habit and taken to be enough', 'Not sure. I would need to check']},
  'points': [{'n': 1, 'label': 'Hours won back each time', 'canvas': False}, {'n': 2, 'label': 'Revenue at stake a year', 'canvas': True}],
  'prompts': ['No, sized by habit', 'How sure is the ₹1.5 crore?', 'Why leave the operating theatre out?']},
 'canvas': {'blocks': [
  {'type': 'heading', 'eyebrow': 'Dead bed time, turned into money', 'title': 'From one bed to a year',
   'deck': 'Every figure is yours. Move the hours won back between 3 and 4 to see the range.'},
  {'type': 'bed-count', 'occupied': 267, 'occupied_label': 'beds occupied, 300 at 89%', 'stay': 6.5, 'per_day_label': 'beds change patient every day',
   'rate': 8000, 'beds_caption': 'Each bed sits 4 to 5 hours with no bill when it changes patient. The red line is that time.',
   'hours': {'label': 'Hours won back each time', 'min': 3, 'max': 4, 'step': 0.5, 'value': 3.5},
   'hint': 'Move the slider. Tap a figure to see the working.',
   'readouts': [{'label': 'Bed hours won back a year', 'calc': 'hy', 'note': '41 beds, the hours, 365 days'},
                {'label': 'Full days of bed time', 'calc': 'd', 'note': 'those hours, divided by 24'},
                {'label': 'Revenue at stake a year', 'calc': 'v', 'note': 'at ₹8,000 a bed day', 'state': 'outcome', 'point': 2}],
   'caption': 'It holds only if freed hours are filled, and at 89% full they can. It uses the bed charge alone, so it understates.',
   'sheets': [{'key': 'hy', 'when': 'The working · 1', 'title': 'Bed hours won back', 'text': '267 beds ÷ 6.5 days is about 41 changes a day. Each one wins back 3 to 4 hours, over 365 days.',
               'lines': [{'label': 'From', 'value': 'Your beds, stay and dead bed time'}]},
              {'key': 'd', 'when': 'The working · 2', 'title': 'Full days of bed time', 'text': 'The hours won back, divided by 24. About 1,900 to 2,500 bed days a year.',
               'lines': [{'label': 'From', 'value': 'The line before'}]},
              {'key': 'v', 'when': 'The working · 3', 'title': 'Revenue at stake', 'text': 'Those bed days at ₹8,000 each. Your ₹28 lakh a day suggests the ₹8,000 is the bed charge alone, so this is on the low side.',
               'lines': [{'label': 'Range', 'value': '₹1.5 to 2 crore a year', 'state': 'outcome'}]}]},
  {'type': 'effect', 'label': 'A shorter average stay', 'value': 'Counted once, inside this',
   'sub': 'A shorter stay frees the same days of bed time. Adding it on top would count them twice.'}]}})

# ------------------------------------------------------------------------------------------ bm-dg-10 · Turn 16
EVID = [('One team does both jobs', '“one team does both”', 'who runs what',
         'Discharges and admissions sit with the same team. You placed it nearer both at once, and your times said afternoon.'),
        ('Admission time about 3½ hours', '“1 PM, in the bed 4:30”', 'your five times',
         'About 3½ hours on a good day, 5½ at worst. About an hour of it is paperwork. The rest is waiting.'),
        ('No set way to match beds', '“it happens, but informally”', 'tomorrow’s beds',
         'Nothing matches tomorrow’s admissions against the beds due to free. The picture comes together as the day goes.'),
        ('Dead bed time 4 to 5 hours', '“12 to 1, then 5 PM”', 'your billing times',
         'On every change of patient, up to 8 hours on bad days. About ₹1.5 to 2 crore a year.'),
        ('No team ever sized', '“not sure”, “sized by habit”', 'who readies beds',
         'Nobody has worked out whether housekeeping, transport or the admissions desk keep up at the busiest times.')]
SPECS.append({
 'turn': turn('bm-dg-10', 'findings', 'No — sized by habit, assumed adequate', 'Transcript turn 16 · everything you told me, in one place',
   'That’s the last of them — and “sized by habit” is the same answer you gave for housekeeping, which means nobody has ever tested whether the people doing this work can keep up when it matters. The graphic is everything you’ve told me, in one place. Nothing in it is mine. What I’d propose responds to all five of those, not just the timing. Shall I walk you through it?'),
 'chat': {
  'text': ['That’s the last of them. “Sized by habit” is the same answer you gave for housekeeping.',
           'So nobody has ever tested whether the people doing this work can keep up when it matters.',
           'The board is everything you’ve told me, in one place, in the order you told me. Nothing on it is mine.'],
  'invite': 'What I’d propose answers all five, not just the timing. Shall I walk you through it?',
  'note': 'Five findings, all in your own words.',
  'question': {'text': 'Your answer', 'options': ['Yes, show me', 'Not yet. I have questions about the numbers first']},
  'points': [{'n': 1, 'label': 'One team does both jobs', 'canvas': True}, {'n': 2, 'label': 'Admission time about 3½ hours', 'canvas': True},
             {'n': 3, 'label': 'No set way to match tomorrow’s beds', 'canvas': True}, {'n': 4, 'label': 'Dead bed time 4 to 5 hours', 'canvas': True},
             {'n': 5, 'label': 'No team has ever been sized', 'canvas': True}],
  'prompts': ['Yes, show me', 'Can we check the numbers first?', 'Which of these matters most?']},
 'canvas': {'blocks': [
  {'type': 'heading', 'eyebrow': 'What you’ve told me', 'title': 'Five findings, all your answers',
   'deck': 'In the order you gave them. Every stop is your own answer, or simple arithmetic on your own figures.'},
  {'type': 'evidence-board', 'banner': 'Nothing on this board is mine', 'hint': 'Tap a card to see where it came from.',
   'cards': [{'finding': f, 'quote': q, 'from': fr, 'point': i + 1} for i, (f, q, fr, d) in enumerate(EVID)],
   'sheets': [{'key': 'e%d' % i, 'when': 'Finding %d · %s' % (i + 1, fr), 'title': f, 'text': d} for i, (f, q, fr, d) in enumerate(EVID)]}]}})

# ------------------------------------------------------------------------------------------ bm-dg-11 · the missing diagnosis turn
LOOP = [('a', 'Bed given only when nearly free', None, 'No bed is put against a patient ahead of time, even when you know it will free up.'),
        ('b', 'Nobody called in early', None, 'Without a bed to give, there is nothing to call a patient in against. Calls wait until late.'),
        ('c', 'Patients arrive and wait', '1 to 4:30 PM', 'Your own times. Patients arrive in the early afternoon and wait for the bed to catch up.'),
        ('d', 'Beds never seem ready sooner', None, 'Because no bed is given early, nobody plans for one to free early. So they don’t, and the rule looks right.')]
SPECS.append({
 'turn': turn('bm-dg-11', 'diagnosis', 'Yes, show me', 'Not in the transcript · the diagnosis turn the playbook (§2) says belongs here',
   'Playbook §2: The hospital allocates a bed only once it has been confirmed physically ready, or about to be. So allocation cannot happen until the bed is nearly free. So there is nothing to call a patient in against until late in the day. So the patient arrives at 1 PM and is in the bed at 4:30 PM — and the assumption that beds would not be free earlier has made itself true.',
   note_for_review='Written new from the playbook §2: the practice run went straight from the findings to the five parts.'),
 'chat': {
  'text': ['Before the fix, here is why it happens. Your five findings come back to one rule, and you told me it yourself.',
           'You give a bed only once it is confirmed ready. Follow that rule through a day, and each step leads to the next.',
           'By evening, the belief that beds could not free earlier has made itself true. What I’ll propose is built to break this loop.'],
  'invite': 'Next is the fix, in five parts.',
  'note': 'The wait makes itself true.',
  'points': [{'n': i + 1, 'label': x[1], 'canvas': True} for i, x in enumerate(LOOP)],
  'prompts': ['Show me the five parts', 'Can’t we just drop the rule?', 'Is this common in other hospitals?']},
 'canvas': {'blocks': [
  {'type': 'heading', 'eyebrow': 'Why it happens', 'title': 'One rule, and the loop it starts',
   'deck': 'Your five findings come back to one rule. Follow it round once and it starts itself again.'},
  {'type': 'rule-loop', 'feeds_label': 'Your five findings lead back to one rule', 'hint': 'Tap a step to follow the loop.',
   'feeds': ['One team does both jobs', 'Admission time about 3½ hours', 'No set way to match beds', 'Beds idle 4 to 5 hours', 'No team ever sized'],
   'rule': 'A bed is given only once it is confirmed ready, or about to be.', 'rule_from': 'Your own words, with your times',
   'steps': [dict({'text': t, 'point': i + 1}, **({'clock': v} if v else {}), **({'outcome': True} if i == 3 else {})) for i, (k, t, v, d) in enumerate(LOOP)],
   'back': 'And the next morning, the same rule starts the loop again.',
   'sheets': [{'key': k, 'when': 'Then %d of 4' % (i + 1), 'title': t, 'text': d} for i, (k, t, v, d) in enumerate(LOOP)]}]}})

# ------------------------------------------------------------------------------------------ bm-dg-12 · Turn 17 (the five parts, named)
ANSW = ['Finding 3, no set way to match beds', 'Findings 1 and 2, the team and the wait', 'Everyone the rule touches', 'Finding 5, no team ever sized', 'All five, week by week']
PARTS = [('auto', 'Automations I can build for you', 'The bed picture for tomorrow, worked out and shared, and call-in times for each bed.'),
         ('proc', 'Changes to current processes', 'The steps that change on the wards, at the desk and with housekeeping.'),
         ('ppl', 'The people key to success', 'Who has to agree, and how we get each of them on board.'),
         ('team', 'Changes to teams and roles', 'Who does what differently, and which teams need sizing for the busy hours.'),
         ('kpi', 'The numbers and targets we set', 'What we measure each week, so we know it is working.')]
SPECS.append({
 'turn': turn('bm-dg-12', 'overview', 'Show me the five parts', 'Transcript turn 17 · the overview (the five parts named, none opened yet)',
   'Right — this is what I’d build for you, and it’s the full design rather than a trimmed version, because your admissions run ahead of the beds that free up overnight: about 41 a day against about 33. The effects don’t stop at beds either — discharge, ICU step-down and OT scheduling all move with it. Five parts, in the graphic, along with what this is worth and the one thing it will not do. Click any of the five and I’ll take you through what it actually involves.',
   note_for_review='Still Diagnosis: the five parts are only named here. Picking one of them opens Solutions.'),
 'chat': {
  'text': ['This is what I’d build for you. It is the full design, not a trimmed one. Your admissions run ahead of the beds that free up overnight.',
           'About 41 admissions a day, against about 33 beds free overnight. The effects don’t stop at beds either. Discharge, ICU step-down and the operating theatre list all move with it.',
           'Five parts, with what this is worth and the one thing it will not do. Pick any of the five and I’ll take you through it.'],
  'note': 'Five parts, one aim: the bed earning again sooner.',
  'question': {'text': 'Which part first?', 'options': [p[1] for p in PARTS]},
  'points': [{'n': i + 1, 'label': p[1], 'canvas': True} for i, p in enumerate(PARTS)],
  'prompts': ['Start with the automations', 'Why not just add beds?', 'What will it not do?']},
 'canvas': {'blocks': [
  {'type': 'heading', 'eyebrow': 'What I’d build for you', 'title': 'Five parts, the full design',
   'deck': 'The full design, because your admissions run ahead of the beds that free up overnight.'},
  {'type': 'scale', 'left': {'value': '41', 'label': 'Admissions a day', 'note': 'Planned and emergency, your average'},
   'right': {'value': '33', 'label': 'Beds free overnight', 'note': 'On an average night'},
   'verdict_label': 'So the answer is', 'verdict': 'The full design',
   'text': 'Admissions run ahead of the beds that free up overnight. A trimmed version would not keep up.'},
  {'type': 'corridor', 'label': 'The five parts, none opened yet', 'hint': 'Tap a door to look in. Pick one in the chat to go into it.',
   'doors': [{'name': t, 'text': x, 'point': i + 1} for i, (k, t, x) in enumerate(PARTS)],
   'sheets': [{'key': k, 'when': 'Part %d of 5' % (i + 1), 'title': t, 'text': x,
               'lines': [{'label': 'Answers', 'value': ANSW[i]}]} for i, (k, t, x) in enumerate(PARTS)]},
  {'type': 'effect', 'label': 'Revenue at stake', 'value': '₹1.5 to 2 crore a year', 'state': 'outcome', 'sub': 'What all five parts are aimed at, from your own figures.'},
  {'type': 'effect', 'label': 'Not an occupancy play', 'value': 'Occupancy stays where it is',
   'sub': 'Your 89% is set by demand and length of stay, not by scheduling. The gain is the bed earning again sooner.'}]}})

NOTES = {
 'bm-dg-02': 'Transcript turn 8. The five areas on the rim of a lens; the one asked now is marked.',
 'bm-dg-03': 'Transcript turn 9. Two days drawn bed by bed, hour by hour, so the question does not lead.',
 'bm-dg-04': 'Transcript turn 10. The way from the door to the bed with blank clock times: tap a stop and type its time.',
 'bm-dg-05': 'Transcript turn 11. The same way, filled, with the wait between stops (a redraw, so it keeps the first theme). Adds the stopwatch.',
 'bm-dg-06': 'Transcript turn 12. Two bill tags tied to one bed, times blank: type both.',
 'bm-dg-07': 'Transcript turn 13. The same tags, filled (a redraw). Adds the example set against your number, and the dead bed time.',
 'bm-dg-08': 'Transcript turn 14. A paper bill with five lines: type each figure on its line.',
 'bm-dg-09': 'Transcript turn 15. The 41 beds that change patient each day, and what the hours are worth. Move the slider.',
 'bm-dg-10': 'Transcript turn 16. The five findings pinned on one thread, in the order you gave them, each with your words.',
 'bm-dg-11': 'New, from the playbook §2. Your findings feed one rule; the rule starts a loop that comes back round.',
 'bm-dg-12': 'Transcript turn 17. Demand against supply on a balance, then the five parts as closed doors. The last Diagnosis turn.'}
man = {'note': 'The turns of Bed Management Diagnosis, in conversation order. Only these are built.',
       'turns': [{'file': 'bm-dg-01-A.json', 'note': 'Transcript turn 7, the case reveal. Approved 30 Sep 2026: Sample A, the day on one line.'}]}  # bm-dg-02 to 12 approved 1 Oct 2026
for s in SPECS:
    s['review'] = {'status': 'approved', 'date': '2026-10-01', 'note': 'Approved by Avishek with the second Diagnosis set (one drawing per turn).'}
    dg_actions.add(s)
    fn = s['turn']['id'] + '.json'
    json.dump(s, open(os.path.join(HERE, fn), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    man['turns'].append({'file': fn, 'note': NOTES[s['turn']['id']]})
json.dump(man, open(os.path.join(HERE, 'turns.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('wrote', len(SPECS), 'specs and turns.json')
