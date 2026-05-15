# Lesson 15: Edit employees inline with hx-put

## Concept
Edit employees inline with hx-put.


## 1. Edit employees inline with hx-put

Now you complete full CRUD by adding inline Update behavior.

- Click Edit
- Load inline edit form inside the row
- Save asynchronously with PUT
- Replace row dynamically

### 1.1 Add Edit button in row actions

In `templates/partials/employees_table.html` rows, add Edit above Delete:

```html
<button
    hx-get="/edit-employee/{{ employee.id }}"
    hx-target="closest tr"
    hx-swap="outerHTML">

    Edit

</button>
```

- Sends GET request
- Flask returns editable row HTML
- Current row is replaced

### 1.2 Create editable row partial

Create `templates/partials/edit_employee_row.html`:

```html
<tr>

<form
    hx-put="/update-employee/{{ employee.id }}"
    hx-target="closest tr"
    hx-swap="outerHTML">

    <td>{{ employee.id }}</td>

    <td>
        <input
            type="text"
            name="name"
            value="{{ employee.name }}">
    </td>

    <td>
        <input
            type="text"
            name="department"
            value="{{ employee.department }}">
    </td>

    <td>
        <button type="submit">
            Save
        </button>
    </td>

</form>

</tr>
```

### 1.3 Create normal display row partial

Create `templates/partials/employee_row.html`:

```html
<tr>

    <td>{{ employee.id }}</td>
    <td>{{ employee.name }}</td>
    <td>{{ employee.department }}</td>

    <td>

        <button
            hx-get="/edit-employee/{{ employee.id }}"
            hx-target="closest tr"
            hx-swap="outerHTML">

            Edit

        </button>

        <button
            hx-delete="/delete-employee/{{ employee.id }}"
            hx-confirm="Are you sure?"
            hx-trigger="click"
            hx-target="closest tr"
            hx-swap="outerHTML">

            Delete

        </button>

    </td>

</tr>
```

### 1.4 Refactor table body to reusable include

In `templates/partials/employees_table.html`, loop becomes:

```html
<tbody>

{% for employee in employees %}

    {% include "partials/employee_row.html" %}

{% endfor %}

</tbody>
```

This introduces reusable server-rendered UI components.

### 1.5 Add edit route

In `app.py`:

```python
@app.route("/edit-employee/<int:id>")
def edit_employee(id):

    employee = next(
        (
            employee
            for employee in employees
            if employee["id"] == id
        ),
        None
    )

    return render_template(
        "partials/edit_employee_row.html",
        employee=employee
    )
```

### 1.6 Add update route with PUT

In `app.py`:

```python
@app.route("/update-employee/<int:id>", methods=["PUT"])
def update_employee(id):

    employee = next(
        (
            employee
            for employee in employees
            if employee["id"] == id
        ),
        None
    )

    employee["name"] = request.form.get("name")
    employee["department"] = request.form.get("department")

    return render_template(
        "partials/employee_row.html",
        employee=employee
    )
```

- `hx-put` sends HTTP PUT for update operations.

### 1.7 Test it

Refresh page, then:
- Click Edit on a row
- Row transforms into inline form
- Modify values
- Click Save
- Row updates dynamically

No page refresh and no frontend framework needed.

