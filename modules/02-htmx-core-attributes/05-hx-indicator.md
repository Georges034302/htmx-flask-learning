# Lesson 07: Add loading indicators with hx-indicator

## Concept
Add loading indicators with hx-indicator.

## 1. Add loading indicators with hx-indicator

Make the UI visually react while waiting for the server.

- When HTMX sends a request: a loading message appears
- When response returns: loading message disappears automatically
- without JavaScript

### 1.1 Add a loading element

Add this BELOW your input field in `templates/index.html`:

```html
<p id="loading" style="display:none;">
    Loading...
</p>
```

### 1.2 Update the input field

Add `hx-indicator="#loading"` to your input:

```html
<input
    type="text"
    name="query"
    placeholder="Type something..."
    hx-get="/search"
    hx-trigger="keyup changed delay:500ms"
    hx-target="#search-results"
    hx-indicator="#loading">
```

What `hx-indicator` does:
- Tells HTMX: "While the request is active, show this element"
- When request finishes: HTMX automatically hides it again

### 1.3 Why you may not notice it yet

Your Flask response is currently very fast.

To make it visible, add a short server delay.

### 1.4 Add artificial delay

At the TOP of `app.py`, add:

```python
import time
```

### 1.5 Add delay inside /search

Inside your `/search` route, BEFORE filtering:

```python
time.sleep(1)
```

Full route example:

```python
@app.route("/search")
def search():
    time.sleep(1)

    query = request.args.get("query", "").lower()

    filtered_employees = []
    for employee in employees:
        if query in employee["name"].lower():
            filtered_employees.append(employee)

    return render_template(
        "partials/search_results.html",
        employees=filtered_employees
    )
```

**Note:** This simulates:
- Database latency
- API delay
- Network wait
- Backend processing

### 1.6 Test it

Refresh your browser.

Now type something.

Expected behavior:
- "Loading..." appears
- Delay occurs (1 second)
- Results appear
- Loading disappears automatically

**Note:**
- You just implemented async UX feedback, loading states, and reactive request indicators
- without extra frontend state code
- Behavior is described declaratively: `hx-indicator="#loading"`
- Instead of imperative JS logic
- This keeps frontend simpler, UI cleaner, maintenance easier

