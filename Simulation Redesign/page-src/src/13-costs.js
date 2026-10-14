/* ===== Costs of each change (example figures, ₹) =====
   one: one-time cost per unit added (equipment, set-up, stock). mo: monthly running cost per unit added (salaries, licences).
   For switches, a unit is "switched on". For changes where lower is better (ward rounds earlier), there is no unit cost. */
const COSTS = {
  icunurse:{mo:45000}, wardnurse:{mo:35000}, hk:{mo:15000}, billexec:{mo:30000}, preauthstaff:{mo:30000}, biomed:{mo:50000}, coun:{mo:30000}, cssdtech:{mo:25000},
  dccoord:{mo:40000},
  icubeds:{one:800000, mo:20000}, ventk:{one:650000, mo:5000}, autoclave:{one:350000, mo:4000}, carm:{one:800000, mo:6000}, lap:{one:650000, mo:5000},
  echo:{one:600000, mo:4000}, usg:{one:400000, mo:3000}, ct:{one:18000000, mo:60000}, mri:{one:35000000, mo:100000},
  s_dis:{one:600000, mo:50000}, s_bill:{one:600000, mo:50000}, s_adm:{one:500000, mo:50000}, s_diag:{one:500000, mo:50000}, s_proc:{one:400000, mo:50000},
  generic:{one:80000}, incentive:{}, implant:{one:50000}, round8:{}, icupar:{one:200000}, linenpar:{one:150000}
};
