/* ===== Page 2 · Option B · Ladders: start from the nine outcomes, then see what each one takes ===== */
LOOKS.push({ key:"ladders", letter:"B", name:"Ladders", note:"<b>B · Ladders.</b> Outcome first. Each KPI is a ladder from today (bottom rung) to best practice (top); Tojo's realistic value is the gold rung. Drag the pin up to set your target. The green column rising inside is what the targets underneath back. Pick a ladder to see what it takes, and let Tojo fill the targets under it to match.",
css: P2_CSS + `
.lk-web .lads{display:grid;grid-template-columns:repeat(9,minmax(0,1fr));gap:10px;margin-bottom:18px}
.lk-web .lad{border:2px solid var(--w-line);border-radius:14px;background:var(--w-sheet);padding:10px 8px 10px;display:flex;flex-direction:column;align-items:center;gap:6px;min-width:0}
.lk-web .lad.sel{border-color:var(--w-ink);box-shadow:6px 6px 0 rgba(22,33,62,.14)}
.lk-web .lad .pick{border:0;background:none;padding:0;text-align:center;cursor:pointer;color:var(--w-ink);min-height:44px;width:100%}
.lk-web .lad .pick b{display:block;font-family:var(--f-num);font-weight:400;font-size:20px;line-height:1;letter-spacing:.02em}
.lk-web .lad .pick span{display:block;font-family:var(--f-num);font-size:26px;line-height:1.1}
.lk-web .lad .pick small{display:block;font-size:10.5px;color:var(--w-mute)}
.lk-web .lad.mine .pick span{color:var(--w-gold-ink)}
.lk-web .shaft{position:relative;width:64px;height:250px}
.lk-web .shaft .rails{position:absolute;inset:0 12px;border-left:3px solid var(--w-ink);border-right:3px solid var(--w-ink);background:repeating-linear-gradient(0deg,transparent 0 23px,var(--w-line) 23px 25px)}
.lk-web .shaft .back{position:absolute;left:18px;right:18px;bottom:0;height:var(--b);background:linear-gradient(0deg,rgba(30,122,76,.55),rgba(30,122,76,.25));border-radius:3px 3px 0 0;transition:height .3s}
.lk-web .lad[data-state="short"] .shaft .back{background:linear-gradient(0deg,rgba(178,59,59,.5),rgba(178,59,59,.2))}
.lk-web .shaft .rung-r{position:absolute;left:6px;right:6px;bottom:var(--r);height:4px;margin-bottom:-2px;background:var(--w-gold);border-radius:2px}
.lk-web .shaft .lb{position:absolute;right:calc(100% + 2px);font-size:10px;color:var(--w-mute);white-space:nowrap;transform:translateY(50%)}
.lk-web .shaft input[type=range]{position:absolute;inset:-9px 0;width:100%;height:calc(100% + 18px);margin:0;writing-mode:vertical-lr;direction:rtl;-webkit-appearance:none;appearance:none;background:transparent;cursor:pointer}
.lk-web .shaft input[type=range]::-webkit-slider-runnable-track{width:64px;background:transparent}
.lk-web .shaft input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:52px;height:16px;border-radius:8px;background:#fff;border:3px solid var(--w-ink);box-shadow:0 2px 0 rgba(22,33,62,.25)}
.lk-web .shaft input[type=range]::-moz-range-thumb{width:46px;height:12px;border-radius:8px;background:#fff;border:3px solid var(--w-ink)}
.lk-web .lad.mine .shaft input[type=range]::-webkit-slider-thumb{background:var(--w-ink);border-color:var(--w-gold)}
.lk-web .shaft input[type=range]:focus-visible{outline:3px solid var(--w-gold)}
.lk-web .lad .tag{font-size:11px;font-weight:600;color:var(--w-mute);text-align:center;line-height:1.25}
.lk-web .lad[data-state="short"] .tag{color:var(--w-none)}
.lk-web .lad[data-state="ahead"] .tag{color:var(--w-yours)}
.lk-web .takes{border:2px solid var(--w-ink);border-radius:16px;background:var(--w-sheet);box-shadow:8px 8px 0 rgba(22,33,62,.12)}
.lk-web .takes-h{display:flex;flex-wrap:wrap;align-items:center;gap:8px 16px;padding:14px 16px;border-bottom:1.5px solid var(--w-line)}
.lk-web .takes-h h2{margin:0;font-family:var(--f-num);font-weight:400;font-size:30px;line-height:1}
.lk-web .takes-h p{margin:0;flex:1 1 300px;font-size:13.5px;color:var(--w-mute)}
.lk-web .takes-h .hand{font-family:var(--f-hand);font-weight:700;font-size:23px;color:var(--w-gold-ink);line-height:1}
.lk-web .tk{display:grid;grid-template-columns:minmax(160px,1.1fr) 60px minmax(150px,2fr) 84px 92px;gap:6px 12px;align-items:center;padding:8px 16px;border-top:1px solid #E6EAF0}
.lk-web .tk .k{font-size:10.5px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--w-mute)}
.lk-web .tk .wbar{height:6px;border-radius:3px;background:#E6EAF0;overflow:hidden}.lk-web .tk .wbar i{display:block;height:100%;background:var(--w-ink)}
.lk-web .tk .rd{font-family:var(--f-num);font-size:22px;text-align:right}
.lk-web .tk.sw-row{grid-template-columns:minmax(160px,1.1fr) 60px minmax(0,1fr)}
.lk-web .tk .ctl{display:flex;gap:8px;flex-wrap:wrap}
.lk-web .tk-h{display:grid;grid-template-columns:minmax(160px,1.1fr) 60px minmax(150px,2fr) 84px 92px;gap:12px;padding:8px 16px 0;font-size:10.5px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--w-mute)}
@media (max-width:1180px){.lk-web .lads{grid-template-columns:repeat(5,minmax(0,1fr))}}
@media (max-width:760px){.lk-web .lads{grid-template-columns:repeat(3,minmax(0,1fr))}.lk-web .shaft{height:190px}.lk-web .shaft .lb{display:none}.lk-web .tk,.lk-web .tk.sw-row{grid-template-columns:minmax(0,1fr) 80px}.lk-web .tk .wcol,.lk-web .tk-h{display:none}.lk-web .tk .rl{grid-column:1/-1}}
`,
mount(stage){
  this.sel = this.sel || "EBITDA";
  const lads = KPIS.map(k => { const it = ITEMS[k.id];
    return `<div class="lad" data-lad="${k.id}" data-mine="${k.id}"><button type="button" class="pick" data-pick="${k.id}" aria-pressed="false"><b>${esc(k.s)}</b><span data-tv="${k.id}"></span><small>${esc(unitOf(it))} · today ${esc(fmtV(k.id,it.t))}</small></button>
      <div class="shaft" style="--r:${fracOf(k.id,it.r)*100}%"><div class="rails"></div><div class="back"></div><div class="rung-r" title="Tojo's realistic ${esc(fmtV(k.id,it.r))}"></div><span class="lb" style="bottom:100%">best ${esc(fmtV(k.id,it.b))}</span><span class="lb" style="bottom:0">today</span>
        <input type="range" min="0" max="1" step="0.01" data-lf="${k.id}" aria-label="Your target for ${esc(k.n)}, as a share of the way from today to best practice"></div>
      <div class="tag" data-ltag="${k.id}"></div></div>`; }).join("");
  p2Mount(stage, `${p2Head("Start from the outcomes", "Set how far each KPI should climb, from today to best practice. Then open any ladder to see the targets underneath it: the people, equipment, ways of working, automations and measures that have to move with it.")}
    <div class="tools"><div class="legend2"><span><i class="lg-t"></i>Bottom rung: today</span><span><i class="lg-r"></i>Tojo's realistic</span><span><i style="width:14px;height:12px;background:rgba(30,122,76,.5)"></i>Backed by the targets underneath</span><span><i class="lg-y"></i>Your pin</span></div><button type="button" class="act ghost" data-p2="reset" style="margin-left:auto">Reset everything to Tojo's realistic</button></div>
    <div class="lads">${lads}</div>
    <section class="takes" aria-live="polite"><div data-v="takes"></div></section>
    <div style="margin-top:18px">${p2CtaHTML()}</div>`);
  stage.querySelectorAll("[data-lf]").forEach(r => r.addEventListener("input", () => { const id = r.dataset.lf, it = ITEMS[id]; setTarget(id, it.t + (+r.value)*(it.b-it.t)); if (this.sel !== id) { this.sel = id; this.renderTakes(stage); } }));
  stage.querySelectorAll("[data-pick]").forEach(b => b.addEventListener("click", () => { this.sel = b.dataset.pick; this.renderTakes(stage); refresh(null); }));
  this.renderTakes(stage);
},
renderTakes(root){
  const id = this.sel, it = ITEMS[id];
  const ins = (INPUTS[id]||[]).slice().sort((a,b)=>b[1]-a[1]);
  const kindW = f => { const x = ITEMS[f]; return x.kind==="lever" ? KIND[x.k][0] : x.kind==="kpi" ? "Outcome" : "Measure"; };
  const rows = ins.map(([f,w]) => { const x = ITEMS[f];
    if (isSwitch(x)) return `<div class="tk sw-row" data-mine="${f}"><div>${nameBtn(f)}<div class="k">${kindW(f)}</div></div><div class="wcol"><div class="wbar" title="weight ${w}"><i style="width:${w*100}%"></i></div></div><div class="ctl">${controlHTML(f)}</div></div>`;
    return `<div class="tk" data-mine="${f}"><div>${nameBtn(f)}<div class="k">${kindW(f)} ${srcMini(f)}</div></div><div class="wcol"><div class="wbar" title="weight ${w}"><i style="width:${w*100}%"></i></div></div>${rulerHTML(f)}<div class="rd" data-tv="${f}"></div><div>${controlHTML(f)}</div></div>`; }).join("");
  const box = root.querySelector('[data-v="takes"]');
  box.innerHTML = `<div class="takes-h"><h2>What it takes: ${esc(it.n)}</h2><p>Your target <b data-tv="${id}"></b> ${esc(unitOf(it))} asks for <b data-askp="${id}"></b> of the way from today to best practice. The ${ins.length} targets underneath back <b data-bkp="${id}"></b>. Heavier bars pull harder.</p>
    <span class="hand" data-hand="${id}"></span><button type="button" class="act" data-p2="solve:${id}">Fill what it takes</button></div>
    <div class="tk-h"><span>Target underneath</span><span>Pull</span><span>Today → best</span><span style="text-align:right">Target</span><span>Type</span></div>${rows}`;
  wireTargets(box);
},
update(root){ syncTargets(root); syncGlyphs(root);
  root.querySelectorAll("[data-lf]").forEach(r => { if (document.activeElement !== r) r.value = fracOf(r.dataset.lf); });
  root.querySelectorAll(".lad").forEach(l => { const id = l.dataset.lad, t = tension(id), b = backed(id); l.dataset.state = t>.15?"short":t<-.15?"ahead":"ok"; l.classList.toggle("sel", id===this.sel); l.querySelector(".pick").setAttribute("aria-pressed", id===this.sel);
    l.querySelector(".shaft").style.setProperty("--b", ((b??0)*100)+"%");
    l.querySelector("[data-ltag]").textContent = t>.15 ? `short by ${pct(t)}` : t<-.15 ? "backed, with room" : "backed"; });
  root.querySelectorAll("[data-askp]").forEach(e => e.textContent = pct(fracOf(e.dataset.askp)));
  root.querySelectorAll("[data-bkp]").forEach(e => e.textContent = pct(backed(e.dataset.bkp)));
  root.querySelectorAll("[data-hand]").forEach(e => { const t = tension(e.dataset.hand); e.textContent = t>.15 ? "not enough underneath" : "it holds"; });
}});
