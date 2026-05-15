# Lesson 05: Template Inheritance (base.html)

## Concept
Template Inheritance (base.html).

## 1. Template Inheritance (base.html)

### Goal
Replace repeated boilerplate HTML (DOCTYPE, `<head>`, HTMX CDN, `<body>`) across templates with a single `base.html` layout that all full-page templates inherit from.

---

### 1.1 The problem: duplicated HTML

Currently, every full-page template in `templates/` repeats this structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HTMX Learning</title>
    <script src="https://unpkg.com/htmx.org@1.9.12"></script>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/main.css') }}">
</head>
<body>
    <!-- page-specific content -->
</body>
</html>
```

Problems with this pattern:
- Adding a new script tag (e.g., a new CSS file) requires editing every template.
- Changing the page title format means touching all files.
- No single place to define the nav bar or footer.

Jinja2 solves this with **template inheritance**.

---

### 1.2 Create templates/base.html

Create file: `templates/base.html`

```html
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>{% block title %}HTMX + Flask{% endblock %}</title>

    <!-- HTMX CDN — loaded once, inherited by all child templates -->
    <script src="https://unpkg.com/htmx.org@1.9.12"></script>

    <!-- Dashboard design system -->
    <link rel="stylesheet" href="{{ url_for('static', filename='css/main.css') }}">

    <!-- Child templates can inject extra <head> content here -->
    {% block extra_head %}{% endblock %}
</head>

<body>

<div class="app">

    <!-- Sidebar navigation -->
    <nav class="sidebar">
        <div class="brand">
            <span>
                <div class="brand-name">Employee Hub</div>
                <div class="brand-tag">HTMX + Flask</div>
            </span>
        </div>

        <div class="side-section-title">Navigation</div>

        <nav class="side-nav">
            <a href="/" class="{{ 'active' if request.path == '/' else '' }}">
                Dashboard
            </a>
        </nav>

        <div class="side-author">
            <div>
                <div class="name">Admin</div>
                <div class="role">Employee Dashboard</div>
            </div>
        </div>
    </nav>

    <!-- Main content area -->
    <div class="main">

        <!-- Flash messages rendered globally -->
        {% with messages = get_flashed_messages(with_categories=True) %}
            {% if messages %}
                <div id="flash-container">
                    {% for category, message in messages %}
                        <div class="flash flash-{{ category }}">{{ message }}</div>
                    {% endfor %}
                </div>
            {% endif %}
        {% endwith %}

        <!-- Each child template fills this block -->
        {% block content %}{% endblock %}

    </div><!-- /.main -->

</div><!-- /.app -->

    <!-- Child templates can inject page-specific scripts here -->
    {% block extra_scripts %}{% endblock %}

</body>
</html>
```

Key Jinja2 constructs:
- `{% block title %}...{% endblock %}` — defines a named slot with a default value.
- `{% block content %}{% endblock %}` — defines an empty slot that child templates must fill.
- `{{ url_for(...) }}` — resolves static file paths safely regardless of deployment prefix.
- `{% with %}` — creates a local variable scope; used here for flash messages.
- `.app` grid gives the dark sidebar + light content layout from `main.css`.
- `.flash-{{ category }}` maps Flask's flash categories (`success`, `error`, `warning`) to CSS colour classes.

---

### 1.3 Update templates/index.html to extend base.html

Replace the full contents of `templates/index.html` with:

```html
{% extends "base.html" %}

{% block title %}Employee Dashboard{% endblock %}

{% block content %}

<div class="page-header">
    <div>
        <h1>Employees</h1>
        <p>Search, add, and manage employee records.</p>
    </div>
</div>

<div class="controls-bar">

    <div class="search-bar">
        <input
            type="text"
            name="query"
            placeholder="Search employees…"
            hx-get="/employees"
            hx-trigger="keyup changed delay:500ms"
            hx-target="#employees-container"
            hx-swap="innerHTML">
    </div>

    <div id="search-count" class="search-count"></div>

</div>

<div class="add-panel">
    <h3>Add Employee</h3>
    <form
        hx-post="/add-employee"
        hx-target="#employees-container"
        hx-swap="innerHTML"
        hx-trigger="submit">

        <input type="text" name="name" placeholder="Name" required>
        <input type="text" name="department" placeholder="Department" required>
        <button type="submit" class="btn btn-primary">Add Employee</button>

    </form>
</div>

<div id="flash-container"></div>

<div
    id="employees-container"
    hx-get="/employees"
    hx-trigger="load"
    hx-swap="innerHTML">
</div>

<div id="modal"></div>

{% endblock %}

{% block extra_scripts %}
<script>
    document.body.addEventListener("employee-added", function () {
        document.querySelector("form").reset();
    });
</script>
{% endblock %}
```

How this works:
- `{% extends "base.html" %}` — tells Jinja2 to use `base.html` as the parent layout.
- `{% block title %}Employee Dashboard{% endblock %}` — overrides the default title.
- `{% block content %}...{% endblock %}` — injects the page body into the `.main` area.
- `{% block extra_scripts %}...{% endblock %}` — adds the form reset listener just before `</body>`.
- `.page-header` renders the page title block from `main.css`.
- `.controls-bar` places the search bar in a toolbar row above the table.
- `.add-panel` wraps the Add Employee form in a styled card.
- `#modal` is the mount point for HTMX-injected modal content (Module 06).
- Everything outside a `{% block %}` tag is **ignored** in child templates.

---

### 1.4 Why partials do NOT extend base.html

HTMX partial templates in `templates/partials/` must **not** extend `base.html`.

Reason:
- HTMX swaps inject only the fragment returned by the server into a specific DOM target.
- If a partial included a full `<!DOCTYPE html>` layout, the browser would receive nested HTML — invalid and broken.

Correct partial (no extends):

```html
{# templates/partials/employees_table.html #}
<table class="data-table">
    <thead>
        <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Department</th>
            <th>Actions</th>
        </tr>
    </thead>
    <tbody>
        {% for employee in employees %}
        <tr>
            <td>{{ employee.id }}</td>
            <td>{{ employee.name }}</td>
            <td><span class="pill">{{ employee.department }}</span></td>
            <td class="actions">
                <button
                    class="btn btn-danger btn-sm"
                    hx-delete="/delete-employee/{{ employee.id }}"
                    hx-confirm="Are you sure?"
                    hx-target="closest tr"
                    hx-swap="outerHTML">
                    Delete
                </button>
            </td>
        </tr>
        {% endfor %}
    </tbody>
</table>
```

Rule: **Full pages extend base. Partials are standalone fragments.**

---

### 1.5 Verify the result

Restart Flask:

```bash
python app.py
```

Open browser at `http://127.0.0.1:5000`.

Expected:
- Page loads with the full layout from `base.html`.
- Title tab shows "Employee Dashboard".
- HTMX CDN is loaded once from `base.html`.
- Flash messages appear in the global container when triggered.
- Employee form and table work exactly as before.

Check in browser DevTools → Sources:
- `index.html` should show only the `{% block content %}` region in the page source.
- No duplicated `<script src="htmx...">` tags.

---

### Project structure after this step

```
templates/
├── base.html              ← new: shared layout
├── index.html             ← updated: now extends base.html
└── partials/
    ├── employees_table.html   ← unchanged: standalone fragment
    ├── search_results.html    ← unchanged: standalone fragment
    └── ...
```

---

### Summary

| Pattern | Template type | Extends base? |
|---|---|---|
| Full page (`/`, `/login`, `/dashboard`) | Page template | Yes — `{% extends "base.html" %}` |
| HTMX fragment (`/employees`, `/add-employee`) | Partial | No — raw fragment only |
| Error page (404, 500) | Page template | Yes — `{% extends "base.html" %}` |
