# Lesson 46: Clean Architecture and Route Design for HTMX Apps

## Concept
Clean Architecture and Route Design for HTMX Apps.

## 1. Clean Architecture and Route Design for HTMX Apps

### Goal
Establish clear, consistent naming conventions for Flask routes and template files in HTMX applications — distinguishing between full-page routes and fragment routes — so the codebase scales without confusion.

> **Prerequisites:** Lesson 18 (refactor), Lesson 19 (Blueprints), Lesson 42 (template inheritance), Lesson 43 (detecting HTMX requests). This lesson is a design reference, not a new feature.

---

### 1.1 The problem with ad-hoc route naming

As the app grows, route naming becomes inconsistent:

```
/employees         → returns full page OR fragment (ambiguous)
/employees-table   → returns table fragment
/add-employee      → POST, returns fragment
/delete-employee/1 → DELETE, returns empty
/employee-row/1    → returns a single row
/close-modal       → returns empty string to clear modal
```

Problems:
- No clear signal whether a route returns a page or a fragment.
- Routes mix verbs and nouns inconsistently (`/add-employee` vs `/employee-row`).
- Hard to onboard new developers — they must read every route to understand what it returns.

---

### 1.2 Page routes vs fragment routes

Define two categories:

**Page routes** — return a full HTML page (or redirect):
- Intended for browser navigation.
- Use progressive enhancement (Lesson 43) to also serve HTMX.
- Return `render_template("some_page.html")` (which extends `base.html`).

**Fragment routes** — return an HTML fragment only:
- Never called by the browser directly (no bookmark, no direct navigation).
- Return `render_template("partials/something.html")`.
- May also return an empty string (for delete/close actions).

---

### 1.3 Naming convention for HTMX fragment routes

Recommended convention:

| Route pattern | HTTP method | Returns | Example |
|---|---|---|---|
| `/resource` | GET | Full page | `/employees` |
| `/resource` | POST | Fragment or redirect | `/employees` (add) |
| `/resource/<id>` | GET | Full detail page or fragment | `/employees/1` |
| `/resource/<id>` | PUT | Fragment (updated row/card) | `/employees/1` |
| `/resource/<id>` | DELETE | Empty string | `/employees/1` |
| `/resource/<id>/edit` | GET | Edit form fragment | `/employees/1/edit` |
| `/resource/<id>/row` | GET | Single row fragment (cancel/restore) | `/employees/1/row` |

Using the resource as the URL noun and HTTP methods (GET/POST/PUT/DELETE) as the verb:
- Removes the need for `/add-employee`, `/delete-employee`, `/update-employee`.
- All employee operations live under `/employees` or `/employees/<id>`.

---

### 1.4 Refactor routes/main_routes.py to follow the convention

Below is the route structure with clean naming applied. The logic inside each route does not change — only the URLs are reorganised.

```python
from flask import Blueprint, render_template, request, flash
import time

main = Blueprint("main", __name__)

# ---------------------------------------------------------------------------
# PAGE ROUTE
# ---------------------------------------------------------------------------

@main.route("/")
def home():
    """Full page — redirects to /employees."""
    return render_template("index.html")


# ---------------------------------------------------------------------------
# RESOURCE: /employees
# ---------------------------------------------------------------------------

@main.route("/employees", methods=["GET"])
def list_employees():
    """
    GET /employees
    Page route: returns full page for browser navigation.
    Fragment route: returns table partial for HTMX requests.
    """
    from routes.main_routes import is_htmx_request  # uses helper from Lesson 43
    from data.mock import employees as employees_data

    query_str = request.args.get("query", "").lower()
    sort = request.args.get("sort", "id")
    page = int(request.args.get("page", 1))
    per_page = 5

    filtered = [
        e for e in employees_data
        if query_str in e["name"].lower() or query_str in e["department"].lower()
    ]
    sort_key = sort if sort in ("id", "name", "department") else "id"
    sorted_employees = sorted(filtered, key=lambda e: str(e.get(sort_key, "")))
    total_pages = -(-len(sorted_employees) // per_page)
    start = (page - 1) * per_page
    paginated = sorted_employees[start:start + per_page]

    ctx = dict(employees=paginated, query=query_str, sort=sort,
               page=page, total_pages=total_pages)

    if is_htmx_request():
        return render_template("partials/employees_table.html", **ctx)
    return render_template("index.html", **ctx)


@main.route("/employees", methods=["POST"])
def create_employee():
    """POST /employees — add a new employee, return refreshed table fragment."""
    from data.mock import employees as employees_data

    name = request.form.get("name", "").strip()
    department = request.form.get("department", "").strip()

    existing = [e for e in employees_data if e["name"].lower() == name.lower()]
    if existing:
        flash("Employee already exists.", "warning")
        return render_template("partials/employees_table.html",
                               employees=employees_data), 200, {
            "HX-Trigger": "refresh-messages"
        }

    new_id = max((e["id"] for e in employees_data), default=0) + 1
    employees_data.append({"id": new_id, "name": name, "department": department})
    flash("Employee added.", "success")
    return render_template("partials/employees_table.html",
                           employees=employees_data), 200, {
        "HX-Trigger": "employee-added, refresh-messages"
    }


@main.route("/employees/<int:id>", methods=["PUT"])
def update_employee(id):
    """PUT /employees/<id> — save inline edit, return updated row fragment."""
    from data.mock import employees as employees_data

    for employee in employees_data:
        if employee["id"] == id:
            employee["name"] = request.form.get("name", employee["name"]).strip()
            employee["department"] = request.form.get("department",
                                                       employee["department"]).strip()
            return render_template("partials/employee_row.html", employee=employee)

    return "Not found", 404


@main.route("/employees/<int:id>", methods=["DELETE"])
def delete_employee(id):
    """DELETE /employees/<id> — remove employee, return empty (row removes itself)."""
    from data.mock import employees as employees_data

    employees_data[:] = [e for e in employees_data if e["id"] != id]
    return ""


@main.route("/employees/<int:id>/edit", methods=["GET"])
def edit_employee_form(id):
    """GET /employees/<id>/edit — return inline edit form fragment."""
    from data.mock import employees as employees_data

    employee = next((e for e in employees_data if e["id"] == id), None)
    if employee is None:
        return "Not found", 404
    return render_template("partials/employee_edit_row.html", employee=employee)


@main.route("/employees/<int:id>/row", methods=["GET"])
def employee_row(id):
    """GET /employees/<id>/row — return read-only row fragment (cancel edit)."""
    from data.mock import employees as employees_data

    employee = next((e for e in employees_data if e["id"] == id), None)
    if employee is None:
        return "Not found", 404
    return render_template("partials/employee_row.html", employee=employee)
```

**Imports inside functions** are shown here to be explicit about the data source. In practice, keep imports at the top of the file.

---

### 1.5 Update hx- attributes in templates to match new URLs

After renaming routes, update any `hx-*` attributes that reference the old route names.

In `templates/partials/employees_table.html`:

```html
<!-- Old -->
hx-delete="/delete-employee/{{ employee.id }}"
hx-get="/edit-employee/{{ employee.id }}"
hx-get="/employee-row/{{ employee.id }}"

<!-- New (clean resource URLs) -->
hx-delete="/employees/{{ employee.id }}"
hx-get="/employees/{{ employee.id }}/edit"
hx-get="/employees/{{ employee.id }}/row"
```

In `templates/index.html` form:

```html
<!-- Old -->
hx-post="/add-employee"

<!-- New -->
hx-post="/employees"
```

---

### 1.6 Scaling to multiple blueprints

For apps with multiple resources, create one Blueprint per resource:

```
routes/
├── employees.py     ← Blueprint("employees", __name__, url_prefix="/employees")
├── departments.py   ← Blueprint("departments", __name__, url_prefix="/departments")
└── auth.py          ← Blueprint("auth", __name__, url_prefix="/auth")
```

Register all in `app.py`:

```python
from routes.employees import employees_bp
from routes.departments import departments_bp
from routes.auth import auth_bp

app.register_blueprint(employees_bp)
app.register_blueprint(departments_bp)
app.register_blueprint(auth_bp)
```

With `url_prefix="/employees"`, the route decorator becomes:

```python
# In routes/employees.py
@employees_bp.route("/", methods=["GET"])     # resolves to GET /employees
@employees_bp.route("/", methods=["POST"])    # resolves to POST /employees
@employees_bp.route("/<int:id>", methods=["DELETE"])  # resolves to DELETE /employees/<id>
```

---

### 1.7 Template folder structure at scale

```
templates/
├── base.html                    ← shared layout (Lesson 42)
├── index.html                   ← home page (extends base.html)
├── employees/
│   ├── list.html                ← full employee list page (extends base.html)
│   └── partials/
│       ├── table.html           ← table fragment
│       ├── row.html             ← single row (read-only)
│       ├── edit_row.html        ← single row (edit form)
│       └── count.html           ← count badge (OOB target)
├── auth/
│   ├── login.html               ← login page (extends base.html)
│   └── partials/
│       └── login_errors.html    ← validation error fragment
└── shared/
    └── flash_messages.html      ← reusable flash fragment
```

Rules:
- Page templates live directly in their feature folder and always extend `base.html`.
- Partial templates live in a `partials/` subfolder and never extend `base.html`.
- Shared fragments (flash messages, spinners) live in `templates/shared/`.

---

### Summary

| Before | After |
|---|---|
| `/add-employee` POST | `/employees` POST |
| `/delete-employee/<id>` DELETE | `/employees/<id>` DELETE |
| `/edit-employee/<id>` GET | `/employees/<id>/edit` GET |
| `/employee-row/<id>` GET | `/employees/<id>/row` GET |
| `templates/partials/` (flat) | `templates/employees/partials/` (nested by resource) |
