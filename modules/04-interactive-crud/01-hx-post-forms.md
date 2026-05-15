# Lesson 11: Create your first HTMX form submission with hx-post

## Concept
Create your first HTMX form submission with hx-post.


## 1. Create your first HTMX form submission with hx-post

So far you have fetched data, loaded fragments, and updated content dynamically.

Now you will send data to the server.

- Create a form
- Submit data with HTMX
- Flask receives form data
- Flask returns HTML response
- HTMX updates page dynamically

### 1.1 Add new route to app.py

Add:

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

    return f"""
        <p>
            Added employee:
            <strong>{name}</strong>
            ({department})
        </p>
    """
```

- `methods=["POST"]` allows POST requests.
- `request.form.get(...)` reads submitted form data.
- This is different from `request.args` (query parameters).

### 1.2 Add form to index.html

Add below employee table section:

```html
<hr>

<h2>Add Employee</h2>

<form
    hx-post="/add-employee"
    hx-target="#form-result">

    <input
        type="text"
        name="name"
        placeholder="Employee Name"
        required>

    <input
        type="text"
        name="department"
        placeholder="Department"
        required>

    <button type="submit">
        Add Employee
    </button>

</form>

<div id="form-result"></div>
```

What HTMX does automatically:
- Serializes form fields
- Sends async POST request
- Handles server response
- Updates target element

### 1.3 Test it

Refresh browser and submit:
- Name: Sarah
- Department: Security

Expected:
- Added employee: Sarah (Security)
- Appears dynamically without page refresh

Observe Network tab:
- POST request
- Form payload
- HTML response

