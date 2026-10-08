"""
skins: three candidate identities for the Financial domain (8 Oct 2026, for review).

Each skin keeps the frame of sc_common (same places, same sizes) and the type scale of 07 §2
(name 48/42, claim 37-40/34, body 14-15, labels 12-13 at 600, phone floors 14 / 11 / 10.5).
It changes the families, the shapes, the paper, the marks and the dress of rail, header and chat.

  A  The ledger         Playfair Display + Source Serif 4. Square corners, hairlines, double rules,
                        a red double margin, ruled paper, book thumb-index rail, cloth-bound chat.
  B  The till roll      Space Mono + Space Grotesk. Paper slips with torn zigzag edges on a counter,
                        dashed tear lines, ticket rail with punched notches, rubber-stamp note.
  C  The annual report  Inter Tight + Instrument Serif italic. Flat planes, no corners, heavy rules,
                        numbered sections, big figures, a black flat chat with an editorial note.
"""
import sc_common as C

def _ix(i, n, d, cur, fmt):
    return fmt(i, n)

# ==========================================================================================
# A · THE LEDGER
A_FONTS = C.fonts([('Playfair Display', 'playfair-display', 700, 'normal'), ('Playfair Display', 'playfair-display', 600, 'normal'),
                   ('Playfair Display', 'playfair-display', 400, 'italic'),
                   ('Source Serif 4', 'source-serif-4', 400, 'normal'), ('Source Serif 4', 'source-serif-4', 400, 'italic'),
                   ('Source Serif 4', 'source-serif-4', 600, 'normal')])
A_CSS = r'''
.skin-a{--f-d:'Playfair Display',Georgia,'Times New Roman',serif;--f-b:'Source Serif 4',Georgia,'Times New Roman',serif;--rule:#C3CEDA}
.skin-a .sh-app,.skin-a .sh-m,.skin-a .lp{font-family:var(--f-b)}
.skin-a .sh-app *,.skin-a .sh-m *{font-variant-numeric:lining-nums}
.skin-a button,.skin-a input,.skin-a textarea{font-family:inherit}
.skin-a :focus-visible{outline:2px solid var(--hi);outline-offset:2px}
/* rail: the book's thumb index */
.skin-a .sh-rail{border-right:1px solid var(--ink);box-shadow:inset -3px 0 0 var(--card),inset -4px 0 0 var(--line),inset -7px 0 0 var(--card),inset -8px 0 0 var(--line)}
.skin-a .sh-rail .sh-home{background:var(--card);color:var(--hi);border:1px solid var(--ink);box-shadow:0 0 0 3px var(--g),0 0 0 4px var(--ink)}
.skin-a .sh-rail .sh-home[aria-current=page]{background:var(--ink);color:var(--card)}
.skin-a .sh-rail a.sh-tab{border:1px solid var(--ink);border-left:0;font-size:12.5px;font-weight:600;letter-spacing:.07em;text-transform:uppercase}
.skin-a .sh-rail a.sh-tab .ix{writing-mode:horizontal-tb;transform:rotate(180deg);width:22px;height:22px;border-radius:50%;border:1px solid currentColor;display:flex;align-items:center;justify-content:center;font:italic 400 13px var(--f-d);letter-spacing:0;text-transform:none}
.skin-a .sh-rail a.sh-tab.is-cur{background:var(--ink);color:var(--card)}
.skin-a .sh-rail a.sh-tab.is-cur .ix{background:var(--hi);border-color:var(--hi);color:#fff}
/* header */
.skin-a .sh-bar{border-bottom:3px double var(--ink)}
.skin-a .sh-t{font:700 30px/1 var(--f-d);color:var(--ink)}
.skin-a .sh-bar small{font:italic 400 15px var(--f-b);color:var(--mut)}
.skin-a .sh-btn-o{background:transparent;border:1px solid var(--ink);border-radius:0;color:var(--ink);font-weight:600;font-size:13.5px}
.skin-a .sh-btn-g{background:var(--ink);border:0;border-radius:0;color:var(--card);font-weight:600;font-size:13.5px;box-shadow:inset 0 -3px 0 var(--hi)}
/* chat: a cloth-bound book */
.skin-a .sh-panel{border-radius:2px;color:#F6F0DE;box-shadow:inset 0 0 0 7px var(--panel),inset 0 0 0 8px rgba(246,240,222,.28)}
.skin-a .sh-ph{border-bottom:1px solid rgba(246,240,222,.2);margin:0 8px;padding:18px 14px}
.skin-a .sh-av{border-radius:50%;border:1px solid var(--hi-dark);color:var(--hi-dark);font:italic 400 24px var(--f-d);box-shadow:inset 0 0 0 3px var(--panel),inset 0 0 0 4px var(--hi-dark)}
.skin-a .sh-tname{font:700 26px/1 var(--f-d)}
.skin-a .sh-tsub{font-size:12.5px;font-style:italic;color:rgba(246,240,222,.72)}
.skin-a .sh-pb{padding:20px 22px}
.skin-a .sh-tm{color:var(--ink);border-radius:0;padding:11px 16px 11px 34px;line-height:22px;
 background:linear-gradient(90deg,transparent 21px,var(--hi) 21px 22px,transparent 22px 25px,var(--hi) 25px 26px,transparent 26px),repeating-linear-gradient(var(--card) 0 21px,var(--rule) 21px 22px);background-position:0 0,0 11px}
.skin-a .sh-lab{font-size:12px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:rgba(246,240,222,.72)}
.skin-a .sh-note{font:italic 400 28px/1.15 var(--f-d);color:var(--hi-dark)}
.skin-a .sh-pt{background:transparent;border:0;border-bottom:1px solid rgba(246,240,222,.22);border-radius:0;color:#F6F0DE;padding:6px 4px;font-size:14px}
.skin-a .sh-pt i{border:1px solid rgba(246,240,222,.5);border-radius:50%;font:italic 400 13px var(--f-d)}
.skin-a .sh-pt[aria-pressed=true]{background:var(--hi-dark);color:var(--panel);font-weight:600}
.skin-a .sh-pt[aria-pressed=true] i{border-color:var(--panel)}
.skin-a .sh-pr{background:transparent;border:0;border-bottom:1px dotted rgba(246,240,222,.45);border-radius:0;color:#F6F0DE;padding:8px 4px;font-size:14px;font-style:italic}
.skin-a .sh-pr svg{color:var(--hi-dark);flex-shrink:0}
.skin-a .sh-inp{background:rgba(0,0,0,.2);border-top:1px solid rgba(246,240,222,.2);margin:0 8px 8px}
.skin-a .sh-inp textarea{background:var(--card);color:var(--ink);border-radius:0;font-family:var(--f-b);font-size:14.5px}
.skin-a .sh-ib{color:#F6F0DE}
.skin-a .sh-send{border-radius:0;background:var(--hi-dark);color:var(--panel)}
/* phone frame */
.skin-a .sh-mt{border-bottom:3px double var(--ink)}
.skin-a .sh-homem{background:var(--card);color:var(--hi);border:1px solid var(--ink);box-shadow:0 0 0 2px var(--g),0 0 0 3px var(--ink)}
.skin-a .sh-homem[aria-current=page]{background:var(--ink);color:var(--card)}
.skin-a .sh-mtn{font:700 22px/1 var(--f-d)}.skin-a .sh-mts{font-style:italic;color:var(--mut)}
.skin-a .sh-mt .sh-btn-o{min-height:40px}
.skin-a .sh-who{letter-spacing:.14em;text-transform:uppercase;color:var(--mut)}
.skin-a .sh-who .sh-av{border-color:var(--ink);color:var(--ink);box-shadow:none;font-size:16px}
.skin-a .sh-mpanel{border-radius:2px;color:#F6F0DE;box-shadow:inset 0 0 0 5px var(--panel),inset 0 0 0 6px rgba(246,240,222,.28)}
.skin-a .sh-mi{background:var(--panel)}
.skin-a .sh-mi .sh-box{background:var(--card);border-radius:0}
.skin-a .sh-mi input{color:var(--ink);font-family:var(--f-b)}
.skin-a .sh-mi .sh-ib{color:var(--ink)}
.skin-a .sh-mf{background:var(--panel);color:rgba(246,240,222,.85);border-top:1px solid rgba(246,240,222,.25)}
.skin-a .sh-mf a{color:inherit}
.skin-a .sh-mf a[aria-current=page]{color:var(--hi-dark);box-shadow:inset 0 3px 0 var(--hi-dark)}
/* page parts */
.skin-a.bm{background-image:linear-gradient(90deg,transparent 17px,var(--hi) 17px 18px,transparent 18px 21px,var(--hi) 21px 22px,transparent 22px)}
.skin-a .bm-mast{border-bottom:3px double var(--ink)}
.skin-a .bm-emb{background:var(--card);border-radius:50%;box-shadow:0 0 0 1px var(--ink),inset 0 0 0 4px var(--card),inset 0 0 0 5px var(--ink)}
.skin-a .bm-kick{font-size:13.5px;font-weight:400;font-style:italic}
.skin-a .bm-name{font:700 46px/1.04 var(--f-d);white-space:normal;max-width:560px;letter-spacing:-.005em}
.skin-a .lp-stamp-at{font-size:13.5px}.skin-a .lp-stamp-since{font-size:13px;font-style:italic}
.skin-a .lp-refresh{border-radius:0;border:1px solid var(--ink);font-weight:600;font-size:14px}
.skin-a .bm-claim{font:700 38px/1.12 var(--f-d)}
.skin-a .bm-deck{font-size:16px}
.skin-a .bm-sech{border-bottom:1px solid var(--ink);padding-bottom:7px}
.skin-a .bm-lab{font-size:13px;font-weight:600;letter-spacing:.14em;text-transform:uppercase}
.skin-a .bm-labsub{font-style:italic;font-size:13.5px}
.skin-a .bm-tag{border-radius:0;font-size:12px;font-style:italic;font-weight:600}
.skin-a .bm-pend{gap:0 36px}
.skin-a .bm-pi{font-size:15px;padding:9px 0;border-bottom:1px solid var(--rule)}
.skin-a .bm-pm{border:1px solid var(--ink);border-radius:0;width:15px;height:15px;margin-top:4px}
.skin-a .bm-pi.wait .bm-pm{border:1.5px dashed var(--amber)}
.skin-a .bm-need{font-style:italic;font-weight:600}
.skin-a .lp-act{border-radius:0;border:1px solid var(--ink);background:var(--card)}
.skin-a .lp-act-k{font:700 18px/1.2 var(--f-d)}.skin-a .lp-act-d{font-size:14px;font-style:italic}
.skin-a.lp .lp-act-go{background:var(--ink);color:var(--card);box-shadow:inset 0 -4px 0 var(--hi);padding-left:18px}
.skin-a .bm-open{border-radius:0;border:1px solid var(--ink);font-weight:600;font-size:14px}
.skin-a .js-sel.is-up{transform:translate(-3px,-3px);box-shadow:0 0 0 1.5px var(--hi),5px 5px 0 var(--ink) !important}
.skin-a .js-sel:not(.is-up):hover{transform:translate(-1px,-1px);box-shadow:2px 2px 0 var(--line)}
.skin-a .is-lit{outline:3px solid var(--hi) !important;outline-offset:3px;border-radius:0}
@container lp (max-width:699px){
 .skin-a.bm{background-image:linear-gradient(90deg,transparent 6px,var(--hi) 6px 7px,transparent 7px 9px,var(--hi) 9px 10px,transparent 10px)}
 .skin-a .bm-name{font-size:40px}
 .skin-a .bm-claim{font-size:32px}
 .skin-a .bm-pi{font-size:14.5px}
}
'''
A = {'key': 'a', 'cls': 'skin-a', 'fonts': A_FONTS, 'css': A_CSS,
     'rail_inner': lambda i, n, d, cur: '<span>%s</span><b class="ix">%s</b>' % (n, n[0]),
     'foot_word': lambda n: ''}

# ==========================================================================================
# B · THE TILL ROLL
B_FONTS = C.fonts([('Space Mono', 'space-mono', 400, 'normal'), ('Space Mono', 'space-mono', 700, 'normal'),
                   ('Space Grotesk', 'space-grotesk', 400, 'normal'), ('Space Grotesk', 'space-grotesk', 500, 'normal'),
                   ('Space Grotesk', 'space-grotesk', 600, 'normal')])
ZIG = 'conic-gradient(from 135deg at top,#0000,#000 1deg 89deg,#0000 90deg) top/14px 51% repeat-x,conic-gradient(from -45deg at bottom,#0000,#000 1deg 89deg,#0000 90deg) bottom/14px 51% repeat-x'
ZIG_B = 'linear-gradient(#000 0 0) top/100% calc(100% - 7px) no-repeat,conic-gradient(from -45deg at bottom,#0000,#000 1deg 89deg,#0000 90deg) bottom/14px 7px repeat-x'
NOTCH = 'radial-gradient(circle 7px at 50% 0,#0000 97%,#000) top/100% 51% no-repeat,radial-gradient(circle 7px at 50% 100%,#0000 97%,#000) bottom/100% 51% no-repeat'
NOTCH_X = 'radial-gradient(circle 8px at 0 50%,#0000 97%,#000) left/51% 100% no-repeat,radial-gradient(circle 8px at 100% 50%,#0000 97%,#000) right/51% 100% no-repeat'
B_CSS = r'''
.skin-b{--f-d:'Space Mono',ui-monospace,Menlo,Consolas,monospace;--f-b:'Space Grotesk',system-ui,'Segoe UI',sans-serif;--zig:@ZIG@;--zigb:@ZIGB@;--notch:@NOTCH@;--notchx:@NOTCHX@}
.skin-b .sh-app,.skin-b .sh-m,.skin-b .lp{font-family:var(--f-b);font-variant-numeric:tabular-nums}
.skin-b button,.skin-b input,.skin-b textarea{font-family:inherit}
.skin-b :focus-visible{outline:2px dashed var(--hi);outline-offset:3px}
.skin-b .sh-app,.skin-b .sh-m{background-image:radial-gradient(rgba(0,0,0,.09) 1px,transparent 1.3px);background-size:16px 16px}
/* rail: tear-off tickets */
.skin-b .sh-rail{border-right:2px dashed rgba(38,35,46,.35);gap:8px}
.skin-b .sh-rail .sh-home{border-radius:50%;background:var(--ink);color:var(--card);box-shadow:0 0 0 3px var(--g),0 0 0 5px var(--ink)}
.skin-b .sh-rail .sh-home[aria-current=page]{background:var(--hi);box-shadow:0 0 0 3px var(--g),0 0 0 5px var(--hi)}
.skin-b .sh-rail a.sh-tab{-webkit-mask:var(--notch);mask:var(--notch);font:700 12px var(--f-d);letter-spacing:.06em;text-transform:uppercase;gap:10px}
.skin-b .sh-rail a.sh-tab .ix{writing-mode:horizontal-tb;transform:rotate(180deg);font:400 11px var(--f-d);padding:2px 0;border-top:1.5px dashed currentColor;border-bottom:1.5px dashed currentColor}
.skin-b .sh-rail a.sh-tab.is-cur{background:var(--ink);color:var(--card)}
.skin-b .sh-rail a.sh-tab.is-cur .ix{color:var(--hi-dark)}
/* header */
.skin-b .sh-bar{border-bottom:2px dashed var(--ink)}
.skin-b .sh-t{font:700 24px/1 var(--f-d);text-transform:uppercase;letter-spacing:-.01em}
.skin-b .sh-bar small{font:400 12.5px var(--f-d);text-transform:uppercase;color:var(--mut)}
.skin-b .sh-bar small::before{content:"/ "}
.skin-b .sh-btn-o{background:var(--card);border:1.5px solid var(--ink);border-radius:0;color:var(--ink);font:700 12px var(--f-d);text-transform:uppercase}
.skin-b .sh-btn-g{background:var(--hi);border:0;border-radius:0;color:#fff;font:700 12px var(--f-d);text-transform:uppercase}
/* chat: the till, printing slips */
.skin-b .sh-panel{border-radius:4px;color:#ECE9F2;box-shadow:inset 0 3px 0 rgba(255,255,255,.08)}
.skin-b .sh-ph{border-bottom:2px dashed rgba(236,233,242,.25)}
.skin-b .sh-av{border-radius:0;background:var(--hi-dark);color:var(--panel);font:700 22px var(--f-d)}
.skin-b .sh-tname{font:700 22px/1 var(--f-d);text-transform:uppercase}
.skin-b .sh-tsub{font:400 11.5px var(--f-d);color:#BDB8C8;text-transform:uppercase}
.skin-b .sh-tm{background:var(--card);color:var(--ink);padding:16px 16px 22px;-webkit-mask:var(--zigb);mask:var(--zigb);font-size:14px}
.skin-b .sh-lab{font:400 11.5px var(--f-d);letter-spacing:.06em;text-transform:uppercase;color:#BDB8C8}
.skin-b .sh-lab::before{content:"-- "}
.skin-b .sh-note{display:inline-block;font:700 19px/1.3 var(--f-d);text-transform:uppercase;color:var(--hi-dark);border:3px double var(--hi-dark);padding:8px 12px;transform:rotate(-2deg);margin:4px 0 4px 4px}
.skin-b .sh-pt{background:transparent;border:1.5px dashed rgba(236,233,242,.32);border-radius:0;color:#ECE9F2;padding:6px 12px 6px 6px;font-size:13.5px}
.skin-b .sh-pt i{background:var(--card);color:var(--ink);border-radius:0;font:700 12px var(--f-d)}
.skin-b .sh-pt[aria-pressed=true]{background:var(--hi-dark);color:var(--panel);border-style:solid;border-color:var(--hi-dark);font-weight:600}
.skin-b .sh-pt[aria-pressed=true] i{background:var(--panel);color:var(--hi-dark)}
.skin-b .sh-pr{background:transparent;border:0;border-top:1.5px dashed rgba(236,233,242,.25);border-radius:0;color:#ECE9F2;padding:8px 4px;font-size:13.5px}
.skin-b .sh-pr span::before{content:"> ";font-family:var(--f-d);color:var(--hi-dark)}
.skin-b .sh-pr svg{color:var(--hi-dark);flex-shrink:0}
.skin-b .sh-inp{background:rgba(0,0,0,.25);border-top:2px dashed rgba(236,233,242,.25)}
.skin-b .sh-inp textarea{background:var(--card);color:var(--ink);border-radius:0;font-size:14px}
.skin-b .sh-ib{color:#ECE9F2}
.skin-b .sh-send{border-radius:0;background:var(--hi-dark);color:var(--panel)}
/* phone frame */
.skin-b .sh-mt{border-bottom:2px dashed var(--ink)}
.skin-b .sh-homem{border-radius:50%;background:var(--ink);color:var(--card)}
.skin-b .sh-homem[aria-current=page]{background:var(--hi);color:#fff}
.skin-b .sh-mtn{font:700 20px/1 var(--f-d);text-transform:uppercase}.skin-b .sh-mts{font:400 11px var(--f-d);text-transform:uppercase;color:var(--mut)}
.skin-b .sh-mt .sh-btn-o{min-height:40px}
.skin-b .sh-who{font:700 12px var(--f-d);text-transform:uppercase;color:var(--mut)}
.skin-b .sh-who .sh-av{font-size:14px}
.skin-b .sh-mpanel{border-radius:4px;color:#ECE9F2}
.skin-b .sh-mi{background:var(--panel)}
.skin-b .sh-mi .sh-box{background:var(--card);border-radius:0}
.skin-b .sh-mi input{color:var(--ink)}
.skin-b .sh-mi .sh-ib{color:var(--ink)}
.skin-b .sh-mf{background:var(--panel);color:#ECE9F2;border-top:2px dashed rgba(236,233,242,.25)}
.skin-b .sh-mf a{color:inherit}
.skin-b .sh-mf a[aria-current=page]{color:var(--hi-dark);box-shadow:inset 0 -3px 0 var(--hi-dark)}
/* page parts */
.skin-b .bm-mast{border-bottom:2px dashed var(--ink)}
.skin-b .bm-emb{border-radius:0;background:var(--ink);box-shadow:inset 0 0 0 4px var(--ink),inset 0 0 0 5.5px var(--card)}
.skin-b .bm-kick{font:400 12px var(--f-d);text-transform:uppercase;letter-spacing:.02em}
.skin-b .bm-name{font:700 42px/1.02 var(--f-d);text-transform:uppercase;letter-spacing:-.035em;white-space:normal;max-width:600px}
.skin-b .lp-stamp-at{font:700 12.5px var(--f-d);text-transform:uppercase}.skin-b .lp-stamp-since{font:400 12px var(--f-d)}
.skin-b .lp-refresh{border-radius:0;border:1.5px solid var(--ink);font:700 12.5px var(--f-d);text-transform:uppercase}
.skin-b .bm-claim{font:700 34px/1.18 var(--f-d);letter-spacing:-.03em}
.skin-b .bm-deck{font-size:15.5px}
.skin-b .bm-sech{border-bottom:2px dashed var(--ink);padding-bottom:7px}
.skin-b .bm-lab{font:700 13px var(--f-d);text-transform:uppercase}
.skin-b .bm-lab::before{content:"## "}
.skin-b .bm-labsub{font-size:13px}
.skin-b .bm-tag{border-radius:0;font:700 10.5px var(--f-d);text-transform:uppercase;letter-spacing:.02em}
.skin-b .bm-sec-pend .bm-pend{background:var(--card);padding:26px 26px 30px;-webkit-mask:var(--zig);mask:var(--zig);filter:none}
.skin-b .bm-pi{font-size:14.5px}
.skin-b .bm-pm{border-radius:0;border:2px solid var(--ink)}
.skin-b .bm-need{font:700 11.5px var(--f-d);text-transform:uppercase}
.skin-b .lp-act{border:0;border-radius:0;background:var(--card);-webkit-mask:var(--notchx);mask:var(--notchx);padding:10px 26px}
.skin-b .lp-act-k{font:700 14px var(--f-d);text-transform:uppercase}.skin-b .lp-act-d{font-size:13.5px}
.skin-b.lp .lp-act-go{background:var(--ink);color:var(--card);box-shadow:inset 0 5px 0 var(--hi);padding-left:26px}
.skin-b .bm-open{border-radius:0;border:1.5px solid var(--ink);font:700 12.5px var(--f-d);text-transform:uppercase}
.skin-b .js-sel.is-up{transform:translateY(-7px) rotate(-1.2deg);box-shadow:none !important;filter:drop-shadow(0 0 0 var(--hi)) drop-shadow(0 16px 14px rgba(0,0,0,.28))}
.skin-b .js-sel:not(.is-up):hover{transform:translateY(-2px);box-shadow:none}
.skin-b .is-lit{outline:3px dashed var(--hi) !important;outline-offset:4px;border-radius:0}
@container lp (max-width:699px){
 .skin-b .bm-name{font-size:34px}
 .skin-b .bm-claim{font-size:26px}
 .skin-b .bm-sec-pend .bm-pend{padding:22px 16px 26px}
 .skin-b .lp-act{padding:10px 22px}
}
'''.replace('@ZIG@', ZIG).replace('@ZIGB@', ZIG_B).replace('@NOTCH@', NOTCH).replace('@NOTCHX@', NOTCH_X)
B_SKIN = {'key': 'b', 'cls': 'skin-b', 'fonts': B_FONTS, 'css': B_CSS,
          'rail_inner': lambda i, n, d, cur: '<span>%s</span><b class="ix">%02d</b>' % (n, i),
          'foot_word': lambda n: ''}

# ==========================================================================================
# C · THE ANNUAL REPORT
C_FONTS = C.fonts([('Inter Tight', 'inter-tight', 400, 'normal'), ('Inter Tight', 'inter-tight', 500, 'normal'),
                   ('Inter Tight', 'inter-tight', 600, 'normal'), ('Inter Tight', 'inter-tight', 800, 'normal'),
                   ('Instrument Serif', 'instrument-serif', 400, 'italic')])
C_CSS = r'''
.skin-c{--f-d:'Inter Tight','Helvetica Neue',Arial,sans-serif;--f-b:'Inter Tight','Helvetica Neue',Arial,sans-serif;--f-n:'Instrument Serif',Georgia,serif}
.skin-c .sh-app,.skin-c .sh-m,.skin-c .lp{font-family:var(--f-b);font-variant-numeric:tabular-nums}
.skin-c button,.skin-c input,.skin-c textarea{font-family:inherit}
.skin-c :focus-visible{outline:3px solid var(--ink);outline-offset:2px}
/* rail: flat numbered bars */
.skin-c .sh-rail{border-right:1px solid var(--ink);gap:3px}
.skin-c .sh-rail .sh-home{border-radius:0;background:var(--ink);color:var(--hi)}
.skin-c .sh-rail .sh-home[aria-current=page]{box-shadow:6px 6px 0 var(--hi)}
.skin-c .sh-rail a.sh-tab{font:600 13.5px var(--f-b);letter-spacing:-.005em;justify-content:space-between;padding:12px 0}
.skin-c .sh-rail a.sh-tab .ix{font:800 12px var(--f-d)}
.skin-c .sh-rail a.sh-tab.is-cur{background:var(--ink);color:var(--card);box-shadow:inset 6px 0 0 var(--hi)}
/* header */
.skin-c .sh-bar{border-bottom:1px solid var(--ink)}
.skin-c .sh-t{font:800 28px/1 var(--f-d);letter-spacing:-.035em}
.skin-c .sh-bar small{font:500 14px var(--f-b);color:var(--mut)}
.skin-c .sh-bar small::before{content:"— "}
.skin-c .sh-btn-o{background:transparent;border:1px solid var(--ink);border-radius:0;color:var(--ink);font-weight:600;font-size:13.5px}
.skin-c .sh-btn-g{background:var(--hi);border:0;border-radius:0;color:var(--ink);font-weight:800;font-size:13.5px}
/* chat: flat black, editorial */
.skin-c .sh-chat{padding:0}
.skin-c .sh-panel{border-radius:0;color:#ECECE6}
.skin-c .sh-ph{border-bottom:1px solid rgba(236,236,230,.16);padding:22px 26px}
.skin-c .sh-av{border-radius:0;background:var(--hi);color:var(--ink);font:800 22px var(--f-d)}
.skin-c .sh-tname{font:800 26px/1 var(--f-d);letter-spacing:-.03em}
.skin-c .sh-tsub{font-size:12.5px;color:#A9AAA3}
.skin-c .sh-pb{padding:22px 26px;gap:20px}
.skin-c .sh-tm{font-size:15px;line-height:1.55;color:#ECECE6;gap:10px}
.skin-c .sh-lab{font-size:12px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:#A9AAA3}
.skin-c .sh-notewrap{border-top:1px solid rgba(236,236,230,.16);padding-top:14px}
.skin-c .sh-note{font:italic 400 32px/1.08 var(--f-n);color:var(--hi-dark)}
.skin-c .sh-col{gap:0}
.skin-c .sh-col .sh-lab{margin-bottom:6px}
.skin-c .sh-pt{background:transparent;border:0;border-top:1px solid rgba(236,236,230,.16);border-radius:0;color:#ECECE6;padding:6px 0;font-size:14px}
.skin-c .sh-pt i{font:800 15px var(--f-d);color:var(--hi-dark);justify-content:flex-start}
.skin-c .sh-pt[aria-pressed=true]{background:var(--hi-dark);color:var(--panel);font-weight:600;padding-left:8px}
.skin-c .sh-pt[aria-pressed=true] i{color:var(--panel)}
.skin-c .sh-pr{background:transparent;border:0;border-top:1px solid rgba(236,236,230,.16);border-radius:0;color:#ECECE6;padding:8px 0;font-size:14px}
.skin-c .sh-pr svg{color:var(--hi-dark);flex-shrink:0}
.skin-c .sh-inp{background:var(--panel);border-top:1px solid rgba(236,236,230,.16);padding:16px 26px 20px}
.skin-c .sh-inp textarea{background:#1E1F22;color:#ECECE6;border-radius:0;font-size:14.5px}
.skin-c .sh-inp textarea::placeholder{color:#A9AAA3}
.skin-c .sh-ib{color:#ECECE6}
.skin-c .sh-send{border-radius:0;background:var(--hi-dark);color:var(--panel)}
/* phone frame */
.skin-c .sh-mt{border-bottom:1px solid var(--ink)}
.skin-c .sh-homem{border-radius:0;background:var(--ink);color:var(--hi)}
.skin-c .sh-mtn{font:800 22px/1 var(--f-d);letter-spacing:-.03em}.skin-c .sh-mts{color:var(--mut);font-weight:500}
.skin-c .sh-mt .sh-btn-o{min-height:40px}
.skin-c .sh-who{letter-spacing:.1em;text-transform:uppercase;color:var(--mut)}
.skin-c .sh-who .sh-av{font-size:14px}
.skin-c .sh-mpanel{border-radius:0;color:#ECECE6}
.skin-c .sh-mi{background:var(--panel)}
.skin-c .sh-mi .sh-box{background:#1E1F22;border-radius:0}
.skin-c .sh-mi input{color:#ECECE6}
.skin-c .sh-mi input::placeholder{color:#A9AAA3}
.skin-c .sh-mi .sh-ib{color:#ECECE6}
.skin-c .sh-mf{background:var(--panel);color:#ECECE6;border-top:1px solid rgba(236,236,230,.16)}
.skin-c .sh-mf a{color:inherit}
.skin-c .sh-mf a[aria-current=page]{color:var(--ink);background:var(--hi-dark)}
/* page parts */
.skin-c.bm{counter-reset:sec}
.skin-c .bm-mast{border-bottom:6px solid var(--ink)}
.skin-c .bm-emb{border-radius:0;background:var(--ink);box-shadow:none}
.skin-c .bm-kick{font-size:12.5px;font-weight:600;letter-spacing:.08em;text-transform:uppercase}
.skin-c .bm-name{font:800 46px/1 var(--f-d);letter-spacing:-.04em;white-space:normal;max-width:620px}
.skin-c .lp-refresh{border-radius:0;border:1px solid var(--ink);font-weight:600;background:transparent}
.skin-c .bm-claim{font:800 40px/1.04 var(--f-d);letter-spacing:-.035em}
.skin-c .bm-deck{font-size:16px;color:var(--mut)}
.skin-c .bm-sec{border-top:1px solid var(--ink);padding-top:12px;counter-increment:sec}
.skin-c .bm-sech{margin-bottom:18px}
.skin-c .bm-lab{font:800 16px var(--f-d);letter-spacing:-.01em}
.skin-c .bm-lab::before{content:counter(sec,decimal-leading-zero);display:inline-block;min-width:40px;color:var(--mut)}
.skin-c .bm-labsub{font-size:13px}
.skin-c .bm-tag{border-radius:0;font-size:11px;font-weight:600;letter-spacing:.02em}
.skin-c .bm-tag.guess{border:0;background:var(--soft);color:var(--ink)}
.skin-c .bm-pend{gap:0 36px}
.skin-c .bm-pi{font-size:15px;padding:10px 0;border-top:1px solid var(--line)}
.skin-c .bm-pm{border-radius:0;border:0;background:var(--ink);width:10px;height:10px;margin-top:7px}
.skin-c .bm-pi.wait .bm-pm{background:transparent;border:2px dashed var(--amber)}
.skin-c .lp-act{border:0;border-top:4px solid var(--ink);border-radius:0;background:var(--card);padding:12px 18px}
.skin-c .lp-act-k{font:800 16px/1.2 var(--f-d);letter-spacing:-.01em}.skin-c .lp-act-d{font-size:13.5px}
.skin-c.lp .lp-act-go{background:var(--ink);color:var(--card);box-shadow:none;border-top-color:var(--hi);padding-left:18px}
.skin-c .bm-open{border-radius:0;border:1px solid var(--ink);font-weight:600}
.skin-c .js-sel.is-up{transform:translate(-4px,-4px);box-shadow:0 0 0 2px var(--ink),8px 8px 0 var(--hi) !important}
.skin-c .js-sel:not(.is-up):hover{transform:none;box-shadow:0 0 0 1px var(--ink)}
.skin-c .is-lit{outline:4px solid var(--hi) !important;outline-offset:3px;border-radius:0}
@container lp (max-width:699px){
 .skin-c .bm-name{font-size:40px}
 .skin-c .bm-claim{font-size:32px}
 .skin-c .bm-lab::before{min-width:32px}
}
'''
C_SKIN = {'key': 'c', 'cls': 'skin-c', 'fonts': C_FONTS, 'css': C_CSS,
          'rail_inner': lambda i, n, d, cur: '<span>%s</span><b class="ix">%02d</b>' % (n, i),
          'foot_word': lambda n: ''}

SKINS = {'a': A, 'b': B_SKIN, 'c': C_SKIN}

# ==========================================================================================
# V · ROUND TWO (8 Oct 2026): Avishek kept the Virevo type, and asked for C's clean look and
# colours with the ledger of A and the receipt of B. So the Financial identity now lives only in
# shapes, paper, marks, frame dress and drawings. Fonts and sizes are the Virevo ones (07 §2):
# Bebas Neue for names, claims and big numbers; Poppins for everything else; Caveat 700 for
# Tojo's Note and one-line hand notes. Sizes: name 48/42, claim 40/34, landing figures 24-30,
# body 14-15, labels 12-13 at 600, phone floors 14 / 11 / 10.5.
V_FONTS = C.B.embedded_fonts()
V_CSS = r'''
.skin-v{--f-d:'Bebas Neue',sans-serif;--f-b:'Poppins','Segoe UI',system-ui,sans-serif;--f-n:'Caveat',cursive;--rule:#D9DAD2;
 --zig:@ZIG@;--zigb:@ZIGB@}
.skin-v .sh-app,.skin-v .sh-m,.skin-v .lp{font-family:var(--f-b)}
.skin-v button,.skin-v input,.skin-v textarea{font-family:inherit}
.skin-v :focus-visible{outline:3px solid var(--ink);outline-offset:2px}
/* rail: flat numbered bars */
.skin-v .sh-rail{border-right:1px solid var(--ink);gap:3px}
.skin-v .sh-rail .sh-home{border-radius:0;background:var(--ink);color:var(--hi)}
.skin-v .sh-rail .sh-home[aria-current=page]{box-shadow:6px 6px 0 var(--hi)}
.skin-v .sh-rail a.sh-tab{font-size:13px;font-weight:600;letter-spacing:.09em;text-transform:uppercase;justify-content:space-between;padding:12px 0}
.skin-v .sh-rail a.sh-tab .ix{font:400 18px var(--f-d);letter-spacing:.02em}
.skin-v .sh-rail a.sh-tab.is-cur{background:var(--ink);color:var(--card);box-shadow:inset 6px 0 0 var(--hi)}
/* header */
.skin-v .sh-bar{border-bottom:1px solid var(--ink);gap:16px}
.skin-v .sh-bt{min-width:0}
.skin-v .sh-t{font:400 40px/1 var(--f-d)}
.skin-v .sh-bar small{font-size:13px;font-weight:600;letter-spacing:.09em;text-transform:uppercase;color:var(--mut)}
.skin-v .sh-btn-o{background:transparent;border:1.5px solid var(--ink);border-radius:0;color:var(--ink);font-weight:500}
.skin-v .sh-btn-g{background:var(--hi);border:0;border-radius:0;color:var(--ink);font-weight:600;letter-spacing:.05em;text-transform:uppercase}
/* chat: flat black */
.skin-v .sh-chat{padding:0}
.skin-v .sh-panel{border-radius:0;color:#ECECE6}
.skin-v .sh-ph{border-bottom:1px solid rgba(236,236,230,.16);padding:20px 26px}
.skin-v .sh-av{border-radius:0;background:var(--hi);color:var(--ink);font:400 24px var(--f-d)}
.skin-v .sh-tname{font:400 28px/1 var(--f-d)}
.skin-v .sh-tsub{font-size:12px;color:#A9AAA3}
.skin-v .sh-pb{padding:22px 26px;gap:18px}
.skin-v .sh-tm{font-size:14px;line-height:1.55;color:#ECECE6;gap:10px}
.skin-v .sh-lab{font-size:12px;font-weight:600;letter-spacing:.09em;text-transform:uppercase;color:#A9AAA3}
.skin-v .sh-notewrap{border-top:1px solid rgba(236,236,230,.16);padding-top:14px}
.skin-v .sh-note{font:700 31px/1.1 var(--f-n);color:var(--hi-dark)}
.skin-v .sh-col{gap:0}
.skin-v .sh-col .sh-lab{margin-bottom:6px}
.skin-v .sh-pt{background:transparent;border:0;border-top:1px solid rgba(236,236,230,.16);border-radius:0;color:#ECECE6;padding:6px 0}
.skin-v .sh-pt i{font:400 18px var(--f-d);color:var(--hi-dark);justify-content:flex-start}
.skin-v .sh-pt[aria-pressed=true]{background:var(--hi-dark);color:var(--panel);font-weight:600;padding-left:8px}
.skin-v .sh-pt[aria-pressed=true] i{color:var(--panel)}
.skin-v .sh-pr{background:transparent;border:0;border-top:1px solid rgba(236,236,230,.16);border-radius:0;color:#ECECE6;padding:8px 0}
.skin-v .sh-pr svg{color:var(--hi-dark);flex-shrink:0}
.skin-v .sh-inp{background:var(--panel);border-top:1px solid rgba(236,236,230,.16);padding:16px 26px 20px}
.skin-v .sh-inp textarea{background:#1E1F22;color:#ECECE6;border-radius:0}
.skin-v .sh-inp textarea::placeholder{color:#A9AAA3}
.skin-v .sh-ib{color:#ECECE6}
.skin-v .sh-send{border-radius:0;background:var(--hi-dark);color:var(--panel)}
/* phone frame */
.skin-v .sh-mt{border-bottom:1px solid var(--ink)}
.skin-v .sh-homem{border-radius:0;background:var(--ink);color:var(--hi)}
.skin-v .sh-mtn{font:400 24px/1 var(--f-d)}.skin-v .sh-mts{color:var(--mut)}
.skin-v .sh-mt .sh-btn-o{min-height:40px}
.skin-v .sh-who{letter-spacing:.09em;text-transform:uppercase;color:var(--mut)}
.skin-v .sh-who .sh-av{font-size:17px}
.skin-v .sh-mpanel{border-radius:0;color:#ECECE6}
.skin-v .sh-mi{background:var(--panel)}
.skin-v .sh-mi .sh-box{background:#1E1F22;border-radius:0}
.skin-v .sh-mi input{color:#ECECE6}
.skin-v .sh-mi input::placeholder{color:#A9AAA3}
.skin-v .sh-mi .sh-ib{color:#ECECE6}
.skin-v .sh-mf{background:var(--panel);color:#ECECE6;border-top:1px solid rgba(236,236,230,.16)}
.skin-v .sh-mf a{color:inherit}
.skin-v .sh-mf a[aria-current=page]{color:var(--ink);background:var(--hi-dark)}
/* page parts: Virevo type, Financial shapes */
.skin-v.bm{counter-reset:sec}
.skin-v .bm-mast{border-bottom:6px solid var(--ink)}
.skin-v .bm-emb{border-radius:0;background:var(--ink);box-shadow:none}
.skin-v .bm-name{font-size:48px;white-space:normal}
.skin-v .lp-refresh{border-radius:0;background:transparent}
.skin-v .bm-claim{font-size:40px;line-height:1.02}
.skin-v .bm-sec{border-top:1px solid var(--ink);padding-top:12px;counter-increment:sec}
.skin-v .bm-sech{margin-bottom:16px}
.skin-v .bm-lab::before{content:counter(sec,decimal-leading-zero);display:inline-block;min-width:36px;font:400 22px/1 var(--f-d);color:var(--mut);vertical-align:-2px}
.skin-v .bm-tag{border-radius:0}
.skin-v .bm-tag.guess{border:0;background:var(--soft);color:var(--ink)}
.skin-v .bm-pend{gap:0 36px}
.skin-v .bm-pi{padding:10px 0;border-top:1px solid var(--line)}
.skin-v .bm-pm{border-radius:0;border:2px solid var(--ink);width:15px;height:15px;margin-top:4px}
.skin-v .bm-pi.wait .bm-pm{border:2px dashed var(--amber)}
.skin-v .lp-act{border:0;border-top:4px solid var(--ink);border-radius:0;background:var(--card)}
.skin-v.lp .lp-act-go{background:var(--ink);color:var(--card);box-shadow:none;border-top-color:var(--hi);padding-left:18px}
.skin-v .bm-open{border-radius:0;border:1.5px solid var(--ink)}
.skin-v .js-sel.is-up{transform:translate(-4px,-4px);box-shadow:0 0 0 2px var(--ink),8px 8px 0 var(--hi) !important}
.skin-v .js-sel:not(.is-up):hover{transform:none;box-shadow:0 0 0 1px var(--ink)}
.skin-v .is-lit{outline:4px solid var(--hi) !important;outline-offset:3px;border-radius:0}
.skin-v p,.skin-v li,.skin-v b,.skin-v span{overflow-wrap:anywhere}
@container lp (max-width:699px){
 .skin-v .bm-name{font-size:42px}
 .skin-v .bm-claim{font-size:34px}
 .skin-v .bm-lab::before{min-width:30px}
}
'''.replace('@ZIG@', ZIG).replace('@ZIGB@', ZIG_B)
V_SKIN = {'key': 'v', 'cls': 'skin-v', 'fonts': V_FONTS, 'css': V_CSS,
          'rail_inner': lambda i, n, d, cur: '<span>%s</span><b class="ix">%02d</b>' % (n, i),
          'foot_word': lambda n: ''}
SKINS.update({'d': V_SKIN, 'e': V_SKIN, 'f': V_SKIN})
