# Lesson 04: Add Real-Time Table Filtering with HTMX

## Concept
Add Real-Time Table Filtering with HTMX.


## 1. Add Real-Time Table Filtering with HTMX

### Goal
Wire the search input directly to the employee table so typing filters the table live — no separate search results section.

### 1.1 Updated /employees route (routes/main_routes.py)

Added query-parameter filtering, matching both `name` and `department`:

```python
@main.route("/employees")
def get_employees():
    query = request.args.get("query", "").lower()

    filtered_employees = []
    for employee in employees:
        name_match = query in employee["name"].lower()
        department_match = query in employee["department"].lower()
        if name_match or department_match:
            filtered_employees.append(employee)

    return render_template(
        "partials/employees_table.html",
        employees=filtered_employees
    )
```

### 1.2 Updated search input (templates/index.html)

Changed `hx-get` and `hx-target` to point at the employee table container:

```html
<input
    type="text"
    name="query"
    placeholder="Search employees..."
    hx-get="/employees"
    hx-trigger="keyup changed delay:500ms"
    hx-target="#employee-table-container"
    hx-indicator="#loading"
    hx-swap="innerHTML">
```

Removed the now-redundant `<div id="search-results"></div>`.

### 1.3 Updated employee table container (templates/index.html)

Added `id="employee-table-container"` so the search input can target it:

```html
<div
    id="employee-table-container"
    hx-get="/employees"
    hx-trigger="load, employee-added from:body"
    hx-target="this">
    Loading employees...
</div>
```

### 1.4 Behaviour

- Table auto-loads on page open.
- Typing in the search box sends `/employees?query=...` and replaces the table contents live.
- Adding an employee fires `employee-added` and the table refreshes automatically.
- Single unified component owns display, filtering, and updates.

