/* ===== Page 6 · Your team · three options for naming the head of each department and who leads each change ===== */
const P6_CSS = P5_CSS + `
.lk-web .pi6{display:grid;grid-template-columns:1fr 1fr;gap:6px}
.lk-web .pi6 label{display:grid;gap:1px;min-width:0} .lk-web .pi6 small{font-size:10.5px;font-weight:600;color:var(--w-mute)}
.lk-web .pi6 input{min-height:36px;padding:4px 8px;border:1.5px solid var(--w-line);border-radius:8px;font-size:13.5px;background:#fff;color:var(--w-ink);min-width:0;width:100%}
.lk-web .pi6 input.bad{border-color:var(--w-none);background:#FFF4F4}
.lk-web .pi6.c input{min-height:32px;font-size:13px}
.lk-web .ds6{font-size:11px;font-weight:700;border-radius:999px;padding:2px 8px;border:1.5px solid currentColor;white-space:nowrap;color:var(--w-none)}
.lk-web .ds6[data-ok="true"]{color:var(--w-yours)}
.lk-web .who6{font-weight:600} .lk-web .who6.none{color:var(--w-mute);font-weight:400;font-style:italic}
.lk-web select{min-height:34px;padding:4px 8px;border:1.5px solid var(--w-ink);border-radius:8px;background:#fff;color:var(--w-ink);font-size:13px;max-width:100%}
.lk-web .cf6{display:flex;flex-wrap:wrap;align-items:center;gap:10px;border:2px solid var(--w-yours);background:#F1F8F3;border-radius:14px;padding:12px 16px;margin:0 0 14px;font-size:14px}
.lk-web .cf6[hidden]{display:none} .lk-web .cf6 b{color:var(--w-yours)} .lk-web .cf6 .go{margin-left:auto;min-height:44px;padding:8px 18px}
.lk-web .pi6.t3{grid-template-columns:1fr 1fr 1fr}
@media (max-width:560px){.lk-web .pi6.t3{grid-template-columns:1fr}}
.lk-web .tf6{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:10px 16px;align-items:center;border:2px dashed var(--w-ink);border-radius:14px;background:var(--w-sheet);padding:12px 16px;margin:0 0 14px}
.lk-web .tf6.over{background:#FFF7E3;border-color:var(--w-gold-ink)}
.lk-web .tf6 h2{margin:0 0 2px;font-family:var(--f-num);font-weight:400;font-size:22px;line-height:1}
.lk-web .tf6 p{margin:0;font-size:13px;color:var(--w-mute)}
.lk-web .tf6-b{display:flex;flex-wrap:wrap;gap:8px;justify-content:flex-end}
.lk-web .tf6-up{position:relative;display:inline-flex;align-items:center;cursor:pointer;min-height:44px;padding:8px 16px}
.lk-web .tf6-up input{position:absolute;inset:0;width:100%;height:100%;opacity:0;cursor:pointer}
.lk-web .tf6-up:focus-within{outline:3px solid var(--w-gold);outline-offset:2px}
.lk-web .tf6-r{grid-column:1/-1;font-size:13px}
.lk-web .tf6-r:empty{display:none}
.lk-web .tf6-r p{color:var(--w-ink);margin:0 0 6px}
.lk-web .un6{list-style:none;margin:0;padding:0;display:grid;gap:6px}
.lk-web .un6 li{display:flex;flex-wrap:wrap;gap:8px;align-items:center;justify-content:space-between;border:1px solid var(--w-line);border-radius:10px;padding:6px 10px;background:#fff}
.lk-web .nd6 .n{display:grid} .lk-web .nd6 .tt6{font-size:11px;font-weight:400;color:var(--w-mute)} .lk-web .nd6 .tt6:empty{display:none}
@media (max-width:760px){.lk-web .tf6{grid-template-columns:1fr}.lk-web .tf6-b{justify-content:flex-start}}
.lk-web .kpo6{list-style:none;margin:0;padding:6px 16px 12px;display:grid;gap:8px}
.lk-web .kpo6 li{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,240px) minmax(0,160px);gap:10px;align-items:center;font-size:13.5px}
@media (max-width:700px){.lk-web .kpo6 li{grid-template-columns:1fr}}
`;
function kpiOwners6(d){ return `<section class="box5" style="margin-top:16px"><h2>Who owns each KPI<small>one owner each</small></h2><ul class="kpo6">${d.kpis.map(x => `<li>${nameBtn(x.k)}<select data-kown="${x.k}" aria-label="Owner of ${esc(x.n)}">${DEPT_ORDER.map(k => `<option value="${k}">${esc(DEPTS[k][0])}</option>`).join("")}</select><span class="who6" data-who="${kpiOwner(x.k)}"></span></li>`).join("")}</ul></section>`; }
const AREAS6 = ["Leadership","Clinical","Operations","Business"];

/* A · Department cards */
LOOKS.push({ key:"p6cards", page:"p6", step:5, letter:"A", name:"Department cards", note:"<b>A · Department cards.</b> One card for each department your plan needs, grouped as leadership, clinical, operations and business. Each card takes the head's name and mobile, and lists the changes they lead, the ones they help with, the KPIs they own and the months they are busy. The owner can be copied into every empty card.",
css: P6_CSS + `
.lk-web .ar6>h2{font-family:var(--f-num);font-weight:400;font-size:24px;margin:18px 0 8px}
.lk-web .cards6{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:12px}
.lk-web .dc6{border:2px solid var(--w-ink);border-radius:14px;background:var(--w-sheet);padding:12px 14px;display:grid;gap:8px;align-content:start;min-width:0}
.lk-web .dc6-h{display:flex;justify-content:space-between;gap:8px;align-items:baseline}
.lk-web .dc6-h .linkbtn b{font-size:15px}
.lk-web .dc6 ul{list-style:none;margin:0;padding:0;display:grid;gap:3px;font-size:12.5px}
.lk-web .dc6 h4{margin:4px 0 2px;font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--w-mute)}
.lk-web .dc6 li{display:flex;justify-content:space-between;gap:8px} .lk-web .dc6 li em{font-style:normal;color:var(--w-mute);white-space:nowrap}
.lk-web .dc6 .hp{color:var(--w-mute)}
.lk-web .mt6{position:relative;height:8px;border-radius:4px;background:#E6EAF0;margin-top:2px}
.lk-web .mt6 i{position:absolute;top:0;bottom:0;border-radius:4px;background:var(--w-yours)}
.lk-web .mt6l{display:flex;justify-content:space-between;font-size:11px;color:var(--w-mute)}
.lk-web .dc6 .kp{display:flex;flex-wrap:wrap;gap:4px} .lk-web .dc6 .kp span{font-size:11.5px;font-weight:600;border-radius:999px;padding:2px 8px;background:#FFF7E3;border:1px solid var(--w-gold)}
`,
mount(stage){ const d = SIMR.frozen ? p6Data() : null; if (!d) return p6Mount(stage, "");
  const card = x => `<article class="dc6"><div class="dc6-h"><button type="button" class="linkbtn" data-ref="dept:${x.k}"><b>${esc(x.role)}</b></button><span class="ds6" data-dstate="${x.k}"></span></div>
    ${personInputs(x.k)}
    ${x.kpis.length ? `<div class="kp">${x.kpis.map(y => `<span>Owns ${esc(y.n)}</span>`).join("")}</div>` : ""}
    ${x.leads.length ? `<div><h4>Leads ${x.leads.length}</h4><ul>${x.leads.map(c => `<li><span>${esc(c.n)}</span><em>month ${c.start}–${c.full}</em></li>`).join("")}</ul></div>` : ""}
    ${x.helps.length ? `<div><h4>Helps with ${x.helps.length}</h4><ul class="hp">${x.helps.map(c => `<li><span>${esc(c.n)}</span><em>${esc(DEPTS[leadOf(c.id)][0].split(" ")[0])} leads</em></li>`).join("")}</ul></div>` : ""}
    ${x.from ? `<div><div class="mt6l"><span>Busy month ${x.from}–${x.to}</span><span>of ${d.s.D}</span></div><div class="mt6"><i style="left:${(x.from-1)/d.s.D*100}%;width:${Math.max(4,(Math.min(x.to,d.s.D)-x.from+1)/d.s.D*100)}%"></i></div></div>` : `<small class="cl">Signs off the budget and gets the daily summary.</small>`}</article>`;
  p6Mount(stage, `${p6Head("Your team", "Add the head of each department this plan needs: a name and a mobile number. Tojo sends each of them their own tasks every morning.")}
    ${p6Tiles(d)}${p6Done()}${p6Actions()}
    ${AREAS6.map(a => { const xs = d.depts.filter(x => x.area === a); return xs.length ? `<section class="ar6"><h2>${a}</h2><div class="cards6">${xs.map(card).join("")}</div></section>` : ""; }).join("")}
    ${kpiOwners6(d)}`); },
update(root){ sync6(root); }
});

/* B · Change by change */
LOOKS.push({ key:"p6list", page:"p6", step:5, letter:"B", name:"Change by change", note:"<b>B · Change by change.</b> The same layout as Simulate. On the left, every approved change with its lead (which you can move to another department) and its helpers, named as soon as you add them. On the right, frozen while you scroll, the team: each department head's name and mobile, and how many changes they lead.",
css: P6_CSS + `
.lk-web .grp5{border:2px solid var(--w-ink);border-radius:14px;background:var(--w-sheet);margin-bottom:14px;overflow:hidden}
.lk-web .grp5>h2{margin:0;padding:10px 16px;border-bottom:1.5px solid var(--w-line);background:#F3F5F8;font-family:var(--f-num);font-weight:400;font-size:24px;line-height:1}
.lk-web .grp5>h2 small{font-family:var(--f-body);font-size:12.5px;color:var(--w-mute);margin-left:8px}
.lk-web .cr6{display:grid;grid-template-columns:minmax(0,1.2fr) minmax(0,1fr) minmax(0,1.1fr);gap:8px 14px;align-items:center;padding:10px 16px;border-top:1px solid #E6EAF0}
.lk-web .grp5>h2+.cr6{border-top:0}
.lk-web .cr6 .nm small{display:block;font-size:11.5px;color:var(--w-mute)}
.lk-web .cr6 .ld{display:grid;gap:3px} .lk-web .cr6 .ld small{font-size:10.5px;font-weight:600;color:var(--w-mute)}
.lk-web .cr6 .hl6{display:flex;flex-wrap:wrap;gap:4px;font-size:12px}
.lk-web .cr6 .hl6 span{border:1px solid var(--w-line);border-radius:999px;padding:2px 8px;background:#fff}
.lk-web .tm6{position:sticky;top:12px;max-height:calc(100vh - 24px);overflow:auto;border:2px solid var(--w-ink);border-radius:16px;background:var(--w-sheet);box-shadow:8px 8px 0 rgba(22,33,62,.12)}
.lk-web .tm6>h2{margin:0;padding:12px 14px 8px;font-family:var(--f-num);font-weight:400;font-size:26px;border-bottom:1.5px solid var(--w-line);position:sticky;top:0;background:var(--w-sheet);z-index:2}
.lk-web .tm6 ul{list-style:none;margin:0;padding:4px 14px 10px}
.lk-web .tm6 li{padding:10px 0;border-bottom:1px solid #E6EAF0;display:grid;gap:6px}
.lk-web .tm6 .th{display:flex;justify-content:space-between;gap:8px;align-items:baseline;font-size:13px}
.lk-web .tm6 .th small{color:var(--w-mute)}
.lk-web .sim6{display:grid;grid-template-columns:minmax(0,1fr) 380px;gap:20px;align-items:start}
@media (max-width:1100px){.lk-web .cr6{grid-template-columns:1fr 1fr}.lk-web .cr6 .nm{grid-column:1/-1}}
@media (max-width:1000px){.lk-web .sim6{grid-template-columns:1fr}.lk-web .tm6{position:static;max-height:none}}
@media (max-width:600px){.lk-web .cr6{grid-template-columns:1fr}}
`,
mount(stage){ const d = SIMR.frozen ? p6Data() : null; if (!d) return p6Mount(stage, "");
  const row = c => `<div class="cr6"><div class="nm">${nameBtn(c.id)}<small>month ${c.start}–${c.full} · ${c.tot ? money(L_(c.tot)) : "no cost"}</small></div>
    <div class="ld" data-noopen><small>Lead</small>${leadSelect(c.id)}<span class="who6" data-who="${leadOf(c.id)}"></span></div>
    <div class="ld"><small>Helps</small><div class="hl6">${helpersOf(c.id).map(h => `<span>${esc(DEPTS[h][0])}: <b class="who6" data-who="${h}"></b></span>`).join("") || "<span>No helpers</span>"}</div></div></div>`;
  const groups = ["a","k","w","p"].map(k => { const xs = d.changes.filter(c => c.kind === k); return xs.length ? `<section class="grp5"><h2>${KINDNAME[k]}<small>${xs.length}</small></h2>${xs.map(row).join("")}</section>` : ""; }).join("");
  const panel = `<aside class="tm6" aria-label="Your team"><h2>Your team</h2><ul>${d.depts.map(x => `<li><div class="th"><button type="button" class="linkbtn" data-ref="dept:${x.k}"><b>${esc(x.role)}</b></button><span class="ds6" data-dstate="${x.k}"></span></div>
    ${personInputs(x.k, true)}<small class="cl">Leads ${x.leads.length} · helps with ${x.helps.length}${x.kpis.length ? ` · owns ${x.kpis.length} KPI${x.kpis.length>1?"s":""}` : ""}</small></li>`).join("")}</ul></aside>`;
  p6Mount(stage, `${p6Head("Who leads each change", "Each approved change has one lead department and some helpers. Add each head's name and mobile on the right; move a lead if another department should own it.")}
    ${p6Tiles(d)}${p6Done()}${p6Actions()}<div class="sim6"><div>${groups}${kpiOwners6(d)}</div>${panel}</div>`); },
update(root){ sync6(root); }
});

/* C · Team chart */
LOOKS.push({ key:"p6org", page:"p6", step:5, letter:"C", name:"Team chart", note:"<b>C · Team chart (approved 14 Oct, with file upload).</b> The owner at the top, then the heads in three columns (clinical, operations, business). Click a person to add their name, designation and mobile. Or fill everyone at once: download the CSV or Excel template, fill it in, and upload it (or drop it on the box); each row is matched to a department, and rows that do not match can be placed by hand.",
css: P6_CSS + `
.lk-web .org6{border:2px solid var(--w-ink);border-radius:16px;background:var(--w-sheet);padding:18px 16px}
.lk-web .top6{display:flex;justify-content:center;position:relative;padding-bottom:22px}
.lk-web .top6::after{content:"";position:absolute;left:50%;bottom:0;height:22px;border-left:2px solid var(--w-line)}
.lk-web .cols6{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;border-top:2px solid var(--w-line);padding-top:18px;position:relative}
.lk-web .col6>h3{margin:0 0 8px;text-align:center;font-size:11.5px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--w-mute)}
.lk-web .col6{display:grid;gap:8px;align-content:start}
.lk-web .nd6{display:grid;grid-template-columns:44px minmax(0,1fr);gap:4px 10px;align-items:center;text-align:left;border:2px solid var(--w-ink);border-radius:14px;background:#fff;padding:8px 10px;color:var(--w-ink);width:100%;min-height:64px}
.lk-web .nd6[aria-pressed="true"]{background:#FFF7E3;border-color:var(--w-gold-ink);box-shadow:4px 4px 0 rgba(107,79,22,.25)}
.lk-web .nd6 .av{grid-row:span 2;width:44px;height:44px;border-radius:50%;display:grid;place-items:center;background:var(--w-ink);color:#fff;font-family:var(--f-num);font-size:20px}
.lk-web .nd6 .av.none{background:#E6EAF0;color:var(--w-mute);border:2px dashed var(--w-line)}
.lk-web .nd6 .r{font-size:12px;color:var(--w-mute)} .lk-web .nd6 .n{font-weight:700;font-size:14px}
.lk-web .nd6 .c{grid-column:2;font-size:11.5px;color:var(--w-mute)} .lk-web .nd6 .c b{color:var(--w-yours)} .lk-web .nd6 .c i{font-style:normal;color:var(--w-gold-ink);font-weight:600}
.lk-web .top6 .nd6{max-width:340px}
.lk-web .ed6{border:2px solid var(--w-ink);border-radius:16px;background:var(--w-sheet);padding:14px 16px;margin-top:14px;display:grid;grid-template-columns:minmax(0,340px) minmax(0,1fr);gap:16px}
.lk-web .ed6 h2{margin:0 0 8px;font-family:var(--f-num);font-weight:400;font-size:26px;line-height:1}
.lk-web .ed6 ul{list-style:none;margin:0;padding:0;display:grid;gap:3px;font-size:13px}
.lk-web .ed6 li{display:flex;justify-content:space-between;gap:8px} .lk-web .ed6 li em{font-style:normal;color:var(--w-mute);white-space:nowrap}
.lk-web .ed6 h4{margin:6px 0 2px;font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--w-mute)}
@media (max-width:900px){.lk-web .cols6{grid-template-columns:1fr}.lk-web .ed6{grid-template-columns:1fr}}
`,
mount(stage){ const d = SIMR.frozen ? p6Data() : null; if (!d) return p6Mount(stage, "");
  if (!P6C.sel || !d.depts.find(x => x.k === P6C.sel)) P6C.sel = "owner";
  const node = x => `<button type="button" class="nd6" data-nd="${x.k}" aria-pressed="${P6C.sel===x.k}"><span class="av" data-av="${x.k}"></span><span class="r">${esc(x.role)}</span><span class="n"><span class="who6 n" data-who="${x.k}"></span><small class="tt6" data-tt="${x.k}"></small></span>
    <span class="c">${x.leads.length ? `leads <b>${x.leads.length}</b>` : ""}${x.leads.length && x.helps.length ? " · " : ""}${x.helps.length ? `helps ${x.helps.length}` : ""}${x.kpis.length ? ` · <i>owns ${x.kpis.length} KPI${x.kpis.length>1?"s":""}</i>` : ""}${!x.leads.length && !x.helps.length && !x.kpis.length ? "signs off the budget" : ""}</span></button>`;
  const sel = d.depts.find(x => x.k === P6C.sel);
  p6Mount(stage, `${p6Head("Your team", "Everyone this plan needs, from the owner down. Click a person to add their name, designation and mobile, or fill everyone at once from a file.")}
    ${p6Tiles(d)}${p6Done()}${p6Actions()}${teamFileHTML6()}
    <section class="org6" aria-label="Team chart"><div class="top6">${node(d.depts.find(x => x.k === "owner"))}</div>
      <div class="cols6">${["Clinical","Operations","Business"].map(a => `<div class="col6"><h3>${a}</h3>${d.depts.filter(x => x.area === a).map(node).join("") || `<small class="cl" style="text-align:center">No one needed</small>`}</div>`).join("")}</div></section>
    <section class="ed6" aria-label="Selected person"><div><h2>${esc(sel.role)}</h2><span class="ds6" data-dstate="${sel.k}"></span><div style="margin-top:8px">${personInputs(sel.k, false, true)}</div></div>
      <div>${sel.leads.length ? `<h4>Leads ${sel.leads.length}</h4><ul>${sel.leads.map(c => `<li><span>${nameBtn(c.id)}</span><em>month ${c.start}–${c.full}</em></li>`).join("")}</ul>` : ""}
      ${sel.helps.length ? `<h4>Helps with ${sel.helps.length}</h4><ul>${sel.helps.map(c => `<li><span>${esc(c.n)}</span><em>${esc(DEPTS[leadOf(c.id)][0])} leads</em></li>`).join("")}</ul>` : ""}
      ${sel.kpis.length ? `<h4>Owns</h4><ul>${sel.kpis.map(y => `<li><span>${esc(y.n)}</span></li>`).join("")}</ul>` : ""}
      ${!sel.leads.length && !sel.helps.length ? `<p class="cl">Signs off the budget and gets one daily summary across every department.</p>` : ""}</div></section>
    ${kpiOwners6(d)}`);
  wireTeamFile6(stage);
  stage.querySelectorAll("[data-nd]").forEach(b => b.addEventListener("click", () => { P6C.sel = b.dataset.nd; mountLook(LOOKS.indexOf(CUR)); const f = document.querySelector('.ed6 [data-pn]'); if (f) f.focus({preventScroll:false}); })); },
update(root){ sync6(root); syncTeamFile6(root); root.querySelectorAll("[data-tt]").forEach(e => e.textContent = titleOf(e.dataset.tt)); root.querySelectorAll("[data-av]").forEach(e => { const k = e.dataset.av, n = (personOf(k).name || "").trim(); e.textContent = n ? n.split(/\s+/).filter(w => !/^dr\.?$/i.test(w)).slice(0,2).map(w => w[0]).join("").toUpperCase() : "?"; e.classList.toggle("none", !n); }); }
});
const P6C = { sel: "owner" };
