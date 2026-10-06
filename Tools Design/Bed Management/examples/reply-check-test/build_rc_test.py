"""Build the reply-check test turns: each page, then one review book (Bed Management Diagnosis generator)."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); BM = os.path.dirname(os.path.dirname(HERE))
sys.path[:0] = [os.path.join(BM, 'diagnosis-html-generator'), os.path.join(os.path.dirname(BM), 'Discharge Process')]
import bm_diagnosis_html as B, dp_common as D
OUT = os.path.join(BM, 'out', 'reply-check-test'); os.makedirs(OUT, exist_ok=True)
reg = B.load_registry(); specs = []
NAMES = {'answer': 'Answers', 'reset': 'Reset line, recheck, rework'}
for t in json.load(open(os.path.join(HERE, 'turns.json'), encoding='utf-8'))['turns']:
    s = json.load(open(os.path.join(HERE, t['file']), encoding='utf-8'))
    errs, warns = B.validate(s, reg)
    if errs: sys.exit('%s: %s' % (t['file'], errs))
    r = s['reply_check']; lr = r['last_reply']
    read = lr['class'].replace('_', ' ') + (' · %s, %s' % (lr['cause'].replace('_', ' '), lr['priority']) if lr.get('cause') else '')
    s['turn']['transcript'] = {'label': 'Counted turn %d · run %d · %s' % (r['counted_turn'], r['run'], NAMES[r['action']])}
    s['turn']['context'] = '%s Last reply read as: %s.' % (s['turn']['note_for_review'], read)
    for v in ('desktop', 'mobile'):
        open(os.path.join(OUT, '%s.%s.html' % (s['turn']['id'], v)), 'w', encoding='utf-8').write(B.render_page(s, v, reg))
    specs.append(s)
html = D.book_page(specs, reg, 'Diagnosis', B.render_page, B.tone_of, B, B.dh, B.GEN)
html = html.replace('Discharge Process · Diagnosis turns', 'Reply check (rule 09) · test turns').replace('Discharge Process Diagnosis colours', 'Bed Management Diagnosis colours')
open(os.path.join(OUT, 'reply-check-test-turns.html'), 'w', encoding='utf-8').write(html)
print('built', len(specs), 'turns ->', OUT)
