# Lesson 07: Add Modal Windows for Employee Details

## Concept
Add Modal Windows for Employee Details.


## 1. Add Modal Windows for Employee Details

### Goal
Open employee details inside a server-rendered modal overlay using HTMX partial swaps.

### 1.1 Added modal routes (routes/main_routes.py)

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

### 1.2 Added modal partial (templates/partials/employee_details_modal.html)

Created using `.lightbox`, `.lightbox-card`, `.lightbox-head`, `.lightbox-body`, and `.lightbox-actions` from `main.css`:

```html
<div class="lightbox open">
    <div class="lightbox-card">

        <div class="lightbox-head">
            <h3>Employee Details</h3>
            <button
                class="lightbox-close"
                hx-get="/close-modal"
                hx-target="#modal"
                hx-swap="innerHTML">
                &times;
            </button>
        </div>

        <div class="lightbox-body">
            <dl>
                <dt>ID</dt>
                <dd>{{ employee.id }}</dd>
                <dt>Name</dt>
                <dd>{{ employee.name }}</dd>
                <dt>Department</dt>
                <dd><span class="pill">{{ employee.department }}</span></dd>
            </dl>
        </div>

        <div class="lightbox-actions">
            <button
                class="btn btn-ghost"
                hx-get="/close-modal"
                hx-target="#modal"
                hx-swap="innerHTML">
                Close
            </button>
        </div>

    </div>
</div>
```

- `.lightbox.open` makes the overlay visible (`opacity: 1; pointer-events: auto`).
- `.lightbox-card` is the centered content card with `border-radius` and `box-shadow`.
- `.lightbox-close` is the × button in the top-right corner.
- The `dl`/`dt`/`dd` grid in `.lightbox-body` gives a clean two-column label/value layout.
- Styles come entirely from `static/css/main.css` — no custom CSS is needed.

### 1.3 Added View action in table rows (templates/partials/employee_row.html)

Added button:

```html
<button
    class="btn btn-ghost btn-sm"
    hx-get="/employee-details/{{ employee.id }}"
    hx-target="#modal"
    hx-swap="innerHTML">
    View
</button>
```

This opens the modal without page refresh.

### 1.4 Added modal mount point (templates/index.html)

Added container:

```html
<div id="modal"></div>
```

All modal content is dynamically injected into this region.

### 1.5 CSS — static/css/main.css

`main.css` provides the complete modal system. No custom CSS is needed.

Classes used:

| Class | Purpose |
|---|---|
| `.lightbox` | Fixed overlay with blur backdrop (`opacity: 0` by default) |
| `.lightbox.open` | Makes the overlay visible and interactive |
| `.lightbox-card` | Centered white card with rounded corners and shadow |
| `.lightbox-head` | Title row with close button |
| `.lightbox-body` | Content area with `dl`/`dt`/`dd` grid |
| `.lightbox-close` | \u00d7 button (top right) |
| `.lightbox-actions` | Footer row for action buttons |

The `/close-modal` route returns an empty string, clearing `#modal` and collapsing the overlay.

### 1.6 Test

1. Load employee table.
2. Click **View** on any row.
3. Modal appears with employee details.
4. Click **Close**.
5. Modal disappears without refreshing the page.

