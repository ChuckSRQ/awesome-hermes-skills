---
name: full-site-color-system-refactor
description: "How to do a full-site color palette redesign across a Next.js + Tailwind CSS codebase. Covers: CSS variable updates, glob replace for token references, glob replace for hex values, style page swatch/reference cleanup, and docs sync."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [css, color, design-system, tailwind, next-js, refactor]
    related_skills: [tailwind-to-css-variable-migration, real-estate-web-design]
---

# Full-Site Color System Refactor

Use when: the client changes the site's color palette and every page/component needs updating.

## The Pattern (proven approach)

Do NOT patch files one by one. Use a batch script approach:

### Step 1: Audit First

Before touching anything, run an audit script to get a complete picture:

```python
import os, re

base = "/path/to/project/src"
pages = {}

for dirpath, dirnames, filenames in os.walk(base):
    for filename in filenames:
        if filename.endswith('.tsx') or filename.endswith('.css'):
            filepath = os.path.join(dirpath, filename)
            with open(filepath) as f:
                content = f.read()
            hexes = sorted(set(re.findall(r'#([0-9a-fA-F]{6})', content)))
            css_vars = sorted(set(re.findall(r'--color-[a-z-]+', content)))
            pages[filepath] = {'hexes': hexes, 'css_vars': css_vars}
```

Print results in a table. This tells you exactly how many files need changing and what color families exist.

### Step 2: Define the Replacement Map

Create a complete replacement map covering ALL forms of each token:

```python
replacements = [
    # CSS variable tokens (className= and inline style references)
    ('--color-old-token)', '--color-new-token)'),
    ('var(--color-old-token)', 'var(--color-new-token)'),
    # Hex values (case-insensitive)
    ('#OLDHEX1', '#NEWHEX'),
    ('#oldhex1', '#newhex'),
]
```

Key lesson: `--color-token)` (closing paren) and `var(--color-token)` (no paren) are DIFFERENT patterns — both exist in JSX. Include both.

### Step 3: Apply to ALL Files in One Pass

```python
files_changed = []
for dirpath, dirnames, filenames in os.walk(base):
    for filename in filenames:
        if filename.endswith('.tsx') or filename.endswith('.css'):
            filepath = os.path.join(dirpath, filename)
            with open(filepath) as f:
                content = f.read()
            original = content
            for old, new in replacements:
                content = content.replace(old, new)
            if content != original:
                with open(filepath, 'w') as f:
                    f.write(content)
                files_changed.append(filepath)
```

### Step 4: Verify Build Passes FIRST

```bash
npm run build
```

Fix any TypeScript/compilation errors before proceeding.

### Step 5: Audit for "Swatch Display" Sections

**Critical gap discovered in practice:** The `/style` page has a "CSS Reference" section that lists color tokens as display cards — hex values shown as labels. These get updated by the batch script (the hex values change), but the labels/captions describing those tokens still reference old names.

Example problem after batch replace:
```tsx
// The swatch for "Gold" still says "Gold" even though --color-gold no longer exists
{ label: "Gold", hex: "#e8d5a3", vars: "--color-gold" }
```

Fix: Search for the old token names in the style page's reference sections:
```bash
grep -n "--color-old-token\|label: \"Old Name\"" src/app/style/page.tsx
```

Also check the CSS reference grid at the bottom of the style page — it may list tokens that no longer exist.

### Step 6: Update the Design System CSS File FIRST

Before running the batch script, update `app.css` (the design tokens file) so all references downstream are consistent. The batch script then propagates the new token names.

### Step 7: Sync All Docs

After the build passes clean:
- `SPEC.md` — rewrite the color palette section with new tokens and hex values
- `README.md` — update the color token table
- `CLAUDE.md` — update CSS variables reference + add deprecated tokens list

Commit message should enumerate all 15-20 changed files.

## Common Pitfalls

1. **Only replacing CSS vars, not hex values**: Components often have hardcoded hex values (especially old pages with `backgroundColor: "#C9A84C"`). Replace both.
2. **Style page swatch labels not matching**: The style page shows color swatches — if labels say "Gold" but the token is now "Gold Light", that's wrong.
3. **Building without verifying**: Always `npm run build` after mass replacement — catch broken references immediately.
4. **Missing `href` vs `className` patterns**: Some color refs appear in `style={{ color: "var(--color-x)" }}` (inline) and others in `className="text-[var(--color-x)]"` — both need the same replacement.
