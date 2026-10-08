"""The three buttons for every Bed Management Diagnosis turn (rules/08 §8, added 5 Oct 2026 at Avishek's request).
Proceed with next step says the next turn's message; Add more opens the user's own words; Jump goes to Solutions."""
JUMP = {'tab': 'Solutions', 'detail': 'How the bed problem could be fixed', 'say': 'Take me to Solutions'}

def A(go_detail, go_say, add_detail, add_say):
    return {'go': {'detail': go_detail, 'say': go_say}, 'add': {'detail': add_detail, 'say': add_say}, 'jump': dict(JUMP)}

ACTIONS = {
    'bm-dg-01': A('Next: what happens next', 'Yes, that’s our day. What happens next?', 'Tell me about your day', 'Our day with beds looks like this: '),
    'bm-dg-02': A('Next: who runs discharges and admissions', 'One team does both', 'Tell me about your teams', 'Our teams work like this: '),
    'bm-dg-03': A('Next: when each team does what', 'Pattern B, both at once', 'Tell me how your day runs', 'Our discharges and admissions run like this: '),
    'bm-dg-04': A('Next: fill in the times', 'Arrival about 1 PM, in the bed by 4:30 PM', 'Tell me your times', 'Our admission times are: '),
    'bm-dg-05': A('Next: is the morning kept for discharges', 'It happens, but informally', 'Tell me more about the wait', 'About the wait for a bed: '),
    'bm-dg-06': A('Next: when the bill closes', 'The bill closes about 12 to 1 PM', 'Tell me about your billing', 'Our billing on a bed works like this: '),
    'bm-dg-07': A('Next: the money figures', 'Not sure, I’d need to check', 'Tell me what billing shows', 'Our billing team says: '),
    'bm-dg-08': A('Next: send the five figures', 'I’ll send all five now', 'Send the figures you have', 'Here are the figures I have: '),
    'bm-dg-09': A('Next: how the team is sized', 'No, sized by habit', 'Tell me about your team size', 'Our admissions team is sized like this: '),
    'bm-dg-10': A('Next: the reason behind it', 'Yes, show me', 'Tell me what I missed', 'One more thing about our beds: '),
    'bm-dg-11': A('Next: the five parts', 'Show me the five parts', 'Tell me about the rule', 'About the ready-bed rule: '),
    'bm-dg-12': A('Next: start with the automations', 'Start with the automations', 'Tell me which part matters most', 'The part that matters most to us is: '),
}

def add(spec):
    spec['canvas']['actions'] = ACTIONS[spec['turn']['id']]
    return spec
