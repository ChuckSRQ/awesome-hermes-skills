---
name: color-and-palette
description: Universal color theory and palette-building principles for web design. Covers relationships, temperature, psychology, WCAG contrast, and critical Tailwind v4 implementation rules. Use when building or evaluating any color system.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [color, color-theory, palette, contrast, accessibility]
    related_skills: [aesthetic-principles, typography, design-quality]
---

# Color and Palette

## The 60-30-10 Rule (Relationship, Not Recipe)

The single most useful formula in color design. Every professional palette follows it:

| Role | % of Visual Space | Function |
|------|-------------------|----------|
| Dominant (background, large areas) | 60% | Sets the mood, establishes atmosphere |
| Secondary (cards, sections, supporting UI) | 30% | Supports the dominant, creates structure |
| Accent (CTAs, highlights, links) | 10% | Draws the eye to what matters most |

The dominant is almost always a neutral. The secondary can be a tint of the dominant or a near-neutral surface color. The accent is the ONE chromatic note — one hue, used sparingly.

**This is a relationship principle, not a hex code recipe.** The percentages describe how visual attention distributes, not which colors to use.

## Five Color Relationships

Choose one archetype per project. Mixing archetypes is how amateur palettes happen.

**1. Monochromatic** — One hue, multiple tints/shades. Cohesive, harmonious, lowest risk of clashing. Best for: data apps, dev tools, professional services, minimal luxury.

**2. Analogous** — Three adjacent hues on the color wheel. Creates a soothing, cohesive feel. Best for: healthcare, wellness, lifestyle, editorial. Risk: low visual tension means weak hierarchy.

**3. Complementary** — Two hues opposite each other on the wheel. Maximum contrast, high visual tension. Use one dominant and the other as a small accent. Best for: brands that want energy and confidence. Risk: if both hues compete equally, they fight.

**4. Triadic** — Three hues equally spaced (120 degrees apart). Vibrant, balanced, maximum color variety. Risk: almost impossible to balance at equal saturation — one hue must clearly dominate.

**5. Split-Complementary** — One hue plus two adjacent to its complement. Like complementary but with less tension. Easier to balance than triadic. Best for: reaching for bold without aggression.

## Color Temperature

Temperature sets emotional tone:

**Warm colors** (reds, oranges, yellows, warm neutrals): Feel intimate, close, energetic, organic, human. Best for: lifestyle, hospitality, food, warm consumer brands.

**Cool colors** (blues, teals, purples, cool neutrals): Feel distant, calm, technical, trustworthy, premium. Best for: tech, finance, healthcare, professional services, luxury.

## The One Saturated Color Rule

**Never use more than one saturated color at full intensity.**

Muted tones create harmony. One saturated accent plus everything else muted equals professional palette. Saturated colors fight each other for attention.

## Hue Psychology

| Hue | Best For | Avoid In |
|-----|----------|----------|
| Red | CTAs that convert, sale badges, food brands | Luxury, corporate |
| Orange | Consumer apps, startups, food, playful | Luxury, finance |
| Yellow | Accent only — too much fatigues eyes | As dominant, as text on white |
| Green | Environmental, finance, healthcare, wellness | Over-saturated lime — reads cheap |
| Blue | Corporate, finance, healthcare, tech, water | Warmth contexts — feels cold |
| Purple | Premium tech, creative tools, beauty | Too much reads as childish |
| Gold/Brass | Universal accent for premium — works on light AND dark | Bright yellow (#ffd700) — cheapens instantly |
| Brown/Earth | Coffee, artisan, ranch, rustic luxury | Cool/tech contexts |

## Contrast Requirements (WCAG 2.1 AA)

| Element Type | Minimum Ratio | Target |
|-------------|-------------|--------|
| Normal text (under 18px) | 4.5:1 | 7:1+ |
| Large text (18px+ or 14px bold) | 3:1 | 4.5:1+ |
| UI components and graphical objects | 3:1 | — |
| Decorative elements | No requirement | — |

**Quick safe references:**
- #1a1a1a on #ffffff = 16:1 (excellent)
- #6b7280 on #ffffff = 5.9:1 (passes AA)
- #9ca3af on #ffffff = 2.5:1 (fails — never use for body text)

## How to Build a Palette in 5 Steps

**Step 1:** Identify the emotional goal. What feeling should the site/project convey?

**Step 2:** Choose the dominant hue. Usually white or a very light neutral.

**Step 3:** Choose the accent — the hardest decision. This is the ONE chromatic color.

**Step 4:** Build the neutral hierarchy. Text: near-black / Muted: medium gray / Border: light gray / Surface: off-white.

**Step 5:** Verify contrast. Run every text combination through a contrast checker.

## Critical: Tailwind v4 Silent Class Failure

**Tailwind v4 silently ignores undefined custom color classes.** No error, no warning. The class simply produces no visible color.

**Symptoms:**
- Hero sections render with no background (transparent)
- Text that should be colored appears in default/black
- Layout looks broken with zero build errors
- No console errors in browser

**Common undefined classes:**
- `bg-navy`, `bg-gold`, `bg-sapphire`, `bg-emerald`, `bg-rust`, `bg-burgundy`
- `text-gold`, `text-amber-400`, `text-blue-100`
- `from-navy-deep`, `via-navy`, `to-navy`, `to-navy-light`

**The fix — always use CSS variables via inline styles:**

```tsx
// WRONG — undefined class, renders as nothing
<div className="bg-navy text-gold">

// CORRECT — always works
<div style={{ backgroundColor: "var(--color-navy-light)", color: "var(--color-gold-light)" }}>
```

**Rule: For any color in your custom palette, always use inline styles with CSS variables. Never use Tailwind utility class names for colors outside the standard Tailwind palette.**

## Related Skills

- aesthetic-principles — overarching principles that apply to all design
- typography — applies these principles to type decisions
- design-quality — use to review color choices against these principles
