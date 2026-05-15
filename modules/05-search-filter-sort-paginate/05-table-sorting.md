# Lesson 24: Add Sorting to the Employee Table

## Concept
Add Sorting to the Employee Table.


## 1. Add Sorting to the Employee Table

### Goal
Make column headers clickable so the table reorders dynamically — server-side, no JavaScript.

### 1.1 Updated /employees route (routes/main_routes.py)

Added `sort` parameter, sorting logic, and passed both `sort` and `query` to the template:

```python
@main.route("/employees")
def get_employees():
    query = request.args.get("query", "").lower()
    sort = request.args.get("sort", "id")

    filtered_employees = []
    for employee in employees:
        name_match = query in employee["name"].lower()
        department_match = query in employee["department"].lower()
        if name_match or department_match:
            filtered_employees.append(employee)

    filtered_employees.sort(key=lambda employee: employee[sort])

    return render_template(
        "partials/employees_table.html",
        employees=filtered_employees,
        sort=sort,
        query=query
    )
```

`filtered_employees.sort(key=lambda employee: employee[sort])` dynamically sorts by `id`, `name`, or `department` based on the query parameter.

Passing `sort` and `query` back to the template preserves state across interactions.

### 1.2 Updated table headers (templates/partials/employees_table.html)

Each header is now a clickable HTMX link that preserves the current search query:

```html
<th>
    <a hx-get="/employees?query={{ query }}&sort=id"
       hx-target="#employee-table-container">ID</a>
</th>
<th>
    <a hx-get="/employees?query={{ query }}&sort=name"
       hx-target="#employee-table-container">Name</a>
</th>
<th>
    <a hx-get="/employees?query={{ query }}&sort=department"
       hx-target="#employee-table-container">Department</a>
</th>
```

### 1.3 Test cases

- Click **Name** → table sorts alphabetically by name.
- Click **Department** → table sorts by department.
- Click **ID** → table returns to insertion order.
- Type `IT` then click **Name** → filtered results sort by name, query preserved.

DevTools shows requests like `/employees?query=it&sort=name`.

**Note:** The server owns sorting state, filter state, and rendering. The frontend has no sort logic — only declarative HTMX attributes.

