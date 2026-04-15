---
name: tailwind-to-css-variable-migration
description: "Use when migrating pages or components from hardcoded Tailwind color utilities to the PrtyPix CSS variable design system. Covers: layout file checks, CSS variable mapping, grep verification, Playwright testing, and changelog updates."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [css, tailwind, design-system, frontend, migration, theming]
    related_skills: [systematic-debugging, test-driven-development]
---

# Tailwind to CSS Variable Migration

## When to Use

Use this skill whenever:
- A page or component still shows old gray/white Tailwind styling instead of the new themed design
- You are tasked with "migrating a page to the new design system"
- A recently migrated page "looks wrong" despite the migration being complete
- You're doing a design audit and find hardcoded Tailwind color utilities

## The Critical First Step: Check the Layout File FIRST

**Most common mistake:** Migrating a page's inline styles while the PARENT LAYOUT FILE still has old Tailwind classes.

**Pattern seen in production:** `app/(admin)/layout.tsx` had `className="min-h-screen bg-gray-100"` — the page itself was fully migrated but still looked broken because the outer wrapper was still gray.

**Rule:** Before touching any page file, check its parent layout file(s). Look for hardcoded Tailwind color utilities on the outer wrapper divs.

## Workflow

### 1. Read the Source of Truth FIRST

Read these files BEFORE writing any code:

```
prtypix/docs/design/DESIGN_SYSTEM.md
prtypix/docs/design/DESIGN_SYSTEM_ADDENDUM
prtypix/app/globals.css
prtypix/docs/design/PAGE_TEMPLATE.tsx
```

**IMPORTANT:** Design docs may list `--text-primary` but `globals.css` uses `--text`. Always verify against `globals.css`.

### 2. Identify All Files to Migrate

Use `rg` (ripgrep) to find every hardcoded Tailwind color utility across the files being migrated:

```bash
rg -n "bg-white|bg-gray-|text-gray-|border-gray-|text-indigo-|text-red-|border-white|bg-green-|bg-purple-|bg-red-|bg-indigo-" \
  app/path/to/page.tsx \
  components/SomeComponent.tsx
```

The `C` constant in `PAGE_TEMPLATE.tsx` maps tokens to CSS variables — use it as a reference.

### 3. Check the Layout File

For every page being migrated, also check:
- `app/layout.tsx` (root layout)
- `app/(admin)/layout.tsx` (admin layout)
- Any route-group layout files like `app/(auth)/layout.tsx`

Look for `bg-gray-`, `bg-white`, or other old Tailwind backgrounds on outer wrapper divs.

### 4. Apply the Migration

Token reference from `globals.css`:

| Old Tailwind | CSS Variable |
|---|---|
| `text-gray-900` | `var(--text)` |
| `text-gray-600` | `var(--text-muted)` |
| `text-gray-500` | `var(--text-dim)` |
| `text-indigo-600` | `var(--cyan)` |
| `text-red-*`, `bg-red-*` | `var(--magenta)` |
| `bg-green-*` | `var(--cyan)` |
| `bg-purple-*` | `var(--magenta)` |
| `bg-white`, `bg-gray-*` (backgrounds) | `var(--surface)`, `var(--surface-2)` |
| `border-gray-*`, `border-white` | `var(--border)` |

#### Page Background (required on every migrated page)

Apply this inline style to the outermost div of every migrated page:

```tsx
style={{
  background: `radial-gradient(ellipse 70% 55% at 5% 10%, var(--glow-c) 0%, transparent 65%), radial-gradient(ellipse 60% 50% at 95% 90%, var(--glow-m) 0%, transparent 65%), radial-gradient(ellipse 45% 40% at 50% 50%, var(--glow-p) 0%, transparent 70%), var(--bg)`
}}
```

#### Card System

Every content section should use the glassmorphic card style:

```tsx
style={{
  background: 'var(--surface)',
  border: '1px solid var(--border)',
  borderRadius: 10,
  padding: '16px',
  position: 'relative',
  overflow: 'hidden',
}}
```

With the 3px cyan→magenta gradient top stripe:

```tsx
<div style={{
  position: 'absolute',
  top: 0, left: 0, right: 0,
  height: 3,
  background: 'linear-gradient(90deg, var(--cyan), var(--magenta))',
  borderRadius: '10px 10px 0 0',
}} />
```

### 5. Add Playwright Tests

After migration, add tests that:

```javascript
// tests/<page-name>.spec.mjs

test('page loads without console errors', async ({ page }) => {
  const errors = [];
  page.on('console', msg => { if (msg.type() === 'error') errors.push(msg.text()); });
  await page.goto('/admin/events/[id]');
  await page.waitForLoadState('networkidle');
  expect(errors).toHaveLength(0);
});

test('no hardcoded Tailwind color utilities remain', async ({ page }) => {
  await page.goto('/admin/events/[id]');
  const html = await page.content();
  const forbidden = ['bg-white', 'bg-gray-', 'text-gray-', 'border-gray-',
                      'text-indigo-', 'bg-purple-', 'bg-green-', 'bg-red-'];
  for (const pattern of forbidden) {
    expect(html).not.toContain(pattern);
  }
});

test('dark mode renders correctly', async ({ page }) => {
  await page.goto('/admin/events/[id]');
  await page.evaluate(() => document.documentElement.setAttribute('data-theme', 'dark'));
  await page.waitForLoadState('networkidle');
  await expect(page.locator('text=Photos')).toBeVisible();
});
```

Make sure `@playwright/test` is in `package.json` devDependencies before committing tests.

### 6. Verify No Regressions

```bash
# Grep all migrated files — must return zero matches
rg -n "bg-white|bg-gray-|text-gray-|border-gray-|text-indigo-|text-red-" \
  app/path/to/page.tsx \
  components/Component.tsx

npm run typecheck
npm run test:e2e
```

### 7. Update CHANGELOG.md

Add an entry under the current date:

```markdown
## YYYY-MM-DD — ui: migrated <page> to CSS variable design system

- `app/path/to/page.tsx`: replaced all hardcoded Tailwind color utilities
  (`bg-white`, `text-gray-*`, `border-gray-*`, etc.) with CSS variable inline
  styles (`var(--surface)`, `var(--text)`, `var(--border)`, etc.)
- `app/path/to/component.tsx`: same migration
- Added Playwright regression tests
```

## Common Pitfalls

1. **Missing the layout file** — always check `layout.tsx` files first
2. **Using `--text-primary` instead of `--text`** — `globals.css` defines `--text`, not `--text-primary`
3. **Forgetting the page background gradient** — every page needs the radial glow background
4. **Applying `overflow: hidden` to card wrappers** — this clips `overflow-x-auto` scroll containers inside stats strips; use `overflow: hidden` only on cards that don't scroll
5. **Leaving `next/image` off user-facing images** — use `next/image` not `<img>` for all photos/avatars

## Decision Rules

- **Grep first, then write code** — always find all instances before starting
- **Layout file before page file** — check the parent before the child
- **Test after migration** — add Playwright tests alongside every migration
- **Changelog every change** — keep the record current
