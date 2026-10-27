/* ===== Example data: Financial Health suite, 250-bed hospital, Bhubaneswar. All figures are examples.
   The suite watches the hospital's money every day: EBITDA, gross revenue, OPD, diagnostic and IP revenue, plus two
   measures the user picks (financial or operational). Each morning's close is checked against what was expected for the
   day and since the start of the project; when a measure is out of range, the suite traces it to its causes, does what
   it is allowed to do, advises the owner, and asks the CEO to confirm anything that costs money or changes policy.
   Causes link to the other suites (Diagnostic Scheduling, Discharge Summary, Billing & Insurance, Procurement, Admission). ===== */
if (typeof SUITES==="undefined") var SUITES = [];
SUITES.push({ key:"financial", data:{
  fh: true,
  suite: "Financial Health",
  family: "Hospital finance",
  hospital: "250-bed hospital, Bhubaneswar",
  started: "1 Sep 2026", week: 8, weeksPlanned: 26, asOf: "24 Oct 2026, 6:10 AM (daily close)",
  dayLabel: "23 Oct", sinceLabel: "since 1 Sep", dayNo: 53,
  recoverLine:"If the three decisions are confirmed this week, break-even comes back to November.",
  aheadRisk:"The risk to watch is the MRI 2 console: if the repair slips again, diagnostic revenue drags EBITDA down again.",
  tabs: [["overview","Overview"],["links","Integrations"],["measures","KPIs"],["recovery","Recovery"],["team","Taskboards"],["health","Project Status"],["files","Resources"],["chat","Chat"]],
  chat:{ sub:"Financial Health suite · 250-bed hospital, Bhubaneswar",
    msg:["Yesterday closed at ₹9.1 lakh EBITDA against ₹10.4 lakh expected for the day. Since 1 September we are at ₹471 lakh against ₹512 lakh expected, 8% short.","Three things explain most of it: implants bought above the agreed price, MRI 2 down since 18 October, and late discharges on Wards 4 and 7. I have already acted on four items. Three decisions are waiting for you.","Pick a point to add to it, or choose what to do next."],
    note:"Confirm the mobile MRI today. It pays for itself in five days.",
    points:["EBITDA 8% behind since 1 September","Diagnostic revenue down while MRI 2 is out","Three decisions waiting for the CEO","Break-even moving to December"],
    asks:["What happens if I approve all three decisions?","Which department lost the most this month?","Why is OPD revenue ahead when diagnostics are behind?"] },
  milestone: { what: "CEO decision desk on the phone goes live", date: "28 Oct", days: 4, part: 11 },
  today: { gross: 62.8, grossExp: 63.5, ebitda: 9.1, ebitdaExp: 10.4, out: 3, actions: 10 },

  /* grp: rev (revenue feeds), cost, cash, brain (the suite itself), out (what it sends) */
  parts: [
    { id:1,  short:"Bills and revenue", name:"Bills and revenue, every service", src:"Hospital software (HIS) billing", grp:"rev", st:"live", when:"Live since 8 Sep", fresh:"closed 6:00 AM", owner:"manoj", vol:"about 2,900 bill lines a day", note:"Reads every bill line by department, doctor and payer, so revenue is known by the morning, not at month end." },
    { id:2,  short:"General ledger costs", name:"Costs from the general ledger", src:"ERP general ledger", grp:"cost", st:"live", when:"Live since 12 Sep", fresh:"closed 6:00 AM", owner:"meera", vol:"about 600 entries a day", note:"Reads daily costs by head, with month-end items spread across the month so the daily EBITDA is fair." },
    { id:3,  short:"Bed census", name:"Bed census, admissions and discharges", src:"HIS admission, transfer and discharge", grp:"rev", st:"live", when:"Live since 8 Sep", fresh:"2 min ago", owner:"sanjay", vol:"about 230 beds", note:"Occupancy, length of stay and discharge times, bed by bed." },
    { id:4,  short:"OPD and prescriptions", name:"OPD registrations and prescriptions", src:"OPD records, with the Diagnostic Scheduling suite", grp:"rev", st:"live", when:"Live since 15 Sep", fresh:"5 min ago", owner:"sunil", vol:"about 520 patients a day", note:"Footfall by doctor, new and returning, and what was prescribed against what was done here." },
    { id:5,  short:"Lab, imaging, pharmacy", name:"Lab, imaging and pharmacy sales", src:"Lab system, imaging consoles, pharmacy", grp:"rev", st:"live", when:"Live since 22 Sep", fresh:"10 min ago", owner:"sanjay", vol:"about 1,100 tests a day", note:"Test and pharmacy revenue by room and unit; MRI 2 read through the Diagnostic Scheduling suite's sheet until its console opens." },
    { id:6,  short:"Payroll and overtime", name:"Payroll, rosters and overtime", src:"Payroll and nursing rosters", grp:"cost", st:"testing", when:"Goes live 30 Oct", fresh:"test, yesterday's roster", owner:"meera", vol:"about 640 staff", note:"Daily manpower cost, with overtime by ward, so a costly roster shows the next morning." },
    { id:7,  short:"Supplier bills", name:"Purchases and supplier bills", src:"Procurement suite", grp:"cost", st:"testing", when:"Goes live 28 Oct", fresh:"test feed, 6:00 AM", owner:"meera", vol:"about 90 bills a day", note:"Consumable and implant costs, with bills above the agreed price flagged by the Procurement suite." },
    { id:8,  short:"Bank and collections", name:"Bank statements and collections", src:"Two banks' statement feeds", grp:"cash", st:"blocked", when:"9 days late · now 4 Nov", fresh:"weekly upload by hand", owner:"sanjay", vol:"about 180 receipts a day",
      note:"Matches money received to bills, so collection days and cash in hand are known every morning.",
      delay:"The main bank has not approved the statement feed; its approval form is with the bank's branch since 15 Oct. Until it opens, collections are uploaded by hand once a week, so collection days are measured weekly and cash in hand can be up to six days old.",
      fixes:[["Upload both banks' statements by hand every morning instead of weekly","ipsita","25 Oct"],["CFO to call the bank's regional head","meera","27 Oct"],["Statement feed live","sanjay","4 Nov"]] },
    { id:9,  short:"Insurer claims", name:"Insurer claims and approvals", src:"Insurer portals, with the Billing & Insurance suite", grp:"cash", st:"building", when:"Due 9 Nov", fresh:"2 of 6 insurers", owner:"manoj", vol:"about 40 claims a day", note:"Claims raised, approved, queried and paid, so money stuck with insurers is visible by payer." },
    { id:10, short:"Expected value each day", name:"Expected value for every day", src:"Two years of history, budget and season", grp:"brain", st:"live", when:"Live since 18 Sep", fresh:"set for 24 Oct", owner:"ipsita", vol:"7 measures × every day", note:"Sets what each measure should be each day, allowing for weekday, season and festivals, so a quiet Sunday is not read as a loss." },
    { id:11, short:"CEO decision desk", name:"CEO decision desk on the phone", src:"CEO's phone", grp:"out", st:"testing", when:"Goes live 28 Oct", fresh:"test, 2 decisions", owner:"kavya", vol:"about 3 decisions a day", note:"Anything that costs money or changes a policy comes to the CEO to confirm with one tap, with the expected gain and cost." },
    { id:12, short:"Doctor and payer profit", name:"Doctor-wise and payer-wise profit", src:"Bills, costs and claims together", grp:"out", st:"notstarted", when:"Starts 16 Nov", fresh:"not started", owner:"ipsita", vol:"—", note:"Profit by doctor, department and payer each month, for the pricing and package talks." }
  ],
  handoffs: [
    { name:"MRI 2 console repair, from the Diagnostic Scheduling suite", to:"Diagnostic Scheduling", st:"blocked", when:"Repair due 27 Oct" },
    { name:"Implant bills above the agreed price, from the Procurement suite", to:"Procurement", st:"testing", when:"Feed live 28 Oct" }
  ],

  /* Measures. Values per day in ₹ lakh unless the unit says otherwise. day: [expected, actual] for the last closed day.
     td: since 1 Sep, [expected, actual]: a total for money, an average for rates. base: daily before the project; target: at full run. */
  core: ["K1","K2","K3","K4","K5"],
  chosen: ["K6","K7"],
  pool: [
    { id:"K1", name:"EBITDA", short:"EBITDA", unit:"L", dir:"up", base:8.6, target:12.5, day:[10.4,9.1], td:[512,471], tdKind:"total" },
    { id:"K2", name:"Gross revenue", short:"Gross revenue", unit:"L", dir:"up", base:58, target:68, day:[63.5,62.8], td:[3330,3262], tdKind:"total" },
    { id:"K3", name:"OPD revenue", short:"OPD revenue", unit:"L", dir:"up", base:3.6, target:4.6, day:[4.1,4.3], td:[214,218], tdKind:"total",
      why:"Cardiology OPD footfall is up 18% since the new consultant joined, and returning patients are booked into the evening session." },
    { id:"K4", name:"Diagnostic revenue", short:"Diagnostic revenue", unit:"L", dir:"up", base:7.2, target:9.6, day:[8.3,7.6], td:[430,401], tdKind:"total" },
    { id:"K5", name:"IP revenue", short:"IP revenue", unit:"L", dir:"up", base:44, target:50.5, day:[47.8,47.3], td:[2540,2496], tdKind:"total" },
    { id:"K6", name:"Average length of stay", short:"ALOS", unit:"d", dir:"down", base:4.6, target:3.9, day:[4.3,4.5], td:[4.4,4.52], tdKind:"average", kind:"Operational" },
    { id:"K7", name:"OP-to-IP conversion", short:"OP-to-IP", unit:"%", dir:"up", base:6.5, target:9, day:[7.8,8.1], td:[7.5,7.6], tdKind:"average", kind:"Operational",
      why:"Cardiology and orthopaedics OPD patients advised admission are now called back by the admissions desk within a day." },
    { id:"K8", name:"Revenue per occupied bed (ARPOB)", short:"ARPOB", unit:"k", dir:"up", base:24.0, target:27.5, day:[25.6,25.1], td:[25.2,24.9], tdKind:"average", kind:"Financial" },
    { id:"K9", name:"Bed occupancy", short:"Occupancy", unit:"%", dir:"up", base:72, target:82, day:[77,79], td:[76,76.8], tdKind:"average", kind:"Operational",
      why:"Admissions called in before the bed is free, from the Admission Process suite, fill beds on the same day." },
    { id:"K10", name:"Collection days", short:"Collection days", unit:"d", dir:"down", base:62, target:45, day:[55,58], td:[57,59], tdKind:"average", kind:"Financial" },
    { id:"K11", name:"Claims denied by insurers", short:"Claim denials", unit:"%", dir:"down", base:7.5, target:3, day:[5.8,6.1], td:[6.2,6.3], tdKind:"average", kind:"Financial" },
    { id:"K12", name:"Manpower cost to revenue", short:"Manpower cost", unit:"%", dir:"down", base:31, target:27, day:[29.5,30.6], td:[29.8,30.4], tdKind:"average", kind:"Financial" },
    { id:"K13", name:"Operation theatre use", short:"OT use", unit:"%", dir:"up", base:58, target:75, day:[66,68], td:[64,65], tdKind:"average", kind:"Operational",
      why:"Elective lists are now booked into the morning gaps the theatre register shows each evening." }
  ],

  /* Causes: what pushed the measures off. e: effect on yesterday's EBITDA (₹ lakh); etd: effect since 1 Sep. */
  drivers: [
    { id:"D1", name:"MRI 2 out of service since 18 Oct", kpis:["K4","K2","K1","K8"], e:-0.45, etd:-3.2, src:"Diagnostic Scheduling suite", owner:"sanjay", since:"18 Oct",
      note:"The console fault takes out about 22 scans a day. Walk-in MRI patients are sent elsewhere at peak; about ₹0.55 lakh of revenue a day is lost." },
    { id:"D2", name:"OPD tests done outside the hospital", kpis:["K4","K2","K1"], e:-0.20, etd:-10.5, src:"Diagnostic Scheduling suite", owner:"sunil", since:"before the project",
      note:"62% of tests prescribed to returning patients are still done elsewhere, about ₹0.35 lakh of revenue a day above plan." },
    { id:"D3", name:"Discharges after 1 PM on Wards 4 and 7", kpis:["K6","K5","K1","K8"], e:-0.25, etd:-9.8, src:"Discharge Summary suite", owner:"mishra", since:"since 1 Sep",
      note:"Two wards still discharge in the afternoon, holding about 6 bed-days a day that the next admissions could have used." },
    { id:"D4", name:"Implants bought above the agreed price", kpis:["K1"], e:-0.45, etd:-12.0, src:"Procurement suite", owner:"meera", since:"since 1 Sep",
      note:"Orthopaedic and cardiac implants from two suppliers are billed about 9% above the agreed rates." },
    { id:"D5", name:"Nursing overtime on Wards 4 and 7", kpis:["K1","K12"], e:-0.30, etd:-8.4, src:"Payroll and rosters", owner:"meera", since:"since 10 Sep",
      note:"Evening shifts short by four nurses are covered by overtime at 1.5 times the rate." },
    { id:"D6", name:"Insurer approvals taking over 4 hours", kpis:["K5","K6","K10","K11"], e:-0.10, etd:-4.6, src:"Billing & Insurance suite", owner:"manoj", since:"since 1 Sep",
      note:"Insured patients wait for the final approval, so beds and collections are both held up." },
    { id:"D7", name:"Cardiology OPD footfall up 18%", kpis:["K3","K7","K2","K1"], e:0.45, etd:7.5, src:"OPD records", owner:"sunil", since:"since 1 Oct", lift:true,
      note:"The new cardiology consultant's clinic is full by 11 AM; more patients are advised admission and tests." },
    { id:"D8", name:"Bank statements uploaded weekly by hand", kpis:["K10"], e:0, etd:0, src:"Bank statements feed", owner:"sanjay", since:"since 1 Sep",
      note:"Collection days can only be measured weekly until the bank opens the statement feed." }
  ],

  /* What the suite did, advised and is waiting on. st: done (done by the automation), advised (sent to an owner), awaiting (needs the CEO). gain: ₹ lakh a day. */
  actions: [
    { id:"A1", st:"done", t:"Moved 14 evening MRI 1 slots to OPD patients who were waiting for MRI 2", drv:["D1"], gain:0.18, when:"23 Oct, 6:20 AM", who:"sanjay",
      note:"Within the slot rules it may change on its own. Patients got their new time by message; 11 of 14 confirmed." },
    { id:"A2", st:"done", t:"Reminded 38 OPD patients of the tests prescribed yesterday, with a slot here today", drv:["D2"], gain:0.08, when:"24 Oct, 6:15 AM", who:"sunil",
      note:"Sent through the Diagnostic Scheduling suite's patient guide." },
    { id:"A3", st:"done", t:"Held payment on 9 implant bills above the agreed price and sent them to the buyer", drv:["D4"], gain:0.30, when:"23 Oct, 6:25 AM", who:"meera",
      note:"₹2.7 lakh of payments held until the supplier corrects the rate. The CFO is copied." },
    { id:"A4", st:"done", t:"Escalated 6 insurer approvals waiting over 4 hours", drv:["D6"], gain:0.06, when:"24 Oct, 6:12 AM", who:"manoj",
      note:"Sent to each insurer's escalation desk with the discharge summary attached." },
    { id:"A5", st:"advised", t:"Open an evening cardiology OPD on Tuesdays and Thursdays", drv:["D7"], gain:0.25, when:"Advised 21 Oct", who:"sunil", reply:"No reply yet · 3 days",
      note:"The morning clinic turns away about 14 patients a day. An evening session would keep them, and their tests, here." },
    { id:"A6", st:"advised", t:"Hold an 11 AM discharge huddle on Wards 4 and 7", drv:["D3"], gain:0.20, when:"Advised 21 Oct", who:"mishra", reply:"Agreed · starts 27 Oct",
      note:"The two wards that still discharge late. Each bed freed by noon is used by the evening admission." },
    { id:"A7", st:"advised", t:"Upload both banks' statements every morning until the feed opens", drv:["D8"], gain:0, when:"Advised 23 Oct", who:"ipsita", reply:"Agreed · from 25 Oct",
      note:"So collection days are measured daily, not weekly." },
    { id:"A8", ceo:0, st:"awaiting", t:"Rent a mobile MRI for 10 days until the MRI 2 console is repaired", drv:["D1"], gain:0.45, cost:"₹2.4 lakh for 10 days", net:"+₹2.1 lakh over 10 days; pays for itself in about 5 days", when:"Raised 23 Oct, 6:15 AM", wait:"Waiting 1 day",
      note:"Two vendors can place a van at the back gate within 48 hours. Walk-in MRI patients stay here instead of being sent away." },
    { id:"A9", ceo:1, st:"awaiting", t:"Move 4 nurses from day to evening shift on Wards 4 and 7, instead of paying overtime", drv:["D5"], gain:0.22, cost:"No extra cost", net:"+₹6.6 lakh a month", when:"Raised 23 Oct, 6:18 AM", wait:"Waiting 1 day",
      note:"The day shift on these wards is over-staffed by four against the patient load; the nursing in-charge has seen the roster." },
    { id:"A10", ceo:2, st:"awaiting", t:"Offer 10% off afternoon CT and ultrasound for 30 days", drv:["D2"], gain:0.15, cost:"About ₹0.04 lakh a day of discount", net:"+₹3.3 lakh over 30 days", when:"Raised 24 Oct, 6:20 AM", wait:"New today",
      note:"Afternoon slots run 40% empty. Returning OPD patients who now go elsewhere for price would stay." }
  ],
  runLog: [
    ["6:00 AM","Yesterday's close read from all six live feeds"],
    ["6:05 AM","7 measures checked against the day and against the total since 1 Sep"],
    ["6:08 AM","3 out of range: EBITDA, diagnostic revenue, length of stay"],
    ["6:10 AM","Traced to 6 causes; 1 cause lifting revenue"],
    ["6:20 AM","2 actions done within its rules, 1 advised, 1 decision sent to the CEO"],
    ["8:30 AM","Morning brief sent to the CEO and CFO"]
  ],

  people: [
    { key:"anil", name:"Anil Pattnaik", role:"CEO", from:"Hospital · confirms the suite's decisions", done:3, due:5, late:1,
      today:[["Confirm the mobile MRI","waiting 1 day"],["Confirm the nurse shift change","waiting 1 day"],["Confirm afternoon test prices","new today"],["Read the morning brief",1]],
      impact:"Two decisions waiting a day: about ₹0.67 lakh of EBITDA a day not yet recovered.",
      next:[["Decision desk on the phone","28 Oct"],["Monthly review with the board","2 Nov"],["Package price talks with two insurers","9 Nov"]] },
    { key:"meera", name:"Meera Rath", role:"CFO, suite owner", from:"Hospital", done:6, due:7, late:0,
      today:[["Call the implant supplier on the held bills",1],["Approve the daily cost spread rules","in progress"]],
      next:[["Payroll feed live","30 Oct"],["Bank regional head call","27 Oct"],["Month-end close in 3 days, not 9","5 Nov"]] },
    { key:"sunil", name:"Sunil Jena", role:"COO", from:"Hospital", done:4, due:7, late:2,
      today:[["Reply on the evening cardiology OPD","late 3 days"],["Afternoon CT staffing plan","late 1 day"],["OPD footfall review",1]],
      impact:"Evening cardiology OPD undecided for 3 days: about 14 patients a day turned away, ₹0.25 lakh of revenue a day.",
      next:[["Evening cardiology OPD decision","25 Oct"],["Afternoon test staffing","28 Oct"],["OPD layout change","9 Nov"]] },
    { key:"mishra", name:"Dr. Anup Mishra", role:"Medical Superintendent", from:"Hospital (also on the Discharge Summary suite)", done:4, due:5, late:1,
      today:[["11 AM huddle plan for Wards 4 and 7",1],["Length-of-stay review with orthopaedics","late 2 days"]],
      impact:"Orthopaedics review 2 days late: length of stay stays 0.2 days over plan, about 6 bed-days a day.",
      next:[["11 AM huddle starts","27 Oct"],["Length-of-stay by doctor, monthly","2 Nov"]] },
    { key:"manoj", name:"Manoj Sahu", role:"Billing head", from:"Hospital (also on the Billing & Insurance suite)", done:5, due:6, late:0,
      today:[["Follow up the 6 escalated approvals","in progress"],["Daily revenue check against the close",1]],
      next:[["Two more insurer portals","26 Oct"],["Claims feed live","9 Nov"]] },
    { key:"ipsita", name:"Ipsita Nanda", role:"Financial Health Analyst", from:"New role we recommended · joined 22 Sep", done:12, due:12, late:0,
      today:[["Check the morning close against the bank",1],["Prepare the CEO's decision notes",1],["Set expected values for Diwali week",1]],
      next:[["Daily bank upload starts","25 Oct"],["Festival-week expected values","28 Oct"],["Doctor-wise profit design","16 Nov"]] },
    { key:"sanjay", name:"Sanjay Mohanty", role:"IT integration lead", from:"Hospital IT (shared with five suites)", done:3, due:5, late:1,
      today:[["Bank statement feed form","late 9 days"],["Payroll feed test",1]],
      impact:"Bank feed 9 days late: collection days measured weekly, cash in hand up to six days old.",
      next:[["Payroll feed live","30 Oct"],["Bank feed live","4 Nov"]] },
    { key:"kavya", name:"Kavya Iyer", role:"Virevo project lead", from:"Virevo", done:5, due:5, late:0,
      today:[["CEO decision desk test",1],["Weekly report to the CEO",1]],
      next:[["Decision desk live","28 Oct"],["Eight-week review","2 Nov"]] }
  ],

  months: ["Sep","Oct"],
  spend: [
    { cat:"Subscription", v:[2.5,2.5] },
    { cat:"Salaries of roles we recommended", v:[0.3,0.6], note:"Financial Health Analyst ₹7.2 lakh a year (example)" },
    { cat:"One-time costs", v:[3.0,1.2], note:"Sep: finance data set-up · Oct: CEO decision desk" }
  ],
  revenue: [2.0,9.4], ebitda:[1.2,6.8],
  runRate: { revenue:30, ebitda:14 },
  cumMonths:["Sep","Oct","Nov","Dec","Jan","Feb","Mar","Apr","May","Jun"],
  cumSpend:[5.8,10.1,13.2,16.3,19.4,22.5,25.6,28.7,31.8,34.9],
  cumPlan:[1.5,9.5,20.0,31.0,43.0,55.5,68.0,80.5,93.0,105.5],
  cumFore:[1.2,8.0,12.6,19.5,28.5,39.0,50.5,62.5,74.5,86.5],
  actualTo:1,
  breakeven:{ plan:"Nov 2026", fore:"Dec 2026", late:"about 4 weeks", planIdx:2, foreIdx:3 },
  healthFactors:[["Three CEO decisions waiting, so their gains are not in yet",40],["MRI 2 out of service since 18 Oct",35],["Bank feed late, so cash cannot be managed daily",25]],
  healthFixes:[["CEO decision desk on the phone","kavya","28 Oct"],["Mobile MRI until the repair (awaiting the CEO)","anil","25 Oct"],["Bank statement feed live","sanjay","4 Nov"]],
  watch: [
    { t:"EBITDA since 1 Sep: ₹41 lakh short of expected", who:"meera", ref:"kpi:K1" },
    { t:"Diagnostic revenue down while MRI 2 is out", who:"sanjay", ref:"kpi:K4" },
    { t:"Mobile MRI waiting for the CEO's decision", who:"anil", ref:"act:A8" }
  ],
  resources: [
    ["Project plan and milestones","PDF · 1 Sep"],["How each day's expected value is set","2 pages · 18 Sep"],
    ["What the suite may do on its own, and what needs the CEO","1 page · signed 15 Sep"],["Daily morning briefs","53 briefs · latest today"],
    ["Weekly review notes","7 notes · latest 21 Oct"],["Subscription agreement and invoices","2 files"]
  ]
}});
