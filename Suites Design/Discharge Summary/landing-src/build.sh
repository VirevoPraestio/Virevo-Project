#!/bin/bash
cd "$(dirname "$0")"
{ cat 00-head.html; echo "<script>"; cat 10-data.js 20-shared.js 3*.js 90-init.js; echo "</script>"; } > page.html
{ echo '<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><style>
@font-face{font-family:"Bebas Neue";src:url(file:///mnt/user-data/uploads/Discharge/tojo-html/diagnosis-html-generator/assets/fonts/bebas-neue-latin-400-normal.woff2)}
@font-face{font-family:"Caveat";font-weight:500 700;src:url(file:///mnt/user-data/uploads/Discharge/tojo-html/diagnosis-html-generator/assets/fonts/caveat-latin-700-normal.woff2)}
@font-face{font-family:"Poppins";font-weight:400;src:url(file:///mnt/user-data/uploads/Discharge/tojo-html/diagnosis-html-generator/assets/fonts/poppins-latin-400-normal.woff2)}
@font-face{font-family:"Poppins";font-weight:500;src:url(file:///mnt/user-data/uploads/Discharge/tojo-html/diagnosis-html-generator/assets/fonts/poppins-latin-500-normal.woff2)}
@font-face{font-family:"Poppins";font-weight:600;src:url(file:///mnt/user-data/uploads/Discharge/tojo-html/diagnosis-html-generator/assets/fonts/poppins-latin-600-normal.woff2)}
@font-face{font-family:"Poppins";font-weight:700;src:url(file:///mnt/user-data/uploads/Discharge/tojo-html/diagnosis-html-generator/assets/fonts/poppins-latin-700-normal.woff2)}
</style></head><body>'; grep -v 'fonts.g' page.html; echo '</body></html>'; } > preview.html
