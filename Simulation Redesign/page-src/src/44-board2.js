/* ===== Page 2 · Measuring board (revised 13 Oct): by department, data-driven, plain English ===== */
const subOf = it => it.g!=="up" ? "" : it.x==="a" ? "a" : (it.x==="k" || it.id==="ct" || it.id==="mri") ? "k" : "w";
function glyphsHTML(id){ const it = ITEMS[id]; if (!(it.x==="p" || it.x==="k")) return ""; return `<span class="glyphs ${it.x==="k"?"kit":""}" data-gl="${id}" aria-hidden="true"></span>`; }
function syncGlyphs(root){ root.querySelectorAll("[data-gl]").forEach(g => { const it = ITEMS[g.dataset.gl], v = valOf(g.dataset.gl); const base = Math.round(it.t), tgt = Math.round(v), n = Math.min(40, Math.max(base,tgt));
  let h = ""; for (let i=0;i<n;i++) h += `<i class="${i<Math.min(base,tgt)?"":i<tgt?"add":"cut"}"></i>`; g.innerHTML = h; }); }
function controlHTML(id){ const it = ITEMS[id];
  if (isSwitch(it)) return `<button type="button" class="sw" data-sw="${id}" aria-pressed="false">No</button>${it.x==="a"?`<label class="sr-only" for="go-${id}">Go-live month</label><select class="gomo" id="go-${id}" data-go="${id}">${Array.from({length:12},(_,i)=>`<option value="${i+1}" ${TS.go[id]===i+1?"selected":""}>Live in month ${i+1}</option>`).join("")}</select>`:""}`;
  return `<label class="sr-only" for="n-${id}">Type a target for ${esc(it.n)}</label><input class="num" id="n-${id}" type="number" step="${stepOf(it)}" data-num="${id}" inputmode="decimal">`; }
LOOKS.push({ key:"board2", page:"p2", step:1, letter:"2", name:"Measuring board, revised", note:"<b>Measuring board, revised (13 Oct).</b> Grouped by department: Financial first, then Operational, Clinical, Marketing, Administrative (staffing) and Process upgrades. What appears depends on the hospital's files: parameters we assess everywhere always show, marked <b>No data yet</b> when the files are missing; others show only when the files contain them. Try the review buttons above to see the page change with the data.",
css: P2_CSS + `
.lk-web .p2head h1{max-width:14ch}
.lk-web .shown{display:flex;flex-wrap:wrap;align-items:center;gap:6px 14px;margin:0 0 12px;padding:10px 14px;border:1.5px dashed var(--w-ink);border-radius:12px;background:var(--w-sheet);font-size:13.5px}
.lk-web .shown b{font-family:var(--f-num);font-weight:400;font-size:22px;vertical-align:-2px}
.lk-web .shown button{margin-left:auto;border:1.5px solid var(--w-ink);background:#fff;border-radius:999px;padding:4px 12px;font-size:12.5px;font-weight:600;min-height:36px;color:var(--w-ink)}
.lk-web .lg-nd{width:2px;height:14px;border-left:2px dashed var(--w-ref)}
.lk-web .rl.nodata .rl-t{background:none;border-left:2px dashed var(--w-ref);width:0}
.lk-web .rl.nodata .rl-gap{background:repeating-linear-gradient(90deg,#E4DDF3 0 6px,transparent 6px 10px)}
.lk-web .bd{display:grid;grid-template-columns:minmax(0,1fr) 360px;gap:24px;align-items:start}
.lk-web .bd-sec{border:2px solid var(--w-ink);border-radius:14px;background:var(--w-sheet);margin-bottom:16px;overflow:hidden}
.lk-web .bd-sec>h2{display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 12px;margin:0;padding:12px 16px;border-bottom:1.5px solid var(--w-line);background:#F3F5F8}
.lk-web .bd-sec>h2 span{font-family:var(--f-num);font-weight:400;font-size:28px;line-height:1;letter-spacing:.01em;color:var(--w-ink)}
.lk-web .bd-sec>h2 small,.lk-web .bd-sec>h2 em{text-transform:none;letter-spacing:0}
.lk-web .bd-sec>h2 small{font-weight:500;color:var(--w-mute);font-size:13px}
.lk-web .bd-sec>h2 em{margin-left:auto;font-style:normal;font-size:12px;color:var(--w-mute)}
.lk-web .bd-sub{padding:10px 16px 2px;font-size:11.5px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--w-mute);border-top:1px dashed var(--w-line)}
.lk-web .bd-sec>h2+.bd-sub{border-top:0}
.lk-web .row{display:grid;grid-template-columns:minmax(190px,1.2fr) minmax(150px,2fr) 100px 92px;gap:6px 14px;align-items:center;padding:9px 16px;border-top:1px solid #E6EAF0}
.lk-web .row .nm{min-width:0;display:flex;flex-direction:column;gap:3px}
.lk-web .row .nm small{font-size:11.5px;color:var(--w-mute);display:flex;gap:6px;align-items:center;flex-wrap:wrap}
.lk-web .nd{font-size:10.5px;font-weight:700;color:var(--w-none);border:1.5px dotted var(--w-none);border-radius:999px;padding:0 7px;white-space:nowrap}
.lk-web .row .rd{font-family:var(--f-num);font-size:24px;line-height:1;text-align:right;font-variant-numeric:tabular-nums}
.lk-web .row .rd small{display:block;font-family:var(--f-body);font-size:10.5px;color:var(--w-mute);line-height:1.25}
.lk-web .row .rd .warn{color:var(--w-none);font-weight:600}
.lk-web .row .rd .more{color:var(--w-yours);font-weight:600}
.lk-web .bd-sec.fin .row .rd{font-size:30px}
.lk-web .row.sw-row{grid-template-columns:minmax(190px,1.2fr) minmax(0,2fr)}
.lk-web .row.sw-row .ctl{display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.lk-web .suite-chip{display:inline-block;width:10px;height:10px;border-radius:3px}
.lk-web .side{position:sticky;top:calc(12px + env(safe-area-inset-top,0px));border:2px solid var(--w-ink);border-radius:14px;background:var(--w-sheet);box-shadow:8px 8px 0 rgba(22,33,62,.12);max-height:calc(100vh - 24px);overflow:auto}
.lk-web .side h2{margin:0;padding:14px 16px 4px;font-family:var(--f-num);font-weight:400;font-size:28px;line-height:1}
.lk-web .side .intro{margin:0;padding:0 16px 10px;font-size:13px;color:var(--w-mute)}
.lk-web .side .key{display:grid;gap:4px;margin:0 16px 8px;padding:8px 10px;border-radius:10px;background:#F1F4F8;font-size:12.5px}
.lk-web .side .key span{display:flex;align-items:center;gap:8px}
.lk-web .k-today{width:10px;height:10px;border-radius:50%;background:#9AA5B8}
.lk-web .k-tgt{width:0;height:0;border-left:7px solid transparent;border-right:7px solid transparent;border-top:11px solid var(--w-ink)}
.lk-web .k-lik{width:12px;height:12px;border-radius:50%;border:3px solid var(--w-yours);background:#fff}
.lk-web .k-gap{width:18px;height:6px;border-radius:3px;background:var(--w-none);opacity:.55}
.lk-web .side ul{list-style:none;margin:0;padding:0 16px 14px;display:grid;gap:12px}
.lk-web .au{border-top:1px solid #E6EAF0;padding-top:10px}
.lk-web .au .hd{display:flex;justify-content:space-between;gap:8px;align-items:baseline}
.lk-web .au .hd .w{font-size:11.5px;font-weight:700}
.lk-web .au[data-st="short"] .w{color:var(--w-none)} .lk-web .au[data-st="ok"] .w{color:var(--w-yours)} .lk-web .au[data-st="room"] .w{color:var(--w-yours)}
.lk-web .line{position:relative;height:30px;margin:6px 4px 0}
.lk-web .line .tr{position:absolute;left:0;right:0;top:15px;height:4px;border-radius:2px;background:#DCE2EA}
.lk-web .line .seg{position:absolute;top:13px;height:8px;border-radius:4px;left:min(var(--y),var(--l));width:calc(max(var(--y),var(--l)) - min(var(--y),var(--l)));background:var(--w-none);opacity:.5}
.lk-web .au[data-st="room"] .line .seg{background:var(--w-yours);opacity:.35} .lk-web .au[data-st="ok"] .line .seg{opacity:0}
.lk-web .line .td{position:absolute;left:var(--z);top:12px;width:10px;height:10px;margin-left:-5px;border-radius:50%;background:#9AA5B8}
.lk-web .line .yt{position:absolute;left:var(--y);top:1px;margin-left:-7px;width:0;height:0;border-left:7px solid transparent;border-right:7px solid transparent;border-top:12px solid var(--w-ink)}
.lk-web .line .lk{position:absolute;left:var(--l);top:10px;width:14px;height:14px;margin-left:-7px;border-radius:50%;border:3px solid var(--w-yours);background:#fff}
.lk-web .line .be{position:absolute;right:0;top:4px;font-size:10px;color:var(--w-mute)}
.lk-web .au .nums{display:flex;flex-wrap:wrap;gap:2px 12px;font-size:12.5px;color:var(--w-mute)}
.lk-web .au .nums b{color:var(--w-ink)}
.lk-web .au .help{display:flex;flex-wrap:wrap;gap:4px;margin-top:5px;align-items:center;font-size:12px;color:var(--w-mute)}
.lk-web .au .help button{border:1.5px solid var(--w-line);background:#fff;border-radius:999px;padding:2px 9px;font-size:12px;font-weight:600;color:var(--w-ink);min-height:30px}
.lk-web .au .fillb{margin-top:6px;border:1.5px solid var(--w-ink);background:var(--w-gold);border-radius:8px;padding:5px 10px;font-size:12.5px;font-weight:600;min-height:36px;color:var(--w-ink)}
@media (max-width:1150px){.lk-web .bd{grid-template-columns:1fr}.lk-web .side{position:static;max-height:none}}
@media (max-width:700px){.lk-web .row{grid-template-columns:minmax(0,1fr) 96px;grid-template-areas:"nm rd" "rl rl" "nu nu"}.lk-web .row .nm{grid-area:nm}.lk-web .row .rl{grid-area:rl}.lk-web .row .rd{grid-area:rd}.lk-web .row .numwrap{grid-area:nu}
  .lk-web .row.sw-row{grid-template-columns:1fr;grid-template-areas:none}.lk-web .shown button{margin-left:0}}
`,
mount(stage){
  const row = id => { const it = ITEMS[id], has = hasData(id);
    const today = has ? `${it.x==="a"?"Not running today":`Today ${esc(withU(id, it.t))}`}` : `<span class="nd">No data yet</span> typical ${esc(withU(id, it.t))}`;
    if (isSwitch(it)) return `<div class="row sw-row" data-mine="${id}"><div class="nm">${nameBtn(id, it.c?` <span class="suite-chip" style="background:${it.c}"></span>`:"")}<small>${it.x==="a"?"Virevo automation suite":`Today: ${it.t?"yes":"no"}`} <span class="mine-dot">· your target</span></small></div><div class="ctl">${controlHTML(id)}</div></div>`;
    return `<div class="row" data-mine="${id}"><div class="nm">${nameBtn(id)}<small>${today} <span class="mine-dot">· your target</span></small>${glyphsHTML(id)}</div>${rulerHTML(id)}<div class="rd"><span data-tv="${id}"></span><small>${esc(unitOf(it))}</small><small data-rw="${id}"></small></div><div class="numwrap">${controlHTML(id)}</div></div>`; };
  const sec = ([g, name, sub]) => { const ids = shownIds(g); if (!ids.length) return ""; const nd = ids.filter(id=>!hasData(id)).length;
    let body;
    if (g==="up") body = ["a","k","w"].map(s => { const sids = ids.filter(id => subOf(ITEMS[id])===s); return sids.length ? `<div class="bd-sub">${UPSUB[s]}</div>${sids.map(row).join("")}` : ""; }).join("");
    else if (g==="adm") { const m = ids.filter(id=>ITEMS[id].x!=="p"), p = ids.filter(id=>ITEMS[id].x==="p"); body = `${m.map(row).join("")}${p.length?`<div class="bd-sub">Staff numbers</div>${p.map(row).join("")}`:""}`; }
    else body = ids.map(row).join("");
    return `<section class="bd-sec ${g}"><h2><span>${name}</span><small>${sub}</small><em>${ids.length} parameters${nd?` · ${nd} with no data yet`:""}</em></h2>${body}</section>`; };
  const c = counts();
  p2Mount(stage, `<div class="p2head"><div><div class="eb">Simulation · step 2 of 8 · ${esc(HOSPITAL.name)}, ${HOSPITAL.beds} beds</div><h1>Set your targets</h1><p class="lede">Every target starts at the realistic value for twelve months. Change only what you want to. On the right, see whether your financial targets can be reached with the other targets you have set.</p></div>
      <div class="pulse" role="group" aria-label="Readings">
        <button type="button" class="pz" data-ref="p2:set"><span class="pl">Targets you set</span><b data-v="p2set"></b><small>the rest stay at the realistic value</small></button>
        <button type="button" class="pz" data-ref="p2:short"><span class="pl">Financial targets</span><b data-v="p2short"></b><small data-v="p2shortSub"></small></button>
        <button type="button" class="pz" data-ref="p2:nodata"><span class="pl">No data yet</span><b data-v="p2nd"></b><small>targets can still be set</small></button>
        <button type="button" class="pz" data-ref="p2:shown"><span class="pl">On this page</span><b data-v="p2shown"></b><small data-v="p2shownSub"></small></button></div></div>
    <div class="shown"><span>Showing <b>${c.all}</b> parameters: <b>${c.all-c.extraShown}</b> we check in every hospital, and <b>${c.extraShown}</b> more found in your files.${c.nodata.length?` <b>${c.nodata.length}</b> have no data yet; they start from typical values and can still take a target.`:""}</span><button type="button" data-ref="p2:shown">What decides this</button></div>
    <div class="tools"><div class="legend2"><span><i class="lg-t"></i>Today</span><span><i class="lg-nd"></i>Typical start, no data yet</span><span><i class="lg-r"></i>Realistic in 12 months</span><span><i class="lg-b"></i>Best practice</span><span><i class="lg-y"></i>Your target (drag it)</span></div><button type="button" class="act ghost" data-p2="reset" style="margin-left:auto">Put every target back to realistic</button></div>
    <div class="bd"><div>${GROUPS.map(sec).join("")}${p2CtaHTML2()}</div>
      <aside class="side" aria-label="Will your targets add up?"><h2>Will your targets add up?</h2>
        <p class="intro">For each financial target, we check whether the targets you have set elsewhere on this page are enough to get there. Move any pin and this updates.</p>
        <div class="key"><span><i class="k-today"></i>Where you are today</span><span><i class="k-tgt"></i>The target you set</span><span><i class="k-lik"></i>Where your other targets would take it</span><span><i class="k-gap"></i>The gap between the two</span></div>
        <ul>${shownIds("fin").map(id => `<li class="au" data-au="${id}"><div class="hd">${nameBtn(id)}<span class="w" data-auw="${id}"></span></div>
          <div class="line"><i class="tr"></i><i class="seg"></i><i class="td"></i><i class="yt"></i><i class="lk"></i><span class="be">best ${esc(fmtV(id, ITEMS[id].b))}</span></div>
          <div class="nums"><span>Today <b>${esc(withU(id, ITEMS[id].t))}</b></span><span>Target <b data-aut="${id}"></b></span><span>Likely <b data-aul="${id}"></b></span></div>
          <div class="help" data-auh="${id}"></div><div data-auf="${id}"></div></li>`).join("")}</ul></aside></div>`);
},
update(root){ syncTargets(root); syncGlyphs(root);
  const c = counts(); const set = (k,v) => root.querySelectorAll(`[data-v="${k}"]`).forEach(e => e.innerHTML = v);
  set("p2set", `${c.set}<i>/${c.all}</i>`); set("p2short", `${c.fin.length - c.short.length}<i>/${c.fin.length}</i>`); set("p2shortSub", c.short.length ? `can be reached; ${c.short.length} need more` : "can all be reached");
  set("p2nd", `${c.nodata.length}`); set("p2shown", `${c.all}<i>/${c.cat}</i>`); set("p2shownSub", `${c.hidden.length} more appear with more files`);
  set("ctaNote2", c.short.length ? `${c.short.length} financial target${c.short.length>1?"s need":" needs"} more from your other targets. You can still go on; the simulation will show what is likely.` : "Your other targets are enough to reach every financial target.");
  root.querySelectorAll("[data-rw]").forEach(e => { const st = addsUp(e.dataset.rw); e.innerHTML = st==="short" ? `<span class="warn">needs more</span>` : st==="room" ? `<span class="more">could go further</span>` : ""; });
  const pos = f => (4 + Math.max(0, Math.min(1.08, f))*86).toFixed(1) + "%";
  root.querySelectorAll("[data-au]").forEach(li => { const id = li.dataset.au, st = addsUp(id) || "ok", L = likelyOf(id);
    li.dataset.st = st; const ln = li.querySelector(".line"); ln.style.setProperty("--z", pos(0)); ln.style.setProperty("--y", pos(fracOf(id))); ln.style.setProperty("--l", pos(supportFrac(id) ?? fracOf(id)));
    li.querySelector("[data-auw]").textContent = ST_WORD[st];
    li.querySelector("[data-aul]").textContent = L===null ? "—" : withU(id, L); li.querySelector("[data-aut]").textContent = withU(id);
    const hs = helpers(id); li.querySelector("[data-auh]").innerHTML = st==="short" && hs.length ? `Most help from: ${hs.map(h=>`<button type="button" data-ref="it:${h}">${esc(ITEMS[h].n)}</button>`).join("")}` : "";
    li.querySelector("[data-auf]").innerHTML = st==="short" ? `<button type="button" class="fillb" data-p2fill="${id}">Raise these to match my target</button>` : ""; });
}});
function p2CtaHTML2(){ return `<div class="cta"><button type="button" class="go ready" data-p2="go">Confirm targets and pick six KPIs <span aria-hidden="true">→</span></button><span class="cta-note" data-v="ctaNote2"></span></div>`; }
document.addEventListener("click", e => { const b = e.target.closest("[data-p2fill]"); if (!b) return; const id = b.dataset.p2fill, t = fillSupport(id); toast(t.length ? `Raised ${t.length} targets that affect ${ITEMS[id].n}. Yours were not changed.` : "Nothing to change: those targets are all yours."); });
