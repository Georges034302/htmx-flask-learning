# Lesson 02: Add CSS Styling and Improve UX Structure

## Concept
Add CSS Styling and Improve UX Structure.


## 1. Add CSS Styling and Improve UX Structure

### Goal
Add a stylesheet to improve readability, layout, and visual structure without changing architecture.

### 1.1 Create the CSS folder and file

The project uses a pre-built design system at `static/css/main.css`.
If you followed Lesson 01-02, the folder was already created with `mkdir -p static/css`.

Otherwise create it now:

```bash
mkdir -p static/css
touch static/css/main.css
```

Flask serves every file inside `/static/` automatically via `url_for('static', ...)`.

### 1.2 Link main.css in index.html

Inside `<head>`, below the HTMX script tag:

```html
<link rel="stylesheet" href="{{ url_for('static', filename='css/main.css') }}">
```

`url_for('static', filename='css/main.css')` is the correct Flask convention for resolving static paths regardless of deployment prefix.

### 1.3 Design system — static/css/main.css

`main.css` is the single source of truth for all styles in this project.
It provides a complete set of ready-to-use CSS classes:

| Class | Purpose |
|---|---|
| `.app` | Two-column grid: dark sidebar + light main area |
| `.sidebar` / `.side-nav` | Dark navigation sidebar |
| `.main` / `.page-header` | Content area and page title block |
| `.data-table` | Styled employee table (bordered, striped, hoverable) |
| `.btn` / `.btn-primary` / `.btn-ghost` / `.btn-danger` | Button variants |
| `.add-panel` | Card wrapper for Add Employee form |
| `.search-bar` | Search input container |
| `.controls-bar` | Toolbar row above the table |
| `.flash` / `.flash-success` / `.flash-error` / `.flash-warning` | Flash message styles |
| `.panel` / `.panel-title` | Generic card panel |
| `.pill` | Department badge / tag |
| `.pagination` | Page navigation controls |
| `.lightbox` / `.lightbox-card` | Modal overlay |
| `.htmx-indicator` / `.spinner` | HTMX request loading state |
| `.card-grid` / `.card` | Stat summary cards |
| `.empty-state` | Empty table placeholder |

No custom CSS is needed in `index.html` or any partial — add classes from this list directly to your HTML elements.

### 1.4 Current layout structure

```html
<div class="app">

    <nav class="sidebar">
        <div class="brand">...</div>
        <nav class="side-nav">...</nav>
    </nav>

    <div class="main">
        <div class="page-header">...</div>
        <div class="controls-bar">...</div>
        <div id="employees-container">...</div>
    </div>

</div>
```

- `.controls-bar`: places Add Employee form and Search in one row.
- `.data-table`: replaces `border="1" cellpadding="10"` on every `<table>`.
- Flash messages use `.flash .flash-success` / `.flash-error` / `.flash-warning`.
- Responsive breakpoint at `max-width: 800px` collapses sidebar to a top bar.

### 1.5 What you learned
- Flask static files convention — `url_for('static', filename=...)`
- Design system approach: one CSS file, consistent classes throughout
- CSS integration with HTMX — no extra JavaScript needed
- Separation of structure and styling
- HTMX works perfectly with plain HTML + a lightweight stylesheet

---

## Fix: Live Search — switch beforeend to innerHTML

Changed `hx-swap` on the live search input from `beforeend` to `innerHTML`.

**Before:** each keystroke appended results, so old results accumulated.  
**After:** each keystroke replaces the result container, showing only current matches.

```html
hx-swap="innerHTML"
```

---

## Fix: Latest Updates — trigger on employee-added event

The `/latest` section previously only triggered on `load` (page load only).

Updated `hx-trigger` to also respond to `employee-added from:body`:

```html
hx-trigger="load, employee-added from:body"
```

**Note:** `/latest` is a learning demo for HTMX's auto-load trigger. Its content is hardcoded server-side (not a real activity feed). Delete and update are row-level `outerHTML` swaps — they do not fire `employee-added`, so they do not trigger a latest refresh. Only Add Employee fires that event.

Current page layout note:
- Automatic Content now sits below the Employee Table section to keep the Add/Search controls and table interactions visually grouped.

---

