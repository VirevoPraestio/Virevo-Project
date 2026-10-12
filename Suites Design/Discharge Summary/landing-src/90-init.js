/* ===== init ===== */
const stage = document.getElementById("stage"), picks = document.getElementById("picks");
const css = document.createElement("style"); css.textContent = SCHEMES.map(s=>s.css).join("\n"); document.head.appendChild(css);
picks.innerHTML = SCHEMES.map((s,i)=>`<button type="button" data-i="${i}" aria-pressed="${i===0}"><b>${s.letter}</b>${esc(s.name)}</button>`).join("");
picks.onclick = e => { const b = e.target.closest("button"); if (!b) return; UI.scheme = +b.dataset.i; try { localStorage.setItem("suiteScheme", UI.scheme); } catch(_){} render(); scrollTo(0,0); };
if (SCHEMES.length === 1) { picks.hidden = true; document.getElementById("rvSub").textContent = "Scheme C, the hospital diorama (chosen 12 Oct). Example figures for a 250-bed hospital in Bhubaneswar, week 10 of 26."; }
function render(){
  const s = SCHEMES[UI.scheme];
  picks.querySelectorAll("button").forEach((b,i)=>b.setAttribute("aria-pressed", i===UI.scheme));
  document.getElementById("rvNote").innerHTML = s.note;
  Object.entries(s.vars).forEach(([k,v]) => document.documentElement.style.setProperty(k, v));
  document.getElementById("chatFab").style.bottom = `calc(${s.fab||18}px + env(safe-area-inset-bottom,0px))`;
  stage.innerHTML = s.render();
  markTab(document.body.classList.contains("chat-open") ? "chat" : lastTab);
  if (s.after) s.after();
}
try { const v = +localStorage.getItem("suiteScheme"); if (v >= 0 && v < SCHEMES.length) UI.scheme = v; } catch(_){}
const hashMap = {a:0,b:1,c:2,d:3,e:4}; if (hashMap[location.hash.slice(1)] !== undefined && hashMap[location.hash.slice(1)] < SCHEMES.length) UI.scheme = hashMap[location.hash.slice(1)];
if (UI.scheme >= SCHEMES.length) UI.scheme = 0;
render();
