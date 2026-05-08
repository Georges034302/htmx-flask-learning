# Lesson 16: Add a Cancel button to inline editing

Included step: 26

Learning objective:
Master one focused concept from step 26 with precise, sequential execution.

Editor notes:
- Keep the exact sequence from source material.
- Validate behavior at each test checkpoint before continuing.

## Detailed walkthrough

## 26) Add a Cancel button to inline editing

Now inline edit mode can be rolled back cleanly.

Goal:
- Click Cancel in edit mode
- Restore normal row view
- No page refresh

### 26.1 Add Cancel button in edit row partial

In `templates/partials/edit_employee_row.html`, add below Save:

```html
<button
    type="button"
    hx-get="/employee-row/{{ employee.id }}"
    hx-target="closest tr"
    hx-swap="outerHTML">

    Cancel

</button>
```

Important concept:
- `type="button"` prevents unintended submit behavior.

What this does:
- Sends GET request for display row
- Replaces editable row with normal row component

### 26.2 Add restore-row route in app.py

Add:

```python
@app.route("/employee-row/<int:id>")
def employee_row(id):

    employee = next(
        (
            employee
            for employee in employees
            if employee["id"] == id
        ),
        None
    )

    return render_template(
        "partials/employee_row.html",
        employee=employee
    )
```

This returns one row fragment only, which is efficient for inline UI rollback.

### 26.3 Test it

Refresh page.

Then:
- Click Edit
- Editable row appears
- Click Cancel
- Original row returns

No page refresh required.

What you learned:
- Reversible component rendering
- UI rollback pattern
- Inline state switching
- Component restoration
- Efficient row-level rendering

---

