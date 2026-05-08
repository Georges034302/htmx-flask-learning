# Environment Setup Instructions

This file records the exact setup steps run in this repository.

## 1) Check Python version

```bash
python --version || python3 --version
```

Observed version:
- Python 3.12.1

## 2) Create virtual environment

```bash
python3 -m venv venv
```

Verified with:

```bash
ls -ld venv
```

## 3) Activate virtual environment

```bash
source venv/bin/activate
```

Verified with:

```bash
echo "$VIRTUAL_ENV"
which python
python --version
```

Expected verification:
- VIRTUAL_ENV points to `<repo>/venv`
- Python path points to `<repo>/venv/bin/python`
- Python version is 3.12.1

## 4) Add ignore rules

Created `.gitignore` with:

```gitignore
venv/
.vscode/
```

## 5) Install Flask

```bash
source venv/bin/activate && pip install flask
```

Verified with:

```bash
pip show flask
```

Installed version:
- Flask 3.1.3

Package listing:

```bash
source venv/bin/activate && pip list
```

Installed packages at that time:
- blinker 1.9.0
- click 8.3.3
- Flask 3.1.3
- itsdangerous 2.2.0
- Jinja2 3.1.6
- MarkupSafe 3.0.3
- pip 23.2.1
- Werkzeug 3.1.8

## 6) Create and verify requirements file

```bash
source venv/bin/activate
pip freeze > requirements.txt
cat requirements.txt
pip install -r requirements.txt
pip freeze > requirements.txt
```

Notes:
- `cat requirements` was intended, but the actual file is `requirements.txt`.
- Reinstalling from `requirements.txt` confirmed all packages were already satisfied.

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

That is a huge advantage.

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

## 15) Add smart request timing with delay

Right now, every keystroke sends a request immediately.

That works, but in real applications it can generate:
- Too many requests
- Unnecessary server load
- Poor UX

HTMX provides an elegant solution: **delay**

Goal:
- Instead of: Request on EVERY key
- We will make HTMX: Wait briefly while the user types, then only send after typing pauses
- This mimics professional live-search systems

### 15.1 Update hx-trigger with debounce

Replace:

```html
hx-trigger="keyup"
```

WITH:

```html
hx-trigger="keyup changed delay:500ms"
```

Your FULL input should now become:

```html
<input
    type="text"
    name="query"
    placeholder="Type something..."
    hx-get="/search"
    hx-trigger="keyup changed delay:500ms"
    hx-target="#search-results">
```

What this means:
- `keyup`: Trigger after keyboard interaction
- `changed`: Only send request if value actually changed
- `delay:500ms`: Wait 500 milliseconds before sending
- If user keeps typing: timer resets and request waits

Important concept:
- This is called **debouncing**
- In traditional JavaScript frameworks, this requires event listeners, timers, and state logic
- HTMX does it declaratively in HTML

### 15.2 Test it

Refresh your browser.

Now type quickly.

Observe:
- Requests do NOT fire instantly
- HTMX waits briefly
- Request happens after typing pauses

### 15.3 Inspect Network tab

Open DevTools → **Network**.

Type quickly.

You should now see:
- Fewer requests
- Cleaner request timing
- More efficient behavior

Important real-world relevance:
- This pattern is heavily used in search engines, filtering systems, dashboards, autocomplete systems, and admin panels

Mental shift:
- Instead of writing imperative JavaScript logic
- You describe behavior declaratively: `hx-trigger="keyup changed delay:500ms"`
- This is classic HTMX philosophy

What you just learned:
- HTMX event triggers
- Request timing
- Debounce behavior
- Reactive optimization
- Declarative frontend interaction

This is already professional-level frontend behavior.

## 16) Return dynamic HTML fragments instead of plain text

Now we move into one of the MOST important HTMX concepts: **Server-rendered HTML fragments**

Right now your Flask route returns:
- `<p>You typed: hello</p>`

But real HTMX applications usually return:
- Cards
- Table rows
- Lists
- Components
- Partial templates

This is where HTMX starts becoming a real application architecture.

Goal:
- Instead of returning plain text
- Return dynamically generated HTML based on mock data
- Rendered by Flask
- You are about to build your FIRST real HTMX component

### 16.1 Add mock data

Inside `app.py`, ADD this ABOVE your routes (after `app = Flask(__name__)`):

```python
# Mock data
employees = [
    {"id": 1, "name": "Alice", "department": "IT"},
    {"id": 2, "name": "Bob", "department": "HR"},
    {"id": 3, "name": "Charlie", "department": "Finance"},
    {"id": 4, "name": "David", "department": "IT"},
    {"id": 5, "name": "Emma", "department": "Marketing"}
]
```

Why:
- We now simulate database records, API results, and business data
- WITHOUT using a real database yet
- Perfect for Phase 1 learning

### 16.2 Create partial template

Create file: `templates/partials/search_results.html`

Add:

```html
<ul>
{% for employee in employees %}
    <li>
        {{ employee.name }} - {{ employee.department }}
    </li>
{% endfor %}
</ul>
```

Important concept:
- This is a **partial template**
- NOT a full HTML page
- Designed specifically for HTMX injection
- This becomes a core architectural pattern

### 16.3 Update /search route

Replace your current `/search` route WITH:

```python
@app.route("/search")
def search():
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

What this does:
- **Read user input**: `query = request.args.get("query", "").lower()`
- **Filter employees**: If user types "a", matches Alice, Charlie, David, Emma
- **Return partial template**: `render_template(...)` returns ONLY the HTML fragment, NOT an entire page
- This is REAL HTMX architecture

### 16.4 Test it

Refresh your browser.

Now type: **a**

Expected dynamic results:
- Alice
- Charlie
- David
- Emma

Type: **bo**

Expected:
- Bob

Important breakthrough:
- You are now building server-rendered components
- Dynamic filtering
- Partial template rendering
- Live reactive UI
- Without React, Vue, Angular, or JSON APIs
- This is the heart of HTMX

VERY IMPORTANT CONCEPT:

**Traditional SPA:**
- Server returns DATA
- Frontend renders UI

**HTMX:**
- Server returns READY HTML
- The server owns rendering
- Massive architectural simplification

Observe the Network tab again:
- You should now see requests sent while typing
- HTML fragments returned
- DOM updated dynamically
- Professional reactive behavior
- Minimal complexity

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

## 18) Replace vs append content with hx-swap

Now you will learn how HTMX injects returned HTML into the page.

This is controlled by: `hx-swap`

Current behavior in this project:
- Input is configured with `hx-swap="beforeend"`
- Returned HTML is appended to existing content in `#search-results`

Default HTMX behavior (for reference):
- If `hx-swap` is omitted, HTMX uses `innerHTML`
- Existing content inside target gets replaced

Goal:
- Experiment with replacing content
- Experiment with appending content
- Understand DOM injection behavior

### 18.1 Add hx-swap (replace mode)

Update your input field with:

```html
hx-swap="innerHTML"
```

Full input:

```html
<input
    type="text"
    name="query"
    placeholder="Type something..."
    hx-get="/search"
    hx-trigger="keyup changed delay:500ms"
    hx-target="#search-results"
    hx-indicator="#loading"
    hx-swap="innerHTML">
```

What `innerHTML` means:
- Replace ONLY the inside of the target element
- The target container remains, its contents are replaced

### 18.2 Test current behavior

Refresh page and type: `a`

Results replace normally. This is expected.

### 18.3 Switch to beforeend (append mode)

Change:

```html
hx-swap="innerHTML"
```

To:

```html
hx-swap="beforeend"
```

What this means:
- Instead of replacing, HTMX appends returned HTML
- Conceptually similar to: `element.innerHTML += newContent`

Current implementation note:
- The live input in `templates/index.html` is now set to `hx-swap="beforeend"`.
- To go back to replacement behavior, change it to `hx-swap="innerHTML"`.

### 18.4 Test again

Refresh page, then type:
- `a`
- `b`
- `c`

Observe:
- Results keep appending

Important observation:
- You are now controlling DOM insertion strategy
- Content placement behavior
- UI rendering mechanics
- Directly from HTML attributes

## 19) Trigger requests automatically on page load

Now you will learn another very important HTMX capability: `hx-trigger="load"`.

This allows HTMX to automatically fetch content immediately after the page loads, without user interaction.

Common uses:
- Dashboards
- Monitoring systems
- Analytics pages
- Activity feeds
- Admin portals

Goal:
- When the page opens, HTMX automatically requests data
- Flask returns HTML
- Content appears dynamically

### 19.1 Create a new route

Add this route in `app.py`:

```python
@app.route("/latest")
def latest():

    latest_updates = [
        "Server running normally",
        "3 new employees added",
        "Backup completed successfully"
    ]

    return render_template(
        "partials/latest.html",
        updates=latest_updates
    )
```

### 19.2 Create partial template

Create file: `templates/partials/latest.html`

```html
<h3>Latest Updates</h3>

<ul>
{% for update in updates %}
    <li>{{ update }}</li>
{% endfor %}
</ul>
```

### 19.3 Add auto-loading section to index.html

Add this below the search section:

```html
<hr>

<h2>Automatic Content Loading</h2>

<div
    hx-get="/latest"
    hx-trigger="load"
    hx-target="this">

    Loading latest updates...

</div>
```

Important concepts:
- `hx-trigger="load"`: trigger request automatically when element loads
- `hx-target="this"`: replace the element itself with returned HTML

### 19.4 Test it

Refresh browser.

Expected behavior:
- Page loads
- "Loading latest updates..." appears briefly
- HTMX requests `/latest` automatically
- Flask returns HTML fragment
- Content replaces the loading div

No user interaction required.

Observe Network tab:
- Refresh with DevTools open
- You should see automatic `/latest` request

What you learned:
- Automatic HTMX requests
- Load triggers
- Self-replacing components
- Async page initialization
- Dashboard-style rendering

## 20) Build your first dynamic table component

Now we move from simple lists to structured UI rendering.

Goal:
- Reusable table rendering
- Structured HTML fragments
- Server-driven table UI

This pattern is heavily used in:
- Admin portals
- Dashboards
- Inventory systems
- HR systems
- DevOps tools

### 20.1 Create new route

Add in `app.py`:

```python
@app.route("/employees")
def get_employees():

    return render_template(
        "partials/employees_table.html",
        employees=employees
    )
```

What this does:
- Returns only a table fragment
- Not a full page
- Matches HTMX partial architecture

### 20.2 Create table partial

Create file: `templates/partials/employees_table.html`

```html
<table border="1" cellpadding="10">

    <thead>
        <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Department</th>
        </tr>
    </thead>

    <tbody>
    {% for employee in employees %}
        <tr>
            <td>{{ employee.id }}</td>
            <td>{{ employee.name }}</td>
            <td>{{ employee.department }}</td>
        </tr>
    {% endfor %}
    </tbody>

</table>
```

Jinja observation:
- `{{ employee.name }}` uses dot notation on dictionary data
- Bracket notation works too

### 20.3 Add HTMX table loader to index.html

Add below latest updates section:

```html
<hr>

<h2>Employee Table</h2>

<button
    hx-get="/employees"
    hx-target="#employee-table">
    Load Employees
</button>

<div id="employee-table"></div>
```

What this does:
- Button click sends request to `/employees`
- Flask renders table partial
- HTMX injects table into `#employee-table`

### 20.4 Test it

Refresh browser and click **Load Employees**.

Expected:
- Full HTML table appears dynamically
- No page refresh
- No JavaScript table rendering
- No JSON API response required

Why this is powerful:
- Traditional SPA: JSON -> JS -> build table
- HTMX: Flask -> render HTML table -> inject

What you learned:
- Partial table rendering
- Reusable server components
- Structured UI injection
- Dynamic table loading
- Enterprise HTMX pattern

## 21) Create your first HTMX form submission with hx-post

So far you have fetched data, loaded fragments, and updated content dynamically.

Now you will send data to the server.

Goal:
- Create a form
- Submit data with HTMX
- Flask receives form data
- Flask returns HTML response
- HTMX updates page dynamically

### 21.1 Add new route to app.py

Add:

```python
@app.route("/add-employee", methods=["POST"])
def add_employee():

    name = request.form.get("name")
    department = request.form.get("department")

    new_employee = {
        "id": len(employees) + 1,
        "name": name,
        "department": department
    }

    employees.append(new_employee)

    return f"""
        <p>
            Added employee:
            <strong>{name}</strong>
            ({department})
        </p>
    """
```

Important concepts:
- `methods=["POST"]` allows POST requests.
- `request.form.get(...)` reads submitted form data.
- This is different from `request.args` (query parameters).

### 21.2 Add form to index.html

Add below employee table section:

```html
<hr>

<h2>Add Employee</h2>

<form
    hx-post="/add-employee"
    hx-target="#form-result">

    <input
        type="text"
        name="name"
        placeholder="Employee Name"
        required>

    <input
        type="text"
        name="department"
        placeholder="Department"
        required>

    <button type="submit">
        Add Employee
    </button>

</form>

<div id="form-result"></div>
```

What HTMX does automatically:
- Serializes form fields
- Sends async POST request
- Handles server response
- Updates target element

### 21.3 Test it

Refresh browser and submit:
- Name: Sarah
- Department: Security

Expected:
- Added employee: Sarah (Security)
- Appears dynamically without page refresh

Observe Network tab:
- POST request
- Form payload
- HTML response

What you learned:
- `hx-post`
- Async form submission
- POST requests
- Form serialization
- `request.form`
- Server-driven UI updates

## 22) Automatically refresh the employee table after form submission

Now we connect components together.

Current state before this step:
- Form submission works
- Employee gets added
- Table does not refresh automatically

Goal:
- After form submit, employee is added and table refreshes automatically
- Keep UI synchronized without page refresh or custom JavaScript

### 22.1 Add an ID to the form

Update form tag:

```html
<form
    id="employee-form"
    hx-post="/add-employee"
    hx-target="#form-result">
```

### 22.2 Replace employee table section

Use this full section:

```html
<hr>

<h2>Employee Table</h2>

<div
    hx-get="/employees"
    hx-trigger="load, employee-added from:body"
    hx-target="this">

    Loading employees...

</div>
```

Important concept:
- `employee-added from:body` means listen for custom `employee-added` event from page body.
- This enables event-driven component updates.

### 22.3 Update /add-employee route response

Return with HTMX trigger header:

```python
response = f"""
    <p>
        Added employee:
        <strong>{name}</strong>
        ({department})
    </p>
"""

return response, 200, {
    "HX-Trigger": "employee-added"
}
```

Full route:

```python
@app.route("/add-employee", methods=["POST"])
def add_employee():

    name = request.form.get("name")
    department = request.form.get("department")

    new_employee = {
        "id": len(employees) + 1,
        "name": name,
        "department": department
    }

    employees.append(new_employee)

    response = f"""
        <p>
            Added employee:
            <strong>{name}</strong>
            ({department})
        </p>
    """

    return response, 200, {
        "HX-Trigger": "employee-added"
    }
```

How this works:
- POST `/add-employee` succeeds
- Response header fires `employee-added`
- Table component hears event via `hx-trigger`
- Table auto-refreshes with GET `/employees`

### 22.4 Test it

Refresh page.

Expected:
- Table auto-loads
- Submit new employee
- Employee appears in table immediately

No manual reload, no page refresh, no custom JS handlers.

Observe in DevTools network:
- POST `/add-employee`
- Trigger fires
- GET `/employees`

What you learned:
- Custom HTMX events
- `HX-Trigger` response headers
- Event-driven rendering
- Component synchronization
- Reactive UI architecture

## 23) Delete employees dynamically with hx-delete

Now you add the Delete part of CRUD.

Goal:
- Add a Delete button per employee
- Send DELETE request to Flask
- Remove employee from backend list
- Refresh table automatically

### 23.1 Update employee table partial

Open `templates/partials/employees_table.html`.

Add Actions header:

```html
<th>Actions</th>
```

Add this action cell in each employee row:

```html
<td>

    <button
        hx-delete="/delete-employee/{{ employee.id }}"
        hx-confirm="Are you sure?"
        hx-trigger="click">

        Delete

    </button>

</td>
```

Important attributes:
- `hx-delete`: sends HTTP DELETE request
- `hx-confirm`: shows confirmation dialog before request

### 23.2 Add delete route to app.py

Add:

```python
@app.route("/delete-employee/<int:id>", methods=["DELETE"])
def delete_employee(id):

    global employees

    employees = [
        employee
        for employee in employees
        if employee["id"] != id
    ]

    return "", 200, {
        "HX-Trigger": "employee-added"
    }
```

Why reuse `HX-Trigger: employee-added`:
- Table already listens for this event
- Add and delete operations can refresh the same component with one event name

Python note:
- List comprehension rebuilds `employees` while excluding the deleted ID

### 23.3 Test it

Refresh browser.

Then:
- Load table
- Click Delete
- Confirm dialog appears
- Employee is removed
- Table refreshes automatically

No page refresh and no custom JavaScript required.

Observe in DevTools network:
- DELETE request
- Trigger event
- GET `/employees` to refresh table

What you learned:
- `hx-delete`
- DELETE requests
- Confirmation dialogs
- Reactive CRUD updates
- Event reuse
- Dynamic component synchronization

## 24) Remove rows instantly with hx-swap="outerHTML"

Now deletion becomes fine-grained and does not require full table refresh.

Goal:
- Delete only the affected row
- Keep the rest of the table intact
- Avoid secondary table reload request

### 24.1 Update delete button in table partial

In `templates/partials/employees_table.html`, add:
- `hx-target="closest tr"`
- `hx-swap="outerHTML"`

Full button:

```html
<button
    hx-delete="/delete-employee/{{ employee.id }}"
    hx-confirm="Are you sure?"
    hx-trigger="click"
    hx-target="closest tr"
    hx-swap="outerHTML">

    Delete

</button>
```

Concepts:
- `hx-target="closest tr"`: target nearest table row
- `hx-swap="outerHTML"`: replace/remove the entire row element itself

### 24.2 Update delete route

Replace:

```python
return "", 200, {
    "HX-Trigger": "employee-added"
}
```

With:

```python
return ""
```

Full route:

```python
@app.route("/delete-employee/<int:id>", methods=["DELETE"])
def delete_employee(id):

    global employees

    employees = [
        employee
        for employee in employees
        if employee["id"] != id
    ]

    return ""
```

Why it works:
- HTMX targets the row itself
- Server returns empty content
- Row outerHTML is replaced with empty response
- Row disappears immediately

### 24.3 Test it

Refresh browser and delete one employee.

Expected:
- Only selected row disappears
- Table remains visible
- No full-table reload

Observe in DevTools:
- One DELETE request only
- No follow-up GET `/employees` request for delete

What you learned:
- `outerHTML` swaps
- Closest-element targeting
- Fine-grained DOM updates
- Efficient reactive rendering

## 25) Edit employees inline with hx-put

Now you complete full CRUD by adding inline Update behavior.

Goal:
- Click Edit
- Load inline edit form inside the row
- Save asynchronously with PUT
- Replace row dynamically

### 25.1 Add Edit button in row actions

In `templates/partials/employees_table.html` rows, add Edit above Delete:

```html
<button
    hx-get="/edit-employee/{{ employee.id }}"
    hx-target="closest tr"
    hx-swap="outerHTML">

    Edit

</button>
```

What this does:
- Sends GET request
- Flask returns editable row HTML
- Current row is replaced

### 25.2 Create editable row partial

Create `templates/partials/edit_employee_row.html`:

```html
<tr>

<form
    hx-put="/update-employee/{{ employee.id }}"
    hx-target="closest tr"
    hx-swap="outerHTML">

    <td>{{ employee.id }}</td>

    <td>
        <input
            type="text"
            name="name"
            value="{{ employee.name }}">
    </td>

    <td>
        <input
            type="text"
            name="department"
            value="{{ employee.department }}">
    </td>

    <td>
        <button type="submit">
            Save
        </button>
    </td>

</form>

</tr>
```

### 25.3 Create normal display row partial

Create `templates/partials/employee_row.html`:

```html
<tr>

    <td>{{ employee.id }}</td>
    <td>{{ employee.name }}</td>
    <td>{{ employee.department }}</td>

    <td>

        <button
            hx-get="/edit-employee/{{ employee.id }}"
            hx-target="closest tr"
            hx-swap="outerHTML">

            Edit

        </button>

        <button
            hx-delete="/delete-employee/{{ employee.id }}"
            hx-confirm="Are you sure?"
            hx-trigger="click"
            hx-target="closest tr"
            hx-swap="outerHTML">

            Delete

        </button>

    </td>

</tr>
```

### 25.4 Refactor table body to reusable include

In `templates/partials/employees_table.html`, loop becomes:

```html
<tbody>

{% for employee in employees %}

    {% include "partials/employee_row.html" %}

{% endfor %}

</tbody>
```

This introduces reusable server-rendered UI components.

### 25.5 Add edit route

In `app.py`:

```python
@app.route("/edit-employee/<int:id>")
def edit_employee(id):

    employee = next(
        (
            employee
            for employee in employees
            if employee["id"] == id
        ),
        None
    )

    return render_template(
        "partials/edit_employee_row.html",
        employee=employee
    )
```

### 25.6 Add update route with PUT

In `app.py`:

```python
@app.route("/update-employee/<int:id>", methods=["PUT"])
def update_employee(id):

    employee = next(
        (
            employee
            for employee in employees
            if employee["id"] == id
        ),
        None
    )

    employee["name"] = request.form.get("name")
    employee["department"] = request.form.get("department")

    return render_template(
        "partials/employee_row.html",
        employee=employee
    )
```

Important concept:
- `hx-put` sends HTTP PUT for update operations.

### 25.7 Test it

Refresh page, then:
- Click Edit on a row
- Row transforms into inline form
- Modify values
- Click Save
- Row updates dynamically

No page refresh and no frontend framework needed.

What you learned:
- `hx-put`
- Inline editing
- Component replacement
- Reusable partials
- Dynamic form injection
- Full reactive CRUD architecture

## 26) Add a Cancel button to inline editing

Now inline edit mode can be rolled back cleanly.

Goal:
- Click Cancel in edit mode
- Restore normal row view
- No page refresh

### 26.1 Add Cancel button in edit row partial

In `templates/partials/edit_employee_row.html`, add below Save:

```html
<button
    type="button"
    hx-get="/employee-row/{{ employee.id }}"
    hx-target="closest tr"
    hx-swap="outerHTML">

    Cancel

</button>
```

Important concept:
- `type="button"` prevents unintended submit behavior.

What this does:
- Sends GET request for display row
- Replaces editable row with normal row component

### 26.2 Add restore-row route in app.py

Add:

```python
@app.route("/employee-row/<int:id>")
def employee_row(id):

    employee = next(
        (
            employee
            for employee in employees
            if employee["id"] == id
        ),
        None
    )

    return render_template(
        "partials/employee_row.html",
        employee=employee
    )
```

This returns one row fragment only, which is efficient for inline UI rollback.

### 26.3 Test it

Refresh page.

Then:
- Click Edit
- Editable row appears
- Click Cancel
- Original row returns

No page refresh required.

What you learned:
- Reversible component rendering
- UI rollback pattern
- Inline state switching
- Component restoration
- Efficient row-level rendering

---

## 27) Add CSS Styling and Improve UX Structure

### Goal
Add a stylesheet to improve readability, layout, and visual structure without changing architecture.

### 27.1 Create CSS File

Created: `static/style.css`

Flask automatically serves files in `/static/` via `url_for('static', ...)`.

### 27.2 Link CSS in index.html

Inside `<head>`, below the HTMX script:

```html
<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
```

`url_for('static', filename='style.css')` is an important Flask convention for referencing static assets.

### 27.3 CSS added (static/style.css)

Styles body, headings, inputs, buttons, table (zebra striping, header), and `#loading` indicator.

### 27.4 What you learned
- Flask static files convention
- CSS integration with HTMX
- UI enhancement without frontend frameworks
- Separation of structure and styling
- HTMX works perfectly with simple HTML + lightweight CSS

---

## Fix: Live Search — switch beforeend to innerHTML

Changed `hx-swap` on the live search input from `beforeend` to `innerHTML`.

**Before:** each keystroke appended results, so old results accumulated.  
**After:** each keystroke replaces the result container, showing only current matches.

```html
hx-swap="innerHTML"
```

---

## Fix: Latest Updates — trigger on employee-added event

The `/latest` section previously only triggered on `load` (page load only).

Updated `hx-trigger` to also respond to `employee-added from:body`:

```html
hx-trigger="load, employee-added from:body"
```

**Note:** `/latest` is a learning demo for HTMX's auto-load trigger. Its content is hardcoded server-side (not a real activity feed). Delete and update are row-level `outerHTML` swaps — they do not fire `employee-added`, so they do not trigger a latest refresh. Only Add Employee fires that event.

---

## 28) Refactor the Flask Application Structure

### Goal
Move mock data out of `app.py` into a separate module — separating data from logic.

### 28.1 Create data/mock.py

Created `data/mock.py` with the employees list:

```python
employees = [
    {"id": 1, "name": "Alice", "department": "IT"},
    {"id": 2, "name": "Bob", "department": "HR"},
    {"id": 3, "name": "Charlie", "department": "Finance"},
    {"id": 4, "name": "David", "department": "IT"},
    {"id": 5, "name": "Emma", "department": "Marketing"}
]
```

### 28.2 Update app.py

Removed the inline `employees` list from `app.py`.

Added import at the top:

```python
from data.mock import employees
```

HTMX behavior, routes, and templates are unchanged.

### Project Structure

```
htmx-flask-learning/
├── app.py
├── requirements.txt
├── data/
│   └── mock.py
├── templates/
│   ├── index.html
│   └── partials/
├── static/
│   └── style.css
└── venv/
```

### What you learned
- Basic project refactoring
- Python module imports
- Separating data from logic
- Improving maintainability
- Incremental architecture evolution — learn mechanics first, then organize structure

---

## 29) Introduce Flask Blueprints (Modular Route Organization)

### Goal
Move all routes from `app.py` into a Blueprint module, leaving `app.py` as a clean entry point.

### 29.1 Create routes/main_routes.py

Created `routes/main_routes.py` with:

```python
from flask import Blueprint, render_template, request
import time
from data.mock import employees

main = Blueprint("main", __name__)
```

All routes moved here with decorators changed from `@app.route` to `@main.route`.

### 29.2 Simplify app.py

`app.py` is now just an entry point:

```python
from flask import Flask
from routes.main_routes import main

app = Flask(__name__)
app.register_blueprint(main)

if __name__ == "__main__":
    app.run(debug=True)
```

`app.register_blueprint(main)` tells Flask to load all routes from the Blueprint.

### Project Structure

```
htmx-flask-learning/
├── app.py
├── requirements.txt
├── data/
│   └── mock.py
├── routes/
│   └── main_routes.py
├── templates/
│   ├── index.html
│   └── partials/
├── static/
│   └── style.css
└── venv/
```

### What you learned
- Flask Blueprints concept and purpose
- Modular route organization
- `register_blueprint()` wiring
- Scalable Flask architecture
- Separation of concerns — entry point vs route logic

---

## 30) Add Real Search Filtering by Multiple Fields

### Goal
Extend the `/search` route to filter by both `name` and `department`, not just name.

### 30.1 Updated filtering logic in routes/main_routes.py

```python
filtered_employees = []
for employee in employees:
    name_match = query in employee["name"].lower()
    department_match = query in employee["department"].lower()
    if name_match or department_match:
        filtered_employees.append(employee)
```

### 30.2 Test cases

| Query    | Expected results  |
|----------|-------------------|
| `IT`     | Alice, David      |
| `Finance`| Charlie           |
| `Emma`   | Emma              |
| `HR`     | Bob               |

### What you learned
- Multi-field backend filtering
- OR logic for search matching
- Server-side search architecture vs frontend JS filtering
- HTMX philosophy: backend owns logic and rendering, frontend stays lightweight
