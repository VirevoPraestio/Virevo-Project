"""
reply_check — the reply-check record on every tool turn (rule 09, 6 Oct 2026).

Rule 09 (`tojo-v2 - Regular Chat/rules/always-on/09-reply-check-rules.md`) is always on, for the regular chat and every
tool. In a tool, each turn spec carries its record as `reply_check`. This module is the one place the tool generators use
for it:

  check(spec)        -> (errors, warnings)   the record against the schema, and the rule's own checks
  lead_in(spec)      -> HTML                 what the app shows between the user's message and Tojo's answer:
                                             the opening line, the rating exchange, the reset line
  FIXED              -> {'opening','rating','reset'}   the three fixed lines, read word for word from rule 09

One source for everything: the words are read from rule 09, the record's fields from
`tojo-v2 - Regular Chat/schema/reply-check-report.schema.json` ($defs.turn_record). Nothing is copied here, so the
tools can never drift from the chat.

A turn without a record still builds, with a warning: the approved turn templates predate rule 09. A live turn must carry
one. A record that is present must be right, or the turn is refused.
Standard library only.
"""
import html, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))           # Virevo-Project
V2 = os.path.join(REPO, 'tojo-v2 - Regular Chat')
RULE_PATH = os.path.join(V2, 'rules', 'always-on', '09-reply-check-rules.md')
SCHEMA_PATH = os.path.join(V2, 'schema', 'reply-check-report.schema.json')
MISSES = ('ignored', 'not_understood', 'changed_subject', 'rating_fine', 'rating_bad')
e = lambda s: html.escape(str(s), quote=True)

# ------------------------------------------------------------------------------------------ the three fixed lines
def _fixed():
    s = open(RULE_PATH, encoding='utf-8').read()
    def quote_after(heading):
        part = s[s.index(heading):]
        m = re.search(r'\n> (.+)\n', part)
        return m.group(1).strip()
    m = re.search(r'\*\*The text, word for word:\*\* "([^"]+)"', s)
    return {'opening': quote_after('### 2.2'), 'reset': quote_after('### 5.2'), 'rating': m.group(1)}

FIXED = _fixed()
RATING_OPTIONS = ('Good', 'Fine', 'Bad')

# ------------------------------------------------------------------------------------------ a small JSON Schema check
_SCHEMA = json.load(open(SCHEMA_PATH, encoding='utf-8'))

def node_ref(ref):
    return ref.split('#/')[1].split('/')

def _check(v, node, path, errs):
    if '$ref' in node:
        target = _SCHEMA
        for k in node_ref(node['$ref']): target = target[k]
        extra = {k: x for k, x in node.items() if k != '$ref'}
        node = dict(target, **extra)
    if 'enum' in node and v not in node['enum']:
        errs.append('%s: %r is not one of %s' % (path, v, ', '.join(map(str, node['enum'])))); return
    t = node.get('type')
    ok = {'object': isinstance(v, dict), 'array': isinstance(v, list), 'string': isinstance(v, str),
          'integer': isinstance(v, int) and not isinstance(v, bool), 'boolean': isinstance(v, bool)}.get(t, True)
    if not ok:
        errs.append('%s: should be %s' % (path, t)); return
    if t == 'object':
        for k in node.get('required', []):
            if k not in v: errs.append('%s.%s: required' % (path, k))
        props = node.get('properties', {})
        for k, x in v.items():
            if k in props: _check(x, props[k], '%s.%s' % (path, k), errs)
            elif node.get('additionalProperties') is False: errs.append('%s.%s: not a field of the record' % (path, k))
    elif t == 'array':
        for i, x in enumerate(v): _check(x, node.get('items', {}), '%s[%d]' % (path, i), errs)
    elif t == 'string' and 'maxLength' in node and len(v) > node['maxLength']:
        errs.append('%s: %d characters, at most %d' % (path, len(v), node['maxLength']))
    elif t == 'integer' and 'minimum' in node and v < node['minimum']:
        errs.append('%s: at least %d' % (path, node['minimum']))

# ------------------------------------------------------------------------------------------ the checks
def check(spec):
    """The record against the schema, then rule 09's own checks. Returns (errors, warnings)."""
    errs, warns = [], []
    rc = spec.get('reply_check')
    if rc is None:
        warns.append('reply_check: missing. Every live turn carries the reply-check record (rule 09 §9); only templates made before it may leave it out')
        return errs, warns
    _check(rc, _SCHEMA['$defs']['turn_record'], 'reply_check', errs)
    if errs: return errs, warns
    lr, act, say = rc['last_reply'], rc['action'], rc.get('say')
    tid = spec.get('turn', {}).get('id')
    if rc['turn_id'] != tid: errs.append('reply_check.turn_id: %r, but the turn is %r' % (rc['turn_id'], tid))
    if lr['class'] in MISSES and not (lr.get('cause') and lr.get('priority')):
        errs.append('reply_check.last_reply: a miss (%s) needs its cause and priority (09 §7, §8)' % lr['class'])
    if lr['class'] == 'unsure' and not lr.get('why'): errs.append('reply_check.last_reply.why: say why the reply was unsure (09 §3.3)')
    if lr['class'] in MISSES and lr.get('priority') == 'high' and lr['class'] in ('ignored', 'changed_subject', 'rating_fine') and lr.get('cause') not in ('invented_figure', 'misread_reference'):
        warns.append('reply_check.last_reply.priority: high for %s; 09 §8 sets medium unless the rework failed or the cause is a wrong figure or fact' % lr['class'])
    if lr['class'] == 'not_understood' and lr.get('priority') != 'high': errs.append('reply_check.last_reply.priority: not_understood is always high (09 §8)')
    if lr['class'] == 'rating_bad' and lr.get('priority') != 'high': errs.append('reply_check.last_reply.priority: a Bad rating is always high (09 §8)')
    if lr.get('quote') and len(lr['quote'].split()) > 25: errs.append('reply_check.last_reply.quote: at most 25 words (09 §9)')
    # what this turn does, and the line the app shows
    if act == 'reset':
        if say != 'reset': errs.append('reply_check.say: a reset turn shows the reset line (say: "reset")')
        if not rc.get('recheck'): errs.append('reply_check.recheck: a reset records what the recheck found (09 §6)')
        if not (lr['class'] in ('rating_fine', 'rating_bad') or rc['run'] >= 2):
            errs.append('reply_check: a reset needs two misses in a row or a Fine or Bad rating (09 §5.1); run is %d' % rc['run'])
    if say == 'reset' and act != 'reset': errs.append('reply_check.say: the reset line goes with action "reset"')
    if act == 'rating' or say == 'rating':
        errs.append('reply_check: the rating question is a text-only turn the app shows; it is not drawn by a tool generator (09 §4.2)')
    if act == 'answer' and (rc['run'] >= 2 or lr['class'] in ('rating_fine', 'rating_bad')):
        errs.append('reply_check.action: two misses in a row, or a Fine or Bad rating, set off a reset (09 §5.1), not a plain answer')
    if say == 'opening' and rc['counted_turn'] != 1: errs.append('reply_check.say: the opening line goes with the first counted turn of a chat (09 §2)')
    if rc['counted_turn'] and rc['counted_turn'] % 10 == 0 and not lr['class'].startswith('rating_'):
        errs.append('reply_check: counted turn %d; the rating is asked before it (09 §4.1)' % rc['counted_turn'])
    if lr['class'] not in MISSES and lr['class'] != 'unsure' and rc['run'] != 0:
        errs.append('reply_check.run: a reply that is not a miss sets the run back to 0 (09 §1)')
    return errs, warns

# ------------------------------------------------------------------------------------------ what the app shows before the answer
CSS = r'''
.rc-msg{margin:0 0 12px;padding:12px 14px;border-radius:12px 12px 12px 4px;background:var(--rc-bg,#F4F1EA);color:var(--rc-ink,#1D2A24);font-size:14px;line-height:1.55;border:1px solid rgba(0,0,0,.08)}
.rc-msg .rc-k{display:block;font-size:10.5px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;opacity:.65;margin-bottom:4px}
.rc-opts{display:flex;gap:8px;margin-top:10px;flex-wrap:wrap}
.rc-opt{border:1.5px solid currentColor;border-radius:16px;padding:4px 14px;font-size:13px;font-weight:600;opacity:.55}
.rc-opt.is-on{opacity:1;background:#d4a94f;border-color:#d4a94f;color:#1D2A24}
.rc-um{margin:0 0 12px auto;max-width:85%;padding:10px 14px;border-radius:12px 12px 4px 12px;background:#d4a94f;color:#1D2A24;font-size:14px;line-height:1.5;width:fit-content}
@media (max-width:699px){.rc-msg{margin:0 12px 12px}.rc-um{margin:0 12px 12px auto}}
'''

def _tojo(kind, text, extra=''):
    return '<div class="rc-msg" data-rc="%s"><span class="rc-k">Tojo</span>%s%s</div>' % (kind, e(text), extra)

def lead_in(spec):
    """The messages between the user's message and Tojo's answer, as the app shows them (09 §2.3, §4, §5.2)."""
    rc = spec.get('reply_check')
    if not rc: return ''
    out, lr = [], rc['last_reply']
    if rc.get('say') == 'opening':
        out.append(_tojo('opening', FIXED['opening']))
    if lr['class'].startswith('rating_') and lr['class'] != 'rating_skipped':
        picked = lr['class'].split('_')[1].capitalize()
        opts = '<div class="rc-opts">%s</div>' % ''.join('<span class="rc-opt%s">%s</span>' % (' is-on' if o == picked else '', o) for o in RATING_OPTIONS)
        out.append(_tojo('rating', FIXED['rating'], opts))
        out.append('<div class="rc-um">%s</div>' % picked)
    if rc.get('say') == 'reset':
        out.append(_tojo('reset', FIXED['reset']))
    return ('<style>%s</style>' % CSS + ''.join(out)) if out else ''
