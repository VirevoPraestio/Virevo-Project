/* ===== Page 5 · Freeze · three options for checking and confirming the frozen plan ===== */
const P5_CSS = SIM_CSS + `
.lk-web .p5t{position:static;box-shadow:none}
.lk-web .stale5{display:flex;flex-wrap:wrap;align-items:center;gap:10px;justify-content:space-between;border:2px solid var(--w-gold);background:#FFF7E3;border-radius:12px;padding:10px 14px;margin:0 0 14px;font-size:13.5px}
.lk-web .stale5[hidden]{display:none}
.lk-web .stamp5{display:inline-flex;align-items:center;gap:8px;font-size:12.5px;color:var(--w-mute);margin:-6px 0 14px}
.lk-web .stamp5 b{font-family:var(--f-num);font-weight:400;font-size:18px;color:var(--w-ink);letter-spacing:.04em}
.lk-web .box5{border:2px solid var(--w-ink);border-radius:14px;background:var(--w-sheet);overflow:hidden;min-width:0}
.lk-web .box5>h2{margin:0;padding:10px 16px;border-bottom:1.5px solid var(--w-line);background:#F3F5F8;font-family:var(--f-num);font-weight:400;font-size:24px;line-height:1}
.lk-web .box5>h2 small{font-family:var(--f-body);font-size:12.5px;color:var(--w-mute);margin-left:8px}
.lk-web .kl5{list-style:none;margin:0;padding:4px 16px 8px;display:grid}
.lk-web .kl5 li{padding:10px 0;border-bottom:1px solid #E6EAF0;display:grid;gap:4px}
.lk-web .kl5 li:last-child{border-bottom:0}
.lk-web .kl5-n{display:flex;justify-content:space-between;gap:8px;align-items:baseline}
.lk-web .kl5-v{display:flex;flex-wrap:wrap;gap:4px 12px;align-items:baseline;font-size:12.5px;color:var(--w-mute)}
.lk-web .kl5-v b{font-family:var(--f-num);font-weight:400;font-size:20px;color:var(--w-ink)}
.lk-web .kl5-v .g{margin-left:auto} .lk-web .kl5-v .g b{color:var(--w-gold-ink)}
.lk-web .cg5{border-top:1.5px solid var(--w-line)} .lk-web .cg5:first-of-type{border-top:0}
.lk-web .cg5 h3{margin:0;padding:10px 16px 4px;font-size:13px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--w-mute);display:flex;justify-content:space-between;gap:8px}
.lk-web .cg5 h3 small{font-size:12.5px;letter-spacing:0;text-transform:none;font-weight:600;color:var(--w-ink)}
.lk-web .cg5 ul{list-style:none;margin:0;padding:0 16px 8px}
.lk-web .cg5 li{display:grid;grid-template-columns:minmax(0,1.4fr) minmax(0,1fr) 90px 92px;gap:8px;align-items:baseline;padding:6px 0;border-bottom:1px dashed #E1E6ED;font-size:13px}
.lk-web .cg5 li:last-child{border-bottom:0}
.lk-web .cg5 .lv{color:var(--w-ink)} .lk-web .cg5 .lv small{color:var(--w-mute)}
.lk-web .cg5 .cs{text-align:right;font-weight:600} .lk-web .cg5 .wh{text-align:right;font-size:12px;color:var(--w-mute)}
.lk-web .cf5{border:2px solid var(--w-ink);border-radius:16px;background:var(--w-sheet);padding:16px 18px;margin-top:16px;box-shadow:8px 8px 0 rgba(22,33,62,.12)}
.lk-web .cf5 h2{margin:0 0 10px;font-family:var(--f-num);font-weight:400;font-size:28px;line-height:1}
.lk-web .tk5{display:grid;gap:6px;margin-bottom:12px}
.lk-web .tk5 label{display:flex;gap:10px;align-items:center;font-size:14px;min-height:36px}
.lk-web .tk5 input{width:20px;height:20px;accent-color:var(--w-yours)}
.lk-web .who5{display:grid;grid-template-columns:repeat(2,minmax(0,260px));gap:10px;margin-bottom:12px}
.lk-web .who5 label{display:grid;gap:2px} .lk-web .who5 small{font-size:11.5px;font-weight:600;color:var(--w-mute)}
.lk-web .who5 input{min-height:40px;padding:6px 10px;border:1.5px solid var(--w-line);border-radius:8px;font-size:14px;background:#fff;color:var(--w-ink)}
.lk-web .cf5-b{display:flex;flex-wrap:wrap;gap:8px;justify-content:flex-end}
.lk-web .cf5-b .go{min-height:48px;padding:10px 22px}
.lk-web .cf5.done{border-color:var(--w-yours);background:#F1F8F3}
.lk-web .cf5.done .cf5-b{display:none}
.lk-web .cf5-done{margin:8px 0 0;display:flex;flex-wrap:wrap;align-items:center;gap:10px;font-size:14px}
.lk-web .cf5-done b{color:var(--w-yours)} .lk-web .cf5-done .go{margin-left:auto;min-height:44px;padding:8px 18px}
.lk-web .empty5{border:2px dashed var(--w-ink);border-radius:16px;padding:28px;text-align:center;background:var(--w-sheet);margin-top:16px}
.lk-web .empty5 h1{font-family:var(--f-num);font-weight:400;font-size:40px;margin:0 0 6px}
@media (max-width:760px){.lk-web .cg5 li{grid-template-columns:1fr auto}.lk-web .cg5 .lv{grid-column:1}.lk-web .cg5 .wh{grid-column:2}.lk-web .who5{grid-template-columns:1fr}}
`;
const stamp5 = () => SIMR.frozen ? `<div class="stamp5"><b>Frozen</b> ${esc(fmtDate(SIMR.frozen.at))} · compared with ${goalWord(SIMR.frozen.mode)} values</div>` : "";

/* A · Plan on a page */
LOOKS.push({ key:"p5sheet", page:"p5", step:4, letter:"A", name:"Plan on a page", note:"<b>A · Plan on a page.</b> The frozen plan as one sheet: the six numbers at the top, every approved change with its level, cost and months on the left, every KPI from today to where the plan takes it on the right. Three ticks and a name to confirm.",
css: P5_CSS + `
.lk-web .two5{display:grid;grid-template-columns:minmax(0,1.5fr) minmax(300px,1fr);gap:16px;align-items:start}
@media (max-width:1000px){.lk-web .two5{grid-template-columns:1fr}}
`,
mount(stage){ const d = SIMR.frozen ? p5Data() : null;
  p5Mount(stage, d && `${p5Head("Confirm your plan", "This is the plan you froze on Simulate. Check it, then confirm it. To change anything, go back to Simulate.")}${stamp5()}${p5Stale()}
    ${p5Tiles(d)}<div class="two5"><section class="box5"><h2>What changes<small>${d.s.n} approved</small></h2>${changeGroups5(d)}</section>
    <section class="box5"><h2>Selected KPIs<small>today → with this plan</small></h2>${kpiRows5(d)}</section></div>${p5Confirm(true)}`); },
update(root){ p5Sync(root); }
});

/* B · Before and after */
LOOKS.push({ key:"p5ba", page:"p5", step:4, letter:"B", name:"Before and after", note:"<b>B · Before and after.</b> Each KPI as a card, today and with the plan side by side. Below it, the money: what the plan spends and what it earns, month by month, and where the two lines cross (break-even). The approved changes underneath. Confirm with a name.",
css: P5_CSS + `
.lk-web .ba5{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin-bottom:16px}
.lk-web .bc5{border:2px solid var(--w-ink);border-radius:14px;background:var(--w-sheet);padding:12px 14px;display:grid;gap:6px;min-width:0}
.lk-web .bc5-h{display:flex;justify-content:space-between;gap:8px;align-items:baseline}
.lk-web .bc5-v{display:grid;grid-template-columns:1fr auto 1fr;align-items:end;gap:8px}
.lk-web .bc5-v div{display:grid} .lk-web .bc5-v span{font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--w-mute)}
.lk-web .bc5-v b{font-family:var(--f-num);font-weight:400;font-size:34px;line-height:1}
.lk-web .bc5-v .now b{color:var(--w-mute)} .lk-web .bc5-v .ar{font-size:22px;color:var(--w-mute);padding-bottom:4px}
.lk-web .bc5-v .pl b{color:var(--w-yours)}
.lk-web .bc5 small{font-size:12px;color:var(--w-mute)} .lk-web .bc5 small b{color:var(--w-gold-ink)}
.lk-web .mon5{padding:12px 16px 14px;position:relative}
.lk-web .mon5 svg{display:block;width:100%;height:auto;overflow:visible}
.lk-web .mon5 .ax{stroke:#C9D0DA;stroke-width:1} .lk-web .mon5 .gr{stroke:#E6EAF0;stroke-width:1}
.lk-web .mon5 text{font-family:var(--f-body);font-size:11px;fill:#4E5A73}
.lk-web .mon5 .lt{font-size:12px;font-weight:600;fill:#16213E}
.lk-web .mon5 .sp{fill:none;stroke:#C76A12;stroke-width:2;stroke-dasharray:6 4;stroke-linecap:round}
.lk-web .mon5 .er{fill:none;stroke:#1E7A4C;stroke-width:2;stroke-linecap:round}
.lk-web .mon5 .be{stroke:#16213E;stroke-width:1.5;stroke-dasharray:2 3}
.lk-web .mon5 .xh{stroke:#16213E;stroke-width:1;opacity:0} .lk-web .mon5 .dot{opacity:0;stroke:#FBFCFD;stroke-width:2}
.lk-web .mon5 .on .xh,.lk-web .mon5 .on .dot{opacity:1}
.lk-web .lg5{display:flex;flex-wrap:wrap;gap:4px 16px;font-size:12px;color:var(--w-mute);margin:0 0 6px}
.lk-web .lg5 i{display:inline-block;width:22px;height:0;border-top:2px solid;vertical-align:middle;margin-right:6px}
.lk-web .tip5{position:absolute;pointer-events:none;background:#16213E;color:#fff;border-radius:8px;padding:6px 9px;font-size:12px;line-height:1.4;white-space:nowrap;opacity:0;transition:opacity .1s}
.lk-web .tip5.on{opacity:1}
.lk-web .cf5.bar{position:sticky;bottom:12px;z-index:5;padding:10px 14px;margin-right:110px}
.lk-web .cf5.bar h2{display:none}
.lk-web .cf5.bar [data-v="cf5"]{display:flex;flex-wrap:wrap;align-items:end;gap:10px}
.lk-web .cf5.bar .who5{margin:0;flex:1 1 360px;grid-template-columns:1fr 1fr}
.lk-web .cf5.bar .cf5-done{margin:0;flex:1 1 100%}
.lk-web .cf5.bar.done{position:static}
@media (max-width:760px){.lk-web .cf5.bar{position:static;margin-right:0}.lk-web .cf5.bar h2{display:block}.lk-web .cf5.bar .who5{flex:1 1 100%;grid-template-columns:1fr}}
@media (max-width:1000px){.lk-web .ba5{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:560px){.lk-web .ba5{grid-template-columns:1fr}}
`,
mount(stage){ const d = SIMR.frozen ? p5Data() : null;
  const card = x => { const [st, w] = kpiState(x); return `<article class="bc5"><div class="bc5-h">${nameBtn(x.k)}<span class="k5-s" data-state="${st}">${w}</span></div>
    <div class="bc5-v"><div class="now"><span>Today</span><b>${esc(fmtV(x.k, x.t))}</b></div><span class="ar" aria-hidden="true">→</span><div class="pl"><span>With plan</span><b>${esc(fmtV(x.k, x.v))}</b></div></div>
    <small>${esc(unitOf(ITEMS[x.k]))} · ${goalWord(d.mode)} <b>${esc(fmtV(x.k, x.goal))}</b>${x.month ? ` · on target by month ${x.month}` : ""}</small></article>`; };
  p5Mount(stage, d && `${p5Head("Before and after", "Where your KPIs are today, and where this plan takes them. Below: what it spends and what it earns. Check, then confirm.")}${stamp5()}${p5Stale()}
    ${p5Tiles(d)}<div class="ba5">${d.kpis.map(card).join("")}</div>
    <section class="box5" style="margin-bottom:16px"><h2>Money in and out<small>running total, month by month</small></h2><div class="mon5" data-mon5></div></section>
    <section class="box5"><h2>What changes<small>${d.s.n} approved · ${money(d.s.tot)} over ${d.s.D} months</small></h2>${changeGroups5(d)}</section>
    <div class="cf5 bar">${p5Confirm(false).replace('<section class="cf5" data-v="cf5" aria-label="Confirm the plan">','<div data-v="cf5" aria-label="Confirm the plan">').replace(/<\/section>$/,'</div>')}</div>`);
  if (d) drawMoney5(stage.querySelector("[data-mon5]"), d); },
update(root){ p5Sync(root); const c = root.querySelector('.cf5.bar'), i = root.querySelector('.cf5.bar [data-v="cf5"]'); if (c && i) c.classList.toggle("done", i.classList.contains("done")); }
});
function drawMoney5(el, d){ const W = Math.max(300, Math.min(1400, (el.clientWidth || 860) - 32)), narrow = W < 560, H = narrow ? 220 : 280, L = 64, R = narrow ? 12 : 110, T = 12, B = 30, N = d.cash.length;
  const max = Math.max(...d.cash.map(c => Math.max(c.spent, c.earned)), 1), x = m => L + (m-1)/(N-1)*(W-L-R), y = v => T + (1 - v/max)*(H-T-B);
  const path = k => d.cash.map((c,i) => `${i?"L":"M"}${x(c.m).toFixed(1)},${y(c[k]).toFixed(1)}`).join("");
  const ticks = [0, .25, .5, .75, 1].map(f => f*max); const mt = d.cash.filter(c => c.m === 1 || c.m % 6 === 0);
  const last = d.cash[N-1], be = d.s.be && d.s.be <= N ? d.s.be : null;
  el.innerHTML = `<div class="lg5"><span><i style="border-color:#C76A12;border-top-style:dashed"></i>Money spent (one-time + monthly)</span><span><i style="border-color:#1E7A4C"></i>Extra EBITDA earned</span></div>
  <svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Running total of money spent and extra EBITDA earned over ${N} months${be ? `; they cross at month ${be}` : ""}">
    ${ticks.map(v => `<line class="gr" x1="${L}" x2="${W-R}" y1="${y(v)}" y2="${y(v)}"/><text x="${L-8}" y="${y(v)+4}" text-anchor="end">${money(v)}</text>`).join("")}
    <line class="ax" x1="${L}" x2="${W-R}" y1="${H-B}" y2="${H-B}"/>
    ${mt.map(c => `<text x="${x(c.m)}" y="${H-B+18}" text-anchor="middle">${c.m===1?"Month 1":c.m}</text>`).join("")}
    ${be ? `<line class="be" x1="${x(be)}" x2="${x(be)}" y1="${T}" y2="${H-B}"/><text class="lt" x="${x(be)+6}" y="${T+12}">${narrow ? "Break-even" : "Break-even, month "+be}</text>` : ""}
    <path class="sp" d="${path("spent")}"/><path class="er" d="${path("earned")}"/>
${narrow ? "" : `<text class="lt" x="${x(N)+8}" y="${y(last.spent)+4}">Spent ${money(last.spent)}</text><text class="lt" x="${x(N)+8}" y="${y(last.earned)+4 + (Math.abs(y(last.earned)-y(last.spent))<14?14:0)}">Earned ${money(last.earned)}</text>`}
    <g class="hv"><line class="xh" y1="${T}" y2="${H-B}"/><circle class="dot d1" r="5" fill="#C76A12"/><circle class="dot d2" r="5" fill="#1E7A4C"/></g>
    <rect x="${L}" y="${T}" width="${W-L-R}" height="${H-T-B}" fill="transparent" data-hit/></svg><div class="tip5" role="status"></div>`;
  const svg = el.querySelector("svg"), g = el.querySelector(".hv"), tip = el.querySelector(".tip5");
  const show = ev => { const r = svg.getBoundingClientRect(), px = (ev.clientX - r.left) / r.width * W; const m = Math.max(1, Math.min(N, Math.round((px - L)/(W-L-R)*(N-1)) + 1)), c = d.cash[m-1];
    g.classList.add("on"); g.querySelector(".xh").setAttribute("x1", x(m)); g.querySelector(".xh").setAttribute("x2", x(m));
    g.querySelector(".d1").setAttribute("cx", x(m)); g.querySelector(".d1").setAttribute("cy", y(c.spent)); g.querySelector(".d2").setAttribute("cx", x(m)); g.querySelector(".d2").setAttribute("cy", y(c.earned));
    tip.innerHTML = `<b>Month ${m}</b><br>Spent ${money(c.spent)}<br>Earned ${money(c.earned)}<br>${c.earned >= c.spent ? "Ahead by " + money(c.earned - c.spent) : "Behind by " + money(c.spent - c.earned)}`;
    const left = x(m)/W*r.width; tip.style.left = Math.min(left + 14, r.width - 150) + "px"; tip.style.top = "36px"; tip.classList.add("on"); };
  const hit = el.querySelector("[data-hit]"); hit.addEventListener("pointermove", show); hit.addEventListener("pointerleave", () => { g.classList.remove("on"); tip.classList.remove("on"); }); }

/* C · Month by month */
LOOKS.push({ key:"p5time", page:"p5", step:4, letter:"C", name:"Month by month", note:"<b>C · Month by month.</b> The frozen plan as a calendar: each approved change as a bar from the month it starts to the month it is fully working, the money going out each month, and the months that matter (break-even, all KPIs on target). The KPIs and confirm box below.",
css: P5_CSS + `
.lk-web .gt5{overflow-x:auto;padding:8px 16px 14px}
.lk-web .gt5 table{border-collapse:separate;border-spacing:0;width:100%;min-width:760px;font-size:12.5px}
.lk-web .gt5 th,.lk-web .gt5 td{padding:0;height:30px;border-bottom:1px solid #E6EAF0}
.lk-web .gt5 thead th{font-size:11px;font-weight:600;color:var(--w-mute);text-align:center;height:24px}
.lk-web .gt5 th.nm{text-align:left;width:230px;padding-right:10px;font-weight:400}
.lk-web .gt5 tbody th.nm .linkbtn b{font-size:12.5px}
.lk-web .gt5 tr.gh th{background:#F3F5F8;text-align:left;padding:4px 8px;font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--w-mute)}
.lk-web .gt5 td{position:relative;border-left:1px solid #EEF1F5}
.lk-web .gt5 .bar{position:absolute;top:7px;bottom:7px;left:2px;right:2px;background:#9FC8B0;border-radius:0}
.lk-web .gt5 .bar.s{border-radius:4px 0 0 4px} .lk-web .gt5 .bar.e{border-radius:0 4px 4px 0;background:var(--w-yours)} .lk-web .gt5 .bar.s.e{border-radius:4px}
.lk-web .gt5 .run{position:absolute;top:14px;height:2px;left:0;right:0;background:var(--w-yours);opacity:.5}
.lk-web .gt5 tr.ms td{height:26px}
.lk-web .gt5 .mk{position:absolute;inset:3px 2px;border-radius:6px;background:var(--w-ink);color:#fff;font-size:10.5px;font-weight:700;display:grid;place-items:center}
.lk-web .gt5 .mk.g{background:var(--w-gold);color:var(--w-ink)}
.lk-web .gt5 tr.mo td{height:56px;vertical-align:bottom}
.lk-web .gt5 .mb{position:absolute;bottom:4px;left:4px;right:4px;background:#C76A12;border-radius:4px 4px 0 0;min-height:2px}
.lk-web .gtk5{display:flex;flex-wrap:wrap;gap:4px 16px;padding:8px 16px 0;font-size:12px;color:var(--w-mute)}
.lk-web .gtk5 i{display:inline-block;width:18px;height:10px;border-radius:3px;margin-right:6px;vertical-align:middle}
.lk-web .low5{display:grid;grid-template-columns:minmax(0,1fr);gap:16px;margin-top:16px}
`,
mount(stage){ const d = SIMR.frozen ? p5Data() : null; if (!d) return p5Mount(stage, "");
  const M = Math.min(24, Math.max(12, ...d.changes.map(c => c.full), d.s.be || 0, d.s.reach || 0) + 1), months = Array.from({length:M}, (_,i)=>i+1);
  const perMonth = months.map(m => { const c = d.cash[m-1], p = d.cash[m-2]; return c ? c.spent - (p ? p.spent : 0) : 0; }), pmMax = Math.max(...perMonth, 1);
  const row = c => `<tr><th class="nm" scope="row">${nameBtn(c.id)}</th>${months.map(m => `<td>${m >= c.start && m <= c.full ? `<i class="bar${m===c.start?" s":""}${m===c.full?" e":""}" title="${esc(c.n)}: ${m===c.full?"fully working":"getting going"} in month ${m}"></i>` : m > c.full ? `<i class="run"></i>` : ""}</td>`).join("")}</tr>`;
  const groups = ["a","k","w","p"].map(k => { const xs = d.changes.filter(c => c.kind === k); return xs.length ? `<tr class="gh"><th colspan="${M+1}">${KINDNAME[k]}</th></tr>${xs.map(row).join("")}` : ""; }).join("");
  p5Mount(stage, `${p5Head("Your plan, month by month", "When each approved change starts, when it is fully working, and what goes out each month. Check, then confirm.")}${stamp5()}${p5Stale()}
    ${p5Tiles(d)}<section class="box5"><h2>The next ${M} months<small>${d.s.n} changes</small></h2>
    <div class="gtk5"><span><i style="background:#9FC8B0"></i>Getting going</span><span><i style="background:#1E7A4C"></i>Fully working</span><span><i style="background:#C76A12"></i>Money out that month</span><span><b>Even</b> = break-even month</span><span><b>KPIs</b> = all KPIs on target</span></div>
    <div class="gt5"><table><thead><tr><th class="nm"></th>${months.map(m => `<th scope="col">${m}</th>`).join("")}</tr></thead><tbody>
      <tr class="ms"><th class="nm" scope="row"><b>Key months</b></th>${months.map(m => `<td>${m===d.s.be ? `<span class="mk" title="Break-even">Even</span>` : m===d.s.reach ? `<span class="mk g" title="All KPIs on target">KPIs</span>` : ""}</td>`).join("")}</tr>
      ${groups}
      <tr class="mo"><th class="nm" scope="row"><b>Money out</b></th>${months.map((m,i) => `<td><i class="mb" style="height:${Math.round(perMonth[i]/pmMax*44)}px" title="Month ${m}: ${money(perMonth[i])}"></i></td>`).join("")}</tr>
    </tbody></table></div></section>
    <div class="low5"><section class="box5"><h2>Selected KPIs<small>today → with this plan</small></h2>${kpiRows5(d)}</section></div>${p5Confirm(false)}`); },
update(root){ p5Sync(root); }
});
