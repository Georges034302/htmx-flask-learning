# Lesson 43: Progressive Enhancement and Detecting HTMX Requests

## Concept
Progressive Enhancement and Detecting HTMX Requests.

## 1. Progressive Enhancement and Detecting HTMX Requests

### Goal
Make Flask routes respond correctly whether the request came from HTMX (expecting an HTML fragment) or from a direct browser navigation (expecting a full HTML page). This is the foundation of progressive enhancement — the same URL works in both contexts.

---

### 1.1 What is the HX-Request header

Every request sent by HTMX includes a custom HTTP header:

```
HX-Request: true
```

Flask can read this header from `request.headers`:

```python
is_htmx = request.headers.get("HX-Request")
# Returns "true" if the request came from HTMX
# Returns None if the browser navigated directly
```

This single check is the entire mechanism behind conditional responses.

---

### 1.2 What progressive enhancement means in this context

Without progressive enhancement:
- Visiting `/employees` directly in a browser returns a bare `<table>` fragment.
- The user sees an unstyled table with no navigation — broken experience.

With progressive enhancement:
- HTMX sends `HX-Request: true` → route returns the fragment only.
- Direct browser visit → route returns the full page (with `base.html` layout, nav, HTMX CDN).

Same URL, same data — different response format based on who is asking.

```
Browser navigates to /employees
    └── HX-Request header missing → return full page (render_template "index.html")

HTMX triggers GET /employees
    └── HX-Request: true → return partial (render_template "partials/employees_table.html")
```

---

### 1.3 Detect HX-Request in routes/main_routes.py

Open `routes/main_routes.py`.

Add this helper at the top of the file, below the imports:

```python
def is_htmx_request():
    """Return True if the current request was made by HTMX."""
    return request.headers.get("HX-Request") == "true"
```

This is a thin helper — no library needed.

---

### 1.4 Apply conditional response to the /employees route

Locate your existing `/employees` GET route in `routes/main_routes.py`.

Replace it with the progressive-enhancement version:

```python
@main.route("/employees")
def employees():
    query_str = request.args.get("query", "").lower()
    sort = request.args.get("sort", "id")
    page = int(request.args.get("page", 1))
    per_page = 5

    filtered = [
        e for e in employees_data
        if query_str in e["name"].lower()
        or query_str in e["department"].lower()
    ]

    sort_key = sort if sort in ("id", "name", "department") else "id"
    sorted_employees = sorted(filtered, key=lambda e: str(e.get(sort_key, "")))

    total_pages = -(-len(sorted_employees) // per_page)  # ceiling division
    start = (page - 1) * per_page
    paginated = sorted_employees[start:start + per_page]

    template_data = dict(
        employees=paginated,
        query=query_str,
        sort=sort,
        page=page,
        total_pages=total_pages
    )

    # Progressive enhancement: return fragment for HTMX, full page for browser
    if is_htmx_request():
        return render_template("partials/employees_table.html", **template_data)

    return render_template("index.html", **template_data)
```

What changed:
- If `HX-Request` is present → returns only the table partial (same as before).
- If browser navigates directly → returns the full `index.html` with layout, which also pre-renders the table via `hx-trigger="load"`.

**Important:** `employees_data` refers to the data source imported at the top of `main_routes.py`. If you are using the mock list, this is `from data.mock import employees as employees_data`. If you completed Lesson 33 and are using SQLAlchemy, apply the same `if is_htmx_request()` check to your database-backed route instead.

---

### 1.5 Apply the same pattern to the /search route (optional)

The same pattern applies to any route that returns a fragment:

```python
@main.route("/search")
def search():
    query_str = request.args.get("query", "").lower()
    filtered = [
        e for e in employees_data
        if query_str in e["name"].lower()
    ]

    if is_htmx_request():
        return render_template("partials/search_results.html", employees=filtered)

    # Fallback: redirect to home with pre-filled search if accessed directly
    return render_template("index.html", employees=filtered, query=query_str)
```

---

### 1.6 Test both modes

**Test HTMX mode (normal):**
1. Open `http://127.0.0.1:5000/`.
2. Type in the search box.
3. Open DevTools → Network tab.
4. Confirm `HX-Request: true` is present in the request headers.
5. Confirm the response body is an HTML fragment (no `<!DOCTYPE html>`).

**Test browser direct navigation mode:**
1. Open `http://127.0.0.1:5000/employees` directly in the browser address bar.
2. Confirm the page renders with the full layout (header, styles, HTMX CDN).
3. Confirm the employee table appears — the page still works.

Expected outcomes:

| Access method | HX-Request header | Response |
|---|---|---|
| HTMX request | `true` | `partials/employees_table.html` fragment |
| Direct browser URL | absent | `index.html` full page |
| `curl http://localhost:5000/employees` | absent | `index.html` full page |

---

### Summary

- `request.headers.get("HX-Request")` is the only detection mechanism needed.
- One route, one data-fetching block, two rendering paths.
- No JavaScript required.
- This pattern ensures your app works with browser bookmarks, back/forward navigation, and screen readers — all of which do not send `HX-Request`.
