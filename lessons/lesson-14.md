# Lesson 14: Remove rows instantly with hx-swap="outerHTML"

Included step: 24

## Concept
Remove rows instantly with hx-swap="outerHTML".

## Step flow

## 24) Remove rows instantly with hx-swap="outerHTML"

Now deletion becomes fine-grained and does not require full table refresh.

- Delete only the affected row
- Keep the rest of the table intact
- Avoid secondary table reload request

### 24.1 Update delete button in table partial

In `templates/partials/employees_table.html`, add:
- `hx-target="closest tr"`
- `hx-swap="outerHTML"`

Full button:

```html
<button
    hx-delete="/delete-employee/{{ employee.id }}"
    hx-confirm="Are you sure?"
    hx-trigger="click"
    hx-target="closest tr"
    hx-swap="outerHTML">

    Delete

</button>
```

Concepts:
- `hx-target="closest tr"`: target nearest table row
- `hx-swap="outerHTML"`: replace/remove the entire row element itself

### 24.2 Update delete route

Replace:

```python
return "", 200, {
    "HX-Trigger": "employee-added"
}
```

With:

```python
return ""
```

Full route:

```python
@app.route("/delete-employee/<int:id>", methods=["DELETE"])
def delete_employee(id):

    global employees

    employees = [
        employee
        for employee in employees
        if employee["id"] != id
    ]

    return ""
```

Why it works:
- HTMX targets the row itself
- Server returns empty content
- Row outerHTML is replaced with empty response
- Row disappears immediately

### 24.3 Test it

Refresh browser and delete one employee.

Expected:
- Only selected row disappears
- Table remains visible
- No full-table reload

Observe in DevTools:
- One DELETE request only
- No follow-up GET `/employees` request for delete

