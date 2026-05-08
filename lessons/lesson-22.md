# Lesson 22: Add Dynamic Search Result Count

Included step: 32

Learning objective:
Master one focused concept from step 32 with precise, sequential execution.

Editor notes:
- Keep the exact sequence from source material.
- Validate behavior at each test checkpoint before continuing.

## Detailed walkthrough

## 32) Add Dynamic Search Result Count

### Goal
Display the number of matching employees alongside search results so users always know how many records were found.

### 32.1 Updated templates/partials/search_results.html

```html
{% if employees %}

<p>
    <strong>{{ employees|length }}</strong>
    employee{% if employees|length != 1 %}s{% endif %} found.
</p>

<ul>
{% for employee in employees %}
    <li>
        {{ employee.name }} - {{ employee.department }}
    </li>
{% endfor %}
</ul>

{% else %}

<p>No employees found.</p>

{% endif %}
```

Key Jinja concepts used:
- `employees|length` — Jinja filter equivalent to `len(employees)`, calculates list size.
- `{% if employees|length != 1 %}s{% endif %}` — handles singular/plural grammar ("1 employee found" vs "2 employees found").

### 32.2 Test cases

| Query  | Expected result          |
|--------|--------------------------|
| `IT`   | **2** employees found.   |
| `Emma` | **1** employee found.    |
| `zzzz` | No employees found.      |

### Architectural note
The backend now controls filtering, rendering, count calculation, and UX messaging in one place. The frontend receives ready-to-display HTML — no JavaScript counter logic required.

### What you learned
- Jinja filters (`|length`)
- Singular/plural conditional rendering
- Dynamic result counts
- Continuous UI feedback
- Centralized server-driven UX states

---

