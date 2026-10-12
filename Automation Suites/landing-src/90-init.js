/* ===== init: one runtime, three page modes =====
   PAGE.mode "review"  → one suite, several look options (PAGE.suite, PAGE.schemes)
   PAGE.mode "pages"   → every approved suite landing, one picker (for the development team)
   PAGE.mode "library" → the suite block library (91-library.js) */
const SCHEME_SUITE = { monitor:"discharge", sheet:"discharge", diorama:"discharge", departures:"discharge", dispensary:"discharge",
  tubes:"billing", meters:"billing", sorter:"billing", signal:"admission", radar:"admission", dayboard:"diagnostic", prism:"diagnostic", racks:"procurement", lines:"procurement" };
const APPROVED = [["discharge","diorama"],["billing","sorter"],["admission","radar"],["diagnostic","dayboard"],["procurement","lines"]];
const stage = document.getElementById("stage"), picks = document.getElementById("picks");
const css = document.createElement("style"); css.textContent = SCHEMES.map(s=>s.css).join("\n"); document.head.appendChild(css);
const byKey = k => SCHEMES.find(s=>s.key===k);
let LIST = [];
if (PAGE.mode === "pages") LIST = APPROVED.filter(a=>byKey(a[1]) && SUITES.find(s=>s.key===a[0])).map(([su,k],i)=>({ suite:su, scheme:byKey(k), letter:String(i+1), label:SUITES.find(s=>s.key===su).data.suite }));
else if (PAGE.mode === "review") LIST = PAGE.schemes.map(k=>({ suite:PAGE.suite, scheme:byKey(k), letter:byKey(k).letter, label:byKey(k).name }));
document.getElementById("rvTitle").textContent = PAGE.title;
document.getElementById("rvSub").textContent = PAGE.sub;
if (PAGE.mode === "library") { picks.hidden = true; setSuite(SUITES[0].key); renderLibrary(); }
else {
  picks.innerHTML = LIST.map((s,i)=>`<button type="button" data-i="${i}" aria-pressed="${i===0}"><b>${esc(s.letter)}</b>${esc(s.label)}</button>`).join("");
  picks.onclick = e => { const b = e.target.closest("button"); if (!b) return; UI.scheme = +b.dataset.i; try { localStorage.setItem("suitePick-"+PAGE.mode+(PAGE.suite||""), UI.scheme); } catch(_){} render(); scrollTo(0,0); };
  if (LIST.length === 1) picks.hidden = true;
  try { const v = +localStorage.getItem("suitePick-"+PAGE.mode+(PAGE.suite||"")); if (v >= 0 && v < LIST.length) UI.scheme = v; } catch(_){}
  const hashMap = {a:0,b:1,c:2,d:3,e:4}; const hv = hashMap[location.hash.slice(1)]; if (hv !== undefined && hv < LIST.length) UI.scheme = hv;
  if (UI.scheme >= LIST.length) UI.scheme = 0;
  render();
}
function render(){
  if (PAGE.mode === "library") return renderLibrary();
  const it = LIST[UI.scheme], s = it.scheme;
  setSuite(it.suite);
  picks.querySelectorAll("button").forEach((b,i)=>b.setAttribute("aria-pressed", i===UI.scheme));
  document.getElementById("rvNote").innerHTML = PAGE.mode === "pages" ? `<b>${esc(D.suite)}</b> · approved look: ${esc(s.name.toLowerCase())}. ${esc(D.hospital)}, week ${D.week} of ${D.weeksPlanned}. Example figures.` : s.note;
  Object.entries(s.vars).forEach(([k,v]) => document.documentElement.style.setProperty(k, v));
  document.getElementById("chatFab").style.bottom = `calc(${s.fab||18}px + env(safe-area-inset-bottom,0px))`;
  stage.innerHTML = `<div data-suite="${it.suite}">${s.render()}</div>`;
  markTab(document.body.classList.contains("chat-open") ? "chat" : lastTab);
  if (s.after) s.after();
}
