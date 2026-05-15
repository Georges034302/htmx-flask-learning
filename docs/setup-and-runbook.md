# Setup and Runbook

## Repository Mode
This repository currently stores curriculum assets (modules/docs/data) and is intended as a modules-first source.

## Minimum Prerequisites
- Python 3.10+
- Git
- SQLite CLI (`sqlite3`) for DB modules
- Docker/Azure CLI only for advanced deployment modules

## Study Workflow
1. Open [docs/index.md](../docs/index.md)
2. Complete modules in order
3. Apply each lesson into a clean working project directory
4. Validate expected behavior at each checkpoint

## Database Script Usage
Initialize seeded employee data for DB-integrated steps:

```bash
sqlite3 employees.db < data/employee_db_setup.sql
```

Reference script: [data/employee_db_setup.sql](../data/employee_db_setup.sql)

## Recovery Runbook
If local progress diverges:
1. Re-open the target lesson
2. Re-apply the lesson steps in a fresh branch/workspace
3. Re-run validation checkpoints before moving forward

## Operational Note
Lessons 37-41 depend on infrastructure and credentials (container runtime, cloud subscription, CI secrets).
