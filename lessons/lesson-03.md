# Lesson 03: Your first reactive HTMX interaction with hx-trigger

Included step: 13

## Concept
Your first reactive HTMX interaction with hx-trigger.

## Step flow

## 13) Your first reactive HTMX interaction with hx-trigger

Make HTMX send requests automatically while typing.

### 13.1 Add new /search route to app.py

Add this NEW route below the `/hello` route:

```python
@app.route("/search")
def search():
    return "<p>Searching...</p>"
```

Your `app.py` should now contain BOTH `/hello` and `/search` routes.

Save the file.

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

- `hx-trigger="keyup"` sends a request on each key release.

Request flow:
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
- without page refresh or JavaScript

- Currently `return "<p>Searching...</p>"` is static
- Later you will pass query parameters, dynamic values, and filtered data

