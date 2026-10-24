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
  uframe.addEventListener('load',function(){
    var d=uframe.contentDocument; if(!d||!d.getElementById('stage'))return;
    suiteLoaded=true; suiteSt={}; suitesSeen[suiteKey]=1;
    /* name the shared parts so every look can be pointed at the same way */
    var w=d.querySelector('#stage > div > div'); if(w){var wrap=w.querySelector('.wrap')||w; var kids=Array.prototype.slice.call(wrap.children), zi=0;
      kids.forEach(function(k){ if(k.tagName==='NAV')k.id='u-bar'; else if(k.classList.contains('head'))k.id='u-head'; else if(k.tagName==='SECTION'){var t=k.textContent.slice(0,200); k.id=/^\s*\d?\s*KPIs/.test(t)||/\bKPIs\b/.test((k.querySelector('h2,h3')||{}).textContent||'')?'u-kpis':/Taskboards/.test(t.slice(0,80))?'u-tasks':/Project Status/.test(t.slice(0,80))?'u-status':(zi++===0?'u-links':'')} else if(!k.id&&k.tagName==='DIV')k.id='u-watch'})}
    d.addEventListener('click',function(e){var t=e.target; if(!t.closest)return; var tb=t.closest('[data-tab]'); if(tb&&tb.dataset.tab!=='overview')setTimeout(function(){fire('u:tab')},150); if(t.closest('[data-view="week"]'))setTimeout(function(){fire('u:week')},150)},true);
    d.defaultView.addEventListener('scroll',function(){place()});
    clearInterval(suitePoll);
    suitePoll=setInterval(function(){var d=UD(); if(!d||uframe.hidden)return;
      var pe=d.querySelector('#peek.on'), pk=pe?pe.textContent.slice(0,80):'', sh=d.querySelector('#sheet.on'), sk=sh?sh.textContent.slice(0,80):'', ch=d.body.classList.contains('chat-open');
      if(pk&&pk!==suiteSt.pk)fire('u:peek'); suiteSt.pk=pk;
      if(sk&&sk!==suiteSt.sk)fire('u:sheet'); suiteSt.sk=sk;
      if(ch&&!suiteSt.ch)fire('u:chat'); suiteSt.ch=ch;
    },300);
    suiteLock(); var q=suiteWait; suiteWait=[]; q.forEach(function(f){f()});
    fire('suiteopen'); fire('suite:'+suiteKey);
  });
  function suiteLock(){var d=UD(); if(!d)return; var on=!area.hidden&&tIx===5&&idx<stepsN(); d.documentElement.classList.toggle('tour-lock',on)}
  function uScrollTo(sel,off){var d=UD(); if(!d)return; var el=d.querySelector(sel); var w=d.defaultView; if(!el){w.scrollTo(0,0);return} w.scrollTo(0,Math.max(0,el.getBoundingClientRect().top+w.scrollY-(off==null?20:off)))}
  function uClean(){var d=UD(); if(!d)return; var p=d.getElementById('peek'); if(p)p.classList.remove('on'); var s=d.getElementById('sheet'); if(s)s.classList.remove('on'); if(d.body.classList.contains('chat-open')){var x=d.querySelector('#chat button[aria-label*="inimise"], #chatClose'); if(x)x.click(); else d.body.classList.remove('chat-open')}}
  function suiteAt(key,sel,off){openSuite(key,false,function(){uClean(); uScrollTo(sel,off)})}
  (function(){var MAP={'Discharge Summary':'discharge','Billing & Insurance':'billing','Admission Process':'admission','Diagnostic Scheduling':'diagnostic','Procurement':'procurement'};
    $$('#subAuto a').forEach(function(a){var k=MAP[a.textContent.trim()]; if(k){a.dataset.suite=k; a.addEventListener('click',function(){view('home'); openSuite(k,true)})} else a.addEventListener('click',function(){say(a.textContent.trim()+' is still being built.')})})})();
  /* ---------- Tour 6 card extras ---------- */
  var LOOP=[['Do','The suite closes the bill for bed 12 at 11:40.'],['Watch','At 12:20 it is still open: 40 minutes past its time.'],['Decide','The billing desk is one person short today.'],['Correct','It moves the bill to the next free biller and tells the billing head.'],['Learn','Next Tuesday it plans a second biller before noon.']];
  function loopHtml(){return '<div class="loop"><ol id="lpN">'+LOOP.map(function(l,i){return '<li data-i="'+i+'"><b>'+l[0]+'</b><span>'+l[1]+'</span></li>'}).join('')+'</ol><button type="button" class="go" id="lpGo">▶ Run the loop</button><small class="dmx">Example only.</small></div>'}
  function bindLoop(){var g=$('#lpGo'); if(!g)return; g.addEventListener('click',function(){g.disabled=true; var lis=$$('#lpN li'); lis.forEach(function(l){l.classList.remove('on')}); lis.forEach(function(l,i){setTimeout(function(){l.classList.add('on'); if(i===lis.length-1){g.disabled=false; g.textContent='↻ Run it again'; fire('loop')}},reduce?0:i*1100)})})}
  function suitePickHtml(){return '<div class="spick">'+Object.keys(SUITE_NAMES).map(function(k){return '<button type="button" data-k="'+k+'" class="'+(k===suiteKey?'on':'')+(suitesSeen[k]?' seen':'')+'">'+SUITE_NAMES[k]+'</button>'}).join('')+'</div>'}
  function bindSuitePick(){$$('.spick button',card).forEach(function(b){b.addEventListener('click',function(){openSuite(b.dataset.k,false,function(){uScrollTo('#u-bar',20); $$('.spick button',card).forEach(function(x){x.classList.toggle('on',x.dataset.k===suiteKey); x.classList.toggle('seen',!!suitesSeen[x.dataset.k])}); if(Object.keys(suitesSeen).length>=3)fire('suites3')})})})}
  function ceoHtml(){return '<div class="ceo"><div class="c0"><b>MyCEO Agent</b><span>Holds your targets, settles clashes between departments, closes yesterday’s P&amp;L by 7 AM.</span></div><div class="c1"><span><b>Task Master</b>Operations</span><span><b>Quarter Master</b>Supply chain</span><span><b>Ward Round</b>Clinical</span><span><b>Referral Engine</b>Marketing</span></div><div class="c2">The suites: Discharge Summary · Billing &amp; Insurance · Admission Process · Diagnostic Scheduling · Procurement · Financial Health</div></div>'}
