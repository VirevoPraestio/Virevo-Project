/* ===== Example data: Procurement suite, 250-bed hospital, Bhubaneswar. All figures are examples.
   No domain reference file exists yet for supply chain and procurement. Content follows the approved
   Supply Chain and Procurement tool (Tools Design/Supply Chain Procurement: README.md, landing3.py):
   about ₹3 crore of supplies a month, about ₹20 lakh lost (₹8 lakh above the best price, ₹5 lakh rushed buys,
   ₹4 lakh used but never billed, ₹3 lakh expired); the three fixes (one agreed price per item, a lowest level
   per item, bill each item at the bedside); the helpers (price watch 1 AM, reorder 6 AM, bill matcher 9 PM);
   the processes (Monday shelf count, weekly buying meeting, morning numbers, every rushed buy signed) and the
   Stores Lead role. ===== */
if (typeof SUITES==="undefined") var SUITES = [];
SUITES.push({ key:"procurement", data:{
  suite: "Procurement",
  family: "Supply Chain and Procurement",
  hospital: "250-bed hospital, Bhubaneswar",
  started: "21 Sep 2026", week: 4, weeksPlanned: 20, asOf: "12 Oct 2026, 10:40 AM",
  recoverLine:"If all three land, break-even comes back to November.",
  aheadRisk:"The risk to watch is the agreed prices: until the top 200 items are covered, bills above the price will creep back.",
  chat:{ sub:"Procurement suite · 250-bed hospital, Bhubaneswar",
    msg:["Three of the twelve parts are live. Every supplier bill is now checked against the agreed price overnight, and bills above the price are down from 1 in 3 to 1 in 7.","Three measures are off track: rushed buys, items used but not billed, and supplier bills paid on time. The bill matcher is held up by the item codes, and accounts still pays in a monthly batch.","Pick a point to add to it, or choose what to do next."],
    note:"Sign the agreed prices this week. The biggest money is in the price.",
    points:["The bill matcher held up by item codes","Rushed buys still above plan","Supplier bills paid late","Break-even moving to December"],
    asks:["Which items are we paying most above the price for?","Which wards rush-buy the most?","Can we take the early-payment discounts?"] },
  milestone: { what: "Agreed prices for the top 200 items go live", date: "18 Oct", days: 6, part: 2 },
  month: { bought: 3.0, lost: 20, boughtToday: 10.2, aboveToday: 0.3, last: "PO 7712 · gloves · at agreed price" },

  /* bay: buying, stores, wards */
  parts: [
    { id:1,  name:"Purchase orders and supplier bills read", src:"ERP purchase module", bay:"buying", st:"live", when:"Live since 24 Sep", fresh:"5 min ago", owner:"ashok", vol:"about 90 bills a day", note:"Every purchase order, delivery note and supplier bill is read and matched line by line." },
    { id:2,  name:"One agreed price per item", src:"Supplier rate list", bay:"buying", st:"testing", when:"Goes live 18 Oct", fresh:"top 200 items in test", owner:"ashok", vol:"1,900 items · 41 suppliers", note:"One agreed price per item from fewer suppliers; the top 200 items carry about 70% of the spend." },
    { id:3,  name:"Price watch, every night at 1 AM", src:"Supplier bills and agreed prices", bay:"buying", st:"live", when:"Live since 1 Oct", fresh:"ran 1:04 AM", owner:"pratima", vol:"about 90 bills checked a night", note:"Flags every bill above the agreed price and sends the buyer one slip each morning." },
    { id:4,  name:"Lowest level for each item, ward by ward", src:"Ward stock in the ERP", bay:"stores", st:"testing", when:"Goes live 22 Oct", fresh:"set for 6 of 9 wards", owner:"pratima", vol:"about 340 items on ward shelves", note:"Each ward has a lowest level per item, so the store tops up before a shelf runs out." },
    { id:5,  name:"Reorder helper, every morning at 6 AM", src:"ERP indents", bay:"stores", st:"building", when:"Due 2 Nov", fresh:"no feed yet", owner:"sanjay", vol:"—", note:"Raises the order for anything below its lowest level and sends it to the buyer to approve." },
    { id:6,  name:"Monday shelf count on the phone", src:"Ward phones", bay:"wards", st:"live", when:"Live since 5 Oct", fresh:"Monday 10:30 AM", owner:"lipika", vol:"9 wards", note:"Each ward sister counts the shelves against the lowest levels and sends the count to the store." },
    { id:7,  name:"Every rushed buy signed", src:"Local purchase register", bay:"stores", st:"testing", when:"Goes live 15 Oct", fresh:"paper register meanwhile", owner:"pratima", vol:"about 46 rushed buys a month", note:"No one buys from a local shop unless the Stores Lead signs and says why the shelf ran out." },
    { id:8,  name:"Bill matcher, every evening at 9 PM", src:"Drug chart and billing, with the Billing & Insurance suite", bay:"wards", st:"blocked", when:"11 days late · now 30 Oct", fresh:"no feed yet", owner:"sanjay", vol:"about 3,100 items used a day",
      note:"Compares what each ward used today with what reached the patient's bill.",
      delay:"Ward item codes do not match the billing codes for about 400 consumables, the same match the Billing & Insurance suite is waiting on. Until it is done, about 1 in 12 items used still never reaches a bill.",
      fixes:[["Match the 400 codes jointly with the Billing & Insurance suite","sanjay","24 Oct"],["Billing desk checks the top 50 items by hand each evening meanwhile","smita","14 Oct"],["Bill matcher live","sanjay","30 Oct"]] },
    { id:9,  name:"Expiry watch: oldest stock used first", src:"Store batch records", bay:"stores", st:"building", when:"Due 26 Oct", fresh:"batches being loaded", owner:"rakesh", vol:"about 2,600 batches", note:"Puts the oldest batch first on the pick list and warns 60 days before expiry so stock can move to a busier ward." },
    { id:10, name:"Supplier delivery and quality score", src:"Goods received records", bay:"buying", st:"notstarted", when:"Starts 9 Nov", fresh:"not started", owner:"ashok", vol:"41 suppliers", note:"Scores each supplier on late, short and wrong deliveries, for the weekly buying meeting." },
    { id:11, name:"Use forecast from tomorrow's admissions and theatre list", src:"Admission Process suite and the theatre list", bay:"wards", st:"notstarted", when:"Starts 16 Nov", fresh:"not started", owner:"pratima", vol:"—", note:"Sets tomorrow's ward top-ups from the bed map and the operations booked." },
    { id:12, name:"Supplier bills paid on time", src:"Accounts payable", bay:"buying", st:"testing", when:"Goes live 26 Oct", fresh:"weekly run in test", owner:"rajesh", vol:"about ₹3 crore a month", note:"Pays each bill on its due date instead of in one monthly batch, so early-payment discounts are not lost." }
  ],
  handoffs: [
    { name:"Item codes for the bill matcher", to:"Billing & Insurance", st:"blocked", when:"Joint match due 24 Oct" },
    { name:"Tomorrow's admissions and theatre list", to:"Admission Process", st:"notstarted", when:"Starts 16 Nov" }
  ],

  kpis: [
    { id:"K1", name:"Supplier bills above the agreed price", short:"Bills above price", unit:"%", dir:"down", base:33, target:0, plan:18, now:14,
      why:"The price watch runs every night and the buyer clears its slip at the morning numbers." },
    { id:"K2", name:"Paid above the best price each month", short:"Above best price", unit:"L", dir:"down", base:8, target:1, plan:5.5, now:6.1,
      factors:[["Agreed prices cover only the top 60 items so far",60],["Two surgeons insist on one brand of implants",40]],
      fixes:[["Agreed prices for the top 200 items","ashok","18 Oct"],["Implant brand choice taken to the buying meeting with the surgeons","kavya","22 Oct"]],
      back:"Back on the plan line by week 7 (2 Nov)" },
    { id:"K3", name:"Rushed buys a month", short:"Rushed buys", unit:"n", dir:"down", base:60, target:15, plan:40, now:46,
      factors:[["Lowest levels not yet set on 3 wards",50],["Reorder helper not built, so top-ups wait for the weekly indent",35],["Night shift buys without signing",15]],
      fixes:[["Lowest levels on all 9 wards","pratima","22 Oct"],["Reorder helper live","sanjay","2 Nov"],["Signing rule briefed to night sisters","lipika","15 Oct"]],
      back:"Back on the plan line by week 8 (9 Nov)" },
    { id:"K4", name:"Items used but not billed", short:"Used, not billed", unit:"%", dir:"down", base:10, target:2, plan:7, now:8.5,
      factors:[["Bill matcher held up by 400 item codes",75],["Theatre consumables written on paper",25]],
      fixes:[["Joint code match with Billing & Insurance","sanjay","24 Oct"],["Billing desk checks the top 50 items by hand","smita","14 Oct"]],
      back:"Back on the plan line by week 9 (16 Nov)" },
    { id:"K5", name:"Expired each month", short:"Expired", unit:"L", dir:"down", base:3, target:1, plan:2.4, now:2.3,
      why:"Pharmacy moved 40 near-expiry batches to the ICU and the theatres in October." },
    { id:"K6", name:"Wards that sent the Monday count", short:"Monday counts", unit:"%", dir:"up", base:0, target:100, plan:70, now:78,
      why:"Seven of nine wards count on the phone; the counts reach the store before 11 AM." },
    { id:"K7", name:"Items with an agreed price", short:"Agreed prices", unit:"%", dir:"up", base:22, target:90, plan:50, now:44,
      factors:[["Price talks with three large suppliers still open",70],["Rate list not signed by the CFO",30]],
      fixes:[["CFO sign-off on the rate list","kavya","16 Oct"],["Talks closed with the three suppliers","ashok","18 Oct"]],
      back:"Back on the plan line by week 6 (26 Oct)" },
    { id:"K8", name:"Ward stock-outs a week", short:"Stock-outs", unit:"n", dir:"down", base:38, target:5, plan:25, now:27,
      factors:[["Weekly indent instead of daily top-ups",70],["Shelf counts missed on 2 wards",30]],
      fixes:[["Reorder helper live","sanjay","2 Nov"]],
      back:"Back on the plan line by week 7 (2 Nov)" },
    { id:"K9", name:"Supplier bills paid on time", short:"Paid on time", unit:"%", dir:"up", base:54, target:95, plan:70, now:61,
      factors:[["Accounts still pays in one monthly batch",65],["Bills held for missing delivery notes",35]],
      fixes:[["Weekly payment run","rajesh","26 Oct"],["Delivery notes scanned at the store door","pratima","19 Oct"]],
      back:"Back on the plan line by week 8 (9 Nov)" }
  ],

  people: [
    { key:"pratima", name:"Pratima Mishra", role:"Stores Lead", from:"New role we recommended · joined 28 Sep", done:11, due:12, late:0,
      today:[["Morning numbers with the buyer",1],["Sign 2 rushed buys","in progress"],["Lowest levels for Wards 7 to 9","in progress"]],
      next:[["Signing rule live","15 Oct"],["Delivery notes scanned at the door","19 Oct"],["Lowest levels on all wards","22 Oct"],["First month's savings report to the CFO","2 Nov"]] },
    { key:"ashok", name:"Ashok Panda", role:"Purchase manager (buyer)", from:"Hospital", done:5, due:8, late:2,
      today:[["Close prices with three suppliers","late 6 days"],["Clear last night's price-watch slip",1],["Rate list to the CFO","late 3 days"]],
      impact:"Prices 6 days late: about ₹0.6 lakh a month still paid above the best price, and break-even moves 2 weeks.",
      next:[["Agreed prices for the top 200 items","18 Oct"],["Buying meeting with the surgeons on implants","22 Oct"],["Supplier score starts","9 Nov"]] },
    { key:"lipika", name:"Sister Lipika Behera", role:"Nursing in-charge, ward counts", from:"Hospital (also on the Discharge Summary suite)", done:6, due:7, late:0,
      today:[["Chase Monday counts from Wards 4 and 8","in progress"],["Brief night sisters on signed buys",1]],
      next:[["Signing rule briefed to every night sister","15 Oct"],["All 9 wards counting","19 Oct"]] },
    { key:"smita", name:"Smita Panda", role:"Billing executive", from:"Hospital (also on the Billing & Insurance suite)", done:7, due:8, late:1,
      today:[["Evening hand check of the top 50 items","late 1 day"],["Theatre consumables list",1]],
      impact:"Hand check started a day late: about ₹0.1 lakh of used items missed the bill yesterday.",
      next:[["Hand check every evening","14 Oct"],["Hand over to the bill matcher","30 Oct"]] },
    { key:"rajesh", name:"Rajesh Dash", role:"Accounts payable lead", from:"Hospital", done:3, due:5, late:2,
      today:[["Weekly payment run test","late 4 days"],["List bills held for delivery notes","late 2 days"]],
      impact:"Monthly batch still running: early-payment discounts worth about ₹0.8 lakh a month are lost.",
      next:[["Weekly payment run","26 Oct"],["Early-payment discounts taken","9 Nov"]] },
    { key:"rakesh", name:"Rakesh Behera", role:"Pharmacy in-charge", from:"Hospital (also on the Billing & Insurance suite)", done:5, due:6, late:0,
      today:[["Load batch numbers for the main store",1],["Move 12 near-expiry batches to ICU","in progress"]],
      next:[["Expiry watch live","26 Oct"],["Oldest-first pick list in pharmacy","2 Nov"]] },
    { key:"sanjay", name:"Sanjay Mohanty", role:"IT integration lead", from:"Hospital IT (shared with four suites)", done:3, due:6, late:1,
      today:[["Item code match for 400 consumables","late 11 days"],["Reorder helper set-up",1]],
      impact:"Item codes 11 days late: the bill matcher cannot run, and about 1 in 12 items used never reaches a bill.",
      next:[["Joint code match","24 Oct"],["Bill matcher live","30 Oct"],["Reorder helper live","2 Nov"]] },
    { key:"kavya", name:"Kavya Iyer", role:"Virevo project lead", from:"Virevo", done:5, due:5, late:0,
      today:[["Weekly report to the CFO",1],["Agenda for the implant meeting",1]],
      next:[["CFO sign-off on the rate list","16 Oct"],["Implant meeting","22 Oct"],["Four-week review","9 Nov"]] }
  ],

  months: ["Sep","Oct"],
  spend: [
    { cat:"Subscription", v:[2.0,2.0] },
    { cat:"Salaries of roles we recommended", v:[0.1,0.3], note:"Stores Lead ₹3.6 lakh a year (example)" },
    { cat:"One-time costs", v:[1.5,0.8], note:"Sep: barcode scanners for the stores · Oct: phones for 9 wards" }
  ],
  revenue: [0.3,1.1], ebitda:[1.4,4.6],
  runRate: { revenue:2.5, ebitda:12 },
  cumMonths:["Sep","Oct","Nov","Dec","Jan","Feb","Mar","Apr","May","Jun"],
  cumSpend:[3.6,6.7,9.0,11.3,13.6,15.9,18.2,20.5,22.8,25.1],
  cumPlan:[1.5,6.0,12.0,19.0,26.5,34.3,42.3,50.5,58.9,67.5],
  cumFore:[1.4,6.0,8.6,13.4,19.0,25.2,31.8,38.8,46.0,53.4],
  actualTo:1,
  breakeven:{ plan:"Nov 2026", fore:"Dec 2026", late:"about 4 weeks", planIdx:2, foreIdx:3 },
  healthFactors:[["Agreed prices late, so the biggest saving is not in yet",45],["Bill matcher held up by item codes",30],["Supplier bills still paid in a monthly batch",25]],
  healthFixes:[["Agreed prices for the top 200 items","ashok","18 Oct"],["Joint item code match","sanjay","24 Oct"],["Weekly payment run","rajesh","26 Oct"]],
  watch: [
    { t:"Bill matcher held up by item codes, 11 days late", who:"sanjay", ref:"part:8" },
    { t:"Rushed buys: 46 a month against a plan of 40", who:"pratima", ref:"kpi:K3" },
    { t:"Supplier bills paid on time: 9 points under plan", who:"rajesh", ref:"kpi:K9" }
  ],
  resources: [
    ["Project plan and milestones","PDF · 21 Sep"],["Rate list for the top 200 items (awaiting CFO sign-off)","Spreadsheet · 10 Oct"],
    ["Lowest levels by ward","9 wards · updated 11 Oct"],["Rushed-buy signing rule","1 page"],
    ["Weekly review notes","3 notes · latest 9 Oct"],["Subscription agreement and invoices","2 files"]
  ]
}});
