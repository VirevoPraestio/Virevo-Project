/* ===== helpers ===== */
let D, P, KP, spendTotal, ebitdaTotal, revTotal, onCourse, SUITE_KEY;
function prog(k, v){ return Math.max(0, Math.min(1.15, (v - k.base) / (k.target - k.base))); }
function kstate(k){ const d = prog(k,k.now) - prog(k,k.plan); return d >= 0 ? "ahead" : d > -0.1 ? "watch" : "off"; }
function fmtv(k, v){ if (k.unit === "%") return v + "%"; if (k.unit === "h") return v + " hours"; if (k.unit === "L") return "₹" + v + " lakh"; if (k.unit === "n") return String(v); const h = Math.floor(v/60), m = v%60; return h ? (m ? `${h} h ${m} min` : `${h} h`) : `${m} min`; }
function gapText(k){ const raw = Math.abs(k.now - k.plan); const g = Math.round(raw*10)/10; const amt = k.unit==="%" ? `${g} point${g===1?"":"s"}` : fmtv(k,g);
  if (k.state === "ahead") return `${amt} ahead of plan`; return k.dir==="down" ? `${amt} over plan` : `${amt} under plan`; }
const STATE_WORD = { ahead:"On track", watch:"Slightly behind", off:"Off track" };
const PART_WORD = { live:"Live", testing:"Testing", building:"Being built", blocked:"Late", notstarted:"Not started" };
function pstate(p){ const r = p.done / p.due; return p.late >= 2 || r < 0.6 ? "off" : p.late ? "watch" : "ahead"; }
const PERSON_WORD = { ahead:"Doing well", watch:"Slipping", off:"Lagging" };
const countParts = s => D.parts.filter(p => p.st === s).length;
const L = v => "₹" + (Math.round(v*10)/10).toLocaleString("en-IN") + " lakh";
const sum = a => a.reduce((x,y)=>x+y,0);
/* switch the whole page to one suite's data */
function setSuite(key){ if (SUITE_KEY === key && D) return; const s = SUITES.find(x=>x.key===key); if (!s) return; SUITE_KEY = key; D = s.data;
  P = Object.fromEntries(D.people.map(p => [p.key, p])); KP = Object.fromEntries(D.kpis.map(k => [k.id, k]));
  D.kpis.forEach(k => k.state = kstate(k)); D.people.forEach(p => p.state = pstate(p));
  spendTotal = Math.round(sum(D.spend.map(s=>sum(s.v)))*100)/100; ebitdaTotal = Math.round(sum(D.ebitda)*100)/100; revTotal = Math.round(sum(D.revenue)*100)/100;
  onCourse = D.kpis.filter(k=>k.state!=="off").length;
  if (typeof fillChat === "function") fillChat(); if (typeof onSuite === "function") onSuite(key); }
function suiteOf(el){ const w = el && el.closest && el.closest("[data-suite]"); if (w) setSuite(w.dataset.suite); }
const esc = s => String(s).replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const initials = n => n.replace(/^(Dr\.|Sister)\s+/,"").split(" ").map(w=>w[0]).join("").slice(0,2);
