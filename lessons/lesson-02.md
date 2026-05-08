# Lesson 02: Project Scaffold and First HTMX Requests

Included steps: 7-12

Learning objective:
Create the project structure, first Flask page, and initial HTMX request/inspection loop.

Editor notes:
- This lesson combines foundational app wiring and first browser-network validation.
- Use Developer Tools checks to confirm request/response behavior before adding complexity.

## Included steps
- Step 7) Create the initial project structure
- Step 8) Create your first Flask application
- Step 9) Create the first HTMX page (`index.html`)
- Step 10) Run your Flask server
- Step 11) Trigger your first live HTMX request
- Step 12) Inspect the HTMX request using browser developer tools

## Detailed walkthrough

## 7) Create the initial project structure

Create core folders for Flask + HTMX:

```bash
mkdir templates
mkdir templates/partials
mkdir static
```

Verify structure:

```bash
tree
```

If `tree` is unavailable:

```bash
ls -R
```

Expected key entries:
- `templates/`
- `templates/partials/`
- `static/`
- `venv/`
- `requirements.txt`

Why these folders exist:
- `templates/`: Flask HTML pages, Jinja templates, and HTMX partial fragments.
- `templates/partials/`: Reusable HTML fragments for HTMX updates (table rows, cards, modal content, partial updates).
- `static/`: CSS, images, and optional JavaScript.

Architectural concept:
- Traditional SPA: frontend components render UI.
- HTMX architecture: server renders HTML fragments.
- Therefore `templates/partials/` is a core part of the structure.


## 8) Create your first Flask application

Create backend server file:

```bash
touch app.py
```

Add this code to `app.py`:

```python
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
	return render_template("index.html")


@app.route("/hello")
def hello():
	return "<h3>Hello HTMX + Flask!</h3>"


if __name__ == "__main__":
	app.run(debug=True)
```

What this does:
- Imports Flask app engine and template rendering.
- Creates the app instance with `app = Flask(__name__)`.
- Route `/` renders `templates/index.html`.
- Route `/hello` returns an HTML fragment for HTMX requests.
- `debug=True` enables auto reload and helpful error messages.

Important HTMX mental model:
- The `/hello` route returns HTML, not JSON.
- HTMX updates the page using server-rendered HTML fragments.


## 9) Create the first HTMX page (`index.html`)

Create template file:

```bash
touch templates/index.html
```

Add this code to `templates/index.html`:

```html
<!DOCTYPE html>
<html lang="en">

<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">

	<title>HTMX Learning</title>

	<!-- HTMX CDN -->
	<script src="https://unpkg.com/htmx.org@1.9.12"></script>
</head>

<body>

	<h1>HTMX + Flask</h1>

	<button
		hx-get="/hello"     <!-- On click, HTMX sends GET /hello to Flask (@app.route("/hello")) -->
		hx-target="#result"> <!-- HTMX finds <div id="result"> and injects the returned HTML there -->
		Click Me
	</button>

	<div id="result"></div>

</body>
</html>
```

What this adds:
- HTMX is loaded directly from CDN (no npm/webpack/build tool required).
- `hx-get="/hello"` sends a GET request to the Flask `/hello` route when clicked.
- `hx-target="#result"` injects the returned HTML into `<div id="result"></div>`.

Flow:
- Button click.
- HTMX request.
- Flask route (`/hello`).
- HTML response.
- `#result` updated.

Important concept:
- Flask returns HTML fragments (not JSON) for HTMX swaps.


## 10) Run your Flask server

Make sure virtual environment is active:

```bash
source venv/bin/activate
```

Run the app:

```bash
python app.py
```

Expected output includes:
- `* Running on http://127.0.0.1:5000`
- `* Debug mode: on`

What is happening:
- Flask is listening for HTTP requests.
- Routes are exposed and serving HTML.
- `/` serves `index.html`.
- `/hello` serves an HTML fragment.

Important concept:
- This is a live backend server running in Codespaces and accessible in the browser.
- This is no longer static HTML.

Keep the server running:
- Do not stop the terminal while testing.
- Open a new terminal for additional commands.


## 11) Trigger your first live HTMX request

With the Flask server still running:

1. Open your browser to http://127.0.0.1:5000
2. Click the **"Click Me"** button

What should happen:
- WITHOUT refreshing the page, `<div id="result"></div>` dynamically becomes:
- `<div id="result"><h3>Hello HTMX + Flask!</h3></div>`

What just happened internally:

**Browser Loaded Initial Page:**
- Flask rendered `render_template("index.html")`
- HTMX JavaScript loaded from CDN

**HTMX Intercepted the Click:**
- The `hx-get="/hello"` attribute triggered an asynchronous HTTP GET request
- No page reload

**Flask Executed the Route:**
- `@app.route("/hello")` was triggered
- Returned: `<h3>Hello HTMX + Flask!</h3>`

**HTMX Updated the DOM:**
- The `hx-target="#result"` attribute identified the target element
- HTMX injected the returned HTML into `<div id="result"></div>`

The critical breakthrough:
- You just performed AJAX, DOM updates, partial rendering, and async communication
- **WITHOUT** JavaScript, fetch(), axios, React state, or JSON APIs
- **ONLY** HTML, HTTP, Flask, and HTMX

Important reflection:
- This tiny example demonstrates why HTMX is powerful
- Why server-side rendering is returning
- Why developers are moving away from overly complex SPAs for many applications


## 12) Inspect the HTMX request using browser developer tools

This is one of the most important learning steps.

### 12.1 Open browser developer tools

Inside the browser running your app, open DevTools:
- Press **F12**, or
- Right Click → **Inspect**

### 12.2 Open the Network tab

Inside DevTools, click the **Network** tab.

This tab shows:
- HTTP requests and responses
- Headers
- Timing
- Payloads

### 12.3 Clear existing requests

Click the clear icon to empty the panel.

### 12.4 Click the button again

Click the **"Click Me"** button.

You should see a request appear in the Network tab, likely labeled:
- `hello` or
- `/hello`

### 12.5 Click the /hello request

Now inspect it carefully.

What you should observe:

**Request Method:**
- You should see: `GET`
- Because: `hx-get="/hello"` creates an HTTP GET request

**Request URL:**
- You should see: `/hello`
- Which maps directly to: `@app.route("/hello")`

**Response:**
- You should see: `<h3>Hello HTMX + Flask!</h3>`
- This is the exact HTML returned by Flask

**Critical observation:**
- The server returned **HTML**, not JSON
- This is the defining HTMX architecture principle

### 12.6 Observe HTMX headers

Look under **Request Headers**.

You may notice special HTMX headers like:
- `HX-Request: true`

This tells Flask:
- "This request came from HTMX"
- Very important later for partial rendering and conditional responses

What you just learned:

- HTMX sends real HTTP requests
- Flask handles them normally
- HTML fragments return
- HTMX swaps returned HTML into the DOM
- Browser DevTools help debug everything

Why this step matters:

Many developers use frameworks without understanding:
- requests
- responses
- rendering flow

You are now learning the actual web architecture underneath.

