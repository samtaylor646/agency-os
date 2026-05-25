# Mobile UI Design Plan: Refined Technical Aesthetic

## Overview
This document outlines the design specification for upgrading the AgencyOS mobile user interface. Based on an evaluation of the current mobile screenshots (`docs/qa/screenshots/mobile-*`), the UI currently suffers from excessive whitespace, cramped data tables, and a generic, consumer-app aesthetic.

The client's directive is to achieve a **"really refined tech feel"** and **"better data viz"**. To accomplish this, we are shifting from a loose, rounded, card-heavy layout to a tighter, sharper, and denser data-driven aesthetic.

---

## 1. Global Styling & Aesthetic Principles

### Typography
* **Primary Font:** Keep the clean sans-serif for headings, but reduce sizes globally by one step (e.g., from `text-xl` to `text-lg` for card titles) to increase density.
* **Data Font:** Introduce a monospace font (`font-mono`) for all tabular data, numbers, timestamps, and emails. This instantly elevates the "tech/developer" feel.
* **Weights:** Use high-contrast font weights. Strict `font-medium` or `font-semibold` for headers, and `font-normal` or `font-light` for secondary text. Avoid muddy mid-weights.

### Spacing & Layout
* **Density:** Transition from spacious padding (`p-6`) to high-density padding (`p-3` or `p-4`). 
* **Borders & Corners:** Replace large border radiuses (`rounded-xl` or `rounded-2xl`) with tighter corners (`rounded-sm` or `rounded-md`). 
* **Separators:** Rely more on subtle borders (`border-b border-gray-200` or `border-slate-800` in dark mode) rather than wrapping everything in distinct floating cards. Reduce nested cards entirely.

### Color Palette
* **Monochrome Base:** Use a strict grayscale base (slate or zinc in Tailwind). 
* **Accent Colors:** Use sharp, vibrant accents (like an electric blue or neon green) sparingly for primary actions or data viz, rather than soft pastels.

---

## 2. Component-Specific Recommendations

### A. Dashboards & KPI Cards (e.g., `mobile-client-dashboard.png`)
* **Current Issue:** Numbers like "3" and "2" are massive and lack context. Cards take up too much vertical space.
* **Recommendation:**
  * Convert stacked KPI cards into a 2-column grid on mobile (`grid-cols-2 gap-3`).
  * Reduce the KPI number size (`text-3xl` instead of `text-5xl`).
  * **Data Viz Addition:** Embed micro-charts (sparklines or miniature bar charts) directly into the KPI cards to show trends over time, rather than just raw numbers.
  * Align labels and numbers to the left, tightly packed.

### B. Data Tables & Logs (e.g., `mobile-audit-log-table.png`)
* **Current Issue:** Traditional HTML tables on mobile cause horizontal overflow, text truncating, and a cramped reading experience.
* **Recommendation:**
  * **Card-List Pattern:** On mobile (`< md`), abandon the `<table>` layout. Render each table row as a vertical list item (a stacked card).
  * **Example Structure:** 
    ```html
    <div class="border-b border-slate-200 py-3">
      <div class="flex justify-between">
        <span class="font-mono text-xs text-slate-500">5/24/2026, 11:51 PM</span>
        <span class="text-xs font-semibold text-blue-600">system</span>
      </div>
      <div class="mt-1 font-mono text-sm truncate">admin@agencyos.com</div>
    </div>
    ```
  * **Timestamps:** Format dates into relative time ("2 hrs ago") or a much tighter format (e.g., `MM/DD HH:MM`) for mobile.
  * Remove outer card wrappers for lists so they bleed closer to the screen edges, maximizing horizontal real estate.

### C. Settings & Forms (e.g., `mobile-workplace-settings.png`)
* **Current Issue:** Nested cards (Workspace Settings > API Keys) create massive left/right margins, leaving only ~60% of the screen width for actual content. Buttons wrap awkwardly.
* **Recommendation:**
  * **Flatten Hierarchy:** Remove the outer card border for the main sections. Use full-width sections separated by thick divider lines or background color shifts.
  * **Action Placement:** Move primary actions (like "Invite User" or "Add Credential") from the header to full-width buttons below the lists, or use compact icon-buttons.
  * **Form Inputs:** Use a highly structural look for inputs—sharp borders, background slightly darker than the page, and small uppercase labels (`text-[10px] uppercase tracking-wider`).

### D. Global Floating Action (Chat Input)
* **Current Issue:** The floating chat input at the bottom looks like a consumer messenger app.
* **Recommendation:**
  * Dock the input directly to the bottom of the screen (full width, no side margins, `rounded-none` or only rounded top corners).
  * Make the send button a sharp square or subtle icon without a massive blue circular background.
  * Add a subtle backdrop-blur (`backdrop-blur-md bg-white/80`) to emphasize the modern tech feel.

---

## 3. Tailwind Implementation Guide

To achieve this updated look, developers should utilize the following utility classes:

*   **Borders:** `border border-slate-200 dark:border-slate-800`
*   **Radii:** `rounded-sm` or `rounded` (Avoid `rounded-lg` and above)
*   **Typography:** `font-mono text-xs`, `tracking-tight` for headings, `tracking-wider text-[10px] uppercase` for micro-labels.
*   **Shadows:** Replace soft drop shadows (`shadow-md`) with hard offsets or remove them entirely in favor of border-driven separation. Use `shadow-sm` if necessary.

## Conclusion
By flattening the layout, increasing data density, utilizing monospace typography, and replacing horizontal tables with stacked list items, the AgencyOS mobile UI will immediately shed its generic feel and adopt the requested refined, high-performance technical aesthetic.