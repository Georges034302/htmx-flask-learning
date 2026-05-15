# Lesson 02: Project Scaffold and First HTMX Requests

## Concept
Project Scaffold and First HTMX Requests.

## 1. Create the initial project structure

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

- Traditional SPA: frontend components render UI.
- HTMX architecture: server renders HTML fragments.
- Therefore `templates/partials/` is a core part of the structure.

## 2. Create your first Flask application

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

- Imports Flask app engine and template rendering.
- Creates the app instance with `app = Flask(__name__)`.
- Route `/` renders `templates/index.html`.
- Route `/hello` returns an HTML fragment for HTMX requests.
- `debug=True` enables auto reload and helpful error messages.
- The `/hello` route returns HTML, not JSON.
- HTMX updates the page using server-rendered HTML fragments.

## 3. Create the first HTMX page (`index.html`)

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

- HTMX is loaded directly from CDN (no npm/webpack/build tool required).
- `hx-get="/hello"` sends a GET request to the Flask `/hello` route when clicked.
- `hx-target="#result"` injects the returned HTML into `<div id="result"></div>`.

Request flow:
- Button click.
- HTMX request.
- Flask route (`/hello`).
- HTML response.
- `#result` updated.

- Flask returns HTML fragments (not JSON) for HTMX swaps.

## 4. Run your Flask server

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

**Note:** What is happening:
- Flask is listening for HTTP requests.
- Routes are exposed and serving HTML.
- `/` serves `index.html`.
- `/hello` serves an HTML fragment.

- This is a live backend server running in Codespaces and accessible in the browser.
- This is no longer static HTML.

Keep the server running:
- Do not stop the terminal while testing.
- Open a new terminal for additional commands.

## 5. Trigger your first live HTMX request

With the Flask server still running:

1. Open your browser to http://127.0.0.1:5000
2. Click the **"Click Me"** button

What should happen:
- `<div id="result"><h3>Hello HTMX + Flask!</h3></div>` appears without a page reload.

**Note:**
- Click triggers `GET /hello`.
- Flask returns an HTML fragment.
- HTMX swaps that fragment into `#result`.

## 6. Inspect the HTMX request using browser developer tools

### 6.1 Open browser developer tools

Inside the browser running your app, open DevTools:
- Press **F12**, or
- Right Click → **Inspect**

### 6.2 Open the Network tab

Inside DevTools, click the **Network** tab.

This tab shows:
- HTTP requests and responses
- Headers
- Timing
- Payloads

### 6.3 Clear existing requests

Click the clear icon to empty the panel.

### 6.4 Click the button again

Click the **"Click Me"** button.

You should see a request appear in the Network tab, likely labeled:
- `hello` or
- `/hello`

### 6.5 Click the /hello request

Now inspect it carefully.

What you should observe:
- Method: `GET`
- URL: `/hello`
- Response body: `<h3>Hello HTMX + Flask!</h3>`
- Response type: HTML fragment (not JSON)

### 6.6 Observe HTMX headers

Look under **Request Headers**.

You may notice special HTMX headers like:
- `HX-Request: true`

This means the request was triggered by HTMX.
Use it when you need different responses for partial updates versus full page loads.

