/* ===== Example data: Admission Process suite, 250-bed hospital, Bhubaneswar. All figures are examples.
   Content from bed-management.md §7.1 point 4 (five admission stages), §7.3 point 5 (dead bed time, bill to bill),
   §7.4.1 (bed mapping 2 PM / 6 PM, predictive LOS, ICU step-down, discharge linkage, emergency reserve, call-in timing),
   §7.4.2 (OPD prescription intake, 5 PM rounds, desk-console link, stage timestamps), §7.4.4 (Bed Manager, Admissions Executives)
   and discharge-process.md (evening provisional flags, real discharge timings). ===== */
if (typeof SUITES==="undefined") var SUITES = [];
SUITES.push({ key:"admission", data:{
  suite: "Admission Process",
  family: "Bed Management",
  hospital: "250-bed hospital, Bhubaneswar",
  started: "21 Sep 2026", week: 4, weeksPlanned: 20, asOf: "12 Oct 2026, 10:40 AM",
  recoverLine:"If all three land, break-even comes back to December.",
  aheadRisk:"The risk to watch is the 5 PM rounds: if they keep slipping, tomorrow's bed map stops holding.",
  chat:{ sub:"Admission Process suite · 250-bed hospital, Bhubaneswar",
    msg:["Four of the twelve parts are live. A patient now reaches a bed 2 h 8 min after arriving, down from 3 h 20 min and ahead of plan.","Three measures are off track: patients in a bed by noon, dead bed time and the 5 PM rounds. All three come back to the same thing: tomorrow's discharges are not confirmed early enough to call patients in before the bed frees.","Pick a point to add to it, or choose what to do next."],
    note:"Get the 5 PM rounds done every day. Tomorrow's bed map depends on them.",
    points:["The 5 PM Medical Supervisory rounds","Dead bed time, bill to bill","Patient records approval for length-of-stay prediction","Break-even moving to January"],
    asks:["Why are patients still arriving after 2 PM?","Which wards free beds latest?","Can we call patients in before the housekeeping signal is live?"] },
  milestone: { what: "Housekeeping bed-ready signal goes live", date: "17 Oct", days: 5, part: 6 },
  tomorrow: { planned: 46, mapped: 38, unmapped: 8, icuUnmapped: 2, reserve: 6, freeze: "6 PM", firstPass: "2 PM" },
  today: { admitted: 21, avgTat: "2 h 8 min", last: "Bed 214 · 41 min" },
  /* the five admission stages (bed-management.md §7.1 point 4), minutes: before, now, floor */
  stages: [
    { name:"Arrival to start of paperwork", base:35, now:20, floor:2 },
    { name:"Paperwork (documentation)", base:20, now:18, floor:18 },
    { name:"Bed given in the system", base:85, now:46, floor:2 },
    { name:"Ward or ICU confirms bed is ready", base:45, now:30, floor:4 },
    { name:"Patient taken to the bed", base:15, now:14, floor:4 }
  ],

  /* stage: which of the five stages each part speeds up (1–5) */
  parts: [
    { id:1,  name:"OPD prescription captured for planned admissions", src:"OPD records (EMR)", stage:1, st:"live", when:"Live since 28 Sep", fresh:"6 min ago", owner:"biswajit", vol:"about 30 planned admissions a day", note:"Date, procedure, expected stay and theatre need are read from the OPD prescription, so every planned admission enters the map." },
    { id:2,  name:"Tomorrow's bed map, 2 PM and 6 PM", src:"Bed board in the hospital software", stage:3, st:"testing", when:"Goes live 19 Oct", fresh:"test run, 2 PM today", owner:"sunita", vol:"about 46 planned admissions a day", note:"Maps every planned admission to a bed that is free, freeing, or likely to free from patients near their usual stay. First pass by 2 PM, final freeze by 6 PM." },
    { id:3,  name:"Length-of-stay prediction for likely discharges", src:"Inpatient records", stage:3, st:"blocked", when:"12 days late · now 30 Oct", fresh:"no feed yet", owner:"sanjay", vol:"about 215 inpatients",
      note:"Flags patients approaching the usual stay for their treatment, so beds can be mapped before a doctor says the word.",
      delay:"The records committee has not yet approved reading inpatient notes for the prediction. Until it does, the bed map only uses confirmed and evening-flagged discharges, so about 1 in 6 beds that will free tomorrow is missed.",
      fixes:[["Records committee sign-off, with the de-identified data plan attached","kavya","17 Oct"],["Use discharge flags from the Discharge Summary suite meanwhile","sunita","14 Oct"],["Prediction live","sanjay","30 Oct"]] },
    { id:4,  name:"ICU step-down mapping", src:"ICU system", stage:3, st:"building", when:"Due 2 Nov", fresh:"no feed yet", owner:"rashmi", vol:"about 6 step-downs a day", note:"Maps planned procedures against ICU beds, confirmed step-downs and likely step-downs; step-down signals are due by 1 PM." },
    { id:5,  name:"Real discharge timings from the Discharge Summary suite", src:"Discharge Summary suite", stage:3, st:"live", when:"Live since 5 Oct", fresh:"2 min ago", owner:"sunita", vol:"about 42 discharges a day", note:"Uses when beds actually free, not when they are reported to, and checks the two against each other." },
    { id:6,  name:"Housekeeping bed-ready signal", src:"Housekeeping app", stage:4, st:"testing", when:"Goes live 17 Oct", fresh:"test, 3 wards", owner:"prakash", vol:"about 45 turnarounds a day", note:"The housekeeper marks the bed clean on a phone; the ward and the desk see it at once." },
    { id:7,  name:"Call-in time sent to the patient", src:"SMS and phone call", stage:1, st:"notstarted", when:"Starts 26 Oct", fresh:"not started", owner:"biswajit", vol:"—", note:"Works back from when each mapped bed will be free to when its patient should come in, and tells the patient." },
    { id:8,  name:"Emergency bed reserve from past demand", src:"Three years of emergency records", stage:1, st:"notstarted", when:"Starts 9 Nov", fresh:"not started", owner:"sunita", vol:"6 beds held today, by hand", note:"Holds back beds for emergency patients by day of week, month and hour, based on three years of history." },
    { id:9,  name:"Time stamps for all five admission stages", src:"Admission desk (hospital software)", stage:2, st:"live", when:"Live since 21 Sep", fresh:"1 min ago", owner:"biswajit", vol:"about 44 admissions a day", note:"Every admission now records arrival, paperwork, bed given, bed ready and patient in bed." },
    { id:10, name:"Insurer pre-approval started at the desk", src:"Insurer portals, with the Billing & Insurance suite", stage:2, st:"building", when:"Due 9 Nov", fresh:"2 of 6 insurers", owner:"lopamudra", vol:"about 26 insured admissions a day", note:"Shared with the Billing & Insurance suite's pre-approval line." },
    { id:11, name:"Two-way link between the desk and the bed board", src:"Hospital software", stage:3, st:"testing", when:"Goes live 19 Oct", fresh:"test, 1 desk", owner:"sunita", vol:"—", note:"A date confirmed at the desk shows on the bed board at once, with a bed already attached." },
    { id:12, name:"First bill entry when the patient reaches the bed", src:"Billing, with the Billing & Insurance suite", stage:5, st:"live", when:"Live since 21 Sep", fresh:"3 min ago", owner:"lopamudra", vol:"about 44 a day", note:"Opens the bill on arrival at the bed, which ends the dead bed time on that bed." }
  ],
  handoffs: [
    { name:"Real discharge timings and evening flags", to:"Discharge Summary", st:"live", when:"Live since 5 Oct" },
    { name:"Bill opened on arrival", to:"Billing & Insurance", st:"live", when:"Live since 21 Sep" }
  ],

  kpis: [
    { id:"K1", name:"Arrival to patient in bed", short:"Arrival to bed", unit:"min", dir:"down", base:200, target:30, plan:140, now:128,
      why:"Stage time stamps showed the bed was given in the system 46 minutes after paperwork, not 85; the desk now asks the bed board first." },
    { id:"K2", name:"Planned admissions in a bed by 12 noon", short:"In bed by noon", unit:"%", dir:"up", base:9, target:65, plan:25, now:19,
      factors:[["Patients still called for 2 PM by habit",45],["Tomorrow's discharges confirmed too late to call patients earlier",35],["Bed-ready signal not live, so wards wait to confirm",20]],
      fixes:[["Call-in times from the bed map, sent the evening before","biswajit","26 Oct"],["5 PM rounds held every day","mishra","19 Oct"],["Housekeeping bed-ready signal live","prakash","17 Oct"]],
      back:"Back on the plan line by week 8 (9 Nov)" },
    { id:"K3", name:"Planned admissions mapped to a bed by the 6 PM freeze", short:"Mapped by 6 PM", unit:"%", dir:"up", base:0, target:95, plan:50, now:58,
      why:"Evening discharge flags from the Discharge Summary suite feed the map; 38 of tomorrow's 46 are already placed." },
    { id:"K4", name:"2 PM mappings that hold to 6 PM", short:"2 PM holds", unit:"%", dir:"up", base:0, target:85, plan:40, now:34,
      factors:[["Discharges changed after the 5 PM rounds",60],["Length-of-stay prediction not live",40]],
      fixes:[["Rounds moved to finish by 5 PM sharp","mishra","19 Oct"],["Records committee sign-off","kavya","17 Oct"]],
      back:"Back on the plan line by week 7 (2 Nov)" },
    { id:"K5", name:"Dead bed time, bill to bill", short:"Dead bed time", unit:"min", dir:"down", base:570, target:180, plan:450, now:505,
      factors:[["Next patient arrives in the afternoon though the bed frees by noon",55],["Housekeeping turnaround still confirmed by phone",25],["Discharge tail after the bill closes",20]],
      fixes:[["Call-in times from the bed map","biswajit","26 Oct"],["Housekeeping bed-ready signal live","prakash","17 Oct"],["Insurer evening bill from the Billing & Insurance suite","sunita","2 Nov"]],
      back:"Back on the plan line by week 9 (16 Nov)" },
    { id:"K6", name:"Ward discharges flagged 24 hours ahead", short:"Flagged 24 h ahead", unit:"%", dir:"up", base:6, target:80, plan:35, now:31,
      factors:[["Orthopaedics and cardiology not yet flagging by voice",70],["Weekend rounds not covered",30]],
      fixes:[["Doctor leads in the two departments, shared with the Discharge Summary suite","mishra","26 Oct"]],
      back:"Back on the plan line by week 7 (2 Nov)" },
    { id:"K7", name:"Emergency patients waiting over an hour for a bed", short:"Waits over 1 h", unit:"%", dir:"down", base:38, target:5, plan:28, now:26,
      why:"Six beds are held back each day for emergencies, chosen by hand from last month's pattern until the reserve model is ready." },
    { id:"K8", name:"5 PM supervisory rounds done on time", short:"5 PM rounds", unit:"%", dir:"up", base:0, target:95, plan:60, now:44,
      factors:[["Rounds clash with the evening OPD on 3 days a week",65],["No named stand-in when the Medical Superintendent is away",35]],
      fixes:[["Rounds moved to 4:15 PM on OPD days","mishra","19 Oct"],["Deputy named for rounds","mishra","15 Oct"]],
      back:"Back on the plan line by week 6 (26 Oct)" },
    { id:"K9", name:"Desk confirmations shown on the bed board at once", short:"Desk to board", unit:"%", dir:"up", base:0, target:98, plan:50, now:61,
      why:"The two-way link is in test on the main desk, which handles most planned admissions." }
  ],

  people: [
    { key:"sunita", name:"Sunita Mohapatra", role:"Bed Manager", from:"New role we recommended · joined 22 Sep", done:12, due:13, late:0,
      today:[["2 PM bed map for tomorrow","2 PM"],["Hold 6 emergency beds",1],["Agree tomorrow's discharges with Ritika",1]],
      next:[["Bed map goes live","19 Oct"],["Desk-board link goes live","19 Oct"],["Emergency reserve model starts","9 Nov"],["First monthly review with the COO","16 Nov"]] },
    { key:"biswajit", name:"Biswajit Nanda", role:"Admissions desk lead", from:"Hospital", done:9, due:11, late:1,
      today:[["Stop booking 2 PM call-ins by default","late 4 days"],["Check stage time stamps for yesterday",1]],
      impact:"Default 2 PM call-ins: planned patients in a bed by noon stay 6 points under plan, about 9 billable hours lost a day.",
      next:[["Call-in times sent to patients","26 Oct"],["Desk rota split from discharges","19 Oct"],["Second desk on the board link","2 Nov"]] },
    { key:"lopamudra", name:"Lopamudra Swain", role:"Admissions Executive, mornings", from:"New role we recommended · joined 29 Sep", done:14, due:14, late:0,
      today:[["Paperwork for 9 planned admissions before 11 AM","in progress"],["Pre-approval requests for 4 insured patients",1]],
      next:[["Pre-approval at the desk for the two largest insurers","26 Oct"],["Train the evening executive","2 Nov"]] },
    { key:"mishra", name:"Dr. Anup Mishra", role:"Medical Superintendent, runs the 5 PM rounds", from:"Hospital", done:3, due:6, late:2,
      today:[["5 PM rounds of beds likely to free tomorrow","5 PM"],["Name a deputy for rounds","late 6 days"],["Move OPD-day rounds to 4:15 PM","late 3 days"]],
      impact:"Rounds done on time only 44% of days: the 6 PM bed map changes after the freeze and about 4 patients a day are called in late.",
      next:[["Deputy named for rounds","15 Oct"],["Rounds at 4:15 PM on OPD days","19 Oct"],["Doctor leads for 24-hour flags","26 Oct"]] },
    { key:"rashmi", name:"Dr. Rashmi Tripathy", role:"ICU in-charge", from:"Hospital", done:4, due:5, late:1,
      today:[["Step-down list by 1 PM","late 1 day"],["Review ICU mapping test",1]],
      impact:"Step-down list late once this week: 2 planned surgeries waited for an ICU bed.",
      next:[["Step-down list by 1 PM every day","15 Oct"],["ICU step-down mapping live","2 Nov"]] },
    { key:"prakash", name:"Prakash Jena", role:"Housekeeping supervisor", from:"Hospital", done:6, due:7, late:0,
      today:[["Phones issued to 12 housekeepers",1],["Bed-ready test on Wards 3, 5 and 7","in progress"]],
      next:[["Bed-ready signal live on all wards","17 Oct"],["Turnaround under 45 minutes","2 Nov"]] },
    { key:"sanjay", name:"Sanjay Mohanty", role:"IT integration lead", from:"Hospital IT (shared with two other suites)", done:3, due:6, late:1,
      today:[["Records committee papers","late 12 days"],["Desk-board link test",1]],
      impact:"Inpatient records not approved: about 1 in 6 beds that will free tomorrow is missing from the bed map.",
      next:[["Records committee sign-off","17 Oct"],["Length-of-stay prediction live","30 Oct"],["ICU system link","2 Nov"]] },
    { key:"kavya", name:"Kavya Iyer", role:"Virevo project lead", from:"Virevo", done:5, due:5, late:0,
      today:[["Weekly report to the COO",1],["Data plan for the records committee",1]],
      next:[["Records committee meeting","17 Oct"],["Process flow sign-off by the COO for split desk and discharge teams","19 Oct"],["Four-week review","9 Nov"]] }
  ],

  months: ["Sep","Oct"],
  spend: [
    { cat:"Subscription", v:[1.8,1.8] },
    { cat:"Salaries of roles we recommended", v:[0.12,0.62], note:"Bed Manager ₹4.25 lakh a year; one more Admissions Executive ₹3.25 lakh a year" },
    { cat:"One-time costs", v:[0.6,1.4], note:"Sep: patient messaging set-up · Oct: bed board screens for 9 wards" }
  ],
  revenue: [0.4,2.9], ebitda:[0.3,1.9],
  runRate: { revenue:9.5, ebitda:5.8 },
  cumMonths:["Sep","Oct","Nov","Dec","Jan","Feb","Mar","Apr","May","Jun"],
  cumSpend:[2.52,6.34,8.76,11.18,13.6,16.02,18.44,20.86,23.28,25.7],
  cumPlan:[0.5,3.0,6.8,11.4,16.6,22.4,28.6,35.0,41.6,48.4],
  cumFore:[0.3,2.2,5.3,9.3,13.9,19.0,24.5,30.2,36.1,42.0],
  actualTo:1,
  breakeven:{ plan:"Dec 2026", fore:"Jan 2027", late:"about 4 weeks", planIdx:3, foreIdx:4 },
  healthFactors:[["Length-of-stay prediction held up by the records committee",40],["5 PM rounds done on time only 44% of days",35],["Patients still called for 2 PM by habit",25]],
  healthFixes:[["Records committee sign-off with the data plan","kavya","17 Oct"],["Deputy named and OPD-day rounds moved","mishra","19 Oct"],["Call-in times sent from the bed map","biswajit","26 Oct"]],
  watch: [
    { t:"Patient records approval 12 days late", who:"sanjay", ref:"part:3" },
    { t:"Dead bed time: 55 min over plan", who:"sunita", ref:"kpi:K5" },
    { t:"5 PM rounds on time only 44% of days", who:"mishra", ref:"kpi:K8" }
  ],
  resources: [
    ["Project plan and milestones","PDF · 21 Sep"],["Admission process flow for COO sign-off","Draft 3 · 9 Oct"],
    ["Bed map rules: 2 PM pass and 6 PM freeze","2 pages"],["Five-stage time stamp definitions","1 page"],
    ["Weekly review notes","3 notes · latest 9 Oct"],["Subscription agreement and invoices","2 files"]
  ]
}});
