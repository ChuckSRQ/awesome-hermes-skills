---
name: invisible-elements-debugging
description: Diagnose and fix invisible elements caused by undefined Tailwind color classes — white-on-white text, transparent sections, blank screenshots despite DOM elements existing.
---

# Invisible Elements Debugging

## When to Use
When elements appear to exist (accessibility tree shows them, DOM has them) but render as invisible — blank screenshots, white-on-white text, or sections that look "squished" or "broken" with no visible color.

This is the signature pattern of **undefined Tailwind color classes**.

---

## The Core Pattern

**Symptom:** A section looks broken — text invisible (white on white), or a colored section renders as blank/transparent.

**Why it happens:** Undefined Tailwind classes silently produce NO color. They don't error, they just render as:
- `bg-navy` → transparent background (if `bg-navy` isn't in app.css)
- `text-gold` → default browser text color (usually black or dark gray)
- `from-navy-deep` → gradient that doesn't exist → transparent

**Why it's sneaky:**
- The JSX looks valid — `bg-navy` looks like real Tailwind
- No console errors
- Accessibility tree shows elements ARE there (so a snapshot check passes)
- A browser screenshot of the broken section appears BLANK
- The content exists — it's just invisible

---

## Diagnostic Steps

### 1. Scrape the live page's raw HTML
Look for undefined class patterns in the rendered output:
- `bg-navy`, `bg-emerald`, `bg-rust`, `bg-sapphire`, `bg-gold`
- `text-gold`, `text-amber-400`, `text-blue-100`
- `from-navy-deep`, `via-navy`, `to-navy`

### 2. Check if classes exist in CSS
```bash
grep -r "bg-navy" src/app/app.css
# If nothing found → the class is undefined
```

### 3. Verify tailwind.config.ts colors
If the color isn't in `extend.colors`, Tailwind won't generate the class.

### 4. Common undefined class patterns (always check these):
```
bg-navy, bg-navy-deep, bg-gold (base class), bg-sapphire,
bg-emerald, bg-rust, bg-burgundy, text-gold (as class),
text-amber-400, text-blue-100, from-navy-deep, via-navy,
to-navy, to-navy-light
```

---

## The Fix

**For accent colors — use inline styles instead of Tailwind classes:**
```tsx
// WRONG — undefined class, produces no visible color
<div className="bg-navy text-gold">

// RIGHT — always works
<div style={{ backgroundColor: "var(--color-navy-light)", color: "var(--color-gold-light)" }}>
```

**For section backgrounds:**
```tsx
// WRONG
<section className="bg-navy">

// RIGHT
<section style={{ backgroundColor: "var(--color-navy-light)" }}>
```

**For accent text:**
```tsx
// WRONG
<p className="text-gold">Gold text</p>

// RIGHT
<p style={{ color: "var(--color-gold-light)" }}>Gold text</p>
```

---

## Prevention

Before committing color changes:
1. Run `npm run build` — catches TS/component errors but NOT undefined CSS classes
2. Visually verify pages in browser (screenshot or live dev)
3. Check the raw HTML for classes that look "made up"
4. When adding new color tokens, add them to BOTH `tailwind.config.ts` AND `app.css`

---

## Related
- Always check `src/app/app.css` and `tailwind.config.ts` when introducing new colors
- Inline styles with CSS variables are more reliable than Tailwind classes for custom palette colors
