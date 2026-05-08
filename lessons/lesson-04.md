# Lesson 04: Send input data from HTMX to Flask

Included step: 14

Learning objective:
Master one focused concept from step 14 with precise, sequential execution.

Editor notes:
- Keep the exact sequence from source material.
- Validate behavior at each test checkpoint before continuing.

## Detailed walkthrough

## 14) Send input data from HTMX to Flask

Now we will make the server receive the actual text being typed.

This is a major step because your UI becomes truly dynamic.

### 14.1 Update the input field

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

Important concept:
- `name="query"` works exactly like a normal HTML form field
- HTMX automatically sends `query=<typed value>` to the backend

### 14.2 Update app.py imports

Modify your imports:

```python
from flask import Flask, render_template, request
```

Why:
- `request` allows Flask to access query parameters, form values, and HTTP data

### 14.3 Update /search route

Replace the existing `/search` route with:

```python
@app.route("/search")
def search():
    query = request.args.get("query", "")
    return f"<p>You typed: {query}</p>"
```

What this does:
- `request.args.get("query", "")` retrieves the query parameter from the URL
- Example: if user types "apple", HTMX sends `/search?query=apple`
- Flask receives `apple` in the `query` variable
- Returns HTML with the typed value: `<p>You typed: apple</p>`

### 14.4 Test it

Refresh your browser.

Now type: **hello**

Expected result:
- `You typed: hello` appears dynamically while typing
- Without page refresh or native JavaScript

Critical breakthrough:
- You just implemented client → server communication
- Dynamic input binding
- Live request processing
- Server-generated reactive UI
- WITHOUT JavaScript frameworks

Important architecture insight:
- HTMX automatically serializes input values
- You do NOT manually build fetch requests, JSON payloads, or event listeners
- HTML itself becomes interactive

Inspect Network tab again:
- Open DevTools → **Network**
- Type something
- Observe requests like: `/search?query=test`
- This demonstrates query parameters in action

What you learned:
- Input serialization
- Query parameters
- Dynamic server rendering
- Live request handling
- Reactive server-driven UI

This is foundational web engineering.

