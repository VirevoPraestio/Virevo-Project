#!/usr/bin/env python3
"""
dp_automations_html — the Discharge Process Automations generator (v1, 5 Oct 2026).

Draws each Discharge Automations turn from its JSON spec with the latest Automations generator
(Bed Management/automations-html-generator/bm_automations_html.py, loaded as its own copy; see ../dp_common.py): the
library's switch-room motifs (the night shift, the brain, the thinker, the switchboard, the desk helper, the relay, the
station panel) layered with the common tool layer, the three buttons, the background every four turns and the phone
order. Discharge's look (the switch room) is in registry.json and DP_CSS below; its own drawing (file) in dp_au_blocks.py.

  python3 dp_automations_html.py build               # every turn in ../examples/automations/turns.json -> ../out/automations/
Standard library only.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DP = os.path.dirname(HERE)
sys.path[:0] = [HERE, DP]
import dp_common as D          # noqa: E402

base = D.load_base('automations', 'dp_base_automations')
D.point_at_discharge(base, os.path.join(HERE, 'registry.json'), 'dp_automations_html 1.0', ['#D8DDE1', '#DFE3E6', '#D5DADF', '#DCE0E4', '#D7DCE0'])
import dp_au_blocks            # noqa: E402
base.RENDER.update(dp_au_blocks.register({'e': base.e, 'B': base.bm_au_blocks, 'au': base.au}))
base.ITEM_KEYS = tuple(base.ITEM_KEYS) + ('docs',)

DP_CSS = r'''
/* ---- Discharge Process Automations: the switch room ---- */
.ax[data-theme="dp"]{--ground:#E4E7EA;--panel:#F9FAFB;--ink:#1C2A33;--muted:#4B5963;--teal:#0F6E6B;--teal-l:#8FD3CD;--off:#8C98A0;--amber:#8A5608;--gold:#d4a94f;--gold-t:#6B4F16;
  --screen:#16222A;--screen-2:#1F2F38;--glow:#8FD3CD;--red:#8E2F1C;--green:#2F6B4F;--line:rgba(28,42,51,.14);--soft:#EDF0F2;--acc:#0F6E6B;--card:#F9FAFB;
  background-image:radial-gradient(rgba(28,42,51,.07) 1px,transparent 1.2px);background-size:18px 18px;padding:24px 34px 32px}
.ax[data-theme="dp"][data-tone="night"]{--ground:#DCE1E5;--panel:#FCFDFD;--soft:#E8ECEF;background-image:linear-gradient(rgba(28,42,51,.05) 1px,transparent 1px),linear-gradient(90deg,rgba(28,42,51,.05) 1px,transparent 1px);background-size:22px 22px}
@container ax (max-width:699px){.ax[data-theme="dp"]{padding:18px 14px 26px}}
/* the build panel in the switch room's charcoal and teal */
.ax[data-theme="dp"] .pn-board{background:var(--screen);color:#E3EAED}
.ax[data-theme="dp"] .pn-main{border-color:#33464F;background:var(--screen-2)}
.ax[data-theme="dp"] .pn-msw{border-color:#7F9099}.ax[data-theme="dp"] .pn-msw i{background:#7F9099}
.ax[data-theme="dp"] .pn-main em,.ax[data-theme="dp"] .pn-head{color:#AFBDC3}
.ax[data-theme="dp"] .pn-row{background:var(--screen-2);border-color:#2C3E47;color:#E3EAED}
.ax[data-theme="dp"] .pn-row.tl-pick.is-up{background:#10302F!important}
.ax[data-theme="dp"] .pn-n{border-color:#AFBDC3}.ax[data-theme="dp"] .pn-t em{color:#BFCBD0}
.ax[data-theme="dp"] .pn-lamp{border-color:#7F9099}.ax[data-theme="dp"] .pn-lamp.is-on{background:var(--teal)}
.ax[data-theme="dp"] .pn-foot{border-top-color:#33464F;color:#BFCBD0}
'''
base.PAGE_CSS = base.PAGE_CSS + dp_au_blocks.CSS + DP_CSS
_page = base.render_page
def render_page(spec, view, reg, fonts=True):
    return _page(spec, view, reg, fonts).replace('</body></html>', '<script>%s</script></body></html>' % dp_au_blocks.JS, 1)
base.render_page = render_page

_canvas = base.render_canvas
def render_canvas(spec, reg):
    return _canvas(spec, reg).replace('<div class="ax" data-theme="bm"', '<div class="ax" data-theme="dp" data-tool="dp"', 1)
base.render_canvas = render_canvas

def shell_theme(reg, tone):
    k = dict(reg['theme']['tokens'])
    if tone == 'night': k.update({x: reg['tones']['list']['night'][x] for x in ('ground', 'card', 'muted')})
    return base.C.theme(k['ground'], k['card'], k['ink'], k['muted'], k['line'], k['soft'], k['grey'], base.RAIL, '12px', '--acc:%s;--accl:#8FD3CD' % k['accent'])
base.shell_theme = shell_theme

load_registry, validate, render_page, tone_of = base.load_registry, base.validate, base.render_page, base.tone_of

if __name__ == '__main__':
    D.cli('Automations', base, load_registry, validate, render_page, tone_of, base.bmd, base.dh, base.GEN,
          os.path.join(DP, 'examples', 'automations'), os.path.join(DP, 'out', 'automations'), base.C)
