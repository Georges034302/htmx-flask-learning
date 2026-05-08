# Lesson 03: Your first reactive HTMX interaction with hx-trigger

Included step: 13

Learning objective:
Master one focused concept from step 13 with precise, sequential execution.

Editor notes:
- Keep the exact sequence from source material.
- Validate behavior at each test checkpoint before continuing.

## Detailed walkthrough

## 13) Your first reactive HTMX interaction with hx-trigger

Now we will make HTMX send requests automatically while typing.

This is the beginning of:
- Live search
- Autocomplete
- Reactive forms
- Dynamic filtering
- WITHOUT JavaScript

### 13.1 Add new /search route to app.py

Add this NEW route below the `/hello` route:

```python
@app.route("/search")
def search():
    return "<p>Searching...</p>"
```

Your `app.py` should now contain BOTH `/hello` and `/search` routes.

Save the file.

Important observation:
- Because `debug=True`, Flask automatically reloads the server
- You do NOT need to restart manually
- Watch terminal output for reload activity

### 13.2 Add search input to templates/index.html

Add this BELOW the button section:

```html
<hr>

<h2>Live Search Demo</h2>

<input
    type="text"
    placeholder="Type something..."
    hx-get="/search"
    hx-trigger="keyup"
    hx-target="#search-results">

<div id="search-results"></div>
```

What is new here:

**hx-trigger="keyup":**
- Tells HTMX: "Send the request every time the user releases a keyboard key"
- This creates reactive behavior

Flow:
1. User types
2. keyup event fires
3. HTMX sends GET /search
4. Flask returns HTML
5. #search-results updates

### 13.3 Refresh your browser

Refresh your page once.

You should now see:
- The existing button demo
- The new input field

### 13.4 Test the input

Type inside the input field.

Expected:
- "Searching..." appears dynamically while typing
- WITHOUT page refresh or JavaScript

Important mental breakthrough:
- You just created reactive frontend behavior
- Event-driven UI
- Live requests
- Using only HTML attributes and Flask routes

This is a major HTMX capability.

Important note:
- Currently `return "<p>Searching...</p>"` is static
- Later you will pass query parameters, dynamic values, and filtered data
- This evolves naturally into live search, autocomplete, and filtering systems

