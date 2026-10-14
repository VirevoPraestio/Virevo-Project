# Virevo App — Login & Dashboard

A modern, themeable login interface with a post-login chat home screen and analytics dashboard.

## Folder Structure

```
virevo-app/
├── index.html              ← Main entry point
├── README.md               ← This file
├── css/
│   └── styles.css          ← All styles (themes, layout, components, responsive)
├── js/
│   └── app.js              ← All JavaScript (login flow, sidebar, theme, navigation)
└── images/
    ├── Tojo_with_Virevo.png  ← Logo shown on the login card
    └── Tojo_Namaste.png      ← Mascot icon (sidebar logo + greeting)
```

## Features

- **Multi-step Login** — Email → Password → App transition with loading animations
- **Collapsible Sidebar** — Icon-only (collapsed) or full-width (expanded) navigation
- **Theme Switcher** — Three themes with smooth CSS variable transitions:
  - **Dark** — Deep black/charcoal with green & gold accents
  - **Light** — Warm cream/white with subtle shadows
  - **Corporate** — Navy blue professional palette
- **Chat Home Screen** — Centered greeting with animated mascot + input box
- **Dashboard** — Stats cards, workflow grid, welcome banner
- **Responsive** — Mobile-friendly with sidebar auto-hide

## How to Run

Simply open `index.html` in any modern browser. No build tools or server required.

## Tech Stack

- HTML5, CSS3 (custom properties for theming), Vanilla JavaScript
- Google Fonts: Outfit + Playfair Display
- Zero dependencies
