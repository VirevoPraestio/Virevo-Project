"""
tojo_layer — the common tool layer, for every tool and every place (Common Elements).

Two behaviours any generator can put on top of a library block, without changing the block's own look:

  picking  An item of a drawing (an event, a step, a row) carries pick_attrs(). The first item loads raised
           (lifted, gold edge, solid and soft shadow) with its sheet open. Tapping another raises it and opens
           its sheet; the rest drop back. Each sheet exists twice: one shared desktop sheet (class bx-desk,
           inside bx-desk-wrap) and one right under its item on a phone (class bx-mob). Both carry
           data-box="group:key".
  entries  entry() puts an "Add yours" field inside the drawing. What the user types goes into the chat message
           with the place it came from, under "Added on the drawing:". Every entry is added; none replaces
           another. A prompt or option sets the first line of the message and keeps the entries.
           (Avishek, 30 Sep 2026: data is entered in the HTML itself, and entries append.)

Used by Bed Management first (bm_diagnosis_html.py). Colours come from the page's own variables
(--gold, --acc, --ink, --card, --green, --muted), so the layer takes each tool's look.
Standard library only.
"""
import html

e = lambda s: html.escape('' if s is None else str(s), quote=True)

def pick_attrs(grp, key, first, extra_cls=''):
    """Attributes for a pickable item. The first one loads raised with its sheet open."""
    return ' class="tl-pick%s%s" data-grp="%s" data-key="%s" aria-expanded="%s"' % (
        ' is-up' if first else '', (' ' + extra_cls) if extra_cls else '', grp, key, 'true' if first else 'false')

def entry(label, question, placeholder, cls=''):
    """An inline entry. label: how the entry is named in the chat message. question: shown above the button."""
    return ('<div class="tl-entry%s" data-entry-label="%s"><div class="tj-label">%s</div>'
            '<button type="button" class="tl-add" aria-expanded="false"><span class="tl-plus" aria-hidden="true"></span><span class="shut">Add yours</span><span class="open">Close</span></button>'
            '<div class="tl-field" hidden><label class="sr">%s</label><textarea rows="2" placeholder="%s"></textarea>'
            '<span class="tl-inmsg" hidden>In your message</span></div></div>') % (
        (' ' + cls) if cls else '', e(label), e(question), e(question), e(placeholder))

def hint(text):
    return '<p class="tl-hint">%s</p>' % e(text)

RUNTIME = r'''
(function(){
  var $$=function(s,r){return [].slice.call((r||document).querySelectorAll(s));};
  var input=document.getElementById('tojo-input');
  /* ---- picking: first item raised with its sheet open; tap another to switch */
  function pick(g,k,scroll){
    $$('.tl-pick[data-grp="'+g+'"]').forEach(function(o){var on=o.getAttribute('data-key')===k;o.classList.toggle('is-up',on);o.setAttribute('aria-expanded',on?'true':'false');});
    $$('[data-box^="'+g+':"]').forEach(function(b){b.hidden=b.getAttribute('data-box')!==g+':'+k;});
    if(scroll){var m=$$('.bx-mob[data-box="'+g+':'+k+'"]').filter(function(b){return b.offsetParent;})[0];if(m&&m.scrollIntoView)m.scrollIntoView({block:'nearest',behavior:'smooth'});}
  }
  $$('.tl-pick').forEach(function(b){
    b.addEventListener('click',function(){pick(b.getAttribute('data-grp'),b.getAttribute('data-key'),true);});
    b.addEventListener('keydown',function(ev){if(ev.key==='Enter'||ev.key===' '){ev.preventDefault();b.click();}});});
  /* ---- the message: what the user picked or typed (lead) + @points + every entry made on the drawing */
  var lead='', entries=[];   /* entries: [{label, value}] in the order first made */
  function tags(){return $$('.sh-pt[aria-pressed=true]').map(function(p){return '@Point'+p.getAttribute('data-n');}).join(' ');}
  function compose(){
    var head=[tags(),lead].filter(Boolean).join(' ');
    var list=entries.filter(function(x){return x.value.trim();}).map(function(x){return '• '+x.label+': '+x.value.trim();});
    input.value=head+(list.length?(head?'\n\n':'')+'Added on the drawing:\n'+list.join('\n'):'');
    grow();
  }
  function grow(){input.style.height='auto';input.style.height=Math.min(input.scrollHeight,260)+'px';}
  input.addEventListener('input',function(){var v=input.value,i=v.indexOf('Added on the drawing:');lead=(i<0?v:v.slice(0,i)).replace(/@Point\d+\s*/g,'').trim();grow();});
  $$('.sh-pr,.sh-opt').forEach(function(b){b.addEventListener('click',function(){lead=b.getAttribute('data-text');compose();input.focus();});});
  $$('.sh-pt').forEach(function(p){p.addEventListener('click',function(){
    p.setAttribute('aria-pressed',p.getAttribute('aria-pressed')==='true'?'false':'true');
    var on=$$('.sh-pt[aria-pressed=true]').map(function(x){return x.getAttribute('data-n');});
    $$('.tj [data-tj-point]').forEach(function(el){el.classList.toggle('tj-lit',on.indexOf(el.getAttribute('data-tj-point'))>=0);});
    compose();});});
  $$('.tl-entry').forEach(function(box){
    var btn=box.querySelector('.tl-add'),field=box.querySelector('.tl-field'),ta=box.querySelector('textarea'),ok=box.querySelector('.tl-inmsg');
    var rec={label:box.getAttribute('data-entry-label'),value:''};
    btn.addEventListener('click',function(ev){ev.stopPropagation();var open=field.hidden;field.hidden=!open;btn.setAttribute('aria-expanded',open?'true':'false');if(open)ta.focus();});
    ta.addEventListener('click',function(ev){ev.stopPropagation();});
    ta.addEventListener('input',function(){
      rec.value=ta.value;if(entries.indexOf(rec)<0)entries.push(rec);
      ok.hidden=!ta.value.trim();box.classList.toggle('has-entry',!!ta.value.trim());compose();});
  });
  /* the sheets of one item exist twice (desktop and phone): keep the two fields in step */
  $$('.tl-entry textarea').forEach(function(ta){ta.addEventListener('input',function(){
    var lab=ta.closest('.tl-entry').getAttribute('data-entry-label');
    $$('.tl-entry[data-entry-label="'+lab.replace(/"/g,'\\"')+'"] textarea').forEach(function(o){if(o!==ta&&o.value!==ta.value){o.value=ta.value;
      var b=o.closest('.tl-entry');b.querySelector('.tl-inmsg').hidden=!ta.value.trim();b.classList.toggle('has-entry',!!ta.value.trim());}});});});
})();
'''

CSS = r'''.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
.tl-hint{margin:0;font-size:12.5px;font-style:italic;color:var(--muted)}
/* picking: raised, gold edge, solid and soft shadow (standing rule 4) */
.tl-pick{cursor:pointer;transition:transform .18s ease,box-shadow .18s ease,background-color .18s}
.tl-pick.is-up{position:relative;z-index:3;transform:translateY(-5px);box-shadow:0 0 0 2.5px var(--gold),0 7px 0 -1px rgba(26,43,69,.22),0 18px 28px -8px rgba(26,43,69,.34)!important;background:#FFF8E6!important}
.tl-pick:not(.is-up):hover{transform:translateY(-2px)}
.tl-pick:focus-visible{outline:3px solid var(--gold);outline-offset:3px}
.bx[hidden]{display:none!important}
.bx-mob{display:none}
.bx-desk-wrap{display:block}
.tl-entry{display:flex;flex-direction:column;gap:10px;align-items:flex-start}
.tl-entry .tj-label{color:var(--ink);font-size:12.5px;line-height:1.45}
.tl-add{display:inline-flex;align-items:center;gap:8px;min-height:44px;padding:0 18px;border:2px dashed var(--acc);border-radius:22px;background:transparent;color:var(--acc)!important;font-size:14px;font-weight:600}
.tl-add[aria-expanded=true]{border-style:solid;background:var(--acc);color:#fff!important}
.tl-add[aria-expanded=true] .shut,.tl-add[aria-expanded=false] .open{display:none}
.tl-plus{position:relative;width:12px;height:12px}.tl-plus::before,.tl-plus::after{content:"";position:absolute;background:currentColor;left:5px;top:0;width:2px;height:12px}.tl-plus::after{transform:rotate(90deg)}
.tl-add[aria-expanded=true] .tl-plus{transform:rotate(45deg)}
.tl-field{display:flex;flex-direction:column;gap:6px;width:100%}
.tl-field[hidden]{display:none}
.tl-field textarea{width:100%;min-height:64px;resize:vertical;font:inherit;font-size:15px;line-height:1.45;color:var(--ink);background:var(--card);border:2px dashed var(--acc);border-radius:6px;padding:10px 12px}
.tl-entry.has-entry .tl-field textarea{border-style:solid;border-color:var(--green)}
.tl-inmsg{display:inline-flex;align-items:center;gap:6px;font-size:12.5px;font-weight:600;color:var(--green)}
.tl-inmsg::before{content:"";width:6px;height:11px;border-right:2.5px solid currentColor;border-bottom:2.5px solid currentColor;transform:rotate(45deg);margin:-3px 4px 0 2px}
.tl-more-entry{padding:18px 22px;border-style:dashed;border-color:var(--acc)}
@container tj (max-width:699px){
 .bx-desk-wrap{display:none!important}
 .bx-mob{display:grid;margin:8px 0 12px}
 .bx-mob[hidden]{display:none!important}
}
@media (prefers-reduced-motion:reduce){.tl-pick,.tl-pick.is-up{transition:none;transform:none!important}}
'''
