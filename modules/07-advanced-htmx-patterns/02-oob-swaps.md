# Lesson 02: Out-of-Band Swaps (hx-swap-oob)

## Concept
Out-of-Band Swaps (hx-swap-oob).

## 1. Out-of-Band Swaps (hx-swap-oob)

### Goal
Use `hx-swap-oob` to update multiple regions of the page from a single server response — without needing a second HTMX request or a custom event trigger.

---

### 1.1 What OOB swaps are and why they matter

Normally, one HTMX request → one swap target.

```
POST /add-employee
    └── hx-target="#employees-container"  → updates the table
    (but the employee count badge is now stale)
```

The current workaround is `HX-Trigger` + a second request:
1. Server fires `HX-Trigger: employee-added`.
2. Another element listens and sends GET `/employees`.
3. Table refreshes, but count still needs a separate route.

**Out-of-band swaps** solve this in one response:

```
POST /add-employee
    └── Primary response → updates #employees-container (main target)
    └── OOB element in same response → updates #employee-count (secondary target)
```

One request, two DOM updates, no second round-trip.

---

### 1.2 How hx-swap-oob works

Any element in the server response that has `hx-swap-oob="true"` is pulled out of the response and used to replace the element with the matching `id` in the current DOM.

Response body example:

```html
<!-- Primary content: replaces hx-target -->
<table>...</table>

<!-- OOB element: replaces #employee-count in the DOM, regardless of hx-target -->
<span id="employee-count" hx-swap-oob="true">6 employees</span>
```

Rules:
- The OOB element **must have an `id`** that matches an existing DOM element.
- The OOB element is **removed from the primary swap** — it is not inserted at the target.
- Multiple OOB elements can exist in the same response.

---

### 1.3 Create a counter partial template

Create file: `templates/partials/employee_count.html`

```html
<span id="employee-count" hx-swap-oob="true">
    {{ count }} employee{% if count != 1 %}s{% endif %}
</span>
```

- `hx-swap-oob="true"` tells HTMX this element should replace the DOM node with `id="employee-count"`.
- The count text uses the same singular/plural pattern from Module 05, Lesson 03.

---

### 1.4 Update the /add-employee route

Open `routes/main_routes.py`.

Locate the `/add-employee` POST route. Update it to return both the refreshed table and the OOB counter update in a single response:

```python
@main.route("/add-employee", methods=["POST"])
def add_employee():
    name = request.form.get("name", "").strip()
    department = request.form.get("department", "").strip()

    # Duplicate check
    existing = [e for e in employees_data if e["name"].lower() == name.lower()]

    if existing:
        flash("Employee already exists.", "warning")
        return render_template("partials/employees_table.html",
                               employees=employees_data), 200, {"HX-Trigger": "refresh-messages"}

    new_id = max((e["id"] for e in employees_data), default=0) + 1
    employees_data.append({"id": new_id, "name": name, "department": department})

    # Build primary response (refreshed table)
    table_html = render_template("partials/employees_table.html",
                                 employees=employees_data)

    # Build OOB counter update
    count_html = render_template("partials/employee_count.html",
                                 count=len(employees_data))

    # Concatenate: HTMX processes primary + OOB in one response
    flash("Employee added.", "success")
    return table_html + count_html, 200, {
        "HX-Trigger": "employee-added, refresh-messages"
    }
```

Key points:
- `table_html + count_html` — string concatenation is all that is needed.
- HTMX parses the combined response, extracts the OOB element, and swaps both targets.
- `employees_data` is the in-memory list. If using SQLAlchemy (Module 08, Lesson 01), replace list operations with `db.session.add()` and `Employee.query.all()`.

---

### 1.5 Add the counter element to index.html

In `templates/index.html`, add the counter `<span>` somewhere visible — for example, above the table container:

```html
{% block content %}

<div id="search-container">
    <input
        type="text"
        name="query"
        placeholder="Search employees..."
        hx-get="/employees"
        hx-trigger="keyup changed delay:500ms"
        hx-target="#employees-container"
        hx-swap="innerHTML">
</div>

<!-- Employee count badge — updated via OOB swap after add/delete -->
<p>
    Total: <span id="employee-count">{{ employees|length if employees else 0 }} employees</span>
</p>

<div id="form-container">
    <form
        hx-post="/add-employee"
        hx-target="#employees-container"
        hx-swap="innerHTML"
        hx-trigger="submit">
        <input type="text" name="name" placeholder="Name" required>
        <input type="text" name="department" placeholder="Department" required>
        <button type="submit">Add Employee</button>
    </form>
</div>

<div
    id="employees-container"
    hx-get="/employees"
    hx-trigger="load"
    hx-swap="innerHTML">
</div>

{% endblock %}
```

The `<span id="employee-count">` is the DOM node that OOB will target.

---

### 1.6 Optional: OOB on delete

Apply the same pattern to the delete route so the counter decrements when an employee is removed.

In the `/delete-employee/<id>` route, after removing the employee:

```python
@main.route("/delete-employee/<int:id>", methods=["DELETE"])
def delete_employee(id):
    global employees_data
    employees_data = [e for e in employees_data if e["id"] != id]

    # OOB counter update returned alongside the empty primary response
    count_html = render_template("partials/employee_count.html",
                                 count=len(employees_data))

    # Empty primary response removes the row (via hx-swap="outerHTML" on the button)
    return count_html
```

Because the delete button uses `hx-swap="outerHTML"` on `closest tr`, the primary swap is the row removal. The OOB element in the response still updates `#employee-count` independently.

---

### 1.7 Test the result

1. Restart Flask: `python app.py`.
2. Open `http://127.0.0.1:5000/`.
3. Add a new employee via the form.

Expected:
- The table refreshes with the new employee (primary swap).
- The "Total: N employees" counter increments (OOB swap).
- Only **one** network request in DevTools — no secondary GET triggered.

4. Delete an employee.

Expected:
- The row disappears immediately (outerHTML swap).
- The counter decrements (OOB swap).

---

### Summary

| Mechanism | Round trips | When to use |
|---|---|---|
| `HX-Trigger` + listener | 2 (trigger + follow-up GET) | When the secondary update is complex or needs its own route |
| `hx-swap-oob` | 1 (combined response) | When the secondary update is a small, known fragment |
