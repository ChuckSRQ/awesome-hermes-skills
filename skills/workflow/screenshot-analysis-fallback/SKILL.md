---
name: screenshot-analysis-fallback
description: When browser vision tools fail, use accessibility snapshots + local source inspection to reverse-engineer visual designs.
category: workflow
---

# Screenshot Analysis Fallback

## When to Use

The vision/analyze tools (browser_vision, vision_analyze) fail or return "I can't see the image." This happens in some environments.

## Fallback Method

### Step 1 — Get the page's accessibility snapshot
```typescript
browser_snapshot({ full: true })
```
Returns a text tree with all elements, their content, and structural relationships. Can reveal:
- Image file names (e.g. `img "1.png"`)
- Heading hierarchy
- Section ordering
- Link targets
- Form field names

### Step 2 — Compare with local source
Read the local page source (`page.tsx`, components) to understand:
- What images are used locally vs. what's on the live site
- Color values defined in tailwind/config/css
- Structural differences in layout

### Step 3 — Infer visual design from structure
From the snapshot alone you can reverse-engineer:
- Color schemes from inline styles or CSS class names
- Section order changes
- Presence/absence of image grids
- Broken links (different hrefs between snapshot and local)
- Form field differences

## Key Insight

An accessibility snapshot of a real site is often enough to reconstruct the visual design for a redesign — image names, color patterns in CSS, heading order, and layout flow all appear in the text tree. You don't always need pixel-perfect vision analysis.

## Pitfall

The snapshot won't tell you: exact hex colors not in CSS classes, font families, shadow intensity, border radii, or gradient stops. For those you'd still need vision analysis working. The fallback gets you ~80% of the information needed for a redesign when the vision tool is unavailable.
