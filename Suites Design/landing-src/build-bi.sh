#!/bin/bash
cd "$(dirname "$0")"
{ python3 -c "import re,sys;print(re.sub(r'<title>.*?</title>','<title>Billing &amp; Insurance Suite</title>',open('00-head.html').read()),end='')"; echo "<script>"; cat 12-data-billing.js 15-helpers.js 16-ticker.js 20-shared.js 36-tubes.js 37-meters.js 38-sorter.js 90-init.js; echo "</script>"; } > page-bi.html
sed -n '1,/<\/style><\/head><body>/p' preview.html > preview-bi.html; grep -v 'fonts.g' page-bi.html >> preview-bi.html; echo '</body></html>' >> preview-bi.html
