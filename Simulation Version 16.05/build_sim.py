import re
import os

cwd = r"d:\Test\MANJARI DADA\NEW PROJECT\SAAS\virevo-app\virevo-app"
os.chdir(cwd)

with open('analysis.html', 'r', encoding='utf-8') as f:
    base_content = f.read()

with open('virevo_simulation.html', 'r', encoding='utf-8') as f:
    sim_content = f.read()

# 1. Extract style from virevo_simulation.html
style_match = re.search(r'<style>(.*?)</style>', sim_content, re.DOTALL)
sim_style = style_match.group(1) if style_match else ''

# Clean up simulation body styles
sim_style = re.sub(r':root\{.*?\}', '', sim_style, flags=re.DOTALL)
sim_style = re.sub(r'body\{.*?\}', '', sim_style)
sim_style = re.sub(r'\*\{box-sizing:border-box;margin:0;padding:0\}', '', sim_style)

# Remove border bottom from .hdr
sim_style = sim_style.replace('border-bottom:1px solid var(--border);', '')

# Remap theme variables to sync with the main app (styles.css)
theme_mappings = {
    'var(--surface)': 'var(--bg-card)',
    'var(--card)': 'var(--bg-card)',
    'var(--card2)': 'var(--bg-card-hover)',
    'var(--border2)': 'var(--border)',
    'var(--text)': 'var(--text-primary)',
    'var(--text2)': 'var(--text-secondary)',
    'var(--text3)': 'var(--text-muted)',
    'var(--blue)': 'var(--green-light)',
    'var(--blue2)': 'var(--green-primary)',
    'var(--teal)': 'var(--green-light)',
    'var(--amber)': 'var(--gold)',
    'var(--green2)': 'var(--green-primary)',
    'var(--green)': 'var(--green-light)',
    'var(--bg)': 'var(--bg-deep)'
}
for old_var, new_var in theme_mappings.items():
    sim_style = sim_style.replace(old_var, new_var)

# 2. Extract body content from virevo_simulation.html
body_match = re.search(r'<body>(.*?)</body>', sim_content, re.DOTALL)
sim_body = body_match.group(1) if body_match else ''
# Remove overlay, we don't need its full screen overlay if we want to rely on parent
# Actually let's keep it but scope it so it stays inside simulation container
sim_body = sim_body.replace('<div class="overlay"', '<div class="overlay" style="position:absolute;"')

# Remove the "VIREVO Hospital Simulation Engine" texts
sim_body = re.sub(r'<div class="hdr-logo">.*?</div>', '', sim_body)

# 3. Process analysis.html to create simulation.html template
out_html = base_content.replace('<title>Virevo — Analysis</title>', '<title>Virevo — Simulation</title>')

# Inject sim_style into head
style_inject = f"""
  <link rel="stylesheet" href="css/analysis.css">
  <style>
    /* Scoped Simulation Styles */
    #virevo-sim-container {{
       width: 100%;
       height: 100%;
       display: flex;
       flex-direction: column;
       position: relative;
    }}
    #virevo-sim-container .page {{
       flex: 1;
    }}

    /* ── Theme Dropdown Z-Index Fix ── */
    .analysis-topbar {{
       z-index: 99999 !important;
       position: relative;
    }}
    .theme-wrapper {{
       position: relative;
       z-index: 99999;
    }}
    .theme-dropdown {{
       z-index: 99999;
    }}
    /* Lower the simulation sticky headers so they don't overlap the theme dropdown */
    #virevo-sim-container .hdr {{
       z-index: 90;
    }}
    #virevo-sim-container .sim-action-bar {{
       z-index: 40;
    }}
    #virevo-sim-container .defn-summary-bar {{
       z-index: 40;
    }}
    
    {sim_style}
  </style>
</head>"""
out_html = out_html.replace('</head>', style_inject)

# Change TOPBAR title
out_html = out_html.replace('<div class="analysis-title">Analysis <span>Results</span></div>', '<div class="analysis-title">Simulation <span>Engine</span></div>')

# Set sidebar active state for Simulation icon
# Find analysis active icon
out_html = out_html.replace('<a href="analysis.html" class="nav-icon active" title="Analysis">', '<a href="analysis.html" class="nav-icon" title="Analysis">')
out_html = out_html.replace('<a href="simulation.html" class="nav-icon" title="Simulation">', '<a href="simulation.html" class="nav-icon active" title="Simulation">')

# Add Chat Collapse Button
chat_header_actions = r'<div class="chat-panel-actions">'
collapse_btn = r'''<div class="chat-panel-actions">
          <button class="panel-action-btn" id="chatCollapseBtn" title="Hide Chat">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="9 18 15 12 9 6"/>
            </svg>
          </button>'''
out_html = out_html.replace(chat_header_actions, collapse_btn)

# Add Expand Chat button beside theme icon
expand_btn_inject = '''<div style="display: flex; align-items: center; gap: 12px;">
          <button class="theme-btn" id="chatExpandBtn" title="Show Chat" style="display: none;">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
            </svg>
          </button>
          <div class="theme-wrapper" id="themeWrapper">'''
out_html = out_html.replace('<div class="theme-wrapper" id="themeWrapper">', expand_btn_inject)
# close the wrapper div introduced by expand_btn_inject after theme-dropdown ends
out_html = out_html.replace('</div>\n        </div>\n      </div>\n\n      <div class="analysis-content"', '</div>\n        </div>\n        </div>\n      </div>\n\n      <div class="analysis-content"')

# Now inject into analysis-content
app_content_start = out_html.find('<div class="analysis-content" id="analysisContent">')
app_content_end = out_html.find('</div>', app_content_start)

before_content = out_html[:app_content_start + len('<div class="analysis-content" id="analysisContent">')]
after_content = out_html[app_content_end:]

sim_body_wrapped = f"""
      <!-- SIMULATION FULL CONTENT -->
      <div id="virevo-sim-container" style="overflow-y: auto; height: 100%;">
{sim_body}
      </div>
"""

out_html = before_content + sim_body_wrapped + after_content

# Replace the specific analysis JS with simulation JS
out_html = out_html.replace('<script src="js/analysis.js"></script>', '<script src="js/simulation_layout.js"></script>')

with open('simulation.html', 'w', encoding='utf-8') as f:
    f.write(out_html)

print("Generated simulation.html with chat section")
