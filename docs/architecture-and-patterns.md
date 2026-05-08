# Architecture and Patterns

## Architectural Style
Server-driven UI with Flask + HTMX:
- Backend owns state, rules, and HTML fragment rendering
- Frontend uses declarative HTMX attributes for interaction
- Minimal custom JavaScript for targeted UX enhancements

## Core Patterns
1. Partial Rendering
- Server returns focused HTML fragments for specific UI regions

2. Event-Driven Updates
- Backend emits HTMX triggers
- Dependent components refresh via event listeners

3. Progressive Enhancement
- Simple HTML first
- Dynamic behavior layered through HTMX attributes

4. Layered Validation
- Field-level checks
- Business rule checks
- Persistence actions only after validation passes

## Data Evolution Path
- Early steps use in-memory/mock data
- Advanced path transitions to SQLAlchemy and SQLite

## Maintainability Principles
- Keep routes cohesive and explicit
- Use reusable partial templates
- Prefer deterministic server responses over client-side state duplication

## Related Lessons
- UI interaction flow: [lessons/lesson-03.md](../lessons/lesson-03.md) to [lessons/lesson-32.md](../lessons/lesson-32.md)
- Data integration: [lessons/lesson-33.md](../lessons/lesson-33.md)
- Production concerns: [lessons/lesson-37.md](../lessons/lesson-37.md) to [lessons/lesson-41.md](../lessons/lesson-41.md)
