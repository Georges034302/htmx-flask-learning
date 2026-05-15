# Database Notes

## Objective
Provide a consistent, reproducible database baseline for advanced modules.

## Canonical Script
- Setup script: [data/employee_db_setup.sql](../data/employee_db_setup.sql)

## What the Script Does
- Drops existing `employees` table if present
- Creates `employees` table
- Inserts 12 seed employee records
- Wraps operations in a transaction (`BEGIN`/`COMMIT`)

## Execute
```bash
sqlite3 employees.db < data/employee_db_setup.sql
```

## Verify
```bash
sqlite3 employees.db "SELECT COUNT(*) FROM employees;"
```
Expected result: `12`

## Module Mapping
- Primary: [08-data-persistence/01-sqlalchemy-integration.md](../modules/08-data-persistence/01-sqlalchemy-integration.md)
- Related: [08-data-persistence/02-form-validation.md](../modules/08-data-persistence/02-form-validation.md)

## Notes
- Script is SQLite-friendly and SQL-portable with minor adjustments.
- Re-running resets table state by design for deterministic practice.
