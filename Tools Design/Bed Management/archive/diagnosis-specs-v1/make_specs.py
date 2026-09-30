"""Writes the Bed Management Diagnosis turn specs (bm-dg-01 … bm-dg-11) as JSON, from the approved Nagpur transcript
(bed-management-sample-chat-transcript.md, turns 7–16) and the diagnosis turn the playbook (§2) says was left out.
The JSON files are the record: each keeps the user's message, the chat parts, the three prompts and the canvas.
Tojo's wording is the transcript's, put into the plain English the rules require; the transcript's own wording is
kept beside it under turn.transcript.said. Run once; afterwards edit the JSON files."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = {'tool': 'Bed Management', 'tab': 'Diagnosis', 'register': 'guided'}

def turn(id_, type_, user, src, said, **kw):
    t = dict(BASE, id=id_, type=type_, user_message=user, transcript={'label': src, 'said': said})
    t.update(kw); return t

SPECS = []

# ---------------------------------------------------------------- bm-dg-01 · Turn 7 · case reveal
SPECS.append({
 'turn': turn('bm-dg-01', 'reveal', 'Beds. That’s the problem I want to work on.', 'Transcript turn 7 · case reveal',
   'Beds it is — and what you’ve described lines up closely with a hospital we worked with. Let me show you their day rather than describe it. One thing to watch as you read it: that bed stopped earning hours before it was empty. Does that look like your day? And is there anything about your own setup you’d add to what’s there?',
   note_for_review='The user’s line is paraphrased in the transcript (“commits to the bed problem”).'),
 'chat': {
  'text': ['Beds it is. What you’ve described lines up closely with a hospital we worked with.',
           'Let me show you their day rather than describe it. One thing to watch: that bed stopped earning hours before it was empty.',
           'Does that look like your day? Is there anything about your own setup you’d add?'],
  'note': 'The bed stops earning long before it is empty.',
  'prompts': ['Yes, that looks like our day', 'Ours is sometimes even longer', 'What happens next?']},
 'canvas': {'blocks': [
  {'type': 'heading', 'eyebrow': 'A hospital much like yours', 'title': 'The bed that stopped earning',
   'deck': 'One bed through one day. Watch where the bill stops, and how long it stays stopped.'},
  {'type': 'revenue-dial', 'stops_billing_at': 11, 'starts_billing_at': 22,
   'labels': {'billing': 'Billing', 'dead': 'Nothing bills on this bed', 'again': 'Billing again'},
   'stops': [
    {'key': 'a', 'at': 11, 'when': 'Late morning', 'title': 'Final bill closed', 'line': 'Sent for insurance approval.', 'bed': 'in',
     'detail': 'The leaving patient’s final bill is closed and sent for insurance approval. The patient is still in the bed.',
     'bill': 'The bill stops here. Nothing more is charged to this bed.'},
    {'key': 'b', 'at': 14, 'when': 'Afternoon', 'title': 'Approval, payment, family briefing', 'line': 'The patient is still in the bed.', 'bed': 'in',
     'detail': 'Approval comes through, the family pays and is told what happens at home. All this time the patient is still in the bed.',
     'bill': 'Still nothing billing, with the bed still in use.'},
    {'key': 'c', 'at': 19, 'when': 'Evening', 'title': 'Patient leaves, bed made ready', 'line': 'Housekeeping cleans and readies it.', 'bed': 'empty',
     'detail': 'The patient finally leaves. Housekeeping cleans the bed and gets it ready for the next patient.',
     'bill': 'The bed is empty now. Still nothing billing.'},
    {'key': 'd', 'at': 22, 'when': 'Later still', 'title': 'Next patient admitted', 'line': 'Only now does a new bill open.', 'bed': 'next', 'outcome': True,
     'detail': 'The next patient is admitted. Only now does a new bill open against this bed.',
     'bill': 'The bed starts earning again.'}],
   'caption': 'Nothing bills on this bed across this whole stretch. That includes pharmacy, tests, scans and procedures.'},
  {'type': 'effect', 'label': 'Dead bed time', 'value': 'Last bill closed to next bill opened', 'outcome': True,
   'sub': 'Often half a day or more on one bed. Most hospitals have never measured it on its own.'}]}})

# ---------------------------------------------------------------- bm-dg-02 · Turn 8 · the five areas
SPECS.append({
 'turn': turn('bm-dg-02', 'agenda', 'Yes, that’s our day. Ours is sometimes even longer. What happens next?', 'Transcript turn 8 · the questions, and the first one',
   'That’s worth holding on to — and most hospitals can’t say how much longer, because nobody measures that stretch end to end. Now I need to pin down how your hospital actually runs it. The graphic has the whole list so you can see where this is going; I’ll take them one at a time rather than dump them on you. First one: does the same team handle both your discharges and your admissions, or are those two separate teams?',
   note_for_review='The user’s line is paraphrased in the transcript (confirms the case, theirs is sometimes longer, asks what next).'),
 'chat': {
  'text': ['That’s worth holding on to. Most hospitals can’t say how much longer, because nobody measures that stretch end to end.',
           'Now I need to pin down how your hospital runs it. The clipboard has the whole list, so you can see where this is going.',
           'I’ll take them one at a time. First one: does one team handle both discharges and admissions, or two separate teams?'],
  'note': 'Five areas. One question at a time.',
  'question': {'text': 'Pick the closest', 'options': ['One team does both', 'Two separate teams', 'It varies by ward. I’d need to check']},
  'points': [{'n': 1, 'label': 'Who runs what', 'canvas': True}, {'n': 2, 'label': 'How long an admission takes', 'canvas': True},
             {'n': 3, 'label': 'Tomorrow’s bed picture', 'canvas': True}, {'n': 4, 'label': 'When billing stops and starts again', 'canvas': True},
             {'n': 5, 'label': 'Who gets the bed ready again', 'canvas': True}],
  'prompts': ['One team does both', 'Why does that matter?', 'Can I answer some of these later?']},
 'canvas': {'blocks': [
  {'type': 'heading', 'eyebrow': 'What I need to know', 'title': 'Five areas, one question at a time',
   'deck': 'This is where the questions are going, so nothing comes as a surprise.'},
  {'type': 'clipboard', 'title': 'Questions for your hospital', 'footer': 'No fixed order between them. I’ll ask one, then wait for your answer.',
   'items': [
    {'key': 'who', 'name': 'Who runs what', 'now': True, 'point': 1, 'ask': 'Does one team handle both discharges and admissions, or two separate teams?'},
    {'key': 'tat', 'name': 'How long an admission takes', 'point': 2, 'ask': 'The five steps of an admission, and a typical day’s clock time for each.'},
    {'key': 'map', 'name': 'Tomorrow’s bed picture', 'point': 3, 'ask': 'Is there a set way to match tomorrow’s planned admissions against the beds you expect to free up?'},
    {'key': 'bill', 'name': 'When billing stops and starts again', 'point': 4, 'ask': 'When the leaving patient’s final bill closes, and when the next patient’s first charge appears.'},
    {'key': 'turn', 'name': 'Who gets the bed ready again', 'point': 5, 'ask': 'Has anyone worked out how many beds housekeeping and transport can ready in the busiest hours?'}]}]}})

# ---------------------------------------------------------------- bm-dg-03 · Turn 9 · pattern A or B
SPECS.append({
 'turn': turn('bm-dg-03', 'question', 'one team does both', 'Transcript turn 9 · the follow-up to “one team”',
   'One team — that’s the more common of the two answers. So the follow-up matters: which of the two patterns in the graphic is closer to how that team’s day actually runs?'),
 'chat': {
  'text': ['One team. That’s the more common of the two answers.',
           'So the follow-up matters. Which of the two patterns is closer to how that team’s day really runs?'],
  'note': 'Same team, two very different days.',
  'question': {'text': 'Which is closer?', 'options': ['Pattern A: one after the other', 'Pattern B: both at once', 'Somewhere between the two']},
  'prompts': ['Pattern B, both at once', 'It changes from day to day', 'Why does the order matter?']},
 'canvas': {'blocks': [
  {'type': 'heading', 'eyebrow': 'One team, two ways to run the day', 'title': 'Which day is closer to yours?',
   'deck': 'The same three moments of the day, run two ways. Read across each row.'},
  {'type': 'pattern-pair', 'rows': ['Morning', 'Midday', 'Afternoon and evening'],
   'patterns': [
    {'key': 'a', 'name': 'Pattern A', 'tag': 'One after the other',
     'steps': ['Discharges first, through the morning', 'The team switches to admissions', 'Admissions land late in the day'],
     'detail': 'The team finishes one job before starting the other. New patients wait for the switch.'},
    {'key': 'b', 'name': 'Pattern B', 'tag': 'Both at once',
     'steps': ['Discharges and admissions worked together', 'Patients already called in for beds due to free', 'Admissions land across the day'],
     'detail': 'The team works both jobs side by side. New patients are called in before their bed is free.'}]}]}})

# ---------------------------------------------------------------- bm-dg-04 · Turn 10 · the blank chain
STAGES = [
 ('arr', 'Patient arrives, or Emergency says admit', 'The clock starts when the patient arrives, or when Emergency decides to admit.'),
 ('doc', 'Paperwork done', 'Registration and admission papers are complete.'),
 ('bed', 'Bed given in the system', 'A bed is put against the patient’s name in your hospital software.'),
 ('rdy', 'Ward or ICU confirms the bed is ready', 'The ward or ICU says the bed is clean and ready to take the patient.'),
 ('in', 'Patient in the bed', 'The patient is physically in the bed. The clock stops here.')]
SPECS.append({
 'turn': turn('bm-dg-04', 'data-ask', 'pattern b', 'Transcript turn 10 · admission time, as a blank chain',
   'Pattern B is the better of the two, and less common than you’d think. Which makes the next one worth getting precise, because it’s what shows the pattern is actually landing: every admission runs through five steps, and the gap between the first and the last is your Admission TAT. The graphic has that chain with the times left blank. Fill in a typical day’s clock times and we’ll see exactly where the time goes.'),
 'chat': {
  'text': ['Pattern B is the better of the two, and less common than you’d think.',
           'That makes the next one worth getting exact. It shows whether the pattern is really landing.',
           'Every admission runs through five steps. The gap between the first and the last is your admission time. Fill in a typical day’s clock times, and we’ll see where the time goes.'],
  'note': 'Clock times settle it.',
  'prompts': ['Arrival about 1 PM, in the bed by 4:30 PM', 'Our times change a lot from day to day', 'Do the times need to be exact?']},
 'canvas': {'blocks': [
  {'type': 'heading', 'eyebrow': 'How long an admission takes', 'title': 'Five steps, times left blank',
   'deck': 'A typical day’s clock times are enough. They do not have to be exact.'},
  {'type': 'admission-line', 'mode': 'blank', 'stages': [{'key': k, 'name': n, 'what': w} for k, n, w in STAGES],
   'caption': 'The gap between the first step and the last is your admission time.'}]}})

# ---------------------------------------------------------------- bm-dg-05 · Turn 11 · the filled chain
TIMES = [('1:00 PM', None), ('2:00 PM', '3 to 4 PM'), ('3:00 PM, sometimes 4', '4 to 5 PM'), ('4:00 PM', '5 to 6 PM'), ('4:30 PM', '6:30 PM, up to 8 PM')]
st5 = []
for (k, n, w), (ty, wo) in zip(STAGES, TIMES):
    d = {'key': k, 'name': n, 'what': w, 'typical': ty}
    if wo: d['worst'] = wo
    if k == 'in': d['outcome'] = True
    st5.append(d)
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
  'pointer': 'Your times are on the admission line.',
  'note': 'Your numbers tell a different story from the claim.',
  'invite': 'Next: is there a set way to match tomorrow’s planned admissions against the beds you expect to free up?',
  'question': {'text': 'Pick the closest',
               'options': ['Yes, a set way, done every day', 'It happens, but informally', 'No, the picture comes together as the day goes']},
  'prompts': ['It happens, but informally', 'We do call some patients in early', 'Why would the morning go to discharges?']},
 'canvas': {'tone': 'count', 'blocks': [
  {'type': 'heading', 'eyebrow': 'Admission time, from your own clock', 'title': 'Five steps, your times',
   'deck': 'A typical day on top, the worst day beneath. The last step is where the patient finally lands.'},
  {'type': 'admission-line', 'mode': 'filled', 'stages': st5},
  {'type': 'time-split', 'title': 'Where the time goes on a good day',
   'parts': [{'label': 'Paperwork', 'hours': 1, 'kind': 'work', 'detail': 'From arrival at 1 PM to paperwork done by 2 PM.'},
             {'label': 'Waiting on the next step', 'hours': 2.5, 'kind': 'wait', 'detail': 'Waiting for a bed to be given, then for the ward to confirm it, then for the move.'}],
   'caption': 'About an hour of this is paperwork. The rest is waiting on the next step.'},
  {'type': 'effect', 'label': 'Admission time from your own times', 'value': 'About 3½ hours on a good day', 'outcome': True,
   'sub': '5½ hours at worst, and up to 7 on the days it stretches to 8 PM.'}]}})

# ---------------------------------------------------------------- bm-dg-06 · Turn 12 · the two blank bills
SLIPS = [('out', 'Patient going home', 'Final bill closed', 'The leaving patient’s final bill is closed. From here, nothing more is charged to this bed.'),
         ('in', 'Next patient, same bed', 'First charge for the next patient', 'The first charge of any kind appears against the next patient in that same bed.')]
SPECS.append({
 'turn': turn('bm-dg-06', 'data-ask', 'it happens but informally', 'Transcript turn 12 · when billing stops and starts again',
   'Informally is the most common of the three answers. Next one, and it is the one that puts a number on what all of this costs: what time does the outgoing patient’s final bill actually get closed, and what time does the first billable entry appear against the next patient in that same bed? Both are blank in the graphic below — same idea as the last one.'),
 'chat': {
  'text': ['Informally is the most common of the three answers.',
           'The next one puts a number on what all this costs. What time does the leaving patient’s final bill close? And when does the first charge appear against the next patient in that same bed?',
           'Both are blank on the two bills. Same idea as the last one.'],
  'note': 'Two times from your billing desk.',
  'prompts': ['The bill closes about 12 to 1 PM', 'I’d have to ask our billing team', 'Why the bill, and not the empty bed?']},
 'canvas': {'blocks': [
  {'type': 'heading', 'eyebrow': 'When billing stops and starts again', 'title': 'Two times on one bed',
   'deck': 'The leaving patient’s last bill, and the next patient’s first charge, on the same bed.'},
  {'type': 'bill-slips', 'mode': 'blank', 'arrow': 'Nothing bills in between',
   'slips': [{'key': k, 'who': w, 'label': l, 'detail': d} for k, w, l, d in SLIPS],
   'captions': ['Everything between these two times bills nothing. That gap is the dead bed time.',
                'Both times almost surely sit in your billing system already. What is rare is putting them side by side for the same bed.']}]}})

# ---------------------------------------------------------------- bm-dg-07 · Turn 13 · the filled bills
SPECS.append({
 'turn': turn('bm-dg-07', 'data-back', 'Final bill typically closed 12–1 PM. First billable entry for the next patient: we try for 5 pm but could go up to 7–8 pm.',
   'Transcript turn 13 · dead bed time, worked out',
   'That is the number this whole conversation has been circling, and it is now yours rather than borrowed from anyone else. Both times are in the graphic, with the gap between them worked out. Last area, and it is a different kind of question: has anyone at the hospital ever actually calculated how many bed turnovers your housekeeping and transport staff can handle in the peak hours — or is that staffing assumed adequate because it has not caused a visible crisis?',
   redraw_of='bm-dg-06'),
 'chat': {
  'text': ['That is the number this whole conversation has been circling. It is now yours, not borrowed from anyone else.',
           'Both times are on the two bills, with the gap between them worked out.',
           'Last area, and a different kind of question. How many beds can your housekeeping and transport staff get ready in the busiest hours?'],
  'note': 'Four to five hours, every time a bed changes patient.',
  'invite': 'Has anyone worked that out? Or is the staffing taken to be enough, because nothing has gone badly wrong?',
  'question': {'text': 'Pick the closest',
               'options': ['Yes, we have worked it out', 'No, it is taken to be enough', 'Not sure. I would need to check']},
  'prompts': ['Not sure, I’d need to check', 'Is 4 to 5 hours a lot?', 'That matches what our billing shows']},
 'canvas': {'blocks': [
  {'type': 'heading', 'eyebrow': 'When billing stops and starts again', 'title': 'Your two times, and the gap',
   'deck': 'Worked out from your own two times. One bed, one change of patient.'},
  {'type': 'bill-slips', 'mode': 'filled', 'arrow': 'Nothing bills in between',
   'slips': [dict(key='out', who='Patient going home', label='Final bill closed', detail=SLIPS[0][3], value='12 to 1 PM'),
             dict(key='in', who='Next patient, same bed', label='First charge for the next patient', detail=SLIPS[1][3], value='5 PM, the goal', worst='Up to 7 to 8 PM', outcome=True)]},
  {'type': 'gap-ruler', 'from': '12:30', 'to': '17:00', 'worst_to': '20:00', 'from_label': 'Bill closed', 'to_label': 'First charge',
   'usual': 'About 4 to 5 hours with nothing billing.', 'worst': 'Up to 8 hours on the days it stretches.'},
  {'type': 'effect', 'label': 'Dead bed time', 'value': 'About 4 to 5 hours, every change of patient', 'outcome': True,
   'sub': 'Up to 8 hours on the days it stretches. Simple arithmetic on your own two times.'}]}})

# ---------------------------------------------------------------- bm-dg-08 · Turn 14 · five money figures
FIG = [('arpob', 'Average earning of one occupied bed a day', '₹ a day', 'Turns each lost hour of bed time into rupees.'),
       ('stay', 'Average stay, in days', 'days', 'Tells us how often each bed changes patient.'),
       ('rev', 'Average daily revenue of the hospital', '₹ a day', 'Lets us check the bed figure against the whole hospital.'),
       ('occ', 'How full the beds are, and the ICU alone', '% of beds', 'Tells us how many beds change patient each day, and where the pressure is.'),
       ('ot', 'Operating theatre use, and its daily revenue', '% and ₹ a day', 'Shows whether a late bed can cost you an operation.')]
SPECS.append({
 'turn': turn('bm-dg-08', 'data-ask', 'not sure', 'Transcript turn 14 · the money figures',
   '“Not sure” is itself the answer — if nobody has run it, nobody knows whether the people doing the physical turnaround can keep up at peak. I’ll come back to that. We now have hours. Hours on their own don’t move anyone, so before we go further I need the figures that turn them into money — they’re listed in the graphic. Once those are in, there’s one more staffing question, on the admissions desk itself.'),
 'chat': {
  'text': ['“Not sure” is itself the answer. If nobody has worked it out, nobody knows whether the people who ready beds keep up at peak. I’ll come back to that.',
           'We now have hours. Hours on their own don’t move anyone. Before we go further, I need the figures that turn them into money.',
           'Once those are in, there’s one more staffing question, on the admissions desk itself.'],
  'pointer': 'The five figures are on the cards.',
  'note': 'Five figures turn hours into money.',
  'points': [{'n': i + 1, 'label': f[1], 'canvas': True} for i, f in enumerate(FIG)],
  'prompts': ['I’ll send all five now', 'I only have some of these', 'Why the ICU on its own?']},
 'canvas': {'blocks': [
  {'type': 'heading', 'eyebrow': 'Turning hours into money', 'title': 'Five figures I need from you',
   'deck': 'Each one turns something we already have into rupees.'},
  {'type': 'figure-cards', 'items': [{'key': k, 'name': n, 'unit': u, 'turns_into': t, 'point': i + 1} for i, (k, n, u, t) in enumerate(FIG)]}]}})

# ---------------------------------------------------------------- bm-dg-09 · Turn 15 · into money
SPECS.append({
 'turn': turn('bm-dg-09', 'sizing', 'ARPOB ₹8,000 a day. ALOS 6.5 days. Average daily revenue ₹28 lakhs. Bed occupancy 89%, ICU 94%. OT utilisation 75%, daily OT revenue ₹5 lakhs.',
   'Transcript turn 15 · dead bed time turned into money',
   'That’s everything I needed. The graphic below turns your dead bed time into a revenue number, step by step, so you can check every line of the arithmetic rather than take it from me. Two things I’ve deliberately left out of it: an ALOS gain on top, because that would be the same bed-days counted twice; and OT, which needs more from you before it can be sized honestly. Last question before we move on: has anyone worked out what your admissions desk can actually handle per hour at peak — counting internal bed transfers alongside admissions — or is that team sized by habit?',
   user_words=['ARPOB', 'ALOS', 'OT']),
 'chat': {
  'text': ['That’s everything I needed.',
           'The steps turn your dead bed time into a revenue number, one line at a time. You can check every line rather than take it from me.',
           'Two things I’ve left out on purpose. A shorter stay on top, because that would count the same days twice. And the operating theatre, which needs more from you first.'],
  'note': '₹1.5 to 2 crore a year, from your own figures.',
  'invite': 'Last one before we move on. Has anyone worked out what your admissions desk can handle an hour at peak, bed transfers included?',
  'question': {'text': 'Pick the closest',
               'options': ['Yes, we have worked it out', 'No, sized by habit and taken to be enough', 'Not sure. I would need to check']},
  'prompts': ['No, sized by habit', 'How sure is the ₹1.5 crore?', 'Why leave the operating theatre out?']},
 'canvas': {'blocks': [
  {'type': 'heading', 'eyebrow': 'Dead bed time, turned into money', 'title': 'From one bed to a year',
   'deck': 'Four steps, each worked out from your figures. Tap a step to see the working.'},
  {'type': 'step-ledger', 'steps': [
    {'key': 'occ', 'label': 'Beds occupied', 'value': '267', 'source': 'derived', 'how': '300 beds, 89% full. 300 × 0.89 is 267.'},
    {'key': 'turn', 'label': 'Beds changing patient a day', 'value': 'About 41', 'source': 'derived', 'how': '267 beds, and each patient stays 6.5 days on average. 267 ÷ 6.5 is about 41.'},
    {'key': 'hrs', 'label': 'Hours won back each time', 'value': '3 to 4 of the 4 to 5', 'source': 'estimate', 'how': 'Not all dead bed time can be won back. We count only the part a better plan can reach.'},
    {'key': 'days', 'label': 'Bed days won back a year', 'value': '1,900 to 2,500', 'source': 'derived', 'outcome': True, 'how': '41 changes a day, 3 to 4 hours each, over 365 days. Divided by 24 hours, that is 1,900 to 2,500 days.'}],
   'condition': 'This holds only if the freed hours can be filled. At 89% full, with patients waiting for beds, they can.'},
  {'type': 'effect', 'label': 'Revenue at stake', 'value': '₹1.5 to 2 crore a year', 'outcome': True,
   'sub': 'At ₹8,000 a bed day. Your figures suggest that is the bed charge alone, so this understates the real amount.'},
  {'type': 'effect', 'label': 'A shorter average stay', 'value': 'Counted once, inside this',
   'sub': 'A shorter stay frees the same bed days. Adding it on top would count them twice.'}]}})

# ---------------------------------------------------------------- bm-dg-10 · Turn 16 · consolidation
CARDS = [('team', 'One team does both jobs', 'Your answer on who runs what', 'Discharges and admissions sit with the same team.'),
         ('tat', 'Admission time about 3½ hours', 'Your five clock times', 'From arrival at 1 PM to the bed at 4:30 PM, on a good day.'),
         ('map', 'No set way to match tomorrow’s beds', 'You said “it happens, but informally”', 'The bed picture comes together as the day goes.'),
         ('dead', 'Dead bed time 4 to 5 hours', 'Your two billing times', 'Bill closed at 12 to 1 PM, first new charge at 5 PM or later.'),
         ('size', 'No team has ever been sized', 'Housekeeping “not sure”, the desk “sized by habit”', 'Nobody has tested whether these teams keep up at the busiest times.')]
SPECS.append({
 'turn': turn('bm-dg-10', 'findings', 'No — sized by habit, assumed adequate', 'Transcript turn 16 · everything you told me, in one place',
   'That’s the last of them — and “sized by habit” is the same answer you gave for housekeeping, which means nobody has ever tested whether the people doing this work can keep up when it matters. The graphic is everything you’ve told me, in one place. Nothing in it is mine. What I’d propose responds to all five of those, not just the timing. Shall I walk you through it?'),
 'chat': {
  'text': ['That’s the last of them. “Sized by habit” is the same answer you gave for housekeeping.',
           'So nobody has ever tested whether the people doing this work can keep up when it matters.',
           'The board is everything you’ve told me, in one place. Nothing on it is mine.'],
  'note': 'Five findings, all in your own words.',
  'invite': 'What I’d propose answers all five, not just the timing. Shall I walk you through it?',
  'question': {'text': 'Your answer',
               'options': ['Yes, show me', 'Not yet. I have questions about the numbers first']},
  'points': [{'n': i + 1, 'label': c[1], 'canvas': True} for i, c in enumerate(CARDS)],
  'prompts': ['Yes, show me', 'Can we check the numbers first?', 'Which of these matters most?']},
 'canvas': {'blocks': [
  {'type': 'heading', 'eyebrow': 'What you’ve told me', 'title': 'Five findings, in the order you gave them',
   'deck': 'Every card is your own answer, or simple arithmetic on your own figures.'},
  {'type': 'pin-board', 'banner': 'Nothing on this board is mine',
   'cards': [{'key': k, 'text': t, 'from': f, 'detail': d, 'point': i + 1} for i, (k, t, f, d) in enumerate(CARDS)]}]}})

# ---------------------------------------------------------------- bm-dg-11 · the missing diagnosis turn (playbook §2)
SPECS.append({
 'turn': turn('bm-dg-11', 'diagnosis', 'Yes, show me', 'Not in the transcript · the diagnosis turn the playbook (§2) says belongs here',
   'Playbook §2: The hospital allocates a bed only once it has been confirmed physically ready, or about to be. So allocation cannot happen until the bed is nearly free. So there is nothing to call a patient in against until late in the day. So the patient arrives at 1 PM and is in the bed at 4:30 PM — and the assumption that beds would not be free earlier has made itself true.',
   note_for_review='The one turn written new: the transcript went straight to the solution here. Wording follows the playbook §2.'),
 'chat': {
  'text': ['Before the fix, here is why it happens. It comes down to one rule, and you told me it yourself.',
           'You give a bed only once it is confirmed ready. Follow that rule through a day, and each step leads to the next.',
           'By evening, the belief that beds could not free earlier has made itself true. Everything I’ll propose is built to break this loop.'],
  'invite': 'Next is the fix, in five parts.',
  'note': 'The wait makes itself true.',
  'points': [{'n': 1, 'label': 'A bed can’t be given early', 'canvas': True}, {'n': 2, 'label': 'Nobody to call in', 'canvas': True},
             {'n': 3, 'label': 'Arrive 1 PM, in bed 4:30 PM', 'canvas': True}, {'n': 4, 'label': 'The wait proves itself', 'canvas': True}],
  'prompts': ['Show me the five parts', 'Can’t we just drop the rule?', 'Is this common in other hospitals?']},
 'canvas': {'blocks': [
  {'type': 'heading', 'eyebrow': 'Why it happens', 'title': 'One rule, and the loop it starts',
   'deck': 'Your own rule, followed through a day, with your own clock times against it.'},
  {'type': 'rule-loop', 'rule': 'A bed is given only once it is confirmed ready, or about to be.', 'rule_from': 'Your words, when you gave your times',
   'steps': [
    {'key': 'a', 'text': 'A bed can’t be given until it is nearly free', 'point': 1, 'detail': 'No bed is put against a patient ahead of time, even when you know it will free up.'},
    {'key': 'b', 'text': 'Nobody can be called in early', 'point': 2, 'detail': 'Without a bed to give, there is nothing to call a patient in against. Calls wait until late in the day.'},
    {'key': 'c', 'text': 'Patients arrive and wait', 'clock': '1 PM in, 4:30 PM in bed', 'point': 3, 'detail': 'Your own times. The patient arrives in the early afternoon and reaches the bed late afternoon.'},
    {'key': 'd', 'text': 'Beds never seem ready earlier', 'outcome': True, 'point': 4, 'detail': 'Because no bed is given early, nobody plans for one to free early. So they don’t, and the rule seems right.'}],
   'back': 'And the next morning, the same rule starts it again'}]}})

MAN = {'note': 'The turns of Bed Management Diagnosis, in conversation order. Only these are built.', 'turns': []}
NOTES = {'bm-dg-01': 'The case reveal. Tap the numbered steps round the dial.',
         'bm-dg-02': 'The five areas on a clipboard, then the first question.',
         'bm-dg-03': 'Two neutral patterns side by side, so the question does not lead.',
         'bm-dg-04': 'The admission line with blank times. Tap a step, then add a time.',
         'bm-dg-05': 'The same line, filled (a redraw, so it keeps the first theme). Adds where the time goes, and the effect.',
         'bm-dg-06': 'Two blank bills on one bed.',
         'bm-dg-07': 'The same bills, filled (a redraw). Adds the gap on a ruler with a usual or worst day switch.',
         'bm-dg-08': 'Five money figures to fill in, 3 + 2 on desktop, 2 + 2 + 1 on a phone.',
         'bm-dg-09': 'The arithmetic as a staircase. Tap a step for the working.',
         'bm-dg-10': 'The five findings pinned to a notice board, in the order they were given.',
         'bm-dg-11': 'New: the diagnosis turn the transcript left out (playbook §2). The rule in the middle, the loop round it.'}
for s in SPECS:
    tid = s['turn']['id']
    fn = '%s.json' % tid
    json.dump(s, open(os.path.join(HERE, fn), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    MAN['turns'].append({'file': fn, 'note': NOTES[tid]})
json.dump(MAN, open(os.path.join(HERE, 'turns.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('wrote', len(SPECS), 'specs')
