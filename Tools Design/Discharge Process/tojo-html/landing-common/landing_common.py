"""
landing_common: the parts every tab landing page shares, whichever tab generator draws it.

A landing page is a canvas like any other turn, with the chat panel beside it (desktop) or
under it (mobile). Every landing page carries the same five zones, in the same order, so
the pages feel like one family even though each tab draws them in its own way:

  1. masthead   the tab's emblem, its name, and the update stamp with "Refresh now"
  2. standing   one plain sentence on where this tab stands
  3. progress   the tab's own drawing of what has happened so far
  4. pending    what Tojo still has to do here (some items wait on a figure from you)
  5. actions    Proceed with next step · Add more · Jump to the next tab

Each page has two states: "filled" (the user has talked to Tojo) and "empty" (first visit).
The stamp says when the page was last brought up to date: every night at midnight, or when
the user presses Refresh now.

This module builds three outputs from one render function per sample:
  - a plain HTML preview in the app shell (fonts embedded, works offline)
  - a design-canvas artboard (.dc.html) with a state switch and working buttons
Standard library only.
"""
import base64, html, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DIAG = os.path.join(ROOT, 'diagnosis-html-generator')
sys.path.insert(0, DIAG)
from preview import SHELL_CSS, TABS, ico, CLIP, MIC, SEND, SHEET, HOME  # noqa: E402

e = lambda s: html.escape('' if s is None else str(s), quote=True)
TAB_ORDER = ['Diagnosis', 'Solutions', 'Automations', 'Processes']
GOOGLE_FONTS = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bebas+Neue&amp;family=Poppins:ital,wght@0,400;0,500;0,600;0,700;1,400'
                '&amp;family=Caveat:wght@500;700&amp;display=swap">')

def embedded_fonts():
    d = os.path.join(DIAG, 'assets', 'fonts')
    faces = [('Bebas Neue', 'bebas-neue-latin-400-normal', 400, 'normal'), ('Poppins', 'poppins-latin-400-normal', 400, 'normal'),
             ('Poppins', 'poppins-latin-400-italic', 400, 'italic'), ('Poppins', 'poppins-latin-500-normal', 500, 'normal'),
             ('Poppins', 'poppins-latin-600-normal', 600, 'normal'), ('Poppins', 'poppins-latin-700-normal', 700, 'normal'),
             ('Caveat', 'caveat-latin-500-normal', 500, 'normal'), ('Caveat', 'caveat-latin-700-normal', 700, 'normal')]
    out = []
    for fam, fn, w, st in faces:
        b = base64.b64encode(open(os.path.join(d, fn + '.woff2'), 'rb').read()).decode()
        out.append("@font-face{font-family:'%s';src:url(data:font/woff2;base64,%s) format('woff2');font-weight:%d;font-style:%s;font-display:swap}" % (fam, b, w, st))
    return '<style>%s</style>' % ''.join(out)

# ---------------------------------------------------------------------------------------------
# Mode: the same render function writes plain HTML or design-canvas markup.
class Mode:
    def __init__(self, kind, state, data):
        self.kind, self.state, self.data = kind, state, data     # kind: 'html' | 'dc'
        self.d = data[state]
    @property
    def dc(self): return self.kind == 'dc'
    def pt(self, n):
        """Attributes that let a chat @Point light this item up."""
        if n is None: return ''
        return ' data-pt="%d"%s' % (n, ' data-lit="{{lit%d}}"' % n if self.dc else '')
    def stamp(self):
        s = self.d['stamp']
        if self.dc:
            t, since = '{{stamp}}', '{{since}}'
            btn = '<button class="lp-refresh" type="button" onClick="{{refresh}}">%s<span>Refresh now</span></button>' % REFRESH_ICO
        else:
            t, since = e(s['at']), e(s['since'])
            btn = '<button class="lp-refresh" type="button" data-fresh="%s" data-fresh-since="%s">%s<span>Refresh now</span></button>' % (e(s['fresh']), e(s['fresh_since']), REFRESH_ICO)
        return ('<div class="lp-stamp"><div class="lp-stamp-txt"><span class="lp-stamp-at">%s</span><span class="lp-stamp-since">%s</span></div>%s</div>' % (t, since, btn))
    def actions(self, cls=''):
        a = self.d['actions']
        def b(kind, key, head, detail):
            click = ' onClick="{{act_%s}}"' % key if self.dc else ' data-text="%s"' % e(a[key]['say'])
            return ('<button class="lp-act lp-act-%s" type="button"%s><span class="lp-act-k">%s</span><span class="lp-act-d">%s</span></button>' % (
                kind, click, e(head), e(detail)))
        return ('<nav class="lp-acts %s" aria-label="What to do next">%s%s%s</nav>' % (cls,
                b('go', 'go', 'Proceed with next step', a['go']['detail']),
                b('add', 'add', 'Add more', a['add']['detail']),
                b('jump', 'jump', 'Jump to ' + a['jump']['tab'], a['jump']['detail'])))

REFRESH_ICO = ('<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
               '<path d="M20 11a8 8 0 10-2.3 5.7"/><path d="M20 4v7h-7"/></svg>')

# ---------------------------------------------------------------------------------------------
# Chat panel (unchanged Tojo design): text, Tojo's note, points, three prompts.
def chat_html(c):
    paras = ''.join('<p>%s</p>' % e(t) for t in c['text'])
    if c.get('pointer'): paras += '<p>%s</p>' % e(c['pointer'])
    out = ['<div class="sh-tm">%s</div>' % paras,
           '<div><div class="sh-lab" style="margin-bottom:4px">Tojo’s note</div><p class="sh-note">%s</p></div>' % e(c['note'])]
    if c.get('points'):
        out.append('<div class="sh-col"><div class="sh-lab">Add to a point — pick one or more</div>%s</div>' % ''.join(
            '<button class="sh-pt" aria-pressed="false" data-n="%d"><i>P%d</i><span>%s</span></button>' % (p['n'], p['n'], e(p['label'])) for p in c['points']))
    out.append('<div class="sh-col"><div class="sh-lab">Or ask next</div>%s</div>' % ''.join(
        '<button class="sh-pr" data-text="%s">%s%s</button>' % (e(p), e(p), ico(SEND, '#d4a94f', 16)) for p in c['prompts']))
    return ''.join(out)

def chat_dc(data):
    def txt(c):
        paras = ''.join('<p>%s</p>' % e(t) for t in c['text'])
        if c.get('pointer'): paras += '<p>%s</p>' % e(c['pointer'])
        return ('<div class="sh-tm">%s</div><div><div class="sh-lab" style="margin-bottom:4px">Tojo’s note</div><p class="sh-note">%s</p></div>' % (paras, e(c['note'])))
    np = max(len(data['filled']['chat'].get('points', [])), 1)
    return ('<sc-if value="{{filled}}" hint-placeholder-val="{{ true }}">%s</sc-if><sc-if value="{{empty}}" hint-placeholder-val="{{ false }}">%s</sc-if>'
            '<sc-if value="{{hasPoints}}" hint-placeholder-val="{{ true }}"><div class="sh-col"><div class="sh-lab">Add to a point — pick one or more</div>'
            '<sc-for list="{{points}}" as="p" hint-placeholder-count="%d"><button class="sh-pt" aria-pressed="{{p.pressed}}" onClick="{{p.toggle}}"><i>P{{p.n}}</i><span>{{p.label}}</span></button></sc-for></div></sc-if>'
            '<div class="sh-col"><div class="sh-lab">Or ask next</div><sc-for list="{{prompts}}" as="q" hint-placeholder-count="3"><button class="sh-pr" onClick="{{q.use}}">{{q.t}}%s</button></sc-for></div>') % (
        txt(data['filled']['chat']), txt(data['empty']['chat']), np, ico(SEND, '#d4a94f', 16))

# ---------------------------------------------------------------------------------------------
# App shell with the current tab marked.
RAIL_COLS = ['#E3E6DF', '#EDE3CB', '#DDE3DE', '#E8E1D4', '#D9DDD6']; RAIL_HS = [136, 124, 124, 140, 128]
LP_SHELL_CSS = '''
.sh-rail a.sh-tab{width:60px;border-radius:0 12px 12px 0;color:#10241a;writing-mode:vertical-rl;transform:rotate(180deg);display:flex;align-items:center;justify-content:center;text-decoration:none;font-size:13px;font-weight:600;letter-spacing:.09em;text-transform:uppercase}
.sh-rail a.sh-tab[aria-current=page]{width:70px;font-weight:700}
.sh-mf a[aria-current=page]{box-shadow:inset 0 3px 0 #d4a94f}
.sh-mid main{flex-grow:1}
body{margin:0}
[data-lit="true"],.lp .is-lit{outline:4px solid #d4a94f !important;outline-offset:3px}
'''

def rail(tab, theme, dc):
    home = 'Main.dc.html' if dc else '#'
    items = []
    for (n, _), c, h in zip(TABS, RAIL_COLS, RAIL_HS):
        if n == tab:
            items.append('<a class="sh-tab" href="#" aria-current="page" style="height:%dpx;background:%s;color:%s">%s</a>' % (h + 16, theme['rail_bg'], theme['rail_fg'], n))
        else:
            items.append('<a class="sh-tab" href="#" style="height:%dpx;background:%s">%s</a>' % (h, c, n))
    return '<nav class="sh-rail" aria-label="Sections"><a class="sh-home" href="%s" aria-label="Home">%s</a>%s</nav>' % (home, ico(HOME, '#d4a94f', 22), ''.join(items))

def input_desktop(dc):
    val = ' value="{{draft}}" onChange="{{onDraft}}"' if dc else ''
    return ('<div class="sh-inp"><label for="tojo-input" style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)">Message Tojo</label>'
            '<textarea id="tojo-input" rows="2" placeholder="Write to Tojo…"%s></textarea>'
            '<div style="display:flex;align-items:center"><button class="sh-ib" aria-label="Attach a file">%s</button><button class="sh-ib" aria-label="Attach a spreadsheet">%s</button>'
            '<button class="sh-ib" aria-label="Voice note">%s</button><span style="flex-grow:1"></span><button class="sh-send" aria-label="Send">%s</button></div></div>') % (
        val, ico(CLIP), ico(SHEET), ico(MIC), ico(SEND, '#10241a'))

def desktop(tab, theme, canvas, chat, dc, height):
    bar = ('<header class="sh-bar"><div><span class="sh-t">Discharge Process</span><small>%s</small></div>'
           '<div style="display:flex;gap:10px"><button class="sh-btn-o">Guided tour</button><button class="sh-btn-g">Your tasks for the day</button></div></header>') % e(tab)
    panel = ('<aside class="sh-chat" aria-label="Chat with Tojo"><div class="sh-panel"><div class="sh-ph"><div class="sh-av">T</div><div>'
             '<div style="font-family:\'Bebas Neue\',sans-serif;font-size:28px;line-height:1">Tojo</div><div style="font-size:12px;color:#9CA9A1">250-bed hospital, Bhubaneswar</div></div></div>'
             '<div class="sh-pb">%s</div>%s</div></aside>') % (chat, input_desktop(dc))
    size = 'width:1440px;height:%dpx;' % height if dc else ''
    return '<div class="sh-app" style="%sbackground:%s">%s<div class="sh-mid">%s<main>%s</main></div>%s</div>' % (size, theme['ground'], rail(tab, theme, dc), bar, canvas, panel)

def mobile(tab, theme, canvas, chat, dc, height):
    val = ' value="{{draft}}" onChange="{{onDraft}}"' if dc else ''
    top = ('<div class="sh-mt"><div style="display:flex;align-items:center;gap:10px"><a href="#" aria-label="Home" style="width:44px;height:44px;border-radius:50%%;background:#10241a;display:flex;align-items:center;justify-content:center">%s</a>'
           '<div><div style="font-family:\'Bebas Neue\',sans-serif;font-size:24px;line-height:1">Virevo</div><div style="font-size:12px;color:#44544A">Discharge Process · %s</div></div></div><button class="sh-btn-o">Tour</button></div>') % (ico(HOME, '#d4a94f', 20), e(tab))
    who = '<div class="sh-who"><span class="sh-av" style="width:30px;height:30px;font-size:17px">T</span>Tojo</div>'
    inp = ('<div class="sh-mi" style="position:static"><div class="sh-box"><label for="tojo-input" style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)">Message Tojo</label>'
           '<input id="tojo-input" placeholder="Write to Tojo…"%s><button class="sh-ib" style="width:40px;height:40px" aria-label="Attach a file">%s</button>'
           '<button class="sh-ib" style="width:40px;height:40px;border-radius:50%%;background:rgba(16,36,26,.08)" aria-label="Voice note">%s</button></div>'
           '<button class="sh-send" aria-label="Send">%s</button></div>') % (val, ico(CLIP, '#10241a', 19), ico(MIC, '#10241a', 19), ico(SEND, '#10241a'))
    foot = '<nav class="sh-mf" style="position:static" aria-label="Sections">%s</nav>' % ''.join(
        '<a href="#" aria-label="%s"%s>%s</a>' % (n, ' aria-current="page"' if n == tab else '', ico(d, '#d4a94f' if n == tab else '#F3F1EA', 22)) for n, d in TABS)
    size = 'height:%dpx;' % height if dc else ''
    return ('<div class="sh-m" style="%sbackground:%s">%s<div class="sh-mc">%s%s<div class="sh-mpanel">%s</div></div>%s%s</div>') % (
        size, theme['ground'], top, who, canvas, chat, inp, foot)

# ---------------------------------------------------------------------------------------------
PLAIN_JS = r'''
(function(){
  var input=document.getElementById('tojo-input');
  var pts=[].slice.call(document.querySelectorAll('.sh-pt'));
  function sel(){return pts.filter(function(p){return p.getAttribute('aria-pressed')==='true';}).map(function(p){return p.getAttribute('data-n');});}
  function tags(){return sel().map(function(n){return '@Point'+n;}).join(' ');}
  function say(t){var g=tags();input.value=(g?g+' ':'')+t;input.focus();}
  pts.forEach(function(p){p.addEventListener('click',function(){
    p.setAttribute('aria-pressed',p.getAttribute('aria-pressed')==='true'?'false':'true');
    var s=sel();[].slice.call(document.querySelectorAll('.lp [data-pt]')).forEach(function(el){el.classList.toggle('is-lit',s.indexOf(el.getAttribute('data-pt'))>=0);});
    var g=tags();input.value=(g?g+' ':'')+input.value.replace(/@Point\d+\s*/g,'');});});
  [].slice.call(document.querySelectorAll('.sh-pr,.lp-act')).forEach(function(b){b.addEventListener('click',function(){say(b.getAttribute('data-text'));});});
  [].slice.call(document.querySelectorAll('.lp-refresh')).forEach(function(b){b.addEventListener('click',function(){
    var s=b.closest('.lp-stamp');s.querySelector('.lp-stamp-at').textContent=b.getAttribute('data-fresh');
    s.querySelector('.lp-stamp-since').textContent=b.getAttribute('data-fresh-since');b.classList.add('is-done');});});
})();
'''

def plain_page(tab, theme, css, canvas, chat_data, view):
    chat = chat_html(chat_data)
    body = desktop(tab, theme, canvas, chat, False, 0) if view == 'desktop' else mobile(tab, theme, canvas, chat, False, 0)
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>%s landing page</title>%s<style>%s%s%s</style></head><body>%s<script>%s</script></body></html>') % (
        e(tab), embedded_fonts(), SHELL_CSS, LP_SHELL_CSS, LP_BASE_CSS + css, body, PLAIN_JS)

LOGIC = r'''<script type="text/x-dc" data-dc-script data-props='{"state":{"editor":"enum","options":["In progress","First visit"],"default":"In progress"},"$preview":{"width":%(W)d,"height":%(H)d}}'>
class Component extends DCLogic {
  constructor(props) { super(props); this.state = { pts: {}, draft: '', fresh: false }; }
  renderVals() {
    const ALL = %(data)s;
    const filled = (this.props.state ?? 'In progress') !== 'First visit';
    const D = filled ? ALL.filled : ALL.empty;
    const s = this.state;
    const P = D.points;
    const tags = (pts) => P.filter((p) => pts[p.n]).map((p) => '@Point' + p.n);
    const say = (t) => { const g = tags(s.pts); this.setState({ draft: (g.length ? g.join(' ') + ' ' : '') + t }); };
    const rest = (s.draft || '').replace(/@Point\d+\s*/g, '');
    const out = {
      filled: filled, empty: !filled, hasPoints: P.length > 0,
      points: P.map((p) => ({ n: p.n, label: p.label, pressed: !!s.pts[p.n], toggle: () => {
        const pts = { ...s.pts, [p.n]: !s.pts[p.n] }; const g = tags(pts);
        this.setState({ pts: pts, draft: (g.length ? g.join(' ') + ' ' : '') + rest }); } })),
      prompts: D.prompts.map((q) => ({ t: q, use: () => say(q) })),
      stamp: s.fresh ? D.stamp.fresh : D.stamp.at,
      since: s.fresh ? D.stamp.fresh_since : D.stamp.since,
      refresh: () => this.setState({ fresh: true }),
      act_go: () => say(D.actions.go.say), act_add: () => say(D.actions.add.say), act_jump: () => say(D.actions.jump.say),
      draft: s.draft, onDraft: (ev) => this.setState({ draft: ev.target.value })
    };
    for (let n = 1; n <= 9; n++) out['lit' + n] = filled && !!s.pts[n];
    return out;
  }
}
</script>'''

def dc_page(tab, theme, css, canvas_filled, canvas_empty, data, view, height, title):
    canvas = ('<sc-if value="{{filled}}" hint-placeholder-val="{{ true }}">%s</sc-if><sc-if value="{{empty}}" hint-placeholder-val="{{ false }}">%s</sc-if>' % (canvas_filled, canvas_empty))
    chat = chat_dc(data)
    body = desktop(tab, theme, canvas, chat, True, height) if view == 'desktop' else mobile(tab, theme, canvas, chat, True, height)
    W = 1440 if view == 'desktop' else 390
    slim = {k: {'points': [{'n': p['n'], 'label': p['label']} for p in data[k]['chat'].get('points', [])], 'prompts': data[k]['chat']['prompts'],
                'stamp': data[k]['stamp'], 'actions': data[k]['actions']} for k in ('filled', 'empty')}
    js = json.dumps(slim, ensure_ascii=False).replace("'", '\\u0027').replace('</', '<\\/')
    logic = LOGIC % dict(W=W, H=height, data=js)
    return ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<title>%s</title>\n<script src="./support.js"></script>\n</head>\n<body>\n<x-dc>\n<helmet>\n%s\n'
            '<style>\n%s\n%s\n%s\n</style>\n</helmet>\n%s\n</x-dc>\n%s\n</body>\n</html>\n') % (e(title), GOOGLE_FONTS, SHELL_CSS, LP_SHELL_CSS, LP_BASE_CSS + css, body, logic)

def canvas_wrap(tab_cls, sample_cls, inner, state):
    return '<div class="lp-host"><div class="lp %s %s" data-lp-state="%s">%s</div></div>' % (tab_cls, sample_cls, state, inner)

LP_BASE_CSS = '''
.lp-host{container-type:inline-size;container-name:lp;width:100%}
.lp{box-sizing:border-box;font-family:'Poppins','Segoe UI',system-ui,sans-serif}
.lp *,.lp *::before,.lp *::after{box-sizing:border-box}
.lp button{font:inherit;color:inherit;cursor:pointer}
.lp :focus-visible{outline:3px solid #d4a94f;outline-offset:2px}
.lp p{margin:0}
.lp ul,.lp ol{margin:0;padding:0;list-style:none}
.lp-refresh{display:inline-flex;align-items:center;gap:8px;min-height:44px;padding:0 16px;flex-shrink:0}
.lp-refresh.is-done svg{transform:rotate(360deg);transition:transform .6s ease}
@media (prefers-reduced-motion:reduce){.lp *{animation:none !important;transition:none !important}}
.lp-act{display:flex;flex-direction:column;align-items:flex-start;gap:2px;text-align:left;min-height:56px}
.lp-act-k{font-weight:600}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
'''
