/* ===== Page 3 · Option A · Six seats: six empty seats at the top, every KPI below by department ===== */
const P3_CSS = P2_CSS + `
.lk-web .lev3{border:2px solid var(--w-ink);border-radius:14px;background:var(--w-sheet);padding:12px 16px;margin-bottom:18px}
.lk-web .lev3 h2{margin:0 0 4px;font-size:12px;font-weight:700;letter-spacing:.12em;text-transform:uppercase}
.lk-web .lev3 p{margin:0 0 10px;font-size:13px;color:var(--w-mute)}
.lk-web .lev3 .kinds{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}
.lk-web .lev3 .kind h3{margin:0 0 6px;font-size:11.5px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--w-mute)}
.lk-web .tok{display:inline-flex;align-items:center;gap:5px;margin:0 4px 4px 0;border:1.5px dashed var(--w-line);border-radius:999px;padding:3px 9px;font-size:12px;color:var(--w-mute);background:#fff;min-height:28px}
.lk-web .tok.on{border:1.5px solid var(--w-ink);color:var(--w-ink);background:#FFF7E3}
.lk-web .tok b{display:none;font-size:10.5px;background:var(--w-ink);color:#fff;border-radius:999px;padding:0 6px}
.lk-web .tok.on b{display:inline}
.lk-web .pick3{border:1.5px solid var(--w-ink);background:#fff;border-radius:999px;padding:5px 12px;font-size:12.5px;font-weight:600;min-height:36px;color:var(--w-ink)}
.lk-web .pick3.on{background:var(--w-ink);color:#fff}
.lk-web .pick3:disabled{opacity:.4;cursor:not-allowed}
@media (max-width:900px){.lk-web .lev3 .kinds{grid-template-columns:1fr 1fr}}
@media (max-width:520px){.lk-web .lev3 .kinds{grid-template-columns:1fr}}
`;
function leverTokensHTML(){ const all = CATALOGUE.filter(c => isLever(c) && isShown(c.id));
  return `<section class="lev3" aria-live="polite"><h2>Changes the selected KPIs bring in</h2><p>Every change that affects the selected KPIs, directly or through other numbers. Lit changes go into the simulation on the next page. The number shows how many selected KPIs each one affects.</p>
    <div class="kinds">${["a","k","w","p"].map(k => `<div class="kind"><h3>${KINDNAME[k]}</h3>${all.filter(c=>leverKind(c)===k).map(c=>`<button type="button" class="tok" data-tok="${c.id}" data-ref="it:${c.id}">${esc(c.n)}<b></b></button>`).join("")}</div>`).join("")}</div></section>`; }
function syncTokens(root){ const c = cover3(); root.querySelectorAll("[data-tok]").forEach(t => { const n = c.lev[t.dataset.tok] || 0; t.classList.toggle("on", n>0); t.querySelector("b").textContent = n>1 ? `×${n}` : n ? "✓" : ""; }); }
LOOKS.push({ key:"seats", page:"p3", step:2, letter:"A", name:"Six seats", note:"<b>A · Six seats.</b> Six seats at the top. Every KPI on the page sits below by department, with its target from page 2 and how many changes it would bring into the simulation. Picking a KPI fills a seat and lights the changes it brings in, so you can see the selected KPIs cover the hospital, or lean on one corner of it.",
css: P3_CSS + `
.lk-web .seats{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:10px;margin-bottom:14px}
.lk-web .seat{position:relative;min-height:150px;border:2px dashed var(--w-line);border-radius:14px;background:rgba(251,252,253,.6);padding:12px;display:flex;flex-direction:column;gap:4px}
.lk-web .seat .no{font-family:var(--f-num);font-size:34px;line-height:1;color:#C9D0DA}
.lk-web .seat.full{border:2px solid var(--w-ink);background:var(--w-sheet);box-shadow:6px 6px 0 rgba(22,33,62,.12)}
.lk-web .seat.full .no{color:var(--w-gold)}
.lk-web .seat .g{font-size:10.5px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--w-mute)}
.lk-web .seat .nm b{font-size:14px}
.lk-web .seat small{font-size:11.5px;color:var(--w-mute)}
.lk-web .seat .x{position:absolute;top:8px;right:8px;width:32px;height:32px;border-radius:50%;border:1.5px solid var(--w-line);background:#fff;font-size:16px;line-height:1;color:var(--w-ink)}
.lk-web .seat .empty{margin-top:auto;font-size:12.5px;color:var(--w-mute)}
.lk-web .seat .nd{align-self:flex-start}
.lk-web .acts3{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:16px}
.lk-web .dept{margin-bottom:16px}
.lk-web .dept>h2{display:flex;align-items:baseline;gap:12px;margin:0 0 8px}
.lk-web .dept>h2 span{font-family:var(--f-num);font-weight:400;font-size:28px;line-height:1}
.lk-web .dept>h2 small{font-weight:500;color:var(--w-mute);font-size:13px;text-transform:none;letter-spacing:0}
.lk-web .kc{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:10px}
.lk-web .kcard{border:1.5px solid var(--w-line);border-radius:12px;background:var(--w-sheet);padding:10px 12px;display:flex;flex-direction:column;gap:6px;min-width:0}
.lk-web .kcard.on{border-color:var(--w-ink);box-shadow:4px 4px 0 var(--w-gold)}
.lk-web .kcard small{font-size:12px;color:var(--w-mute)}
.lk-web .kcard .row3{display:flex;justify-content:space-between;align-items:center;gap:8px;margin-top:auto}
.lk-web .kcard .bring{font-size:12px;color:var(--w-ink)}
.lk-web .kcard .bring b{font-family:var(--f-num);font-size:20px;font-weight:400}
.lk-web .kcard .st{font-size:11px;font-weight:700}
.lk-web .kcard .st.short{color:var(--w-none)}
@media (max-width:1100px){.lk-web .seats{grid-template-columns:repeat(3,minmax(0,1fr))}}
@media (max-width:560px){.lk-web .seats{grid-template-columns:repeat(2,minmax(0,1fr))}}
`,
mount(stage){
  const pool = poolIds();
  const card = id => { const it = ITEMS[id], st = addsUp(id);
    return `<div class="kcard" data-kc="${id}">${nameBtn(id)}<small>${hasData(id)?"":`<span class="nd">No data yet</span> `}${esc(kpiLine(id))}</small>${st==="short"?`<span class="st short">Needs more from other targets</span>`:""}
      <div class="row3"><span class="bring">brings in <b>${leversOf(id).length}</b> changes</span><button type="button" class="pick3" data-pick3="${id}" aria-pressed="false">Pick</button></div></div>`; };
  const depts = P3G.map(g => { const ids = pool.filter(id => ITEMS[id].g===g); const G = GROUPS.find(x=>x[0]===g);
    return ids.length ? `<section class="dept"><h2><span>${G[1]}</span><small>${G[2]}</small></h2><div class="kc">${ids.map(card).join("")}</div></section>` : ""; }).join("");
  p3Mount(stage, `${p3Head("Pick six KPIs", "The plan is built around these six. Each one brings in every change that affects it. Picking from different departments gives a fuller plan.")}
    <div class="seats" data-v="seats"></div>
    <div class="acts3"><button type="button" class="act" data-p3="suggest">Let Tojo suggest a balanced six</button><button type="button" class="act ghost" data-p3="clear">Empty the seats</button></div>
    ${leverTokensHTML()}${depts}${p3Cta()}`);
},
update(root){ p3Sync(root); syncTokens(root);
  const box = root.querySelector('[data-v="seats"]'); box.innerHTML = Array.from({length:6}, (_,i) => { const id = S3.sel[i];
    if (!id) return `<div class="seat"><span class="no">${i+1}</span><span class="empty">Empty seat. Pick a KPI below.</span></div>`;
    const it = ITEMS[id]; return `<div class="seat full"><span class="no">${i+1}</span><span class="g">${esc(GNAME[it.g])}</span><span class="nm">${nameBtn(id)}</span><small>${esc(kpiLine(id))}</small>${hasData(id)?"":`<span class="nd">No data yet</span>`}<small>brings in ${leversOf(id).length} changes</small><button type="button" class="x" data-pick3="${id}" data-keep="1" aria-label="Remove ${esc(it.n)}">×</button></div>`; }).join("");
  box.querySelectorAll("[data-pick3]").forEach(b => b.addEventListener("click", e => { e.stopPropagation(); toggle3(b.dataset.pick3); }));
  root.querySelectorAll("[data-kc]").forEach(k => k.classList.toggle("on", S3.sel.includes(k.dataset.kc)));
  root.querySelectorAll(".pick3").forEach(b => b.textContent = b.classList.contains("on") ? "Picked ✓" : "Pick");
}});
