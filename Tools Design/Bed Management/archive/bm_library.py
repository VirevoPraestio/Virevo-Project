"""
Adds the approved Bed Management landing pages (v3, 30 Sep 2026) to the Tojo block library,
and marks every landing page with its tool: Discharge Process or Bed Management.

  python3 bm_library.py IN.html OUT.html

IN is the current block library (the live artifact's saved copy). The Bed Management pages are
drawn by v3.py and shown in frames, so their styles never touch the rest of the library.
Running it twice is safe: an earlier Bed Management section is replaced.
"""
import html, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bm_common as C
from landing_common import GOOGLE_FONTS
import v3

ROWS = [
 ('home', 'Home · The ward plan', 'home B', 'Bed Management home page, the ward plan.',
  'A ward seen from above: one room for each place off one corridor, a small bed for each step, the nurses’ station counting the beds made up. Tap a small bed to read its step.'),
 ('diagnosis', 'Diagnosis · The morning count', 'landing B', 'Diagnosis landing page, the morning count.',
  'One example ward of 20 beds at 8 AM, 11 AM, 2 PM and 5 PM, a day strip of arrivals against beds coming free, the five stages as doors, the evidence pinned.'),
 ('solutions', 'Solutions · The corridor of fixes', 'landing B', 'Solutions landing page, the corridor of fixes.',
  'Each fix is a room off one corridor, its door plate carrying the four stops from idea to agreed. Tap a room for what it is, what it depends on and how it was drawn.'),
 ('automations', 'Automations · The station panel', 'landing C', 'Automations landing page, the station panel.',
  'The nurses’ station status panel: the main switch on top, one row of four lamps for each automation, idea to switched on. Tap a row for what it does and needs.'),
 ('processes', 'Processes · The trial ward', 'landing B', 'Processes landing page, the trial ward.',
  'One ward seen from above with each change pinned where it happens, seats for new roles at the station, the measures on its wall and the two-week trial at the foot.'),
]
RULES = ('Chat one screen tall with its own scroll · desktop header fixed to the line under Refresh now · '
         'first element raised with its box open · on a phone each box opens right under its element.')

CSS = '''
<style>
.g-tool{justify-self:start;align-self:start;display:inline-block;margin:8px 0 8px 6px;padding:2px 10px;border-radius:12px;font-size:12px;font-weight:600;border:1.5px solid}
.g-tool-dp{background:#EEF2EC;color:#10241a;border-color:#10241a}
.g-tool-bm{background:#1C2542;color:#F3F1EA;border-color:#1C2542}
.bm-lib-frame{position:relative;overflow:hidden;border:1.5px solid #d6d0c2;border-radius:10px;background:#fff}
.bm-lib-frame iframe{border:0;display:block;transform-origin:0 0}
.bm-lib-st{display:inline-flex;margin-top:10px;border:1.5px solid #10241a;border-radius:20px;overflow:hidden}
.bm-lib-st button{min-height:40px;padding:0 16px;border:0;background:#fff;font:500 13px Poppins,sans-serif;color:#10241a;cursor:pointer}
.bm-lib-st button[aria-pressed=true]{background:#d4a94f;font-weight:600}
.bm-lib-phone{border:10px solid #1b1b1b;border-radius:34px;overflow:hidden;width:390px;background:#fff}
.bm-lib-phone iframe{border:0;display:block;width:390px;height:844px}
</style>'''

JS = r'''<script>
(function(){
  [].slice.call(document.querySelectorAll('.bm-lib-row')).forEach(function(row){
    var st=[].slice.call(row.querySelectorAll('.bm-lib-st button'));
    st.forEach(function(b){b.addEventListener('click',function(){
      var s=b.getAttribute('data-st');
      [].slice.call(row.querySelectorAll('.bm-lib-st button')).forEach(function(o){o.setAttribute('aria-pressed',o.getAttribute('data-st')===s?'true':'false');});
      [].slice.call(row.querySelectorAll('iframe[data-v]')).forEach(function(f){
        if(!f.hasAttribute('data-filled'))f.setAttribute('data-filled',f.getAttribute('srcdoc'));
        f.setAttribute('srcdoc',f.getAttribute('data-'+s));});});});
  });
})();
</script>'''

def light(page):
    """Each frame carries its own fonts, so it looks right with no network."""
    return page

def section(pages):
    rows = []
    for k, title, tmpl, lead, what in ROWS:
        tpls = ''
        rows.append((
            '<section class="g-row bm-lib-row" id="bm-landing-%s"><div class="g-meta"><div class="g-id">%s <span>%s · v3</span></div>'
            '<span class="g-status" style="background:#2f7350">approved in landing page</span>'
            '<span class="g-scope g-scope-one" title="Only the Bed Management tool uses this template">Bed Management only</span>'
            '<span class="g-tool g-tool-bm">Tool: Bed Management</span>'
            '<p><b>%s</b> %s</p><p class="g-small">%s</p></div>'
            '<div class="g-views"><div><div class="g-cap">Desktop · one 1440 × 900 screen, shown at 75%%</div>'
            '<div class="bm-lib-frame" style="width:1080px;height:675px"><iframe data-v="desktop" title="%s, desktop" style="width:1440px;height:900px;transform:scale(.75)" srcdoc="%s" data-empty="%s"></iframe></div>'
            '<div class="bm-lib-st" role="group" aria-label="Page state"><button type="button" data-st="filled" aria-pressed="true">In progress</button><button type="button" data-st="empty" aria-pressed="false">First visit</button></div></div>'
            '<div><div class="g-cap">Phone · 390 × 844</div><div class="bm-lib-phone"><iframe data-v="mobile" title="%s, phone" srcdoc="%s" data-empty="%s"></iframe></div></div></div>%s</section>') % (
            k, html.escape(title), tmpl, html.escape(lead), html.escape(what), html.escape(RULES), html.escape(title),
            html.escape(light(pages['%s.desktop.filled' % k]), quote=True), html.escape(light(pages['%s.desktop.empty' % k]), quote=True),
            html.escape(title), html.escape(light(pages['%s.mobile.filled' % k]), quote=True), html.escape(light(pages['%s.mobile.empty' % k]), quote=True), tpls))
    head = ('<!--bm-landing-start--><h2 class="g-h2" id="bm-landing-pages">Approved landing pages · Bed Management</h2>'
            '<p class="g-lead">The Bed Management tool’s own home page and its four place pages, approved 30 September 2026. Each has its own look, taken from the ward plan '
            'on the home page. They belong to Bed Management only and are not the Discharge Process pages above. Each frame is one real screen: scroll inside it.</p>')
    return head + ''.join(rows) + '<!--bm-landing-end-->'

def unwrap(src):
    """The saved copy of a published page carries the publishing wrapper; keep only the page itself."""
    i = src.find('<!doctype html>', 20)
    if src.startswith('<!doctype html><html><head><meta charset=utf8>') and i > 0:
        src = src[i:]
        j = src.rfind('</html>', 0, src.rfind('</html>'))
        if j > 0: src = src[:j + 7]
    return src

def inject(src, pages):
    src = unwrap(src)
    s = re.sub(r'<!--bm-landing-start-->.*?<!--bm-landing-end-->', '', src, flags=re.S)
    s = s.replace('<h2 class="g-h2" id="landing-pages">Approved landing pages</h2>', '<h2 class="g-h2" id="landing-pages">Approved landing pages · Discharge Process</h2>')
    for tab in ('Diagnosis', 'Solutions', 'Automations', 'Processes'):
        a = '>%s only</span><p><b>%s landing page' % (tab, tab)
        if a in s and 'g-tool-dp' not in s.split(a)[1][:400]:
            s = s.replace(a, '>%s only</span><span class="g-tool g-tool-dp">Tool: Discharge Process</span><p><b>%s landing page' % (tab, tab), 1)
    s = s.replace('<h2 class="g-h2" id="shared-parts">', section(pages) + '<h2 class="g-h2" id="shared-parts">', 1)
    toc = ('<a href="#bm-landing-pages" style="background:#1C2542;color:#F3F1EA">Bed Management pages</a>'
           + ''.join('<a href="#bm-landing-%s">bm-%s</a>' % (k, k) for k, *_ in ROWS))
    if 'href="#bm-landing-pages"' not in s:
        s = s.replace('<a href="#shared-parts" style="background:#10241a;color:#F3F1EA">Shared parts</a>', toc + '<a href="#shared-parts" style="background:#10241a;color:#F3F1EA">Shared parts</a>', 1)
    lead_add = ' Landing pages carry a second badge naming their tool: <b>Tool: Discharge Process</b> or <b>Tool: Bed Management</b>. The five Bed Management pages sit in their own section.'
    if 'Tool: Bed Management</b>' not in s:
        s = s.replace('mean only that place uses it.</p>', 'mean only that place uses it.' + lead_add + '</p>', 1)
    if 'g-tool-bm{' not in s:
        s = s.replace('</head>', CSS + '</head>', 1)
    if 'bm-lib-row' in s and "querySelectorAll('.bm-lib-row')" not in s:
        a, b, c = s.rpartition('</body>')
        s = a + JS + b + c
    return s

if __name__ == '__main__':
    src, out = sys.argv[1], sys.argv[2]
    pages = v3.build()
    open(out, 'w').write(inject(open(src).read(), pages))
    print('wrote', out, os.path.getsize(out))
