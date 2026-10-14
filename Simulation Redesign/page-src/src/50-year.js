/* ===== Page 4 · Option C · The year ahead: when each change starts, and month by month what it does to your six ===== */
LOOKS.push({ key:"year", page:"p4", step:3, letter:"C", name:"The year ahead", note:"<b>C · The year ahead.</b> The plan on a twelve-month calendar. Each change is a bar: it starts in the month you choose and builds up over the time it really takes (hiring about three months, equipment about six, process changes one, automations from go-live). Below, your six as lines across the year against their targets, so you can see when each one gets there, or doesn't.",
css: P4_CSS + `
.lk-web .gantt{border:2px solid var(--w-ink);border-radius:16px;background:var(--w-sheet);overflow:hidden;margin-bottom:16px}
.lk-web .g-row{display:grid;grid-template-columns:minmax(200px,1.1fr) 112px minmax(0,3fr);align-items:center;border-top:1px solid #E6EAF0;min-height:46px}
.lk-web .g-row.hd{background:#F3F5F8;border-top:0;font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--w-mute);min-height:34px}
.lk-web .g-row.kind{background:#F8FAFC;font-size:11.5px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;min-height:30px;padding-left:12px}
.lk-web .g-nm{padding:6px 12px;min-width:0}
.lk-web .g-nm small{display:block;font-size:11px;color:var(--w-mute)}
.lk-web .g-ctl{display:flex;flex-direction:column;gap:3px;padding:4px 6px}
.lk-web .g-ctl .inc{border:1.5px solid var(--w-ink);background:#fff;border-radius:999px;padding:2px 8px;font-size:11px;font-weight:600;min-height:30px;color:var(--w-ink)}
.lk-web .g-ctl .inc[aria-pressed="true"]{background:var(--w-ink);color:#fff}
.lk-web .g-ctl .mv{display:flex;gap:3px;align-items:center;font-size:11px;color:var(--w-mute)}
.lk-web .g-ctl .mv button{width:30px;height:30px;border:1.5px solid var(--w-line);border-radius:8px;background:#fff;color:var(--w-ink)}
.lk-web .g-tl{position:relative;height:100%;min-height:44px;display:grid;grid-template-columns:repeat(12,1fr);background:repeating-linear-gradient(90deg,transparent 0 calc(100%/12 - 1px),#E6EAF0 calc(100%/12 - 1px) calc(100%/12))}
.lk-web .g-tl span{font-size:11px;text-align:center;align-self:center}
.lk-web .g-bar{position:absolute;top:12px;bottom:12px;border-radius:6px;border:1.5px solid var(--w-ink)}
.lk-web .g-row.off .g-bar{border-style:dashed;opacity:.4}
.lk-web .g-cur{position:absolute;top:0;bottom:0;width:2px;background:var(--w-none);pointer-events:none}
.lk-web .g-row.off{background:#F7F8FA}
.lk-web .lines6{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin-bottom:6px}
.lk-web .l6{border:2px solid var(--w-ink);border-radius:14px;background:var(--w-sheet);padding:10px 12px}
.lk-web .l6 .t{display:flex;justify-content:space-between;gap:8px;align-items:baseline}
.lk-web .l6 .v{font-family:var(--f-num);font-size:26px;line-height:1}
.lk-web .l6 svg{display:block;width:100%;height:auto;margin-top:6px}
.lk-web .l6 .s{font-size:12px;font-weight:700}
.lk-web .l6 .when{font-size:12px;color:var(--w-mute)}
@media (max-width:1050px){.lk-web .lines6{grid-template-columns:1fr 1fr}}
@media (max-width:720px){.lk-web .lines6{grid-template-columns:1fr}.lk-web .g-row{grid-template-columns:minmax(0,1fr) 104px}.lk-web .g-tl{grid-column:1/-1;min-height:36px}.lk-web .g-row.hd .g-tl{display:none}.lk-web .g-row.hd{grid-template-columns:1fr}}
`,
mount(stage){ init4();
  const months = Array.from({length:12},(_,i)=>`<span>${i+1}</span>`).join("");
  const row = id => { const it = ITEMS[id], k = kind4(id);
    return `<div class="g-row" data-chg="${id}"><div class="g-nm">${nameBtn(id)}<small>${isSwitch(it)?"":`level ${esc(withU(id, S4.val[id]))} · `}${k==="a"?"works from go-live":k==="k"?"about 6 months to install":k==="p"?"about 3 months to hire":"about a month to take hold"}</small></div>
      <div class="g-ctl"><button type="button" class="inc" data-inc4="${id}" aria-pressed="true">In the plan</button><span class="mv"><button type="button" data-mv="${id}:-1" aria-label="Start one month earlier">◀</button>start <b data-sm="${id}"></b><button type="button" data-mv="${id}:1" aria-label="Start one month later">▶</button></span></div>
      <div class="g-tl"><i class="g-bar" data-gb="${id}"></i><i class="g-cur" data-cur></i></div></div>`; };
  const rows = ["a","k","w","p"].map(k => { const ids = changes4().filter(id => kind4(id)===k); return ids.length ? `<div class="g-row kind">${KINDNAME[k]}</div>${ids.map(row).join("")}` : ""; }).join("");
  p4Mount(stage, `${p4Head("Simulate the year ahead", "Each change starts in a month you choose and takes as long as it really takes. Shift the start months, leave changes out, and watch your six move through the year. Save the versions you like as scenarios.")}
    <div class="lines6">${S3.sel.map(id => `<div class="l6"><div class="t">${nameBtn(id)}<span class="v" data-sv="${id}"></span></div><svg viewBox="0 0 300 110" data-l6="${id}" aria-hidden="true"></svg><span class="s" data-st="${id}"></span> <span class="when" data-wh="${id}"></span></div>`).join("")}</div>
    ${monthBarHTML()}
    <section class="gantt" aria-label="When each change happens"><div class="g-row hd"><div class="g-nm">Change</div><div class="g-ctl">In plan · start</div><div class="g-tl">${months}<i class="g-cur" data-cur></i></div></div>${rows}</section>
    <div class="tools"><button type="button" class="act ghost" data-p4="all">Put every change in</button><button type="button" class="act ghost" data-p4="reset">Back to my page-2 levels and months</button></div>
    ${othersHTML()}${p4Cta()}`);
  stage.querySelectorAll("[data-mv]").forEach(b => b.addEventListener("click", () => { const [id,d] = b.dataset.mv.split(":"); S4.start[id] = Math.max(1, Math.min(12, (S4.start[id]||1) + +d)); changed4(); }));
},
update(root){ sync4(root); syncOthers(root);
  root.querySelectorAll("[data-sm]").forEach(e => e.textContent = `M${S4.start[e.dataset.sm]}`);
  root.querySelectorAll("[data-gb]").forEach(b => { const id = b.dataset.gb, st = S4.start[id], len = RAMP[kind4(id)][1]; const L = (st-1)/12*100, R = 100;
    const full = Math.min(100, (st-1+len)/12*100); b.style.left = L+"%"; b.style.width = (R-L)+"%";
    b.style.background = `linear-gradient(90deg, rgba(212,169,79,.25) 0%, rgba(212,169,79,1) ${Math.max(1,((full-L)/(R-L||1))*100)}%, rgba(212,169,79,1) 100%)`; });
  root.querySelectorAll("[data-cur]").forEach(c => c.style.left = `calc(${(S4.month-.5)/12*100}% - 1px)`);
  S3.sel.forEach(id => { const it = ITEMS[id], svg = root.querySelector(`[data-l6="${id}"]`); if (!svg) return;
    const vals = Array.from({length:12},(_,i) => simVal(id, i+1)), tgt = valOf(id);
    const lo = Math.min(it.t, it.b, tgt, ...vals), hi = Math.max(it.t, it.b, tgt, ...vals), pad = (hi-lo)*.1 || 1;
    const Y = v => { let p = (v - (lo-pad)) / ((hi+pad) - (lo-pad)); if (it.d < 0) p = 1-p; return (100 - p*88).toFixed(1); }, X = i => (12 + i*(276/11)).toFixed(1);
    const reach = vals.findIndex(v => it.d > 0 ? v >= tgt - Math.abs(it.b-it.t)*.03 : v <= tgt + Math.abs(it.b-it.t)*.03);
    svg.innerHTML = `<line x1="8" x2="292" y1="${Y(tgt)}" y2="${Y(tgt)}" stroke="#d4a94f" stroke-width="2" stroke-dasharray="6 4"/><text x="292" y="${(+Y(tgt)-4).toFixed(1)}" font-size="10" text-anchor="end" fill="#6B4F16">target ${esc(fmtV(id, tgt))}</text>
      <line x1="8" x2="292" y1="${Y(it.t)}" y2="${Y(it.t)}" stroke="#9AA5B8" stroke-width="1"/><text x="10" y="${(+Y(it.t)+11).toFixed(1)}" font-size="10" fill="#4E5A73">today</text>
      <polyline fill="none" stroke="#16213E" stroke-width="2.5" points="${vals.map((v,i)=>`${X(i)},${Y(v)}`).join(" ")}"/>
      <circle cx="${X(S4.month-1)}" cy="${Y(vals[S4.month-1])}" r="5" fill="#16213E" stroke="#fff" stroke-width="2"/>${reach>=0?`<circle cx="${X(reach)}" cy="${Y(vals[reach])}" r="6" fill="none" stroke="#1E7A4C" stroke-width="2.5"/>`:""}`;
    const wh = root.querySelector(`[data-wh="${id}"]`); if (wh) wh.textContent = reach >= 0 ? `· reaches target in month ${reach+1}` : "· not within the year"; });
}});
