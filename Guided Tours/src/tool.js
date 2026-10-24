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
