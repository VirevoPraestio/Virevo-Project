"""
bm_common: the parts every Bed Management page shares (the home page and the four place pages).

Same five zones as every landing page, in the same order:
  masthead (emblem, name, stamp with Refresh now) · where this stands · the drawing ·
  what Tojo still has to do · the three buttons.
Roomy by design (feedback 30 Sep 2026): a desktop page may run to 1.5-2 screens, so each zone
gets space to breathe. Standard library only (Playwright only for measure()).
"""
import glob, html, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = HERE                                                    # the Bed Management folder
COMMON = os.path.join(os.path.dirname(HERE), 'Common Elements')   # shared rules, generators and the block library
sys.path[:0] = [os.path.join(COMMON, 'landing-common'), os.path.join(COMMON, 'diagnosis-html-generator')]
from landing_common import embedded_fonts, REFRESH_ICO, chat_html  # noqa: E402
from preview import SHELL_CSS, TABS, ico, CLIP, MIC, SEND, SHEET, HOME  # noqa: E402

e = lambda s: html.escape('' if s is None else str(s), quote=True)
TOOL = 'Bed Management'
HOSPITAL = ['300-bed hospital, Nagpur']  # the Bed Management practice hospital (settled 30 Sep 2026)
ICONS = dict(TABS)
PLACES = ['Diagnosis', 'Solutions', 'Automations', 'Processes']
NEXT = {'Diagnosis': 'Solutions', 'Solutions': 'Automations', 'Automations': 'Processes', 'Processes': 'Diagnosis'}
BED_ICO = '<path d="M3 19V6"/><path d="M3 15h18v4"/><path d="M21 15v-2.5A2.5 2.5 0 0018.5 10H11v5"/><circle cx="7" cy="12" r="2"/>'
TAGS = {'yours': 'Your number', 'derived': 'Worked out from yours', 'guess': 'Tojo’s guess', 'example': 'Example only', 'goal': 'Goal', 'need': 'Need from you'}
STAMP = {
    'filled': {'at': 'Brought up to date at midnight, 30 September', 'since': '3 conversations since then are not in yet',
               'fresh': 'Brought up to date just now, 11:40 AM', 'fresh_since': 'Everything you have said is in'},
    'empty': {'at': 'Nothing to bring up to date yet', 'since': 'This page fills in as you talk to Tojo',
              'fresh': 'Checked just now, 11:40 AM', 'fresh_since': 'No conversations yet'},
}

# ------------------------------------------------------------------------------------------
def pt(n):
    return '' if n is None else ' data-pt="%d"' % n

def stamp(s):
    return ('<div class="lp-stamp"><div class="lp-stamp-txt"><span class="lp-stamp-at">%s</span><span class="lp-stamp-since">%s</span></div>'
            '<button class="lp-refresh" type="button" data-fresh="%s" data-fresh-since="%s">%s<span>Refresh now</span></button></div>') % (
        e(s['at']), e(s['since']), e(s['fresh']), e(s['fresh_since']), REFRESH_ICO)

def masthead(kicker, name, emblem, st):
    return ('<header class="bm-mast"><div class="bm-id">%s<div><div class="bm-kick">%s</div><h1 class="bm-name">%s</h1></div></div>%s</header>') % (
        emblem, e(kicker), e(name), stamp(st))

def emblem(icon_path, shape=''):
    return '<span class="bm-emb %s">%s</span>' % (shape, ico(icon_path, '#d4a94f', 30))

def standing(claim, deck, empty):
    return '<div class="bm-stand%s"><h2 class="bm-claim">%s</h2><p class="bm-deck">%s</p></div>' % (' is-empty' if empty else '', e(claim), e(deck))

def section(label, inner, cls='', sub=''):
    return '<section class="bm-sec %s" aria-label="%s"><div class="bm-sech"><h3 class="bm-lab">%s</h3>%s</div>%s</section>' % (
        cls, e(label), e(label), '<span class="bm-labsub">%s</span>' % e(sub) if sub else '', inner)

def pending(items):
    li = ''.join('<li class="bm-pi%s"%s><i class="bm-pm" aria-hidden="true"></i><span>%s%s</span></li>' % (
        ' wait' if p.get('need') else '', pt(p.get('pt')), e(p['text']),
        '<b class="bm-need">%s</b>' % e(p['need']) if p.get('need') else '') for p in items)
    return section('What Tojo still has to do', '<ul class="bm-pend">%s</ul>' % li, 'bm-sec-pend')

def actions(a):
    b = lambda k, head, det: '<button class="lp-act lp-act-%s" type="button" data-text="%s"><span class="lp-act-k">%s</span><span class="lp-act-d">%s</span></button>' % (
        k, e(a[k]['say']), e(head), e(det))
    return '<nav class="lp-acts" aria-label="What to do next">%s%s%s</nav>' % (
        b('go', 'Proceed with next step', a['go']['detail']), b('add', 'Add more', a['add']['detail']),
        b('jump', 'Jump to ' + a['jump']['tab'], a['jump']['detail']))

def tag(t):
    return '<span class="bm-tag %s">%s</span>' % ('yours' if t == 'yours' else 'need' if t == 'need' else 'guess', e(TAGS[t]))

def say_btn(label, text, cls='bm-open'):
    return '<button class="%s" type="button" data-text="%s">%s %s</button>' % (cls, e(text), e(label), ico(SEND, 'currentColor', 16))

# ------------------------------------------------------------------------------------------
BASE_CSS = '''
.lp-host{container-type:inline-size;container-name:lp;width:100%}
.lp{box-sizing:border-box;font-family:'Poppins','Segoe UI',system-ui,sans-serif}
.lp *,.lp *::before,.lp *::after{box-sizing:border-box}
.lp button{font:inherit;color:inherit;cursor:pointer}
.lp :focus-visible{outline:3px solid #d4a94f;outline-offset:2px}
:where(.lp) :where(p,h1,h2,h3,h4){margin:0}
:where(.lp) :where(ul,ol){margin:0;padding:0;list-style:none}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
.bm{padding:28px 40px 48px;color:var(--ink);--gold:#d4a94f;--dgold:#6B4F16;--amber:#8A5608;--green:#2F6B4F;--red:#8E2F1C}
.bm-mast{display:flex;align-items:center;justify-content:space-between;gap:24px;padding-bottom:18px;border-bottom:2px solid var(--ink)}
.bm-id{display:flex;align-items:center;gap:16px;min-width:0}
.bm-emb{flex-shrink:0;width:56px;height:56px;border-radius:6px;background:var(--ink);display:flex;align-items:center;justify-content:center;box-shadow:inset 0 0 0 3px var(--ink),inset 0 0 0 5px rgba(212,169,79,.55)}
.bm-kick{font-size:12.5px;font-weight:600;color:var(--mut)}
.bm-name{font-family:'Bebas Neue',sans-serif;font-weight:400;font-size:52px;line-height:.95;white-space:nowrap}
.lp-stamp{display:flex;align-items:center;gap:14px}
.lp-stamp-txt{display:flex;flex-direction:column;text-align:right;max-width:360px}
.lp-stamp-at{font-size:13px;font-weight:600}.lp-stamp-since{font-size:12.5px;color:var(--mut)}
.lp-refresh{display:inline-flex;align-items:center;gap:8px;min-height:44px;padding:0 18px;flex-shrink:0;border:1.5px solid var(--ink);background:var(--card);border-radius:var(--btnr);font-size:13.5px;font-weight:500}
.lp-refresh.is-done svg{transform:rotate(360deg);transition:transform .6s ease}
.bm-stand{margin:30px 0 36px;max-width:820px}
.bm-claim{font-family:'Bebas Neue',sans-serif;font-weight:400;font-size:44px;line-height:1}
.bm-deck{font-size:15.5px;line-height:1.55;color:var(--mut);margin-top:10px}
.bm-stand.is-empty .bm-claim{color:var(--mut)}
.bm-sec{margin-top:44px}
.bm-sech{display:flex;align-items:baseline;justify-content:space-between;gap:16px;margin-bottom:14px}
.bm-lab{font-size:14px;font-weight:600}
.bm-labsub{font-size:12.5px;color:var(--mut)}
.bm-hint{font-size:12.5px;color:var(--mut);font-style:italic;margin-top:10px}
.bm-tag{display:inline-block;align-self:flex-start;font-size:11px;font-weight:600;padding:2px 8px;border-radius:3px;white-space:nowrap}
.bm-tag.yours{border:1.5px solid var(--green);color:var(--green)}.bm-tag.guess{border:1.5px dashed var(--dgold);color:var(--dgold)}.bm-tag.need{border:1.5px dashed var(--red);color:var(--red)}
.bm-pend{display:grid;grid-template-columns:1fr 1fr;gap:14px 36px}
.bm-pi{display:flex;gap:12px;font-size:14.5px;line-height:1.5}
.bm-pm{width:17px;height:17px;border:2px solid var(--ink);border-radius:4px;flex-shrink:0;margin-top:3px}
.bm-pi.wait .bm-pm{border:2px dashed var(--amber)}
.bm-need{display:block;font-size:13px;font-weight:600;color:var(--amber);margin-top:2px}
.lp-acts{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin-top:40px}
.lp-act{display:flex;flex-direction:column;align-items:flex-start;justify-content:center;gap:3px;text-align:left;min-height:68px;padding:10px 18px;border:1.5px solid var(--ink);background:var(--card);border-radius:var(--btnr)}
.lp-act-k{font-weight:600;font-size:15px}.lp-act-d{font-size:13px;color:var(--mut)}
.lp .lp-act-go{background:var(--ink);color:var(--card);box-shadow:inset 6px 0 0 #d4a94f;padding-left:22px}.lp .lp-act-go .lp-act-d{color:inherit;opacity:.85}
.bm-open{display:inline-flex;align-items:center;gap:8px;min-height:44px;padding:0 16px;border:1.5px solid var(--ink);border-radius:var(--btnr);background:transparent;font-size:13.5px;font-weight:600;white-space:nowrap}
.bm-paper{background-color:var(--card);background-image:linear-gradient(var(--gridc) 1px,transparent 1px),linear-gradient(90deg,var(--gridc) 1px,transparent 1px);background-size:20px 20px}
.lp .is-lit{outline:4px solid #d4a94f !important;outline-offset:3px;border-radius:6px}
details.bm-more>summary{list-style:none;display:inline-flex;align-items:center;gap:8px;min-height:40px;padding:0 14px;border:1.5px solid var(--ink);border-radius:20px;font-size:13px;font-weight:600;cursor:pointer}
details.bm-more>summary::-webkit-details-marker{display:none}
details.bm-more>summary::after{content:"";width:7px;height:7px;border-right:2px solid currentColor;border-bottom:2px solid currentColor;transform:rotate(45deg);margin:-4px 0 0 2px}
details.bm-more[open]>summary::after{transform:rotate(-135deg);margin-top:3px}
details.bm-more ul{margin-top:10px;display:flex;flex-direction:column;gap:6px}
details.bm-more li{font-size:13.5px;line-height:1.45;padding-left:16px;position:relative}
details.bm-more li::before{content:"";position:absolute;left:2px;top:.6em;width:6px;height:6px;border-radius:50%;background:var(--ink)}
@media (prefers-reduced-motion:reduce){.lp *{animation:none !important;transition:none !important}}
@container lp (max-width:699px){
 .bm{padding:20px 16px 32px}
 .bm-mast{flex-direction:column;align-items:flex-start;gap:14px}
 .bm-name{font-size:42px;white-space:normal}
 .lp-stamp{width:100%;justify-content:space-between}.lp-stamp-txt{text-align:left;max-width:none}
 .bm-stand{margin:22px 0 26px}
 .bm-claim{font-size:34px}
 .bm-deck{font-size:14.5px}
 .bm-sec{margin-top:32px}
 .bm-sech{flex-direction:column;gap:2px}
 .bm-pend{grid-template-columns:1fr;gap:12px}
 .bm-pi{font-size:14px}
 .lp-acts{grid-template-columns:1fr;gap:10px;margin-top:28px}
}
'''

# ------------------------------------------------------------------------------------------
def shell_css(t):
    return '''
.bm-app,.bm-m{color:%(ink)s}
.bm-app .sh-bar{border-bottom-color:rgba(0,0,0,.14)}.bm-app .sh-rail{border-right-color:rgba(0,0,0,.14)}
.bm-app .sh-rail .sh-home,.bm-m .sh-homem{background:%(ink)s}
.bm-app .sh-rail .sh-home[aria-current=page],.bm-m .sh-homem[aria-current=page]{box-shadow:0 0 0 3px %(ground)s,0 0 0 5.5px #d4a94f}
.bm-app .sh-bar .sh-t{color:%(ink)s}.bm-app .sh-bar small{color:%(ink)s;opacity:.8}
.bm-app .sh-btn-o,.bm-m .sh-btn-o{border-color:%(ink)s;color:%(ink)s}
.sh-rail a.sh-tab{width:60px;border-radius:0 12px 12px 0;color:%(ink)s;writing-mode:vertical-rl;transform:rotate(180deg);display:flex;align-items:center;justify-content:center;text-decoration:none;font-size:13px;font-weight:600;letter-spacing:.09em;text-transform:uppercase}
.sh-rail a.sh-tab[aria-current=page]{width:70px;font-weight:700}
.sh-mf a[aria-current=page]{box-shadow:inset 0 3px 0 #d4a94f}
.bm-m .sh-mt{border-bottom-color:rgba(0,0,0,.14)}
.sh-mid main{flex-grow:1}
body{margin:0;background:%(ground)s}
''' % t

def desktop(t, place, canvas, chat):
    tabs = []
    for (n, _), c, h in zip(TABS, t['rail'], [136, 124, 124, 140, 128]):
        if n == place:
            tabs.append('<a class="sh-tab" href="#" aria-current="page" style="height:%dpx;background:%s;color:%s">%s</a>' % (h + 16, t['rail_bg'], t['rail_fg'], n))
        else:
            tabs.append('<a class="sh-tab" href="#" style="height:%dpx;background:%s">%s</a>' % (h, c, n))
    home_cur = ' aria-current="page"' if place is None else ''
    rail = '<nav class="sh-rail" aria-label="Sections"><a class="sh-home" href="#"%s aria-label="Home">%s</a>%s</nav>' % (home_cur, ico(HOME, '#d4a94f', 22), ''.join(tabs))
    bar = ('<header class="sh-bar"><div><span class="sh-t">%s</span><small>%s</small></div>'
           '<div style="display:flex;gap:10px"><button class="sh-btn-o">Guided tour</button><button class="sh-btn-g">Your tasks for the day</button></div></header>') % (TOOL, e(place or 'Home'))
    panel = ('<aside class="sh-chat" aria-label="Chat with Tojo"><div class="sh-panel"><div class="sh-ph"><div class="sh-av">T</div><div>'
             '<div style="font-family:\'Bebas Neue\',sans-serif;font-size:28px;line-height:1">Tojo</div><div style="font-size:12px;color:#9CA9A1">%s</div></div></div>'
             '<div class="sh-pb">%s</div><div class="sh-inp"><label for="tojo-input" class="sr">Message Tojo</label><textarea id="tojo-input" rows="2" placeholder="Write to Tojo…"></textarea>'
             '<div style="display:flex;align-items:center"><button class="sh-ib" aria-label="Attach a file">%s</button><button class="sh-ib" aria-label="Attach a spreadsheet">%s</button>'
             '<button class="sh-ib" aria-label="Voice note">%s</button><span style="flex-grow:1"></span><button class="sh-send" aria-label="Send">%s</button></div></div></div></aside>') % (
        e(HOSPITAL[0]), chat, ico(CLIP), ico(SHEET), ico(MIC), ico(SEND, '#10241a'))
    return '<div class="sh-app bm-app" style="background:%s">%s<div class="sh-mid">%s<main>%s</main></div>%s</div>' % (t['ground'], rail, bar, canvas, panel)

def mobile(t, place, canvas, chat):
    home_cur = ' aria-current="page"' if place is None else ''
    top = ('<div class="sh-mt"><div style="display:flex;align-items:center;gap:12px"><a href="#" class="sh-homem"%s aria-label="Home" style="width:44px;height:44px;border-radius:50%%;display:flex;align-items:center;justify-content:center">%s</a>'
           '<div><div style="font-family:\'Bebas Neue\',sans-serif;font-size:24px;line-height:1">Virevo</div><div style="font-size:12px;opacity:.8">%s · %s</div></div></div><button class="sh-btn-o">Tour</button></div>') % (
        home_cur, ico(HOME, '#d4a94f', 20), TOOL, e(place or 'Home'))
    who = '<div class="sh-who" style="color:inherit"><span class="sh-av" style="width:30px;height:30px;font-size:17px">T</span>Tojo</div>'
    inp = ('<div class="sh-mi" style="position:static"><div class="sh-box"><label for="tojo-input" class="sr">Message Tojo</label><input id="tojo-input" placeholder="Write to Tojo…">'
           '<button class="sh-ib" style="width:40px;height:40px" aria-label="Attach a file">%s</button><button class="sh-ib" style="width:40px;height:40px;border-radius:50%%;background:rgba(16,36,26,.08)" aria-label="Voice note">%s</button></div>'
           '<button class="sh-send" aria-label="Send">%s</button></div>') % (ico(CLIP, '#10241a', 19), ico(MIC, '#10241a', 19), ico(SEND, '#10241a'))
    foot = '<nav class="sh-mf" style="position:static" aria-label="Sections">%s</nav>' % ''.join(
        '<a href="#" aria-label="%s"%s>%s</a>' % (n, ' aria-current="page"' if n == place else '', ico(dd, '#d4a94f' if n == place else '#F3F1EA', 22)) for n, dd in TABS)
    return '<div class="sh-m bm-m" style="background:%s">%s<div class="sh-mc">%s%s<div class="sh-mpanel">%s</div></div>%s%s</div>' % (t['ground'], top, who, canvas, chat, inp, foot)

JS = r'''
(function(){
  var $$=function(s,r){return [].slice.call((r||document).querySelectorAll(s));};
  var input=document.getElementById('tojo-input');
  var pts=$$('.sh-pt');
  function sel(){return pts.filter(function(p){return p.getAttribute('aria-pressed')==='true';}).map(function(p){return p.getAttribute('data-n');});}
  function tags(){return sel().map(function(n){return '@Point'+n;}).join(' ');}
  function say(t){var g=tags();input.value=(g?g+' ':'')+t;input.focus();}
  pts.forEach(function(p){p.addEventListener('click',function(){
    p.setAttribute('aria-pressed',p.getAttribute('aria-pressed')==='true'?'false':'true');
    var s=sel();$$('.lp [data-pt]').forEach(function(el){el.classList.toggle('is-lit',s.indexOf(el.getAttribute('data-pt'))>=0);});
    var g=tags();input.value=(g?g+' ':'')+input.value.replace(/@Point\d+\s*/g,'');});});
  $$('.sh-pr,.sh-opt,.lp-act,.bm-open,[data-say]').forEach(function(b){b.addEventListener('click',function(ev){ev.stopPropagation();say(b.getAttribute('data-text'));});});
  $$('.lp-refresh').forEach(function(b){b.addEventListener('click',function(){
    var s=b.closest('.lp-stamp');s.querySelector('.lp-stamp-at').textContent=b.getAttribute('data-fresh');
    s.querySelector('.lp-stamp-since').textContent=b.getAttribute('data-fresh-since');b.classList.add('is-done');});});
  /* pick one of a group: buttons [data-grp][data-key]; panels [data-det="grp:key"] */
  $$('.js-pick').forEach(function(b){b.addEventListener('click',function(){
    var g=b.getAttribute('data-grp'),k=b.getAttribute('data-key');
    $$('.js-pick[data-grp="'+g+'"]').forEach(function(o){o.setAttribute('aria-pressed',o.getAttribute('data-key')===k?'true':'false');});
    $$('[data-det^="'+g+':"]').forEach(function(d){d.hidden=d.getAttribute('data-det')!==g+':'+k;});
    var root=b.closest('[data-view]');if(root)root.setAttribute('data-view',k);});});
  /* small bed or lamp: fill the caption of its box */
  $$('.js-cap').forEach(function(b){b.addEventListener('click',function(){
    var box=b.closest('[data-capbox]');$$('.js-cap',box).forEach(function(o){o.setAttribute('aria-pressed',o===b?'true':'false');});
    var c=box.querySelector('.js-capt');c.textContent=b.getAttribute('data-cap');c.classList.add('is-set');});});
  /* turn: toggle aria-expanded on itself */
  $$('.js-turn').forEach(function(b){b.addEventListener('click',function(){
    b.setAttribute('aria-expanded',b.getAttribute('aria-expanded')==='true'?'false':'true');});});
})();
'''

FONTS = []
def page(t, place, canvas_inner, css, chat, view, title, cls):
    if not FONTS: FONTS.append(embedded_fonts())
    canvas = '<div class="lp-host"><div class="lp bm %s" style="%s">%s</div></div>' % (cls, t['vars'], canvas_inner)
    ch = chat_html(chat)
    body = desktop(t, place, canvas, ch) if view == 'desktop' else mobile(t, place, canvas, ch)
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>%s</title>%s<style>%s%s%s%s</style></head><body>%s<script>%s</script></body></html>') % (
        e(title), FONTS[0], SHELL_CSS, shell_css(t), BASE_CSS, css, body, JS)

# ------------------------------------------------------------------------------------------
def build(out, prefix, samples, themes, render):
    """samples: {key: ...}; render(key, state) -> (place, canvas_inner, css, chat, cls). Writes every page, returns them."""
    os.makedirs(out, exist_ok=True)
    pages = {}
    for k in samples:
        for st in ('filled', 'empty'):
            for v in ('desktop', 'mobile'):
                place, inner, css, chat, cls = render(k, st)
                h = page(themes[k], place, inner, css, chat, v, '%s %s, sample %s' % (TOOL, place or 'home', k.upper()), cls)
                pages['%s.%s.%s' % (k, v, st)] = h
                open(os.path.join(out, '%s-%s.%s.%s.html' % (prefix, k, v, st)), 'w').write(h)
    return pages

def review(title, intro, about, themes, pages, note=''):
    """about: {key: (name, what it is, colours)}"""
    data = json.dumps(pages, ensure_ascii=False).replace('</', '<\\/')
    first = next(iter(about))
    picks = ''.join('<button class="rv-s" type="button" data-s="%s" aria-pressed="%s"><b>Sample %s</b><span>%s</span><i style="background:%s;border-color:%s"></i></button>' % (
        k, 'true' if k == first else 'false', k.upper(), e(v[0]), themes[k]['ground'], themes[k]['ink']) for k, v in about.items())
    tpl = open(os.path.join(HERE, 'review_template.html')).read()
    return (tpl.replace('@@TITLE@@', e(title)).replace('@@INTRO@@', e(intro)).replace('@@NOTE@@', e(note)).replace('@@PICKS@@', picks)
               .replace('@@FIRST@@', first).replace('@@ABOUT@@', json.dumps(about, ensure_ascii=False)).replace('@@DATA@@', data))

def measure(out, prefix):
    from playwright.sync_api import sync_playwright
    shots = os.path.join(out, 'shots'); os.makedirs(shots, exist_ok=True)
    rows = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        for f in sorted(glob.glob(os.path.join(out, prefix + '-*.html'))):
            n = os.path.basename(f)[len(prefix) + 1:-5]; mob = '.mobile.' in n
            pg = b.new_page(viewport={'width': 390 if mob else 1440, 'height': 900})
            errs = []; pg.on('pageerror', lambda x: errs.append(str(x)))
            pg.goto('file://' + f); pg.wait_for_timeout(250)
            r = pg.evaluate('''()=>{const c=document.querySelector('.lp-host');const t=document.querySelector('.lp').innerText+' '+document.querySelector('.sh-chat,.sh-mpanel').innerText;
              return {canvas:Math.round(c.getBoundingClientRect().height),side:document.documentElement.scrollWidth>window.innerWidth,tab:/\\btabs?\\b/i.test(t)}}''')
            pg.screenshot(path=os.path.join(shots, n + '.png'), full_page=True)
            flags = (['SIDEWAYS'] if r['side'] else []) + (['WORD TAB'] if r['tab'] else []) + (['JS ERROR ' + errs[0]] if errs else [])
            if not mob and r['canvas'] > 1800: flags.append('OVER 2 SCREENS')
            rows.append('%-22s %5d  %s' % (n, r['canvas'], ' '.join(flags)))
            pg.close()
        b.close()
    print('\n'.join(rows))

# ------------------------------------------------------------------------------------------
# The small bed, seen from above: the mark every Bed Management page counts with.
# States: done (blanket filled), now (gold), later (plain), none / empty (dashed grey).
BED_SVG = ('<svg viewBox="0 0 40 54" width="%d" height="%d" aria-hidden="true"><rect class="h" x="4" y="2" width="32" height="6" rx="3"/>'
           '<rect class="f" x="6" y="8" width="28" height="43" rx="4"/><rect class="p" x="11" y="12" width="18" height="8" rx="4"/>'
           '<path class="k" d="M6 25h28v22a4 4 0 01-4 4H10a4 4 0 01-4-4z"/></svg>')
def bed_svg(w=40):
    return BED_SVG % (w, round(w * 54 / 40))

BED_CSS = '''
.bmb svg .h{fill:var(--ink)}.bmb svg .f{fill:var(--card);stroke:var(--ink);stroke-width:2}.bmb svg .p{fill:var(--soft);stroke:var(--ink);stroke-width:1.2}.bmb svg .k{fill:none}
.bmb.s-done svg .k{fill:var(--ink)}
.bmb.s-now svg .k,.bmb.s-now svg .h{fill:#d4a94f}
.bmb.s-later svg .k{fill:var(--soft)}
.bmb.s-none svg .f,.bmb.s-empty svg .f{stroke:var(--grey);stroke-dasharray:4 3;fill:transparent}.bmb.s-none svg .h,.bmb.s-empty svg .h{fill:var(--grey)}
.bmb.s-none svg .p,.bmb.s-empty svg .p{stroke:var(--grey);fill:transparent}
.bmb{display:inline-flex}
button.bmb{padding:3px;border:0;background:none;border-radius:6px;align-items:center;justify-content:center;min-width:40px;min-height:40px}
button.bmb[aria-pressed=true]{outline:3px solid #d4a94f;outline-offset:1px}
.bm-key{display:flex;flex-wrap:wrap;gap:8px 22px;margin-top:14px;font-size:12.5px;color:var(--mut)}
.bm-key span{display:inline-flex;align-items:center;gap:7px}.bm-key i{width:13px;height:13px;border-radius:3px;border:1.5px solid var(--ink)}
.bm-key .k-done{background:var(--ink)}.bm-key .k-now{background:#d4a94f;border-color:#d4a94f}.bm-key .k-later{background:var(--soft)}.bm-key .k-none{border:1.5px dashed var(--grey)}
'''
def bed_key(words=('Done', 'Now', 'Still to do', 'Not started')):
    return ('<div class="bm-key" aria-hidden="true"><span><i class="k-done"></i>%s</span><span><i class="k-now"></i>%s</span>'
            '<span><i class="k-later"></i>%s</span><span><i class="k-none"></i>%s</span></div>') % tuple(e(w) for w in words)

def theme(ground, card, ink, mut, line, soft, grey, rail, btnr='6px', extra=''):
    r, g, b = int(ink[1:3], 16), int(ink[3:5], 16), int(ink[5:7], 16)
    return {'ground': ground, 'ink': ink, 'rail_bg': ink, 'rail_fg': '#d4a94f', 'rail': rail,
            'vars': '--g:%s;--card:%s;--ink:%s;--mut:%s;--line:%s;--soft:%s;--grey:%s;--btnr:%s;--gridc:rgba(%d,%d,%d,.05);%s' % (
                ground, card, ink, mut, line, soft, grey, btnr, r, g, b, extra)}

def place_render(place, data, samples, css_common):
    """Builds the render function for a place page from {key: (canvas_fn, css)}."""
    def render(k, st):
        fn, css = samples[k]
        return place, fn(data[st], st == 'empty'), css_common + css, data[st]['chat'], 'bm-%s bm-%s-%s' % (place.lower(), place.lower()[:1], k)
    return render

def place_main(place, prefix, data, samples, css_common, themes, about, intro, note=''):
    out = os.path.join(ROOT, 'out', 'landing', place.lower())
    pages = build(out, prefix, list(samples), themes, place_render(place, data, samples, css_common))
    rv = os.path.join(out, 'bed-management-%s-samples.html' % place.lower())
    open(rv, 'w').write(review('Bed Management · %s page samples' % place, intro, about, themes, pages, note))
    print('built', rv)
    if '--measure' in sys.argv: measure(out, prefix)

# ==========================================================================================
# v3 (30 Sep 2026 feedback)
#  1. The chat panel is one screen tall, desktop and phone, and scrolls on its own. Only the canvas scrolls.
#  2. On a phone, each element's box opens right under that element. On desktop, one shared box.
#  3. The page loads with the first element raised (lifted, shadowed, gold edge) and its box open.
#     Picking another element raises it, opens its box, and puts the rest back.
SHELL_V3_CSS = '''
html,body{height:100%;overflow:hidden}
.sh-app{height:100vh;min-height:0;overflow:hidden}
.sh-rail{height:100vh;box-sizing:border-box;overflow:hidden}
.sh-mid{height:100vh;overflow-y:auto;overscroll-behavior:contain}
.sh-mid .sh-bar{position:sticky;top:0;z-index:6;background:inherit}
.sh-chat{height:100vh;box-sizing:border-box}
.sh-panel{min-height:0}
.sh-pb{flex:1 1 auto;min-height:0;overflow-y:auto;overscroll-behavior:contain}
.sh-m{height:100vh;min-height:0;overflow:hidden}
.sh-mt{flex:none}
.sh-mc{flex:1 1 auto;min-height:0;overflow-y:auto;overscroll-behavior:contain}
.sh-mc > .sh-mpanel{flex:none;height:calc(100vh - 250px);min-height:360px;overflow-y:auto;overscroll-behavior:contain}
.sh-mi,.sh-mf{flex:none}
.sh-scrollnote{font-size:11px;color:#9CA9A1;text-align:center;margin-top:-6px}
@container lp (min-width:700px){
 .bm{padding-top:0}
 .bm-mast{position:sticky;top:76px;z-index:5;background:var(--g);padding-top:24px;box-shadow:0 10px 12px -12px rgba(0,0,0,.25)}
}
'''
SEL_CSS = '''
.js-sel{cursor:pointer;transition:transform .18s ease,box-shadow .18s ease,background-color .18s ease}
.js-sel.is-up{position:relative;z-index:3;transform:translateY(-5px);
  box-shadow:0 0 0 2.5px #d4a94f,0 7px 0 -1px rgba(0,0,0,.2),0 18px 28px -6px rgba(0,0,0,.32) !important}
.js-sel:not(.is-up):hover{transform:translateY(-2px);box-shadow:0 4px 12px -4px rgba(0,0,0,.25)}
.bx[hidden]{display:none !important}
.bx-mob{display:none}
@container lp (max-width:699px){
 .bx-desk{display:none !important}
 .bx-mob{display:block;position:relative;margin:12px 0 4px}
 .bx-mob[hidden]{display:none !important}
 .bx-mob::before{content:"";position:absolute;left:26px;top:-9px;width:16px;height:16px;background:inherit;border-left:inherit;border-top:inherit;transform:rotate(45deg)}
 .js-sel .sel-chev{display:inline-block}
}
.sel-chev{display:none;width:9px;height:9px;border-right:2.5px solid currentColor;border-bottom:2.5px solid currentColor;transform:rotate(45deg);margin:-4px 2px 0 auto;flex-shrink:0;transition:transform .18s ease}
.js-sel.is-up .sel-chev{transform:rotate(-135deg);margin-top:4px}
@media (prefers-reduced-motion:reduce){.js-sel,.js-sel.is-up{transition:none;transform:none}}
'''
SEL_JS = r'''
(function(){
  var $$=function(s,r){return [].slice.call((r||document).querySelectorAll(s));};
  function pick(g,k,scroll){
    $$('.js-sel[data-grp="'+g+'"]').forEach(function(o){var on=o.getAttribute('data-key')===k;o.classList.toggle('is-up',on);o.setAttribute('aria-expanded',on?'true':'false');});
    $$('[data-box^="'+g+':"]').forEach(function(b){b.hidden=b.getAttribute('data-box')!==g+':'+k;});
    if(scroll){var m=$$('.bx-mob[data-box="'+g+':'+k+'"]').filter(function(b){return b.offsetParent;})[0];if(m&&m.scrollIntoView)m.scrollIntoView({block:'nearest',behavior:'smooth'});}
  }
  $$('.js-sel').forEach(function(b){b.addEventListener('click',function(){pick(b.getAttribute('data-grp'),b.getAttribute('data-key'),true);});});
})();
'''
def sel(grp, key, first, extra=''):
    """Attributes for a pickable element. The first one loads raised with its box open."""
    return ' data-grp="%s" data-key="%s" aria-expanded="%s"%s' % (grp, key, 'true' if first else 'false', extra)
def sel_cls(first):
    return 'js-sel is-up' if first else 'js-sel'
def box(grp, key, inner, first, where, cls=''):
    """where: 'desk' (the shared box on desktop) or 'mob' (right under the element on a phone)."""
    return '<div class="bx bx-%s %s" data-box="%s:%s"%s>%s</div>' % (where, cls, grp, key, '' if first else ' hidden', inner)
CHEV = '<span class="sel-chev" aria-hidden="true"></span>'

def page_v3(t, place, canvas_inner, css, chat, view, title, cls):
    if not FONTS: FONTS.append(embedded_fonts())
    canvas = '<div class="lp-host"><div class="lp bm %s" style="%s">%s</div></div>' % (cls, t['vars'], canvas_inner)
    ch = chat_html(chat)
    body = desktop(t, place, canvas, ch) if view == 'desktop' else mobile(t, place, canvas, ch)
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>%s</title>%s<style>%s%s%s%s%s%s</style></head><body>%s<script>%s%s</script></body></html>') % (
        e(title), FONTS[0], SHELL_CSS, shell_css(t), SHELL_V3_CSS + '.bm-app .sh-bar{background:%s}' % t['ground'], BASE_CSS, SEL_CSS, css, body, JS, SEL_JS)
