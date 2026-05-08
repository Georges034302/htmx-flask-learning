# Lesson 10: Build your first dynamic table component

Included step: 20

## Concept
Build your first dynamic table component.

## Step flow

## 20) Build your first dynamic table component

Now we move from simple lists to structured UI rendering.

- Reusable table rendering
- Structured HTML fragments
- Server-driven table UI

This pattern is heavily used in:
- Admin portals
- Dashboards
- Inventory systems
- HR systems
- DevOps tools

### 20.1 Create new route

Add in `app.py`:

```python
@app.route("/employees")
def get_employees():

    return render_template(
        "partials/employees_table.html",
        employees=employees
    )
```

- Returns only a table fragment
- Not a full page
- Matches HTMX partial architecture

### 20.2 Create table partial

Create file: `templates/partials/employees_table.html`

```html
<table border="1" cellpadding="10">

    <thead>
        <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Department</th>
        </tr>
    </thead>

    <tbody>
    {% for employee in employees %}
        <tr>
            <td>{{ employee.id }}</td>
            <td>{{ employee.name }}</td>
            <td>{{ employee.department }}</td>
        </tr>
    {% endfor %}
    </tbody>

</table>
```

**Note:** Jinja observation:
- `{{ employee.name }}` uses dot notation on dictionary data
- Bracket notation works too

### 20.3 Add HTMX table loader to index.html

Add below latest updates section:

```html
<hr>

<h2>Employee Table</h2>

<button
    hx-get="/employees"
    hx-target="#employee-table">
    Load Employees
</button>

<div id="employee-table"></div>
```

- Button click sends request to `/employees`
- Flask renders table partial
- HTMX injects table into `#employee-table`

### 20.4 Test it

Refresh browser and click **Load Employees**.

Expected:
- Full HTML table appears dynamically
- No page refresh
- No JavaScript table rendering
- No JSON API response required

**Note:**
- Traditional SPA: JSON -> JS -> build table
- HTMX: Flask -> render HTML table -> inject

