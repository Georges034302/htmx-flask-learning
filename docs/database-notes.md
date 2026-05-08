# Database Notes

## Objective
Provide a consistent, reproducible database baseline for advanced lessons.

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

## Lesson Mapping
- Primary: [lessons/lesson-33.md](../lessons/lesson-33.md)
- Related: [lessons/lesson-34.md](../lessons/lesson-34.md)

## Notes
- Script is SQLite-friendly and SQL-portable with minor adjustments.
- Re-running resets table state by design for deterministic practice.
