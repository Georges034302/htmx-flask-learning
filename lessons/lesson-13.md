# Lesson 13: Delete employees dynamically with hx-delete

Included step: 23

## Concept
Delete employees dynamically with hx-delete.


## 23) Delete employees dynamically with hx-delete

Now you add the Delete part of CRUD.

- Add a Delete button per employee
- Send DELETE request to Flask
- Remove employee from backend list
- Refresh table automatically

### 23.1 Update employee table partial

Open `templates/partials/employees_table.html`.

Add Actions header:

```html
<th>Actions</th>
```

Add this action cell in each employee row:

```html
<td>

    <button
        hx-delete="/delete-employee/{{ employee.id }}"
        hx-confirm="Are you sure?"
        hx-trigger="click">

        Delete

    </button>

</td>
```

- `hx-delete`: sends HTTP DELETE request
- `hx-confirm`: shows confirmation dialog before request

### 23.2 Add delete route to app.py

Add:

```python
@app.route("/delete-employee/<int:id>", methods=["DELETE"])
def delete_employee(id):

    global employees

    employees = [
        employee
        for employee in employees
        if employee["id"] != id
    ]

    return "", 200, {
        "HX-Trigger": "employee-added"
    }
```

Why reuse `HX-Trigger: employee-added`:
- Table already listens for this event
- Add and delete operations can refresh the same component with one event name

Python note:
- List comprehension rebuilds `employees` while excluding the deleted ID

### 23.3 Test it

Refresh browser.

Then:
- Load table
- Click Delete
- Confirm dialog appears
- Employee is removed
- Table refreshes automatically

No page refresh and no custom JavaScript required.

Observe in DevTools network:
- DELETE request
- Trigger event
- GET `/employees` to refresh table

