import re
app=open('src/app.html').read()
a='<div class="ni"><svg class="ic" viewBox="0 0 24 24"><path d="M4 5h16v11H9l-5 4z"/></svg>Chat'
assert a in app; app=app.replace(a,'<div class="ni" id="niChat"><svg class="ic" viewBox="0 0 24 24"><path d="M4 5h16v11H9l-5 4z"/></svg>Chat',1)
app=app.replace('<div class="app locked" id="app">','<div class="app locked" id="app" data-view="home">',1)
# insert thread before the closing of .main (second-to-last </div>)
last=app.rfind('</div>'); second=app.rfind('</div>',0,last)
tool=open('src/tool.html').read().replace('{{GENERIC}}',open('src/generic.html').read())+open('src/levels.html').read()
app=app[:second]+open('src/thread.html').read()+tool+'        '+app[second:]
s=open('src/shell.html').read()
css=open('src/thread.css').read()+open('src/tool.css').read()+open('src/levels.css').read()+"\n.sub a.cur{color:#fff;background:#12301e;border-radius:0 8px 8px 0}\n"+"\n.tchat{position:relative}\n"
s=s.replace('{{APPCSS}}',open('src/app.css').read()).replace('{{THREADCSS}}',css).replace('{{APP}}',app).replace('{{JS}}',open('src/tours.js').read())
import base64,json
L='live/'
h=open(L+'discharge.html').read()
font='data:font/ttf;base64,'+base64.b64encode(open(L+'BebasNeue-Regular.ttf','rb').read()).decode()
css=open(L+'discharge.css').read().replace("url('../../fonts/BebasNeue-Regular.ttf?v=1')","url('"+font+"')")
rep=[('<link rel="icon" href="Images/fav_icon.webp" type="image/webp">',''),
 ('<link rel="stylesheet" href="assets/css/discharge.css?v=39">','<style>'+css+'</style>'),
 ('<link rel="stylesheet" href="assets/css/credits.css?v=1">','<style>'+open(L+'credits.css').read()+'</style>'),
 ('<script src="assets/js/discharge.js?v=23" defer></script>','<script>'+open(L+'discharge.js').read()+'</script>'),
 ('<script src="assets/js/credits.js?v=1" defer></script>','<script>'+open(L+'credits.js').read()+'</script>'+open('src/toolhook.html').read())]
for a,c in rep:
    assert a in h, a; h=h.replace(a,c)
h=h[:h.index('</body>')+7]+'\n</html>\n'
s=s.replace('{{TOOLDOC}}',json.dumps(h).replace('</','<\\/').replace('<!--','<\\u0021--').replace('<script','<\\u0073cript'))
S='live/sim/'
sh=open(S+'simulation.html').read()
rep=[('<link rel="icon" type="image/webp" href="Images/fav_icon.webp">',''),('<link rel="icon" type="image/png" href="Images/fav_icon.png">',''),('<link rel="apple-touch-icon" href="Images/fav_icon.png">',''),
 ('<link rel="stylesheet" href="assets/css/simulation.css?v=3">','<style>'+open(S+'simulation.css').read()+'</style>'),
 ('<script src="assets/js/simulation.js?v=7" defer></script>','<script>'+open(S+'simulation.js').read()+'</script>'),
 ('<script src="assets/js/genie.js?v=3" defer></script>','<script>'+open(S+'genie.js').read()+'</script>'+open('src/simhook.html').read())]
for a,c in rep:
    assert a in sh, a; sh=sh.replace(a,c)
sh=sh[:sh.index('</body>')+7]+'\n</html>\n'
s=s.replace('{{SIMDOC}}',json.dumps(sh).replace('</','<\\/').replace('<!--','<\\u0021--').replace('<script','<\\u0073cript'))
U='live/suites/'
docs={}
for k,f in [('discharge','discharge-summary'),('billing','billing-insurance'),('admission','admission-process'),('diagnostic','diagnostic-scheduling'),('procurement','procurement')]:
    docs[k]='<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head><body>'+open(U+f+'-suite-landing.html').read()+open('src/suitehook.html').read()+'</body></html>'
s=s.replace('{{SUITEDOCS}}',json.dumps(docs).replace('</','<\\/').replace('<!--','<\\u0021--').replace('<script','<\\u0073cript'))
open('tojo-tours.html','w').write(s)
print(len(s))
