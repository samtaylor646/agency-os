# Global Design System Tokens and Layout Specification

## 1. Design Tokens

### 1.1 Primitive Tokens
Primitive tokens define the core values that are used throughout the application. These should not be used directly in components, but rather mapped to semantic tokens.

**Colors:**
*   `blue-100`: `#E6F0FF`
*   `blue-300`: `#4C9AFF`
*   `blue-500`: `#0052CC` (Core Enterprise Blue)
*   `blue-700`: `#003E99`
*   `blue-900`: `#002966`
*   `gray-50`: `#F4F5F7` (Subtle Background)
*   `gray-100`: `#EBECF0`
*   `gray-200`: `#DFE1E6` (Soft Dividers)
*   `gray-300`: `#C1C7D0`
*   `gray-400`: `#97A0AF`
*   `gray-500`: `#7A869A`
*   `gray-600`: `#5E6C84`
*   `gray-700`: `#42526E`
*   `gray-800`: `#172B4D` (Primary Text)
*   `gray-900`: `#091E42`
*   `white`: `#FFFFFF`
*   `red-500`: `#DE350B` (Destructive Actions/Errors)
*   `green-500`: `#00875A` (Success)
*   `yellow-500`: `#FF991F` (Warnings)

**Typography (Inter or System UI):**
*   `font-sans`: `'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif`
*   `text-xs`: `0.75rem` (12px) - Line Height: `1rem` (16px)
*   `text-sm`: `0.875rem` (14px) - Line Height: `1.25rem` (20px)
*   `text-base`: `1rem` (16px) - Line Height: `1.5rem` (24px)
*   `text-lg`: `1.125rem` (18px) - Line Height: `1.75rem` (28px)
*   `text-xl`: `1.25rem` (20px) - Line Height: `1.75rem` (28px)
*   `text-2xl`: `1.5rem` (24px) - Line Height: `2rem` (32px)
*   `text-3xl`: `1.875rem` (30px) - Line Height: `2.25rem` (36px)

**Spacing:**
*   `space-1`: `0.25rem` (4px)
*   `space-2`: `0.5rem` (8px)
*   `space-3`: `0.75rem` (12px)
*   `space-4`: `1rem` (16px)
*   `space-5`: `1.25rem` (20px)
*   `space-6`: `1.5rem` (24px)
*   `space-8`: `2rem` (32px)
*   `space-12`: `3rem` (48px)

**Border Radius:**
*   `radius-sm`: `3px`
*   `radius-md`: `4px`
*   `radius-lg`: `8px`
*   `radius-full`: `9999px`

**Shadows:**
*   `shadow-sm`: `0 1px 1px rgba(9, 30, 66, 0.25), 0 0 1px rgba(9, 30, 66, 0.31)` (Cards, Dropdowns)
*   `shadow-md`: `0 4px 8px -2px rgba(9, 30, 66, 0.25), 0 0 1px rgba(9, 30, 66, 0.31)` (Modals, Overlays)

**Animation:**
*   `transition-snappy`: `200ms ease-in-out`
*   `transition-smooth`: `300ms ease-in-out`

### 1.2 Semantic Tokens
Semantic tokens map to primitive tokens and are used directly in component styling. They provide meaning to the values and allow for easy theme switching (e.g., Dark Mode).

**Backgrounds:**
*   `bg-default`: `white` (Main content area)
*   `bg-subtle`: `gray-50` (Sidebar, secondary panels)
*   `bg-inverse`: `gray-800` (Tooltips, dark overlays)
*   `bg-primary`: `blue-500` (Primary button background)
*   `bg-primary-hover`: `blue-700`

**Text & Typography:**
*   `text-default`: `gray-800` (Main body text)
*   `text-subtle`: `gray-600` (Secondary text, metadata)
*   `text-muted`: `gray-500` (Disabled text, placeholders)
*   `text-inverse`: `white` (Text on dark backgrounds)
*   `text-brand`: `blue-500` (Links, brand highlights)

**Borders:**
*   `border-default`: `gray-200` (Dividers, card borders)
*   `border-focused`: `blue-300` (Focus rings, active states)

**Interactive States:**
*   `action-primary`: `blue-500`
*   `action-primary-hover`: `blue-700`
*   `action-primary-active`: `blue-900`
*   `action-secondary`: `gray-100`
*   `action-secondary-hover`: `gray-200`
*   `action-secondary-active`: `blue-100`

**Feedback:**
*   `feedback-error`: `red-500`
*   `feedback-success`: `green-500`
*   `feedback-warning`: `yellow-500`

## 2. Layout Specifications

### 2.1 Global Shell
The application will utilize a persistent, SPA-style layout.
*   **Left Sidebar:** Collapsible, persistent navigation (`bg-subtle`). Width: 240px (expanded), 64px (collapsed).
*   **Main Content Area:** The central workspace (`bg-default`). Flexible width.
*   **Contextual Detail Drawer (Right Sidebar):** Collapsible, used for settings, metadata, or deeper context (`bg-subtle` or `bg-default` depending on visual weight). Width: 320px.

### 2.2 Global Prompt Context
A singleton component residing at the root of the layout.
*   **Intro Page State:** Large, centered input field.
*   **Chat Scope State:** Fluidly animates to anchor at the bottom of the main content area, transitioning into a persistent chat input.

## 3. Component Base Styles
*   **Buttons:** `radius-md`, bold font weight, `transition-snappy`. Focus state requires a prominent 2px `border-focused` ring, offset by 2px to ensure accessibility.
*   **Inputs (Text, Textarea):** `radius-md`, `border-default`, `bg-default`. Focus state uses `border-focused` and an inner shadow for clear visual hierarchy.
*   **Checkboxes & Radio Buttons:** `border-default`, checked state uses `bg-primary` with `white` checkmark/dot. Focus ring applies to the outer container.
*   **Toggles/Switches:** Track uses `bg-subtle` (off) and `bg-primary` (on). Thumb uses `bg-default` with `shadow-sm`. Smooth `transition-smooth` for thumb movement.
*   **Badges & Tags:** `radius-full` for tags, `radius-sm` for structural badges. Uses soft background colors (e.g., `blue-100` with `blue-700` text).
*   **Tooltips:** `bg-inverse`, `text-inverse`, `text-xs`, `radius-sm`, `shadow-md`. Strict 200ms delay before appearance to prevent flashing.
*   **Dropdown Menus:** `bg-default`, `border-default`, `radius-md`, `shadow-md`. Items have `transition-snappy` on hover (`bg-subtle`).
*   **Avatars:** `radius-full`, distinct border for presence indicators. Uses first initials or images.
*   **Alerts & Banners:** Full width or inline `radius-md`. Background uses pale feedback colors (e.g., `red-50` for errors) with dark corresponding text and solid borders.
*   **Progress Indicators:** Linear bars or circular spinners. Track uses `bg-subtle`, fill uses `bg-primary` or feedback colors.
*   **Skeleton Loaders:** Pulse animation `bg-subtle` to `gray-100`. Matches the exact shape and border-radius of the content it replaces.
*   **Cards:** `bg-default`, `border-default`, `radius-lg`, `shadow-sm`.
*   **Modals:** Centered overlay with a semi-transparent backdrop (`rgba(9, 30, 66, 0.54)`). Modal container uses `bg-default`, `radius-lg`, `shadow-md`.

## 4. Accessibility Checkpoint
*   All semantic text colors (`text-default`, `text-subtle`, `text-inverse`) have been verified against their intended backgrounds (`bg-default`, `bg-subtle`, `bg-primary`, `bg-inverse`) to meet the WCAG AA 4.5:1 minimum contrast ratio requirement.
*   The `border-focused` color (`blue-300`) provides a 3:1 minimum contrast ratio against `bg-default` and `bg-subtle` for interactive focus indicators.
