---
name: design-quality
description: Conduct comprehensive design quality reviews — both before design decisions and after implementation using Playwright. Covers design principle application, responsive layouts, accessibility compliance (WCAG 2.1 AA), and visual quality. Use when reviewing visual changes, evaluating design decisions, or verifying pull request quality.
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [design, quality, review, ui, ux, accessibility, playwright]
    related_skills: [aesthetic-principles, color-and-palette, typography]
---

# Design Quality

## Overview

This skill provides a structured design quality workflow in two modes:
1. **Pre-design review** — applying foundational principles before implementation
2. **Post-implementation review** — verifying quality with Playwright automated testing

It follows rigorous standards inspired by top design teams.

## When to Use

**Pre-design mode:**
- Before implementing any design decision
- When choosing colors, typography, or layout for a new project or feature
- When evaluating design direction against foundational principles

**Post-implementation mode:**
- Reviewing PRs with UI component changes
- Testing responsive design across viewports
- Verifying accessibility compliance
- Validating visual consistency and design quality
- Conducting pre-merge design reviews

## Review Phases

### Phase 0: Pre-Design Principle Check

Apply foundational principles BEFORE writing any code:

**Check against aesthetic-principles:**
- Does this decision reflect restraint, or am I adding elements just because they're possible?
- Does it feel "chosen, not generated"?
- Are there competing CTAs or rainbow palette risks?
- Does this match the emotional goal of the project?

**Check against color-and-palette:**
- Does this follow the 60-30-10 relationship?
- Is there exactly one saturated accent?
- Have I verified WCAG contrast for all text/background combinations?
- Am I using CSS variables via inline styles for custom palette colors, NOT undefined Tailwind utility classes?

**Check against typography:**
- Is the type hierarchy immediately visible before reading?
- Are fonts specified exactly (name + weight), not "something elegant"?
- Does letter-spacing match the context (negative for headlines, wide for labels)?

**Only proceed to implementation if Phase 0 passes.**

### Phase 1: Interaction & User Flow
- Execute primary user flows
- Test all interactive states (hover, active, disabled)
- Verify destructive action confirmations
- Assess perceived performance

### Phase 2: Responsiveness Testing
- Desktop viewport (1440px)
- Tablet viewport (768px)
- Mobile viewport (375px)
- Verify no horizontal scrolling or overlap

### Phase 3: Visual Polish
- Layout alignment and spacing
- Typography hierarchy — is hierarchy visible before reading?
- Color palette consistency
- Visual hierarchy

### Phase 4: Accessibility (WCAG 2.1 AA)
- Keyboard navigation (Tab order)
- Focus states visibility
- Keyboard operability
- Semantic HTML
- Form labels and associations
- Image alt text
- Color contrast (4.5:1 minimum for body text)

### Phase 5: Robustness
- Form validation testing
- Content overflow scenarios
- Loading, empty, error states

### Phase 6: Code Health
- Component reuse vs duplication
- **Design token usage** — are colors using CSS variables via inline styles for custom palette colors?
- **Foundational principle adherence** — does the implementation reflect aesthetic-principles, color-and-palette, and typography decisions?
- Established pattern adherence

### Phase 7: Content & Console
- Grammar and clarity
- Browser console errors/warnings

## Output Format

```
### Design Quality Summary
[Positive opening + overall assessment]

### Findings

#### Blockers
- [Problem + screenshot evidence]

#### High-Priority
- [Problem + screenshot evidence]

#### Medium-Priority / Suggestions
- [Problem]

#### Nitpicks
- Nit: [Problem]
```

## Issue Triage

| Severity | Description |
|----------|-------------|
| [Blocker] | Critical failures - immediate fix required |
| [High-Priority] | Significant issues - fix before merge |
| [Medium-Priority] | Improvements for follow-up |
| [Nitpick] | Minor aesthetic details |

## Dependencies

Requires Playwright MCP server (`mcp__playwright__*` tools) for browser automation and visual testing in post-implementation phases (1-7). Phase 0 requires no tooling — just principles.

## Priority Rule

Foundational principles (aesthetic-principles, color-and-palette, typography) ALWAYS apply. If a project file (CLAUDE.md) specifies different values, the project file wins for that specific project — but foundational principles still apply for the reasoning and relationships.
