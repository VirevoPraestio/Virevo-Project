/* ===== Page 4 · Option B · Cause and effect: changes on the left, the numbers they move in the middle, your six on the right ===== */
function mids4(){ const out = []; const six = new Set(S3.sel);
  S3.sel.forEach(k => (INPUTS[k]||[]).forEach(([f]) => { const it = ITEMS[f]; if (isLever(it) || six.has(f) || out.includes(f)) return; out.push(f);
    (INPUTS[f]||[]).forEach(([g]) => { const jt = ITEMS[g]; if (!isLever(jt) && !six.has(g) && !out.includes(g) && (INPUTS[g]||[]).some(([h]) => isLever(ITEMS[h]))) out.push(g); }); }));
  return out.filter(id => (INPUTS[id]||[]).length); }
LOOKS.push({ key:"chain", page:"p4", step:3, letter:"B", name:"Cause and effect", note:"<b>B · Cause and effect.</b> The plan drawn as a chain. On the left, the changes; in the middle, the numbers they move; on the right, your six. Lines grow thicker as more effect flows through them, and grey out when a change is left out. Rest on any box to light only its paths.",
css: P4_CSS + `
.lk-web .chain{position:relative;display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,.9fr) minmax(0,1fr);gap:56px;border:2px solid var(--w-ink);border-radius:18px;background:var(--w-sheet);padding:16px;box-shadow:8px 8px 0 rgba(22,33,62,.12)}
.lk-web .chain>svg{position:absolute;inset:0;width:100%;height:100%;pointer-events:none}
.lk-web .col{display:flex;flex-direction:column;gap:6px;position:relative;z-index:1;min-width:0}
.lk-web .col h2{margin:0 0 4px;font-size:12px;font-weight:700;letter-spacing:.12em;text-transform:uppercase}
.lk-web .col h3{margin:8px 0 2px;font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--w-mute)}
.lk-web .cbox{border:1.5px solid var(--w-line);border-radius:10px;background:#fff;padding:6px 8px;display:grid;gap:4px;min-width:0}
.lk-web .cbox.off{opacity:.5;background:#F3F5F8}
.lk-web .cbox .r1{display:flex;justify-content:space-between;gap:6px;align-items:center}
.lk-web .cbox .r1 .linkbtn{font-size:12.5px;line-height:1.25}
.lk-web .cbox .r2{display:flex;flex-wrap:wrap;gap:6px;align-items:center}
.lk-web .cbox .num{width:74px;min-height:34px}
.lk-web .cbox .inc{border:1.5px solid var(--w-ink);background:#fff;border-radius:999px;padding:2px 9px;font-size:11.5px;font-weight:600;min-height:32px;color:var(--w-ink)}
.lk-web .cbox .inc[aria-pressed="true"]{background:var(--w-ink);color:#fff}
.lk-web .cbox .sw{min-height:34px}
.lk-web .mbox{border:1.5px solid var(--w-line);border-radius:10px;background:#fff;padding:7px 9px;font-size:12.5px}
.lk-web .mbox b{display:block}
.lk-web .mbox .mv{font-family:var(--f-num);font-size:18px}
.lk-web .mbox .bar{height:5px;border-radius:3px;background:#E6EAF0;overflow:hidden;margin-top:3px}.lk-web .mbox .bar i{display:block;height:100%;background:var(--w-yours)}
.lk-web .kbox{border:2px solid var(--w-ink);border-radius:12px;background:#fff;padding:10px 12px}
.lk-web .kbox .v{font-family:var(--f-num);font-size:32px;line-height:1}
.lk-web .kbox small{display:block;font-size:12px;color:var(--w-mute)}
.lk-web .kbox .s{font-size:12px;font-weight:700}
.lk-web .ln{fill:none;stroke-linecap:round;transition:stroke-width .2s,opacity .2s}
.lk-web .chain.hov .ln{opacity:.08} .lk-web .chain.hov .ln.hl{opacity:1}
@media (max-width:980px){.lk-web .chain{grid-template-columns:1fr;gap:16px}.lk-web .chain>svg{display:none}}
`,
mount(stage){ init4();
  const cbox = id => { const it = ITEMS[id]; return `<div class="cbox" data-chg="${id}" data-node="${id}"><div class="r1">${nameBtn(id)}${isSwitch(it)?"":`<button type="button" class="inc" data-inc4="${id}" aria-pressed="true">In</button>`}</div><div class="r2">${changeControl4(id)}${isSwitch(it)?"":`<small style="font-size:11px;color:var(--w-mute)">${esc(unitOf(it))} · today ${esc(fmtV(id,it.t))}</small>`}</div></div>`; };
  const left = ["a","k","w","p"].map(k => { const ids = changes4().filter(id => kind4(id)===k); return ids.length ? `<h3>${KINDNAME[k]}</h3>${ids.map(cbox).join("")}` : ""; }).join("");
  const mid = mids4().map(id => `<div class="mbox" data-node="${id}">${nameBtn(id)}<span class="mv" data-sv="${id}"></span> <small style="color:var(--w-mute)">${esc(unitOf(ITEMS[id]))} · today ${esc(fmtV(id, ITEMS[id].t))}</small><div class="bar"><i data-mb="${id}"></i></div></div>`).join("");
  const right = S3.sel.map(id => `<div class="kbox" data-node="${id}">${nameBtn(id)}<div class="v" data-sv="${id}"></div><small>${esc(unitOf(ITEMS[id]))} · today ${esc(fmtV(id, ITEMS[id].t))} · target ${esc(fmtV(id))}</small><span class="s" data-st="${id}"></span></div>`).join("");
  p4Mount(stage, `${p4Head("Simulate your plan", "Follow each change through the numbers it moves to your six. Change a level or leave a change out, and the chain redraws. Save the versions you like as scenarios.")}
    ${monthBarHTML()}<div class="tools"><button type="button" class="act ghost" data-p4="all">Put every change in</button><button type="button" class="act ghost" data-p4="none">Take every change out</button><button type="button" class="act ghost" data-p4="reset">Back to my page-2 levels</button></div>
    <div class="chain"><svg aria-hidden="true"></svg><div class="col"><h2>The changes</h2>${left}</div><div class="col"><h2>The numbers they move</h2>${mid}</div><div class="col"><h2>Your six</h2>${right}</div></div>
    ${othersHTML()}${p4Cta()}`);
  const ch = stage.querySelector(".chain");
  ch.addEventListener("pointerover", e => { const n = e.target.closest("[data-node]"); if (!n) return; ch.classList.add("hov"); const id = n.dataset.node; ch.querySelectorAll(".ln").forEach(l => l.classList.toggle("hl", l.dataset.a===id || l.dataset.b===id)); });
  ch.addEventListener("pointerleave", () => { ch.classList.remove("hov"); });
  this._ro = this._ro || new ResizeObserver(() => this.lines(stage)); this._ro.disconnect(); this._ro.observe(ch);
},
lines(root){ const ch = root.querySelector(".chain"); if (!ch) return; const svg = ch.querySelector("svg"); const box = ch.getBoundingClientRect(); if (getComputedStyle(svg).display === "none") return;
  const pos = id => { const n = ch.querySelector(`[data-node="${id}"]`); if (!n) return null; const r = n.getBoundingClientRect(); return { l: r.left - box.left, r: r.right - box.left, y: r.top - box.top + r.height/2 }; };
  const f = simFracs(); const nodes = new Set([...ch.querySelectorAll("[data-node]")].map(n => n.dataset.node)); let h = "";
  const colOf = id => ch.querySelector(`[data-node="${id}"]`)?.closest(".col");
  nodes.forEach(to => (INPUTS[to]||[]).forEach(([from,w]) => { if (!nodes.has(from) || colOf(from) === colOf(to)) return; const a = pos(from), b = pos(to); if (!a || !b) return;
    const eff = f(from), on = eff > 0.001, sw = 1 + w*eff*7; const x1 = a.r, x2 = b.l, mx = (x1+x2)/2;
    h += `<path class="ln" data-a="${from}" data-b="${to}" d="M${x1} ${a.y} C${mx} ${a.y} ${mx} ${b.y} ${x2} ${b.y}" stroke="${on?"#d4a94f":"#C9D0DA"}" stroke-width="${sw.toFixed(1)}" ${on?"":'stroke-dasharray="4 4"'}/>`; }));
  svg.setAttribute("viewBox", `0 0 ${box.width} ${box.height}`); svg.innerHTML = h; },
update(root){ sync4(root); syncOthers(root);
  const f = simFracs(); root.querySelectorAll("[data-mb]").forEach(i => i.style.width = (Math.min(1,f(i.dataset.mb))*100)+"%");
  root.querySelectorAll(".cbox .inc").forEach(b => b.textContent = b.getAttribute("aria-pressed")==="true" ? "In" : "Out");
  requestAnimationFrame(() => this.lines(root)); }
});
