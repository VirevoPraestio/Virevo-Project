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
    d.addEventListener('click',function(e){var t=e.target; if(!t.closest)return; if(t.closest('[data-pick5]'))setTimeout(function(){fire('sim:pick')},150); if(t.closest('[data-p6="owner"]'))setTimeout(function(){fire('sim:owner')},150)},false);
    d.defaultView.addEventListener('scroll',function(){place()});
    clearInterval(simPoll);
    simPoll=setInterval(function(){var d=SD(); if(!d||sframe.hidden)return;
      var st=simStep(), pk=!!(d.querySelector('#peek.on')||d.querySelector('#sheet.on')), ch=d.body.classList.contains('chat-open'), ok=!!d.querySelector('[data-p5n]');
      if(st!==simSt.st){simSt.st=st; fire('sim:step'+st)}
      if(pk&&!simSt.pk)fire('sim:peek'); simSt.pk=pk;
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
  function simGo(n,then){openSim(false,function(){var tries=0;
    (function loop(){var d=SD(), cur=simStep(); if(cur===n||tries++>8){sTop(); if(then)setTimeout(then,250); return}
      if(n<cur){var b=d.querySelector('nav.jr button[data-step="'+n+'"]'); if(b)b.click(); return setTimeout(loop,500)}
      var q=function(s){return d.querySelector(s)};
      if(cur===0&&q('[data-act="go"]'))q('[data-act="go"]').click();
      else if(cur===1&&q('[data-p2="go"]'))q('[data-p2="go"]').click();
      else if(cur===2&&q('[data-p3="go"]'))q('[data-p3="go"]').click();
      else if(cur===3){var f=q('[data-freeze]'); if(f)f.click(); setTimeout(function(){var y=q('[data-frz="yes"]'); if(y)y.click()},350)}
      else if(cur===4){var i=q('[data-p5in="by"]'); if(i&&!i.value){i.value='Sample CEO'; i.dispatchEvent(new Event('input',{bubbles:true}))} var c=q('[data-p5="confirm"]'); if(c)c.click(); setTimeout(function(){var g=q('[data-p5n]'); if(g)g.click()},350)}
      setTimeout(loop,cur>=3?900:600)})()})}
  (function(){var n=$$('#gAgents .ni').filter(function(x){return /Simulations/.test(x.textContent)})[0]; if(n){n.id='niSim'; n.addEventListener('click',function(){openSim(true)})}})();
