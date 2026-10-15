/* ===== review page: option picker ===== */
let CUR = null;
if (PAGE.only) { const keep = PAGE.only.map(k => LOOKS.find(l => l.key === k)).filter(Boolean); LOOKS.length = 0; LOOKS.push(...keep); }
const LSKEY = "simlook:" + PAGE.title;
function mountLook(i){
  CUR = LOOKS[i]; const stage = document.getElementById("stage");
  document.getElementById("lookCss").textContent = CUR.css;
  CUR.mount(stage); refresh(null);
  document.getElementById("rvNote").innerHTML = CUR.note;
  document.querySelectorAll("#picks button").forEach((b,j)=>b.setAttribute("aria-pressed", j===i?"true":"false"));
  try { localStorage.setItem(LSKEY, String(i)); } catch(e) {} window.scrollTo(0,0);
}
function refresh(arrived){
  const root = document.querySelector("#stage .lk"); if (!root) return;
  fillCommon(root); CUR.update(root, arrived);
  if (!chatBody.querySelector(".you")) fillChat();
}
listeners.push(refresh);
document.head.insertAdjacentHTML("beforeend", '<style id="lookCss"></style>');
document.getElementById("picks").innerHTML = LOOKS.map((l,i)=>`<button type="button" data-i="${i}"><b>${PAGE.byPage ? (l.step+1) : l.letter}</b>${esc(PAGE.byPage ? JOURNEY[l.step][0] : l.name)}</button>`).join("");
document.querySelectorAll("#picks button").forEach(b => b.onclick = () => mountLook(+b.dataset.i));
document.getElementById("rvTitle").textContent = PAGE.title; document.getElementById("rvSub").textContent = PAGE.sub;
document.getElementById("picks").hidden = LOOKS.length < 2;
document.querySelector(".rvtools").hidden = PAGE.rvtools === false;
document.querySelectorAll("[data-rv]").forEach(b => b.onclick = () => b.dataset.rv==="sample" ? playSample() : clearAll());
openingState();
let start = 0; if (!PAGE.product) { try { start = +(localStorage.getItem(LSKEY)||0); } catch(e) {} }
if (PAGE.product) { document.querySelector(".rv").hidden = true; document.getElementById("rvNote").hidden = true; document.title = PAGE.title; }
const fromHash = LOOKS.findIndex(l => "#"+l.key === location.hash);
mountLook(fromHash>=0 ? fromHash : (start < LOOKS.length ? start : 0));
document.addEventListener("click", e => { const b = e.target.closest("#stage [data-step]"); if (!b || !PAGE.byPage) return; const st = +b.dataset.step;
  /* the single-file product: go back freely, forward only as far as the page buttons have taken you */
  if (PAGE.product && st > Math.max(REACHED, CUR.step)) { toast(LOOKS.some(l => l.step === st) ? "Finish this step first. The button at the end of the page takes you on." : `The ${JOURNEY[st][0]} page comes in the next round.`); return; }
  const i = LOOKS.findIndex(l => l.step === st); if (i >= 0 && LOOKS[i] !== CUR) mountLook(i); else if (i < 0) toast(`The ${JOURNEY[st][0]} page comes in the next round.`); });
