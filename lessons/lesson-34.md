# Lesson 34: Form Validation System

Included step: 44

## Concept
Form Validation System.


## 44) Form Validation System

> **Not yet implemented** — instructions below describe the full server-side validation pattern to add once the DB step is ready (or directly on top of mock data).

### Goal
Add field-level validation to the Add Employee form: required fields, minimum length, allowed department values, and inline error feedback — all server-side, rendered as HTMX partials.

---

### 44.1 Create validation helper (utils/validators.py)

Create folder and file `utils/validators.py`:

```python
VALID_DEPARTMENTS = {"IT", "HR", "Finance", "Marketing", "Security"}

def validate_employee(name, department):
    errors = []

    if not name or len(name.strip()) < 2:
        errors.append("Name must be at least 2 characters.")

    if not department or department.strip() not in VALID_DEPARTMENTS:
        errors.append(
            f"Department must be one of: {', '.join(sorted(VALID_DEPARTMENTS))}."
        )

    return errors
```

Returns a list of error strings. Empty list means valid.

---

### 44.2 Create validation error partial (templates/partials/form_errors.html)

```html
{% if errors %}
<div class="form-errors">
    <ul>
    {% for error in errors %}
        <li>{{ error }}</li>
    {% endfor %}
    </ul>
</div>
{% endif %}
```

This partial is injected into `#form-result` when validation fails.

---

### 44.3 Update add_employee route (routes/main_routes.py)

Import validator:

```python
from utils.validators import validate_employee
```

Add validation before duplicate check:

```python
@main.route("/add-employee", methods=["POST"])
def add_employee():
    name = request.form.get("name", "").strip()
    department = request.form.get("department", "").strip()

    errors = validate_employee(name, department)
    if errors:
        return render_template("partials/form_errors.html", errors=errors), 200

    # existing duplicate check follows...
```

If validation fails:
- Returns rendered error partial into `#form-result`.
- No employee is added.
- No flash message fires.
- Table is unaffected.

---

### 44.4 Add error styles (static/style.css)

```css
.form-errors {
    background-color: #f8d7da;
    color: #721c24;
    padding: 12px;
    margin-bottom: 15px;
    border-radius: 5px;
}

.form-errors ul {
    margin: 0;
    padding-left: 18px;
}
```

---

### 44.5 Full validation + duplicate check flow

```
POST /add-employee
  → validate fields
      INVALID → render form_errors.html into #form-result, stop
  → check duplicate
      DUPLICATE → flash warning, fire refresh-messages, stop
  → add employee
      SUCCESS → flash success, fire employee-added + refresh-messages
```

---

### 44.6 Test cases

| Input                         | Expected result                              |
|-------------------------------|----------------------------------------------|
| Name: `A`, Dept: `IT`         | Error: name too short                        |
| Name: `Alice`, Dept: `Foo`    | Error: invalid department                    |
| Name: ``, Dept: ``            | Both errors rendered                         |
| Name: `Alice`, Dept: `IT`     | Duplicate warning (Alice already exists)     |
| Name: `Zara`, Dept: `Finance` | Success — employee added                     |

---

