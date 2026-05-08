# Lesson 06: Return dynamic HTML fragments instead of plain text

Included step: 16

Learning objective:
Master one focused concept from step 16 with precise, sequential execution.

Editor notes:
- Keep the exact sequence from source material.
- Validate behavior at each test checkpoint before continuing.

## Detailed walkthrough

## 16) Return dynamic HTML fragments instead of plain text

Now we move into one of the MOST important HTMX concepts: **Server-rendered HTML fragments**

Right now your Flask route returns:
- `<p>You typed: hello</p>`

But real HTMX applications usually return:
- Cards
- Table rows
- Lists
- Components
- Partial templates

This is where HTMX starts becoming a real application architecture.

Goal:
- Instead of returning plain text
- Return dynamically generated HTML based on mock data
- Rendered by Flask
- You are about to build your FIRST real HTMX component

### 16.1 Add mock data

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

Why:
- We now simulate database records, API results, and business data
- WITHOUT using a real database yet
- Perfect for Phase 1 learning

### 16.2 Create partial template

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

Important concept:
- This is a **partial template**
- NOT a full HTML page
- Designed specifically for HTMX injection
- This becomes a core architectural pattern

### 16.3 Update /search route

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

What this does:
- **Read user input**: `query = request.args.get("query", "").lower()`
- **Filter employees**: If user types "a", matches Alice, Charlie, David, Emma
- **Return partial template**: `render_template(...)` returns ONLY the HTML fragment, NOT an entire page
- This is REAL HTMX architecture

### 16.4 Test it

Refresh your browser.

Now type: **a**

Expected dynamic results:
- Alice
- Charlie
- David
- Emma

Type: **bo**

Expected:
- Bob

Important breakthrough:
- You are now building server-rendered components
- Dynamic filtering
- Partial template rendering
- Live reactive UI
- Without React, Vue, Angular, or JSON APIs
- This is the heart of HTMX

VERY IMPORTANT CONCEPT:

**Traditional SPA:**
- Server returns DATA
- Frontend renders UI

**HTMX:**
- Server returns READY HTML
- The server owns rendering
- Massive architectural simplification

Observe the Network tab again:
- You should now see requests sent while typing
- HTML fragments returned
- DOM updated dynamically
- Professional reactive behavior
- Minimal complexity

