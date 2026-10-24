(function(){
  var $=function(s,r){return (r||document).querySelector(s)};
  var $$=function(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s))};
  var reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
  var KEY='tojoTours';
  function load(){try{return JSON.parse(localStorage.getItem(KEY)||'{}')}catch(e){return {}}}
  function save(o){try{localStorage.setItem(KEY,JSON.stringify(o))}catch(e){}}
  function prog(n){return load()['t'+n]||{step:0,finished:false}}
  function setProg(n,p){var s=load(); s['t'+n]=p; s.last=n; save(s)}

  var picker=$('#picker'), area=$('#tourArea'), box=$('#stageBox'), stage=$('#stage'), app=$('#app'), scroller=$('#scroll'), card=$('#card'), ov=$('#ov'), toast=$('#toast'), nav=$('#nav'), tchat=$('#threadChat');
  var LATER='We’ll open this up properly in its own tour.';
  var Q='Discharges are slipping past 2pm on Ward 4 — where is it going wrong?';

  /* ================= app behaviour ================= */
  var listeners=[];
  function fire(ev){var n=0; listeners.slice().forEach(function(l){if(l.ev===ev){l.fn(); n++}}); return n}
  function on(ev,fn){var l={ev:ev,fn:fn}; listeners.push(l); return function(){listeners=listeners.filter(function(x){return x!==l})}}
  var tt; function say(m){toast.textContent=m; toast.classList.add('on'); clearTimeout(tt); tt=setTimeout(function(){toast.classList.remove('on')},2600)}

  $$('.ni[data-sub]').forEach(function(n){n.addEventListener('click',function(){var s=document.getElementById(n.dataset.sub); var o=!s.classList.contains('open'); s.classList.toggle('open',o); n.classList.toggle('open',o); fire('expand:'+n.id)})});
  $('#sun').addEventListener('click',function(){app.classList.toggle('light'); fire('sun')});
  $('#chipKpi').addEventListener('click',function(){var t=$('#ask'); t.value='Show me this week’s bed management KPIs: occupancy, bed turnaround, and discharges before noon, ward by ward.'; fire('chip')});
  $('#send').addEventListener('click',function(){if(!fire('send'))say('Sending is off in the tour, so nothing is sent or billed.')});
  $('#addpb').addEventListener('click',function(){var b=$('#addpb'); if(!b.classList.contains('naming')){b.classList.add('naming'); setTimeout(function(){$('#pbName').focus()},50); fire('pb')}});
  $('#pbName').addEventListener('keydown',function(e){if(e.key==='Enter'){e.preventDefault(); var v=this.value.trim(); say(v?'“'+v+'” would be created. Not saved in the tour.':'Type a name first.')}});
  $$('.side .ni, .side .newchat').forEach(function(n){n.addEventListener('mouseenter',function(){fire('hoverside')}); n.addEventListener('touchstart',function(){fire('hoverside')},{passive:true})});
  $$('.pc').forEach(function(n){n.addEventListener('mouseenter',function(){fire('hovercard')}); n.addEventListener('click',function(){n.classList.toggle('hov'); fire('hovercard')})});
  $('#newchat').addEventListener('click',function(){view('home'); scroller.scrollTop=0; var t=$('#ask'); t.value=''; t.focus({preventScroll:true}); fire('newchat')});
  var typedOnce=false;
  $('#ask').addEventListener('input',function(){if(!typedOnce&&/ward\s*4/i.test(this.value)){typedOnce=true; var t=this; setTimeout(function(){t.value=Q; fire('typed')},250)}});
  document.addEventListener('keydown',function(e){if(area.hidden)return; if((e.ctrlKey||e.metaKey)&&(e.key==='k'||e.key==='K')){e.preventDefault(); $('#newchat').click()} else if(e.key==='Escape')skip()});
  /* thread */
  var STOPD=[['The bill','A running total from day one.','Made after the decision.'],['The discharge summary','Drafts itself from daily notes.','Typed from paper files.'],['Medicines and supplies','Ordered and returned by likely use.','Counted by hand at the end.'],['Doctors’ advice and notes','Recorded digitally, by voice if needed.','On paper, typed up later.']];
  $$('.stp').forEach(function(b){b.addEventListener('click',function(){$$('.stp').forEach(function(x){x.classList.toggle('on',x.dataset.s===b.dataset.s)}); var d=STOPD[+b.dataset.s]; $('#stopD').innerHTML='<b>'+d[0]+'</b><span class="row2"><span><small>The Tojo way</small>'+d[1]+'</span><span><small>Today</small>'+d[2]+'</span></span>'; fire('stop')})});
  $$('.pts button').forEach(function(b){b.addEventListener('click',function(){var el=document.getElementById(b.dataset.pt); if(!el)return; el.classList.add('hl'); if(el.classList.contains('stp'))el.click(); setTimeout(function(){el.classList.remove('hl')},1800); fire('stop')})});
  $$('.ctabs button').forEach(function(b){b.addEventListener('click',function(){$$('.ctabs button').forEach(function(x){x.classList.toggle('on',x===b)}); $$('.cpane').forEach(function(p){p.hidden=p.dataset.cp!==b.dataset.ct}); if(b.dataset.ct==='src')fire('sources')})});
  $('#ctxBtn').addEventListener('click',function(){$('#ctxPanel').classList.toggle('open')});
  function ctxTab(t){$$('.ctabs button').forEach(function(x){x.classList.toggle('on',x.dataset.ct===t)}); $$('.cpane').forEach(function(p){p.hidden=p.dataset.cp!==t})}

  function view(v){app.dataset.view=v}
  function resetThread(){clearTimeout(revealT); lit=null; $$('#threadView .part').forEach(function(p){p.classList.add('pend')}); $('#ctxPanel').classList.remove('open'); ctxTab('vis'); $$('.stp').forEach(function(x){x.classList.remove('on')}); $('#stopD').innerHTML='<b>Tap any stop.</b> Each shows what changes, today against the Tojo way.'; tchat.scrollTop=0}
  function showThread(){clearTimeout(revealT); lit=null; view('thread'); $$('#threadView .part').forEach(function(p){p.classList.remove('pend')})}
  var PARTS=[['pVerdict','the verdict, first line'],['pCauses','the causes, two or three'],['canvasDraw','the drawing that shows them'],['pNote','Tojo’s Note, in his own hand'],['pPoints','@points, each linked to the drawing'],['pAsk','one question back, never five'],['prompts','three likely next questions']];
  var lit=null, revealT=null;
  function reveal(){view('thread'); resetThread(); var i=0;
    (function nx(){ if(i>=PARTS.length){lit=null; fire('revealed'); return}
      var id=PARTS[i][0], el=document.getElementById(id); el.classList.remove('pend');
      if(el.parentNode===tchat)tchat.scrollTop=Math.max(0,el.offsetTop-tchat.clientHeight+el.offsetHeight+20);
      lit=id; var lb=$('#partLbl'); if(lb)lb.textContent='Now: '+PARTS[i][1]; i++; revealT=setTimeout(nx,reduce?400:1600)})();
  }

  /* ================= comparison scene (Tour 3) ================= */
  var CQ='Insurance approvals keep delaying our patient discharges. We’ve tried everything. Should we just accept this?';
  var gEls=$$('#gWin > *'), cmpT=[], cmpLit=null;
  function words(el){return (el.textContent.trim().match(/\S+/g)||[]).length}
  var gTotal=gEls.reduce(function(a,e){return a+words(e)},0), gQs=(($('#gWin').textContent.match(/\?/g))||[]).length;
  function resetCmp(){cmpT.forEach(clearTimeout); cmpT=[]; cmpLit=null; $$('.cqt').forEach(function(q){q.textContent=CQ}); gEls.forEach(function(e){e.classList.add('off')}); $('#gW').textContent='0'; $('#gT').textContent='0'; $('#gQ').textContent='0'; $('#gD').textContent='0'; $$('#gFlags li').forEach(function(l){l.classList.add('off')}); $$('#cmpRead > span, .zero').forEach(function(s){s.classList.add('off')}); $('#cmpTojo').classList.add('off'); $('#wis').classList.add('off'); $('#tW').textContent='0'}
  function showCmpAll(){cmpT.forEach(clearTimeout); cmpT=[]; cmpLit=null; gEls.forEach(function(e){e.classList.remove('off')}); $('#gW').textContent=gTotal; $('#gT').textContent=(gTotal/230).toFixed(1); $('#gQ').textContent=gQs; $$('#gFlags li, #cmpRead > span, .zero').forEach(function(s){s.classList.remove('off')}); $('#cmpTojo').classList.remove('off'); $('#wis').classList.remove('off'); $('#tW').textContent=words($('#cmpTojo .av1'))+words($('#cmpTojo p:nth-of-type(2)'))}
  function at(ms,fn){cmpT.push(setTimeout(fn,reduce?Math.min(ms,50):ms))}
  function playCmp(){resetCmp(); var w=$('#gWin'), acc=0, n=gEls.length, step=Math.max(90,Math.floor(6500/n)); cmpLit='cmpGen'; setLbl('the generic AI writes');
    gEls.forEach(function(e,i){at(300+i*step,function(){e.classList.remove('off'); acc+=words(e); w.scrollTop=w.scrollHeight; $('#gW').textContent=acc; $('#gT').textContent=(acc/230).toFixed(1); if(/\?/.test(e.textContent))$('#gQ').textContent=+$('#gQ').textContent+(e.textContent.match(/\?/g)||[]).length})});
    var t0=300+n*step+300;
    $$('#gFlags li').forEach(function(l,i){at(t0+i*600,function(){l.classList.remove('off')})});
    var t1=t0+2200; at(t1,function(){cmpLit='cmpRead'; setLbl('Tojo reads his own library')});
    $$('#cmpRead > span').forEach(function(s,i){at(t1+300+i*450,function(){s.classList.remove('off')})});
    at(t1+300+6*450,function(){$('.zero').classList.remove('off')});
    var t2=t1+300+6*450+900; at(t2,function(){cmpLit='cmpTojo'; setLbl('Tojo answers: a few lines and one drawing'); $('#cmpTojo').classList.remove('off'); $('#tW').textContent=words($('#cmpTojo .av1'))+words($('#cmpTojo p:nth-of-type(2)'))});
    at(t2+2200,function(){$('#wis').classList.remove('off'); cmpLit=null; fire('played')});
  }
  function setLbl(t){var lb=$('#partLbl'); if(lb)lb.textContent='Now: '+t}

  /* ================= the real Tool (Tour 3) =================
     The Discharge Tool is the live page itself (its own HTML, CSS and script,
     captured from virevo.works/discharge), loaded into a frame over the stage.
     Selectors that start with "T:" point inside it. */
  var frame=$('#toolFrame'), toolLoaded=false, toolWait=[];
  function TD(){try{return toolLoaded?frame.contentDocument:null}catch(e){return null}}
  function openTool(fresh,then){
    frame.hidden=false;
    if(then)toolWait.push(then);
    if(fresh||!frame.dataset.on){toolLoaded=false; frame.dataset.on='1'; frame.srcdoc=TOOLDOC; setTimeout(function(){if(!toolLoaded&&!frame.hidden)say('The Discharge Tool is taking long to open here. Try Restart this tour.')},9000)}
    else if(toolLoaded){var w=toolWait; toolWait=[]; w.forEach(function(f){f()})}
  }
  function closeTool(){frame.hidden=true}
  window.__tojoTool=function(href){ if(href==='/chat'){closeTool(); view('home'); scroller.scrollTop=0; fire('toolhome')} else openTool(true) };
  frame.addEventListener('load',function(){
    var d=frame.contentDocument; if(!d||!d.getElementById('dis'))return;
    toolLoaded=true; var dis=d.getElementById('dis');
    new MutationObserver(function(){fire('tool:view'+dis.getAttribute('data-view')); var p=dis.getAttribute('data-panel'); if(p)fire('tool:panel:'+p)}).observe(dis,{attributes:true,attributeFilter:['data-view','data-panel']});
    d.addEventListener('click',function(e){var t=e.target; if(!t.closest)return; if(t.closest('.rm-hit'))fire('tool:stop'); if(t.closest('#resources [aria-pressed]'))fire('tool:pill')});
    var main=d.getElementById('disMain'); if(main)main.addEventListener('scroll',function(){place()});
    toolLock(); simLock(); suiteLock(); var w=toolWait; toolWait=[]; w.forEach(function(f){f()});
    fire('toolopen');
  });
  function toolLock(){var d=TD(); if(!d)return; var on=!area.hidden&&tIx===2&&idx<stepsN(); d.documentElement.classList.toggle('tour-lock',on)}
  var DESKKEY={dx:'diagnosis',sol:'solutions',aut:'automations',prc:'processes'};
  function toolDesk(p){openTool(false,function(){var d=TD(), dis=d.getElementById('dis'); if(dis.getAttribute('data-panel')===p)return; var a=d.querySelector('.rail-tab[href="#'+DESKKEY[p]+'"]'); if(a)a.click()})}
  function toolSheet(){var d=TD(); if(!d)return; var dis=d.getElementById('dis'); if(dis.hasAttribute('data-panel')){dis.removeAttribute('data-panel'); $$('.rail-tab',d).forEach(function(x){x.removeAttribute('aria-current')}); var b=d.getElementById('barW'); if(b)b.textContent='with Tojo'}}
  function tScrollTo(sel){var d=TD(); if(!d)return; var el=d.querySelector(sel); if(!el)return; var m=d.getElementById('disMain'), w=d.defaultView; var y=el.getBoundingClientRect().top; if(m&&/(auto|scroll)/.test(w.getComputedStyle(m).overflowY)){m.scrollTop+=y-m.getBoundingClientRect().top-260} else w.scrollBy(0,y-260)}
  function toolView1(){openTool(false,function(){var d=TD(); if(d.getElementById('dis').getAttribute('data-view')!=='1')openTool(true); else toolSheet()})}
  function toolView2(){openTool(false,function(){var d=TD(), dis=d.getElementById('dis'); toolSheet(); if(dis.getAttribute('data-view')==='1'){var c=d.querySelector('.v1 .ct-chip'); if(c){c.click(); var f=d.getElementById('ctForm'); if(f&&f.requestSubmit)f.requestSubmit()}}})}
  $$('#subOps a').forEach(function(a,i){if(i===0){a.id='navDischarge'; a.addEventListener('click',function(){openTool(true)})}});

  var TOOLDOC={{TOOLDOC}};
  /* ================= the real Simulation page (Tour 5) =================
     Captured from virevo.works/simulation and loaded into a frame over the
     stage. Selectors that start with "S:" point inside it. */
  var sframe=$('#simFrame'), simLoaded=false, simWait=[], simPoll=null, simSt={};
  function SD(){try{return simLoaded?sframe.contentDocument:null}catch(e){return null}}
  function openSim(fresh,then){
    sframe.hidden=false;
    if(then)simWait.push(then);
    if(fresh||!sframe.dataset.on){simLoaded=false; sframe.dataset.on='1'; sframe.srcdoc=SIMDOC; setTimeout(function(){if(!simLoaded&&!sframe.hidden)say('The Simulation is taking long to open here. Try Restart this tour.')},9000)}
    else if(simLoaded){var w=simWait; simWait=[]; w.forEach(function(f){f()})}
  }
  function closeSim(){sframe.hidden=true}
  window.__tojoSim=function(){closeSim(); view('home'); scroller.scrollTop=0; fire('simhome')};
  function simStep(){var d=SD(); if(!d)return -1; var b=d.querySelector('nav.jr li.now button'); return b?+b.dataset.step:-1}
  sframe.addEventListener('load',function(){
    var d=sframe.contentDocument; if(!d||!d.getElementById('stage'))return;
    simLoaded=true; simSt={};
    d.addEventListener('click',function(e){var t=e.target; if(!t.closest)return; if(t.closest('[data-pick5]'))setTimeout(function(){fire('sim:pick')},150); if(t.closest('[data-p6="owner"]'))setTimeout(function(){fire('sim:owner')},150)},true);
    d.defaultView.addEventListener('scroll',function(){place()});
    clearInterval(simPoll);
    simPoll=setInterval(function(){var d=SD(); if(!d||sframe.hidden)return;
      var st=simStep(), pe=d.querySelector('#peek.on')||d.querySelector('#sheet.on'), pk=pe?pe.textContent.slice(0,80):'', ch=d.body.classList.contains('chat-open'), ok=!!d.querySelector('[data-p5n]');
      if(st!==simSt.st){simSt.st=st; fire('sim:step'+st)}
      if(pk&&pk!==simSt.pk)fire('sim:peek'); simSt.pk=pk;
      if(ch&&!simSt.ch)fire('sim:chat'); simSt.ch=ch;
      if(ok&&!simSt.ok)fire('sim:p5ok'); simSt.ok=ok;
    },300);
    simLock(); var w=simWait; simWait=[]; w.forEach(function(f){f()});
    fire('simopen');
  });
  function simLock(){var d=SD(); if(!d)return; var on=!area.hidden&&tIx===4&&idx<stepsN(); d.documentElement.classList.toggle('tour-lock',on)}
  function sTop(){var d=SD(); if(d)d.defaultView.scrollTo(0,0)}
  function sScrollTo(sel,off){var d=SD(); if(!d)return; var el=d.querySelector(sel); if(!el)return; var w=d.defaultView; w.scrollTo(0,Math.max(0,el.getBoundingClientRect().top+w.scrollY-(off||120)))}
  /* move the real page to step n: back through the step bar, forward with each page's own button */
  function simGo(n,then,keep){openSim(false,function(){var tries=0;
    (function loop(){var d=SD(), cur=simStep(); if(cur===n&&keep)return; if(cur===n||tries++>8){sTop(); if(then)setTimeout(then,250); return}
      if(n<cur){var b=d.querySelector('nav.jr button[data-step="'+n+'"]'); if(b)b.click(); return setTimeout(loop,500)}
      var q=function(s){return d.querySelector(s)};
      if(cur===0&&q('[data-act="go"]'))q('[data-act="go"]').click();
      else if(cur===1&&q('[data-p2="go"]'))q('[data-p2="go"]').click();
      else if(cur===2&&q('[data-p3="go"]'))q('[data-p3="go"]').click();
      else if(cur===3){var f=q('[data-freeze]'); if(f)f.click(); setTimeout(function(){var y=q('[data-frz="yes"]'); if(y)y.click()},350)}
      else if(cur===4){var i=q('[data-p5in="by"]'); if(i&&!i.value){i.value='Sample CEO'; i.dispatchEvent(new Event('input',{bubbles:true}))} var c=q('[data-p5="confirm"]'); if(c)c.click(); setTimeout(function(){var g=q('[data-p5n]'); if(g)g.click()},350)}
      setTimeout(loop,cur>=3?900:600)})()})}
  (function(){var n=$$('#gAgents .ni').filter(function(x){return /Simulations/.test(x.textContent)})[0]; if(n){n.id='niSim'; n.addEventListener('click',function(){openSim(true)})}})();

  var SIMDOC={{SIMDOC}};
  /* ================= the approved Automation Suite landings (Tour 6) =================
     Each approved suite landing (Automation Suites\Approved landing pages) is loaded
     into a frame over the stage. Selectors that start with "U:" point inside it. */
  var uframe=$('#suiteFrame'), suiteLoaded=false, suiteWait=[], suitePoll=null, suiteSt={}, suiteKey='', suitesSeen={};
  var SUITE_NAMES={discharge:'Discharge Summary',billing:'Billing & Insurance',admission:'Admission Process',diagnostic:'Diagnostic Scheduling',procurement:'Procurement'};
  function UD(){try{return suiteLoaded?uframe.contentDocument:null}catch(e){return null}}
  function openSuite(key,fresh,then){
    uframe.hidden=false; key=key||suiteKey||'discharge';
    if(then)suiteWait.push(then);
    if(fresh||key!==suiteKey||!uframe.dataset.on){suiteLoaded=false; suiteKey=key; uframe.dataset.on='1'; uframe.srcdoc=SUITEDOCS[key]; setTimeout(function(){if(!suiteLoaded&&!uframe.hidden)say('The suite is taking long to open here. Try Restart this tour.')},9000)}
    else if(suiteLoaded){var w=suiteWait; suiteWait=[]; w.forEach(function(f){f()})}
  }
  function closeSuite(){uframe.hidden=true}
  function uTag(d){var w=d.querySelector('#stage > div > div'); if(w){var wrap=w.querySelector('.wrap')||w; var kids=Array.prototype.slice.call(wrap.children), zi=0;
      kids.forEach(function(k){ if(k.tagName==='NAV')k.id='u-bar'; else if(k.classList.contains('head'))k.id='u-head'; else if(k.tagName==='SECTION'){var t=k.textContent.slice(0,200); k.id=/^\s*\d?\s*KPIs/.test(t)||/\bKPIs\b/.test((k.querySelector('h2,h3')||{}).textContent||'')?'u-kpis':/Taskboards/.test(t.slice(0,80))?'u-tasks':/Project Status/.test(t.slice(0,80))?'u-status':(zi++===0?'u-links':'')} else if(!k.id&&k.tagName==='DIV')k.id='u-watch'})}}

  uframe.addEventListener('load',function(){
    var d=uframe.contentDocument; if(!d||!d.getElementById('stage'))return;
    suiteLoaded=true; suiteSt={}; suitesSeen[suiteKey]=1;
    /* name the shared parts so every look can be pointed at the same way */
    uTag(d);
    d.addEventListener('click',function(e){var t=e.target; if(!t.closest)return; var tb=t.closest('[data-tab]'); if(tb&&tb.dataset.tab!=='overview')setTimeout(function(){fire('u:tab')},150); if(t.closest('[data-view="week"]'))setTimeout(function(){fire('u:week')},150)},true);
    d.defaultView.addEventListener('scroll',function(){place()});
    clearInterval(suitePoll);
    suitePoll=setInterval(function(){var d=UD(); if(!d||uframe.hidden)return; if(!d.getElementById('u-head'))uTag(d);
      var pe=d.querySelector('#peek.on'), pk=pe?pe.textContent.slice(0,80):'', sh=d.querySelector('#sheet.on'), sk=sh?sh.textContent.slice(0,80):'', ch=d.body.classList.contains('chat-open');
      if(pk&&pk!==suiteSt.pk){fire('u:peek'); fire('u:look')} suiteSt.pk=pk;
      if(sk&&sk!==suiteSt.sk){fire('u:sheet'); fire('u:look')} suiteSt.sk=sk;
      if(ch&&!suiteSt.ch)fire('u:chat'); suiteSt.ch=ch;
    },300);
    suiteLock(); var q=suiteWait; suiteWait=[]; q.forEach(function(f){f()});
    fire('suiteopen'); fire('suite:'+suiteKey);
  });
  function suiteLock(){var d=UD(); if(!d)return; var on=!area.hidden&&tIx===5&&idx<stepsN(); d.documentElement.classList.toggle('tour-lock',on)}
  function uScrollTo(sel,off){var d=UD(); if(!d)return; var el=d.querySelector(sel); var w=d.defaultView; if(!el){w.scrollTo(0,0);return} w.scrollTo(0,Math.max(0,el.getBoundingClientRect().top+w.scrollY-(off==null?20:off)))}
  function uClean(){var d=UD(); if(!d)return; var p=d.getElementById('peek'); if(p)p.classList.remove('on'); var s=d.getElementById('sheet'); if(s)s.classList.remove('on'); if(d.body.classList.contains('chat-open')){var x=d.querySelector('#chat button[aria-label*="inimise"], #chatClose'); if(x)x.click(); else d.body.classList.remove('chat-open')}}
  function suiteAt(key,sel,off,keep){openSuite(key,false,function(){if(keep)return; uClean(); uScrollTo(sel,off)})}
  (function(){var MAP={'Discharge Summary':'discharge','Billing & Insurance':'billing','Admission Process':'admission','Diagnostic Scheduling':'diagnostic','Procurement':'procurement'};
    $$('#subAuto a').forEach(function(a){var k=MAP[a.textContent.trim()]; if(k){a.dataset.suite=k; a.addEventListener('click',function(){view('home'); openSuite(k,true)})} else a.addEventListener('click',function(){say(a.textContent.trim()+' is still being built.')})})})();
  /* ---------- Tour 6 card extras ---------- */
  var LOOP=[['Do','The suite closes the bill for bed 12 at 11:40.'],['Watch','At 12:20 it is still open: 40 minutes past its time.'],['Decide','The billing desk is one person short today.'],['Correct','It moves the bill to the next free biller and tells the billing head.'],['Learn','Next Tuesday it plans a second biller before noon.']];
  function loopHtml(){return '<div class="loop"><ol id="lpN">'+LOOP.map(function(l,i){return '<li data-i="'+i+'"><b>'+l[0]+'</b><span>'+l[1]+'</span></li>'}).join('')+'</ol><button type="button" class="go" id="lpGo">▶ Run the loop</button><small class="dmx">Example only.</small></div>'}
  function bindLoop(){var g=$('#lpGo'); if(!g)return; g.addEventListener('click',function(){g.disabled=true; var lis=$$('#lpN li'); lis.forEach(function(l){l.classList.remove('on')}); lis.forEach(function(l,i){setTimeout(function(){l.classList.add('on'); if(i===lis.length-1){g.disabled=false; g.textContent='↻ Run it again'; fire('loop')}},reduce?0:i*1100)})})}
  function suitePickHtml(){return '<div class="spick">'+Object.keys(SUITE_NAMES).map(function(k){return '<button type="button" data-k="'+k+'" class="'+(k===suiteKey?'on':'')+(suitesSeen[k]?' seen':'')+'">'+SUITE_NAMES[k]+'</button>'}).join('')+'</div>'}
  function bindSuitePick(){$$('.spick button',card).forEach(function(b){b.addEventListener('click',function(){openSuite(b.dataset.k,false,function(){uScrollTo('#u-bar',20); $$('.spick button',card).forEach(function(x){x.classList.toggle('on',x.dataset.k===suiteKey); x.classList.toggle('seen',!!suitesSeen[x.dataset.k])}); if(Object.keys(suitesSeen).length>=3)fire('suites3')})})})}
  function ceoHtml(){return '<div class="ceo"><div class="c0"><b>MyCEO Agent</b><span>Holds your targets, settles clashes between departments, closes yesterday’s P&amp;L by 7 AM.</span></div><div class="c1"><span><b>Task Master</b>Operations</span><span><b>Quarter Master</b>Supply chain</span><span><b>Ward Round</b>Clinical</span><span><b>Referral Engine</b>Marketing</span></div><div class="c2">The suites: Discharge Summary · Billing &amp; Insurance · Admission Process · Diagnostic Scheduling · Procurement · Financial Health</div></div>'}

  var SUITEDOCS={{SUITEDOCS}};

  /* ---------- Tour 5, step 1: a projection beside a simulation (example only) ---------- */
  function demoHtml(){return '<div class="demo"><label class="dmr"><span>Add beds</span><input type="range" id="dmR" min="0" max="40" step="5" value="0"><b id="dmV">+0</b></label>'+
    '<div class="dm2"><div class="dmA"><small>A projection</small><svg viewBox="0 0 140 90" aria-hidden="true"><path d="M8 82H134M8 82V6" stroke="rgba(255,255,255,.35)" fill="none"/><path id="dmL" d="M8 70L134 52" stroke="var(--key)" stroke-width="3" fill="none"/><text x="10" y="14" fill="rgba(255,255,255,.7)" font-size="9">Revenue</text></svg><p>Draws last year forward. Nothing else moves.</p></div>'+
    '<div class="dmB"><small>Vidur</small><ul id="dmN"><li data-k="rev">Revenue</li><li data-k="nur">Nurses needed</li><li data-k="agy">Agency cost</li><li data-k="occ">Occupancy</li><li data-k="ebi">EBITDA</li></ul><p>Moves everything the beds touch.</p></div></div>'+
    '<small class="dmx">Example only. On your hospital, Vidur works these out from your own data.</small></div>'}
  function bindDemo(){var r=$('#dmR'); if(!r)return; var DIR={rev:'\u25B2 up',nur:'\u25B2 up',agy:'\u25B2 up',occ:'\u25BC down',ebi:'\u25B2 less than the projection'};
    var upd=function(){var v=+r.value; $('#dmV').textContent='+'+v; $('#dmL').setAttribute('d','M8 70L134 '+(52-v*1.1).toFixed(1)); $$('#dmN li').forEach(function(li,i){var on=v>0; li.classList.toggle('on',on); li.dataset.d=on?DIR[li.dataset.k]:''; li.style.transitionDelay=(on?i*120:0)+'ms'}); if(v>=10)fire('demo')};
    r.addEventListener('input',upd)}

  /* ================= Sanjay's three levels (Tour 4) ================= */
  var lvSeen={};
  function lvShow(n){$$('#lvSeg button').forEach(function(b){b.classList.toggle('on',+b.dataset.lv===n)}); $$('#lvCols .lvc').forEach(function(c){var k=+c.dataset.lv; c.classList.toggle('on',k===n); c.classList.toggle('seen',!!lvSeen[k]&&k!==n)}); lvSeen[n]=1; if(Object.keys(lvSeen).length>=3)fire('lv3')}
  $$('#lvSeg button').forEach(function(b){b.addEventListener('click',function(){lvShow(+b.dataset.lv)})});
  $$('#lvCols .lvc').forEach(function(c){c.addEventListener('click',function(){lvShow(+c.dataset.lv)})});
  (function(){var pb=$$('#topbar .tbtn').filter(function(x){return /Listener/.test(x.textContent)})[0]; if(pb)pb.id='planBadge'; var cp=$('#topbar .credits'); if(cp){cp.id='creditsPill'; cp.style.cursor='pointer';
    var pop=document.createElement('div'); pop.className='crpop'; pop.id='crPop'; pop.hidden=true; pop.innerHTML='<b>1,97,865 credits left</b> this month. Every answer uses credits, and deeper levels use more for each answer. Each Tool card shows what it has used. Compare plans shows what each level includes.'; $('#topbar').appendChild(pop);
    cp.addEventListener('click',function(e){e.stopPropagation(); pop.hidden=!pop.hidden; if(!pop.hidden)fire('credits')})}})();

  /* ================= the tours ================= */
  var TOURS=[
   {n:1,name:'The Tojo interface',short:'Where everything lives: agents, tools, resources, playbooks, your account.',mins:'9 steps · 2 min',
    theme:{c1:'#3D52C9',c2:'#1E2A7A',hl:'#FF4FA3',hlSoft:'#FFB3D9',key:'#FFD86B',keyInk:'#1E2A7A'},
    end:{title:'That’s the map',body:['Agents on the left to answer, test and run. Tools for one problem at a time. Resources and Playbooks to keep the work. Your account along the top.'],note:'Next: how to ask me a question, and how I answer.'},
    steps:[
    {title:'Welcome to Tojo', dim:false, target:[], scroll:'top',
     body:['Tojo is your hospital’s operations agent. He answers, tests decisions before you make them, and runs work for you.','This first tour shows where everything lives. Each part gets its own tour later.'],
     note:'Two minutes. Then you’ll know your way round.'},
    {title:'Everything starts on the left', target:['#side'], scroll:'top',
     body:['The left panel has four groups: <b>Agents</b>, <b>Tools</b>, <b>Resources</b> and <b>Playbooks</b>.','Your pinned chats sit at the top. New chat (Ctrl K) is always one click away.'],
     tryit:{ask:'Point at any item on the left. It lights up.', ev:'hoverside', res:'Every item answers to a hover or a tap.', live:'#side, #side .ni, #side .newchat'}},
    {title:'Three agents, three jobs', target:['#gAgents'], scroll:'top',
     body:['<b>Chat</b> answers and advises. This is Sanjay.','<b>Simulations</b> tests a decision before you make it. This is Vidur.','<b>Automations</b> runs the work and watches it. This is Narad.'],
     tryit:{ask:'Click Automations to unfold it.', ev:'expand:niAuto', res:'Six suites, each set up on your own SOPs and roles.', live:'#niAuto', ensure:function(){closeSub('subAuto','niAuto')}}},
    {title:'Tools go deep on one problem', target:['#gTools'], scroll:'top',
     body:['Each Tool is one hospital problem, such as Discharge or Supply Chain. It carries its own references, cases from other hospitals and your live numbers.','Locked rows (Process, KPI Monitoring, Integrations) open on higher plans.'],
     tryit:{ask:'Click Operations.', ev:'expand:niOps', res:'Discharge, Bed Management and OPD & Diagnostics. Financial and Clinical open the same way.', live:'#niOps', ensure:function(){closeSub('subOps','niOps')}}},
    {title:'Where the work is kept', target:['#gRes'], scroll:'top', navTo:'#gTools',
     body:['<b>Projects</b> hold running programmes.','<b>Taskboards</b> hold this week’s tasks and who owns each one.','<b>Repositories</b> hold your files and the data Tojo reads.']},
    {title:'Playbooks keep related chats together', target:['#gPbSide','#pbRow'], scroll:'#pbRow', navTo:'#gRes',
     body:['A Playbook is a folder for one theme, like “Discharge before 2pm”. It keeps its chats, files and notes together.','A new chat started inside it already knows that context.'],
     tryit:{ask:'Click Add new Playbook.', ev:'pb', res:'A name box opens. Type a name and press Enter; in the tour nothing is saved.', live:'#addpb', ensure:function(){$('#addpb').classList.remove('naming'); $('#pbName').value=''}}},
    {title:'Your account at a glance', target:['#topbar'], scroll:'top',
     body:['Switch hospital or group from the name on the left.','The badge shows your plan; the gold pill shows credits left, and Plan opens upgrades. Help reopens these tours any time.'],
     tryit:{ask:'Click the sun to switch light and dark.', ev:'sun', res:'Click it again to switch back. Your choice is kept per device.', live:'#sun'}},
    {title:'Ask anything here', target:['#banner','#hero'], scroll:'top',
     body:['The gold banner says what Tojo can read today: his own skills, or your HIS, ERP and BI once connected.','Type in the box, or start from a chip. The paperclip attaches files; the mic lets you speak.'],
     tryit:{ask:'Click “Bed management KPIs”.', ev:'chip', res:'The question fills the box. It is not sent: sending is off in the tour.', live:'#chipKpi', ensure:function(){$('#ask').value=''}}},
    {title:'Carry on where you stopped', target:['#pickup','#toolsRow'], scroll:'#pickup',
     body:['Each card is a past chat: its Tool, its stage (Diagnosis, Automations), steps taken and the date.','The Tools row shows each Tool’s parameters and the credits it has used so far.'],
     tryit:{ask:'Point at a card (or tap it on a phone).', ev:'hovercard', res:'The card lifts to show its drawing. Opening it takes you back into that chat.', live:'#pickRow, #pickRow .pc'}}
   ]},
   {n:2,name:'Chat',short:'How to ask, when to use a Tool instead, and how Tojo answers with a picture.',mins:'6 steps · 2 min',
    theme:{c1:'#0E8A8F',c2:'#053F4A',hl:'#FF6F4F',hlSoft:'#FFC4B4',key:'#D9F26A',keyInk:'#053F4A'},
    end:{title:'Ask anything. Take topics home.',body:['Chat is for any question. When the question has a home in a Tool, take it there: the Tool knows that problem in depth.','Every answer reads the same way: verdict, causes, drawing, note, one question back, three next steps.'],note:'Next: what a Tool does that Chat can’t.'},
    steps:[
    {title:'Start a chat', view:'home', target:['#niChat','#newchat'], scroll:'top',
     body:['Chat is Sanjay, Tojo’s first level. Ask him anything about running the hospital.','Every chat is saved and comes back under Pick up where you left off.'],
     tryit:{ask:'Click New chat (or press Ctrl K).', ev:'newchat', res:'A fresh chat, with the box ready for your question.', live:'#newchat'}},
    {title:'Ask the way you’d ask your COO', view:'home', target:['#composer'], scroll:'top',
     body:['Write the problem in your own words, with the ward, the time or the number if you have it.','Attach a register or a report with the paperclip, and Tojo reads it before he answers.'],
     tryit:{ask:'Type “Ward 4” in the box.', ev:'typed', res:'Tojo finished the sentence. The more specific you are, the sharper the answer.', live:'#ask', ensure:function(){$('#ask').value=''; typedOnce=false}}},
    {title:'Chat or a Tool?', view:'home', target:['#niChat','#gTools'], scroll:'top',
     body:['Use <b>Chat</b> for general questions: a board note, a policy, a quick check.','Use the <b>Tool</b> when the question is about its topic. A Tool has its own references, cases from other hospitals and your live numbers, so Tojo can dig deeper.'],
     sorter:true, tryit:{ask:'Sort each question into Chat or a Tool.', ev:'sorted', res:'All three placed.'}},
    {title:'How Tojo answers', target:function(){return lit?['#'+lit]:(T().doneAt(3)?['#threadChat','#canvasDraw']:['#composer'])},
     body:['The first line is the verdict. Then the causes, a drawing that shows them, and Tojo’s Note in his own hand.','He asks you one question back, never five.'],
     partLbl:true,
     enter:function(d){if(d)showThread(); else {view('home'); scroller.scrollTop=0; $('#ask').value=Q; resetThread()}},
     tryit:{ask:'Click Send, then watch each part arrive.', ev:'revealed', res:'Verdict, causes, drawing, note, @points, one question, three next steps. Every answer follows this order.', live:'#send', arm:function(){return on('send',reveal)}}},
    {title:'A picture instead of a page', target:['#canvasDraw'],
     body:['Tojo draws the answer so you see it in seconds: where the time goes, and what changes.','The @points in the chat link straight to each part of the drawing.'],
     enter:function(){showThread()},
     tryit:{ask:'Tap any stop on the two lines.', ev:'stop', res:'Each stop shows what changes, today against the Tojo way. The @points work the same way.', live:'#canvasDraw, #canvasDraw .stp, #pPoints'}},
    {title:'Where to go next', target:['#prompts','#ctxPanel'],
     body:['The three prompts are the likely next questions. One click asks them.','The side panel keeps every source Tojo used, the drawings so far, and the tasks that come out of the chat.'],
     enter:function(d){showThread(); if(!d)ctxTab('vis'); $('#ctxPanel').classList.add('open'); tchat.scrollTop=1e4},
     tryit:{ask:'Open Sources in the side panel.', ev:'sources', res:'Every source Tojo used, and which part of the answer it fed.', live:'#ctxPanel, #ctxPanel button'}}
   ]},
   {n:3,frameTour:true,name:'Tools',short:'Open a real Tool: its worksheet, its chat, and the landing page of each place. Plus: same question, two answers.',mins:'11 steps · 4 min',
    theme:{c1:'#9B1D4F',c2:'#4A0B27',hl:'#2EE6F0',hlSoft:'#A9F5F9',key:'#FFE08A',keyInk:'#4A0B27'},
    setup:function(){closeTool(); frame.dataset.on=''; view('home'); resetCmp()},
    end:{title:'One problem, all the way',body:['Every Tool works this way: a worksheet to start from, a chat that stays with the Tool, and five places that take the problem from diagnosis to the people who change.','Discharge, Bed Management, OPD & Diagnostics, Supply Chain and Revenue & EBITDA all follow this shape.'],note:'Next: how deep Sanjay goes at each level.'},
    steps:[
    {title:'Open a Tool', view:'home', target:['#gTools'], scroll:'top', navTo:'#gAgents',
     enter:function(){closeTool(); view('home'); $('#subOps').classList.add('open'); $('#niOps').classList.add('open')},
     body:['Each Tool is one hospital problem. Operations holds Discharge, Bed Management and OPD & Diagnostics; Financial holds Supply Chain and Revenue & EBITDA.','A Tool opens as its own screen, built for that one problem.'],
     tryit:{ask:'Click Discharge under Operations.', ev:'toolopen', res:'This is the real Discharge Tool, exactly as it opens in Tojo.', live:'#subOps, #subOps a'}},
    {title:'A screen of its own', target:['T:.dis-rail','T:.dis-wrap.v1 .dis-head','T:.ct-head'],
     enter:function(){toolView1(false)},
     body:['On the left, the <b>rail</b>: five places for this problem. In the middle, the <b>worksheet</b>. On the right, <b>Tojo’s chat</b> for this Tool only.','The house at the top left takes you back to the main chat.']},
    {title:'The worksheet', target:['T:#disTasks','T:#resources'],
     enter:function(){openTool(false,function(){var d=TD(); if(d.getElementById('dis').getAttribute('data-view')!=='1'){openTool(true,function(){tScrollTo('#resources')})} else {toolSheet(); tScrollTo('#resources')}})},
     body:['Four cards: the numbers that shape discharge, where it usually gets stuck, what the fix is made of, and the agents Tojo suggests.','Your tasks for the day says which files Tojo needs first. Empty cards show what he will look at, not what he has found.'],
     tryit:{ask:'On the numbers card, switch from Timing to Money or Staffing.', ev:'tool:pill', res:'Each card answers to a click. Once your files are in, the numbers fill in here.', live:'T:#resources'}},
    {title:'A chat that stays with the Tool', target:['T:#chat'],
     enter:function(d){if(!d)toolView1(); else toolView2()},
     body:['This conversation belongs to Discharge, so everything said here builds on what the Tool already knows.','Tojo opens by asking for files and offering replies you can send with one click.'],
     tryit:{ask:'Click “We do about 40 a day”, then send it.', ev:'tool:view2', res:'Tojo answers by laying out the whole discharge route on the worksheet.', live:'T:#ctChips, T:#ctForm'}},
    {title:'Walk the chain', target:['T:#routeMap','T:#cardSlot'],
     enter:function(){toolView2()},
     body:['Before suggesting anything, Tojo walks the route a discharge takes, stop by stop: doctors, nurses, pharmacy, billing, insurance and the rest.','Each stop says what he will ask there. The chat follows the stop you pick.'],
     tryit:{ask:'Tap any stop on the map.', ev:'tool:stop', res:'The card and the chat both move to that stop.', live:'T:#routeMap'}},
    {title:'Five places on the rail', target:['T:.rail-tabs'],
     enter:function(){openTool(false,function(){toolSheet()})},
     body:['<b>Resources</b> holds the files and references. <b>Diagnosis</b> finds where it breaks. <b>Solutions</b> shapes the fix. <b>Automations</b> designs what runs it. <b>Processes</b> plans who changes what.','Each place has its own landing page, kept up to date every night.'],
     tryit:{ask:'Click Diagnosis on the rail.', ev:'tool:panel:dx', res:'The middle column becomes the Diagnosis landing page. The chat stays where it was.', live:'T:.rail-tabs'}},
    {title:'Diagnosis', target:['T:#dxWrap'],
     enter:function(){toolDesk('dx')},
     body:['The ring shows how far the diagnosis has got: walk the chain, price the wait, name the cause, check real times, last stops.','Below it, the evidence (your numbers, and what was worked out from them) and what Tojo still has to do.'],
     tryit:{ask:'Click Solutions on the rail.', ev:'tool:panel:sol', res:'On to the fix.', live:'T:.rail-tabs'}},
    {title:'Solutions', target:['T:#solWrap'],
     enter:function(){toolDesk('sol')},
     body:['Each solution comes from a cause Diagnosis found. It moves from idea, to shaped, to tested with you, to agreed.','Each one also shows what it depends on, and is redrawn when something changes.'],
     tryit:{ask:'Click Automations on the rail.', ev:'tool:panel:aut', res:'Now the software that runs the fix.', live:'T:.rail-tabs'}},
    {title:'Automations', target:['T:#autWrap'],
     enter:function(){toolDesk('aut')},
     body:['The clock runs from the evening round to the afternoon. Each automation sits at the hour it does its work, from the summary on the evening round to the alerts when the patient leaves.','The list says what each one waits on, here one link to the hospital software.'],
     tryit:{ask:'Click Processes on the rail.', ev:'tool:panel:prc', res:'Last place: the people.', live:'T:.rail-tabs'}},
    {title:'Processes', target:['T:#prcWrap'],
     enter:function(){toolDesk('prc')},
     body:['Process changes, the measures we watch, and team and role changes, in one place.','A short trial on one ward comes first, before anything changes across the hospital.']},
    {title:'Same question, two answers', partLbl:'Press Play to begin',
     target:function(){return cmpLit?['#'+cmpLit]:['#cmpView']},
     enter:function(d){closeTool(); view('compare'); if(d)showCmpAll(); else resetCmp()},
     body:['Why a Tool goes deeper. A CEO asks: “Should we just accept insurance delays?” A general AI answers from the open internet: a long, careful essay.','Tojo answers from his own library, built from running real hospitals.'],
     tryit:{ask:'Press Play and watch both answers.', ev:'played', res:'Same question. One answer to read; one to act on.', arm:function(){return on('play',playCmp)}, button:'Play'}}
   ]},
   {n:4,name:'Sanjay’s three levels',short:'Listener, Thinker, Strategist: answered, shown, led. One question at three depths.',mins:'4 steps · 2 min',
    theme:{c1:'#C2571A',c2:'#5E2508',hl:'#7CF0B0',hlSoft:'#C9F9DF',key:'#FFF1C7',keyInk:'#5E2508'},
    setup:function(){view('home'); lvSeen={}; lvShow(0); lvSeen={}; var p=$('#crPop'); if(p)p.hidden=true},
    end:{title:'Three levels, one Tojo',body:['Listener answers. Thinker shows you why. Strategist tells you what to do across the hospital, in order, and watches the KPIs with you.','Vidur and Narad both include Sanjay at Strategist level.'],note:'Next: Vidur, who lets you try it first.'},
    steps:[
    {title:'Your level sets the depth', view:'home', target:['#planBadge','#creditsPill'], scroll:'top',
     body:['Chat and Tools together are Sanjay, “the hospital’s 24×7 CEO in a chat window”.','He comes in three levels. Each reads the same hospital, and goes a step further than the one before. Your level shows here, beside your credits.']},
    {title:'Answered, shown, led', view:'levels', target:['#lvSeg','#lvCols'],
     enter:function(d){view('levels'); if(!d){lvSeen={}; lvShow(0)}},
     body:['The same question, answered at each level.','<b>Listener</b>: the answer and the figure it came from. <b>Thinker</b>: why, with the drawing and what other hospitals did. <b>Strategist</b>: what to do across the hospital, in order, and the KPIs to watch.'],
     tryit:{ask:'Switch through all three levels.', ev:'lv3', res:'Each level keeps everything below it and adds the next layer.', live:'#lvSeg, #lvCols'}},
    {title:'How credits work', view:'home', target:['#creditsPill','#toolsRow'], scroll:'#toolsRow',
     enter:function(d){view('home'); if(!d){var p=$('#crPop'); if(p)p.hidden=true}},
     body:['Every answer uses credits. Deeper levels reason across more of the hospital and use more for each answer.','Each Tool card shows what it has used so far.'],
     tryit:{ask:'Click the credits pill.', ev:'credits', res:'What is left this month, and where to compare plans.', live:'#creditsPill'}},
    {title:'Above Sanjay', view:'home', target:['#gAgents'], scroll:'top',
     enter:function(){view('home'); var p=$('#crPop'); if(p)p.hidden=true},
     body:['Sanjay advises. <b>Vidur</b> (Simulations) tests a decision before you make it. <b>Narad</b> (Automations) runs the work.','Vidur and Narad both include Sanjay at Strategist level.']}
   ]},
   {n:5,frameTour:true,name:'Simulations \u00b7 Vidur',short:'Your hospital as one formula. Try every decision before you make it, on the real Simulation.',mins:'13 steps \u00b7 4 min',
    theme:{c1:'#2C5F8A',c2:'#11283F',hl:'#FFB020',hlSoft:'#FFE0A3',key:'#B6F0FF',keyInk:'#11283F'},
    setup:function(){closeSim(); sframe.dataset.on=''; view('home')},
    end:{title:'Live it twice',body:['Vidur ties every measure in the hospital to the ones it affects, learns how your hospital behaves from its own history, and lets you test a plan before a rupee is spent.','Then it freezes the plan, hands it to named people, and turns it into weekly tasks.'],note:'Next: Narad, who runs the plan.'},
    steps:[
    {title:'A projection guesses. A simulation tests.', dim:false, target:[], view:'home', scroll:'top', demo:true,
     enter:function(){closeSim()},
     body:['A projection takes last year\u2019s numbers and draws the line forward. It assumes nothing else moves.','Vidur links every measure to what it affects and what affects it, so a change moves the rest the way it really would.'],
     tryit:{ask:'Slide \u201cAdd beds\u201d to the right.', ev:'demo', res:'Same decision, two pictures. Only one of them shows what it costs you.'}},
    {title:'Meet Vidur', view:'home', target:['#gAgents'], scroll:'top',
     enter:function(){closeSim()},
     body:['Vidur maps the whole hospital into one formula: up to 1,000 measures, from your HIS, ERP and BI history.','The links carry more than numbers. How fast a ward takes up a change, what the owner protects and what he pushes for: each shows up in the history as a weight. The formula learns how your hospital behaves.'],
     note:'Understand before you decide.',
     tryit:{ask:'Click Simulations.', ev:'simopen', res:'This is the real Simulation page, on a sample 150-bed hospital.', live:'#niSim'}},
    {title:'Seven steps, data to action', target:['S:nav.jr'],
     enter:function(d){simGo(0,null,d)},
     body:['Your data, Targets, Six KPIs, Simulate, Freeze, Your team, Taskboards.','Each page\u2019s own button opens the next. You can always step back along this bar.']},
    {title:'One formula, built from your data', target:['S:.wheel'],
     enter:function(d){simGo(0,null,d)},
     body:['EBITDA sits at the centre. Around it, every measure the formula uses, grouped by department: beds, staff, theatres, ICU, scans, pharmacy, billing, OPD, support, money.','A solid line is learned from your files. A dashed line uses reference weights from other hospitals until your numbers arrive.'],
     tryit:{ask:'Point at any measure or link on the wheel.', ev:'sim:peek', res:'Each one says what it is affected by and what it affects downstream.', live:'S:.wheel'}},
    {title:'What your files give it', target:['S:.side'],
     enter:function(d){simGo(0,null,d)},
     body:['Files in, measures found, links set by your own data, and months of history. One month shows where you stand; twelve teach the formula how your measures move together.','Every link still on reference is listed, so nothing is guessed silently.'],
     tryit:{ask:'Click Build the formula.', ev:'sim:step1', res:'The formula is built. On to your targets.', live:'S:[data-act="go"]'}},
    {title:'Set your targets', target:['S:.p2head','S:.shown','S:.tools'],
     enter:function(d){simGo(1,null,d)},
     body:['Every measure, grouped by department, starts at the realistic value: what hospitals of your size reached in twelve months from a start like yours.','Change any target. Tojo tells you whether your targets add up.'],
     tryit:{ask:'Point at one of the four numbers at the top right.', ev:'sim:peek', res:'Every number on these pages explains itself. Each measure below says how it is tracked and how its links were found.', live:'S:.p2head'}},
    {title:'Pick six KPIs', target:['S:.seats','S:.lev3'],
     enter:function(d){simGo(2,null,d)},
     body:['The plan is built around six KPIs, ideally from different departments.','Each one brings in every change that affects it: automations, beds and equipment, process and role changes, staff.'],
     tryit:{ask:'Point at any change the six bring in.', ev:'sim:peek', res:'Each change says how many of your six it moves.', live:'S:.lev3, S:.seats'}},
    {title:'Try the plan before you pay for it', target:['S:.top5','S:.bulk5'],
     enter:function(d){simGo(3,null,d)},
     body:['Approve each change at <b>Achievable</b> or <b>Dream</b>, or leave it out. The strip at the top updates at once: total cost, monthly cost, extra EBITDA, break-even, and how many KPIs reach target.','Every cost can be typed over by hand.'],
     tryit:{ask:'Switch any change to Dream or Not approved, and watch the strip.', ev:'sim:pick', res:'Cost, EBITDA and break-even moved with that one change.', live:'S:.sim5, S:.bulk5'}},
    {title:'Freeze the plan', target:['S:.bulk5','S:.top5'],
     enter:function(d){simGo(3,null,d)},
     body:['When it looks right, freeze it. The frozen plan sets the budget, the timeline and the tasks.','You check it once more on the next page before anything is handed out.'],
     tryit:{ask:'Click Freeze this plan, then Freeze and confirm.', ev:'sim:step4', res:'Frozen. Now the plan, month by month.', live:'S:.bulk5, S:.frz5'}},
    {title:'Your plan, month by month', target:['S:.top5','S:.box5'],
     enter:function(d){simGo(4,null,d)},
     body:['Every change on a calendar: when it starts, and when it is fully working.','The key months are marked: break-even, and when the KPIs reach target. Below, the money going out each month.']},
    {title:'Confirm it with your name', target:['S:.cf5'],
     enter:function(d){if(!d)simGo(4,function(){sScrollTo('.cf5',360)})},
     body:['A plan becomes real when someone owns it.','Your name and role go on it, with the date.'],
     tryit:{ask:'Type your name and click Confirm this plan.', ev:'sim:p5ok', res:'Confirmed. Next, the people who will run it.', live:'S:.cf5'}},
    {title:'Your team', target:['S:.bulk5','S:.org6'],
     enter:function(d){simGo(5,null,d)},
     body:['Everyone this plan needs, from the owner down: a lead for each change and an owner for each KPI.','Add each head\u2019s name and mobile, here or from a CSV or Excel file. Tojo then sends each one their own tasks every morning.'],
     tryit:{ask:'Click Use the owner for every empty department.', ev:'sim:owner', res:'Every gap is filled with the owner for now. Swap in the right heads later.', live:'S:.bulk5'}},
    {title:'Ask Tojo on every page', target:['S:#chatFab'],
     enter:function(d){simGo(5,null,d)},
     body:['Tojo sits on every page. Pick any number, link or change and ask what it means, what it costs, or what to do about it.','After the team is confirmed, Taskboards turns the plan into week-by-week tasks with owners.'],
     tryit:{ask:'Open Ask Tojo.', ev:'sim:chat', res:'Tojo answers about the page you are on.', live:'S:#chatFab, S:#chatHost'}}
   ]},
   {n:6,frameTour:true,name:'Automations · Narad',short:'Suites that do the work, watch it, correct it and keep improving. On the approved suite landings.',mins:'12 steps · 4 min',
    theme:{c1:'#56650F',c2:'#252E05',hl:'#47C7FF',hlSoft:'#B5E8FF',key:'#FFE66B',keyInk:'#252E05'},
    setup:function(){closeSuite(); uframe.dataset.on=''; suitesSeen={}; view('home')},
    end:{title:'Answer, test, run',body:['Sanjay tells you what is wrong and what to do. Vidur tests it before you spend. Narad runs it, watches it and keeps improving it, every day, in every department.','Ask your first question whenever you are ready.'],note:'That’s Tojo.'},
    steps:[
    {title:'Not a robot. A colleague that thinks.', dim:false, target:[], view:'home', scroll:'top', loop:true,
     enter:function(){closeSuite()},
     body:['Narad is Tojo’s highest level: it doesn’t advise, it runs.','Ordinary automation repeats a step. A Narad suite does the step, checks that it worked, steps in when it didn’t, and learns from both.'],
     tryit:{ask:'Press Run the loop.', ev:'loop', res:'Do, watch, decide, correct, learn. Around the clock, in every department.'}},
    {title:'Six suites, ready to switch on', view:'home', target:['#gAgents'], scroll:'top', navTo:'#gAgents',
     enter:function(){closeSuite(); $('#subAuto').classList.add('open'); $('#niAuto').classList.add('open')},
     body:['Discharge Summary, Billing & Insurance, Admission Process, Diagnostic Scheduling, Procurement and Financial Health.','Each one is set up on your own SOPs, roles and escalation paths.'],
     tryit:{ask:'Click Discharge Summary.', ev:'suite:discharge', res:'This is the approved Discharge Summary landing: a 250-bed hospital, week by week. Example figures.', live:'#subAuto, #subAuto a'}},
    {title:'One bar, every section', target:['U:#u-bar'],
     enter:function(d){suiteAt('discharge','#u-bar',20,d)},
     body:['Overview, Integrations, KPIs, Taskboards, Project Status, Resources and Chat. Every suite has the same sections, in the same order.','Resources and Chat open as panels beside the page.'],
     tryit:{ask:'Click KPIs on the bar.', ev:'u:tab', res:'The page moves to that section. Every suite works the same way.', live:'U:#u-bar'}},
    {title:'The suite at a glance', target:['U:#u-head','U:.warn','U:#u-watch'],
     enter:function(d){suiteAt('discharge','#u-bar',20,d)},
     body:['Four pulse readings: parts live against plan, KPIs on course, EBITDA spent against earned back, and the break-even month.','Beside them, the watch list (what is slipping, and who holds it) and a countdown to the next part going live.'],
     tryit:{ask:'Point at an item on the watch list.', ev:'u:peek', res:'Every item explains itself, and carries Ask Tojo about this.', live:'U:#u-head, U:.warn, U:#u-watch'}},
    {title:'Ask Tojo about this', target:['U:.warn','U:#u-watch','U:#chat'],
     enter:function(d){suiteAt('discharge','#u-bar',20,d)},
     body:['Every peek and every detail panel has <b>Ask Tojo about this</b>.','It opens the chat with the item attached and the question already written: where it stands, any delay or overrun, who is responsible, and how we recover.'],
     tryit:{ask:'Point at a watch-list item, then click Ask Tojo about this.', ev:'u:chat', res:'The chat opens with the item attached. Edit the question or send it as it is.', live:'U:#u-head, U:.warn, U:#u-watch, U:#peek, U:#chatHost, U:#chatFab'}},
    {title:'What it is wired to', target:['U:#u-links'],
     enter:function(d){suiteAt('discharge','#u-links',10,d)},
     body:['Each building is a department that feeds the discharge summary, piped to the summary engine.','A pipe flows, ticks or stands empty by how far its link has got. Each numbered part is one piece of the build.'],
     tryit:{ask:'Click any numbered part on the drawing.', ev:'u:sheet', res:'The detail panel says what the part does, who owns it, and what it waits on.', live:'U:#u-links'}},
    {title:'KPIs', target:['U:#u-kpis'],
     enter:function(d){suiteAt('discharge','#u-kpis',10,d)},
     body:['Each KPI shows where it started, where it is now, and the target.','It tells you at once which ones are on course and which are slipping.'],
     tryit:{ask:'Click any KPI.', ev:'u:sheet', res:'Its history, its owner and what moves it.', live:'U:#u-kpis'}},
    {title:'It hands out the work, then follows it up', target:['U:#u-tasks'],
     enter:function(d){suiteAt('discharge','#u-tasks',10,d)},
     body:['Tasks go to named people with a time to finish: the discharge manager, IT, the medical superintendent, nursing, billing.','Narad chases the late ones and closes the done ones.'],
     tryit:{ask:'Switch Taskboards from Today to This week.', ev:'u:week', res:'The whole week, person by person.', live:'U:#u-tasks'}},
    {title:'Project status', target:['U:#u-status'],
     enter:function(d){suiteAt('discharge','#u-status',10,d)},
     body:['Money in and out, month by month: subscription, salaries for the roles we recommended, one-time costs, and EBITDA added so far.','When the roll-out is late, it says why.'],
     tryit:{ask:'Point at a month, or click Why 4 weeks late.', ev:'u:look', res:'The detail behind the number, with Ask Tojo about it.', live:'U:#u-status'}},
    {title:'Same layout. Its own look.', target:['U:#u-bar','U:#u-head'], spick:true,
     enter:function(d){openSuite(null,false,function(){uClean(); uScrollTo('#u-bar',20)})},
     body:['Every suite has the same sections in the same place, so nobody has to learn a new page.','Each one has its own look, so you always know which one you are in.'],
     tryit:{ask:'Open two more suites below.', ev:'suites3', res:'Five suites, one layout, five looks. Financial Health is still being built.'}},
    {title:'One agent above them all', view:'home', target:['#gAgents'], scroll:'top', ceo:true,
     enter:function(){closeSuite(); view('home')},
     body:['On a full Narad roll-out, the suites report to agents that think across departments.']},
    {title:'Advise, test, run', view:'home', target:['#gAgents'], scroll:'top',
     enter:function(){closeSuite(); view('home')},
     body:['<b>Chat</b> (Sanjay) tells you what is wrong and what to do.','<b>Simulations</b> (Vidur) tests it before you spend.','<b>Automations</b> (Narad) runs it, watches it and keeps improving it, every day.']}
   ]}
  ];
  function closeSub(s,n){document.getElementById(s).classList.remove('open'); document.getElementById(n).classList.remove('open')}
  var SORT=[
    {q:'Draft a note to the board on this quarter’s priorities', a:'chat', ok:'A general ask. Chat is quickest.', no:'Not quite. No Tool owns this: it’s a general ask, so Chat.'},
    {q:'Discharges are slipping past 2pm on Ward 4 — where is it going wrong?', a:'tool', ok:'The Discharge Tool’s whole job. It knows where discharges usually stall.', no:'Not quite. Discharge has its own Tool, with its references and past cases.'},
    {q:'Why are we paying more for the same stents?', a:'tool', ok:'Supply Chain. It compares your rates with what other hospitals pay.', no:'Not quite. Price gaps live in the Supply Chain Tool.'}
  ];

  /* ================= engine ================= */
  var tIx=0, idx=0, done={}, full=false, offTry=null, sortState={};
  function T(){var t=TOURS[tIx]; t.doneAt=function(i){return !!done[i]}; return t}
  function built(t){return !!t.steps}
  function theme(t){var r=document.documentElement.style, h=t.theme; r.setProperty('--c1',h.c1); r.setProperty('--c2',h.c2); r.setProperty('--hl',h.hl); r.setProperty('--hl-soft',h.hlSoft); r.setProperty('--key',h.key); r.setProperty('--key-ink',h.keyInk)}

  var scale=1;
  function fit(){var w=box.clientWidth; scale=w/1440; stage.style.transform='scale('+scale+')'; box.style.height=(900*scale)+'px'}
  window.addEventListener('resize',function(){fit(); place()});

  var cur=[], dimOn=false, dimA=0, raf=0;
  function rectOf(sel){ if(sel.indexOf('T:')===0)return trect(sel.slice(2)); if(sel.indexOf('S:')===0)return srect(sel.slice(2)); if(sel.indexOf('U:')===0)return urect(sel.slice(2)); var el=$(sel); if(!el||!el.offsetParent)return null; var b=box.getBoundingClientRect(), r=el.getBoundingClientRect(); var p=8; var x=Math.max(2,r.left-b.left-p), y=Math.max(2,r.top-b.top-p); var x2=Math.min(b.width-2,r.right-b.left+p), y2=Math.min(b.height-2,r.bottom-b.top+p); var sc=el.closest('#scroll, #nav, #threadChat, #toolScroll'); if(sc&&sc!==el){var c=sc.getBoundingClientRect(); y=Math.max(y,c.top-b.top-2); y2=Math.min(y2,c.bottom-b.top+2)} if(y2<=y+4||x2<=x+4)return null; return {x:x,y:y,w:x2-x,h:y2-y}}
  function trect(sel){var d=TD(); if(!d||frame.hidden)return null; var el=d.querySelector(sel); if(!el)return null; var r=el.getBoundingClientRect(); if(!r.width||!r.height)return null; var f=frame.getBoundingClientRect(), b=box.getBoundingClientRect(), k=f.width/1440, p=8;
    var t0=r.top, t1=r.bottom; var m=d.getElementById('disMain'); if(m&&m.contains(el)){var mr=m.getBoundingClientRect(); t0=Math.max(t0,mr.top); t1=Math.min(t1,mr.bottom)}
    t0=Math.max(t0,0); t1=Math.min(t1,900); if(t1<=t0+4)return null;
    var x=f.left-b.left+r.left*k-p, y=f.top-b.top+t0*k-p, x2=f.left-b.left+r.right*k+p, y2=f.top-b.top+t1*k+p;
    x=Math.max(2,x); y=Math.max(2,y); x2=Math.min(b.width-2,x2); y2=Math.min(b.height-2,y2); if(x2-x<4||y2-y<4)return null; return {x:x,y:y,w:x2-x,h:y2-y}}
  function urect(sel){var d=UD(); if(!d||uframe.hidden)return null; var el=d.querySelector(sel); if(!el)return null; var r=el.getBoundingClientRect(); if(!r.width||!r.height)return null; var f=uframe.getBoundingClientRect(), b=box.getBoundingClientRect(), k=f.width/1440, p=8;
    var t0=Math.max(r.top,0), t1=Math.min(r.bottom,900); if(t1<=t0+4)return null;
    var x=f.left-b.left+r.left*k-p, y=f.top-b.top+t0*k-p, x2=f.left-b.left+r.right*k+p, y2=f.top-b.top+t1*k+p;
    x=Math.max(2,x); y=Math.max(2,y); x2=Math.min(b.width-2,x2); y2=Math.min(b.height-2,y2); if(x2-x<4||y2-y<4)return null; return {x:x,y:y,w:x2-x,h:y2-y}}
  function srect(sel){var d=SD(); if(!d||sframe.hidden)return null; var el=d.querySelector(sel); if(!el)return null; var r=el.getBoundingClientRect(); if(!r.width||!r.height)return null; var f=sframe.getBoundingClientRect(), b=box.getBoundingClientRect(), k=f.width/1440, p=8;
    var t0=Math.max(r.top,0), t1=Math.min(r.bottom,900); if(t1<=t0+4)return null;
    var x=f.left-b.left+r.left*k-p, y=f.top-b.top+t0*k-p, x2=f.left-b.left+r.right*k+p, y2=f.top-b.top+t1*k+p;
    x=Math.max(2,x); y=Math.max(2,y); x2=Math.min(b.width-2,x2); y2=Math.min(b.height-2,y2); if(x2-x<4||y2-y<4)return null; return {x:x,y:y,w:x2-x,h:y2-y}}
  function mapRect(el,fr){var r=el.getBoundingClientRect(); if(!r.width||!r.height)return null; var b=box.getBoundingClientRect(); if(!fr)return {x:r.left-b.left,y:r.top-b.top,w:r.width,h:r.height}; var f=fr.getBoundingClientRect(), k=f.width/1440; if(r.bottom<0||r.top>900)return null; return {x:f.left-b.left+r.left*k,y:f.top-b.top+r.top*k,w:r.width*k,h:r.height*k}}
  var remark=null; setInterval(function(){if(remark&&!area.hidden)remark()},400);
  function liveRects(){var s=T().steps[idx]; if(!s||!s.tryit||!s.tryit.live||done[idx])return []; var out=[];
    s.tryit.live.split(',').forEach(function(q){q=q.trim(); var d=document, fr=null; if(q.indexOf('T:')===0){d=TD(); fr=frame; q=q.slice(2)} else if(q.indexOf('S:')===0){d=SD(); fr=sframe; q=q.slice(2)} else if(q.indexOf('U:')===0){d=UD(); fr=uframe; q=q.slice(2)} if(!d)return;
      $$(q,d).forEach(function(el){var ks=$$('button,a,input,textarea,[data-ref],[data-pick5],.rm-hit',el); if(!ks.length)ks=[el]; ks.slice(0,80).forEach(function(k){var r=mapRect(k,fr); if(r)out.push(r)})})});
    return out}
  function targets(){if(idx>=stepsN())return []; var s=T().steps[idx]; var t=typeof s.target==='function'?s.target():(s.target||[]); return t.map(rectOf).filter(Boolean)}
  function stepsN(){return T().steps.length}
  function tick(){
    if(area.hidden){raf=0;return}
    var tgt=targets();
    if(cur.length!==tgt.length)cur=tgt.map(function(r){return {x:r.x,y:r.y,w:r.w,h:r.h}});
    var k=reduce?1:.2;
    cur.forEach(function(c,i){var t=tgt[i]; c.x+=(t.x-c.x)*k; c.y+=(t.y-c.y)*k; c.w+=(t.w-c.w)*k; c.h+=(t.h-c.h)*k});
    dimA+=((dimOn?1:0)-dimA)*(reduce?1:.15);
    var W=box.clientWidth,H=box.clientHeight, hl=T().theme.hl;
    var holes='',rings='';
    cur.forEach(function(c){var a='x="'+c.x.toFixed(1)+'" y="'+c.y.toFixed(1)+'" width="'+Math.max(0,c.w).toFixed(1)+'" height="'+Math.max(0,c.h).toFixed(1)+'" rx="10"';
      holes+='<rect '+a+' fill="#000"/>';
      rings+='<rect '+a+' fill="none" stroke="'+hl+'" stroke-width="12" opacity="'+(dimA*.22).toFixed(2)+'"/><rect '+a+' fill="none" stroke="'+hl+'" stroke-width="3.5" opacity="'+dimA.toFixed(2)+'"/>'});
    ov.setAttribute('viewBox','0 0 '+W+' '+H);
    ov.innerHTML='<defs><mask id="hole"><rect width="'+W+'" height="'+H+'" fill="#fff"/>'+holes+'</mask></defs><rect width="'+W+'" height="'+H+'" fill="rgb(4,6,10)" opacity="'+(dimA*.68).toFixed(3)+'" mask="url(#hole)"/>'+rings;
    raf=requestAnimationFrame(tick);
  }
  function loop(){if(!raf)raf=requestAnimationFrame(tick)}
  scroller.addEventListener('scroll',function(){place()});

  function narrow(){return window.innerWidth<=860}
  /* ---------- placing the card: never over what is being explained ----------
     Every candidate spot is scored by how much it covers the lit area, any popup
     the page has opened, and the controls the user has to click. When nothing
     fits, the card shrinks to its essentials. The user can drag it anywhere; it
     then stays where they put it until they press Auto-place. */
  var pinned=null, curSpot=null, dragging=null;
  function popRects(){var out=[]; [[TD(),frame],[SD(),sframe],[UD(),uframe]].forEach(function(p){var d=p[0],fr=p[1]; if(!d||fr.hidden)return;
      ['#sheet.on','#peek.on','.frz5'].forEach(function(q){$$(q,d).forEach(function(e){var r=mapRect(e,fr); if(r&&r.w>20&&r.h>20)out.push(r)})});
      if(d.body&&d.body.classList.contains('chat-open')){['#chat'].forEach(function(q){var e=d.querySelector(q); var r=e&&mapRect(e,fr); if(r&&r.w>20)out.push(r)})}});
    return out}
  function ovl(a,r){var ix=Math.max(0,Math.min(a.x+a.w,r.x+r.w)-Math.max(a.x,r.x)), iy=Math.max(0,Math.min(a.y+a.h,r.y+r.h)-Math.max(a.y,r.y)); return ix*iy}
  function spotScore(a,rs,hot,pops){var s=0, A=a.w*a.h; rs.forEach(function(r){s+=4*ovl(a,r)/A}); pops.forEach(function(r){s+=6*ovl(a,r)/A}); hot.forEach(function(r){if(ovl(a,r)>0)s+=1.5}); return s}
  function bestSpot(W,H,cw,ch,rs,hot,pops){
    var g=22, cands=[];
    if(rs.length){var u=rs.reduce(function(a,r){return {l:Math.min(a.l,r.x),t:Math.min(a.t,r.y),r:Math.max(a.r,r.x+r.w),b:Math.max(a.b,r.y+r.h)}},{l:1e9,t:1e9,r:-1e9,b:-1e9});
      cands.push([u.r+g,u.t,'r'],[u.l-cw-g,u.t,'l'],[u.l,u.b+g,'c'],[u.l,u.t-ch-g,'c'],[u.r+g,u.b-ch,'r'],[u.l-cw-g,u.b-ch,'l'],[u.r-cw,u.b+g,'c'],[u.r-cw,u.t-ch-g,'c']);
      rs.forEach(function(r){cands.push([r.x+r.w+g,r.y,'r'],[r.x-cw-g,r.y,'l'],[r.x,r.y+r.h+g,'c'],[r.x,r.y-ch-g,'c'])})}
    [12,(W-cw)/2,W-cw-12].forEach(function(x,i){[12,(H-ch)/2,H-ch-12].forEach(function(y){cands.push([x,y,i===2?'l':(i===0?'r':'c')])})});
    var best=null;
    cands.forEach(function(c){var x=Math.max(12,Math.min(c[0],W-cw-12)), y=Math.max(12,Math.min(c[1],H-ch-12)), a={x:x,y:y,w:cw,h:ch};
      var s=spotScore(a,rs,hot,pops);
      if(rs.length){var cx=x+cw/2, cy=y+ch/2, tx=rs[0].x+rs[0].w/2, ty=rs[0].y+rs[0].h/2; s+=Math.hypot(cx-tx,cy-ty)/(W*20)}
      if(!best||s<best.s-1e-6)best={x:x,y:y,side:c[2],s:s}});
    return best}
  function setMinLabel(){var mb=$('#cMin'); if(mb)mb.textContent=card.classList.contains('compact')?'Show more':'Shrink'}
  var cmode='auto';
  var docked=false, dockTimers=[];
  function undock(){if(!docked)return; docked=false; area.classList.remove('dock'); box.style.width=''; fit()}
  function decideDock(){ if(area.hidden||narrow()||pinned||idx>=stepsN())return; var rs=targets(); if(!rs.length)return;
    undock(); var b=box.getBoundingClientRect(), W=b.width, H=b.height, cw=Math.min(350,Math.max(270,W*.3)), hot=liveRects(), pops=popRects();
    var tr=function(w,c){card.style.width=w+'px'; card.classList.toggle('compact',c); return bestSpot(W,H,w,card.offsetHeight,rs,hot,pops).s};
    var best=Math.min(tr(cw,false),tr(250,false),tr(cw,true),tr(250,true)); card.classList.remove('compact');
    if(best>0.12){docked=true; area.classList.add('dock'); var aw=area.clientWidth; box.style.width=(aw-cw-24)+'px'; fit(); curSpot=null}
    place(true)}
  function place(force){
    if(area.hidden||narrow()||dragging)return;
    if(docked&&!pinned){var aw=area.clientWidth, cw0=Math.min(350,Math.max(270,box.clientWidth*.3)); card.style.width=cw0+'px'; card.className='docked'+(cmode==='min'?' compact':''); card.style.left=(aw-cw0)+'px'; card.style.top='0px'; setMinLabel(); return}
    var b=box.getBoundingClientRect(), W=b.width, H=b.height;
    var cw=Math.min(350,Math.max(270,W*.3)); card.style.width=cw+'px';
    if(pinned){card.className='pinned'+(cmode==='min'?' compact':''); var x=Math.max(0,Math.min(pinned.fx*W,W-cw)), y=Math.max(0,Math.min(pinned.fy*H,H-40)); card.style.left=x+'px'; card.style.top=y+'px'; setMinLabel(); return}
    var rs=(idx>=stepsN())?[]:targets();
    if(!rs.length){card.className=cmode==='min'?'compact':''; var chh=card.offsetHeight; card.style.left=((W-cw)/2)+'px'; card.style.top=Math.max(12,(H-chh)/2)+'px'; curSpot=null; setMinLabel(); return}
    var hot=liveRects(), pops=popRects(), use, isCompact;
    var trial=function(w,c){card.style.width=w+'px'; card.classList.toggle('compact',c); var h=card.offsetHeight, s=bestSpot(W,H,w,h,rs,hot,pops); s.w=w; s.h=h; if(w<cw)s.s+=0.02; return s};
    var full=trial(cw,false), f2=trial(250,false); if(f2.s<full.s-0.05)full=f2;
    var small=trial(cw,true), s2=trial(250,true); if(s2.s<small.s-0.05)small=s2;
    card.classList.remove('compact'); var chFull=full.h, chC=small.h;
    if(cmode==='min'){use=small; isCompact=true}
    else if(cmode==='max'){use=full; isCompact=false}
    else if(full.s>0.3&&small.s<full.s-0.15){use=small; isCompact=true}
    else {use=full; isCompact=false}
    var hNow=isCompact?chC:chFull; if(curSpot&&curSpot.w&&curSpot.w!==(use.w||cw)){card.style.width=curSpot.w+'px'; card.classList.toggle('compact',isCompact); hNow=card.offsetHeight}
    if(!force&&curSpot&&curSpot.compact===isCompact){var keep=spotScore({x:curSpot.x,y:curSpot.y,w:cw,h:hNow},rs,hot,pops); if(keep<=use.s+0.12)use={x:curSpot.x,y:curSpot.y,side:curSpot.side,s:keep,w:curSpot.w}}
    card.style.width=(use.w||cw)+'px';
    card.className=(use.side==='c'?'':use.side)+(isCompact?' compact':'');
    card.style.left=use.x+'px'; card.style.top=use.y+'px'; curSpot={x:use.x,y:use.y,side:use.side,s:use.s,compact:isCompact,w:use.w||cw};
    setMinLabel();
  }
  setInterval(function(){if(!area.hidden&&!dragging)place()},500);
  /* dragging the card by its Move handle or its top line */
  card.addEventListener('pointerdown',function(e){var h=e.target.closest&&e.target.closest('.grip, .eh'); if(!h||narrow())return; e.preventDefault(); var b=area.getBoundingClientRect(); dragging={sx:e.clientX,sy:e.clientY,ox:card.offsetLeft,oy:card.offsetTop,W:b.width,H:box.getBoundingClientRect().height}; card.classList.add('drag'); try{card.setPointerCapture(e.pointerId)}catch(x){}});
  card.addEventListener('pointermove',function(e){if(!dragging)return; var x=Math.max(0,Math.min(dragging.ox+e.clientX-dragging.sx,dragging.W-card.offsetWidth)), y=Math.max(0,Math.min(dragging.oy+e.clientY-dragging.sy,dragging.H-40)); card.style.left=x+'px'; card.style.top=y+'px'});
  var endDrag=function(){if(!dragging)return; var d=dragging; dragging=null; card.classList.remove('drag'); if(Math.abs(card.offsetLeft-d.ox)+Math.abs(card.offsetTop-d.oy)>4){if(docked){undock()} pinned={fx:Math.min(card.offsetLeft,box.clientWidth-card.offsetWidth)/box.clientWidth, fy:card.offsetTop/box.clientHeight}; var a=$('#cAuto'); if(a)a.hidden=false} place()};
  card.addEventListener('pointerup',endDrag); card.addEventListener('pointercancel',endDrag);
  card.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('#cAuto,#cMin'); if(!a)return;
    if(a.id==='cAuto'){pinned=null; a.hidden=true; curSpot=null; place(true); return}
    cmode=card.classList.contains('compact')?'max':'min'; curSpot=null; place(true)});
  function scrollFor(s){
    if(s.scroll==='top')scroller.scrollTop=0;
    else if(s.scroll){var el=$(s.scroll); scroller.scrollTop=el.offsetTop-8}
    nav.scrollTop=s.navTo?($(s.navTo).offsetTop-12):0;
  }
  function dotsHtml(n){var d=''; for(var i=0;i<stepsN();i++)d+='<i class="'+(i===n?'on':(i<n?'seen':''))+'"></i>'; return d}
  function sorterHtml(){return '<div class="sort">'+SORT.map(function(s,i){var st=sortState[i]; return '<div class="sq'+(st==='ok'?' ok':'')+'" data-i="'+i+'"><span class="q">“'+s.q+'”</span>'+(st==='ok'?'<span class="why">✓ '+(s.a==='chat'?'Chat':'Tool')+'. '+s.ok+'</span>':'<span class="bb"><button type="button" data-a="chat">Chat</button><button type="button" data-a="tool">Tool</button></span>'+(st?'<span class="why">'+s.no+'</span>':''))+'</div>'}).join('')+'</div>'}
  function CTL(){return '<div class="ctl"><button type="button" class="grip" aria-label="Drag to move this card" title="Drag to move this card">⠇⠇ Move</button><span class="sp"></span><button type="button" id="cAuto"'+(pinned?'':' hidden')+'>Auto-place</button><button type="button" id="cMin">Shrink</button></div>'}
  function render(){
    if(offTry){offTry.forEach(function(f){f()}); offTry=null}
    remark=null;
    $$('.tryable').forEach(function(e){e.classList.remove('tryable')});
    (function(){[TD(),SD(),UD()].forEach(function(d){if(d)$$('.tour-live',d).forEach(function(e){e.classList.remove('tour-live')})})})();
    clearTimeout(revealT); cmpT.forEach(clearTimeout); cmpT=[]; cmpLit=null;
    var t=T(), N=stepsN();
    if(idx>=N){renderEnd();return}
    var s=t.steps[idx]; dimOn=s.dim!==false;
    if(s.view)view(s.view);
    if(s.tryit&&s.tryit.ensure&&!done[idx])s.tryit.ensure();
    if(s.enter)s.enter(!!done[idx]);
    if(!s.enter||s.view==='home')scrollFor(s);
    cmode='auto'; curSpot=null;
    dockTimers.forEach(clearTimeout); undock(); dockTimers=[setTimeout(decideDock,1200),setTimeout(function(){if(!docked)decideDock()},3200)];
    var h=CTL()+'<div class="eh"><span>Tour '+t.n+' · '+t.name+'</span><span>'+(idx+1)+' of '+N+'</span></div>';
    h+='<h2 id="cTitle">'+s.title+'</h2><div class="dots">'+dotsHtml(idx)+'</div>';
    if(s.partLbl&&!done[idx])h+='<span class="live-lbl" id="partLbl">'+(typeof s.partLbl==='string'?s.partLbl:'Press Send to begin')+'</span>';
    h+='<div class="body">'+s.body.map(function(p){return '<p>'+p+'</p>'}).join('')+'</div>';
    if(s.note)h+='<div class="note">'+s.note+'</div>';
    if(s.sorter)h+=sorterHtml();
    if(s.demo)h+=demoHtml();
    if(s.loop)h+=loopHtml(); if(s.spick)h+=suitePickHtml(); if(s.ceo)h+=ceoHtml();
    if(idx>0&&t.n===1)h+='<div class="later">'+LATER+'</div>';
    if(s.tryit&&s.tryit.button&&!done[idx])h+='<button class="go" type="button" id="cPlay" style="margin:0 0 10px">\u25B6 '+s.tryit.button+'</button>';
    if(s.tryit)h+='<div class="try'+(done[idx]?' done':'')+'"><span class="k">'+(done[idx]?'✓ Done':'Try it')+'</span><span>'+s.tryit.ask+(done[idx]?'<span class="res">'+s.tryit.res+'</span>':'')+'</span></div>';
    var need=s.tryit&&!done[idx];
    h+='<div class="cfoot">'+(idx>0?'<button class="lnk" type="button" id="cBack">Back</button>':'')+'<button class="lnk" type="button" id="cSkip">Skip tour</button><span class="sp"></span>'+(need?'<button class="lnk" type="button" id="cSkipTry">Skip this</button>':'')+'<button class="go" type="button" id="cNext"'+(need?' disabled':'')+'>'+(idx===0?'Start':'Proceed')+'</button></div>';
    card.innerHTML=h;
    if(s.tryit&&s.tryit.live&&!done[idx]){var lv=s.tryit.live.split(',').map(function(x){return x.trim()}); var mark=function(){var d=TD(), sd=SD(), ud=UD(); lv.forEach(function(q){if(q.indexOf('T:')===0){if(d)$$(q.slice(2),d).forEach(function(e){e.classList.add('tour-live')})} else if(q.indexOf('S:')===0){if(sd)$$(q.slice(2),sd).forEach(function(e){e.classList.add('tour-live')})} else if(q.indexOf('U:')===0){if(ud)$$(q.slice(2),ud).forEach(function(e){e.classList.add('tour-live')})} else $$(q).forEach(function(e){e.classList.add('tryable')})})}; mark(); remark=mark; if(lv.some(function(q){return q.indexOf('T:')===0}))openTool(false,mark); if(lv.some(function(q){return q.indexOf('S:')===0}))openSim(false,mark); if(lv.some(function(q){return q.indexOf('U:')===0}))openSuite(null,false,mark)}
    toolLock();
    if(s.tryit&&!done[idx]){
      offTry=[on(s.tryit.ev,function(){done[idx]=true; var keep=idx; setTimeout(function(){if(idx===keep)render()},reduce?0:300)})];
      if(s.tryit.arm)offTry.push(s.tryit.arm());
    }
    if(s.sorter)$$('.sq button',card).forEach(function(b){b.addEventListener('click',function(){var row=b.closest('.sq'), i=+row.dataset.i; sortState[i]=(SORT[i].a===b.dataset.a)?'ok':'no'; if(sortState[i]==='no'){row.classList.remove('no'); void row.offsetWidth} render(); var r2=$('.sq[data-i="'+i+'"]',card); if(sortState[i]==='no')r2.classList.add('no'); if(SORT.every(function(x,j){return sortState[j]==='ok'}))fire('sorted')})});
    if($('#cPlay'))$('#cPlay').addEventListener('click',function(){this.disabled=true; fire('play')});
    if(s.demo)bindDemo();
    if(s.loop)bindLoop(); if(s.spick)bindSuitePick();
    $('#cNext').addEventListener('click',function(){go(idx+1)});
    if($('#cBack'))$('#cBack').addEventListener('click',function(){go(idx-1)});
    if($('#cSkipTry'))$('#cSkipTry').addEventListener('click',function(){done[idx]='skipped'; go(idx+1)});
    $('#cSkip').addEventListener('click',skip);
    setProg(t.n,{step:idx,finished:prog(t.n).finished});
    $('#underTxt').textContent='Tour '+t.n+' · '+t.name+(full?' · full tour':'');
    requestAnimationFrame(function(){place(); setTimeout(place,420); setTimeout(place,1100)});
    var f=$('#cNext'); if(f&&!f.disabled)f.focus({preventScroll:true});
  }
  function nextTour(){for(var i=tIx+1;i<TOURS.length;i++)if(built(TOURS[i]))return TOURS[i]; return TOURS[tIx+1]}
  function renderEnd(){
    dockTimers.forEach(clearTimeout); undock(); var t=T(), nt=nextTour(); dimOn=false; app.classList.remove('locked'); setTimeout(function(){toolLock(); simLock(); suiteLock()},0);
    var nb=nt?(built(nt)?'<button class="go" type="button" id="cNextTour">Next tour: '+nt.name+'</button>':'<button class="go" type="button" disabled title="Being built">Next: '+nt.name+' (coming)</button>'):'';
    card.innerHTML=CTL()+'<div class="eh"><span>Tour '+t.n+' · Done</span><span>'+stepsN()+' of '+stepsN()+'</span></div><h2 id="cTitle">'+t.end.title+'</h2><div class="body">'+t.end.body.map(function(p){return '<p>'+p+'</p>'}).join('')+'<p>The screen behind is yours to click around now. Sending stays off.</p></div><div class="note">'+t.end.note+'</div><div class="cfoot"><button class="lnk" type="button" id="cAgain">Take it again</button><button class="lnk" type="button" id="cPick">All tours</button><span class="sp"></span>'+nb+'</div>';
    $('#cAgain').addEventListener('click',function(){start(tIx,0,full)});
    $('#cPick').addEventListener('click',showPicker);
    if($('#cNextTour'))$('#cNextTour').addEventListener('click',function(){start(TOURS.indexOf(nextTour()),0,full)});
    setProg(t.n,{step:0,finished:true});
    requestAnimationFrame(function(){place(); setTimeout(place,420)});
  }
  function go(i){idx=Math.max(0,Math.min(stepsN(),i)); app.classList.toggle('locked',idx<stepsN()); render()}
  function skip(){var t=T(); setProg(t.n,{step:idx<stepsN()?idx:0,finished:prog(t.n).finished}); showPicker()}

  /* ================= picker ================= */
  function buildList(){
    $('#tourList').innerHTML=TOURS.map(function(t){var h=t.theme, p=prog(t.n), b=built(t);
      var tag=b?(p.finished?'✓ Done':(p.step>0?'Resume':'Start')):'Coming next';
      var st='--t1:'+h.c1+';--t2:'+h.c2+';--th:'+(b?h.key:h.hl)+';--tk:'+h.key+';--tki:'+h.keyInk;
      var inner='<span class="n">'+t.n+'</span><h3>'+t.name+'</h3><p>'+t.short+'</p><span class="meta"><span>'+t.mins+'</span><span class="tag">'+tag+'</span></span>';
      return '<li>'+(b?'<button class="tour ready" type="button" data-t="'+(t.n-1)+'" style="'+st+'">'+inner+'</button>':'<div class="tour" style="'+st+'">'+inner+'</div>')+'</li>'}).join('');
    $$('#tourList [data-t]').forEach(function(b){b.addEventListener('click',function(){var i=+b.dataset.t, p=prog(i+1); start(i,p.finished?0:p.step,false)})});
    var s=load(), r=$('#resume'), ln=s.last, lp=ln?prog(ln):null;
    if(lp&&lp.step>0&&!lp.finished){r.hidden=false; r.textContent='Resume tour '+ln+' at step '+(lp.step+1); r.dataset.t=ln-1; r.dataset.s=lp.step}else r.hidden=true;
  }
  function showPicker(){undock(); closeTool(); closeSim(); closeSuite(); clearTimeout(revealT); cmpT.forEach(clearTimeout); area.hidden=true; picker.hidden=false; buildList(); window.scrollTo({top:0})}
  function start(ti,step,isFull){tIx=ti; full=!!isFull; picker.hidden=true; area.hidden=false; done={}; sortState={}; app.classList.remove('light'); view('home'); resetThread(); closeTool(); closeSim(); closeSuite(); theme(T()); if(T().setup)T().setup(); fit(); loop(); go(step||0); area.scrollIntoView({block:'start',behavior:reduce?'auto':'smooth'})}
  $('#fullTour').addEventListener('click',function(){start(0,0,true)});
  $('#pickOne').addEventListener('click',function(){$('#tourList').scrollIntoView({behavior:reduce?'auto':'smooth',block:'center'}); var f=$('#tourList .ready'); if(f)f.focus({preventScroll:true})});
  $('#resume').addEventListener('click',function(){start(+this.dataset.t,+this.dataset.s,false)});
  $('#notNow').addEventListener('click',function(){$('#lede').textContent='No problem. The tours stay here under Help → Guided tours whenever you want them.'});
  $('#toPicker').addEventListener('click',showPicker);
  $('#restart').addEventListener('click',function(){start(tIx,0,full)});
  view('home'); buildList();
})();
