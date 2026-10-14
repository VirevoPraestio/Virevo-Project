/* ===== Page 4 · Option A · The mixing desk: a fader for every change, six dials for your KPIs ===== */
const P4_CSS = P3_CSS + `
.lk-web .mbar{display:flex;flex-wrap:wrap;align-items:center;gap:10px 16px;border:2px solid var(--w-ink);border-radius:14px;background:var(--w-sheet);padding:10px 16px;margin:0 0 16px}
.lk-web .mbar label{font-size:12px;font-weight:700;letter-spacing:.1em;text-transform:uppercase}
.lk-web .mbar input[type=range]{flex:1 1 220px;accent-color:#16213E;min-height:36px}
.lk-web .mbar output{font-family:var(--f-num);font-size:24px;min-width:200px}
.lk-web .mbar .scen{display:flex;flex-wrap:wrap;gap:6px;margin-left:auto}
.lk-web .mbar .scen .act{min-height:40px}
.lk-web .others{border:1.5px dashed var(--w-ink);border-radius:12px;padding:10px 14px;margin:16px 0;background:var(--w-sheet)}
.lk-web .others h2{margin:0 0 6px;font-size:12px;font-weight:700;letter-spacing:.1em;text-transform:uppercase}
.lk-web .others .chips{display:flex;flex-wrap:wrap;gap:6px}
.lk-web .others button{border:1.5px solid var(--w-line);background:#fff;border-radius:999px;padding:4px 10px;font-size:12.5px;min-height:32px;color:var(--w-ink)}
.lk-web [data-state="hit"]{color:var(--w-yours)} .lk-web [data-state="near"]{color:var(--w-gold-ink)} .lk-web [data-state="far"]{color:var(--w-none)}
`;
function dialSVG(id){ return `<svg viewBox="0 0 200 124" class="dial" aria-hidden="true"><path d="M20 105 A80 80 0 0 1 180 105" fill="none" stroke="#DCE2EA" stroke-width="14" stroke-linecap="round"/><path data-arc="${id}" d="" fill="none" stroke="#1E7A4C" stroke-width="14" stroke-linecap="round"/><line data-tk="${id}" x1="0" y1="0" x2="0" y2="0" stroke="#d4a94f" stroke-width="4"/><line data-nd="${id}" x1="100" y1="105" x2="100" y2="30" stroke="#16213E" stroke-width="4" stroke-linecap="round"/><circle cx="100" cy="105" r="8" fill="#16213E"/><text x="20" y="117" font-size="10" fill="#4E5A73">today</text><text x="180" y="117" font-size="10" fill="#4E5A73" text-anchor="end">best</text></svg>`; }
function syncDials(root){ const P = (f,r) => { const a = Math.PI*(1-Math.max(0,Math.min(1,f))); return [100 + r*Math.cos(a), 105 - r*Math.sin(a)]; };
  root.querySelectorAll("[data-nd]").forEach(l => { const id = l.dataset.nd, f = simFracs()(id); const [x,y] = P(f, 72); l.setAttribute("x2", x.toFixed(1)); l.setAttribute("y2", y.toFixed(1));
    const [ax,ay] = P(f, 80); root.querySelector(`[data-arc="${id}"]`).setAttribute("d", f > 0.005 ? `M20 105 A80 80 0 0 1 ${ax.toFixed(1)} ${ay.toFixed(1)}` : "");
    const ft = Math.min(1, fracOf(id)); const [t1x,t1y] = P(ft, 70), [t2x,t2y] = P(ft, 92); const tk = root.querySelector(`[data-tk="${id}"]`); tk.setAttribute("x1",t1x.toFixed(1)); tk.setAttribute("y1",t1y.toFixed(1)); tk.setAttribute("x2",t2x.toFixed(1)); tk.setAttribute("y2",t2y.toFixed(1)); }); }
function othersHTML(){ return `<section class="others"><h2>Other numbers your plan moves</h2><div class="chips" data-v="others"></div></section>`; }
function syncOthers(root){ const box = root.querySelector('[data-v="others"]'); if (!box) return; const o = movedOthers(10);
  box.innerHTML = o.length ? o.map(id => `<button type="button" data-ref="it:${id}">${esc(ITEMS[id].n)}: ${esc(withU(id, simVal(id)))}</button>`).join("") : `<span style="font-size:13px;color:var(--w-mute)">Nothing else moves yet.</span>`; }
LOOKS.push({ key:"desk", page:"p4", step:3, letter:"A", name:"Mixing desk", note:"<b>A · Mixing desk.</b> Every change your six bring in is a fader, grouped as automations, beds and equipment, process and role changes, and staff numbers. Push a fader up toward best practice, switch a change in or out of the plan, and watch the six dials move. The gold mark on each dial is your target. Move the month to see when the results arrive.",
css: P4_CSS + `
.lk-web .dials{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:10px;margin-bottom:14px}
.lk-web .dialc{border:2px solid var(--w-ink);border-radius:14px;background:var(--w-sheet);padding:10px 10px 8px;text-align:center;min-width:0}
.lk-web .dialc .linkbtn{display:block;width:100%;text-align:center;min-height:36px}
.lk-web .dialc .linkbtn b{font-size:13px}
.lk-web .dial{display:block;width:100%;max-width:200px;margin:0 auto}
.lk-web .dialc .v{font-family:var(--f-num);font-size:30px;line-height:1}
.lk-web .dialc small{display:block;font-size:11.5px;color:var(--w-mute)}
.lk-web .dialc .s{font-size:11.5px;font-weight:700}
.lk-web .desk{border:2px solid var(--w-ink);border-radius:16px;background:#1C2745;padding:12px;margin-bottom:6px}
.lk-web .desk h2{margin:6px 6px 8px;color:#E9EDF5;font-size:12px;font-weight:700;letter-spacing:.12em;text-transform:uppercase}
.lk-web .chans{display:grid;grid-template-columns:repeat(auto-fill,minmax(122px,1fr));gap:8px;margin-bottom:10px}
.lk-web .ch{background:#26335A;border:1.5px solid #3A4A78;border-radius:12px;padding:8px;display:flex;flex-direction:column;align-items:center;gap:6px;color:#E9EDF5;min-width:0}
.lk-web .ch.off{opacity:.45}
.lk-web .ch .linkbtn{color:#fff;text-align:center;min-height:40px;font-size:12px;line-height:1.25}
.lk-web .ch .linkbtn b{font-weight:600}
.lk-web .fad{position:relative;width:46px;height:150px;border-radius:10px;background:repeating-linear-gradient(0deg,#33426E 0 14px,#2B3962 14px 15px)}
.lk-web .fad input{position:absolute;inset:0;width:100%;height:100%;margin:0;writing-mode:vertical-lr;-webkit-appearance:none;appearance:none;background:transparent;cursor:pointer}
.lk-web .fad input::-webkit-slider-runnable-track{width:6px;background:#0F1730;border-radius:3px}
.lk-web .fad input::-webkit-slider-thumb{-webkit-appearance:none;width:40px;height:20px;margin-left:-17px;border-radius:5px;background:linear-gradient(#F4F6FA,#C9D0DA);border:2px solid #0F1730}
.lk-web .fad input::-moz-range-thumb{width:36px;height:16px;border-radius:5px;background:#E9EDF5;border:2px solid #0F1730}
.lk-web .fad input:focus-visible{outline:3px solid var(--w-gold)}
.lk-web .ch .fv{font-family:var(--f-num);font-size:20px;line-height:1}
.lk-web .ch .fv small{display:block;font-family:var(--f-body);font-size:10px;color:#B5BFD6}
.lk-web .ch .inc{border:1.5px solid #6B7AA8;background:transparent;color:#E9EDF5;border-radius:999px;padding:3px 10px;font-size:11.5px;font-weight:600;min-height:32px}
.lk-web .ch .inc[aria-pressed="true"]{background:var(--w-gold);border-color:var(--w-gold);color:#16213E}
.lk-web .ch .sw{background:#fff}
.lk-web .ch .gomo{max-width:110px;font-size:12px}
.lk-web .ch .lamp{font-size:10.5px;color:#B5BFD6}
.lk-web .deskacts{display:flex;flex-wrap:wrap;gap:6px;margin:4px 6px 4px}
.lk-web .deskacts button{border:1.5px solid #6B7AA8;background:transparent;color:#E9EDF5;border-radius:999px;padding:4px 12px;font-size:12.5px;font-weight:600;min-height:36px}
@media (max-width:1150px){.lk-web .dials{grid-template-columns:repeat(3,minmax(0,1fr))}}
@media (max-width:560px){.lk-web .dials{grid-template-columns:repeat(2,minmax(0,1fr))}.lk-web .chans{grid-template-columns:repeat(2,minmax(0,1fr))}}
`,
mount(stage){ init4();
  const c3 = cover3();
  const chan = id => { const it = ITEMS[id], [mn,mx] = rangeOf(it);
    const ctl = isSwitch(it) ? `<div style="height:150px;display:flex;flex-direction:column;justify-content:center;gap:8px;align-items:center">${changeControl4(id)}</div>`
      : `<div class="fad"><input type="range" aria-label="Level for ${esc(it.n)}" min="${mn}" max="${mx}" step="${stepOf(it)}" data-r4="${id}" style="direction:${it.d<0?"ltr":"rtl"}"></div><div class="fv"><span data-cv="${id}"></span><small>${esc(unitOf(it)||"")}</small></div>`;
    return `<div class="ch" data-chg="${id}">${nameBtn(id)}${ctl}${isSwitch(it)?"":`<button type="button" class="inc" data-inc4="${id}" aria-pressed="true">In the plan</button>`}<span class="lamp">reaches ${c3.lev[id]} of your six</span></div>`; };
  const groups = ["a","k","w","p"].map(k => { const ids = changes4().filter(id => kind4(id)===k); return ids.length ? `<h2>${KINDNAME[k]}</h2><div class="chans">${ids.map(chan).join("")}</div>` : ""; }).join("");
  p4Mount(stage, `${p4Head("Simulate your plan", "Every change your six bring in starts at the level you set on page 2. Move them, switch them in or out, and watch your six respond. Save the versions you like as scenarios.")}
    <div class="dials">${S3.sel.map(id => `<div class="dialc">${nameBtn(id)}${dialSVG(id)}<div class="v" data-sv="${id}"></div><small>target ${esc(withU(id))}</small><span class="s" data-st="${id}"></span></div>`).join("")}</div>
    ${monthBarHTML()}
    <section class="desk" aria-label="The changes in your plan"><div class="deskacts"><button type="button" data-p4="all">Put every change in the plan</button><button type="button" data-p4="none">Take every change out</button><button type="button" data-p4="reset">Back to my page-2 levels</button></div>${groups}</section>
    ${othersHTML()}${p4Cta()}`);
},
update(root){ sync4(root); syncDials(root); syncOthers(root); root.querySelectorAll("[data-cv]").forEach(e => e.textContent = fmtV(e.dataset.cv, S4.val[e.dataset.cv])); }
});
