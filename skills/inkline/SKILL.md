---
name: inkline
description: Vue 3 component library for Inkline. Use when building with Inkline UI components, creating form elements, modals, or any Inkline-based Vue interfaces.
---

# Inkline - Vue 3 Component Library

## What is Inkline
Vue 3 component library using TypeScript, Composition API, and CSS custom properties for theming.

## Stack
- Vue 3 + TypeScript
- Composition API
- CSS custom properties theming
- pnpm monorepo

## Key Commands

```bash
pnpm run build          # Build all packages
pnpm run build:core    # Build core only
pnpm run build:ui       # Build UI only
pnpm run dev            # Dev mode
pnpm run storybook      # Storybook
pnpm run test           # Tests
```

## Creating Components

1. Create folder in `packages/ui/components/[ComponentName]/`
2. Create `index.ts` - export component and theme
3. Create `theme.ts` - style using `@inkline/core` and `@inkline/theme`
4. Add export to `packages/inkline/src/{component-name}.ts`

## Component Patterns
- PascalCase component names
- Typed props and emits
- Use `@inkline/core` for theming
- Component styles in `theme.ts` (not raw CSS)

## Vue 3 Composition API
```typescript
<script setup lang="ts">
// Use typed props, defineEmits
</script>
```
