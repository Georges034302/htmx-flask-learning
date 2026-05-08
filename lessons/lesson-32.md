# Lesson 32: Add Modal Windows for Employee Details

Included step: 42

## Concept
Add Modal Windows for Employee Details.

## Step flow

## 42) Add Modal Windows for Employee Details

### Goal
Open employee details inside a server-rendered modal overlay using HTMX partial swaps.

### 42.1 Added modal routes (routes/main_routes.py)

New routes:

```python
@main.route("/employee-details/<int:id>")
def employee_details(id):
    ...
    return render_template("partials/employee_details_modal.html", employee=employee)

@main.route("/close-modal")
def close_modal():
    return ""
```

`/employee-details/<id>` renders modal HTML. `/close-modal` clears the modal container.

### 42.2 Added modal partial (templates/partials/employee_details_modal.html)

Created a modal overlay/card partial that shows:
- ID
- Name
- Department

Includes a **Close** button that targets `#modal` and swaps empty HTML via `/close-modal`.

### 42.3 Added View action in table rows (templates/partials/employee_row.html)

Added button:

```html
<button
    hx-get="/employee-details/{{ employee.id }}"
    hx-target="#modal"
    hx-swap="innerHTML">
    View
</button>
```

This opens the modal without page refresh.

### 42.4 Added modal mount point (templates/index.html)

Added container:

```html
<div id="modal"></div>
```

All modal content is dynamically injected into this region.

### 42.5 Added modal styles (static/style.css)

Added:
- `.modal-overlay`
- `.modal-card`
- `.modal-actions`

for centered overlay rendering and clean modal presentation.

### 42.6 Test

1. Load employee table.
2. Click **View** on any row.
3. Modal appears with employee details.
4. Click **Close**.
5. Modal disappears without refreshing the page.

