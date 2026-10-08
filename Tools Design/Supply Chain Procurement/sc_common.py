"""
sc_common: the parts every Supply Chain and Procurement page shares.

The first tool of the Financial domain (8 Oct 2026). Discharge Process, Bed Management and OPD
Diagnostic Leak are Hospital Operations tools. Avishek's rule: every domain has its own identity,
and colour alone is not enough, because tools inside one domain already differ by colour.

What stays the same for every domain (the layout):
  the rail on the left with Home and the five places, the header bar, the page in the middle,
  the chat panel on the right (desktop); top bar, feed, chat, message box, five icons (phone);
  the five landing zones in their order; the type scale and its minimum sizes; plain English;
  picking, the three buttons, the stamp with Refresh now; drawn, not software.

What a domain changes (its identity, set here as a "skin"):
  the type families, the shapes (corners, border weights, edges), the paper and texture,
  the way the rail, header and chat panel are dressed, the marks for done / now / not started,
  how Tojo's Note is set, and the kind of drawing its pages use.

What a tool inside the domain changes: only its colours (ground, card, ink, highlight).

Three skins are drawn for review: A the ledger, B the till roll, C the annual report.
The page parts (masthead, stamp, zones, picking) come from the latest Bed Management parts,
loaded as a private copy (rules/08 §10). Nothing in Bed Management is changed.
"""
import base64, importlib.util, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.dirname(HERE)
BM = os.path.join(TOOLS, 'Bed Management')

_spec = importlib.util.spec_from_file_location('sc_bm_copy', os.path.join(BM, 'bm_common.py'))
B = importlib.util.module_from_spec(_spec)
sys.modules['sc_bm_copy'] = B
_spec.loader.exec_module(B)

TOOL = 'Supply Chain and Procurement'
HOSPITAL = 'Example hospital · 250 beds'
B.TOOL = TOOL
B.HOSPITAL[:] = [HOSPITAL]

e, ico, ICONS, CHEV = B.e, B.ico, B.ICONS, B.CHEV
sel, sel_cls, box, pt, say_btn = B.sel, B.sel_cls, B.box, B.pt, B.say_btn
standing, section, pending, actions = B.standing, B.section, B.pending, B.actions
TABS, CLIP, MIC, SEND, SHEET, HOME = B.TABS, B.CLIP, B.MIC, B.SEND, B.SHEET, B.HOME
TAGS = B.TAGS

def tag(t):
    return '<span class="bm-tag %s">%s</span>' % ('yours' if t == 'yours' else 'need' if t == 'need' else 'guess', e(TAGS[t]))

STAMP = {
    'filled': {'at': 'Brought up to date at midnight, 7 October', 'since': '2 conversations since then are not in yet',
               'fresh': 'Brought up to date just now, 11:40 AM', 'fresh_since': 'Everything you have said is in'},
    'empty': {'at': 'Nothing to bring up to date yet', 'since': 'This page fills in as you talk to Tojo',
              'fresh': 'Checked just now, 11:40 AM', 'fresh_since': 'No conversations yet'},
}

# The tool's mark: a carton with a price tag on a string.
MARK = ('<path d="M3 8l8-4 8 4v9l-8 4-8-4z"/><path d="M3 8l8 4 8-4"/><path d="M11 12v9"/>'
        '<path d="M15.5 6l-8 4"/>')

def masthead(kicker, emblem_html, st):
    return ('<header class="bm-mast"><div class="bm-id">%s<div><div class="bm-kick">%s</div><h1 class="bm-name">%s</h1></div></div>%s</header>') % (
        emblem_html, e(kicker), e(TOOL), B.stamp(st))

# ------------------------------------------------------------------------------------------
# Fonts: embedded so every page works offline. Each family carries its latin and latin-ext
# halves (the rupee sign lives in latin-ext).
FONT_DIR = os.path.join(HERE, 'fonts')
LATIN = 'U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD'
LATIN_EXT = 'U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+1E00-1E9F,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF'

def fonts(faces):
    """faces: [(family, file stem, weight, style)]"""
    out = []
    for fam, stem, w, st in faces:
        for half, rng in (('latin', LATIN), ('latin-ext', LATIN_EXT)):
            p = os.path.join(FONT_DIR, '%s-%s-%d-%s.woff2' % (stem, half, w, st))
            if not os.path.exists(p): continue
            b = base64.b64encode(open(p, 'rb').read()).decode()
            out.append("@font-face{font-family:'%s';src:url(data:font/woff2;base64,%s) format('woff2');font-weight:%d;font-style:%s;font-display:swap;unicode-range:%s}" % (
                fam, b, w, st, rng))
    return '<style>%s</style>' % ''.join(out)

# ------------------------------------------------------------------------------------------
# Colours of this tool. Ground, card, ink, muted, line, soft, grey, highlight, and two the
# domain needs: the highlight when it sits on the dark chat panel, and a dark highlight for text.
def theme(ground, card, ink, mut, line, soft, grey, hi, hi_dark, hi_text, rail, panel, extra=''):
    r, g, b = int(ink[1:3], 16), int(ink[3:5], 16), int(ink[5:7], 16)
    hr, hg, hb = int(hi[1:3], 16), int(hi[3:5], 16), int(hi[5:7], 16)
    return {'ground': ground, 'card': card, 'ink': ink, 'hi': hi, 'hi_dark': hi_dark, 'rail': rail, 'panel': panel,
            'vars': ('--g:%s;--card:%s;--ink:%s;--mut:%s;--line:%s;--soft:%s;--grey:%s;--hi:%s;--hi-dark:%s;--hi-text:%s;'
                     '--hi-soft:rgba(%d,%d,%d,.16);--panel:%s;--gridc:rgba(%d,%d,%d,.06);%s') % (
                ground, card, ink, mut, line, soft, grey, hi, hi_dark, hi_text, hr, hg, hb, panel, r, g, b, extra)}

# ------------------------------------------------------------------------------------------
# The chat panel words (same parts and labels as every tool; the skin dresses them).
def chat_html(c, send_colour='currentColor'):
    paras = ''.join('<p>%s</p>' % e(t) for t in c['text'])
    if c.get('pointer'): paras += '<p>%s</p>' % e(c['pointer'])
    out = ['<div class="sh-tm">%s</div>' % paras,
           '<div class="sh-notewrap"><div class="sh-lab">Tojo’s note</div><p class="sh-note">%s</p></div>' % e(c['note'])]
    if c.get('points'):
        out.append('<div class="sh-col"><div class="sh-lab">Add to a point — pick one or more</div>%s</div>' % ''.join(
            '<button class="sh-pt" aria-pressed="false" data-n="%d"><i>P%d</i><span>%s</span></button>' % (p['n'], p['n'], e(p['label'])) for p in c['points']))
    out.append('<div class="sh-col"><div class="sh-lab">Or ask next</div>%s</div>' % ''.join(
        '<button class="sh-pr" data-text="%s"><span>%s</span>%s</button>' % (e(p), e(p), ico(SEND, send_colour, 16)) for p in c['prompts']))
    return ''.join(out)

# ------------------------------------------------------------------------------------------
# The app frame: the same markup and the same places as every tool, so the layout never moves.
# A skin may only change what sits inside a rail entry (rail_inner) and the CSS.
RAIL_H = [136, 124, 124, 140, 128]

def desktop(sk, t, place, canvas, chat):
    tabs = []
    for i, ((n, d), c, h) in enumerate(zip(TABS, t['rail'], RAIL_H)):
        cur = n == place
        inner = sk['rail_inner'](i, n, d, cur)
        tabs.append('<a class="sh-tab%s" href="#"%s style="height:%dpx;--tc:%s">%s</a>' % (
            ' is-cur' if cur else '', ' aria-current="page"' if cur else '', h + (16 if cur else 0), c, inner))
    home_cur = ' aria-current="page"' if place is None else ''
    rail = '<nav class="sh-rail" aria-label="Sections"><a class="sh-home" href="#"%s aria-label="Home">%s</a>%s</nav>' % (
        home_cur, ico(HOME, 'currentColor', 22), ''.join(tabs))
    bar = ('<header class="sh-bar"><div class="sh-bt"><span class="sh-t">%s</span><small>%s</small></div>'
           '<div class="sh-bb"><button class="sh-btn-o">Guided tour</button><button class="sh-btn-g">Your tasks for the day</button></div></header>') % (TOOL, e(place or 'Home'))
    panel = ('<aside class="sh-chat" aria-label="Chat with Tojo"><div class="sh-panel"><div class="sh-ph"><div class="sh-av">T</div><div>'
             '<div class="sh-tname">Tojo</div><div class="sh-tsub">%s</div></div></div>'
             '<div class="sh-pb">%s</div><div class="sh-inp"><label for="tojo-input" class="sr">Message Tojo</label><textarea id="tojo-input" rows="2" placeholder="Write to Tojo…"></textarea>'
             '<div class="sh-tools"><button class="sh-ib" aria-label="Attach a file">%s</button><button class="sh-ib" aria-label="Attach a spreadsheet">%s</button>'
             '<button class="sh-ib" aria-label="Voice note">%s</button><span style="flex-grow:1"></span><button class="sh-send" aria-label="Send">%s</button></div></div></div></aside>') % (
        e(HOSPITAL), chat, ico(CLIP, 'currentColor'), ico(SHEET, 'currentColor'), ico(MIC, 'currentColor'), ico(SEND, 'currentColor'))
    return '<div class="sh-app bm-app">%s<div class="sh-mid">%s<main>%s</main></div>%s</div>' % (rail, bar, canvas, panel)

def mobile(sk, t, place, canvas, chat):
    home_cur = ' aria-current="page"' if place is None else ''
    top = ('<div class="sh-mt"><div class="sh-mtl"><a href="#" class="sh-homem"%s aria-label="Home">%s</a>'
           '<div><div class="sh-mtn">Virevo</div><div class="sh-mts">%s · %s</div></div></div><button class="sh-btn-o">Tour</button></div>') % (
        home_cur, ico(HOME, 'currentColor', 20), TOOL, e(place or 'Home'))
    who = '<div class="sh-who"><span class="sh-av">T</span>Tojo</div>'
    inp = ('<div class="sh-mi"><div class="sh-box"><label for="tojo-input" class="sr">Message Tojo</label><input id="tojo-input" placeholder="Write to Tojo…">'
           '<button class="sh-ib" aria-label="Attach a file">%s</button><button class="sh-ib sh-mic" aria-label="Voice note">%s</button></div>'
           '<button class="sh-send" aria-label="Send">%s</button></div>') % (ico(CLIP, 'currentColor', 19), ico(MIC, 'currentColor', 19), ico(SEND, 'currentColor'))
    foot = '<nav class="sh-mf" aria-label="Sections">%s</nav>' % ''.join(
        '<a href="#" aria-label="%s"%s>%s<span>%s</span></a>' % (n, ' aria-current="page"' if n == place else '', ico(d, 'currentColor', 20), sk['foot_word'](n))
        for n, d in TABS)
    return '<div class="sh-m bm-m">%s<div class="sh-mc">%s%s<div class="sh-mpanel">%s</div></div>%s%s</div>' % (top, who, canvas, chat, inp, foot)

# The frame CSS every skin builds on: only what keeps the layout (sizes, scrolling, places).
FRAME_CSS = '''
html,body{height:100%;overflow:hidden}
body{margin:0;background:var(--g)}
.sh-app{display:flex;height:100vh;min-height:0;overflow:hidden;background:var(--g);color:var(--ink)}
.sh-rail{width:84px;flex-shrink:0;display:flex;flex-direction:column;align-items:flex-start;gap:6px;padding-top:24px;height:100vh;box-sizing:border-box;overflow:hidden}
.sh-rail .sh-home{width:52px;height:52px;margin:0 0 22px 16px;display:flex;align-items:center;justify-content:center;text-decoration:none}
.sh-rail a.sh-tab{width:60px;writing-mode:vertical-rl;transform:rotate(180deg);display:flex;align-items:center;justify-content:center;gap:8px;text-decoration:none;font-size:13px;font-weight:600;color:var(--ink);background:var(--tc)}
.sh-rail a.sh-tab.is-cur{width:70px}
.sh-mid{flex-grow:1;min-width:0;display:flex;flex-direction:column;height:100vh;overflow-y:auto;overscroll-behavior:contain}
.sh-mid main{flex-grow:1}
.sh-bar{height:76px;flex-shrink:0;padding:0 36px;display:flex;align-items:center;justify-content:space-between;position:sticky;top:0;z-index:6;background:var(--g)}
.sh-bt{display:flex;align-items:baseline;gap:14px;min-width:0}
.sh-bb{display:flex;gap:10px}
.sh-btn-o,.sh-btn-g{min-height:44px;padding:0 16px;font-size:13px;cursor:pointer}
.sh-chat{width:420px;flex-shrink:0;padding:20px 20px 20px 0;display:flex;height:100vh;box-sizing:border-box}
.sh-panel{flex-grow:1;display:flex;flex-direction:column;overflow:hidden;min-height:0;background:var(--panel)}
.sh-ph{padding:18px 22px;display:flex;align-items:center;gap:12px}
.sh-av{width:44px;height:44px;display:flex;align-items:center;justify-content:center;flex-shrink:0}
.sh-pb{flex:1 1 auto;min-height:0;overflow-y:auto;overscroll-behavior:contain;padding:20px 22px;display:flex;flex-direction:column;gap:14px}
.sh-tm{display:flex;flex-direction:column;gap:8px;font-size:14px;line-height:1.55}
.sh-tm p,.sh-note{margin:0}
.sh-col{display:flex;flex-direction:column;gap:6px}
.sh-lab{font-size:12px;font-weight:600}
.sh-notewrap .sh-lab{margin-bottom:6px}
.sh-pt,.sh-pr{min-height:44px;width:100%;display:flex;align-items:center;gap:10px;text-align:left;font-size:13px;line-height:1.35;cursor:pointer}
.sh-pr{justify-content:space-between}
.sh-pt i{flex-shrink:0;min-width:32px;height:32px;display:flex;align-items:center;justify-content:center;font-style:normal;font-size:12px;font-weight:600}
.sh-inp{padding:14px 18px 16px;display:flex;flex-direction:column;gap:8px}
.sh-inp textarea{width:100%;box-sizing:border-box;resize:none;border:none;padding:12px 14px;font-size:14px;line-height:1.5;outline:none}
.sh-tools{display:flex;align-items:center}
.sh-ib{width:44px;height:44px;border:none;background:transparent;display:flex;align-items:center;justify-content:center;cursor:pointer;color:inherit}
.sh-send{width:48px;height:48px;border:none;display:flex;align-items:center;justify-content:center;cursor:pointer}
.sh-m{width:390px;max-width:100%;margin:0 auto;height:100vh;min-height:0;overflow:hidden;display:flex;flex-direction:column;background:var(--g);color:var(--ink)}
.sh-mt{flex:none;padding:14px 16px;display:flex;align-items:center;justify-content:space-between}
.sh-mtl{display:flex;align-items:center;gap:12px}
.sh-homem{width:44px;height:44px;display:flex;align-items:center;justify-content:center}
.sh-mts{font-size:12px}
.sh-mc{flex:1 1 auto;min-height:0;overflow-y:auto;overscroll-behavior:contain;padding:16px 0 20px;display:flex;flex-direction:column;gap:14px}
.sh-mc > .sh-who{margin:0 14px;display:flex;align-items:center;gap:8px;font-size:12px;font-weight:600}
.sh-who .sh-av{width:30px;height:30px;font-size:15px}
.sh-mc > .sh-mpanel{flex:none;margin:0 14px;padding:16px;display:flex;flex-direction:column;gap:14px;height:calc(100vh - 250px);min-height:360px;overflow-y:auto;overscroll-behavior:contain;background:var(--panel)}
.sh-mi{flex:none;padding:12px 14px;display:flex;align-items:center;gap:10px}
.sh-mi .sh-box{flex-grow:1;min-width:0;display:flex;align-items:center;gap:2px;padding:0 4px 0 16px}
.sh-mi input{flex-grow:1;min-width:0;min-height:48px;border:none;background:transparent;font-size:14px;outline:none}
.sh-mi .sh-ib{width:40px;height:40px}
.sh-mf{flex:none;display:grid;grid-template-columns:repeat(5,minmax(0,1fr));padding:0 8px 10px}
.sh-mf a{height:56px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:3px;text-decoration:none;font-size:10.5px;font-weight:600}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
.dom-fin .bm-sec{margin-top:38px}
.dom-fin .lp-acts{margin-top:34px}
.dom-fin .bm-stand{margin-bottom:24px}
@container lp (min-width:700px){
 .bm{padding-top:0}
 .bm-mast{position:sticky;top:76px;z-index:5;background:var(--g);padding-top:24px}
}
'''

def page(sk, t, place, canvas_inner, css, chat, view, title, cls):
    canvas = '<div class="lp-host"><div class="lp bm %s %s" style="%s">%s</div></div>' % (sk['cls'], cls, t['vars'], canvas_inner)
    ch = chat_html(chat)
    body = desktop(sk, t, place, canvas, ch) if view == 'desktop' else mobile(sk, t, place, canvas, ch)
    base = _accent(B.BASE_CSS + B.SEL_CSS)
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>%s</title>%s<style>%s%s%s%s</style></head><body class="dom-fin %s" style="%s">%s<script>%s%s</script></body></html>') % (
        e(title), sk['fonts'], FRAME_CSS, base, sk['css'], css, sk['cls'], t['vars'], body, B.JS, B.SEL_JS)

GOLD = '#d4a94f'
def _accent(css):
    """The shared gold becomes this tool's highlight."""
    return css.replace('rgba(212,169,79,.55)', 'var(--hi)').replace(GOLD, 'var(--hi)')

# ------------------------------------------------------------------------------------------
# Plain English: refuse the registry's listed words in anything a user reads (06 §5.8, F7).
REG = os.path.join(TOOLS, 'Common Elements', 'blocks', 'registry.json')
def plain_check(text):
    pe = json.load(open(REG, encoding='utf-8'))['plain_english']
    bad = []
    for w in pe['abbreviations']:
        if re.search(r'\b%s\b' % re.escape(w), text): bad.append(w)
    for w in pe['words']:
        if re.search(r'\b%s\b' % re.escape(w), text, re.I): bad.append(w)
    for p, why in pe['patterns']:
        if re.search(p, text): bad.append(why)
    if re.search(r'\btabs?\b', text, re.I): bad.append('tab')
    # this domain's own words: shop-floor buying words a hospital manager may not use
    for w in ('procure', 'procured', 'SKU', 'vendor', 'inventory', 'indent', 'GRN', 'PO', 'rate contract', 'consumption'):
        if re.search(r'\b%s\b' % re.escape(w), text, re.I if w.islower() else 0): bad.append(w)
    return bad
