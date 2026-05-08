# Lesson 21: Add Empty-State Handling ("No Results Found")

Included step: 31

Learning objective:
Master one focused concept from step 31 with precise, sequential execution.

Editor notes:
- Keep the exact sequence from source material.
- Validate behavior at each test checkpoint before continuing.

## Detailed walkthrough

## 31) Add Empty-State Handling ("No Results Found")

### Goal
When search returns no results, display a clear message instead of leaving the UI blank.

### 31.1 Updated templates/partials/search_results.html

Replaced the bare `{% for %}` loop with a Jinja conditional:

```html
{% if employees %}
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

`{% if employees %}` evaluates to `True` when the list is non-empty, and `False` when it is empty — equivalent to checking `employees.length > 0`.

### 31.2 Test cases

| Query  | Expected result             |
|--------|-----------------------------|
| `zzzz` | No employees found.         |
| `IT`   | Alice, David                |

### Architectural note
The server decides which UI state to render — results list or empty-state message. No frontend JavaScript required. This is the core HTMX philosophy: centralized, server-driven rendering.

### What you learned
- Jinja conditional rendering (`{% if %} / {% else %} / {% endif %}`)
- Empty-state UX pattern
- Server-driven UI states
- Professional application feedback (loading states, empty states, error states)
- HTMX architecture: server owns all rendering decisions

---

