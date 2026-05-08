# Lesson 20: Add Real Search Filtering by Multiple Fields

Included step: 30

Learning objective:
Master one focused concept from step 30 with precise, sequential execution.

Editor notes:
- Keep the exact sequence from source material.
- Validate behavior at each test checkpoint before continuing.

## Detailed walkthrough

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

### What you learned
- Multi-field backend filtering
- OR logic for search matching
- Server-side search architecture vs frontend JS filtering
- HTMX philosophy: backend owns logic and rendering, frontend stays lightweight

---

