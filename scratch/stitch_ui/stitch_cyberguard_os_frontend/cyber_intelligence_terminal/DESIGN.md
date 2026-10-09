---
name: Cyber Intelligence Terminal
colors:
  surface: '#0d141c'
  surface-dim: '#0d141c'
  surface-bright: '#333a43'
  surface-container-lowest: '#080f17'
  surface-container-low: '#161c24'
  surface-container: '#1a2029'
  surface-container-high: '#242a33'
  surface-container-highest: '#2f353e'
  on-surface: '#dde3ef'
  on-surface-variant: '#bcc9cd'
  inverse-surface: '#dde3ef'
  inverse-on-surface: '#2a313a'
  outline: '#869397'
  outline-variant: '#3d494c'
  surface-tint: '#4cd7f6'
  primary: '#4cd7f6'
  on-primary: '#003640'
  primary-container: '#06b6d4'
  on-primary-container: '#00424f'
  inverse-primary: '#00687a'
  secondary: '#4edea3'
  on-secondary: '#003824'
  secondary-container: '#00a572'
  on-secondary-container: '#00311f'
  tertiary: '#ffb95f'
  on-tertiary: '#472a00'
  tertiary-container: '#e79400'
  on-tertiary-container: '#563400'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#acedff'
  primary-fixed-dim: '#4cd7f6'
  on-primary-fixed: '#001f26'
  on-primary-fixed-variant: '#004e5c'
  secondary-fixed: '#6ffbbe'
  secondary-fixed-dim: '#4edea3'
  on-secondary-fixed: '#002113'
  on-secondary-fixed-variant: '#005236'
  tertiary-fixed: '#ffddb8'
  tertiary-fixed-dim: '#ffb95f'
  on-tertiary-fixed: '#2a1700'
  on-tertiary-fixed-variant: '#653e00'
  background: '#0d141c'
  on-background: '#dde3ef'
  surface-variant: '#2f353e'
typography:
  headline-xl:
    fontFamily: Space Grotesk
    fontSize: 40px
    fontWeight: '700'
    lineHeight: 48px
    letterSpacing: -0.03em
  headline-xl-mobile:
    fontFamily: Space Grotesk
    fontSize: 30px
    fontWeight: '700'
    lineHeight: 38px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Space Grotesk
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.02em
  headline-lg-mobile:
    fontFamily: Space Grotesk
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Space Grotesk
    fontSize: 22px
    fontWeight: '600'
    lineHeight: 30px
    letterSpacing: -0.01em
  headline-sm:
    fontFamily: Space Grotesk
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 26px
  body-lg:
    fontFamily: Geist
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Geist
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  body-sm:
    fontFamily: Geist
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 18px
  label-lg:
    fontFamily: JetBrains Mono
    fontSize: 13px
    fontWeight: '500'
    lineHeight: 18px
    letterSpacing: 0.02em
  label-md:
    fontFamily: JetBrains Mono
    fontSize: 11px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.04em
  label-sm:
    fontFamily: JetBrains Mono
    fontSize: 10px
    fontWeight: '600'
    lineHeight: 14px
    letterSpacing: 0.06em
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  gutter: 1rem
  gutter-desktop: 1.5rem
  margin: 1rem
  margin-desktop: 2rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2.5rem
---

## Brand & Style
The design system powers an autonomous, local-first threat detection and neural monitoring dashboard. The visual tone balances mission-critical tactical clarity with modern developer platform refinement. It evokes absolute operational control, rigorous cryptographic precision, and real-time responsiveness.

The aesthetic synthesizes modern tactical minimalism with subtle glassmorphic depth: deep, low-luminance abyssal navy surfaces, razor-thin translucent borders, monospace telemetry readouts, and restrained neon luminescence. Instead of arbitrary sci-fi clutter, every line, badge, and glow communicates live system telemetry, active packet inspection, and real-time neural inference.

## Colors
The color hierarchy is optimized for prolonged operations in darkened environments, leveraging an intentional threat-state chromatic system:

- **Primary (`#06b6d4` / Neon Cyan):** Interactive surfaces, active neural nodes, primary actions, focused input states, and live link traces.
- **Secondary (`#10b981` / Emerald Green):** Verified secure states, operational consensus, zero-anomaly flags, and operational uptime.
- **Tertiary (`#f59e0b` / Amber Warning):** Elevated friction, suspicious packet heuristics, medium-severity vulnerabilities, and resource bottlenecks.
- **Destructive (`#ef4444` / Crimson Alert):** Critical threat interception, unauthenticated intrusion breaches, process kill switches, and compromised states.
- **Neutral Canvas (`#060c14` Base, `#0b1524` Surface Layer):** Foundation layers that reduce eye fatigue while providing high contrast against data visualizations.
- **Borders & Separators:** Semi-transparent slate (`rgba(148, 163, 184, 0.12)`) providing architectural structure without visual noise.

## Typography
Typography is split into three deliberate roles:

1. **Display & Structural Titles (`Space Grotesk`):** Technical, sharp, and geometric. Used for module headings, operational status overviews, and executive threat scores.
2. **Standard Content & Readouts (`Geist`):** Crisp, unobtrusive neutral sans-serif delivering clear legibility for analytical dossiers, incident explanations, and settings.
3. **Telemetry & Data Attributes (`JetBrains Mono`):** Dedicated to IP addresses, SHA-256 hashes, port indices, latency measurements, and timestamp matrices. Uppercase tracking is applied to micro labels to establish military-grade readability.

## Layout & Spacing
The layout adheres to a 12-column adaptive fluid grid engineered for dense information architecture and multi-pane live telemetry feeds.

- **Desktop (>= 1280px):** 12-column setup using `gutter-desktop` (24px) with fixed lateral sidebars for HUD navigation and secondary dynamic telemetry ribbons. Outer margins enforce `margin-desktop` (32px).
- **Tablet (768px - 1279px):** 6-column fluid structure where secondary HUD panels collapse into off-canvas side sheets. Grid gutter defaults to `gutter` (16px).
- **Mobile (< 768px):** Single-column stacked card feed with persistent sticky telemetry status bars at the screen bottom. Canvas margins reduce to `margin` (16px).
- **Inner Padding Rules:** Compact information density requires component interiors to use `space-sm` (8px) and `space-md` (16px) standard padding.

## Elevation & Depth
Depth is constructed through optical transparency, dark tonal stratification, and localized luminous radiation rather than standard drop shadows:

- **Level 0 (Canvas Base):** Solid `#060c14`. Used exclusively for the global application backdrop.
- **Level 1 (Card & Module Layer):** Backdrops utilize `rgba(11, 21, 36, 0.75)` combined with a `backdrop-filter: blur(12px)` and a precise `1px solid rgba(148, 163, 184, 0.1)`.
- **Level 2 (Popovers, Tooltips, Dynamic HUD Gauges):** `rgba(15, 23, 42, 0.9)` with `1px solid rgba(6, 182, 212, 0.3)`. Emits a subtle cyan perimeter bloom: `0 0 20px -4px rgba(6, 182, 212, 0.15)`.
- **Alert States:** When an element transitions to critical, its elevation border shifts to `rgba(239, 68, 68, 0.45)` with a crimson threat pulse: `0 0 24px -2px rgba(239, 68, 68, 0.25)`.

## Shapes
The design system adopts a soft technical contour (`roundedness: 1`):
- Standard components (buttons, input fields, badges) employ a tight `0.25rem` (4px) corner radius to evoke tactical instrument panels.
- Containers and cards scale to `0.5rem` (8px).
- Modals, complex threat charts, and floating terminal overlays scale to `0.75rem` (12px).
- Circular rounding is strictly reserved for user status avatars, telemetry radar crosshairs, and ping indicators.

## Components

### Action Buttons
- **Primary:** Solid cyan (`#06b6d4`) background, deep black text (`#060c14`), font weight 600. On hover, produces a cyan outer glow (`0 0 16px rgba(6, 182, 212, 0.4)`).
- **Secondary / Outline:** Translucent fill (`rgba(6, 182, 212, 0.05)`), border `1px solid rgba(6, 182, 212, 0.35)`, cyan text.
- **Destructive ("Neutralize Threat"):** Background `rgba(239, 68, 68, 0.15)`, border `1px solid #ef4444`, text `#ef4444`. Pulsing highlight on hover.

### Telemetry Cards
Constructed using glassmorphic plates (`rgba(11, 21, 36, 0.6)`) with `backdrop-filter: blur(16px)` and delicate slate wireframe borders (`rgba(148, 163, 184, 0.08)`). Top corners contain mono micro-labels (`label-sm`) detailing subsystem status and latency ticks.

### Input Fields
Darkened field inserts (`#08101d`) with recessed inset borders (`rgba(148, 163, 184, 0.15)`). Text renders in `Geist` with mono cursor carats. Focused state triggers a sharp cyan border transition and a soft ambient glow.

### Status Chips & Badges
Compact pill markers with monospace labels (`label-sm`). Built with a 10% opacity tint of the target status color, matching border at 30% opacity, and a left-aligned 6px pulsing dot (e.g., emerald for secure, amber for warning, red for breach).

### Checkboxes & Radios
Square, sharp-angled selectors with slate borders. Checked states fill with cyan or emerald and use geometric check marks.

### HUD Radar & Threat Matrices
Vector-based concentric circular sweeps rendered in slate line work (`rgba(148, 163, 184, 0.2)`). Target pings render as luminous radial gradients with rapid fading trails.