import re
import os

html_path = r'd:\Test\MANJARI DADA\NEW PROJECT\SAAS\virevo-app\virevo-app\analysis.html'
css_path = r'd:\Test\MANJARI DADA\NEW PROJECT\SAAS\virevo-app\virevo-app\css\analysis.css'
js_path = r'd:\Test\MANJARI DADA\NEW PROJECT\SAAS\virevo-app\virevo-app\js\analysis.js'

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Extract CSS
style_pattern = re.compile(r'<style>(.*?)</style>', re.DOTALL)
style_match = style_pattern.search(content)

if style_match:
    css_content = style_match.group(1)
    with open(css_path, 'w', encoding='utf-8') as f:
        f.write(css_content.strip() + '\n')
    content = content[:style_match.start()] + '<link rel="stylesheet" href="css/analysis.css">' + content[style_match.end():]

# Extract JS
script_pattern = re.compile(r'<script>\s*document\.addEventListener(.*?)<\/script>', re.DOTALL)
script_match = script_pattern.search(content)

if script_match:
    js_content = 'document.addEventListener' + script_match.group(1)
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(js_content.strip() + '\n')
    content = content[:script_match.start()] + '<script src="js/analysis.js"></script>' + content[script_match.end():]

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Extraction complete!')
