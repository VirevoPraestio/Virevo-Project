#!/usr/bin/env python3
"""
diagnosis_html — offline HTML generator for Tojo responses.

Claude (via the API) returns a JSON "response spec": the chat-panel parts it writes itself
(text, note, points, prompts, question) and a canvas made of blocks chosen from the registry,
with slot values. This program validates that spec against blocks/registry.json and renders
the canvas to self-contained HTML — no model call, no network needed to build.

  python3 diagnosis_html.py render  SPEC.json -o out.html [--view canvas|desktop|mobile]
  python3 diagnosis_html.py validate SPEC.json
  python3 diagnosis_html.py gallery -o gallery.html          # every block, wide + narrow, from samples
  python3 diagnosis_html.py catalog                          # prompt-ready block catalogue (markdown)
  python3 diagnosis_html.py feedback BLOCK approved|changes_requested|retired "note"

Stdlib only. Python 3.8+.
"""
import argparse, datetime, html, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
REG_PATH = os.path.join(ROOT, 'blocks', 'registry.json')
SAMPLES_PATH = os.path.join(ROOT, 'blocks', 'samples.json')
ASSETS = os.path.join(HERE, 'assets')
FONTS = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Poppins:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Caveat:wght@500;700&display=swap">'
GEN_VERSION = '1.0'

def load_registry():
    with open(REG_PATH, encoding='utf-8') as f:
        return json.load(f)

def e(s):
    return html.escape('' if s is None else str(s), quote=True)

CHEV = '<svg class="tj-chev" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>'
TICK = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>'
CROSS = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>'
STATUS_LABEL = {'now': 'Asking now', 'next': 'Next', 'done': 'Done', 'later': 'Later', 'flag': 'Needs attention'}
SRC_LABEL = {'yours': 'Your number', 'derived': 'From your numbers', 'illustrative': 'Example only', 'estimate': 'Tojo’s guess', 'target': 'Goal', 'needed': 'Need from you'}

class Ctx:
    def __init__(self):
        self.n = 0
    def uid(self, p='tj'):
        self.n += 1
        return '%s%d' % (p, self.n)

def pt(item):
    return ' data-tj-point="%d"' % int(item['point']) if item.get('point') is not None else ''

def st(item, default='plain'):
    return ' data-state="%s"' % e(item.get('state') or default)

def toggle(ctx, shut_label, open_label, body_html, cls='tj-toggle'):
    """Native <details>: works with no JavaScript, in the app, in the design canvas and in email previews."""
    return ('<details class="tj-more"><summary class="%s"><span class="shut">%s</span><span class="open">%s</span>%s</summary>'
            '<div class="tj-more-body">%s</div></details>') % (cls, e(shut_label), e(open_label), CHEV, body_html)

def bullets_html(points, lead=None):
    lead_html = '<p class="tj-text" style="color:var(--ink);font-weight:600">%s</p>' % e(lead) if lead else ''
    return lead_html + '<ul class="tj-list">%s</ul>' % ''.join('<li>%s</li>' % e(p) for p in points)

def divider(text):
    return '<p class="tj-divider">%s</p>' % e(text) if text else ''

# ---------------------------------------------------------------- block renderers
def r_heading(b, ctx):
    return ('<header class="tj-heading"><div class="tj-eyebrow">%s</div><h2 class="tj-big">%s</h2>%s</header>'
            % (e(b['eyebrow']), e(b['title']), '<p>%s</p>' % e(b['deck']) if b.get('deck') else ''))

def r_handnote(b, ctx):
    return '<p class="tj-hand tj-handnote">%s</p>' % e(b['text'])

def _callout(s, grp, hidden):
    right = ''
    if s.get('question'):
        now = '<p class="tj-text">This is the one I’m asking now — answer in the chat.</p>' if s['status'] == 'now' else ''
        right = '<div><div class="tj-label">Tojo’s question at this stop</div><p class="q">%s</p>%s</div>' % (e(s['question']), now)
    heard = ('<div class="tj-label">What people usually say</div><p class="tj-hand" style="margin:0;font-size:25px">%s</p>' % e(s['heard_as'])) if s.get('heard_as') else ''
    return ('<div class="tj-card tj-shadow tj-callout" data-tj-panel="%s:%s"%s%s>'
            '<div><div class="hd"><h3 class="tj-big">%s · %s</h3><span class="tj-tag" data-status="%s">%s</span></div>'
            '<p class="tj-text">%s</p>%s</div>%s</div>') % (
        grp, e(s['id']), ' hidden' if hidden else '', pt(s), e(s['id']), e(s['name']), e(s['status']), e(STATUS_LABEL[s['status']]),
        e(s['text']), heard, right)

def r_route_map(b, ctx):
    grp = ctx.uid('route')
    stations = b['stations']
    sel = b.get('selected') or next((s['id'] for s in stations if s['status'] == 'now'), stations[0]['id'])
    statuses = [k for k in ['now', 'done', 'next', 'later', 'flag'] if any(s['status'] == k for s in stations)]
    legend = '' if b.get('legend') is False else '<div class="tj-legend">%s</div>' % ''.join(
        '<span><i data-status="%s"></i>%s</span>' % (k, STATUS_LABEL[k]) for k in statuses)
    def stn(s):
        return ('<button type="button" class="tj-stn" data-tj-pick="%s:%s" aria-pressed="%s"><span class="tj-dot" data-status="%s">%s</span><span class="n">%s</span></button>'
                % (grp, e(s['id']), 'true' if s['id'] == sel else 'false', e(s['status']), e(s['id']), e(s['name'])))
    items = ['<div class="tj-term"><b></b><span class="n">%s</span></div>' % e(b['start_label'])] + [stn(s) for s in stations] + \
            ['<div class="tj-term end"><b></b><span class="n">%s</span></div>' % e(b['end_label'])]
    rows = [items[i:i + 6] for i in range(0, len(items), 6)]
    rhtml = []
    for ri, row in enumerate(rows):
        rev = ri % 2 == 1
        k = len(row)
        style = ''
        if k < 6:
            short = 'calc(46px + %d * (100%% - 92px) / 5)' % (6 - k)
            row = row + ['<div class="tj-pad" aria-hidden="true"></div>'] * (6 - k)
            style = ' style="--short:%s"' % short
        turn = ''
        if ri < len(rows) - 1:
            turn = '<div class="tj-turn %s" aria-hidden="true"></div>' % ('l' if rev else 'r')
        cls = 'tj-rrow' + (' rev' if rev else '') + (' short' if k < 6 else '')
        rhtml.append('<div class="%s"%s>%s%s</div>' % (cls, style, ''.join(row), turn))
    desk = '<div class="tj-desk"><div class="tj-route">%s</div><div style="margin-top:22px">%s</div></div>' % (
        ''.join(rhtml), ''.join(_callout(s, grp, s['id'] != sel) for s in stations))
    vs = []
    for s in stations:
        vs.append('<div><button type="button" class="tj-vstn" data-tj-pick="%s:%s" aria-pressed="%s"><span class="tj-dot" data-status="%s">%s</span><span class="n">%s</span><span class="s">%s</span></button>'
                  '<div class="tj-vdetail">%s</div></div>' % (grp, e(s['id']), 'true' if s['id'] == sel else 'false', e(s['status']), e(s['id']),
                                                            e(s['name']), e(STATUS_LABEL[s['status']]), _callout(s, grp, s['id'] != sel)))
    mob = '<div class="tj-mob"><div class="tj-vroute"><div class="tj-vterm"><b></b>%s</div>%s<div class="tj-vterm end"><b></b>%s</div></div></div>' % (
        e(b['start_label']), ''.join(vs), e(b['end_label']))
    return '<section class="tj-block" data-block="route-map">%s%s%s</section>' % (legend, desk, mob)

def r_chain(b, ctx):
    steps = b['steps']
    parts = []
    if b.get('zone'):
        parts.append('<div class="zone">%s</div>' % e(b['zone']))
    for i, s in enumerate(steps):
        state = s.get('state') or ('outcome' if i == len(steps) - 1 else 'plain')
        flag = '<span class="tj-tag flag">%s</span>' % e(s['flag']) if s.get('flag') else ''
        val = '<div class="tj-val">%s</div>' % e(s['value']) if s.get('value') else ''
        badge = ''
        if s.get('badge'):
            badge = '<div class="badge" data-b="%s">%s %s</div>' % (e(s['badge']), TICK if s['badge'] == 'keep' else CROSS, e(s.get('badge_text', 'Keep' if s['badge'] == 'keep' else 'Change')))
        parts.append('<div class="box" data-state="%s"%s>%s<div class="t">%s</div>%s%s</div>' % (e(state), pt(s), flag, e(s['title']), val, badge))
    label = '<div class="tj-label">%s</div>' % e(b['label']) if b.get('label') else ''
    return '<section class="tj-block" data-block="chain" style="display:flex;flex-direction:column;gap:12px">%s<div class="tj-chain%s">%s</div>%s</section>' % (
        label, ' long' if len(steps) + (1 if b.get('zone') else 0) > 5 else '',
        '<span class="arr" aria-hidden="true">→</span>'.join(parts), divider(b.get('caption')))

def r_two_flow(b, ctx):
    cells = ['<div></div><div class="hd">%s</div><div class="hd">%s</div>' % (e(b['left_title']), e(b['right_title']))]
    for r in b['rows']:
        lv = '<div class="tj-val">%s</div>' % e(r['left_value']) if r.get('left_value') else ''
        rv = '<div class="tj-val">%s</div>' % e(r['right_value']) if r.get('right_value') else ''
        flag = '<span class="tj-tag flag">%s</span>' % e(r['flag']) if r.get('flag') else ''
        cells.append('<div class="rl"%s>%s</div><div class="cell%s" data-state="%s">' % (pt(r), e(r['label']), ' flagged' if flag else '', e(r.get('left_state') or ('target' if flag else 'plain'))) + flag + '<span class="ct">%s</span><span class="t">%s</span>%s</div>'
                     '<div class="cell" data-state="%s"><span class="ct">%s</span><span class="t">%s</span>%s</div>' % (
                         e(b['left_title']), e(r['left']), lv, e(r.get('right_state') or 'plain'), e(b['right_title']), e(r['right']), rv))
    return '<section class="tj-block" data-block="two-flow" style="display:flex;flex-direction:column;gap:12px"><div class="tj-2f">%s</div>%s</section>' % (''.join(cells), divider(b.get('caption')))

def r_compare_table(b, ctx):
    opts, rows, hi = b['options'], b['rows'], b.get('highlight')
    n = len(opts)
    g = ['<div class="h"></div>'] + ['<div class="h%s">%s%s</div>' % (' hi' if hi == i else '', e(o['name']), ' <span class="tj-tag">%s</span>' % e(o['tag']) if o.get('tag') else '') for i, o in enumerate(opts)]
    for r in rows:
        g.append('<div class="rl"%s>%s</div>' % (pt(r), e(r['label'])))
        g += ['<div class="%s">%s</div>' % ('hi' if hi == i else '', e(v)) for i, v in enumerate(r['values'])]
    desk = '<div class="tj-desk"><div class="tj-cmp"><div class="g" style="grid-template-columns: minmax(0,0.8fr) repeat(%d, minmax(0,1fr))">%s</div></div></div>' % (n, ''.join(g))
    cards = []
    for i, o in enumerate(opts):
        dl = ''.join('<dt>%s</dt><dd>%s</dd>' % (e(r['label']), e(r['values'][i])) for r in rows)
        cards.append('<div class="opt%s"><div class="t">%s%s</div><dl>%s</dl></div>' % (' hi' if hi == i else '', e(o['name']), ' <span class="tj-tag">%s</span>' % e(o['tag']) if o.get('tag') else '', dl))
    mob = '<div class="tj-mob"><div class="tj-cmpm">%s</div></div>' % ''.join(cards)
    return '<section class="tj-block" data-block="compare-table" style="display:flex;flex-direction:column;gap:12px">%s%s%s</section>' % (desk, mob, divider(b.get('caption')))

def r_stat_strip(b, ctx):
    items = ''.join('<div class="tj-stat"%s%s><div class="l">%s</div><div class="tj-val">%s</div><span class="tj-src" data-src="%s">%s</span>%s</div>' % (
        st(s), pt(s), e(s['label']), e(s['value']), e(s['source']), e(SRC_LABEL[s['source']]), '<div class="nt">%s</div>' % e(s['note']) if s.get('note') else '')
        for s in b['stats'])
    return '<section class="tj-block" data-block="stat-strip" style="display:flex;flex-direction:column;gap:12px"><div class="tj-stats" style="--n: %d">%s</div>%s</section>' % (len(b['stats']), items, divider(b.get('caption')))

FMT_PY = {
    'int': lambda n: indian(n), 'dec1': lambda n: trim(n), 'pct': lambda n: '%s%%' % round(n, 1),
    'inr': lambda n: '₹' + indian(n), 'inr_l': lambda n: '₹%s lakh' % trim(n / 1e5), 'inr_cr': lambda n: '₹%s crore' % trim(n / 1e7),
    'days': lambda n: '%s %s' % (trim(n, 2), 'day' if n == 1 else 'days'), 'hours': lambda n: '%s %s' % (trim(n), 'hour' if n == 1 else 'hours'), 'raw': lambda n: str(n)}

def trim(n, d=1):
    return ('%.*f' % (d, n)).rstrip('0').rstrip('.')

def indian(n):
    import math
    n = int(math.floor(n + 0.5)); s = str(abs(n))
    if len(s) > 3:
        head, tail = s[:-3], s[-3:]
        parts = []
        while len(head) > 2:
            parts.insert(0, head[-2:]); head = head[:-2]
        if head: parts.insert(0, head)
        s = ','.join(parts) + ',' + tail
    return ('-' if n < 0 else '') + s

def py_eval(expr, vars):
    import ast
    node = ast.parse(expr, mode='eval')
    def ev(n):
        if isinstance(n, ast.Expression): return ev(n.body)
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)): return n.value
        if isinstance(n, ast.Name): return vars[n.id]
        if isinstance(n, ast.UnaryOp) and isinstance(n.op, ast.USub): return -ev(n.operand)
        if isinstance(n, ast.BinOp) and isinstance(n.op, (ast.Add, ast.Sub, ast.Mult, ast.Div)):
            a, b = ev(n.left), ev(n.right)
            return {ast.Add: a + b, ast.Sub: a - b, ast.Mult: a * b, ast.Div: a / b if b else float('nan')}[type(n.op)]
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in ('min', 'max', 'round'):
            return {'min': min, 'max': max, 'round': round}[n.func.id](*[ev(x) for x in n.args])
        raise ValueError('not allowed in a formula')
    return ev(node)

def r_calculator(b, ctx):
    ins = []
    for i in b['inputs']:
        src = '<span class="tj-src" data-src="%s">%s</span>' % (e(i['source']), e(SRC_LABEL[i['source']]))
        val = i.get('value')
        control = i.get('control') or ('field' if val is None else 'fixed')
        fid = ctx.uid('in')
        shown = FMT_PY.get(i.get('format', 'raw'), FMT_PY['raw'])(val) if val is not None else '—'
        if control == 'slider':
            ctl = '<input id="%s" type="range" data-in="%s" min="%s" max="%s" step="%s" value="%s"><div class="rng"><span>%s</span><span>%s</span></div>' % (
                fid, e(i['id']), e(i['min']), e(i['max']), e(i.get('step', 1)), e(val if val is not None else i['min']),
                FMT_PY[i.get('format', 'raw')](i['min']), FMT_PY[i.get('format', 'raw')](i['max']))
        elif control == 'field':
            ctl = '<input id="%s" type="number" inputmode="decimal" data-in="%s" placeholder="Type your figure"%s>' % (fid, e(i['id']), ' value="%s"' % e(val) if val is not None else '')
        else:
            ctl = '<input id="%s" type="hidden" data-in="%s" value="%s">' % (fid, e(i['id']), e(val))
        if control == 'fixed':
            ins.append('<div class="tj-in fixed"%s><div class="top"><label for="%s">%s</label><span class="v" data-in-val="%s">%s</span></div>%s%s</div>' % (
                pt(i), fid, e(i['label']), e(i['id']), e(shown), src, ctl))
            continue
        vshow = '' if control == 'field' else '<div class="v" data-in-val="%s">%s</div>' % (e(i['id']), e(shown))
        ins.append('<div class="tj-in"%s><div class="top"><label for="%s">%s</label>%s</div>%s%s</div>' % (
            pt(i), fid, e(i['label']), src, vshow, ctl))
    vals = {i['id']: i['value'] for i in b['inputs'] if i.get('value') is not None}
    complete = len(vals) == len(b['inputs'])
    steps = []
    for k, s in enumerate(b['steps']):
        shown = '—'
        if complete:
            try:
                vals[s['id']] = py_eval(s['formula'], vals)
                shown = FMT_PY.get(s.get('format', 'raw'), FMT_PY['raw'])(vals[s['id']])
            except Exception:
                shown = '—'
        state = s.get('state') or ('outcome' if k == len(b['steps']) - 1 else 'plain')
        steps.append('<div class="tj-step" data-state="%s"%s><div class="l">%s%s</div><div class="tj-val" data-step="%s">%s</div></div>' % (
            e(state), pt(s), e(s['label']), '<small>%s</small>' % e(s['note']) if s.get('note') else '', e(s['id']), e(shown)))
    waiting = b.get('waiting') or 'Waiting for your number. The sums fill in as soon as you type it.'
    spec = json.dumps({'inputs': [{'id': i['id'], 'format': i.get('format', 'raw')} for i in b['inputs']],
                       'steps': [{'id': s['id'], 'formula': s['formula'], 'format': s.get('format', 'raw')} for s in b['steps']]})
    return ('<section class="tj-block" data-block="calculator" data-tj-calc><script type="application/json">%s</script><div class="tj-calc">'
            '<div class="tj-inputs">%s</div><div class="tj-deriv">%s%s</div></div>%s</section>') % (
        spec.replace('</', '<\\/'), ''.join(ins), '<span class="dn" aria-hidden="true"></span>'.join(steps),
        '' if complete else '<p class="tj-text" data-tj-waiting style="margin-top:10px;color:var(--red);font-weight:600">%s</p>' % e(waiting), divider(b['condition']))

def r_threshold_gauges(b, ctx):
    gs = []
    for g in b['gauges']:
        lo, hi = float(g['min']), float(g['max'])
        pc = lambda v: '%.2f%%' % max(0, min(100, (float(v) - lo) / (hi - lo) * 100))
        v = g.get('value')
        inner = ''
        if v is not None:
            inner += '<div class="fill" style="width:%s"></div>' % pc(v)
        if g.get('band_low') is not None and g.get('band_high') is not None:
            inner += '<div class="band" style="left:%s;width:%.2f%%"></div>' % (pc(g['band_low']), (float(g['band_high']) - float(g['band_low'])) / (hi - lo) * 100)
        if g.get('line') is not None:
            inner += '<div class="line" style="left:%s"></div><div class="ll" style="left:%s">%s</div>' % (pc(g['line']), pc(g['line']), e(g.get('line_label', '')))
        if v is not None:
            anchor = g['band_low'] if g.get('band_low') is not None else v
            inner += '<div class="you" style="left:%s">%s</div>' % (pc(anchor), e(g.get('value_label') or v))
        gs.append('<div class="tj-gauge"%s><div><div class="l">%s</div><div class="c">%s</div></div><div class="tj-track%s">%s</div></div>' % (
            pt(g), e(g['label']), e(g['caption']), '' if v is not None else ' unknown', inner))
    return '<section class="tj-block" data-block="threshold-gauges"><div class="tj-gauges" style="--n: %d">%s</div></section>' % (len(gs), ''.join(gs))

def r_balance(b, ctx):
    tilt = {'right': '8deg', 'left': '-8deg', 'even': '0deg'}[b['heavier']]
    pan = lambda c, l, v: '<div class="tj-pan %s"><i></i><div><small>%s</small><b>%s</b></div></div>' % (c, e(l), e(v))
    return ('<section class="tj-block tj-bal" data-block="balance"><div class="tj-scale" style="--tilt:%s" role="img" aria-label="%s: %s against %s: %s">'
            '<div class="base"></div><div class="post"></div><div class="beam">%s%s</div><div class="pivot"></div></div>'
            '<p class="tj-hand tj-handnote" style="text-align:center">%s</p></section>') % (
        tilt, e(b['left_label']), e(b['left_value']), e(b['right_label']), e(b['right_value']),
        pan('a', b['left_label'], b['left_value']), pan('b', b['right_label'], b['right_value']), e(b['caption']))

def r_progress_trail(b, ctx):
    dots = ''.join('<span class="tj-dot" data-status="%s">%s</span>' % (e(s['status']), e(s['id'])) for s in b['steps'])
    return '<section class="tj-block tj-trailw" data-block="progress-trail"><div class="tj-trail" aria-hidden="true">%s</div><p class="tj-trail-txt"><strong>%s</strong> %s</p></section>' % (dots, e(b['summary']), e(b['next']))

def r_agenda_grid(b, ctx):
    lab = {'covered': 'Covered', 'current': 'Now', 'remaining': 'Still to do'}
    items = []
    for p in b['parts']:
        body = bullets_html(p['detail_points'], p.get('detail')) if p.get('detail_points') else ('<p class="tj-text">%s</p>' % e(p['detail']) if p.get('detail') else '')
        more = toggle(ctx, p.get('more_label') or 'See what’s in it', 'Close', body) if body else ''
        items.append('<div class="tj-item" data-status="%s"%s><div class="h"><span class="t">%s</span><span class="tj-tag"%s>%s</span></div><p class="q">%s</p>%s</div>' % (
            e(p['status']), pt(p), e(p['title']), ' data-status="now"' if p['status'] == 'current' else (' data-status="done"' if p['status'] == 'covered' else ''), lab[p['status']], e(p['question']), more))
    return '<section class="tj-block" data-block="agenda-grid"><div class="tj-grid" style="--cols:%d">%s</div></section>' % (3 if len(items) >= 3 else 2, ''.join(items))

def r_cards(b, ctx):
    items = []
    for c in b['items']:
        tag = '<span class="tj-tag">%s</span>' % e(c['tag']) if c.get('tag') else ''
        body = bullets_html(c['more_points'], c.get('more')) if c.get('more_points') else ('<p class="tj-text">%s</p>' % e(c['more']) if c.get('more') else '')
        more = toggle(ctx, c.get('more_label') or 'Read more', 'Close', body) if body else ''
        items.append('<div class="tj-item"%s%s><div class="h"><span class="t">%s</span>%s</div><p class="q">%s</p>%s</div>' % (st(c), pt(c), e(c['title']), tag, e(c['text']), more))
    label = '<div class="tj-label">%s</div>' % e(b['label']) if b.get('label') else ''
    cols = 3 if len(items) in (3, 5, 6) else 2
    return '<section class="tj-block" data-block="cards" style="display:flex;flex-direction:column;gap:12px">%s<div class="tj-grid" style="--cols:%d">%s</div></section>' % (label, cols, ''.join(items))

def r_role_cards(b, ctx):
    doers = ''.join('<div class="tj-item%s"%s><div class="h"><span class="t">%s</span>%s</div><p class="q">%s</p></div>' % (
        ' resist' if d.get('resistant') else '', pt(d), e(d['role']), '<span class="tj-tag" style="color:var(--st-target)">Most to give up</span>' if d.get('resistant') else '', e(d['ask']))
        for d in b['doers'])
    a = b['approver']
    appr = ('<div class="tj-approver"' + pt(a) + '><span class="tj-tag" data-status="done" style="align-self:flex-start">Approver</span><span class="t" style="font-size:17px;font-weight:700">%s</span>'
            '<p class="tj-text">Approves: %s</p><p class="tj-text" style="color:var(--red)">If this never comes: %s</p></div>') % (e(a['role']), e(a['approves']), e(a['fails_if']))
    return '<section class="tj-block" data-block="role-cards" style="display:flex;flex-direction:column;gap:12px"><div class="tj-roles"><div class="tj-grid">%s</div>%s</div>%s</section>' % (doers, appr, divider(b.get('caption')))

def r_fill_blank(b, ctx):
    parts = []
    for s in b['steps']:
        body = '<div class="tj-val">%s</div>' % e(s['value']) if (b['mode'] == 'filled' and s.get('value')) else '<div class="blank">%s</div>' % e(s['field'])
        parts.append('<div class="box" data-state="%s"%s><div class="t">%s</div>%s</div>' % ('plain' if b['mode'] == 'filled' else 'target', pt(s), e(s['title']), body))
    return '<section class="tj-block tj-fill" data-block="fill-blank" style="display:flex;flex-direction:column;gap:12px"><div class="tj-chain%s">%s</div>%s</section>' % (
        ' long' if len(b['steps']) > 5 else '', '<span class="arr" aria-hidden="true">→</span>'.join(parts), divider(b.get('caption')))

def r_fork(b, ctx):
    opts = ['<div class="tj-item"%s><span class="t">%s</span><p class="q">%s</p></div>' % (pt(o), e(o['title']), e(o['text'])) for o in b['options']]
    return '<section class="tj-block" data-block="fork" style="display:flex;flex-direction:column;gap:14px"><p class="tj-forkq">%s</p><div class="tj-fork%s">%s</div></section>' % (
        e(b['question']), ' n3' if len(opts) == 3 else '', '<span class="or">or</span>'.join(opts))

# ---------------------------------------------------------------- templates from the conversation playbook (v4)
def fmt_hour(t):
    h = t % 24; hh = int(h); m = int(round((h - hh) * 60))
    if m == 60: hh, m = (hh + 1) % 24, 0
    if hh == 0 and m == 0: return 'Midnight'
    if hh == 12 and m == 0: return 'Noon'
    return '%d%s %s' % (hh % 12 or 12, ':%02d' % m if m else '', 'AM' if hh < 12 else 'PM')

def dur(hours):
    whole = int(hours); mins = int(round((hours - whole) * 60))
    if mins == 60: whole, mins = whole + 1, 0
    s = '%d hour%s' % (whole, '' if whole == 1 else 's') if whole else ''
    if mins: s += (' ' if s else '') + '%d minutes' % mins
    return s

def r_time_window(b, ctx):
    lo, hi = float(b['axis_from']), float(b['axis_to'])
    pc = lambda t: max(0.0, min(100.0, (float(t) - lo) / (hi - lo) * 100))
    tick = float(b.get('tick') or 3)
    ticks, t = [], (int(lo // tick) + 1) * tick if lo % tick else lo
    while t <= hi + 1e-9:
        ticks.append(t); t += tick
    evs = sorted(b['events'], key=lambda x: x['time'])
    levels, last = [], {}
    for ev in evs:
        p = pc(ev['time']); lvl = 0
        while lvl in last and p - last[lvl] < 15: lvl += 1
        last[lvl] = p; levels.append(min(lvl, 2))
    top = 48 + 44 * max(levels + [0])
    w = b.get('window')
    band = ''
    if w:
        band = ('<div class="win"%s style="left:%.2f%%;width:%.2f%%"><div class="wl"><b>%s</b><span>%s</span></div></div>') % (
            pt(w), pc(w['start']), pc(w['end']) - pc(w['start']), e(w['label']), e(dur(float(w['end']) - float(w['start']))))
    marks = ''
    for ev, lvl in zip(evs, levels):
        p = pc(ev['time']); align = 'l' if p < 9 else ('r' if p > 91 else 'c')
        marks += ('<div class="ev %s" data-state="%s"%s style="left:%.2f%%;--lift:%dpx"><i></i><div class="lab"><b>%s</b><span>%s</span></div></div>') % (
            align, e(ev.get('state') or 'plain'), pt(ev), p, 16 + 44 * lvl, e(fmt_hour(ev['time'])), e(ev['label']))
    tk = ''.join('<span style="left:%.2f%%">%s</span>' % (pc(x), e(fmt_hour(x))) for x in ticks)
    desk = '<div class="tj-desk"><div class="tj-tw" style="padding-top:%dpx"><div class="track">%s%s</div><div class="ticks">%s</div></div></div>' % (top, band, marks, tk)
    rows = []
    placed = False
    for ev in evs:
        if w and not placed and float(ev['time']) > float(w['start']):
            rows.append('<li class="vwin"%s><b>%s · %s</b>%s</li>' % (pt(w), e(w['label']), e(dur(float(w['end']) - float(w['start']))), '<span>%s</span>' % e(w['note']) if w.get('note') else ''))
            placed = True
        rows.append('<li class="vev" data-state="%s"%s><i></i><b>%s</b><span>%s</span></li>' % (e(ev.get('state') or 'plain'), pt(ev), e(fmt_hour(ev['time'])), e(ev['label'])))
    mob = '<div class="tj-mob"><ol class="tj-twv">%s</ol></div>' % ''.join(rows)
    note = '<p class="tj-text">%s</p>' % e(w['note']) if (w and w.get('note')) else ''
    share = ('<div class="tj-share"><span class="tj-big">%s</span><span>%s</span></div>' % (e(b['share']['value']), e(b['share']['label']))) if b.get('share') else ''
    label = '<div class="tj-label">%s</div>' % e(b['label']) if b.get('label') else ''
    return '<section class="tj-block" data-block="time-window" style="display:flex;flex-direction:column;gap:10px">%s%s%s<div class="tj-desk">%s</div>%s%s</section>' % (
        label, desk, mob, note, share, divider(b.get('caption')))

def r_hour_load(b, ctx):
    bars = b['bars']; n = len(bars); mx = max(float(x['value']) for x in bars) or 1
    inwin = {}
    for wi, w in enumerate(b['windows']):
        for i in range(int(w['start']), int(w['end']) + 1): inwin[i] = wi
    cols = ''.join('<div class="bar%s"><em>%s</em><i style="height:%.1f%%"></i><span>%s</span></div>' % (
        ' on' if i in inwin else '', e(trim(float(x['value']))), float(x['value']) / mx * 100, e(x['label'])) for i, x in enumerate(bars))
    brackets = ''.join('<div class="br"%s style="grid-column:%d / %d"><b>%s</b><span class="tj-tag" data-status="now">%s</span></div>' % (
        pt(w), int(w['start']) + 1, int(w['end']) + 2, e(w['label']), e(w['staff'])) for w in b['windows'])
    desk = '<div class="tj-desk"><div class="tj-hl" style="--n:%d"><div class="brs">%s</div><div class="bars">%s</div></div><div class="tj-label" style="margin-top:6px">%s</div></div>' % (n, brackets, cols, e(b['unit']))
    rows, cur = [], None
    for i, x in enumerate(bars):
        wi = inwin.get(i)
        if wi is not None and wi != cur:
            w = b['windows'][wi]
            rows.append('<div class="hdr"%s><b>%s</b><span class="tj-tag" data-status="now">%s</span></div>' % (pt(w), e(w['label']), e(w['staff'])))
        elif wi is None and cur is not None:
            rows.append('<div class="hdr quiet"><b>Other hours</b></div>')
        cur = wi
        rows.append('<div class="row%s"><span>%s</span><i style="width:%.1f%%"></i><em>%s</em></div>' % (' on' if wi is not None else '', e(x['label']), float(x['value']) / mx * 100, e(trim(float(x['value'])))))
    mob = '<div class="tj-mob"><div class="tj-label" style="margin-bottom:6px">%s</div><div class="tj-hlm">%s</div></div>' % (e(b['unit']), ''.join(rows))
    label = '<div class="tj-label">%s</div>' % e(b['label']) if b.get('label') else ''
    return '<section class="tj-block" data-block="hour-load" style="display:flex;flex-direction:column;gap:10px">%s%s%s%s</section>' % (label, desk, mob, divider(b.get('caption')))

def r_was_now(b, ctx):
    arrow = {'up': '▲', 'down': '▼', 'same': ''}
    rows = ''.join(('<div class="wn"%s><div class="l">%s</div><div class="was"><small>I had</small><s>%s</s></div><div class="to" aria-hidden="true">→</div>'
                    '<div class="now"><small>Your number</small><b>%s</b></div><div class="ch">%s</div>%s</div>') % (
        pt(r), e(r['label']), e(r['was']), e(r['now']),
        ('<span class="tj-tag" data-dir="%s">%s</span>' % (e(r.get('direction', 'same')), (arrow.get(r.get('direction', 'same'), '') + ' ' + e(r['change'])).strip())) if r.get('change') else '',
        '<p class="ko">%s</p>' % e(r['knock_on']) if r.get('knock_on') else '') for r in b['rows'])
    return '<section class="tj-block" data-block="was-now" style="display:flex;flex-direction:column;gap:10px"><div class="tj-wn">%s</div>%s</section>' % (rows, divider(b.get('caption')))

def r_scorecard(b, ctx):
    lab = {'confirmed': 'Confirmed', 'pending': 'Not measured yet', 'new': 'New measure'}
    head = '<div class="h">Measure</div><div class="h">Starting number</div><div class="h">Goal</div><div class="h">Status</div>'
    cells = ''.join(('<div class="m"%s>%s%s</div><div class="s">%s</div><div class="g">%s</div><div class="st"><span class="tj-tag" data-sc="%s">%s</span></div>') % (
        pt(r), e(r['measure']), '<small>%s</small>' % e(r['note']) if r.get('note') else '', e(r['start']), e(r['goal']), e(r['status']), e(lab[r['status']])) for r in b['rows'])
    desk = '<div class="tj-desk"><div class="tj-sc">%s%s</div></div>' % (head, cells)
    cards = ''.join(('<div class="opt"%s><div class="t">%s</div><span class="tj-tag" data-sc="%s">%s</span><dl><dt>Starting number</dt><dd>%s</dd><dt>Goal</dt><dd>%s</dd></dl>%s</div>') % (
        pt(r), e(r['measure']), e(r['status']), e(lab[r['status']]), e(r['start']), e(r['goal']), '<p class="tj-text">%s</p>' % e(r['note']) if r.get('note') else '') for r in b['rows'])
    mob = '<div class="tj-mob"><div class="tj-cmpm">%s</div></div>' % cards
    return '<section class="tj-block" data-block="scorecard" style="display:flex;flex-direction:column;gap:10px">%s%s%s</section>' % (desk, mob, divider(b.get('caption')))

def r_narrow_claim(b, ctx):
    li = lambda xs, mark: ''.join('<li>%s<span>%s</span></li>' % (mark, e(x)) for x in xs)
    ask = ''
    if b.get('ask'):
        a = b['ask']
        ask = '<div class="ask"><span class="tj-big">%s</span><div><b>%s</b><p class="tj-text">%s</p></div></div>' % (e(a['value']), e(a['label']), e(a['condition']))
    return ('<section class="tj-block tj-nc" data-block="narrow-claim"><div class="said"><div class="tj-label">What you said</div><p class="q">“%s”</p>'
            '<div class="tj-label" style="margin-top:8px">The part that’s fair</div><p class="tj-text">%s</p></div>'
            '<div class="cols"><div class="col ch"><div class="tj-label">%s</div><ul>%s</ul></div><div class="col kp"><div class="tj-label">%s</div><ul>%s</ul></div></div>%s</section>') % (
        e(b['said']), e(b['fair']), e(b.get('change_title') or 'What changes'), li(b['changes'], TICK),
        e(b.get('keep_title') or 'What stays as it is'), li(b['keeps'], '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" aria-hidden="true"><path d="M5 12h14"/></svg>'), ask)

def r_converge(b, ctx):
    ins = ''.join('<div class="in"%s><div class="t">%s</div>%s</div>' % (pt(x), e(x['title']), '<p class="tj-text">%s</p>' % e(x['text']) if x.get('text') else '') for x in b['inputs'])
    o = b['output']
    out = '<div class="out" data-state="outcome"%s><div class="t">%s</div>%s%s</div>' % (
        pt(o), e(o['title']), '<div class="tj-val">%s</div>' % e(o['value']) if o.get('value') else '', '<p class="tj-text">%s</p>' % e(o['text']) if o.get('text') else '')
    label = '<div class="tj-label">%s</div>' % e(b['label']) if b.get('label') else ''
    rail = '<span class="rl">%s</span>' % e(b['rail_label']) if b.get('rail_label') else ''
    return ('<section class="tj-block" data-block="converge" style="display:flex;flex-direction:column;gap:10px">%s<div class="tj-cv" style="--n:%d"><div class="ins">%s</div>'
            '<div class="rail" aria-hidden="true">%s</div><div class="down" aria-hidden="true"></div>%s</div>%s</section>') % (
        label, len(b['inputs']), ins, rail, out, divider(b.get('caption')))

def r_bands(b, ctx):
    col = lambda o, cls: '<div class="bd %s"><div class="tj-label">%s</div><ul>%s</ul></div>' % (cls, e(o['title']), ''.join('<li>%s</li>' % e(x) for x in o['items']))
    en = b['engine']
    eng = '<div class="bd eng"%s><div class="tj-label">The one thing doing the work</div><div class="t">%s</div><p>%s</p></div>' % (pt(en), e(en['title']), e(en['text']))
    return ('<section class="tj-block" data-block="bands" style="display:flex;flex-direction:column;gap:10px"><div class="tj-bands">%s<span class="arr" aria-hidden="true">→</span>%s'
            '<span class="arr" aria-hidden="true">→</span>%s</div>%s</section>') % (col(b['inputs'], 'in'), eng, col(b['outputs'], 'out'), divider(b.get('caption')))

def r_shared_flow(b, ctx):
    fl = b['flows']; parts = []
    for i, s in enumerate(b['steps']):
        only = s.get('only')
        vals = ''
        if s.get('values'):
            vals = '<div class="vals">%s</div>' % ''.join('<div><small>%s</small><b>%s</b></div>' % (e(fl[k]), e(v)) for k, v in enumerate(s['values']))
        if only is not None:
            other = fl[1 - int(only)]
            parts.append('<div class="box only" data-state="dashed"%s><span class="bypass" aria-hidden="true"><em>Others go straight on</em></span><div class="t">%s</div><div class="only-lab">%s only</div>%s</div>' % (
                pt(s), e(s['title']), e(fl[int(only)]), vals))
        else:
            parts.append('<div class="box" data-state="%s"%s><div class="t">%s</div>%s</div>' % (e(s.get('state') or ('outcome' if i == len(b['steps']) - 1 else 'plain')), pt(s), e(s['title']), vals))
    legend = '<div class="tj-legend"><span><i style="border-radius:3px"></i>Both: %s and %s</span><span><i style="border-radius:3px;border-style:dashed"></i>Only one of them</span></div>' % (e(fl[0]), e(fl[1]))
    return '<section class="tj-block tj-sf" data-block="shared-flow" style="display:flex;flex-direction:column;gap:12px">%s<div class="tj-chain%s">%s</div>%s</section>' % (
        legend, ' long' if len(parts) > 5 else '', '<span class="arr" aria-hidden="true">→</span>'.join(parts), divider(b.get('caption')))

def r_zoom_trail(b, ctx):
    lv = b['levels']; n = len(lv)
    items = ''.join('<li class="%s" style="--d:%d"><small>%s</small><b>%s</b></li>' % ('cur' if i == n - 1 else '', i, e(x.get('ref') or ('Now' if i == n - 1 else 'Level %d' % (i + 1))), e(x['title'])) for i, x in enumerate(lv))
    return '<section class="tj-block" data-block="zoom-trail"><div class="tj-label" style="margin-bottom:8px">Where this answer sits</div><ol class="tj-zt">%s</ol></section>' % items

def r_phases(b, ctx):
    span = int(b['span']); unit = b['unit']
    pc = lambda x: (float(x) - 1) / span * 100
    scale = ''.join('<span><em>%s </em>%d</span>' % (e(unit), i) for i in range(1, span + 1))
    marks = ''.join('<div class="mk" style="left:%.2f%%"><b>%s</b></div>' % (pc(m['at']), e(m['label'])) for m in b.get('marks', []))
    mlines = ''.join('<span class="ml" style="left:%.2f%%"></span>' % pc(m['at']) for m in b.get('marks', []))
    rows = ''
    for p in b['phases']:
        rng = '%s %s' % (e(unit), trim(float(p['start']))) + (('–%s' % trim(float(p['end']))) if float(p['end']) != float(p['start']) else '')
        rows += ('<div class="ph"%s><div class="pl"><b>%s</b><small>%s</small>%s</div><div class="lane">%s<i data-state="%s" style="left:%.2f%%;width:%.2f%%"></i></div></div>') % (
            pt(p), e(p['title']), rng, '<span>%s</span>' % e(p['text']) if p.get('text') else '', mlines, e(p.get('state') or 'plain'), pc(p['start']), (float(p['end']) - float(p['start']) + 1) / span * 100)
    return ('<section class="tj-block" data-block="phases" style="display:flex;flex-direction:column;gap:10px"><div class="tj-ph" style="--span:%d">'
            '<div class="ph head"><div class="pl"></div><div class="lane scale">%s%s</div></div>%s</div>%s</section>') % (span, scale, marks, rows, divider(b.get('caption')))


RENDER = {'heading': r_heading, 'handnote': r_handnote, 'route-map': r_route_map, 'chain': r_chain, 'two-flow': r_two_flow,
          'compare-table': r_compare_table, 'stat-strip': r_stat_strip, 'calculator': r_calculator, 'threshold-gauges': r_threshold_gauges,
          'balance': r_balance, 'progress-trail': r_progress_trail, 'agenda-grid': r_agenda_grid, 'cards': r_cards, 'role-cards': r_role_cards,
          'fill-blank': r_fill_blank, 'fork': r_fork,
          'time-window': r_time_window, 'hour-load': r_hour_load, 'was-now': r_was_now, 'scorecard': r_scorecard, 'narrow-claim': r_narrow_claim,
          'converge': r_converge, 'bands': r_bands, 'shared-flow': r_shared_flow, 'zoom-trail': r_zoom_trail, 'phases': r_phases}

# ---------------------------------------------------------------- plain English
NON_TEXT_KEYS = {'type', 'id', 'formula', 'format', 'source', 'status', 'state', 'mode', 'theme', 'control', 'heavier', 'badge', 'point', 'n', 'canvas',
                 'register', 'tool', 'context', 'subject', 'user_message', 'user_tag', 'user_words', 'selected', 'review'}

def texts(o, path=''):
    if isinstance(o, str):
        yield path, o
    elif isinstance(o, dict):
        for k, v in o.items():
            if k not in NON_TEXT_KEYS:
                yield from texts(v, path + '.' + k if path else k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from texts(v, '%s[%d]' % (path, i))

def plain_check(spec, reg):
    pe = reg.get('plain_english')
    if not pe:
        return []
    allowed = {w.lower() for w in spec.get('turn', {}).get('user_words', [])}
    probs = []
    for part in ('chat', 'canvas'):
        for path, t in texts(spec.get(part, {}), part):
            for ab, plain in pe['abbreviations'].items():
                if ab.lower() not in allowed and re.search(r'\b' + re.escape(ab) + r's?\b', t):
                    probs.append('%s: “%s” — plain English: %s' % (path, ab, plain))
            for w, plain in pe['words'].items():
                if w.lower() not in allowed and re.search(r'\b' + re.escape(w) + r'(?:s|es|d|ed|ing)?\b', t, re.I):
                    probs.append('%s: “%s” — plain English: %s' % (path, w, plain))
            for pat, fix in pe['patterns']:
                if re.search(pat, t):
                    probs.append('%s: “%s” — %s' % (path, re.search(pat, t).group(0), fix))
    return probs

# ---------------------------------------------------------------- validation
FACT_TURNS = {'question', 'data-ask'}
WITHHELD_IN_FACT_TURNS = {'threshold-gauges', 'balance'}

def words(s):
    return len(re.findall(r"[\w₹%’'-]+", str(s)))

def check_slot(path, spec, val, errs, warns):
    t = spec['type']
    if t == 'text':
        if not isinstance(val, str) or not val.strip():
            errs.append('%s: must be non-empty text' % path); return
        mw = spec.get('max_words')
        if mw and words(val) > mw:
            warns.append('%s: %d words, limit %d — cut it (less text is a standing rule)' % (path, words(val), mw))
    elif t == 'enum':
        if val not in spec['values']:
            errs.append('%s: %r not one of %s' % (path, val, spec['values']))
    elif t == 'number':
        if not isinstance(val, (int, float)) or isinstance(val, bool):
            errs.append('%s: must be a number' % path)
    elif t == 'bool':
        if not isinstance(val, bool):
            errs.append('%s: must be true/false' % path)
    elif t == 'list':
        if not isinstance(val, list):
            errs.append('%s: must be a list' % path); return
        if len(val) < spec['min'] or len(val) > spec['max']:
            errs.append('%s: %d items, allowed %d–%d' % (path, len(val), spec['min'], spec['max']))
        for i, v in enumerate(val):
            check_slot('%s[%d]' % (path, i), spec['item'], v, errs, warns)
    elif t == 'object':
        if not isinstance(val, dict):
            errs.append('%s: must be an object' % path); return
        check_fields(path, spec['fields'], val, errs, warns)

def check_fields(path, fields, obj, errs, warns):
    for k, spec in fields.items():
        if k not in obj or obj[k] is None:
            if spec.get('required', True):
                errs.append('%s.%s: required' % (path, k))
            continue
        check_slot('%s.%s' % (path, k), spec, obj[k], errs, warns)
    for k in obj:
        if k not in fields and k not in ('type', 'id'):
            warns.append('%s.%s: unknown slot (ignored)' % (path, k))

def estimate(block, reg_block, narrow):
    c = reg_block.get('cost', {})
    key = 'narrow' if narrow else 'wide'
    h = c.get(key, 100)
    per = c.get('per_item_' + key, 0)
    if per:
        lists = [v for v in block.values() if isinstance(v, list)]
        h += per * (len(lists[0]) if lists else 0)
    h += c.get('detail_' + key, 0)
    return h

def validate(spec, reg=None):
    reg = reg or load_registry()
    by = {b['id']: b for b in reg['blocks']}
    errs, warns = [], []
    turn = spec.get('turn', {})
    ttype = turn.get('type')
    canvas = spec.get('canvas')
    chat = spec.get('chat', {})
    if canvas:
        blocks = canvas.get('blocks', [])
        if not blocks or blocks[0].get('type') != 'heading':
            errs.append('canvas: first block must be "heading"')
        if sum(1 for b in blocks if b.get('type') == 'heading') > 1:
            errs.append('canvas: only one heading')
        body = [b for b in blocks if b.get('type') not in ('heading',)]
        if len(body) > reg['budget']['max_blocks']:
            errs.append('canvas: %d blocks after the heading, limit %d — split across turns or put detail behind expanders' % (len(body), reg['budget']['max_blocks']))
        if sum(1 for b in blocks if b.get('type') == 'handnote') > 1:
            errs.append('canvas: at most one handnote')
        tones = reg.get('tones', {})
        if canvas.get('tone'):
            if canvas['tone'] not in tones.get('list', {}):
                errs.append('canvas.tone: unknown %r' % canvas['tone'])
            else:
                warns.append('canvas.tone is set by hand — only do this for a fill-in-the-blank redraw; the generator picks the shade from the turn number')
                if tones['list'][canvas['tone']].get('status') != 'approved':
                    errs.append('canvas.tone %r is %s' % (canvas['tone'], tones['list'][canvas['tone']].get('status')))
        if canvas.get('theme') and canvas['theme'] != 'sage':
            errs.append('canvas.theme: only “sage” exists; shades come from the turn number')

        wide = narrow = 0
        for i, b in enumerate(blocks):
            t = b.get('type')
            path = 'canvas.blocks[%d](%s)' % (i, t)
            if t not in by:
                errs.append('%s: unknown block type' % path); continue
            rb = by[t]
            if rb['status'] in ('changes_requested', 'retired'):
                errs.append('%s: block status is %s — do not select' % (path, rb['status']))
            elif rb['status'] == 'draft':
                warns.append('%s: block is draft (not yet approved)' % path)
            if ttype in FACT_TURNS and t in WITHHELD_IN_FACT_TURNS:
                errs.append('%s: not allowed in a %s turn — a threshold or cost/return is a recommendation; withhold it (05 §4)' % (path, ttype))
            check_fields(path, rb['slots'], b, errs, warns)
            if t == 'calculator':
                ids = {x['id'] for x in b.get('inputs', [])}
                for s in b.get('steps', []):
                    names = set(re.findall(r'[A-Za-z_][A-Za-z0-9_]*', s.get('formula', ''))) - {'min', 'max', 'round'}
                    bad = names - ids
                    if bad:
                        errs.append('%s: formula for %s uses unknown names %s' % (path, s.get('id'), sorted(bad)))
                    ids.add(s.get('id'))
                for x in b.get('inputs', []):
                    if x.get('source') == 'estimate' and ttype in FACT_TURNS:
                        errs.append('%s: input %s is your estimate in a fact-collecting turn — ask for it (source "needed") instead of inventing it' % (path, x.get('id')))
                    if x.get('value') is None and x.get('source') != 'needed':
                        errs.append('%s: input %s has no value — its source must be "needed"' % (path, x.get('id')))
            wide += estimate(b, rb, False) + (20 if i else 0)
            narrow += estimate(b, rb, True) + (18 if i else 0)
        wide += 50; narrow += 42     # canvas padding
        if wide > reg['budget']['wide_px']:
            warns.append('canvas: estimated desktop height %dpx > %dpx (one screen). Move detail behind expanders or into the next turn.' % (wide, reg['budget']['wide_px']))
        if narrow > reg['budget']['narrow_px']:
            warns.append('canvas: estimated mobile height %dpx > %dpx.' % (narrow, reg['budget']['narrow_px']))
        spec.setdefault('_estimate', {})['wide_px'] = wide
        spec['_estimate']['narrow_px'] = narrow
        canvas_points = set()
        def walk(o):
            if isinstance(o, dict):
                if 'point' in o and o['point'] is not None: canvas_points.add(int(o['point']))
                for v in o.values(): walk(v)
            elif isinstance(o, list):
                for v in o: walk(v)
        walk(blocks)
    errs += ['plain English: ' + p for p in plain_check(spec, reg)]
    # chat panel (written by Claude)
    prompts = chat.get('prompts', [])
    if len(prompts) != 3:
        errs.append('chat.prompts: exactly 3 predictive prompts, got %d' % len(prompts))
    pts = chat.get('points', [])
    if pts and not (2 <= len(pts) <= 6):
        errs.append('chat.points: 2–6 points, got %d' % len(pts))
    for i, p in enumerate(pts):
        if p.get('n') != i + 1:
            errs.append('chat.points[%d].n must be %d' % (i, i + 1))
        if canvas and p.get('canvas') and p['n'] not in canvas_points:
            warns.append('chat.points[%d]: says it links to the canvas but no canvas item has point %d' % (i, p['n']))
    if chat.get('note') and words(chat['note']) > 16:
        warns.append('chat.note: %d words, keep Tojo’s Note to one line (≤16)' % words(chat['note']))
    text = chat.get('text', '')
    tw = words(' '.join(text) if isinstance(text, list) else text) + sum(words(b) for b in chat.get('bullets', []))
    if tw > 150:
        warns.append('chat.text: %d words, most turns sit under 150 (05 §2)' % tw)
    for k in ('pointer', 'invite'):
        if chat.get(k) and re.search(r'\b(left|right|above|below|sidebar)\b', chat[k], re.I):
            errs.append('chat.%s: says where the canvas is ("left/above…") — the canvas is beside the chat on desktop and above it on mobile; point at it by name instead' % k)
    q = chat.get('question')
    if q:
        if not (2 <= len(q.get('options', [])) <= 5):
            errs.append('chat.question.options: 2–5 options')
        if ttype and ttype != 'question' and ttype != 'data-ask':
            warns.append('chat.question present in a %s turn' % ttype)
    if not canvas and ttype not in ('question', 'data-ask', 'scripted'):
        warns.append('no canvas: most turns can carry one honestly (05 §1)')
    return errs, warns

# ---------------------------------------------------------------- rendering
def asset(name):
    with open(os.path.join(ASSETS, name), encoding='utf-8') as f:
        return f.read()

def render_canvas(spec, reg=None):
    ctx = Ctx()
    canvas = spec['canvas']
    body = ''.join(RENDER[b['type']](b, ctx) for b in canvas['blocks'])
    turn = spec.get('turn', {})
    return '<div class="tj" data-theme="sage" data-tone="%s" data-turn="%s" data-generator="diagnosis_html %s"><div class="tj-stack">%s</div></div>' % (
        e(tone_name(spec)), e(turn.get('id', '')), GEN_VERSION, body)

def tone_name(spec, reg=None):
    """The colour is a rule, not stored content: tone comes from the turn number (sets of three through tones.rotation).
    canvas.tone is only an override, for a fill-in-the-blank redraw that must keep its first tone."""
    reg = reg or load_registry()
    tones = reg.get('tones', {})
    if spec.get('canvas', {}).get('tone'):
        return spec['canvas']['tone']
    rot = tones.get('rotation', ['sage'])
    m = re.search(r'(\d+)', spec.get('turn', {}).get('id', ''))
    return rot[((int(m.group(1)) - 1) // 3) % len(rot)] if m else rot[0]

def tone_of(spec, reg=None):
    reg = reg or load_registry()
    return reg.get('tones', {}).get('list', {}).get(tone_name(spec, reg), {'ground': '#DCE3DA'})

FONT_FILES = [('Bebas Neue', 400, 'normal', 'bebas-neue-latin-400-normal.woff2'), ('Caveat', 500, 'normal', 'caveat-latin-500-normal.woff2'),
              ('Caveat', 700, 'normal', 'caveat-latin-700-normal.woff2'), ('Poppins', 400, 'italic', 'poppins-latin-400-italic.woff2')] + \
             [('Poppins', w, 'normal', 'poppins-latin-%d-normal.woff2' % w) for w in (400, 500, 600, 700)]
FONT_MODE = os.environ.get('TOJO_FONTS', 'embed')   # embed = fully offline (default) · google = link to Google Fonts · none = host page supplies them

def font_css():
    if FONT_MODE != 'embed':
        return ''
    import base64
    out = []
    for fam, w, style, fn in FONT_FILES:
        p = os.path.join(ASSETS, 'fonts', fn)
        if os.path.exists(p):
            with open(p, 'rb') as fh:
                b64 = base64.b64encode(fh.read()).decode('ascii')
            out.append("@font-face{font-family:'%s';font-weight:%d;font-style:%s;font-display:swap;src:url(data:font/woff2;base64,%s) format('woff2')}" % (fam, w, style, b64))
    return '\n'.join(out)

def page(title, body, extra_css='', extra_js=''):
    return ('<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">'
            '<title>%s</title>%s<style>%s\n%s\n%s</style></head><body style="margin:0">%s<script>%s\n%s</script></body></html>\n') % (
        e(title), FONTS if FONT_MODE == 'google' else '', font_css(), asset('tojo.css'), extra_css, body, asset('tojo.js'), extra_js)

def render_page(spec, view='canvas'):
    canvas_html = render_canvas(spec) if spec.get('canvas') else ''
    title = spec.get('canvas', {}).get('blocks', [{}])[0].get('title', 'Tojo')
    if view == 'canvas':
        return page(title, canvas_html)
    from preview import desktop_shell, mobile_shell, SHELL_CSS, SHELL_JS
    shell = desktop_shell if view == 'desktop' else mobile_shell
    return page(title, shell(spec, canvas_html), SHELL_CSS, SHELL_JS)

# ---------------------------------------------------------------- gallery / catalog / feedback
def scope_badge(scope, drawn_in):
    """The block library marks every template: a universal pattern, or one place only."""
    if scope in (None, 'all'):
        return '<span class="g-scope g-scope-all" title="Any place may use this pattern, redrawn in its own look by its own generator">Universal pattern · drawn here for %s</span>' % e(drawn_in)
    return '<span class="g-scope g-scope-one" title="Only %s uses this template">%s only</span>' % (e(scope), e(scope))

def gallery(reg, only=None, title='Tojo block library', intro=None, blocks_only=None):
    with open(SAMPLES_PATH, encoding='utf-8') as f:
        samples = json.load(f)
    ctx = Ctx()
    rows = []
    for rb in reg['blocks']:
        if blocks_only and rb['id'] not in blocks_only:
            continue
        smp = samples.get(rb['id'])
        if not smp:
            continue
        blk = dict(smp, type=rb['id'])
        inner = RENDER[rb['id']](blk, ctx)
        errs, warns = [], []
        check_fields(rb['id'], rb['slots'], blk, errs, warns)
        badge = {'approved': '#2f7350', 'draft': '#B8862B', 'changes_requested': '#8E2F1C', 'retired': '#777'}[rb['status']]
        last = rb.get('feedback', [])[-1]['note'] if rb.get('feedback') else 'No feedback yet.'
        rows.append('''<section class="g-row" id="%s">
  <div class="g-meta"><div class="g-id">%s <span>v%d</span></div><div><span class="g-status" style="background:%s">%s</span> %s</div>
    <p><b>%s.</b> %s</p><p class="g-small"><b>Use when:</b> %s<br><b>Avoid when:</b> %s<br><b>Mobile:</b> %s</p><p class="g-small"><b>Last feedback:</b> %s</p>%s</div>
  <div class="g-views"><div><div class="g-cap">Desktop canvas · 864px</div><div class="tj" data-theme="sage" style="width:864px"><div class="tj-stack">%s</div></div></div>
  <div><div class="g-cap">Mobile canvas · 362px</div><div class="tj" data-theme="sage" style="width:362px"><div class="tj-stack">%s</div></div></div></div>
</section>''' % (rb['id'], rb['id'], rb['version'], badge, rb['status'].replace('_', ' '), scope_badge(rb.get('scope', 'all'), 'Diagnosis'), rb['category'].capitalize(), e(rb['purpose']),
                 e('; '.join(rb['use_when'])), e('; '.join(rb['avoid_when'])), e(rb.get('mobile', 'same layout, reflowed')), e(last),
                 '<p class="g-small" style="color:#8E2F1C">%s</p>' % e('; '.join(errs)) if errs else '', inner, RENDER[rb['id']](blk, ctx)))
    from preview import chat_parts, user_msg, SHELL_CSS
    turns = []
    ex_dir = os.path.join(ROOT, 'examples')
    files = only or [os.path.join(ex_dir, fn) for fn in (sorted(os.listdir(ex_dir)) if os.path.isdir(ex_dir) else []) if fn.endswith('.json')]
    for path in files:
        with open(path, encoding='utf-8') as fh:
            spec = json.load(fh)
        errs, warns = validate(spec, reg)
        est = spec.get('_estimate', {})
        cv = render_canvas(spec)
        rv = spec.get('review', {})
        badge = '<span class="g-status" style="background:%s">%s</span>' % ('#2f7350' if rv.get('status') == 'approved' else '#B8862B', e(rv.get('status', 'draft'))) + ('<p class="g-small">%s</p>' % e(rv['note']) if rv.get('note') else '')
        turns.append('''<section class="g-row" id="%s"><div class="g-meta"><div class="g-id">%s <span>%s turn</span></div>%s
  <p class="g-small">Estimated canvas height: desktop ~%spx of 824 · mobile ~%spx of 1500. %s</p><p class="g-small">%s</p></div>
  <div class="g-views"><div><div class="g-cap">Desktop canvas · 864px</div><div style="width:864px">%s</div></div>
  <div><div class="g-cap">Chat panel (written by Claude)</div><div class="sh-panel" style="width:380px"><div class="sh-pb">%s%s</div></div></div>
  <div><div class="g-cap">Mobile canvas · 362px</div><div style="width:362px">%s</div></div></div></section>''' % (
            spec['turn']['id'], e(spec['turn']['id']), e(spec['turn']['type']), badge, est.get('wide_px', '?'), est.get('narrow_px', '?'),
            'Valid.' if not errs else 'ERRORS: ' + e('; '.join(errs)), e(' · '.join(warns)), cv, user_msg(spec), chat_parts(spec['chat']), cv))
    toc = ''.join('<a href="#%s">%s</a>' % (b['id'], b['id']) for b in reg['blocks'])
    css = '''body{background:#EEF1EC;font-family:Poppins,system-ui,sans-serif;color:#10241a}
.g-top{padding:28px 32px 8px}.g-top h1{font-family:'Bebas Neue',sans-serif;font-weight:400;font-size:56px;margin:0;line-height:1}
.g-top p{max-width:760px;font-size:15px;line-height:1.55;color:#44544A}.g-toc{display:flex;flex-wrap:wrap;gap:8px;padding:0 32px 20px}
.g-toc a{font-size:13px;padding:6px 12px;border:1.5px solid #10241a;border-radius:16px;color:#10241a;text-decoration:none}
.g-row{margin:0 32px 36px;padding-top:24px;border-top:2px solid #10241a;display:flex;flex-direction:column;gap:18px}.g-meta{max-width:1260px;display:grid;grid-template-columns:260px 1fr 1fr;gap:4px 28px;align-items:start}.g-meta>*{margin:0!important}
.g-id{font-family:'Bebas Neue',sans-serif;font-size:34px;line-height:1}.g-id span{font-family:Poppins;font-size:13px;color:#44544A}
.g-scope{justify-self:start;align-self:start;display:inline-block;margin:8px 0 8px 6px;padding:2px 10px;border-radius:12px;font-size:12px;font-weight:600;border:1.5px solid #10241a;color:#10241a;background:#fff}
.g-scope-one{background:#10241a;color:#F3F1EA}
.g-status{justify-self:start;display:inline-block;margin:8px 0;padding:3px 10px;border-radius:12px;color:#fff;font-size:12px;font-weight:600;text-transform:uppercase;letter-spacing:.08em}
.g-meta p{font-size:14px;line-height:1.5;margin:6px 0}.g-small{font-size:13px!important;color:#44544A}
.g-views{display:flex;gap:24px;align-items:flex-start;overflow-x:auto}.g-cap{font-size:12px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;margin-bottom:6px;color:#44544A}
@media (max-width:1100px){.g-meta{grid-template-columns:1fr}}'''
    if blocks_only:
        toc = ''.join('<a href="#%s">%s</a>' % (x, x) for x in blocks_only)
        body = '<div class="g-top"><h1>%s</h1><p>%s</p></div><div class="g-toc">%s</div>%s' % (e(title), e(intro or ''), toc, ''.join(rows))
        return page(title, body, css + SHELL_CSS)
    if only:
        body = '<div class="g-top"><h1>%s</h1><p>%s</p></div>%s' % (e(title), e(intro or ''), ''.join(turns))
        return page(title, body, css + SHELL_CSS + '.g-views .sh-panel{border-radius:18px}')
    body = ('<div class="g-top"><h1>Tojo block library</h1><p>Registry v%d · %s · %d blocks. Each block is shown at the desktop canvas width and the mobile canvas width from the same markup. '
            'Approve or request changes by block id; the registry keeps the log. Sample turns come first, built by the generator from the specs in examples/.</p></div>'
            '<div class="g-toc"><a href="#sample-turns" style="background:#10241a;color:#F3F1EA">Sample turns</a>%s</div><div id="sample-turns">%s</div>%s') % (
        reg['registry_version'], reg['updated'], len(reg['blocks']), toc, ''.join(turns), ''.join(rows))
    return page('Tojo block library', body, css + SHELL_CSS + '.g-views .sh-panel{border-radius:18px}')

def catalog(reg):
    out = ['# Tojo canvas blocks — catalogue (registry v%d, %s)\n' % (reg['registry_version'], reg['updated']),
           'Budget: desktop ≈%dpx, mobile ≈%dpx, at most %d blocks after the heading. Status "changes_requested" or "retired" = never select.\n' % (
               reg['budget']['wide_px'], reg['budget']['narrow_px'], reg['budget']['max_blocks'])]
    def slot_sig(fields):
        parts = []
        for k, s in fields.items():
            opt = '' if s.get('required', True) else '?'
            if s['type'] == 'list':
                inner = s['item']
                desc = '[%s]' % (slot_sig(inner['fields']) if inner['type'] == 'object' else inner['type'])
                parts.append('%s%s: %s(%d–%d)' % (k, opt, desc, s['min'], s['max']))
            elif s['type'] == 'object':
                parts.append('%s%s: {%s}' % (k, opt, slot_sig(s['fields'])))
            elif s['type'] == 'enum':
                parts.append('%s%s: %s' % (k, opt, '|'.join(s['values'])))
            else:
                parts.append('%s%s: %s%s' % (k, opt, s['type'], '≤%dw' % s['max_words'] if s.get('max_words') else ''))
        return ', '.join(parts)
    for b in reg['blocks']:
        if b['status'] in ('retired',):
            continue
        out.append('## %s  (%s, %s)\n%s\n- use when: %s\n- avoid when: %s\n- slots: %s\n' % (
            b['id'], b['category'], b['status'], b['purpose'], '; '.join(b['use_when']), '; '.join(b['avoid_when']), slot_sig(b['slots'])))
    return '\n'.join(out)

def feedback(reg, block_id, verdict, note, by='user'):
    b = next((x for x in reg['blocks'] if x['id'] == block_id), None)
    if not b:
        sys.exit('no block %r' % block_id)
    b.setdefault('feedback', []).append({'date': datetime.date.today().isoformat(), 'by': by, 'verdict': verdict, 'note': note})
    if verdict in ('approved', 'changes_requested', 'retired', 'draft'):
        b['status'] = verdict
    reg['updated'] = datetime.date.today().isoformat()
    with open(REG_PATH, 'w', encoding='utf-8') as f:
        json.dump(reg, f, indent=1, ensure_ascii=False)
    return b

def main():
    ap = argparse.ArgumentParser(description='Tojo offline HTML generator')
    sub = ap.add_subparsers(dest='cmd', required=True)
    r = sub.add_parser('render'); r.add_argument('spec'); r.add_argument('-o', '--out'); r.add_argument('--view', default='canvas', choices=['canvas', 'desktop', 'mobile'])
    r.add_argument('--strict', action='store_true', help='treat warnings as errors')
    v = sub.add_parser('validate'); v.add_argument('spec')
    g = sub.add_parser('gallery'); g.add_argument('-o', '--out', default='gallery.html')
    rv = sub.add_parser('review', help='a review page for chosen turns only'); rv.add_argument('specs', nargs='+'); rv.add_argument('-o', '--out', required=True)
    rv.add_argument('--title', default='Tojo — turns for review'); rv.add_argument('--intro', default='')
    nb = sub.add_parser('blocks', help='a review page for chosen blocks only'); nb.add_argument('ids', nargs='+'); nb.add_argument('-o', '--out', required=True)
    nb.add_argument('--title', default='Tojo — templates for review'); nb.add_argument('--intro', default='')
    sub.add_parser('catalog')
    pr = sub.add_parser('prompt', help='print the full API system-prompt section: rules + contract + live catalogue')
    f = sub.add_parser('feedback'); f.add_argument('block'); f.add_argument('verdict', choices=['approved', 'changes_requested', 'retired', 'draft', 'note']); f.add_argument('note')
    a = ap.parse_args()
    reg = load_registry()
    if a.cmd in ('render', 'validate'):
        with open(a.spec, encoding='utf-8') as fh:
            spec = json.load(fh)
        errs, warns = validate(spec, reg)
        for w in warns: print('warning:', w, file=sys.stderr)
        for x in errs: print('ERROR:', x, file=sys.stderr)
        est = spec.get('_estimate')
        if est: print('estimate: desktop ~%(wide_px)dpx, mobile ~%(narrow_px)dpx' % est, file=sys.stderr)
        if errs or (getattr(a, 'strict', False) and warns):
            sys.exit(1)
        if a.cmd == 'render':
            out = render_page(spec, a.view)
            if a.out:
                with open(a.out, 'w', encoding='utf-8') as fh: fh.write(out)
                print('wrote', a.out, file=sys.stderr)
            else:
                sys.stdout.write(out)
    elif a.cmd == 'gallery':
        with open(a.out, 'w', encoding='utf-8') as fh: fh.write(gallery(reg))
        print('wrote', a.out, file=sys.stderr)
    elif a.cmd == 'blocks':
        with open(a.out, 'w', encoding='utf-8') as fh: fh.write(gallery(reg, title=a.title, intro=a.intro, blocks_only=a.ids))
        print('wrote', a.out, file=sys.stderr)
    elif a.cmd == 'review':
        with open(a.out, 'w', encoding='utf-8') as fh: fh.write(gallery(reg, only=a.specs, title=a.title, intro=a.intro))
        print('wrote', a.out, file=sys.stderr)
    elif a.cmd == 'catalog':
        print(catalog(reg))
    elif a.cmd == 'prompt':
        with open(os.path.join(ROOT, 'prompts', 'tojo-api-system-prompt.md'), encoding='utf-8') as fh:
            tpl = re.sub(r'<!--.*?-->\s*', '', fh.read(), flags=re.S)
        with open(os.path.join(ROOT, 'rules', '06-html-response-rules.md'), encoding='utf-8') as fh:
            rules = fh.read()
        print(tpl.replace('{{RULES_06}}', rules).replace('{{CATALOG}}', catalog(reg)))
    elif a.cmd == 'feedback':
        b = feedback(reg, a.block, a.verdict, a.note)
        print('%s → %s (%d feedback entries)' % (b['id'], b['status'], len(b['feedback'])))

if __name__ == '__main__':
    main()
