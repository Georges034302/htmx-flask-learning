# Lesson 12: Automatically refresh the employee table after form submission

## Concept
Automatically refresh the employee table after form submission.


## 1. Automatically refresh the employee table after form submission

- After form submit, employee is added and table refreshes automatically
- Keep UI synchronized without page refresh or custom JavaScript

### 1.1 Add an ID to the form

Update form tag:

```html
<form
    id="employee-form"
    hx-post="/add-employee"
    hx-target="#form-result">
```

### 1.2 Replace employee table section

Use this full section:

```html
<hr>

<h2>Employee Table</h2>

<div
    hx-get="/employees"
    hx-trigger="load, employee-added from:body"
    hx-target="this">

    Loading employees...

</div>
```

- `employee-added from:body` means listen for custom `employee-added` event from page body.
- This enables event-driven component updates.

### 1.3 Update /add-employee route response

Return with HTMX trigger header:

```python
response = f"""
    <p>
        Added employee:
        <strong>{name}</strong>
        ({department})
    </p>
"""

return response, 200, {
    "HX-Trigger": "employee-added"
}
```

Full route:

```python
@app.route("/add-employee", methods=["POST"])
def add_employee():

    name = request.form.get("name")
    department = request.form.get("department")

    new_employee = {
        "id": len(employees) + 1,
        "name": name,
        "department": department
    }

    employees.append(new_employee)

    response = f"""
        <p>
            Added employee:
            <strong>{name}</strong>
            ({department})
        </p>
    """

    return response, 200, {
        "HX-Trigger": "employee-added"
    }
```

How this works:
- POST `/add-employee` succeeds
- Response header fires `employee-added`
- Table component hears event via `hx-trigger`
- Table auto-refreshes with GET `/employees`

### 1.4 Test it

Refresh page.

Expected:
- Table auto-loads
- Submit new employee
- Employee appears in table immediately

No manual reload, no page refresh, no custom JS handlers.

Observe in DevTools network:
- POST `/add-employee`
- Trigger fires
- GET `/employees`

