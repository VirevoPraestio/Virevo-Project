"""
odl_common: the parts every OPD Diagnostic Leak page shares.

Loads the latest Bed Management page parts as a private copy (rules/08 §10: one set of latest
generators for every tool) and points them at this tool: its name, its example hospital, and its
own colours. Nothing in Bed Management is changed.

Colours (8 Oct 2026): every page of this tool has its own ground, ink and highlight, and none of
them is used by Discharge Process or Bed Management. The highlight (`--hi`) takes the place the
shared gold takes in the other tools: the raised edge, the first button's bar, the emblem.
"""
import importlib.util, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.dirname(HERE)
BM = os.path.join(TOOLS, 'Bed Management')

_spec = importlib.util.spec_from_file_location('odl_bm_copy', os.path.join(BM, 'bm_common.py'))
B = importlib.util.module_from_spec(_spec)
sys.modules['odl_bm_copy'] = B
_spec.loader.exec_module(B)

TOOL = 'OPD Diagnostic Leak'
HOSPITAL = 'Example hospital · 440 outpatients a day'
B.TOOL = TOOL
B.HOSPITAL[:] = [HOSPITAL]

e, ico, ICONS, CHEV = B.e, B.ico, B.ICONS, B.CHEV
sel, sel_cls, box, pt, tag, say_btn = B.sel, B.sel_cls, B.box, B.pt, B.tag, B.say_btn
masthead, standing, section, pending, actions = B.masthead, B.standing, B.section, B.pending, B.actions
STAMP = {
    'filled': {'at': 'Brought up to date at midnight, 7 October', 'since': '2 conversations since then are not in yet',
               'fresh': 'Brought up to date just now, 11:40 AM', 'fresh_since': 'Everything you have said is in'},
    'empty': {'at': 'Nothing to bring up to date yet', 'since': 'This page fills in as you talk to Tojo',
              'fresh': 'Checked just now, 11:40 AM', 'fresh_since': 'No conversations yet'},
}

# The tool's mark: a prescription slip with a drop falling from its corner.
SLIP_ICO = ('<path d="M6 3h9l3 3v11H6z"/><path d="M9 8h6"/><path d="M9 11h6"/><path d="M9 14h3"/>'
            '<path d="M18 19.5a1.5 1.5 0 01-3 0c0-1 1.5-2.6 1.5-2.6s1.5 1.6 1.5 2.6z"/>')

def emblem(path=SLIP_ICO):
    return '<span class="bm-emb">%s</span>' % ico(path, 'var(--hi)', 30)

# ------------------------------------------------------------------------------------------
# Colours. Ground, card, ink, muted, line, soft, grey, highlight.
RAIL_TINTS = ['#ECE6D6', '#E3E5C3', '#F3D9DE', '#F7DCC2', '#CDEBEB']   # Resources, then the four places in their own grounds
def theme(ground, card, ink, mut, line, soft, grey, hi, btnr='8px'):
    r, g, b = int(ink[1:3], 16), int(ink[3:5], 16), int(ink[5:7], 16)
    hr, hg, hb = int(hi[1:3], 16), int(hi[3:5], 16), int(hi[5:7], 16)
    return {'ground': ground, 'ink': ink, 'hi': hi, 'rail_bg': ink, 'rail_fg': hi, 'rail': RAIL_TINTS,
            'vars': ('--g:%s;--card:%s;--ink:%s;--mut:%s;--line:%s;--soft:%s;--grey:%s;--hi:%s;--hi-soft:rgba(%d,%d,%d,.16);'
                     '--btnr:%s;--gridc:rgba(%d,%d,%d,.05)') % (ground, card, ink, mut, line, soft, grey, hi, hr, hg, hb, btnr, r, g, b)}

THEMES = {
    # Home: saffron paper, warm black ink, vermilion drop
    'home': theme('#F1E3B9', '#FFFAEA', '#2B1E05', '#6B5524', '#DCC58A', '#F8EDCB', '#A8946A', '#E0502A'),
    # Diagnosis: khaki lab bench, olive-black ink, magenta
    'diagnosis': theme('#E3E5C3', '#FCFDF2', '#262B07', '#565D36', '#C3C795', '#EEF0D6', '#9A9E78', '#C92A6A'),
    # Solutions: rose prescription pad, raspberry ink, turquoise
    'solutions': theme('#F3D9DE', '#FFF8F9', '#45102A', '#7A485C', '#E2B3BF', '#FAE8EC', '#B08C97', '#0E8F89'),
    # Automations: apricot, burnt umber ink, cobalt
    'automations': theme('#F7DCC2', '#FFF8F1', '#3A1904', '#714C2C', '#E4BC96', '#FCEADB', '#B5967A', '#2C57CC'),
    # Processes: lagoon, deep sea ink, orange
    'processes': theme('#CDEBEB', '#F6FDFD', '#06323A', '#3B5F65', '#9FCFD0', '#E1F4F4', '#7FA3A6', '#E07F0C'),
}

GOLD = '#d4a94f'
def _accent(css):
    return css.replace('rgba(212,169,79,.55)', 'var(--hi)').replace(GOLD, 'var(--hi)')

def page(t, place, canvas_inner, css, chat, view, title, cls):
    """The Bed Management v3 page, with this tool's highlight in place of the shared gold."""
    html = B.page_v3(t, place, canvas_inner, css, chat, view, title, cls)
    # canvas, rail and app frame take the page's highlight; the root carries the variables for the frame
    html = html.replace(GOLD, t['hi']).replace('rgba(212,169,79,.55)', t['hi'])
    return html.replace('<body>', '<body style="--hi:%s">' % t['hi'], 1)

# ------------------------------------------------------------------------------------------
# Plain English: refuse the registry's listed words in anything a user reads (06 §5.8, F7).
REG = os.path.join(TOOLS, 'Common Elements', 'blocks', 'registry.json')
USER_WORDS = {'OPD'}   # the tool's own name, as Avishek named it
def plain_check(text):
    pe = json.load(open(REG, encoding='utf-8'))['plain_english']
    bad = []
    for w in pe['abbreviations']:
        if w not in USER_WORDS and re.search(r'\b%s\b' % re.escape(w), text): bad.append(w)
    for w in pe['words']:
        if re.search(r'\b%s\b' % re.escape(w), text, re.I): bad.append(w)
    for p, why in pe['patterns']:
        if re.search(p, text): bad.append(why)
    if re.search(r'\btabs?\b', text, re.I): bad.append('tab')
    return bad
