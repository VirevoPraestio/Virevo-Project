  /* ================= the real Tool (Tour 3) =================
     The Discharge Tool is the live page itself (its own HTML, CSS and script,
     captured from virevo.works/discharge), loaded into a frame over the stage.
     Selectors that start with "T:" point inside it. */
  var frame=$('#toolFrame'), toolLoaded=false, toolWait=[];
  function TD(){try{return toolLoaded?frame.contentDocument:null}catch(e){return null}}
  function openTool(fresh,then){
    frame.hidden=false;
    if(then)toolWait.push(then);
    if(fresh||!frame.dataset.on){toolLoaded=false; frame.dataset.on='1'; frame.srcdoc=TOOLDOC}
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
    toolLock(); var w=toolWait; toolWait=[]; w.forEach(function(f){f()});
    fire('toolopen');
  });
  function toolLock(){var d=TD(); if(!d)return; var on=!area.hidden&&tIx===2&&idx<stepsN(); d.documentElement.classList.toggle('tour-lock',on)}
  var DESKKEY={dx:'diagnosis',sol:'solutions',aut:'automations',prc:'processes'};
  function toolDesk(p){openTool(false,function(){var d=TD(), dis=d.getElementById('dis'); if(dis.getAttribute('data-panel')===p)return; var a=d.querySelector('.rail-tab[href="#'+DESKKEY[p]+'"]'); if(a)a.click()})}
  function toolSheet(){var d=TD(); if(!d)return; var dis=d.getElementById('dis'); if(dis.hasAttribute('data-panel')){dis.removeAttribute('data-panel'); $$('.rail-tab',d).forEach(function(x){x.removeAttribute('aria-current')}); var b=d.getElementById('barW'); if(b)b.textContent='with Tojo'}}
  function toolView1(fresh){openTool(!!fresh,function(){toolSheet()})}
  function toolView2(){openTool(false,function(){var d=TD(), dis=d.getElementById('dis'); toolSheet(); if(dis.getAttribute('data-view')==='1'){var c=d.querySelector('.v1 .ct-chip:not(.w-only)')||d.querySelector('.v1 .ct-chip'); if(c){c.click(); var f=d.getElementById('ctForm'); if(f&&f.requestSubmit)f.requestSubmit()}}})}
  $$('#subOps a').forEach(function(a,i){if(i===0){a.id='navDischarge'; a.addEventListener('click',function(){openTool(true)})}});
