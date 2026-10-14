/* ===== Page 4 · Option C · By KPI: each of your six with the changes that move it ===== */
LOOKS.push({ key:"bykpi", page:"sim", step:3, letter:"C", name:"By KPI", note:"<b>C · By KPI.</b> Like the old dream-target page. Each of your six has its own section listing the changes that move it, with achievable and dream levels. A change that moves several KPIs appears under each; approving it in one place approves it everywhere. Your six stay frozen on the right; the plan's numbers sit across the top.",
css: SIM_CSS + `
.lk-web .kpis5{display:grid;gap:14px}
.lk-web .ks{border:2px solid var(--w-ink);border-radius:14px;background:var(--w-sheet);overflow:hidden}
.lk-web .ks>summary{list-style:none;cursor:pointer;display:grid;grid-template-columns:minmax(0,1fr) auto;gap:4px 16px;align-items:center;padding:12px 16px;background:#F3F5F8;border-bottom:1.5px solid var(--w-line);min-height:52px}
.lk-web .ks>summary::-webkit-details-marker{display:none}
.lk-web .ks>summary h2{margin:0;font-family:var(--f-num);font-weight:400;font-size:26px;line-height:1}
.lk-web .ks>summary h2::before{content:"▸ ";font-family:var(--f-body);font-size:16px}
.lk-web .ks[open]>summary h2::before{content:"▾ "}
.lk-web .ks .vals{display:flex;flex-wrap:wrap;gap:4px 14px;font-size:12.5px;color:var(--w-mute)}
.lk-web .ks .vals b{font-family:var(--f-num);font-weight:400;font-size:20px;color:var(--w-ink)}
.lk-web .ks .vals .now b{color:var(--w-yours)}
.lk-web .r5{display:grid;grid-template-columns:minmax(180px,1fr) minmax(0,1.5fr);gap:8px 16px;align-items:center;padding:10px 16px;border-top:1px solid #E6EAF0}
.lk-web .r5.off .nm5 .linkbtn b{color:var(--w-mute)}
.lk-web .nm5{min-width:0;display:grid;gap:2px}
.lk-web .nm5 small{font-size:11.5px;color:var(--w-mute)}
.lk-web .ks .none{padding:12px 16px;font-size:13px;color:var(--w-mute)}
@media (max-width:760px){.lk-web .r5{grid-template-columns:1fr}}
`,
mount(stage){ levels5(); if (!Object.keys(SIMR.lvl).length) ch5().forEach(id => SIMR.lvl[id] = "ach");
  const row = (id, k) => { const also = S3.sel.filter(s => s !== k && leversOf(s).includes(id)).map(s => ITEMS[s].n);
    return `<div class="r5" data-row5="${id}"><div class="nm5">${nameBtn(id)}<small>${esc(KINDNAME[leverKind(ITEMS[id])])}${also.length?` · also moves ${esc(also.join(", "))}`:""}</small>${costLine5(id)}</div>${choiceHTML(id)}</div>`; };
  const secs = S3.sel.map((k,i) => { const ids = leversOf(k).filter(l => ch5().includes(l)).sort((a,b) => { const w = x => (INPUTS[k]||[]).find(y=>y[0]===x)?.[1] || 0; return w(b) - w(a); });
    return `<details class="ks" ${i<2?"open":""}><summary><h2>${esc(ITEMS[k].n)}</h2><div class="vals"><span>Today <b>${esc(fmtV(k,ITEMS[k].t))}</b></span><span>Achievable <b>${esc(fmtV(k,ITEMS[k].r))}</b></span><span>Dream <b>${esc(fmtV(k))}</b></span><span class="now">With your plan <b data-k5v="${k}"></b></span></div></summary>
      ${ids.length ? ids.map(id => row(id, k)).join("") : `<div class="none">No change in the plan moves this one directly.</div>`}</details>`; }).join("");
  mount5(stage, `${simHead("Simulate your plan, KPI by KPI", "Open any of your six to see the changes that move it. Approve each at the achievable or the dream level, or leave it out. The panel on the right and the numbers at the top update as you go.")}
    ${topStrip5()}${bulk5()}<div class="sim5"><div class="kpis5">${secs}</div>${kpiPanel5()}</div>`);
},
update(root){ sync5(root); }
});
