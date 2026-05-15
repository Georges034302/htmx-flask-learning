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
- DRA-based design system (`static/css/main.css`) — dark sidebar layout, data table, modals, flash messages
- Docker and Gunicorn (production WSGI)
- Azure Key Vault secrets management and OIDC authentication
- Azure Container Apps deployment with Managed Identity
- Kubernetes (AKS) deployment with Helm 3 and Key Vault CSI driver
- GitHub Actions CI/CD with OIDC (no stored credentials)
- Azure DevOps Pipelines with Workload Identity Federation

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
├── data/                 # mock dataset and DB seed script
├── docs/                 # course documentation
├── static/
│   └── css/
│       └── main.css      # DRA-based design system (single stylesheet)
└── modules/              # 10 lesson modules
```

Full structure: [docs/architecture-and-patterns.md](docs/architecture-and-patterns.md)

## Start Here

[docs/index.md](docs/index.md) — full module and lesson index

## Documentation

| File | Purpose |
|------|---------|
| [static/css/main.css](static/css/main.css) | Dashboard design system — tokens, layout, table, buttons, flash, modal |
| [docs/production.md](docs/production.md) | Azure production deployment reference and architecture |
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
