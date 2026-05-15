# Lesson 06: Add Pagination to the Employee Table

## Concept
Add Pagination to the Employee Table.


## 1. Add Pagination to the Employee Table

### Goal
Limit table rows per page and allow navigation between pages, preserving search and sort state.

### 1.1 Expanded mock data (data/mock.py)

Added 7 more employees (ids 6–12) so pagination is meaningful:

```python
{"id": 6, "name": "Frank", "department": "Security"},
{"id": 7, "name": "Grace", "department": "IT"},
{"id": 8, "name": "Helen", "department": "Finance"},
{"id": 9, "name": "Ian", "department": "HR"},
{"id": 10, "name": "Jack", "department": "Marketing"},
{"id": 11, "name": "Karen", "department": "IT"},
{"id": 12, "name": "Leo", "department": "Security"}
```

### 1.2 Updated /employees route (routes/main_routes.py)

Added `page` parameter, slicing logic, and `total_pages` calculation:

```python
page = int(request.args.get("page", 1))
per_page = 5

start = (page - 1) * per_page
end = start + per_page
paginated_employees = filtered_employees[start:end]
total_pages = (len(filtered_employees) + per_page - 1) // per_page
```

`(len + per_page - 1) // per_page` is integer ceiling division — ensures a partial last page is counted.

Template call updated to pass `page` and `total_pages`:

```python
return render_template(
    "partials/employees_table.html",
    employees=paginated_employees,
    sort=sort,
    query=query,
    page=page,
    total_pages=total_pages
)
```

### 1.3 Added pagination controls (templates/partials/employees_table.html)

Navigation buttons appear below the table and preserve current query and sort:

```html
<div class="pagination">

    {% if page > 1 %}
    <button
        class="btn btn-ghost btn-sm"
        hx-get="/employees?query={{ query }}&sort={{ sort }}&page={{ page - 1 }}"
        hx-target="#employee-table-container">
        &laquo; Previous
    </button>
    {% endif %}

    <span class="page-info">Page {{ page }} of {{ total_pages }}</span>

    {% if page < total_pages %}
    <button
        class="btn btn-ghost btn-sm"
        hx-get="/employees?query={{ query }}&sort={{ sort }}&page={{ page + 1 }}"
        hx-target="#employee-table-container">
        Next &raquo;
    </button>
    {% endif %}

</div>
```

### 1.4 Test cases

- Default load → 5 rows, page 1 of 3, Next button visible.
- Click **Next** → page 2, Previous and Next both visible.
- Search `IT` → 4 results across pages, navigation adjusts.
- Sort by **Name** then page → sort preserved across pages.

DevTools shows requests like `/employees?query=it&sort=name&page=2`.

**Note:** The server slices, sorts, and filters before rendering. The frontend receives only the current page as ready HTML — no full dataset shipped to the browser.

