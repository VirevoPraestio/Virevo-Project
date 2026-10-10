// Every file AB changed since a merge, under its first matching entry of SEGREGATION.json (Tools Design package).
// Usage: node tools/check-map.js <commit-before-the-merge>   (UNMATCHED lines are files the map does not place yet)
const { execSync } = require('child_process');
const s = require('D:/Git_Virevo/Virevo-Project/SEGREGATION.json');
const td = s.packages['Tools Design'];
const from = process.argv[2] || '6fe8300';
const files = execSync(`git -C D:/Git_Virevo/Virevo-Project diff --name-only ${from} HEAD -- "Tools Design"`, { encoding: 'utf8' })
  .trim().split('\n').map(f => f.replace(/^Tools Design\//, ''));
const esc = c => '.+^$()|[]\\'.includes(c) ? '\\' + c : c;
function rx(g) {
  let r = '';
  for (let i = 0; i < g.length; i++) {
    const c = g[i];
    if (c === '*' && g[i + 1] === '*') { r += '.*'; i++; }
    else if (c === '*') r += '[^/]*';
    else if (c === '{') { const j = g.indexOf('}', i); r += '(' + g.slice(i + 1, j).split(',').map(x => [...x].map(esc).join('')).join('|') + ')'; i = j; }
    else r += esc(c);
  }
  return new RegExp('^' + r + '$');
}
const counts = {};
for (const f of files) {
  const e = td.find(e => rx(e.match).test(f));
  const k = e ? e.bucket.padEnd(5) + ' <- ' + e.match : 'UNMATCHED ' + f;
  counts[k] = (counts[k] || 0) + 1;
}
for (const [k, v] of Object.entries(counts)) console.log(String(v).padStart(4), k);
