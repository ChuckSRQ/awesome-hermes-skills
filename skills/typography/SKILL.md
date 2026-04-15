---
name: typography
description: Universal typography principles for web design. Covers font pairing, type scale, spacing, and hierarchy. Use when choosing fonts, setting type scales, or evaluating typographic decisions.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [typography, fonts, type-scale, hierarchy, spacing]
    related_skills: [aesthetic-principles, color-and-palette, design-quality]
---

# Typography

## The Foundational Pairing: Serif + Sans-Serif

The classic luxury pairing that works across contexts:
- **Headlines:** Elegant serif (Playfair Display, Cormorant, Libre Baskerville)
- **Body/UI:** Clean geometric sans-serif (DM Sans, Inter, Source Sans)

This pairing creates immediate hierarchy: serif signals editorial weight, sans signals clarity and modernity.

**Alternative that also works:** Single font family used at multiple weights (Light, Regular, Medium, Bold). Creates cohesion when the family has sufficient weight range.

## Specify Exact Fonts and Weights

**Never say "something elegant" or "a nice serif."**

AI will default to adequate fonts (Roboto, Arial) if not given specific direction. Always specify:
- Exact font family name
- Exact weights (e.g., "400 regular, 600 semibold")
- Google Fonts import or CSS font-stack

## Type Scale in CSS Variables

Define a scale that creates clear steps between levels:

```css
:root {
  --font-size-xs:   0.75rem;
  --font-size-sm:   0.875rem;
  --font-size-base: 1rem;
  --font-size-lg:   1.125rem;
  --font-size-xl:   1.25rem;
  --font-size-2xl:  1.5rem;
  --font-size-3xl:  1.875rem;
  --font-size-4xl:  2.25rem;
  --font-size-5xl:  3rem;
  --font-size-6xl:  3.75rem;
}
```

## Letter-Spacing Refinements

**Headlines:** Slightly negative letter-spacing. Serif headlines at -0.02em to -0.03em feel tighter and more editorial.

**Body text:** Default or slightly positive. 0 to 0.01em. Never wide-tracking body text.

**Labels and eyebrow text:** Wide tracking. Uppercase labels at 0.1em to 0.2em letter-spacing signal premium refinement.

```css
/* Eyebrow/label text */
font-size: 0.75rem;
text-transform: uppercase;
letter-spacing: 0.15em;
```

## Whitespace and Typography

**Whitespace gives the eye a place to rest and signals curation.**

Dense text feels cheap. Generous line heights, ample paragraph spacing, and roomy section padding all signal premium.

Recommended line heights:
- Body text: 1.6 to 1.75
- Headlines: 1.1 to 1.25
- Large display: 1.0 to 1.1

## Hierarchy Before Reading

Typography hierarchy should communicate structure before anyone reads a word:

1. What is the main headline? — largest, boldest, most visual weight
2. What is secondary? — smaller, lighter, supporting
3. What is navigational or UI? — compact, uniform, scannable
4. What is body text? — comfortable reading size, neutral weight

If someone cannot understand the page structure before reading, the typography hierarchy is broken.

## Common Typography Mistakes

1. **Too many font weights.** Three weights maximum: regular, medium, bold.

2. **Mixing more than two font families.** One serif + one sans is deliberate. Three or more feels chaotic.

3. **Line height too tight.** Body text below 1.5 line height is hard to read. Aim for 1.6+.

4. **Tracking too loose on body text.** Wide letter-spacing on body paragraphs reads as formal/museum-like.

5. **Type scale without enough contrast.** If h3 and h2 are nearly the same size, there is no hierarchy.

6. **Using display weights for body.** Thin/light weights (100-300) look elegant at large sizes but become unreadable below 18px.

## Related Skills

- aesthetic-principles — overarching principles that apply to all design
- color-and-palette — applies these principles to color choices
- design-quality — use to review typography against these principles
