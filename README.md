# HTMX + Flask Learning

A structured curriculum for building server-rendered web applications with Flask and HTMX. 48 lessons across 10 independent modules — from environment setup through production deployment.

## Topics Covered

- Flask fundamentals and Blueprint-based project structure
- HTMX core attributes and server-driven UI patterns
- Full CRUD with inline editing and partial HTML updates
- Search, filtering, sorting, and pagination
- UX feedback — flash messages, polling, and modals
- Template inheritance and progressive enhancement
- Out-of-band swaps and clean route architecture
- SQLAlchemy, form validation, and MySQL integration
- Session-based authentication and file uploads
- Docker, CI/CD, Azure, and Render deployment

## Architecture

Server-driven UI: Flask owns state and renders HTML fragments; HTMX replaces targeted DOM regions on response. No frontend framework. Behavior is expressed through declarative `hx-*` attributes on standard HTML elements.

```
Browser ──hx-get/post/put/delete──► Flask route
Flask route ──renders partial──► Jinja2 template fragment
Fragment ──replaces target element──► Browser DOM
```

## Repository Structure

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
    ├── 01-introduction/              (2 lessons)
    ├── 02-htmx-core-attributes/      (7 lessons)
    ├── 03-flask-architecture/        (5 lessons)
    ├── 04-interactive-crud/          (6 lessons)
    ├── 05-search-filter-sort-paginate/ (6 lessons)
    ├── 06-ux-feedback-and-realtime/  (7 lessons)
    ├── 07-advanced-htmx-patterns/    (3 lessons)
    ├── 08-data-persistence/          (3 lessons)
    ├── 09-application-features/      (2 lessons)
    └── 10-production-and-deployment/ (7 lessons)
```

## Start Here

[docs/index.md](docs/index.md) — full module and lesson index

## Documentation

| File | Purpose |
|------|---------|
| [docs/course-overview.md](docs/course-overview.md) | Scope, outcomes, entry points |
| [docs/learning-path.md](docs/learning-path.md) | Phase breakdown and sequencing |
| [docs/architecture-and-patterns.md](docs/architecture-and-patterns.md) | Design patterns and project structure |
| [docs/setup-and-runbook.md](docs/setup-and-runbook.md) | Prerequisites and study workflow |
| [docs/database-notes.md](docs/database-notes.md) | DB seed script reference |
| [docs/changinglog.md](docs/changinglog.md) | Change history |

---

Copyright (c) 2026 Dr. Georges Bou Ghantous. All rights reserved. See [LICENSE.md](LICENSE.md).

---

<sub><i><span style="color:#B0B0B0">👤 Author: Dr. Georges Bou Ghantous</span></i></sub>
