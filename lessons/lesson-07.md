# Lesson 07: Add loading indicators with hx-indicator

Included step: 17

Learning objective:
Master one focused concept from step 17 with precise, sequential execution.

Editor notes:
- Keep the exact sequence from source material.
- Validate behavior at each test checkpoint before continuing.

## Detailed walkthrough

## 17) Add loading indicators with hx-indicator

Now we will make the UI visually react while waiting for the server.

This introduces: **hx-indicator**

Extremely important for:
- Professional UX
- Async feedback
- Real-world applications

Goal:
- When HTMX sends a request: a loading message appears
- When response returns: loading message disappears automatically
- WITHOUT JavaScript

### 17.1 Add a loading element

Add this BELOW your input field in `templates/index.html`:

```html
<p id="loading" style="display:none;">
    Loading...
</p>
```

### 17.2 Update the input field

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

### 17.3 Why you may not notice it yet

Your Flask response is currently very fast.

The loading message may appear too quickly to notice.

So we will simulate server delay.

### 17.4 Add artificial delay

At the TOP of `app.py`, add:

```python
import time
```

### 17.5 Add delay inside /search

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

What this simulates:
- Database latency
- API delay
- Network wait
- Backend processing
- Very realistic

### 17.6 Test it

Refresh your browser.

Now type something.

Expected behavior:
- "Loading..." appears
- Delay occurs (1 second)
- Results appear
- Loading disappears automatically

Important observation:
- You just implemented async UX feedback, loading states, and reactive request indicators
- WITHOUT JavaScript state management, async handlers, or frontend libraries

Important HTMX philosophy:
- Behavior is described declaratively: `hx-indicator="#loading"`
- Instead of imperative JS logic
- This keeps frontend simpler, UI cleaner, maintenance easier

What you learned:
- Request lifecycle visualization
- Async UI feedback
- Loading indicators
- HTMX request states

This is real production-style behavior.

