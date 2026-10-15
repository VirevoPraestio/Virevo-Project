/* ===== Page 2 · shared look: the approved One formula look, plus rulers, switches and asked/backed bars ===== */
const P2_CSS = WEB_CSS + `
.lk-web .jr .done button{color:var(--w-ink);border-color:var(--w-ink)} .lk-web .jr .done button b{background:var(--w-yours);color:#fff}
.lk-web .p2head{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,560px);gap:16px 30px;align-items:end;margin:22px 0 16px}
.lk-web .p2head .pulse{margin:0}
.lk-web .tools{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:0 0 16px}
.lk-web .tools .act{min-height:40px}
.lk-web .legend2{display:flex;flex-wrap:wrap;gap:6px 16px;font-size:12.5px;color:var(--w-mute)}
.lk-web .legend2 span{display:inline-flex;align-items:center;gap:6px}
.lk-web .legend2 i{display:inline-block}
.lk-web .lg-t{width:2px;height:14px;background:var(--w-ink)}
.lk-web .lg-r{width:10px;height:10px;background:var(--w-gold);transform:rotate(45deg)}
.lk-web .lg-b{width:0;height:0;border-left:9px solid var(--w-yours);border-top:6px solid transparent;border-bottom:6px solid transparent}
.lk-web .lg-y{width:14px;height:14px;border-radius:50%;background:var(--w-ink);box-shadow:0 0 0 2px #fff,0 0 0 3.5px var(--w-ink)}
/* ruler */
.lk-web .rl{position:relative;height:34px;min-width:0}
.lk-web .rl-track{position:absolute;left:9px;right:9px;top:14px;height:6px;border-radius:3px;background:#DCE2EA}
.lk-web .rl-gap{position:absolute;top:0;bottom:0;left:var(--pt);width:calc(var(--pb) - var(--pt));background:#CFE6D9;border-radius:3px}
.lk-web .rl-mk{position:absolute;top:50%}
.lk-web .rl-t{left:var(--pt);width:2px;height:18px;margin:-9px 0 0 -1px;background:var(--w-ink)}
.lk-web .rl-r{left:var(--pr);width:10px;height:10px;margin:-5px 0 0 -5px;background:var(--w-gold);transform:rotate(45deg)}
.lk-web .rl-b{left:var(--pb);margin:-15px 0 0 -1px;width:0;height:0;border-left:10px solid var(--w-yours);border-top:6px solid transparent;border-bottom:6px solid transparent}
.lk-web .rl-b::before{content:"";position:absolute;left:-11px;top:-2px;width:2px;height:20px;background:var(--w-yours)}
.lk-web .rl input[type=range]{position:absolute;inset:0;width:100%;height:34px;margin:0;opacity:1;background:transparent;-webkit-appearance:none;appearance:none;cursor:pointer}
.lk-web .rl input[type=range]::-webkit-slider-runnable-track{height:34px;background:transparent}
.lk-web .rl input[type=range]::-moz-range-track{height:34px;background:transparent}
.lk-web .rl input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:18px;height:18px;margin-top:8px;border-radius:50%;background:#fff;border:3px solid var(--w-ink);box-shadow:0 2px 0 rgba(22,33,62,.25)}
.lk-web .rl input[type=range]::-moz-range-thumb{width:14px;height:14px;border-radius:50%;background:#fff;border:3px solid var(--w-ink)}
.lk-web .rl.mine input[type=range]::-webkit-slider-thumb{background:var(--w-ink);border-color:var(--w-gold)}
.lk-web .rl.mine input[type=range]::-moz-range-thumb{background:var(--w-ink);border-color:var(--w-gold)}
.lk-web .rl input[type=range]:focus-visible{outline:3px solid var(--w-gold);outline-offset:2px;border-radius:6px}
.lk-web .num{width:84px;min-height:38px;border:1.5px solid var(--w-line);border-radius:8px;padding:4px 8px;font:inherit;font-size:13.5px;background:#fff;color:var(--w-ink);font-variant-numeric:tabular-nums}
.lk-web .num:focus{outline:3px solid var(--w-gold);border-color:var(--w-ink)}
/* switch */
.lk-web .sw{display:inline-flex;align-items:center;gap:8px;border:1.5px solid var(--w-line);border-radius:999px;background:#fff;padding:4px 12px 4px 4px;min-height:40px;font-weight:600;font-size:13px;color:var(--w-mute)}
.lk-web .sw::before{content:"";width:40px;height:24px;border-radius:12px;background:#DCE2EA;box-shadow:inset 0 0 0 2px #C9D0DA;transition:background .2s}
.lk-web .sw[aria-pressed="true"]{color:var(--w-ink);border-color:var(--w-ink)}
.lk-web .sw[aria-pressed="true"]::before{background:var(--w-yours) radial-gradient(circle at 70% 50%,#fff 7px,transparent 7.5px)}
.lk-web .sw:not([aria-pressed="true"])::before{background:#DCE2EA radial-gradient(circle at 30% 50%,#fff 7px,transparent 7.5px)}
.lk-web .sw.mine{box-shadow:0 0 0 2px var(--w-gold)}
.lk-web .gomo{min-height:38px;border:1.5px solid var(--w-line);border-radius:8px;background:#fff;font:inherit;font-size:13px;padding:0 6px;color:var(--w-ink)}
/* asked and backed */
.lk-web .ab{position:relative;height:16px;border-radius:4px;background:#E6EAF0;overflow:hidden}
.lk-web .ab::before{content:"";position:absolute;left:0;top:0;bottom:8px;width:var(--a);background:var(--w-ink)}
.lk-web .ab::after{content:"";position:absolute;left:0;bottom:0;top:8px;width:var(--b);background:var(--w-yours)}
.lk-web .ab[data-state="short"]::after{background:var(--w-none)}
.lk-web .abtag{font-size:11.5px;font-weight:600;color:var(--w-mute)}
.lk-web [data-state="short"] + .abtag,.lk-web .abtag.short{color:var(--w-none)}
.lk-web .mine-dot{display:none;font-size:11px;font-weight:700;color:var(--w-gold-ink);letter-spacing:.06em;text-transform:uppercase}
.lk-web .mine .mine-dot,.lk-web .mine-dot.mine{display:inline}
.lk-web .srcmini{font-size:10.5px;font-weight:600;border-radius:999px;padding:1px 7px;border:1.5px solid currentColor;white-space:nowrap}
.lk-web .srcmini.yours{color:var(--w-yours)} .lk-web .srcmini.ref{color:var(--w-ref);border-style:dashed} .lk-web .srcmini.manual{color:var(--w-paper2)} .lk-web .srcmini.none{color:var(--w-none);border-style:dotted}
.lk-web .glyphs{display:flex;flex-wrap:wrap;gap:2px;align-items:center;min-height:18px}
.lk-web .glyphs i{display:block;width:9px;height:16px;border-radius:5px 5px 2px 2px;background:var(--w-ink)}
.lk-web .glyphs i.add{background:transparent;box-shadow:inset 0 0 0 2px var(--w-gold)}
.lk-web .glyphs i.cut{background:#DCE2EA}
.lk-web .glyphs.kit i{width:14px;height:12px;border-radius:2px}
.lk-web .linkbtn{border:0;background:none;padding:0;color:inherit;font:inherit;text-align:left;cursor:pointer}
.lk-web .linkbtn:hover b,.lk-web .linkbtn:focus b{text-decoration:underline}
@media (max-width:980px){.lk-web .p2head{grid-template-columns:1fr}}
`;
function glyphsHTML(id){ const it = ITEMS[id]; if (it.kind!=="lever" || (it.k!=="people" && it.k!=="kit") || isSwitch(it)) return "";
  return `<span class="glyphs ${it.k==="kit"?"kit":""}" data-gl="${id}" aria-hidden="true"></span>`; }
function syncGlyphs(root){ root.querySelectorAll("[data-gl]").forEach(g => { const it = ITEMS[g.dataset.gl], v = valOf(g.dataset.gl); const base = Math.round(it.t), tgt = Math.round(v), n = Math.min(40, Math.max(base,tgt));
  let h = ""; for (let i=0;i<n;i++) h += `<i class="${i<Math.min(base,tgt)?"":i<tgt?"add":"cut"}"></i>`; g.innerHTML = h; }); }
function nameBtn(id, extra=""){ const it = ITEMS[id]; return `<button type="button" class="linkbtn" data-ref="it:${id}"><b>${esc(it.n)}</b>${extra}</button>`; }
function srcMini(id){ const it = ITEMS[id]; if (it.kind!=="ms") return ""; const s = msState(MS[id]); return `<span class="srcmini ${s}" title="Today's value: ${SRC_WORD[s]}">${SRC_SHORT[s]}</span>`; }
function controlHTML(id){ const it = ITEMS[id];
  if (isSwitch(it)) return `<button type="button" class="sw" data-sw="${id}" aria-pressed="false">${it.k==="auto"?"Switch on":"In place"}</button>${it.k==="auto"?`<label class="sr-only" for="go-${id}">Go-live month</label><select class="gomo" id="go-${id}" data-go="${id}">${Array.from({length:12},(_,i)=>`<option value="${i+1}" ${TS.go[id]===i+1?"selected":""}>Live month ${i+1}</option>`).join("")}</select>`:""}`;
  return `<label class="sr-only" for="n-${id}">Type a target for ${esc(it.n)}</label><input class="num" id="n-${id}" type="number" step="${stepOf(it)}" data-num="${id}" inputmode="decimal">`; }
function p2Mount(stage, inner){ stage.innerHTML = `<div class="lk lk-web">${journeyHTML(1)}${inner}</div>`; wireTargets(stage); }
function p2Head(title, lede){ return `<div class="p2head"><div><div class="eb">Simulation · step 2 of 8 · ${esc(HOSPITAL.name)}, ${HOSPITAL.beds} beds</div><h1>${title}</h1><p class="lede">${lede}</p></div>${p2PulseHTML()}</div>`; }
