/* ===== Page 2 · Targets: what each item is today, what Tojo thinks is realistic in 12 months, and best practice =====
   d: +1 when higher is better, -1 when lower is better. Example figures for the sample hospital.
   same: the item is set once, under the name given (a KPI or a lever), so it is not repeated. */
const TGT = {
  /* outcomes (the KPIs) */
  EBITDA:{t:8.0,r:11.0,b:13.5,u:"%",d:1,dp:1}, REV:{t:612,r:665,b:720,u:"₹ L/month",d:1}, ARPOB:{t:3110,r:3600,b:4500,u:"₹/bed-day",d:1},
  LOS:{t:5.3,r:4.6,b:3.7,u:"days",d:-1,dp:1}, OCC:{t:73.4,r:80,b:85,u:"%",d:1,dp:1}, OTU:{t:58,r:68,b:76,u:"%",d:1},
  RECV:{t:81,r:58,b:40,u:"days",d:-1}, DRUG:{t:23.8,r:20.5,b:17.5,u:"%",d:-1,dp:1}, AGENCY:{t:29.4,r:16,b:8,u:"₹ L/month",d:-1,dp:1},
  /* measures */
  occ:{same:"OCC"}, los:{same:"LOS"}, turn:{t:15.1,r:9,b:6.5,u:"hours",d:-1,dp:1}, dclag:{t:2.1,r:1,b:0.5,u:"hours",d:-1,dp:1}, round:{same:"L:round8"},
  agency:{t:56,r:30,b:15,u:"% of shifts",d:-1}, agcost:{same:"AGENCY"}, vac:{t:16,r:6,b:0,u:"posts",d:-1}, leave:{t:12,r:8,b:4,u:"a year",d:-1}, ratio:{t:7.5,r:6,b:5,u:"patients",d:-1,dp:1},
  otuse:{same:"OTU"}, otcan:{t:17.3,r:9,b:5,u:"%",d:-1,dp:1}, cssd:{t:90,r:65,b:50,u:"minutes",d:-1}, otrev:{t:98,r:115,b:130,u:"₹ L/month",d:1}, first:{t:64,r:35,b:15,u:"% of days",d:-1},
  icul:{t:5.8,r:4.8,b:3.9,u:"days",d:-1,dp:1}, overflow:{t:11,r:5,b:2,u:"% of ICU beds",d:-1}, vent:{t:55,r:70,b:80,u:"% in use",d:1}, step:{t:18,r:8,b:4,u:"hours",d:-1},
  mach:{t:60,r:72,b:82,u:"% in use",d:1}, leak:{t:28,r:15,b:8,u:"% sent out",d:-1}, rtat:{t:4.2,r:2.5,b:1.5,u:"hours",d:-1,dp:1}, pm:{t:36,r:70,b:90,u:"% on time",d:1}, down:{t:46,r:20,b:8,u:"hours/month",d:-1},
  dcost:{same:"DRUG"}, gen:{t:0,r:50,b:80,u:"%",d:1}, stock:{t:22,r:10,b:3,u:"a month",d:-1}, prn:{t:2.3,r:1.6,b:1.0,u:"× own nurses",d:-1,dp:1},
  arpob:{same:"ARPOB"}, sublag:{t:11.9,r:6,b:3,u:"days",d:-1,dp:1}, instat:{t:38,r:28,b:20,u:"days",d:-1}, recv:{same:"RECV"}, preauth:{t:5.5,r:3,b:1.5,u:"hours",d:-1,dp:1},
  conv:{t:16.8,r:19,b:22,u:"%",d:1,dp:1}, mix:{t:8,r:11,b:15,u:"% cardiology",d:1}, ref:{t:64,r:80,b:100,u:"a month",d:1}, mkt:{t:2100,r:1700,b:1300,u:"₹/admission",d:-1}, follow:{t:0,r:60,b:90,u:"% called back",d:1},
  clean:{t:132,r:90,b:60,u:"minutes",d:-1}, hkstaff:{same:"L:hk"}, linen:{t:4.2,r:2,b:1,u:"hours",d:-1,dp:1}, util:{t:410,r:370,b:330,u:"₹/bed-day",d:-1},
  ebitda:{same:"EBITDA"}, readm:{t:5.3,r:4,b:3,u:"%",d:-1,dp:1}, inf:{t:4.1,r:2.8,b:1.5,u:"per 1,000 days",d:-1,dp:1}, sat:{t:3.8,r:4.2,b:4.6,u:"out of 5",d:1,dp:1}, set:{none:true}
};

/* levers: what the hospital can change. k: people, kit (equipment and beds), way (ways of working), auto (Virevo automation suites).
   m: the measures each one moves, with the reference weight. */
const LEVERS = [
  {id:"icunurse", k:"people", n:"Permanent ICU nurses", t:12, r:16, b:20, u:"nurses", m:[["agency",.9],["prn",.4],["AGENCY",.7]]},
  {id:"wardnurse", k:"people", n:"Permanent ward and theatre nurses", t:24, r:30, b:36, u:"nurses", m:[["ratio",.6],["otcan",.2],["AGENCY",.4]]},
  {id:"dccoord", k:"people", n:"Discharge coordinators", t:0, r:1, b:2, u:"people", m:[["dclag",.65],["turn",.4]]},
  {id:"hk", k:"people", n:"Housekeepers on the morning shift", t:18, r:22, b:26, u:"people", m:[["clean",.55],["turn",.48]]},
  {id:"billexec", k:"people", n:"Billing and TPA executives", t:3, r:5, b:6, u:"people", m:[["sublag",.86],["RECV",.5]]},
  {id:"preauthstaff", k:"people", n:"Pre-approval desk staff", t:0.5, r:1.5, b:2, u:"people", dp:1, m:[["preauth",.8],["instat",.5]]},
  {id:"biomed", k:"people", n:"Biomedical engineers", t:1.5, r:2.5, b:3.5, u:"people", dp:1, m:[["pm",.9],["down",.6]]},
  {id:"coun", k:"people", n:"Admission counsellors", t:4, r:5, b:6, u:"people", m:[["conv",.8],["follow",.6]]},
  {id:"cssdtech", k:"people", n:"CSSD technicians, morning", t:2, r:3, b:4, u:"people", m:[["cssd",.75]]},
  {id:"icubeds", k:"kit", n:"ICU beds open", t:12, r:14, b:15, u:"beds", m:[["overflow",.78],["icul",.4]]},
  {id:"ventk", k:"kit", n:"Ventilators", t:2, r:4, b:6, u:"units", m:[["vent",.6],["ARPOB",.3]]},
  {id:"autoclave", k:"kit", n:"Autoclaves", t:2, r:3, b:3, u:"units", m:[["cssd",.6]]},
  {id:"carm", k:"kit", n:"C-arms", t:1, r:2, b:2, u:"units", m:[["otcan",.3]]},
  {id:"lap", k:"kit", n:"Laparoscopy towers", t:1, r:2, b:2, u:"units", m:[["otcan",.3],["OTU",.2]]},
  {id:"echo", k:"kit", n:"Echo machines", t:1, r:2, b:2, u:"units", m:[["mix",.5]]},
  {id:"usg", k:"kit", n:"Ultrasound machines", t:2, r:3, b:3, u:"units", m:[["leak",.3],["mach",.3]]},
  {id:"mri", k:"kit", n:"Own MRI", t:0, r:0, b:1, u:"switch", m:[["leak",.6],["mix",.5]]},
  {id:"round8", k:"way", n:"Ward rounds start by", t:10.5, r:9, b:8, u:"time", d:-1, dp:2, m:[["round",1],["dclag",.4]]},
  {id:"generic", k:"way", n:"Generic formulary in use", t:0, r:1, b:1, u:"switch", m:[["gen",.8],["DRUG",.5]]},
  {id:"incentive", k:"way", n:"Counsellors paid on margin, not volume", t:0, r:1, b:1, u:"switch", m:[["mix",.7]]},
  {id:"implant", k:"way", n:"Framework price contract for implants", t:0, r:1, b:1, u:"switch", m:[["EBITDA",.3]]},
  {id:"icupar", k:"way", n:"ICU drug stock kept", t:3.5, r:5, b:7, u:"days", dp:1, m:[["stock",.7],["prn",.5]]},
  {id:"linenpar", k:"way", n:"Linen stock kept", t:2.5, r:4, b:5, u:"days", dp:1, m:[["linen",.8],["clean",.3]]},
  {id:"s_dis", k:"auto", n:"Discharge Summary suite", t:0, r:1, b:1, u:"switch", go:3, c:"#2F7FD8", m:[["dclag",.7],["sublag",.3]]},
  {id:"s_bill", k:"auto", n:"Billing & Insurance suite", t:0, r:1, b:1, u:"switch", go:5, c:"#C99A1A", m:[["sublag",.6],["instat",.4],["RECV",.4]]},
  {id:"s_adm", k:"auto", n:"Admission Process suite", t:0, r:0, b:1, u:"switch", go:6, c:"#4B3FA8", m:[["preauth",.5],["OCC",.3],["turn",.3]]},
  {id:"s_diag", k:"auto", n:"Diagnostic Scheduling suite", t:0, r:0, b:1, u:"switch", go:6, c:"#B0306E", m:[["rtat",.5],["leak",.5],["mach",.3]]},
  {id:"s_proc", k:"auto", n:"Procurement suite", t:0, r:1, b:1, u:"switch", go:4, c:"#14857A", m:[["stock",.5],["DRUG",.3]]}
];
const KIND = { people:["People","Hire or move staff"], kit:["Beds and equipment","Open, buy or upgrade"], way:["Ways of working","Change how things are done"], auto:["Automations","Virevo suites that do the work"] };

/* the example user: two targets typed in already, so the page opens in a working state */
const EXAMPLE_SET = { EBITDA:13.5, icunurse:20, OTU:72 };
