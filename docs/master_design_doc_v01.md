
# MASTER DESIGN DOCUMENT: OneTimeShare (v1.0)

## 1. Brand Identity System

### 1.1 Logomark: "The Entropic Block"

* **Concept:** A representation of data solidity transitioning into non-existence.
* **Geometry:** A heavy, solid geometric square (aspect ratio 1:1). The left 60% is a solid block. The right 40% consists of a coarse pixel grid (4x4 sub-grid) that progressively dissolves.
* **Fragmentation Gradient:**
* Column 1 (Center-Left): 100% opacity (Solid connection).
* Column 2: 75% density (Randomly missing 25% of pixels).
* Column 3: 50% density.
* Column 4 (Far Right): 10% density (Floating debris).


* **Scaling:**
* **Favicon:** Simplified to just the solid block + one column of debris.
* **Wordmark:** Typeset in **JetBrains Mono Bold**, tracked tight (-2%). Aligned to the baseline of the mark.



### 1.2 Color Palette: "Industrial Urgency"

*Primary Palette: Functional, High-Contrast, Alert-Based.*

* **Primary Action (Safety Orange):** `#FF5F15`
* **Usage:** Primary buttons, active borders, timer integers, critical alerts.
* **Psychology:** Triggers immediate attention without the "danger" semantic of pure red. Associated with heavy machinery and safety equipment.


* **Structural Base (Charcoal):** `#333333`
* **Usage:** Primary text, logo body, inactive borders, code blocks.
* **Psychology:** Reduces eye strain compared to pure black (#000000). Conveys permanence and ink-like legibility.


* **Canvas (Titanium White):** `#F0F2F5`
* **Usage:** Global background, card backgrounds.
* **Psychology:** A "cool" white. Clinical, sterile, creating a "clean room" environment for the data.


* **Null State (Signal Grey):** `#A0A0A0`
* **Usage:** Placeholders, disabled buttons, secondary metadata.
* **Psychology:** Represents absence of activity or value.



---

## 2. Typography System

### 2.1 Typeface Selection

* **Headings / Data:** **JetBrains Mono** (Google Fonts)
* *Rationale:* Monospace implies raw data, code execution, and precision. Eliminates ambiguity between characters (l, 1, I).


* **Body Copy:** **Inter** (Google Fonts)
* *Rationale:* High legibility, neutral tone, optimized for UI interfaces.



### 2.2 Type Scale

* **H1 (Timer/Hero):** 4rem (64px) | Weight: 700 (Bold) | Font: JetBrains Mono
* **H2 (Headlines):** 2rem (32px) | Weight: 600 (SemiBold) | Font: Inter
* **H3 (Labels):** 1rem (16px) | Weight: 500 (Medium) | Font: JetBrains Mono | Uppercase
* **Body:** 1rem (16px) | Weight: 400 (Regular) | Font: Inter
* **Input/Code:** 0.875rem (14px) | Weight: 400 | Font: JetBrains Mono

---

## 3. UI Architecture & States

### 3.1 Global Layout

* **Grid:** Bootstrap 5 Container (Fluid).
* **Vertical Alignment:** Absolute Center (Flexbox `justify-content: center; align-items: center; min-height: 100vh`).
* **Whitespace:** Aggressive padding. Minimum `2rem` between functional groups.

### 3.2 State 1: The "Clean Room" (Upload)

* **Visual Metaphor:** A sterile containment unit waiting for a specimen.
* **Component: Drop Zone**
* **Dimensions:** 600px width (max), 300px height.
* **Border:** 2px dashed `#333333`.
* **Background:** Transparent.
* **Interaction:**
* *Default:* Center icon (Upload glyph) + "DRAG FILE SECURELY".
* *Hover/Drag:* Border turns solid `#FF5F15`. Background tint `#FF5F15` at 5% opacity.




* **Component: Settings Panel**
* Located below Drop Zone.
* Minimal toggles for "Password Protection" (Optional).



### 3.3 State 2: Kinetic Decay (Active View/Download)

* **Visual Metaphor:** A system counting down to failure.
* **Element: The Entropy Bar**
* **Position:** Fixed top, full width.
* **Height:** 8px.
* **Color:** `#FF5F15`.
* **Behavior:** Shrinks from width 100% to 0% based on Redis TTL. Linear interpolation.


* **Element: The Countdown**
* **Position:** Center screen, dominant.
* **Typography:** H1 JetBrains Mono.
* **Format:** `HH:MM:SS`. Tabular figures (fixed width) to prevent jitter.


* **Element: Action Button**
* **Style:** Sharp corners (border-radius: 0).
* **Fill:** `#FF5F15`.
* **Text:** `#FFFFFF` | "SECURE DOWNLOAD".
* **Hover:** Invert colors (Border `#FF5F15`, Text `#FF5F15`, Background Transparent).


* **Dynamic Background:**
* The background `#F0F2F5` darkens by 1% for every 10% of TTL elapsed, ending at `#D0D2D5` to subliminally signal approaching expiration.



### 3.4 State 3: Heat Death (Terminal/Expired)

* **Visual Metaphor:** The Void.
* **Trigger:** File download completion OR Timer = 0.
* **Transition:** Hard cut (0ms duration). No fade outs.
* **Visuals:**
* Background: Flat Signal Grey `#E0E0E0`.
* All UI elements: **Removed**.
* Center Text: "DATA PURGED" (JetBrains Mono, `#333333`, Uppercase).
* Subtext: "The requested object no longer exists on this server."



---

## 4. Interaction Principles

### 4.1 Feedback Loops

* **Upload Success:** The Drop Zone snaps shut (border becomes solid, icon changes to Lock).
* **Error State:**
* Border: `#FF5F15` (Orange is used for error, not Red, to maintain palette consistency).
* Animation: Shake (Horizontal, 50ms).
* Text: "INVALID OBJECT" (Monospace).



### 4.2 Motion Design

* **General:** Instant or "Snap" curves. No ease-in-out.
* **Reasoning:** The app is a utility tool, not a lifestyle product. Interactions should feel mechanical and switch-like.

### 4.3 Mobile Adaptation

* **Entropy Bar:** Moves to bottom of screen (thumb reach).
* **Typography:** H1 scales to 2.5rem.
* **Margins:** Reduced to 1rem.

---

## 5. Implementation Notes (Dev Handoff)

* **CSS Variables (Extended):**
```css
:root {
  /* ===== PRIMARY ===== */
  --color-primary: #FF5F15;           /* Safety Orange - Action */
  --color-primary-hover: #E54D00;     /* Darker on hover */
  --color-primary-10: rgba(255, 95, 21, 0.1);  /* 10% for drag state */

  /* ===== SEMANTIC ===== */
  --color-success: #10B981;           /* Upload complete, valid */
  --color-success-pale: #D1FAE5;      /* Success backgrounds */
  --color-error: #DC2626;             /* Validation errors */
  --color-error-pale: #FEE2E2;        /* Error backgrounds */
  --color-warning: #F59E0B;           /* Expiry warnings */
  --color-info: #3B82F6;              /* Informational */

  /* ===== BASE ===== */
  --color-base: #333333;              /* Charcoal - text, borders */
  --color-canvas: #F0F2F5;            /* Titanium White - bg */
  --color-null: #A0A0A0;              /* Signal Grey - disabled */
  --color-void: #E0E0E0;              /* Heat Death state bg */

  /* ===== SPACING (8px base) ===== */
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-6: 24px;
  --space-8: 32px;
  --space-12: 48px;
  --space-16: 64px;

  /* ===== TYPOGRAPHY ===== */
  --font-mono: 'JetBrains Mono', monospace;
  --font-ui: 'Inter', sans-serif;

  /* ===== SHADOWS (Hard, Industrial) ===== */
  --shadow-sm: 0px 2px 0px var(--color-base);
  --shadow-md: 0px 4px 0px var(--color-base);
  --shadow-lg: 0px 8px 0px var(--color-base);

  /* ===== MOTION ===== */
  --ease-mechanical: cubic-bezier(0.0, 0.0, 0.2, 1);
  --ease-snap: cubic-bezier(0.25, 0.1, 0.25, 1);
  --duration-instant: 0ms;
  --duration-fast: 100ms;
  --duration-normal: 200ms;
}
```


* **Assets:**
* Logo must be SVG only.
* No raster shadows. Use CSS `box-shadow` with `0px 4px 0px #333333` (Hard shadow) for depth if needed.