# ChangingLog

## Purpose
Track meaningful curriculum/documentation changes at repository level.

## Format
Use dated entries with concise impact summaries.

## Entries

### 2026-05-16
- Added `static/css/main.css` — DRA-adapted single-file design system (tokens, dark-mode, sidebar layout, `.data-table`, `.btn` variants, `.flash` variants, `.lightbox`, `.pagination`, `.card-grid`, `.htmx-indicator`, responsive breakpoint)
- Applied `main.css` classes across all 10 modules; removed all inline CSS and legacy `style.css` references
- Added `.panel-login` and `.flash ul` rules to `main.css` for login-page centering and error-list spacing
- Fixed bare `<button>` tags in modules 07, 09 — all submit buttons now use `.btn .btn-primary`
- Fixed invalid HTML in module 09 session-auth (`<a><button>` nesting) — replaced with `<a class="btn btn-ghost">`
- Fixed inline `style=` attributes in modules 08, 09 — replaced with `.panel-login` and `.page-header` classes
- Updated `README.md`: added DRA design system to Topics Covered, `static/css/main.css` to project tree and docs table
- Updated `docs/architecture-and-patterns.md`: Pattern 6 "Single-File Design System", class reference table
- Verified: 48 lessons across 10 modules, all `docs/index.md` links resolve correctly, CSS braces balanced (116/116)

### 2026-05-15
- Renamed `lessons/` directory to `modules/`
- Organized all 48 lessons into 10 named module directories
- Renamed lesson files to local `01`-based indexing within each module
- Moved `index.md` from `modules/` to `docs/` and restructured as module-grouped table
- Moved `license.md` to root as `LICENSE.md`
- Rewrote `README.md`: removed stale app file references, added topics list, architecture overview, and doc table
- Updated `architecture-and-patterns.md`: added project tree, replaced stale lesson links with module paths
- Updated `learning-path.md`: replaced lesson-number phases with module-number phases
- Fixed stale `../docs/index.md` self-reference in `course-overview.md`
- Fixed stale `lesson-33/34` links in `database-notes.md`

### 2026-05-08
- Converted repository focus to modules-first curriculum assets
- Added structured modules directory and indexed learning path
- Removed source-of-truth references to previous setup file in modules
- Aligned lesson notes with current UI/CSS behavior updates
- Added SQL seed script: [data/employee_db_setup.sql](../data/employee_db_setup.sql)
- Updated lesson 33 to use SQL script seeding flow
- Added repository-level docs set in [docs](.)

## Update Rule
For every substantial change to lesson flow, sequencing, or execution guidance, append one entry here.
