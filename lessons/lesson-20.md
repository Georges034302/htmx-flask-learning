# Lesson 20: Add Real Search Filtering by Multiple Fields

Included step: 30

## Concept
Add Real Search Filtering by Multiple Fields.

## Step flow

## 30) Add Real Search Filtering by Multiple Fields

### Goal
Extend the `/search` route to filter by both `name` and `department`, not just name.

### 30.1 Updated filtering logic in routes/main_routes.py

```python
filtered_employees = []
for employee in employees:
    name_match = query in employee["name"].lower()
    department_match = query in employee["department"].lower()
    if name_match or department_match:
        filtered_employees.append(employee)
```

### 30.2 Test cases

| Query    | Expected results  |
|----------|-------------------|
| `IT`     | Alice, David      |
| `Finance`| Charlie           |
| `Emma`   | Emma              |
| `HR`     | Bob               |

