---
name: web-travel-research
description: Research flights and hotels using browser automation — handles bot protection on travel sites
triggers:
  - find flights to [destination]
  - search for hotels in [city]
  - travel deal research
  - Tampa to Madrid October 2026
---

# Web-Based Travel Research

## Context
Researching flights and hotels for international travel (Tampa FL to Madrid, Oct 2026 trip) involved significant trial and error with browser automation tools.

## Key Findings

### Sites with Bot Protection (avoid or use with caution)
- **Expedia** — Bot detection wall ("Show us your human side...")
- **Skyscanner** — CAPTCHA/robot verification
- **Google Search** — "Unusual traffic" blocking, requires JavaScript human verification
- **Google Flights** — Pre-filled URLs often don't work; form interaction triggers blocks
- **Travelzoo** — HTTP protocol errors

### Sites That Partially Work
- **KAYAK** — Landing page loads, packages search available, but Madrid wasn't pre-filled in package search. Flights search form works but results may vary
- **Booking.com** — Generally accessible for hotels

### What Didn't Work
- Direct URL manipulation for pre-filled forms (Google Flights)
- Generic search engine queries for specific deals
- Browser snapshot of empty/blank pages

## Successful Approach Pattern

1. **Start with meta-search aggregators**: KAYAK, Google Flights (manual entry preferred)
2. **For flights**: Use direct search URLs with query parameters rather than form automation
3. **For hotels**: Booking.com, Hotels.com, or KAYAK stays
4. **For packages**: Look for "flight + hotel" bundle options on KAYAK or directly from airlines

## Alternative Strategies

- **Set price alerts** on Google Flights (even if you can't see results, you can set up tracking)
- **Check airline websites directly**: Iberia, American Airlines, Delta often have competitive Europe fares
- **Use miles/points aggregators**: British Airways Avios, Amex Fixed Miles, etc.
- **Consider nearby airports**: Tampa (TPA), Orlando (MCO), Miami (MIA) for more flight options

## Verification Notes
- Most travel sites have aggressive bot detection
- Browser automation on travel sites often triggers verification challenges
- Manual browsing remains the most reliable method for complex searches
- Mobile user-agent may bypass some restrictions

## When to Use This Skill
- Task involves finding flights/hotels for specific dates and destinations
- Browser-based research has been attempted and failed
- Need to document alternative approaches for travel research
