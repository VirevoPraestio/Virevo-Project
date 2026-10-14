/* ===== Simulation · page 1 (Your data) · data model =====
   One entry per data family. Each family lists the files that feed it and the measures the formula needs from it.
   src: "erp" = comes from a system export; "manual" = kept on paper or a spreadsheet; "none" = not recorded anywhere today.
   req: true for the files the engine cannot run without. */
const SAMPLE = {"dim_beds":[150,"",""],"dim_doctors":[15,"",""],"dim_drugs":[20,"",""],"dim_equipment":[22,"",""],"dim_implants":[16,"",""],"dim_instrument_sets":[10,"",""],"dim_patients":[400,"",""],"dim_payers":[8,"",""],"dim_procedures":[22,"",""],"dim_referral_doctors":[28,"",""],"dim_staff":[60,"",""],"dim_staff_grades":[17,"",""],"dim_surgical_consumables":[14,"",""],"dim_wards":[12,"",""],"fact_admissions":[285,"2024-02","2024-02"],"fact_billing_claims":[227,"2024-02","2024-02"],"fact_biomedical_log":[74,"2024-01","2024-02"],"fact_camp_log":[3,"2024-02","2024-02"],"fact_clinical_events":[17,"2024-02","2024-02"],"fact_complaints_log":[18,"2024-02","2024-02"],"fact_cssd_processing_log":[147,"2024-02","2024-02"],"fact_daily_revenue_summary":[28,"2024-02","2024-02"],"fact_diagnostic_utilisation":[196,"2024-02","2024-02"],"fact_dietary_operations":[28,"2024-02","2024-02"],"fact_discharges":[227,"2024-02","2024-02"],"fact_housekeeping_log":[227,"2024-02","2024-02"],"fact_housekeeping_staff":[336,"2024-02","2024-02"],"fact_hr_attrition_log":[4,"2024-01","2024-02"],"fact_hr_staff_register":[207,"",""],"fact_hr_vacancy_log":[16,"2023-11","2024-01"],"fact_icu_census":[263,"2024-02","2024-02"],"fact_implant_usage":[70,"2024-02","2024-02"],"fact_infection_surveillance":[196,"2024-02","2024-02"],"fact_insurance_claims":[138,"2024-02","2024-03"],"fact_ip_daily_census":[1403,"2024-02","2024-02"],"fact_marketing_spend":[9,"",""],"fact_monthly_cost_summary":[12,"",""],"fact_nabh_audit":[28,"2024-02","2024-02"],"fact_nursing_shifts":[1632,"2024-02","2024-02"],"fact_online_reviews":[12,"2024-02","2024-02"],"fact_opd_visits":[1699,"2024-02","2024-02"],"fact_ot_consumable_usage":[540,"2024-02","2024-02"],"fact_ot_sessions":[168,"2024-02","2024-02"],"fact_patient_satisfaction":[86,"2024-02","2024-02"],"fact_payroll_summary":[8,"",""],"fact_pharmacy_dispensing":[5524,"2024-02","2024-02"],"fact_pharmacy_inventory":[364,"2024-02","2024-02"],"fact_readmission_detail":[12,"",""],"fact_referral_performance":[8,"",""],"fact_utility_costs":[140,"2024-02","2024-02"],"sim_parameters":[70,"",""]};

/* the files left out of the opening state, so every kind of gap shows */
const HELD_BACK = ["fact_biomedical_log","fact_hr_attrition_log","fact_hr_vacancy_log","fact_payroll_summary","fact_marketing_spend","fact_camp_log","fact_online_reviews","fact_referral_performance","dim_referral_doctors","fact_complaints_log","fact_nabh_audit","fact_utility_costs","fact_dietary_operations"];

const REQUIRED = ["sim_parameters","dim_wards","dim_staff","fact_nursing_shifts","fact_ot_sessions","fact_discharges","fact_daily_revenue_summary","fact_billing_claims","fact_insurance_claims","fact_pharmacy_dispensing","fact_icu_census","fact_opd_visits","fact_admissions","fact_housekeeping_log","fact_housekeeping_staff"];

/* plain names for files, as a person would say them */
const FILE_NAME = {
  dim_beds:"Bed list", dim_wards:"Ward list", fact_ip_daily_census:"Daily bed census", fact_admissions:"Admissions", fact_discharges:"Discharges",
  fact_nursing_shifts:"Nursing shift roster", dim_staff:"Staff list", dim_staff_grades:"Staff grades and pay bands", fact_hr_staff_register:"HR staff register", fact_hr_vacancy_log:"Open posts log", fact_hr_attrition_log:"Leavers log", fact_payroll_summary:"Payroll summary",
  fact_ot_sessions:"Theatre sessions", fact_cssd_processing_log:"Sterilising (CSSD) log", fact_ot_consumable_usage:"Theatre consumables used", dim_procedures:"Procedure list and prices", dim_instrument_sets:"Instrument sets", dim_surgical_consumables:"Surgical consumables list", fact_implant_usage:"Implants used", dim_implants:"Implant list and prices",
  fact_icu_census:"ICU census",
  fact_diagnostic_utilisation:"Scans and tests by machine", dim_equipment:"Equipment register", fact_biomedical_log:"Maintenance log",
  fact_pharmacy_dispensing:"Pharmacy dispensing", fact_pharmacy_inventory:"Pharmacy stock", dim_drugs:"Drug list",
  fact_billing_claims:"Bills and claims", fact_insurance_claims:"Insurer settlements", dim_payers:"Insurers and TPAs", fact_daily_revenue_summary:"Daily revenue",
  fact_opd_visits:"OPD visits", dim_doctors:"Doctor list", dim_patients:"Patient list", dim_referral_doctors:"Referring doctors", fact_referral_performance:"Referrals by doctor", fact_marketing_spend:"Marketing spend", fact_camp_log:"Health camps", fact_online_reviews:"Online reviews",
  fact_housekeeping_log:"Room cleaning log", fact_housekeeping_staff:"Housekeeping roster", fact_dietary_operations:"Kitchen and diet log", fact_utility_costs:"Power, water and gas bills",
  fact_clinical_events:"Clinical incidents", fact_infection_surveillance:"Infection watch", fact_nabh_audit:"NABH audit findings", fact_readmission_detail:"Readmissions", fact_patient_satisfaction:"Patient feedback", fact_complaints_log:"Complaints", fact_monthly_cost_summary:"Monthly costs", sim_parameters:"Current settings and targets"
};

const DOMAINS = [
  { id:"beds", name:"Beds and wards", short:"Beds", files:["dim_beds","dim_wards","fact_ip_daily_census","fact_admissions","fact_discharges"],
    it:"From the HIS admission and bed modules: one row per admission (patient, ward, bed, admitted at, discharge decided at, discharged at) and one row per bed per day.",
    ms:[ {id:"occ", n:"Bed occupancy", src:"erp", f:["fact_ip_daily_census"]},
         {id:"los", n:"Average length of stay", src:"erp", f:["fact_admissions","fact_discharges"]},
         {id:"turn", n:"Bed empty to next patient", src:"erp", f:["fact_discharges","fact_housekeeping_log"]},
         {id:"dclag", n:"Discharge decision to patient out", src:"manual", f:["fact_discharges"], note:"The decision time is typed in after the patient leaves, so it is often wrong."},
         {id:"round", n:"Ward round start time", src:"none", f:[], note:"Not written down anywhere. A two-week register at the nursing station is enough to start."} ] },
  { id:"nurse", name:"Nurses and staff", short:"Staff", files:["fact_nursing_shifts","dim_staff","dim_staff_grades","fact_hr_staff_register","fact_hr_vacancy_log","fact_hr_attrition_log","fact_payroll_summary"],
    it:"From the roster and HR systems: one row per shift (nurse, ward, date, shift, own or agency, hours) and the vacancy and leavers registers.",
    ms:[ {id:"agency", n:"Agency share of ICU shifts", src:"erp", f:["fact_nursing_shifts"]},
         {id:"agcost", n:"Agency cost a month", src:"erp", f:["fact_nursing_shifts","fact_payroll_summary"]},
         {id:"vac", n:"Open nursing posts", src:"erp", f:["fact_hr_vacancy_log"]},
         {id:"leave", n:"Nurses leaving a year", src:"erp", f:["fact_hr_attrition_log"]},
         {id:"ratio", n:"Patients per nurse, by shift", src:"erp", f:["fact_nursing_shifts","fact_ip_daily_census"]} ] },
  { id:"ot", name:"Theatres and sterilising", short:"Theatres", files:["fact_ot_sessions","fact_cssd_processing_log","fact_ot_consumable_usage","dim_procedures","dim_instrument_sets","dim_surgical_consumables","fact_implant_usage","dim_implants"],
    it:"From the OT scheduler and CSSD: one row per booked case (theatre, surgeon, booked start, actual start, end, cancelled and why) and one row per instrument set cycle.",
    ms:[ {id:"otuse", n:"Theatre time used", src:"erp", f:["fact_ot_sessions"]},
         {id:"otcan", n:"Cases cancelled, and why", src:"erp", f:["fact_ot_sessions"]},
         {id:"cssd", n:"Instrument set turnaround", src:"erp", f:["fact_cssd_processing_log"]},
         {id:"otrev", n:"Theatre revenue", src:"erp", f:["fact_ot_sessions","dim_procedures"]},
         {id:"first", n:"First case starting late", src:"manual", f:["fact_ot_sessions"], note:"Actual start is filled in by hand in the OT register."} ] },
  { id:"icu", name:"ICU", short:"ICU", files:["fact_icu_census"],
    it:"From the ICU module: one row per ICU bed per day (patient, acuity score, on ventilator Y/N, could step down Y/N).",
    ms:[ {id:"icul", n:"ICU length of stay", src:"erp", f:["fact_icu_census"]},
         {id:"overflow", n:"ICU beds held by ward-level patients", src:"erp", f:["fact_icu_census"]},
         {id:"vent", n:"Ventilator days", src:"erp", f:["fact_icu_census"]},
         {id:"step", n:"Wait for a step-down bed", src:"none", f:[], note:"Nobody records when a patient was ready to leave the ICU."} ] },
  { id:"diag", name:"Scans and tests", short:"Diagnostics", files:["fact_diagnostic_utilisation","dim_equipment","fact_biomedical_log"],
    it:"From the RIS/LIS and the biomedical team: one row per study (machine, ordered at, done at, reported at, done outside Y/N) and one row per maintenance job.",
    ms:[ {id:"mach", n:"Use of each machine", src:"erp", f:["fact_diagnostic_utilisation","dim_equipment"]},
         {id:"leak", n:"Tests sent outside", src:"erp", f:["fact_diagnostic_utilisation"]},
         {id:"rtat", n:"Scan to signed report", src:"erp", f:["fact_diagnostic_utilisation"]},
         {id:"pm", n:"Maintenance done on time", src:"erp", f:["fact_biomedical_log"]},
         {id:"down", n:"Machine downtime hours", src:"manual", f:["fact_biomedical_log"], note:"Breakdowns are logged on paper in the biomedical room."} ] },
  { id:"pharm", name:"Pharmacy", short:"Pharmacy", files:["fact_pharmacy_dispensing","fact_pharmacy_inventory","dim_drugs"],
    it:"From the pharmacy system: one row per issue (drug, patient, ward, ordered by, as-needed Y/N, cost) and a daily stock snapshot.",
    ms:[ {id:"dcost", n:"Drug cost as a share of revenue", src:"erp", f:["fact_pharmacy_dispensing","fact_daily_revenue_summary"]},
         {id:"gen", n:"Generic share of prescriptions", src:"erp", f:["fact_pharmacy_dispensing","dim_drugs"]},
         {id:"stock", n:"Stock-outs on the wards", src:"erp", f:["fact_pharmacy_inventory"]},
         {id:"prn", n:"As-needed doses ordered", src:"erp", f:["fact_pharmacy_dispensing"]} ] },
  { id:"bill", name:"Billing and insurance", short:"Billing", files:["fact_billing_claims","fact_insurance_claims","dim_payers","fact_daily_revenue_summary"],
    it:"From billing and the TPA desk: one row per bill (raised, sent to insurer, queried, settled, amount claimed and paid) and daily revenue by department.",
    ms:[ {id:"arpob", n:"Revenue per occupied bed", src:"erp", f:["fact_daily_revenue_summary","fact_ip_daily_census"]},
         {id:"sublag", n:"Discharge to claim sent", src:"erp", f:["fact_billing_claims"]},
         {id:"instat", n:"Claim sent to money in", src:"erp", f:["fact_insurance_claims"]},
         {id:"recv", n:"Money waiting to be collected", src:"erp", f:["fact_billing_claims","fact_insurance_claims"]},
         {id:"preauth", n:"Pre-approval wait at admission", src:"manual", f:[], note:"The TPA desk keeps this in a notebook."} ] },
  { id:"opd", name:"OPD and referrals", short:"OPD", files:["fact_opd_visits","dim_doctors","dim_patients","dim_referral_doctors","fact_referral_performance","fact_marketing_spend","fact_camp_log","fact_online_reviews"],
    it:"From the OPD module and marketing: one row per visit (doctor, new or repeat, advised admission Y/N, admitted Y/N) and referrals by source.",
    ms:[ {id:"conv", n:"OPD visits that become admissions", src:"erp", f:["fact_opd_visits","fact_admissions"]},
         {id:"mix", n:"Specialty mix of admissions", src:"erp", f:["fact_admissions"]},
         {id:"ref", n:"Referrals by doctor", src:"erp", f:["fact_referral_performance","dim_referral_doctors"]},
         {id:"mkt", n:"Marketing spend per admission", src:"erp", f:["fact_marketing_spend"]},
         {id:"follow", n:"Counsellor follow-up after advice", src:"none", f:[], note:"Counsellors call patients but keep no record of it."} ] },
  { id:"supp", name:"Housekeeping and support", short:"Support", files:["fact_housekeeping_log","fact_housekeeping_staff","fact_dietary_operations","fact_utility_costs"],
    it:"From housekeeping and facilities: one row per room cleaned (requested, started, done) and the monthly utility bills.",
    ms:[ {id:"clean", n:"Room cleaning time", src:"erp", f:["fact_housekeeping_log"]},
         {id:"hkstaff", n:"Housekeepers on each shift", src:"erp", f:["fact_housekeeping_staff"]},
         {id:"linen", n:"Linen request to delivery", src:"manual", f:["fact_housekeeping_log"], note:"Linen requests go by phone; the laundry writes them in a book."},
         {id:"util", n:"Power and water cost per bed", src:"erp", f:["fact_utility_costs"]} ] },
  { id:"qual", name:"Money and quality", short:"Money", files:["fact_monthly_cost_summary","sim_parameters","fact_readmission_detail","fact_clinical_events","fact_infection_surveillance","fact_patient_satisfaction","fact_complaints_log","fact_nabh_audit"],
    it:"From finance and quality: the monthly profit and loss by cost head, readmissions with reason, incidents, infections and feedback scores.",
    ms:[ {id:"ebitda", n:"EBITDA and the cost base", src:"erp", f:["fact_monthly_cost_summary","fact_daily_revenue_summary"]},
         {id:"readm", n:"Readmissions within 30 days", src:"erp", f:["fact_readmission_detail"]},
         {id:"inf", n:"Hospital infections", src:"erp", f:["fact_infection_surveillance"]},
         {id:"sat", n:"Patient satisfaction", src:"erp", f:["fact_patient_satisfaction"]},
         {id:"set", n:"Current settings and targets", src:"erp", f:["sim_parameters"]} ] }
];

/* the KPIs the formula drives, and which measures feed each one (weight = share of the reference relation) */
const KPIS = [
  {id:"EBITDA", n:"EBITDA", s:"EBITDA", u:"%"}, {id:"REV", n:"Gross revenue", s:"Revenue", u:"₹ L"}, {id:"ARPOB", n:"Revenue per bed", s:"Per bed", u:"₹"},
  {id:"LOS", n:"Length of stay", s:"Stay", u:"days"}, {id:"OCC", n:"Occupancy", s:"Occupancy", u:"%"}, {id:"OTU", n:"Theatre use", s:"Theatres", u:"%"},
  {id:"RECV", n:"Days to collect", s:"Collect", u:"days"}, {id:"DRUG", n:"Drug cost", s:"Drug cost", u:"%"}, {id:"AGENCY", n:"Agency cost", s:"Agency", u:"₹ L"}
];
const LINKS = [
  ["round","LOS",.5],["dclag","LOS",.55],["rtat","LOS",.28],["los","OCC",.5],["turn","OCC",.6],["occ","REV",.8],["los","REV",.4],["turn","REV",.3],
  ["agency","AGENCY",.91],["vac","AGENCY",.95],["leave","AGENCY",.4],["ratio","AGENCY",.3],["agcost","EBITDA",.66],
  ["otuse","OTU",.9],["otcan","OTU",.84],["cssd","OTU",.45],["pm","OTU",.55],["first","OTU",.35],["otrev","REV",.4],
  ["icul","LOS",.3],["overflow","ARPOB",.3],["vent","ARPOB",.3],["step","LOS",.25],
  ["mach","REV",.35],["leak","REV",.4],["leak","ARPOB",.55],["down","OTU",.25],
  ["dcost","DRUG",.9],["gen","DRUG",.7],["stock","DRUG",.45],["prn","DRUG",.65],
  ["arpob","ARPOB",.95],["sublag","RECV",.86],["instat","RECV",.7],["recv","RECV",.9],["preauth","RECV",.55],
  ["conv","REV",.5],["mix","ARPOB",.74],["ref","REV",.3],["mkt","EBITDA",.2],["follow","REV",.25],
  ["clean","OCC",.55],["hkstaff","OCC",.48],["linen","OCC",.42],["util","EBITDA",.2],
  ["ebitda","EBITDA",1],["readm","LOS",.2],["inf","LOS",.3],["sat","REV",.15],["set","EBITDA",.3],
  ["REV","EBITDA",.65],["ARPOB","EBITDA",.45],["DRUG","EBITDA",.7],["AGENCY","EBITDA",.66],["RECV","EBITDA",.3],["LOS","OCC",.5],["OTU","REV",.4]
];

const JOURNEY = [
  ["Your data","Send us what you record"],["Targets","Your numbers"],["Six KPIs","Pick what to track"],["Simulate","Achievable or dream"],
  ["Freeze","Check and confirm"],["Your team","Who owns what"],["Taskboards","Week by week"]
];

const HOSPITAL = { name:"Sample hospital", beds:150, city:"example data" };
