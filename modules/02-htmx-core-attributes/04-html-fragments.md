# Lesson 06: Return dynamic HTML fragments instead of plain text

## Concept
Return dynamic HTML fragments instead of plain text.

## 1. Return dynamic HTML fragments instead of plain text

Current route returns:
- `<p>You typed: hello</p>`

Next step is returning rendered fragments such as:
- Cards
- Table rows
- Lists
- Components
- Partial templates

### 1.1 Add mock data

Inside `app.py`, ADD this ABOVE your routes (after `app = Flask(__name__)`):

```python
# Mock data
employees = [
    {"id": 1, "name": "Alice", "department": "IT"},
    {"id": 2, "name": "Bob", "department": "HR"},
    {"id": 3, "name": "Charlie", "department": "Finance"},
    {"id": 4, "name": "David", "department": "IT"},
    {"id": 5, "name": "Emma", "department": "Marketing"}
]
```

- We now simulate database records, API results, and business data
- without using a real database yet

### 1.2 Create partial template

Create file: `templates/partials/search_results.html`

Add:

```html
<ul>
{% for employee in employees %}
    <li>
        {{ employee.name }} - {{ employee.department }}
    </li>
{% endfor %}
</ul>
```

- This is a **partial template**
- It is not a full page, only the piece HTMX will swap.

### 1.3 Update /search route

Replace your current `/search` route WITH:

```python
@app.route("/search")
def search():
    query = request.args.get("query", "").lower()

    filtered_employees = []
    for employee in employees:
        if query in employee["name"].lower():
            filtered_employees.append(employee)

    return render_template(
        "partials/search_results.html",
        employees=filtered_employees
    )
```

- **Read user input**: `query = request.args.get("query", "").lower()`
- **Filter employees**: If user types "a", matches Alice, Charlie, David, Emma
- **Return partial template**: `render_template(...)` returns only the fragment to swap

### 1.4 Test it

Refresh and type "a".

Expected dynamic results:
- Alice
- Charlie
- David
- Emma

Type: **bo**

Expected:
- Bob

**Note:**
- SPA pattern: server returns data and client renders UI.
- HTMX pattern: server returns ready HTML fragments.

Observe the Network tab again:
- You should now see requests sent while typing
- HTML fragments returned
- DOM updated dynamically

