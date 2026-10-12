#!/bin/bash
cd "$(dirname "$0")"
{ cat 00-head.html; echo "<script>"; cat 10-data.js 15-helpers.js 20-shared.js 33-diorama.js 90-init.js; echo "</script>"; } > page-c.html
sed -n '1,/<\/style><\/head><body>/p' preview.html > preview-c.html; grep -v 'fonts.g' page-c.html >> preview-c.html; echo '</body></html>' >> preview-c.html
