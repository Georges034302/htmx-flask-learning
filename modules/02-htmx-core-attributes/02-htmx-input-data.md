# Lesson 02: Send input data from HTMX to Flask

## Concept
Understand how input values move from HTMX attributes to Flask request arguments.

## 1. Send input data from HTMX to Flask

Make the server receive the actual text being typed.

### 1.1 Update the input field

Modify your existing input to include `name="query"`:

```html
<input
    type="text"
    name="query"
    placeholder="Type something..."
    hx-get="/search"
    hx-trigger="keyup"
    hx-target="#search-results">
```

- `name="query"` works exactly like a normal HTML form field
- HTMX automatically sends `query=<typed value>` to the backend

### 1.2 Update app.py imports

Modify your imports:

```python
from flask import Flask, render_template, request
```

- `request` allows Flask to access query parameters, form values, and HTTP data

### 1.3 Update /search route

Replace the existing `/search` route with:

```python
@app.route("/search")
def search():
    query = request.args.get("query", "")
    return f"<p>You typed: {query}</p>"
```

- `request.args.get("query", "")` retrieves the query parameter from the URL
- Example: if user types "apple", HTMX sends `/search?query=apple`
- Flask receives `apple` in the `query` variable
- Returns HTML with the typed value: `<p>You typed: apple</p>`

### 1.4 Test it

Refresh and type "hello".

Expected:
- `You typed: hello` appears dynamically while typing
- No full page refresh

- `name="query"` makes HTMX send `/search?query=<value>`.
- Flask reads that value with `request.args.get("query")` and returns HTML.
- HTMX swaps that HTML into `#search-results`.

Verify in DevTools Network:
- Open DevTools → **Network**
- Type `test`
- Confirm `GET /search?query=test` and an HTML response body

