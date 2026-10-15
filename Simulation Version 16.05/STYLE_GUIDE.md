# Virevo App — UI / UX / Style Guide

> **Purpose:** This document serves as the single source of truth (contract file) for all UI, UX, and styling decisions across the Virevo application. Every new page, component, or modification **must** follow these guidelines to maintain visual and behavioral consistency.

---

## Table of Contents

1. [Design Principles](#1-design-principles)
2. [Theme System](#2-theme-system)
3. [Color Tokens](#3-color-tokens)
4. [Typography](#4-typography)
5. [Spacing & Layout](#5-spacing--layout)
6. [Border Radius](#6-border-radius)
7. [Shadows & Elevation](#7-shadows--elevation)
8. [Components](#8-components)
9. [Icons](#9-icons)
10. [Animations & Transitions](#10-animations--transitions)
11. [Responsive Design](#11-responsive-design)
12. [Scrollbar Styling](#12-scrollbar-styling)
13. [Accessibility](#13-accessibility)
14. [Naming Conventions](#14-naming-conventions)
15. [External Dependencies](#15-external-dependencies)
16. [File & Folder Structure](#16-file--folder-structure)
17. [Do's and Don'ts](#17-dos-and-donts)

---

## 1. Design Principles

| # | Principle | Description |
|---|-----------|-------------|
| 1 | **Dark-First** | Dark theme is the default. All components must look correct in dark mode before adapting to light/corporate. |
| 2 | **Green Accent Focus** | `#2a8c48` (light) and `#1a5c2e` (primary) are the signature interactive colors. |
| 3 | **Smooth Micro-interactions** | Every interactive element has a hover/active/focus state with smooth transitions (0.45s default). |
| 4 | **Minimal Color Palette** | 3–5 colors per theme + neutrals. Avoid introducing new colors without updating CSS variables. |
| 5 | **Consistent Spacing** | Use the 4px/8px grid system. All spacing values should be multiples of 4. |
| 6 | **Typography Hierarchy** | Clear size/weight differences between headings, body, and labels. |
| 7 | **No External UI Frameworks** | Pure custom CSS. Do not introduce Bootstrap, Tailwind, or any CSS framework. |
| 8 | **Inline SVG Icons** | All icons are inline SVGs with `currentColor`. No icon font libraries. |
| 9 | **Responsive & Adaptive** | Collapsible sidebars, fluid grids, mobile-first media queries. |
| 10 | **Graceful Loading States** | Every async action must show a loading indicator (spinner, pulse, or skeleton). |

---

## 2. Theme System

### How Themes Work

Themes are applied via the `data-theme` attribute on `<html>`:

```html
<html lang="en" data-theme="dark">
```

**Supported themes:** `dark` (default), `light`, `corporate`

### Theme Persistence

- Stored in `localStorage` under key `'virevo-theme'`
- Applied on page load before first paint to avoid flash
- Switched via: `document.documentElement.setAttribute('data-theme', theme)`

### Global Tokens (Theme-Independent)

```css
--radius: 14px;
--radius-sm: 10px;
--sidebar-w: 56px;
--sidebar-w-open: 220px;
--tt: background 0.45s ease, color 0.45s ease, border-color 0.45s ease, box-shadow 0.45s ease;
```

---

## 3. Color Tokens

### Dark Theme (Default)

| Token | Value | Usage |
|-------|-------|-------|
| `--bg-deep` | `#08090c` | Page background |
| `--bg-card` | `#111318` | Cards, panels, modals |
| `--bg-card-hover` | `#181b22` | Card hover state |
| `--border` | `#1e2230` | Default borders |
| `--border-focus` | `#2a6e3f` | Focus ring / active border |
| `--green-primary` | `#1a5c2e` | Primary buttons, gradient start |
| `--green-light` | `#2a8c48` | Active states, gradient end, highlights |
| `--green-glow` | `rgba(42, 140, 72, 0.25)` | Focus glow, active backgrounds |
| `--gold` | `#c5a044` | Secondary accent, links, highlights |
| `--gold-light` | `#d4b565` | Gold hover states |
| `--text-primary` | `#e8e6e1` | Main body text |
| `--text-secondary` | `#8a8d98` | Supporting / secondary text |
| `--text-muted` | `#55586a` | Disabled text, placeholders, hints |
| `--danger` | `#d44040` | Errors, destructive actions, warnings |
| `--input-bg` | `#16181e` | Form input backgrounds |
| `--input-border` | `#262a36` | Form input borders |
| `--sidebar-bg` | `#0c0d11` | Sidebar background |
| `--sidebar-border` | `#1a1d28` | Sidebar divider |
| `--topbar-bg` | `rgba(8, 9, 12, 0.85)` | Top bar (with backdrop-filter) |
| `--shadow-lg` | `0 4px 60px rgba(0, 0, 0, 0.5)` | Large elevation shadow |
| `--shadow-card` | `0 2px 20px rgba(0, 0, 0, 0.3)` | Card shadow |
| `--chip-bg` | `#1a1d26` | Chip / tag background |
| `--chip-border` | `#282c3a` | Chip border |
| `--chip-hover` | `#22263a` | Chip hover background |
| `--dropdown-bg` | `#14161c` | Dropdown / popover background |
| `--ambient-green` | `rgba(26, 92, 46, 0.08)` | Subtle green tint overlays |
| `--ambient-gold` | `rgba(197, 160, 68, 0.06)` | Subtle gold tint overlays |

### Light Theme

| Token | Value |
|-------|-------|
| `--bg-deep` | `#f5f3ef` |
| `--bg-card` | `#ffffff` |
| `--bg-card-hover` | `#f8f7f5` |
| `--border` | `#e4e1da` |
| `--text-primary` | `#1a1a1a` |
| `--text-secondary` | `#6b6e7a` |
| `--text-muted` | `#9a9da8` |
| `--input-bg` | `#ffffff` |
| `--input-border` | `#ddd9d0` |
| `--sidebar-bg` | `#ffffff` |
| `--sidebar-border` | `#ebe8e2` |
| `--topbar-bg` | `rgba(245, 243, 239, 0.9)` |
| `--shadow-lg` | `0 4px 40px rgba(0, 0, 0, 0.06)` |
| `--shadow-card` | `0 1px 12px rgba(0, 0, 0, 0.05)` |
| `--chip-bg` | `#f0ede8` |
| `--chip-border` | `#e0ddd6` |
| `--chip-hover` | `#e8e5de` |
| `--dropdown-bg` | `#ffffff` |

> Green/gold accent colors remain consistent across all themes. Only surface, text, and shadow colors change.

### Corporate Theme

| Token | Value |
|-------|-------|
| `--bg-deep` | `#0f1923` |
| `--bg-card` | `#172332` |
| `--bg-card-hover` | `#1d2d40` |
| `--border` | `#243447` |
| `--green-primary` | `#1e6b9a` |
| `--green-light` | `#3b9fd4` |
| `--gold` | `#d4a853` |

> Corporate theme swaps green accent to blue (`#1e6b9a` / `#3b9fd4`) for a professional look.

### Gradients

| Name | Value | Usage |
|------|-------|-------|
| Primary Button | `linear-gradient(135deg, #1a5c2e, #2a8c48)` | CTAs, primary actions |
| Card Top Accent | `linear-gradient(90deg, #2a8c48, #c5a044, transparent)` | Card hover top border |
| Gold highlight | `linear-gradient(135deg, var(--gold), var(--gold-light))` | Secondary highlights |

### Adding New Colors

> **Rule:** Never hardcode a color value. Always create or reuse a CSS variable under `[data-theme]` selectors in `css/styles.css`. Update all three themes when adding a new token.

---

## 4. Typography

### Font Stack

| Role | Font Family | Loaded Weights | Usage |
|------|------------|----------------|-------|
| **Primary UI** | `'Outfit', sans-serif` | 300, 400, 500, 600, 700 | All UI text, buttons, labels, body |
| **Display/Serif** | `'Playfair Display', serif` | 700, italic 400 | Greeting headlines, hero text |
| **Secondary** | `'Poppins', sans-serif` | 300, 400, 500, 600, 700 | Analysis page text |

### Type Scale

| Level | Size | Weight | Line Height | Usage |
|-------|------|--------|-------------|-------|
| **Display** | `2rem` | 700 | 1.2 | Greeting headlines (Playfair) |
| **H1** | `1.5rem` | 700 | 1.3 | Page titles, form titles |
| **H2** | `1.1rem` | 600 | 1.4 | Section headers |
| **H3 / Subtitle** | `1rem` | 600 | 1.4 | Card titles, subsection headers |
| **Body** | `0.92rem` | 400 | 1.5 | Default body text |
| **Body Small** | `0.88rem` | 400–500 | 1.5 | Nav items, dropdown options |
| **Label** | `0.82rem` | 500–600 | 1.4 | Form labels, chip text, small buttons |
| **Caption** | `0.75rem` | 500 | 1.3 | Timestamps, meta text, status labels |
| **Micro** | `0.7rem` | 400 | 1.3 | Hints, secondary labels |

### Font Color Rules

- Headings / primary content → `var(--text-primary)`
- Supporting / descriptive text → `var(--text-secondary)`
- Hints, placeholders, disabled → `var(--text-muted)`
- Links / interactive text → `var(--gold)` or `var(--green-light)`
- Error text → `var(--danger)`

---

## 5. Spacing & Layout

### Spacing Scale (4px grid)

| Token | Value | Usage |
|-------|-------|-------|
| `4px` | 4px | Tight gaps (icon-to-text in nav) |
| `8px` | 8px | Small gaps (chip icons, inline elements) |
| `10px` | 10px | Nav item padding, small gaps |
| `12px` | 12px | Icon gaps, section dividers |
| `16px` | 16px | Grid gaps, card inner spacing, form field gaps |
| `20px` | 20px | Card padding, section padding (mobile) |
| `24px` | 24px | Card padding (desktop), topbar horizontal padding |
| `32px` | 32px | Large section padding, page padding (desktop) |
| `40px` | 40px | Login card horizontal padding |
| `48px` | 48px | Login card top padding |

### Layout Patterns

#### App Shell (3-Panel)

```
┌──────────┬─────────────────────────────┬──────────────┐
│ Sidebar  │       Main Content          │  Chat Panel  │
│  56px    │       flex: 1               │    380px     │
│ (220px   │                             │ (collapsible)│
│  open)   │                             │              │
└──────────┴─────────────────────────────┴──────────────┘
```

```css
/* Sidebar */
width: var(--sidebar-w);          /* 56px collapsed */
width: var(--sidebar-w-open);     /* 220px expanded */

/* Main Content */
flex: 1;
overflow-y: auto;

/* Chat Panel (when present) */
width: 380px;                     /* 320px on tablet */
```

#### Top Bar

```css
height: 52px;
display: flex;
align-items: center;
justify-content: space-between;
padding: 0 24px;
background: var(--topbar-bg);
backdrop-filter: blur(20px);
border-bottom: 1px solid var(--border);
position: sticky; top: 0; z-index: 100;
```

#### Grid Systems

**Stats Grid (fixed columns):**
```css
display: grid;
grid-template-columns: repeat(4, 1fr);   /* 2 on mobile */
gap: 16px;
```

**Auto-fill Card Grid:**
```css
display: grid;
grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
gap: 16px;
```

**Department / Large Card Grid:**
```css
display: grid;
grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
gap: 16px;
```

**KPI Grid:**
```css
display: grid;
grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
gap: 18px;
```

---

## 6. Border Radius

| Component | Radius | Variable |
|-----------|--------|----------|
| Cards, Panels, Modals, Login Card | `14px` | `var(--radius)` |
| Buttons, Inputs, Small Cards | `10px` | `var(--radius-sm)` |
| Chat Message Bubbles | `16px` (with one `4px` corner) | — |
| Chips, Tags, Pills | `24px` | — |
| Avatars, Circular Icons | `50%` | — |
| Scrollbar Thumb | `5px` | — |

---

## 7. Shadows & Elevation

| Level | Value | Usage |
|-------|-------|-------|
| **None** | `none` | Default state of flat elements |
| **Card** | `var(--shadow-card)` — `0 2px 20px rgba(0,0,0,0.3)` | Cards at rest |
| **Large** | `var(--shadow-lg)` — `0 4px 60px rgba(0,0,0,0.5)` | Modals, login card, elevated panels |
| **Green Glow** | `0 8px 30px var(--green-glow)` | Primary button hover |
| **Focus Ring** | `0 0 0 3px var(--green-glow)` | Input focus state |
| **Inset Shine** | `0 0 0 1px rgba(255,255,255,0.03) inset` | Subtle card border highlight |

---

## 8. Components

### 8.1 Buttons

#### Primary Button
```css
.btn-primary {
  background: linear-gradient(135deg, var(--green-primary), var(--green-light));
  color: #fff;
  border: none;
  border-radius: 10px;
  padding: 15px;                    /* full-width variant */
  /* OR: padding: 10px 24px;        compact variant */
  font-family: 'Outfit', sans-serif;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: var(--tt);
}
.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 8px 30px var(--green-glow);
}
.btn-primary:active {
  transform: translateY(0);
}
.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
```

#### Outline Button
```css
.btn-outline {
  background: transparent;
  border: 1px solid var(--border);
  color: var(--text-secondary);
  padding: 10px 24px;
  border-radius: 10px;
  font-size: 0.88rem;
  font-weight: 500;
}
.btn-outline:hover {
  border-color: var(--green-light);
  color: var(--green-light);
}
```

#### Button Sizes
| Size | Padding | Font Size |
|------|---------|-----------|
| Default | `15px` (full) / `10px 24px` | `0.95rem` |
| Small `.btn-sm` | `6px 14px` | `0.82rem` |
| Extra Small `.btn-xs` | `4px 10px` | `0.72rem` |

#### Button States
- **Loading:** Add spinner SVG inside, set `opacity: 0.8`, disable pointer events
- **Disabled:** `opacity: 0.6`, `cursor: not-allowed`
- **Success/Approved:** Green background with checkmark icon

---

### 8.2 Form Inputs

```css
input, textarea {
  background: var(--input-bg);
  border: 1.5px solid var(--input-border);
  border-radius: 10px;
  padding: 14px 16px;              /* 14px 16px 14px 46px with icon */
  font-family: 'Outfit', sans-serif;
  font-size: 1rem;
  color: var(--text-primary);
  transition: var(--tt);
}
input:focus, textarea:focus {
  outline: none;
  border-color: var(--border-focus);
  box-shadow: 0 0 0 3px var(--green-glow);
}
input::placeholder {
  color: var(--text-muted);
}
```

**Input with Icon:**
```css
.field-group {
  position: relative;
}
.field-icon {
  position: absolute;
  left: 15px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-muted);
  width: 18px; height: 18px;
}
input { padding-left: 46px; }
```

**Textarea (Chat):**
```css
textarea {
  width: 100%;
  min-height: 48px;
  max-height: 160px;
  resize: none;
  line-height: 1.5;
  padding: 20px 20px 8px;
}
```

Auto-resize pattern (JS):
```javascript
textarea.addEventListener('input', () => {
  textarea.style.height = 'auto';
  textarea.style.height = Math.min(textarea.scrollHeight, maxHeight) + 'px';
});
```

**Error State:**
```css
.error-msg {
  color: var(--danger);
  font-size: 0.82rem;
  animation: shake 0.4s ease;
}
input.error {
  border-color: var(--danger);
}
```

---

### 8.3 Cards

#### Standard Card
```css
.card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius);     /* 14px */
  padding: 20px;                    /* or 24px for larger cards */
  transition: var(--tt);
}
```

#### Interactive Card (with hover)
```css
.card-interactive:hover {
  border-color: var(--border-focus);
  background: var(--bg-card-hover);
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}
/* Gradient top border on hover */
.card-interactive::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 3px;
  background: linear-gradient(90deg, var(--green-light), var(--gold), transparent);
  border-radius: var(--radius) var(--radius) 0 0;
  opacity: 0;
  transition: opacity 0.3s;
}
.card-interactive:hover::before {
  opacity: 1;
}
```

#### Stat Card
```css
.stat-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 20px;
}
.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-primary);
}
.stat-label {
  font-size: 0.75rem;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
```

---

### 8.4 Navigation (Sidebar)

```css
.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px;
  border-radius: 10px;
  color: var(--text-secondary);
  font-size: 0.88rem;
  cursor: pointer;
  transition: var(--tt);
}
.nav-item:hover {
  background: var(--bg-card-hover);
  color: var(--text-primary);
}
.nav-item.active {
  background: var(--green-glow);
  color: var(--green-light);
}
```

**Sidebar states:**
- **Collapsed:** `width: 56px`, icons only, centered
- **Expanded:** `width: 220px`, icons + labels, left-aligned

---

### 8.5 Tabs

```css
.tab-btn {
  padding: 10px 20px;
  font-size: 0.88rem;
  font-weight: 500;
  color: var(--text-secondary);
  background: none;
  border: none;
  border-bottom: 2px solid transparent;
  cursor: pointer;
  transition: var(--tt);
}
.tab-btn:hover {
  color: var(--text-primary);
}
.tab-btn.active {
  color: var(--green-light);
  border-bottom-color: var(--green-light);
}
.tab-btn.active::after {
  animation: tabSlide 0.3s ease;
}
```

---

### 8.6 Chips / Tags

```css
.chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border-radius: 24px;
  background: var(--chip-bg);
  border: 1px solid var(--chip-border);
  font-family: 'Outfit', sans-serif;
  font-size: 0.82rem;
  font-weight: 500;
  color: var(--text-secondary);
  cursor: pointer;
  transition: var(--tt);
}
.chip:hover {
  background: var(--chip-hover);
  border-color: var(--border-focus);
  color: var(--text-primary);
}
```

---

### 8.7 Chat Bubbles

**User Message:**
```css
.msg-user {
  background: var(--green-primary);
  color: #fff;
  padding: 12px 16px;
  border-radius: 16px 16px 4px 16px;
  max-width: 100%;
  align-self: flex-end;
}
```

**Assistant Message:**
```css
.msg-assistant {
  background: var(--bg-card);
  border: 1px solid var(--border);
  color: var(--text-primary);
  padding: 12px 16px;
  border-radius: 16px 16px 16px 4px;
  max-width: 100%;
  align-self: flex-start;
}
```

---

### 8.8 Dropdowns / Popovers

```css
.dropdown {
  position: absolute;
  top: calc(100% + 10px);
  right: 0;
  width: 220px;
  background: var(--dropdown-bg);
  border: 1px solid var(--border);
  border-radius: var(--radius);     /* 14px */
  padding: 8px;
  opacity: 0;
  visibility: hidden;
  transform: translateY(-10px) scale(0.96);
  transform-origin: top right;
  transition: opacity 0.3s, transform 0.3s, visibility 0.3s;
}
.dropdown.open {
  opacity: 1;
  visibility: visible;
  transform: translateY(0) scale(1);
}
```

**Dropdown Item:**
```css
.dropdown-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 11px 12px;
  border-radius: 10px;
  font-size: 0.88rem;
  color: var(--text-secondary);
  cursor: pointer;
}
.dropdown-item:hover {
  background: var(--chip-hover);
}
.dropdown-item.active {
  color: var(--text-primary);
}
```

**Close on Outside Click (JS pattern):**
```javascript
document.addEventListener('click', (e) => {
  if (!container.contains(e.target)) {
    dropdown.classList.remove('open');
  }
});
```

---

### 8.9 Toggle Switch

```css
.toggle-track {
  width: 36px;
  height: 20px;
  border-radius: 10px;
  background: var(--input-border);
  position: relative;
  transition: background 0.3s;
}
.toggle-thumb {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: var(--text-muted);
  position: absolute;
  top: 2px; left: 2px;
  transition: transform 0.3s, background 0.3s;
}
.toggle-track.active {
  background: var(--green-primary);
}
.toggle-track.active .toggle-thumb {
  transform: translateX(16px);
  background: #fff;
}
```

---

### 8.10 Progress / Percentage Bars

```css
.progress-bar {
  height: 6px;
  background: var(--input-border);
  border-radius: 3px;
  overflow: hidden;
}
.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--green-primary), var(--green-light));
  border-radius: 3px;
  transition: width 0.6s ease;
}
```

---

## 9. Icons

### Specification

- **Format:** Inline SVG only (no icon fonts, no external sprite sheets)
- **ViewBox:** `0 0 24 24`
- **Stroke Width:** `1.8` or `2`
- **Color:** `stroke="currentColor"` (inherits parent text color)
- **Fill:** `fill="none"` unless the icon is specifically solid

### Size Scale

| Size | Dimensions | Usage |
|------|-----------|-------|
| XS | `14–16px` | Table row icons, chip icons |
| SM | `18px` | Inline text icons, button icons |
| MD | `20px` | Navigation icons, form icons |
| LG | `22px` | Section header icons |
| XL | `40px` | Mascot, greeting illustrations |

### Example

```html
<svg width="20" height="20" viewBox="0 0 24 24" fill="none"
     stroke="currentColor" stroke-width="1.8" stroke-linecap="round"
     stroke-linejoin="round">
  <path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/>
  <polyline points="9 22 9 12 15 12 15 22"/>
</svg>
```

---

## 10. Animations & Transitions

### Default Transition

```css
transition: var(--tt);
/* Expands to: background 0.45s ease, color 0.45s ease,
              border-color 0.45s ease, box-shadow 0.45s ease */
```

> Apply `transition: var(--tt)` to **all** interactive elements.

### Standard Keyframes

| Name | Duration | Easing | Usage |
|------|----------|--------|-------|
| `fadeUp` | `0.5s` | `ease` | Cards/sections appearing (translateY(20px) → 0) |
| `cardIn` | `0.8s` | `cubic-bezier(0.16, 1, 0.3, 1)` | Modal/card entry |
| `stepIn` | `0.45s` | `cubic-bezier(0.16, 1, 0.3, 1)` | Multi-step form transitions |
| `msgSlide` | `0.3s` | `ease` | Chat message appear |
| `spin` | `0.6–0.8s` | `linear` infinite | Loading spinners |
| `pulse` | `1.5s` | `ease` infinite | Processing indicators |
| `shake` | `0.4s` | `ease` | Error/validation feedback |
| `greetIn` | `0.8s` | `cubic-bezier(0.16, 1, 0.3, 1)` | Hero greeting entry |
| `chipsIn` | `0.6s` | `ease` | Staggered chip reveal |
| `tabSlide` | `0.3s` | `ease` | Tab underline slide |

### Easing Guidelines

| Context | Easing |
|---------|--------|
| Enter/appear | `cubic-bezier(0.16, 1, 0.3, 1)` — snappy overshoot |
| Default hover/state | `ease` |
| Loading spinner | `linear` |
| Elastic/bounce feel | `cubic-bezier(0.34, 1.56, 0.64, 1)` |

### Staggered Animations

Use `data-delay` attribute or CSS `animation-delay` with increments of `0.1s`:

```css
.card:nth-child(1) { animation-delay: 0.1s; }
.card:nth-child(2) { animation-delay: 0.2s; }
.card:nth-child(3) { animation-delay: 0.3s; }
```

---

## 11. Responsive Design

### Breakpoints

| Name | Query | Layout Changes |
|------|-------|----------------|
| **Desktop** | `≥ 1024px` | Full 3-panel layout, sidebar open |
| **Tablet** | `768px – 1023px` | Chat panel → 320px, reduced padding |
| **Mobile** | `< 768px` | Single column, sidebar hidden, stat grid → 2 columns, chat panel → 50vh overlay |

### Responsive Rules

```css
/* Tablet */
@media (max-width: 1024px) {
  .chat-panel { width: 320px; }
  .page-padding { padding: 24px; }
}

/* Mobile */
@media (max-width: 768px) {
  .sidebar { display: none; }                     /* or slide-out drawer */
  .stat-grid { grid-template-columns: repeat(2, 1fr); }
  .chat-panel { width: 100%; height: 50vh; }
  .page-padding { padding: 16px; }
  .display-text { font-size: 1.5rem; }           /* from 2rem */
}
```

### Mobile-First Principles

- Touch targets minimum `44px × 44px`
- Sidebar becomes off-canvas drawer on mobile
- Chat panel becomes bottom sheet on mobile
- Grid columns reduce: 4 → 2 → 1

---

## 12. Scrollbar Styling

```css
/* Webkit (Chrome, Safari, Edge) */
::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-track { background: var(--bg-deep); border-radius: 5px; }
::-webkit-scrollbar-thumb {
  background: var(--border);
  border-radius: 5px;
  border: 2px solid var(--bg-deep);
}
::-webkit-scrollbar-thumb:hover { background: var(--text-muted); }
::-webkit-scrollbar-thumb:active { background: var(--green-light); }

/* Firefox */
* { scrollbar-width: thin; scrollbar-color: var(--border) var(--bg-deep); }
```

> Always include both Webkit and Firefox scrollbar styles.

---

## 13. Accessibility

### Focus States

Every interactive element **must** have a visible focus indicator:

```css
:focus-visible {
  outline: none;
  box-shadow: 0 0 0 3px var(--green-glow);
}
```

### Color Contrast

- `--text-primary` on `--bg-card` must meet **WCAG AA** (4.5:1 minimum)
- Interactive elements must be distinguishable without color alone (use icons, underlines, weight)

### Semantic HTML

- Use `<button>` for actions, `<a>` for navigation
- Use `<nav>`, `<main>`, `<aside>`, `<header>` landmarks
- Use `aria-label` for icon-only buttons
- Use `role` attributes when semantic HTML is insufficient

### Keyboard Navigation

- All interactive elements must be keyboard-reachable
- Dropdowns close on `Escape` key
- Tab order follows visual layout

---

## 14. Naming Conventions

### CSS Classes

| Pattern | Example | Usage |
|---------|---------|-------|
| `component` | `.card`, `.chip`, `.btn` | Base component |
| `component-element` | `.card-title`, `.btn-icon` | Sub-element |
| `component-modifier` | `.btn-primary`, `.btn-outline` | Variant |
| `component.state` | `.nav-item.active`, `.dropdown.open` | State class |
| `section-name` | `.login-scene`, `.chat-panel` | Page sections |

**Conventions:**
- Lowercase, hyphen-separated (`kebab-case`)
- Short, descriptive names
- No abbreviations except common ones (`btn`, `nav`, `msg`, `img`)
- Prefix page-specific styles: `.analysis-sidebar`, `.sim-panel`

### HTML IDs

| Pattern | Example |
|---------|---------|
| `camelCase` | `#emailInput`, `#chatTextarea` |
| Descriptive purpose | `#loginScene`, `#appShell`, `#homePage` |
| Step indicators | `#step1`, `#step2` |

### Data Attributes

| Attribute | Values | Purpose |
|-----------|--------|---------|
| `data-theme` | `dark`, `light`, `corporate` | Theme selection |
| `data-page` | `home`, `simulation`, `dashboard`, `analysis` | Page routing |
| `data-delay` | `0.1s`, `0.2s`, etc. | Animation stagger |
| `data-tip` | String | Tooltip content |

### JavaScript

- **Variables/Functions:** `camelCase`
- **Constants:** `UPPER_SNAKE_CASE`
- **Event Handlers:** `handleClick`, `onSubmit`, `toggleSidebar`
- **DOM Queries:** Prefer `document.querySelector()` / `querySelectorAll()`
- **State Management:** Use `classList.add/remove/toggle` for UI state

---

## 15. External Dependencies

### Required CDN Imports

```html
<!-- Google Fonts — MUST be included in every page -->
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Playfair+Display:ital,wght@0,700;1,400&family=Poppins:wght@300;400;500;600;700&display=swap">
```

### Prohibited

- No CSS frameworks (Bootstrap, Tailwind, Bulma, etc.)
- No icon font libraries (Font Awesome, Material Icons, etc.)
- No jQuery
- No external charting libraries unless explicitly approved

### Allowed (If Needed)

- Chart.js / D3.js — for data visualization only
- Any library must be loaded via CDN, not bundled

---

## 16. File & Folder Structure

```
virevo-app/
├── index.html                  # Login + App Shell (Home, Dashboard)
├── analysis.html               # Analysis page
├── simulation.html             # Simulation page
├── css/
│   ├── styles.css              # Global styles + theme variables + shared components
│   └── analysis.css            # Analysis-specific styles
│   └── [page].css              # Page-specific styles (if needed)
├── js/
│   ├── app.js                  # Global app logic (theme, nav, auth)
│   └── analysis.js             # Analysis page logic
│   └── simulation_layout.js    # Simulation page logic
│   └── [page].js               # Page-specific logic (if needed)
├── images/                     # Static assets
├── Datasets/                   # CSV data files
└── STYLE_GUIDE.md              # This file
```

### Rules for New Pages

1. Create `[page].html` at root level
2. Create `css/[page].css` for page-specific styles (import `styles.css` first)
3. Create `js/[page].js` for page-specific logic
4. Import Google Fonts + `css/styles.css` in the HTML `<head>`
5. Use the same `data-theme` attribute on `<html>`
6. Include the sidebar navigation (copy from `index.html`)
7. Apply theme on load: read from `localStorage.getItem('virevo-theme')`

---

## 17. Do's and Don'ts

### Do

- ✅ Use CSS custom properties for all colors, shadows, and radii
- ✅ Support all three themes (dark, light, corporate)
- ✅ Test every component in all themes before shipping
- ✅ Use `transition: var(--tt)` on interactive elements
- ✅ Use inline SVGs with `currentColor` for icons
- ✅ Use semantic HTML elements
- ✅ Include focus-visible styles for keyboard navigation
- ✅ Add loading/processing states for async operations
- ✅ Use the 4px spacing grid
- ✅ Animate entries with `fadeUp` or `cardIn` keyframes
- ✅ Close dropdowns/modals on outside click and Escape key
- ✅ Use `border-radius: var(--radius)` or `var(--radius-sm)`

### Don't

- ❌ Hardcode color values — always use CSS variables
- ❌ Introduce new fonts without updating the font import
- ❌ Use CSS frameworks (Bootstrap, Tailwind, etc.)
- ❌ Use icon font libraries — use inline SVGs
- ❌ Use `!important` unless absolutely unavoidable
- ❌ Create elements without hover/focus states
- ❌ Use `px` for font sizes — use `rem`
- ❌ Skip the dark theme — it is the default
- ❌ Use JavaScript for styling that CSS can handle
- ❌ Add animations longer than 1s for UI transitions (except infinite loops)
- ❌ Break the sidebar/topbar/content shell pattern

---

## Quick Reference: New Component Checklist

When creating any new component, ensure:

- [ ] Uses CSS variables for all colors
- [ ] Has `transition: var(--tt)` for interactive states
- [ ] Has `:hover` state with subtle background/border change
- [ ] Has `:focus-visible` state with green glow ring
- [ ] Has `:active` state (e.g., `translateY(0)` reset)
- [ ] Has `:disabled` state with reduced opacity
- [ ] Uses `var(--radius)` or `var(--radius-sm)` for border-radius
- [ ] Uses `'Outfit', sans-serif` font family
- [ ] Font sizes in `rem` following the type scale
- [ ] Tested in dark, light, and corporate themes
- [ ] Responsive at all three breakpoints (desktop, tablet, mobile)
- [ ] Entry animation (fadeUp, cardIn) if appropriate
- [ ] Loading state if content is async

---

*Last updated: April 2026*
