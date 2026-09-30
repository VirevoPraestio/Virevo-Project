"""
Preview shells: wrap a rendered canvas in the Tojo app chrome (Version 3 look) so a turn can be
reviewed end to end — the chat-panel parts Claude writes plus the canvas this generator writes.
The production app owns its own chrome; this is for review and for the gallery of sample turns.
"""
import html, json
e = lambda s: html.escape('' if s is None else str(s), quote=True)

TABS = [('Resources', '<path d="M3 5h6a3 3 0 013 3v12a2 2 0 00-2-2H3z"/><path d="M21 5h-6a3 3 0 00-3 3v12a2 2 0 012-2h7z"/>'),
        ('Diagnosis', '<circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/><path d="M7.5 11h2l1-2 1.5 4 1-2h1.5"/>'),
        ('Solutions', '<path d="M9 18h6"/><path d="M10 21h4"/><path d="M12 3a6 6 0 00-4 10.5c.7.7 1 1.5 1 2.5h6c0-1 .3-1.8 1-2.5A6 6 0 0012 3z"/>'),
        ('Automations', '<path d="M13 3L5 14h6l-1 7 8-11h-6z"/>'),
        ('Processes', '<circle cx="6" cy="6" r="2.5"/><circle cx="18" cy="18" r="2.5"/><path d="M8.5 6H15a3 3 0 013 3v6.5"/><path d="M15.5 13l2.5 2.5 2.5-2.5"/>')]
def ico(d, c='#F3F1EA', w=20):
    return '<svg width="%d" height="%d" viewBox="0 0 24 24" fill="none" stroke="%s" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>' % (w, w, c, d)
CLIP = '<path d="M21 11l-8.5 8.5a5 5 0 01-7-7L14 4a3.5 3.5 0 015 5l-8.5 8.5a2 2 0 01-3-3L15 7"/>'
MIC = '<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0014 0"/><path d="M12 18v3"/>'
SEND = '<path d="M5 12h14"/><path d="M13 6l6 6-6 6"/>'
SHEET = '<rect x="4" y="4" width="16" height="16" rx="1"/><path d="M4 10h16"/><path d="M4 15h16"/><path d="M10 4v16"/>'
HOME = '<path d="M3 11l9-7 9 7"/><path d="M5 10v10h14V10"/>'

SHELL_CSS = '''
.sh-app{display:flex;min-height:100vh;background:#DCE3DA;font-family:Poppins,system-ui,sans-serif;color:#10241a}
.sh-rail{width:84px;flex-shrink:0;display:flex;flex-direction:column;align-items:flex-start;gap:6px;padding-top:24px;border-right:1px solid rgba(16,36,26,.2)}
.sh-rail .sh-home{width:52px;height:52px;margin:0 0 22px 16px;border-radius:50%;background:#10241a;display:flex;align-items:center;justify-content:center}
.sh-rail a.tab{width:60px;border-radius:0 12px 12px 0;color:#10241a;writing-mode:vertical-rl;transform:rotate(180deg);display:flex;align-items:center;justify-content:center;text-decoration:none;font-size:13px;font-weight:600;letter-spacing:.09em;text-transform:uppercase}
.sh-mid{flex-grow:1;min-width:0;display:flex;flex-direction:column}
.sh-bar{height:76px;flex-shrink:0;padding:0 36px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid rgba(16,36,26,.2)}
.sh-bar .sh-t{font-family:'Bebas Neue',sans-serif;font-size:40px;line-height:1}
.sh-bar small{font-size:13px;font-weight:600;letter-spacing:.09em;text-transform:uppercase;color:#44544A;margin-left:14px}
.sh-btn-o{min-height:44px;padding:0 16px;background:transparent;border:1.5px solid #10241a;border-radius:22px;font:500 13px Poppins,sans-serif;color:#10241a}
.sh-btn-g{min-height:44px;padding:0 16px;background:#d4a94f;border:none;border-radius:6px;font:600 13px Poppins,sans-serif;letter-spacing:.05em;text-transform:uppercase;color:#10241a}
.sh-chat{width:420px;flex-shrink:0;padding:20px 20px 20px 0;display:flex}
.sh-panel{flex-grow:1;background:#10241a;border-radius:18px;display:flex;flex-direction:column;overflow:hidden;color:#F3F1EA}
.sh-ph{padding:18px 22px;display:flex;align-items:center;gap:12px;border-bottom:1px solid rgba(243,241,234,.12)}
.sh-av{width:44px;height:44px;border-radius:50%;background:#d4a94f;display:flex;align-items:center;justify-content:center;font-family:'Bebas Neue',sans-serif;font-size:24px;color:#10241a;flex-shrink:0}
.sh-pb{flex-grow:1;padding:20px 22px;display:flex;flex-direction:column;gap:14px}
.sh-um{align-self:flex-end;max-width:310px;background:#d4a94f;color:#10241a;padding:12px 14px;border-radius:16px 4px 16px 16px;font-size:14px;line-height:1.5}
.sh-um b{display:inline-block;margin-right:6px;padding:1px 8px;border-radius:10px;background:#10241a;color:#d4a94f;font-size:12px}
.sh-tm{align-self:flex-start;background:#F3F1EA;color:#2b2b2b;padding:14px 16px;border-radius:4px 16px 16px 16px;font-size:14px;line-height:1.55;display:flex;flex-direction:column;gap:8px}
.sh-tm p{margin:0}.sh-tm ul{margin:0;padding-left:18px}.sh-tm li{margin:2px 0}
.sh-lab{font-size:12px;font-weight:600;letter-spacing:.09em;text-transform:uppercase;color:#9CA9A1}
.sh-note{margin:0;font-family:Caveat,cursive;font-size:31px;font-weight:700;line-height:1.1;color:#d4a94f}
.sh-pt{min-height:44px;width:100%;display:flex;align-items:center;gap:10px;padding:6px 12px 6px 6px;background:rgba(243,241,234,.06);color:#F3F1EA;border:1px solid rgba(243,241,234,.22);border-radius:10px;text-align:left;font:13px/1.35 Poppins,sans-serif;cursor:pointer}
.sh-pt i{flex-shrink:0;min-width:32px;height:32px;border-radius:8px;border:1px solid rgba(243,241,234,.35);display:flex;align-items:center;justify-content:center;font-style:normal;font-size:12px;font-weight:600}
.sh-pt[aria-pressed=true]{background:#d4a94f;color:#10241a;border-color:#d4a94f;font-weight:600}.sh-pt[aria-pressed=true] i{background:#10241a;color:#d4a94f;border-color:#10241a}
.sh-pr{min-height:44px;width:100%;display:flex;align-items:center;justify-content:space-between;gap:10px;padding:8px 14px;background:transparent;color:#F3F1EA;border:1px dashed rgba(212,169,79,.7);border-radius:22px;text-align:left;font:13px Poppins,sans-serif;cursor:pointer}
.sh-opt{min-height:44px;padding:0 16px;background:#F3F1EA;color:#10241a;border:none;border-radius:22px;font:500 13px Poppins,sans-serif;cursor:pointer}
.sh-col{display:flex;flex-direction:column;gap:6px}.sh-row{display:flex;flex-wrap:wrap;gap:8px}
.sh-inp{padding:14px 18px 16px;background:#0b1712;display:flex;flex-direction:column;gap:8px}
.sh-inp textarea{width:100%;box-sizing:border-box;resize:none;background:#F3F1EA;color:#2b2b2b;border:none;border-radius:10px;padding:12px 14px;font:14px/1.5 Poppins,sans-serif;outline:none}
.sh-ib{width:44px;height:44px;border:none;background:transparent;display:flex;align-items:center;justify-content:center;cursor:pointer}
.sh-send{width:48px;height:48px;border-radius:50%;background:#d4a94f;border:none;display:flex;align-items:center;justify-content:center;cursor:pointer}
.sh-m{width:390px;margin:0 auto;min-height:100vh;background:#DCE3DA;display:flex;flex-direction:column;font-family:Poppins,system-ui,sans-serif;color:#10241a}
.sh-mt{padding:14px 16px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid rgba(16,36,26,.2)}
.sh-mc{flex-grow:1;padding:16px 0 20px;display:flex;flex-direction:column;gap:14px}
.sh-mc > .sh-um,.sh-mc > .sh-who{margin:0 14px}.sh-mc > .sh-mpanel{margin:0 14px;background:#10241a;color:#F3F1EA;border-radius:18px;padding:16px;display:flex;flex-direction:column;gap:14px}
.sh-who{display:flex;align-items:center;gap:8px;font-size:12px;font-weight:600;letter-spacing:.09em;text-transform:uppercase;color:#44544A}
.sh-mi{padding:12px 14px;background:#0b1712;display:flex;align-items:center;gap:10px;position:sticky;bottom:64px}
.sh-mi .sh-box{flex-grow:1;min-width:0;display:flex;align-items:center;gap:2px;background:#F3F1EA;border-radius:24px;padding:0 4px 0 16px}
.sh-mi input{flex-grow:1;min-width:0;min-height:48px;border:none;background:transparent;font:14px Poppins,sans-serif;color:#2b2b2b;outline:none}
.sh-mf{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));background:#0b1712;padding:0 8px 12px;border-top:1px solid rgba(243,241,234,.12);position:sticky;bottom:0}
.sh-mf a{height:52px;display:flex;align-items:center;justify-content:center}
.sh-m .tj{border-radius:0}
'''

SHELL_JS = r'''
(function(){
  var input = document.getElementById('tojo-input');
  var canvas = document.querySelector('.tj');
  var pts = Array.prototype.slice.call(document.querySelectorAll('.sh-pt'));
  function sel(){ return pts.filter(function(p){return p.getAttribute('aria-pressed')==='true';}).map(function(p){return parseInt(p.getAttribute('data-n'),10);}); }
  function tags(){ return sel().map(function(n){return '@Point'+n;}).join(' '); }
  function rest(){ return input.value.replace(/@Point\d+\s*/g,''); }
  pts.forEach(function(p){ p.addEventListener('click', function(){
    p.setAttribute('aria-pressed', p.getAttribute('aria-pressed')==='true'?'false':'true');
    var t = tags(); input.value = (t ? t + ' ' : '') + rest(); input.focus();
    if (canvas && window.tojoCanvas) window.tojoCanvas.lightPoints(canvas, sel());
  }); });
  Array.prototype.slice.call(document.querySelectorAll('.sh-pr,.sh-opt')).forEach(function(b){ b.addEventListener('click', function(){
    var t = tags(); input.value = (t ? t + ' ' : '') + b.getAttribute('data-text'); input.focus();
  }); });
})();
'''

def chat_parts(chat):
    out = []
    text = chat.get('text') or []
    if isinstance(text, str): text = [text]
    paras = ''.join('<p>%s</p>' % e(t) for t in text)
    if chat.get('bullets'):
        paras += '<ul>%s</ul>' % ''.join('<li>%s</li>' % e(b) for b in chat['bullets'])
    for k in ('pointer', 'invite'):
        if chat.get(k): paras += '<p>%s</p>' % e(chat[k])
    out.append('<div class="sh-tm">%s</div>' % paras)
    if chat.get('note'):
        out.append('<div><div class="sh-lab" style="margin-bottom:4px">Tojo’s note</div><p class="sh-note">%s</p></div>' % e(chat['note']))
    q = chat.get('question')
    if q:
        out.append('<div class="sh-col"><div class="sh-lab">%s</div><div class="sh-row">%s</div>%s</div>' % (
            e(q['text']), ''.join('<button class="sh-opt" data-text="%s">%s</button>' % (e(o), e(o)) for o in q['options']),
            '<div style="font-size:12px;color:#9CA9A1">Or type your own answer.</div>' if q.get('free_text', True) else ''))
    if chat.get('points'):
        out.append('<div class="sh-col"><div class="sh-lab">Add to a point — pick one or more</div>%s</div>' % ''.join(
            '<button class="sh-pt" aria-pressed="false" data-n="%d"><i>P%d</i><span>%s</span></button>' % (p['n'], p['n'], e(p['label'])) for p in chat['points']))
    if chat.get('prompts'):
        out.append('<div class="sh-col"><div class="sh-lab">Or ask next</div>%s</div>' % ''.join(
            '<button class="sh-pr" data-text="%s">%s%s</button>' % (e(p), e(p), ico(SEND, '#d4a94f', 16)) for p in chat['prompts']))
    return ''.join(out)

def user_msg(spec):
    t = spec.get('turn', {})
    if not t.get('user_message'): return ''
    tag = '<b>%s</b>' % e(t['user_tag']) if t.get('user_tag') else ''
    return '<div class="sh-um">%s%s</div>' % (tag, e(t['user_message']))

def desktop_shell(spec, canvas_html):
    cols = ['#E3E6DF', '#EDE3CB', '#DDE3DE', '#E8E1D4', '#D9DDD6']; hs = [136, 124, 124, 140, 128]
    rail = '<nav class="sh-rail" aria-label="Sections"><a class="sh-home" href="#" aria-label="Home">%s</a>%s</nav>' % (ico(HOME, '#d4a94f', 22), ''.join(
        '<a class="sh-tab" href="#" style="height:%dpx;background:%s">%s</a>' % (h, c, n) for (n, _), c, h in zip(TABS, cols, hs)))
    tool = spec.get('turn', {}).get('tool', 'Discharge Process')
    bar = '<header class="sh-bar"><div><span class="sh-t">%s</span><small>In conversation with Tojo</small></div><div style="display:flex;gap:10px"><button class="sh-btn-o">Guided tour</button><button class="sh-btn-g">Your tasks for the day</button></div></header>' % e(tool)
    panel = ('<aside class="sh-chat" aria-label="Chat with Tojo"><div class="sh-panel"><div class="sh-ph"><div class="sh-av">T</div><div><div style="font-family:\'Bebas Neue\',sans-serif;font-size:28px;line-height:1">Tojo</div>'
             '<div style="font-size:12px;color:#9CA9A1">%s</div></div></div><div class="sh-pb">%s%s</div>'
             '<div class="sh-inp"><label for="tojo-input" style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)">Message Tojo</label><textarea id="tojo-input" rows="2" placeholder="Write to Tojo…"></textarea>'
             '<div style="display:flex;align-items:center"><button class="sh-ib" aria-label="Attach a file">%s</button><button class="sh-ib" aria-label="Attach a spreadsheet">%s</button><button class="sh-ib" aria-label="Voice note">%s</button><span style="flex-grow:1"></span><button class="sh-send" aria-label="Send">%s</button></div></div></div></aside>') % (
        e(spec.get('turn', {}).get('context', '')), user_msg(spec), chat_parts(spec.get('chat', {})), ico(CLIP), ico(SHEET), ico(MIC), ico(SEND, '#10241a'))
    import diagnosis_html
    g = diagnosis_html.tone_of(spec)['ground']
    return '<div class="sh-app" style="background:%s">%s<div class="sh-mid">%s<main>%s</main></div>%s</div>' % (g, rail, bar, canvas_html, panel)

def mobile_shell(spec, canvas_html):
    top = ('<div class="sh-mt"><div style="display:flex;align-items:center;gap:10px"><a href="#" aria-label="Home" style="width:44px;height:44px;border-radius:50%%;background:#10241a;display:flex;align-items:center;justify-content:center">%s</a>'
           '<div><div style="font-family:\'Bebas Neue\',sans-serif;font-size:24px;line-height:1">Virevo</div><div style="font-size:12px;color:#44544A">%s · with Tojo</div></div></div><button class="sh-btn-o">Tour</button></div>') % (
        ico(HOME, '#d4a94f', 20), e(spec.get('turn', {}).get('tool', 'Discharge Process')))
    who = '<div class="sh-who"><span class="sh-av" style="width:30px;height:30px;font-size:17px">T</span>Tojo</div>'
    inp = ('<div class="sh-mi"><div class="sh-box"><label for="tojo-input" style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)">Message Tojo</label><input id="tojo-input" placeholder="Write to Tojo…">'
           '<button class="sh-ib" style="width:40px;height:40px" aria-label="Attach a file">%s</button><button class="sh-ib" style="width:40px;height:40px;border-radius:50%%;background:rgba(16,36,26,.08)" aria-label="Voice note">%s</button></div>'
           '<button class="sh-send" aria-label="Send">%s</button></div>') % (ico(CLIP, '#10241a', 19), ico(MIC, '#10241a', 19), ico(SEND, '#10241a'))
    foot = '<nav class="sh-mf" aria-label="Sections">%s</nav>' % ''.join('<a href="#" aria-label="%s">%s</a>' % (n, ico(d, '#F3F1EA', 22)) for n, d in TABS)
    import diagnosis_html
    g = diagnosis_html.tone_of(spec)['ground']
    return ('<div class="sh-m" style="background:%s">' % g) + '%s<div class="sh-mc">%s%s%s<div class="sh-mpanel">%s</div></div>%s%s</div>' % (
        top, user_msg(spec), who, canvas_html, chat_parts(spec.get('chat', {})), inp, foot)
