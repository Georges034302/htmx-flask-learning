# Lesson 28: Prevent Duplicate Employees + Show Flash Message

Included step: 38

## Concept
Prevent Duplicate Employees + Show Flash Message.

## Step flow

## 38) Prevent Duplicate Employees + Show Flash Message

### Goal
Reject duplicate employee names server-side and show a flash message — table unchanged on duplicate attempt.

### 38.1 Updated add_employee route (routes/main_routes.py)

Added duplicate check immediately after reading form data:

```python
existing_employee = next(
    (
        employee
        for employee in employees
        if employee["name"].lower() == name.lower()
    ),
    None
)

if existing_employee:
    flash(f"Employee '{name}' already exists.")
    return "", 200, {
        "HX-Trigger": "refresh-messages"
    }
```

If a duplicate is found:
- Employee is **not** added.
- Flash message is stored.
- Only `refresh-messages` fires — table stays unchanged.

If no duplicate, normal flow continues: employee added, table and messages both refresh.

### 38.2 Logic flow

```
POST /add-employee
  → duplicate found?
      YES → flash warning, fire refresh-messages only
      NO  → append employee, flash success, fire employee-added + refresh-messages
```

### 38.3 Test cases

| Action               | Expected result                          |
|----------------------|------------------------------------------|
| Add "Alice" again    | Flash: "Employee 'Alice' already exists." — table unchanged |
| Add "alice" (lower)  | Same — case-insensitive match            |
| Add "Zara" (new)     | Flash: "Employee Zara added successfully." — table updates |

**Note:** Validation lives entirely on the server. The frontend receives only HTML feedback — no client-side duplicate checking required.

