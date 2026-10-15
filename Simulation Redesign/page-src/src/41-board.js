/* ===== Page 2 · Option A · The measuring board: one ruler per target, grouped as outcomes, levers and measures ===== */
LOOKS.push({ key:"board", letter:"A", name:"Measuring board", note:"<b>A · Measuring board.</b> Every target is a ruler: today (a navy tick), Tojo's realistic value in twelve months (a gold diamond), best practice (a green flag) and your pin. Right is always better. Outcomes first, then the levers (people, beds and equipment, ways of working, automations), then the measures by data family. The panel on the right checks each outcome: how much of the gap it asks for, and how much the targets under it back.",
css: P2_CSS + `
.lk-web .bd{display:grid;grid-template-columns:minmax(0,1fr) 320px;gap:24px;align-items:start}
.lk-web .bd-sec{border:2px solid var(--w-ink);border-radius:14px;background:var(--w-sheet);margin-bottom:16px;overflow:hidden}
.lk-web .bd-sec>h2,.lk-web .bd-sec summary{display:flex;align-items:baseline;gap:10px;margin:0;padding:12px 16px;border-bottom:1.5px solid var(--w-line);font-size:12px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--w-ink);background:#F3F5F8}
.lk-web .bd-sec summary{cursor:pointer;list-style:none;min-height:44px;align-items:center}
.lk-web .bd-sec summary::-webkit-details-marker{display:none}
.lk-web .bd-sec summary::before{content:"▸";font-size:14px;transition:transform .2s} .lk-web details[open] summary::before{transform:rotate(90deg)}
.lk-web .bd-sec h2 small,.lk-web .bd-sec summary small{font-weight:500;letter-spacing:0;text-transform:none;color:var(--w-mute);font-size:12.5px}
.lk-web .bd-sub{padding:8px 16px 2px;font-size:11.5px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--w-mute);border-top:1px dashed var(--w-line)}
.lk-web .bd-sub:first-of-type{border-top:0}
.lk-web .row{display:grid;grid-template-columns:minmax(170px,1.15fr) minmax(150px,2fr) 92px 92px;gap:6px 14px;align-items:center;padding:8px 16px;border-top:1px solid #E6EAF0}
.lk-web .row:first-child{border-top:0}
.lk-web .row .nm{min-width:0;display:flex;flex-direction:column;gap:2px}
.lk-web .row .nm small{font-size:11.5px;color:var(--w-mute);display:flex;gap:6px;align-items:center;flex-wrap:wrap}
.lk-web .row .rd{font-family:var(--f-num);font-size:24px;line-height:1;text-align:right;font-variant-numeric:tabular-nums}
.lk-web .row .rd small{display:block;font-family:var(--f-body);font-size:10.5px;color:var(--w-mute)}
.lk-web .row.big .rd{font-size:30px}
.lk-web .row.sw-row{grid-template-columns:minmax(170px,1.15fr) minmax(0,2fr)}
.lk-web .row.sw-row .ctl{display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.lk-web .suite-chip{display:inline-block;width:10px;height:10px;border-radius:3px}
.lk-web .side{position:sticky;top:calc(12px + env(safe-area-inset-top,0px));border:2px solid var(--w-ink);border-radius:14px;background:var(--w-sheet);box-shadow:8px 8px 0 rgba(22,33,62,.12)}
.lk-web .side h2{margin:0;padding:12px 14px;border-bottom:1.5px solid var(--w-line);font-size:12px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--w-ink)}
.lk-web .side ul{list-style:none;margin:0;padding:6px 14px 10px;display:grid;gap:8px}
.lk-web .side li{display:grid;gap:3px}
.lk-web .side li .t{display:flex;justify-content:space-between;gap:8px;font-size:13px}
.lk-web .side .key{display:flex;gap:12px;padding:0 14px 12px;font-size:11.5px;color:var(--w-mute)}
.lk-web .side .key i{display:inline-block;width:14px;height:6px;margin-right:5px;vertical-align:middle}
.lk-web .side .hand{padding:0 14px 12px;font-family:var(--f-hand);font-weight:700;font-size:22px;line-height:1.05;color:var(--w-gold-ink)}
@media (max-width:1100px){.lk-web .bd{grid-template-columns:1fr}.lk-web .side{position:static;order:-1}}
@media (max-width:700px){.lk-web .row{grid-template-columns:minmax(0,1fr) 84px;grid-template-areas:"nm rd" "rl rl" "nu nu"}.lk-web .row .nm{grid-area:nm}.lk-web .row .rl{grid-area:rl}.lk-web .row .rd{grid-area:rd}.lk-web .row>label+input,.lk-web .row .numwrap{grid-area:nu}
  .lk-web .row.sw-row{grid-template-columns:1fr;grid-template-areas:none}}
`,
mount(stage){
  const row = (id, big) => { const it = ITEMS[id];
    if (isSwitch(it)) return `<div class="row sw-row" data-mine="${id}"><div class="nm">${nameBtn(id, it.c?` <span class="suite-chip" style="background:${it.c}"></span>`:"")}<small>${it.k==="auto"?"Virevo automation suite":"Today: "+(it.t?"in place":"not in place")} <span class="mine-dot">· your target</span></small></div><div class="ctl">${controlHTML(id)}</div></div>`;
    return `<div class="row${big?" big":""}" data-mine="${id}"><div class="nm">${nameBtn(id)}<small>${srcMini(id)}Today ${esc(fmtV(id,it.t))} ${esc(unitOf(it))} <span class="mine-dot">· your target</span></small>${glyphsHTML(id)}</div>${rulerHTML(id)}<div class="rd"><span data-tv="${id}"></span><small>${esc(unitOf(it))}</small></div><div class="numwrap">${controlHTML(id)}</div></div>`; };
  const levers = Object.keys(KIND).map(k => `<div class="bd-sub">${KIND[k][0]} · <span style="text-transform:none;letter-spacing:0;font-weight:500">${KIND[k][1]}</span></div>${LEVERS.filter(l=>l.k===k).map(l=>row(l.id)).join("")}`).join("");
  const fams = DOMAINS.map((d,i) => { const ids = d.ms.map(m=>m.id).filter(id=>ITEMS[id]); if (!ids.length) return "";
    return `<details class="bd-sec"${i<1?" open":""}><summary>${esc(d.name)} <small>${ids.length} targets</small></summary>${ids.map(id=>row(id)).join("")}</details>`; }).join("");
  p2Mount(stage, `${p2Head("Set your targets", "Every target already holds Tojo's realistic value for twelve months. Move a pin or type a number only where you want something different; the panel shows whether your outcomes are backed by what sits under them.")}
    <div class="tools"><div class="legend2">${LEGEND2}</div><button type="button" class="act ghost" data-p2="reset" style="margin-left:auto">Reset everything to Tojo's realistic</button></div>
    <div class="bd"><div>
      <section class="bd-sec"><h2>Outcomes <small>the nine KPIs the formula drives</small></h2>${KPIS.map(k=>row(k.id,true)).join("")}</section>
      <section class="bd-sec"><h2>Levers <small>what the hospital can change</small></h2>${levers}</section>
      <h2 class="eb" style="margin:22px 0 8px">Measures, by data family</h2>${fams}
      ${p2CtaHTML()}</div>
      <aside class="side" aria-label="Outcomes, asked and backed"><h2>Asked and backed</h2><div class="key"><span><i style="background:var(--w-ink)"></i>Your target asks</span><span><i style="background:var(--w-yours)"></i>Targets under it back</span></div>
        <ul>${KPIS.map(k=>`<li><div class="t">${nameBtn(k.id)}<span class="abtag" data-abt="${k.id}"></span></div><div class="ab" data-ask-bk="${k.id}"></div></li>`).join("")}</ul>
        <div class="hand" data-v="boardHand"></div></aside></div>`);
},
update(root){ syncTargets(root); syncGlyphs(root);
  root.querySelectorAll("[data-abt]").forEach(e => { const id = e.dataset.abt, t = tension(id); e.textContent = `${pct(fracOf(id))} · ${pct(backed(id))}`; e.classList.toggle("short", t>.15); });
  const c = counts(); const h = root.querySelector('[data-v="boardHand"]'); if (h) h.textContent = c.tens.length ? `red = asks more than it has under it` : `everything is backed`; }
});
