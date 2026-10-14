/* ===== Page 4 (rebuilt) · shared look: top strip, sticky panel of the six on the right, approvals on the left ===== */
const SIM_CSS = P3_CSS + `
.lk-web .top5{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:0;border:2px solid var(--w-ink);border-radius:14px;background:var(--w-sheet);overflow:hidden;margin:0 0 14px;position:sticky;top:0;z-index:6;box-shadow:0 6px 0 rgba(22,33,62,.10),0 -12px 0 var(--w-paper,#EEF1F5)}
.lk-web .t5{padding:8px 14px;border-left:1.5px solid var(--w-line);cursor:pointer;min-width:0}
.lk-web .t5:first-child{border-left:0}
.lk-web .t5:hover{background:#F1F4F8}
.lk-web .t5 span{display:block;font-size:10.5px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--w-mute)}
.lk-web .t5 b{display:block;font-family:var(--f-num);font-weight:400;font-size:28px;line-height:1.05}
.lk-web .t5 b i{font-style:normal;font-size:16px;color:var(--w-mute)}
.lk-web .t5 small{display:block;font-size:11.5px;color:var(--w-mute);line-height:1.3}
.lk-web .t5.hl{background:#FFF7E3}
.lk-web .bulk5{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin:0 0 14px}
.lk-web .bulk5>span{font-size:12.5px;font-weight:600;color:var(--w-mute)}
.lk-web .bulk5 .frz{margin-left:auto;min-height:44px;padding:8px 20px}
.lk-web .sim5{display:grid;grid-template-columns:minmax(0,1fr) 380px;gap:20px;align-items:start}
.lk-web .kp5{position:sticky;top:calc(var(--t5h,100px) + 18px);max-height:calc(100vh - var(--t5h,100px) - 28px);overflow:auto;border:2px solid var(--w-ink);border-radius:16px;background:var(--w-sheet);box-shadow:8px 8px 0 rgba(22,33,62,.12)}
.lk-web .kp5-top{display:flex;flex-wrap:wrap;align-items:center;gap:8px;justify-content:space-between;padding:12px 14px 8px;border-bottom:1.5px solid var(--w-line);position:sticky;top:0;background:var(--w-sheet);z-index:2}
.lk-web .kp5-top h2{margin:0;font-family:var(--f-num);font-weight:400;font-size:26px;line-height:1}
.lk-web .seg{display:inline-flex;border:1.5px solid var(--w-ink);border-radius:999px;overflow:hidden}
.lk-web .seg button{border:0;background:#fff;padding:5px 10px;font-size:12px;font-weight:600;min-height:34px;color:var(--w-ink)}
.lk-web .seg button[aria-pressed="true"]{background:var(--w-ink);color:#fff}
.lk-web .kp5-sum{display:grid;gap:2px;padding:8px 14px;font-size:12px;color:var(--w-mute);background:#F6F8FA;border-bottom:1px solid var(--w-line)}
.lk-web .kp5 ul{list-style:none;margin:0;padding:4px 14px 8px;display:grid}
.lk-web .k5{padding:10px 0;border-bottom:1px solid #E6EAF0}
.lk-web .k5-h{display:flex;justify-content:space-between;gap:8px;align-items:baseline}
.lk-web .k5-h .linkbtn b{font-size:13.5px}
.lk-web .k5-s{font-size:11.5px;font-weight:700;white-space:nowrap}
.lk-web .k5-s[data-state="hit"]{color:var(--w-yours)} .lk-web .k5-s[data-state="near"]{color:var(--w-gold-ink)} .lk-web .k5-s[data-state="far"]{color:var(--w-none)}
.lk-web .k5-v{display:flex;align-items:baseline;gap:6px;flex-wrap:wrap}
.lk-web .k5-v b{font-family:var(--f-num);font-weight:400;font-size:30px;line-height:1.05}
.lk-web .k5-v small{font-size:11.5px;color:var(--w-mute)}
.lk-web .k5-v em{margin-left:auto;font-style:normal;font-size:12px;font-weight:600;color:var(--w-yours)}
.lk-web .k5-line{position:relative;height:16px;margin:2px 0 4px}
.lk-web .k5-line .tr{position:absolute;left:0;right:0;top:6px;height:5px;border-radius:3px;background:#DCE2EA}
.lk-web .k5-line .fill{position:absolute;left:0;top:5px;height:7px;border-radius:4px;background:var(--w-yours);transition:width .25s}
.lk-web .k5-line .mk{position:absolute;top:0;width:3px;height:16px;margin-left:-1.5px;border-radius:1px}
.lk-web .k5-line .mk.a{background:var(--w-gold)} .lk-web .k5-line .mk.d{background:var(--w-ink)}
.lk-web .k5-n{display:flex;flex-wrap:wrap;gap:2px 12px;font-size:11.5px;color:var(--w-mute)}
.lk-web .k5-n b{color:var(--w-ink)} .lk-web .k5-n .a b{color:var(--w-gold-ink)}
.lk-web .kp5-key{display:flex;flex-wrap:wrap;gap:4px 12px;padding:8px 14px 12px;font-size:11.5px;color:var(--w-mute)}
.lk-web .kp5-key i{display:inline-block;width:12px;height:6px;margin-right:5px;vertical-align:middle;border-radius:2px}
.lk-web .kf{background:var(--w-yours)} .lk-web .ka{background:var(--w-gold);width:3px!important;height:12px!important} .lk-web .kd{background:var(--w-ink);width:3px!important;height:12px!important}
.lk-web .ch5{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));border:1.5px solid var(--w-ink);border-radius:10px;overflow:hidden;min-width:0}
.lk-web .ch5.sw3{grid-template-columns:repeat(3,minmax(0,1fr))}
.lk-web .ch5 button,.lk-web .ch5 .own{border:0;border-left:1.5px solid var(--w-ink);background:#fff;padding:4px 6px;min-height:46px;text-align:center;color:var(--w-ink);display:flex;flex-direction:column;justify-content:center;gap:1px}
.lk-web .ch5>:first-child{border-left:0}
.lk-web .ch5 small{font-size:10.5px;font-weight:600;color:var(--w-mute)}
.lk-web .ch5 b{font-family:var(--f-num);font-weight:400;font-size:17px;line-height:1}
.lk-web .ch5 button[aria-pressed="true"]{background:var(--w-ink);color:#fff} .lk-web .ch5 button[aria-pressed="true"] small{color:#C9D0DA}
.lk-web .ch5 button.a[aria-pressed="true"]{background:var(--w-gold);color:var(--w-ink)} .lk-web .ch5 button.a[aria-pressed="true"] small{color:var(--w-ink)}
.lk-web .ac5{border:1.5px solid var(--w-ink);border-radius:10px;background:#fff;padding:5px 8px 7px;display:grid;grid-template-columns:1fr 1fr;gap:4px 6px;min-width:0}
.lk-web .ac5.set{background:#FBFCFD} .lk-web .ac5.own{background:#FFF7E3;box-shadow:inset 0 0 0 2px var(--w-gold)}
.lk-web .ac5-h{grid-column:1/-1;display:flex;justify-content:space-between;align-items:center;font-size:11.5px;font-weight:700;color:var(--w-ink)}
.lk-web .ac5-r{border:0;background:none;padding:0 2px;font-size:11px;font-weight:600;color:var(--w-gold-ink);text-decoration:underline;min-height:24px}
.lk-web .ac5 label{display:grid;gap:1px;min-width:0}
.lk-web .ac5 small{font-size:10.5px;font-weight:600;color:var(--w-mute);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.lk-web .ac5 .num{width:100%;min-width:0;min-height:30px;padding:3px 6px;font-size:13px;border:1px solid var(--w-line);border-radius:6px;background:#fff;color:var(--w-ink)}
.lk-web .ac5 .num.tot{font-weight:700}
.lk-web .t5 .dur{width:46px;min-height:26px;padding:1px 4px;font-size:12px;border:1px solid var(--w-line);border-radius:6px;background:#fff;color:var(--w-ink)}
.lk-web .ac5 .num.ed{border-color:var(--w-gold);background:#FFF7E3}
.lk-web .cl{font-size:11.5px;color:var(--w-mute)}
.lk-web .frz5{position:fixed;inset:0;z-index:72;background:rgba(10,12,14,.45);display:grid;place-items:center;padding:16px}
.lk-web .frz5[hidden],.frz5[hidden]{display:none}
.frz5{position:fixed;inset:0;z-index:72;background:rgba(10,12,14,.45);display:grid;place-items:center;padding:16px}
.frz5-in{width:min(640px,100%);max-height:88vh;overflow:auto;background:#FBFCFD;border:2px solid #16213E;border-radius:16px;padding:20px;color:#16213E;font-family:var(--f-body)}
.frz5-in h2{margin:0 0 6px;font-family:var(--f-num);font-weight:400;font-size:36px;line-height:1}
.frz5-in p{margin:0 0 12px;color:#4E5A73;font-size:14px}
.frz5-g{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;margin-bottom:12px}
.frz5-g div{border:1px solid #C9D0DA;border-radius:10px;padding:8px 10px;background:#fff}
.frz5-g span{display:block;font-size:11px;font-weight:600;color:#4E5A73}
.frz5-g b{font-family:var(--f-num);font-weight:400;font-size:22px}
.frz5-in ul{margin:0 0 14px;padding-left:18px;font-size:13.5px;display:grid;gap:3px}
.frz5-in small{color:#4E5A73}
.frz5-b{display:flex;flex-wrap:wrap;gap:8px;justify-content:flex-end}
.frz5-b .go{border:2px solid #16213E;background:#d4a94f;color:#16213E;border-radius:12px;padding:10px 20px;font-weight:600;min-height:48px}
.frz5-b .act{border:2px solid #16213E;background:#fff;color:#16213E;border-radius:10px;padding:8px 14px;font-weight:600;min-height:44px}
@media (max-width:1150px){.lk-web .top5{grid-template-columns:repeat(3,minmax(0,1fr))}.lk-web .t5:nth-child(4){border-left:0}.lk-web .t5:nth-child(n+4){border-top:1.5px solid var(--w-line)}}
@media (max-width:1000px){.lk-web .sim5{grid-template-columns:1fr}.lk-web .kp5{position:static;max-height:none;order:-1}}
@media (max-width:560px){.lk-web .top5{grid-template-columns:repeat(3,minmax(0,1fr))!important;top:0}.lk-web .t5{padding:6px 8px;border-left:1.5px solid var(--w-line)!important;border-top:0!important}.lk-web .t5:nth-child(3n+1){border-left:0!important}.lk-web .t5:nth-child(n+4){border-top:1.5px solid var(--w-line)!important}.lk-web .t5 b{font-size:20px}.lk-web .t5 span{font-size:9.5px;letter-spacing:.04em}.lk-web .t5 small{display:none}}
@media (max-width:560px){.lk-web .top5{grid-template-columns:repeat(2,minmax(0,1fr))}.lk-web .t5:nth-child(odd){border-left:0}.lk-web .t5:nth-child(4){border-left:1.5px solid var(--w-line)}.lk-web .t5:nth-child(n+3){border-top:1.5px solid var(--w-line)}.lk-web .ch5{grid-template-columns:1fr 1fr}.lk-web .ch5>:nth-child(3){border-left:0}.lk-web .ch5>:nth-child(n+3){border-top:1.5px solid var(--w-ink)}.frz5-g{grid-template-columns:1fr 1fr}}
`;
function simHead(title, lede){ return `<div class="p2head" style="grid-template-columns:1fr"><div><div class="eb">Simulation · step 4 of 7 · ${esc(HOSPITAL.name)}, ${HOSPITAL.beds} beds</div><h1>${title}</h1><p class="lede">${lede}</p></div></div>`; }
