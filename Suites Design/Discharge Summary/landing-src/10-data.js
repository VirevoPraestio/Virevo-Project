/* ===== Example data: Discharge Summary suite, 250-bed hospital, Bhubaneswar. All figures are examples. ===== */
const D = {
  suite: "Discharge Summary",
  family: "Discharge Process",
  hospital: "250-bed hospital, Bhubaneswar",
  started: "4 Aug 2026", week: 10, weeksPlanned: 26, asOf: "12 Oct 2026, 10:40 AM",
  siblings: ["Discharge Summary","Billing & Insurance","Admission Process","Diagnostic Scheduling","Procurement","Financial Health"],
  milestone: { what: "Doctor signs off on phone goes live", date: "15 Oct", days: 3, part: 11 },

  parts: [
    { id:1,  name:"Admission notes and diagnosis", src:"Hospital software (HIS)", dept:"ward",  st:"live",     when:"Live since 2 Sep",  fresh:"2 min ago",  owner:"sanjay", vol:"about 45 admissions a day", note:"History, symptoms and diagnosis at admission are read in as they are typed." },
    { id:2,  name:"Lab results and abnormal findings", src:"Lab system", dept:"lab", st:"live", when:"Live since 9 Sep", fresh:"6 min ago", owner:"sanjay", vol:"about 610 results a day", note:"Abnormal values are marked and pulled into the summary with the date." },
    { id:3,  name:"Imaging reports", src:"Imaging system (PACS)", dept:"radio", st:"blocked", when:"9 days late · now 28 Oct", fresh:"no feed yet", owner:"sanjay", vol:"about 120 reports a day", note:"The vendor has not opened its data link. Reports are pasted in by hand meanwhile.",
      delay:"The imaging vendor has not opened its data link and has asked for a ₹2.5 lakh interface fee that was not in the plan. Until it opens, about 120 reports a day are pasted in by hand, the imaging section of the summary stays empty, and ₹3.6 lakh of benefit is pushed back.",
      fixes:[["Read imaging reports from the PDF the system already prints, until the link opens","sanjay","20 Oct"],["Escalate to the vendor's regional head and ask for the fee to be credited against next year's support","kavya","31 Oct"],["Imaging link live","sanjay","28 Oct"]] },
    { id:4,  name:"Operation and procedure notes", src:"Theatre register", dept:"ot", st:"testing", when:"Goes live 19 Oct", fresh:"test feed, 1 h ago", owner:"sanjay", vol:"about 22 cases a day", note:"Notes from 3 of 5 theatres are coming through in the test." },
    { id:5,  name:"Medicines given, changed and left over", src:"Pharmacy and drug chart", dept:"pharm", st:"testing", when:"Goes live 22 Oct", fresh:"test feed, 20 min ago", owner:"lipika", vol:"about 2,400 doses a day", note:"Left-over stock is counted in whole strips and bottles, so returns are realistic." },
    { id:6,  name:"Consumables used and left over", src:"Stores (ERP)", dept:"stores", st:"building", when:"Due 30 Oct", fresh:"no feed yet", owner:"sanjay", vol:"about 3,100 items a day", note:"Item codes are being matched between the wards and the stores list." },
    { id:7,  name:"Doctor's daily notes by voice", src:"Voice notes app", dept:"ward", st:"testing", when:"On 4 of 9 wards", fresh:"live on 4 wards", owner:"mishra", vol:"about 160 notes a day", note:"Doctors speak their round notes; nurses check them before they count." },
    { id:8,  name:"Reasons behind each step", src:"Worked out from parts 1 to 7", dept:"engine", st:"notstarted", when:"Starts 2 Nov", fresh:"not started", owner:"kavya", vol:"—", note:"Links each test, procedure and medicine to why it was done and what came of it." },
    { id:9,  name:"Discharge flagged at the evening round", src:"Voice app and doctor's phone", dept:"phone", st:"live", when:"Live on 6 of 9 wards", fresh:"last flag 9:52 PM", owner:"mishra", vol:"about 18 flags an evening", note:"A passing mention on the evening round starts the summary that night." },
    { id:10, name:"Summary put together automatically", src:"Summary engine", dept:"engine", st:"live", when:"Live since 16 Sep", fresh:"1 min ago", owner:"kavya", vol:"about 42 summaries a day", note:"Fills 62% of the summary today; rises as the imaging and stores links land." },
    { id:11, name:"Doctor signs off on phone", src:"Doctor's phone or tablet", dept:"phone", st:"testing", when:"Goes live 15 Oct", fresh:"test, 3 doctors", owner:"mishra", vol:"—", note:"The morning confirmation brings the summary back to the doctor to sign on the spot." },
    { id:12, name:"Nurse checks captured notes", src:"Nursing station", dept:"nurse", st:"live", when:"Live since 23 Sep", fresh:"4 min ago", owner:"lipika", vol:"about 160 checks a day", note:"Nurses approve what was captured from voice notes and any change made on the floor." }
  ],
  handoffs: [
    { name:"Running bill fed from the same records", to:"Billing & Insurance", st:"notstarted", when:"Kick-off moved up to 2 Nov" },
    { name:"Summary sent to the insurer with the final bill", to:"Billing & Insurance", st:"notstarted", when:"After the running bill" }
  ],

  /* dir: "down" means lower is better. Values: base, target, plan (where the plan said we would be in week 10), now. */
  kpis: [
    { id:"K1", name:"Summary ready after the doctor's decision", short:"Summary ready", unit:"min", dir:"down", base:190, target:15, plan:70, now:48,
      why:"Evening flags start the summary the night before, so most are waiting when the doctor confirms." },
    { id:"K2", name:"Discharges flagged at the evening round", short:"Evening flags", unit:"%", dir:"up", base:0, target:70, plan:45, now:41,
      factors:[["Orthopaedics and cardiology doctors not yet flagging by voice",60],["Evening round runs past 9 PM on two wards",40]],
      fixes:[["A doctor lead in each of the two departments, with a weekly count by ward","mishra","26 Oct"],["7 PM reminder on the doctor's phone for patients likely to go","kavya","16 Oct"]],
      back:"Back on the plan line by week 13 (2 Nov)" },
    { id:"K3", name:"Summary filled without typing", short:"Filled automatically", unit:"%", dir:"up", base:0, target:90, plan:70, now:62,
      factors:[["Imaging section empty until the imaging link opens",55],["Consumables section waits on the stores link",30],["Reasons section not started",15]],
      fixes:[["Read imaging reports from the PDF the system already prints, until the link opens","sanjay","20 Oct"],["Stores link live","sanjay","30 Oct"]],
      back:"Back on the plan line by week 14 (9 Nov)" },
    { id:"K4", name:"Morning sign-off time", short:"Sign-off time", unit:"min", dir:"down", base:140, target:20, plan:45, now:35,
      why:"Priya brings each summary to the doctor at the end of the round, before the next ward." },
    { id:"K5", name:"Decision to patient leaving", short:"Decision to exit", unit:"min", dir:"down", base:405, target:150, plan:240, now:290,
      factors:[["The bill is still made by hand; the Billing & Insurance suite has not started",45],["Pharmacy returns counted by hand on 3 wards",25],["Wheelchair and transport wait after 11 AM",15],["Imaging reports pasted in by hand",15]],
      fixes:[["Start the running-bill feed early: Billing & Insurance kick-off moved to 2 Nov","kavya","2 Nov"],["Stores link live, so returns are worked out, not counted","sanjay","30 Oct"],["Book the wheelchair when the summary is signed","ritika","19 Oct"]],
      back:"Back on the plan line by week 16 (23 Nov)" },
    { id:"K6", name:"Cash patients out by 10 AM", short:"Cash out by 10 AM", unit:"%", dir:"up", base:8, target:60, plan:35, now:22,
      factors:[["Tests ordered on the morning round instead of the night before",40],["Bill made by hand",35],["Family arrives after 10 AM",25]],
      fixes:[["The evening flag asks the doctor for any last tests that night","mishra","26 Oct"],["Message to the family the moment the summary is signed","priya","15 Oct"]],
      back:"Back on the plan line by week 17 (30 Nov)" },
    { id:"K7", name:"Insured patients out by 1 PM", short:"Insured out by 1 PM", unit:"%", dir:"up", base:12, target:55, plan:30, now:27,
      factors:[["Insurer's first approval still asked for the next morning",70],["Summary waits for imaging before it goes to the insurer",30]],
      fixes:[["Arjun sends the provisional summary to the insurance desk the same night, by hand for now","arjun","14 Oct"]],
      back:"Back on the plan line by week 12 (26 Oct)" },
    { id:"K8", name:"Family briefed before the patient leaves", short:"Family briefed", unit:"%", dir:"up", base:72, target:100, plan:90, now:96,
      why:"The briefing sheet now prints with the summary, so nurses brief while the bill is closed." },
    { id:"K9", name:"Bill no longer waits on the stock count", short:"No stock-count wait", unit:"%", dir:"up", base:0, target:85, plan:40, now:18,
      factors:[["Consumables link to the stores not live yet",70],["Nurses still do the full count out of habit",30]],
      fixes:[["Stores link live","sanjay","30 Oct"],["Nurses count only the items the system flags","lipika","20 Oct"]],
      back:"Back on the plan line by week 15 (16 Nov)" }
  ],

  people: [
    { key:"ritika", name:"Ritika Das", role:"Discharge Manager", from:"New role we recommended · joined 1 Sep", done:11, due:12, late:0,
      today:[["Morning huddle on 6 wards",1],["Clear 3 summaries stuck at sign-off",1],["Go through missed evening flags with Arjun","5 PM"]],
      next:[["Wheelchair booked at sign-off goes live","19 Oct"],["Wards 4 and 7 brought onto evening flags","24 Oct"],["First monthly review with the COO","2 Nov"],["Pharmacy-returns rule handed to the wards","9 Nov"]] },
    { key:"sanjay", name:"Sanjay Mohanty", role:"IT integration lead", from:"Hospital IT", done:4, due:9, late:2,
      today:[["Imaging vendor call","late 9 days"],["Match stores item codes","due today"],["Fix tablet lock settings",1]],
      impact:"Imaging link 9 days late: ₹3.6 lakh of benefit pushed back, break-even 3 weeks later, plus ₹2.5 lakh unplanned vendor fee.",
      next:[["Theatre register switched on","19 Oct"],["Imaging reports read from PDF meanwhile","20 Oct"],["Imaging link live","28 Oct"],["Stores link live","30 Oct"],["Security sign-off for phone access","5 Nov"]] },
    { key:"mishra", name:"Dr. Anup Mishra", role:"Medical Superintendent, doctor lead", from:"Hospital", done:3, due:5, late:1,
      today:[["Orthopaedics and cardiology onboarding","late 6 days"],["Sign-off test on phone with 3 doctors",1]],
      impact:"Evening flags 4 points under plan: about 3 bed-days a week lost, roughly ₹0.9 lakh a month.",
      next:[["Phone sign-off live for all doctors","15 Oct"],["Doctor lead named in each department","26 Oct"],["Night-before test ordering rule","26 Oct"]] },
    { key:"lipika", name:"Sister Lipika Behera", role:"Nursing in-charge", from:"Hospital", done:7, due:7, late:0,
      today:[["Check yesterday's captured notes on 4 wards",1],["Brief night nurses on the drug-balance test",1]],
      next:[["Count only flagged items","20 Oct"],["Drug balance goes live","22 Oct"],["Night-shift refresher","3 Nov"]] },
    { key:"priya", name:"Priya Nayak", role:"Discharge Executive, mornings", from:"New role we recommended · joined 8 Sep", done:14, due:15, late:0,
      today:[["Take 11 summaries to doctors for sign-off",1],["Family messages for 9 discharges","in progress"]],
      next:[["Family message on sign-off goes live","15 Oct"],["Hand-over sheet with Arjun","17 Oct"],["Train the relief executive","31 Oct"]] },
    { key:"arjun", name:"Arjun Patra", role:"Discharge Executive, evenings", from:"New role we recommended · joined 8 Sep", done:10, due:13, late:1,
      today:[["Chase 6 unflagged likely discharges","8 PM"],["Provisional summaries to insurance desk","9 PM"]],
      impact:"3 evening follow-ups missed last week: 2 discharges slipped past 1 PM.",
      next:[["Same-night insurance send, by hand","14 Oct"],["Evening checklist on the phone","21 Oct"],["Weekly flag count to Ritika","every Friday"]] },
    { key:"manoj", name:"Manoj Sahu", role:"Billing head", from:"Hospital", done:2, due:4, late:2,
      today:[["Sign off the charge list for the running bill","late 5 days"],["Name a billing tester","due today"]],
      impact:"Charge list 5 days late: holds up the Billing & Insurance start, so decision-to-exit stays about 50 min over plan.",
      next:[["Charge list signed off","16 Oct"],["Billing tester named","16 Oct"],["Billing & Insurance kick-off","2 Nov"]] },
    { key:"kavya", name:"Kavya Iyer", role:"Virevo project lead", from:"Virevo", done:6, due:6, late:0,
      today:[["Weekly report to the COO",1],["Plan the early Billing & Insurance start",1]],
      next:[["7 PM reminder live","16 Oct"],["Reasons section starts","2 Nov"],["Six-week review","16 Nov"]] }
  ],

  /* Money in ₹ lakh */
  months: ["Aug","Sep","Oct"],
  spend: [
    { cat:"Subscription", v:[2.4,2.4,2.4] },
    { cat:"Salaries of roles we recommended", v:[0,0.92,0.92], note:"Discharge Manager ₹4.25 lakh a year; two Discharge Executives ₹3.25 lakh a year each" },
    { cat:"One-time costs", v:[4.8,0.9,2.5], note:"Aug: doctors' tablets · Sep: voice headsets · Oct: imaging vendor fee (not in plan)" }
  ],
  revenue: [0.9,5.1,8.6], ebitda:[0.4,2.3,3.9],
  runRate: { revenue:14, ebitda:6.3 },
  cumMonths:["Aug","Sep","Oct","Nov","Dec","Jan","Feb","Mar","Apr","May"],
  cumSpend:[7.2,11.4,17.2,20.6,24.0,27.4,30.8,34.2,37.6,41.0],
  cumPlan:[0.5,3.0,7.5,13.0,19.5,27.5,36.0,44.5,53.0,61.5],
  cumFore:[0.4,2.7,6.6,11.4,17.0,23.6,31.2,39.6,48.4,57.2],
  actualTo:2, /* index of last actual month */
  breakeven:{ plan:"Jan 2027", fore:"Feb 2027", late:"about 4 weeks" },
  healthFactors:[["Imaging link 9 days late, and its unplanned ₹2.5 lakh fee",45],["Bill still made by hand, so the hours saved stop at billing",35],["Evening flags behind plan in orthopaedics and cardiology",20]],
  healthFixes:[["Ask the imaging vendor to credit its fee against next year's support","kavya","31 Oct"],["Start the running-bill feed early","kavya","2 Nov"],["Doctor leads in the two lagging departments","mishra","26 Oct"]],

  watch: [
    { t:"Imaging link 9 days late", who:"sanjay", ref:"part:3" },
    { t:"Cash patients out by 10 AM: 13 points under plan", who:"mishra", ref:"kpi:K6" },
    { t:"Charge list sign-off 5 days late", who:"manoj", ref:"per:manoj" }
  ],
  resources: [
    ["Project plan and milestones","PDF · 4 Aug"],["Discharge process flow approved by the COO","PDF · 2 Sep"],
    ["Link specifications for each system","6 files · updated 10 Oct"],["Doctor training: flagging and signing by voice","4 short videos"],
    ["Weekly review notes","9 notes · latest 9 Oct"],["Subscription agreement and invoices","3 files"]
  ]
};

/* ===== helpers ===== */
const P = Object.fromEntries(D.people.map(p => [p.key, p]));
const KP = Object.fromEntries(D.kpis.map(k => [k.id, k]));
function prog(k, v){ return Math.max(0, Math.min(1.15, (v - k.base) / (k.target - k.base))); }
function kstate(k){ const d = prog(k,k.now) - prog(k,k.plan); return d >= 0 ? "ahead" : d > -0.1 ? "watch" : "off"; }
D.kpis.forEach(k => k.state = kstate(k));
function fmtv(k, v){ if (k.unit === "%") return v + "%"; const h = Math.floor(v/60), m = v%60; return h ? (m ? `${h} h ${m} min` : `${h} h`) : `${m} min`; }
function gapText(k){ const g = Math.abs(k.now - k.plan); if (k.state === "ahead") return k.unit==="%" ? `${g} points ahead of plan` : `${fmtv(k,g)} better than plan`; return k.unit==="%" ? `${g} points under plan` : `${fmtv(k,g)} over plan`; }
const STATE_WORD = { ahead:"On track", watch:"Slightly behind", off:"Off track" };
const PART_WORD = { live:"Live", testing:"Testing", building:"Being built", blocked:"Late", notstarted:"Not started" };
function pstate(p){ const r = p.done / p.due; return p.late >= 2 || r < 0.6 ? "off" : p.late ? "watch" : "ahead"; }
D.people.forEach(p => p.state = pstate(p));
const PERSON_WORD = { ahead:"Doing well", watch:"Slipping", off:"Lagging" };
const countParts = s => D.parts.filter(p => p.st === s).length;
const L = v => "₹" + (Math.round(v*10)/10).toLocaleString("en-IN") + " lakh";
const sum = a => a.reduce((x,y)=>x+y,0);
const spendTotal = Math.round(sum(D.spend.map(s=>sum(s.v)))*100)/100;
const ebitdaTotal = sum(D.ebitda), revTotal = sum(D.revenue);
const onCourse = D.kpis.filter(k=>k.state!=="off").length;
const esc = s => String(s).replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const initials = n => n.replace(/^(Dr\.|Sister)\s+/,"").split(" ").map(w=>w[0]).join("").slice(0,2);
