/* ===== Page 3 · Option C · Ready-made sixes: start from a set Tojo has put together, then swap ===== */
LOOKS.push({ key:"sets", page:"p3", step:2, letter:"C", name:"Ready-made sixes", note:"<b>C · Ready-made sixes.</b> Start from a set instead of a blank page. Tojo offers four sixes, each built for a different worry: a balanced six, margin, patient flow and cash. Each card shows what it covers and what it leaves out. Pick one, then swap any KPI in it for another from the same department or any other.",
css: P3_CSS + `
.lk-web .sets{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin-bottom:20px}
.lk-web .set{border:2px solid var(--w-line);border-radius:16px;background:var(--w-sheet);padding:14px;display:flex;flex-direction:column;gap:8px;min-width:0}
.lk-web .set.on{border-color:var(--w-ink);box-shadow:8px 8px 0 rgba(22,33,62,.14)}
.lk-web .set h2{margin:0;font-family:var(--f-num);font-weight:400;font-size:28px;line-height:1}
.lk-web .set p{margin:0;font-size:13px;color:var(--w-mute)}
.lk-web .set ol{margin:0;padding-left:20px;font-size:13px;display:grid;gap:3px}
.lk-web .set ol li::marker{font-family:var(--f-num);color:var(--w-gold-ink)}
.lk-web .set ol small{color:var(--w-mute)}
.lk-web .set .facts{display:grid;grid-template-columns:repeat(3,1fr);gap:6px;margin-top:auto}
.lk-web .set .facts div{border:1px solid var(--w-line);border-radius:8px;padding:6px;background:#fff;font-size:11px;color:var(--w-mute);line-height:1.2}
.lk-web .set .facts b{display:block;font-family:var(--f-num);font-weight:400;font-size:22px;color:var(--w-ink)}
.lk-web .set .miss{font-size:12px;color:var(--w-none)}
.lk-web .set .hand{font-family:var(--f-hand);font-weight:700;font-size:22px;color:var(--w-gold-ink);line-height:1}
.lk-web .mine3{border:2px solid var(--w-ink);border-radius:16px;background:var(--w-sheet);padding:14px 16px;margin-bottom:18px}
.lk-web .mine3 h2{margin:0 0 4px;font-family:var(--f-num);font-weight:400;font-size:30px;line-height:1}
.lk-web .mine3>p{margin:0 0 12px;font-size:13px;color:var(--w-mute)}
.lk-web .slots{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}
.lk-web .slot{border:1.5px solid var(--w-line);border-radius:12px;padding:10px;background:#fff;display:flex;flex-direction:column;gap:6px;min-width:0}
.lk-web .slot .top{display:flex;gap:8px;align-items:baseline}
.lk-web .slot .top i{font-style:normal;font-family:var(--f-num);font-size:26px;color:var(--w-gold)}
.lk-web .slot small{font-size:12px;color:var(--w-mute)}
.lk-web .slot label{font-size:11.5px;font-weight:600;color:var(--w-mute)}
.lk-web .slot select{min-height:40px;border:1.5px solid var(--w-line);border-radius:8px;font:inherit;font-size:13px;background:#fff;color:var(--w-ink);padding:0 6px;max-width:100%}
@media (max-width:1150px){.lk-web .sets{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:640px){.lk-web .sets,.lk-web .slots{grid-template-columns:1fr}}
`,
mount(stage){
  p3Mount(stage, `${p3Head("Start from a ready-made six", "Each set is built for a different first worry. Pick the one closest to yours, then swap any KPI. You can always build your own from the boxes below.")}
    <div class="sets" data-v="sets"></div>
    <section class="mine3"><h2>Your six</h2><p>Change any of them. The list holds every KPI on page 2, by department.</p><div class="slots" data-v="slots"></div></section>
    <div class="lev-wrap">${leverTokensHTML()}</div>${p3Cta()}`);
  this.drawSets(stage);
},
drawSets(root){
  const box = root.querySelector('[data-v="sets"]'); const cur = S3.sel.slice().sort().join();
  box.innerHTML = SETS3.map(s => { const ids = setIds(s), c = cover3(ids), on = ids.slice().sort().join() === cur && cur;
    const missing = P3G.filter(g => !c.depts.has(g)).map(g => GNAME[g]);
    return `<article class="set${on?" on":""}"><h2>${esc(s.n)}</h2><p>${esc(s.why)}</p><ol>${ids.map(id=>`<li>${nameBtn(id)} <small>${esc(GNAME[ITEMS[id].g])}${hasData(id)?"":" · no data yet"}</small></li>`).join("")}</ol>
      <div class="facts"><div><b>${c.levN}</b>changes brought in</div><div><b>${c.depts.size}/5</b>departments</div><div><b>${ids.length - c.nodata.length}/${ids.length}</b>with data</div></div>
      ${missing.length?`<div class="miss">Leaves out: ${esc(missing.join(", "))}</div>`:`<div class="hand">covers every department</div>`}
      <button type="button" class="act${on?"":" ghost"}" data-p3="set:${s.key}">${on?"In use":"Use this six"}</button></article>`; }).join("");
  box.querySelectorAll("[data-p3]").forEach(b => b.addEventListener("click", () => { const s = SETS3.find(x=>x.key===b.dataset.p3.slice(4)); setSel3(setIds(s)); }));
},
update(root){ p3Sync(root); syncTokens(root); this.drawSets(root);
  const pool = poolIds(); const opts = sel => P3G.map(g => `<optgroup label="${esc(GNAME[g])}">${pool.filter(id=>ITEMS[id].g===g).map(id => `<option value="${id}" ${id===sel?"selected":""} ${id!==sel && S3.sel.includes(id)?"disabled":""}>${esc(ITEMS[id].n)}${hasData(id)?"":" (no data yet)"}</option>`).join("")}</optgroup>`).join("");
  const box = root.querySelector('[data-v="slots"]');
  box.innerHTML = Array.from({length:6},(_,i) => { const id = S3.sel[i];
    return `<div class="slot"><div class="top"><i>${i+1}</i>${id?nameBtn(id):`<span style="color:var(--w-mute);font-size:13px">Empty</span>`}</div>${id?`<small>${esc(kpiLine(id))} · brings in ${leversOf(id).length} changes</small>`:""}
      <label for="sw3-${i}">${id?"Swap for":"Choose a KPI"}</label><select id="sw3-${i}" data-slot="${i}"><option value="">—</option>${opts(id)}</select></div>`; }).join("");
  box.querySelectorAll("[data-slot]").forEach(s => s.addEventListener("change", () => { const i = +s.dataset.slot, v = s.value; const next = S3.sel.slice(); if (v) next[i] = v; else next.splice(i,1); setSel3(next.filter(Boolean)); }));
}});
