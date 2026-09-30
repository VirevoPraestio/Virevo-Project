"""
Export an approved response spec as design-canvas artboards (.dc.html) for the
"Virevo — Discharge Process" design artifact, so the design file and the block library
stay in step. Same canvas markup and CSS as production; chat-panel interactions
(@Point selection, prompts, highlighting the linked canvas item) are wired as
design-component state.

  python3 dc_export.py SPEC.json --view desktop|mobile -o Name.dc.html
"""
import argparse, html, json, re, sys
import diagnosis_html
from preview import SHELL_CSS, TABS, ico, CLIP, MIC, SEND, SHEET, HOME, e

FONTS = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bebas+Neue&amp;family=Poppins:ital,wght@0,400;0,500;0,600;0,700;1,400&amp;family=Caveat:wght@500;700&amp;display=swap">'

def canvas_markup(spec):
    h = diagnosis_html.render_canvas(spec)
    h = re.sub(r'<script type="application/json">.*?</script>', '', h, flags=re.S)       # sums are pre-computed at build time
    h = re.sub(r' data-tj-point="(\d+)"', lambda m: ' data-tj-point="%s" data-lit="{{lit%s}}"' % (m.group(1), m.group(1)), h)
    return h.replace('{{{', '{ {{')

def chat_markup(spec, mobile):
    c = spec['chat']; t = spec.get('turn', {})
    text = c.get('text') or []
    if isinstance(text, str): text = [text]
    paras = ''.join('<p>%s</p>' % e(x) for x in text)
    if c.get('bullets'): paras += '<ul>%s</ul>' % ''.join('<li>%s</li>' % e(b) for b in c['bullets'])
    for k in ('pointer', 'invite'):
        if c.get(k): paras += '<p>%s</p>' % e(c[k])
    user = ('<div class="sh-um">%s%s</div>' % ('<b>%s</b>' % e(t['user_tag']) if t.get('user_tag') else '', e(t['user_message']))) if t.get('user_message') else ''
    note = '<div><div class="sh-lab" style="margin-bottom:4px">Tojo’s note</div><p class="sh-note">%s</p></div>' % e(c['note']) if c.get('note') else ''
    pts = '''<div class="sh-col"><div class="sh-lab">Add to a point — pick one or more</div>
      <sc-for list="{{points}}" as="p" hint-placeholder-count="%d"><button class="sh-pt" aria-pressed="{{p.pressed}}" onClick="{{p.toggle}}"><i>P{{p.n}}</i><span>{{p.label}}</span></button></sc-for></div>''' % len(c.get('points', []))
    prs = '''<div class="sh-col"><div class="sh-lab">Or ask next</div>
      <sc-for list="{{prompts}}" as="q" hint-placeholder-count="3"><button class="sh-pr" onClick="{{q.use}}">{{q.t}}%s</button></sc-for></div>''' % ico(SEND, '#d4a94f', 16)
    return user, '<div class="sh-tm">%s</div>%s%s%s' % (paras, note, pts if c.get('points') else '', prs)

LOGIC = r'''<script type="text/x-dc" data-dc-script data-props='{"$preview":{"width":%(W)d,"height":%(H)d}}'>
class Component extends DCLogic {
  constructor(props) { super(props); this.state = { pts: {}, draft: '' }; }
  renderVals() {
    const P = %(points)s;
    const Q = %(prompts)s;
    const s = this.state;
    const tags = (pts) => P.filter((p) => pts[p.n]).map((p) => '@Point' + p.n);
    const rest = (s.draft || '').replace(/@Point\d+\s*/g, '');
    const out = {
      points: P.map((p) => ({ n: p.n, label: p.label, pressed: !!s.pts[p.n], toggle: () => {
        const pts = { ...s.pts, [p.n]: !s.pts[p.n] }; const t = tags(pts);
        this.setState({ pts, draft: (t.length ? t.join(' ') + ' ' : '') + rest }); } })),
      prompts: Q.map((q) => ({ t: q, use: () => { const t = tags(s.pts); this.setState({ draft: (t.length ? t.join(' ') + ' ' : '') + q }); } })),
      draft: s.draft,
      onDraft: (ev) => this.setState({ draft: ev.target.value })
    };
    for (let n = 1; n <= 9; n++) out['lit' + n] = !!s.pts[n] && P.some((p) => p.n === n && p.canvas);
    return out;
  }
}
</script>'''

def to_dc(spec, view, height):
    user, chat = chat_markup(spec, view == 'mobile')
    ground = diagnosis_html.tone_of(spec)['ground']
    canvas = canvas_markup(spec)
    tool = spec.get('turn', {}).get('tool', 'Discharge Process')
    if view == 'desktop':
        cols = ['#E3E6DF', '#EDE3CB', '#DDE3DE', '#E8E1D4', '#D9DDD6']; hs = [136, 124, 124, 140, 128]
        rail = '<nav class="sh-rail" aria-label="Sections"><a class="sh-home" href="Main.dc.html" aria-label="Home">%s</a>%s</nav>' % (ico(HOME, '#d4a94f', 22), ''.join(
            '<a class="sh-tab" href="#" style="height:%dpx;background:%s">%s</a>' % (h, c, n) for (n, _), c, h in zip(TABS, cols, hs)))
        body = ('<div class="sh-app" style="width:1440px;min-height:%dpx;background:%s">%s<div class="sh-mid"><header class="sh-bar"><div><span class="sh-t">%s</span><small>In conversation with Tojo</small></div>'
                '<div style="display:flex;gap:10px"><button class="sh-btn-o">Guided tour</button><button class="sh-btn-g">Your tasks for the day</button></div></header><main>%s</main></div>'
                '<aside class="sh-chat" aria-label="Chat with Tojo"><div class="sh-panel"><div class="sh-ph"><div class="sh-av">T</div><div><div style="font-family:\'Bebas Neue\',sans-serif;font-size:28px;line-height:1">Tojo</div>'
                '<div style="font-size:12px;color:#9CA9A1">%s</div></div></div><div class="sh-pb">%s%s</div>'
                '<div class="sh-inp"><label for="tojo-input" style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)">Message Tojo</label>'
                '<textarea id="tojo-input" rows="2" placeholder="Write to Tojo…" value="{{draft}}" onChange="{{onDraft}}"></textarea>'
                '<div style="display:flex;align-items:center"><button class="sh-ib" aria-label="Attach a file">%s</button><button class="sh-ib" aria-label="Attach a spreadsheet">%s</button>'
                '<button class="sh-ib" aria-label="Voice note">%s</button><span style="flex-grow:1"></span><button class="sh-send" aria-label="Send">%s</button></div></div></div></aside></div>') % (
            height, ground, rail, e(tool), canvas, e(spec.get('turn', {}).get('context', '')), user, chat, ico(CLIP), ico(SHEET), ico(MIC), ico(SEND, '#10241a'))
        W = 1440
    else:
        foot = ''.join('<a href="#" aria-label="%s">%s</a>' % (n, ico(d, '#F3F1EA', 22)) for n, d in TABS)
        body = ('<div class="sh-m" style="background:%s;min-height:%dpx"><div class="sh-mt"><div style="display:flex;align-items:center;gap:10px"><a href="MobileToday.dc.html" aria-label="Home" style="width:44px;height:44px;border-radius:50%%;background:#10241a;display:flex;align-items:center;justify-content:center">%s</a>'
                '<div><div style="font-family:\'Bebas Neue\',sans-serif;font-size:24px;line-height:1">Virevo</div><div style="font-size:12px;color:#44544A">%s · with Tojo</div></div></div><button class="sh-btn-o">Tour</button></div>'
                '<div class="sh-mc">%s<div class="sh-who"><span class="sh-av" style="width:30px;height:30px;font-size:17px">T</span>Tojo</div>%s<div class="sh-mpanel">%s</div></div>'
                '<div class="sh-mi" style="position:static"><div class="sh-box"><label for="tojo-input" style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)">Message Tojo</label>'
                '<input id="tojo-input" placeholder="Write to Tojo…" value="{{draft}}" onChange="{{onDraft}}">'
                '<button class="sh-ib" style="width:40px;height:40px" aria-label="Attach a file">%s</button><button class="sh-ib" style="width:40px;height:40px;border-radius:50%%;background:rgba(16,36,26,.08)" aria-label="Voice note">%s</button></div>'
                '<button class="sh-send" aria-label="Send">%s</button></div><nav class="sh-mf" style="position:static" aria-label="Sections">%s</nav></div>') % (
            ground, height, ico(HOME, '#d4a94f', 20), e(tool), user, canvas, chat, ico(CLIP, '#10241a', 19), ico(MIC, '#10241a', 19), ico(SEND, '#10241a'), foot)
        W = 390
    css = diagnosis_html.asset('tojo.css') + SHELL_CSS + '\nbody{margin:0}\n.m{margin:0}\n.tj [data-lit="true"]{outline:4px solid #d4a94f;outline-offset:3px}'
    title = '%s — %s' % (spec['canvas']['blocks'][0].get('title', 'Tojo'), view)
    logic = LOGIC % dict(W=W, H=height, points=json.dumps([{'n': p['n'], 'label': p['label'], 'canvas': bool(p.get('canvas'))} for p in spec['chat'].get('points', [])], ensure_ascii=False),
                         prompts=json.dumps(spec['chat']['prompts'], ensure_ascii=False))
    return ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<title>%s</title>\n<script src="./support.js"></script>\n</head>\n<body>\n<x-dc>\n<helmet>\n%s\n<style>\n%s\n</style>\n</helmet>\n%s\n</x-dc>\n%s\n</body>\n</html>\n') % (
        e(title), FONTS, css, body, logic)

def library_dc(width, title, tone='sage'):
    """A design-canvas artboard showing every approved template, rendered from its sample at one canvas width."""
    reg = diagnosis_html.load_registry()
    samples = json.load(open(diagnosis_html.SAMPLES_PATH, encoding='utf-8'))
    ctx = diagnosis_html.Ctx(); parts = []
    for b in reg['blocks']:
        if b['status'] != 'approved' or b['id'] not in samples:
            continue
        inner = diagnosis_html.RENDER[b['id']](dict(samples[b['id']], type=b['id']), ctx)
        inner = re.sub(r'<script type="application/json">.*?</script>', '', inner, flags=re.S)
        parts.append('<section style="display:flex;flex-direction:column;gap:10px;padding-top:26px;border-top:2px solid #10241a">'
                     '<div style="display:flex;align-items:baseline;gap:12px;flex-wrap:wrap"><span style="font-family:\'Bebas Neue\',sans-serif;font-size:30px;line-height:1;color:#10241a">%s</span>'
                     '<span style="font-size:12px;font-weight:600;letter-spacing:.09em;text-transform:uppercase;color:#44544A">%s</span></div>'
                     '<p style="margin:0;font-size:14px;line-height:1.5;color:#44544A;max-width:760px">%s</p>'
                     '<div class="tj" data-theme="sage" data-tone="%s" style="width:%dpx;max-width:100%%"><div class="tj-stack">%s</div></div></section>' % (
                         e(b['id']), e(b['category']), e(b['purpose']), tone, width, inner))
    pad = 24 if width < 500 else 40
    body = ('<div style="box-sizing:border-box;width:%dpx;padding:%dpx;background:#EEF1EC;font-family:Poppins,system-ui,sans-serif;display:flex;flex-direction:column;gap:22px">'
            '<div><div style="font-family:\'Bebas Neue\',sans-serif;font-size:44px;line-height:1;color:#10241a">%s</div><p style="margin:6px 0 0;font-size:14px;color:#44544A">%d approved templates · generated by diagnosis_html from blocks/registry.json and blocks/samples.json</p></div>%s</div>') % (
        width + 2 * pad, pad, e(title), len(parts), ''.join(parts))
    css = diagnosis_html.asset('tojo.css') + '\nbody{margin:0;background:#EEF1EC}'
    logic = '<script type="text/x-dc" data-dc-script data-props=\'{"$preview":{"width":%d,"height":900}}\'>\nclass Component extends DCLogic {\n  renderVals() { return {}; }\n}\n</script>' % (width + 2 * pad)
    return ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<title>%s</title>\n<script src="./support.js"></script>\n</head>\n<body>\n<x-dc>\n<helmet>\n%s\n<style>\n%s\n</style>\n</helmet>\n%s\n</x-dc>\n%s\n</body>\n</html>\n') % (
        e(title), FONTS, css, body, logic)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'library':
        w = int(sys.argv[2]); out = sys.argv[3]; title = sys.argv[4] if len(sys.argv) > 4 else 'Template library'
        open(out, 'w', encoding='utf-8').write(library_dc(w, title)); print('wrote', out); sys.exit(0)
    ap = argparse.ArgumentParser(); ap.add_argument('spec'); ap.add_argument('--view', choices=['desktop', 'mobile'], default='desktop')
    ap.add_argument('--height', type=int, default=900); ap.add_argument('-o', '--out', required=True); a = ap.parse_args()
    spec = json.load(open(a.spec, encoding='utf-8'))
    errs, _ = diagnosis_html.validate(spec)
    if errs: sys.exit('spec does not validate: ' + '; '.join(errs))
    open(a.out, 'w', encoding='utf-8').write(to_dc(spec, a.view, a.height))
    print('wrote', a.out)
