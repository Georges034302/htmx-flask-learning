# Architecture and Patterns

## Architectural Style

Server-driven UI with Flask + HTMX:
- Backend owns state, business rules, and HTML fragment rendering
- Frontend uses declarative `hx-*` attributes for interaction
- No frontend framework; minimal custom JavaScript

## Project Structure

```
htmx-flask-learning/
├── LICENSE.md
├── README.md
├── data/
│   ├── employee_db_setup.sql    # seed script for DB modules
│   └── mock.py                  # in-memory mock dataset
├── docs/
│   ├── index.md                 # full course index
│   ├── architecture-and-patterns.md
│   ├── course-overview.md
│   ├── learning-path.md
│   ├── setup-and-runbook.md
│   ├── database-notes.md
│   └── changinglog.md
└── modules/
    ├── 01-introduction/
    ├── 02-htmx-core-attributes/
    ├── 03-flask-architecture/
    ├── 04-interactive-crud/
    ├── 05-search-filter-sort-paginate/
    ├── 06-ux-feedback-and-realtime/
    ├── 07-advanced-htmx-patterns/
    ├── 08-data-persistence/
    ├── 09-application-features/
    └── 10-production-and-deployment/
```

## Core Patterns

### 1. Partial Rendering
Server returns focused HTML fragments for specific UI regions. Full page reloads are avoided; only the relevant element is replaced.

### 2. Event-Driven Updates
Backend emits HTMX response headers to trigger dependent component refreshes without client-side event wiring.

### 3. Progressive Enhancement
Pages function with direct browser navigation. HTMX layered on top adds reactivity without breaking baseline behavior.

### 4. Out-of-Band Swaps
A single Flask response updates multiple independent DOM regions using `hx-swap-oob`, avoiding redundant requests.

### 5. Layered Validation
Field-level checks → business rule checks → persistence. No write to the database until all validation passes.

## Data Evolution Path

| Stage | Storage |
|-------|---------|
| Early modules | In-memory mock (`data/mock.py`) |
| Module 08 | SQLite via SQLAlchemy |
| Module 08 (advanced) | MySQL with environment-aware config |

## Route Design Principles

- Resource-based naming: `/employees/<id>/edit`, `/employees/<id>/row`
- Blueprints for route grouping at scale
- Partial templates co-located with the feature they serve

## Related Modules

| Topic | Module |
|-------|--------|
| First HTMX interactions | [02-htmx-core-attributes](../modules/02-htmx-core-attributes/) |
| Blueprint structure | [03-flask-architecture/04-flask-blueprints.md](../modules/03-flask-architecture/04-flask-blueprints.md) |
| Template inheritance | [03-flask-architecture/05-template-inheritance.md](../modules/03-flask-architecture/05-template-inheritance.md) |
| OOB swaps | [07-advanced-htmx-patterns/02-oob-swaps.md](../modules/07-advanced-htmx-patterns/02-oob-swaps.md) |
| Clean route design | [07-advanced-htmx-patterns/03-clean-architecture.md](../modules/07-advanced-htmx-patterns/03-clean-architecture.md) |
| SQLAlchemy integration | [08-data-persistence/01-sqlalchemy-integration.md](../modules/08-data-persistence/01-sqlalchemy-integration.md) |
| Azure production deployment | [docs/production.md](production.md) |
| Production config | [10-production-and-deployment](../modules/10-production-and-deployment/) |
