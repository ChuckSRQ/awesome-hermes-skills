---
name: tall-stack-dev
description: Laravel TALL stack (Tailwind, Alpine.js, Laravel, Livewire) development workflow. Use when building Livewire components, admin interfaces with FilamentPHP, Docker-based Laravel Sail environments, or any TALL stack project.
---

# Laravel TALL Stack Development Skill

## Stack Overview

- **Tailwind CSS** - Utility-first CSS
- **Alpine.js** - Lightweight frontend JS
- **Laravel** - PHP backend framework
- **Livewire** - Reactive UI components
- **FilamentPHP** - Admin interfaces
- **Laravel Sail** - Docker dev environment
- **Pest** - PHP testing

## Dev Environment (Laravel Sail)

```bash
./vendor/bin/sail up -d           # Start Docker
./vendor/bin/sail down            # Stop
./vendor/bin/sail artisan migrate --seed
./vendor/bin/sail npm run dev      # Frontend dev
./vendor/bin/sail artisan test    # Tests
```

## Component Architecture

| Need | Solution |
|------|----------|
| Admin + CRUD | FilamentPHP Resource |
| User-facing + real-time | Livewire Component |
| API + external integrations | Laravel Controller |

## MCP Tools

- `mcp__serena__*` - Code analysis and navigation
- `mcp__context7__*` - Documentation access
- `mcp__browsermcp__*` - Browser debugging
- `mcp__zen__codereview` - Code review
- `mcp__zen__precommit` - Quality gates
- `mcp__zen__secaudit` - Security audit

## Key Paths

- `app/Livewire/` - Reactive components
- `app/Services/` - Business logic
- `app/Models/` - Eloquent models
- `resources/views/livewire/` - Livewire templates
