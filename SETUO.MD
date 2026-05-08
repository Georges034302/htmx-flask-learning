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

---

## 31) Add Empty-State Handling ("No Results Found")

### Goal
When search returns no results, display a clear message instead of leaving the UI blank.

### 31.1 Updated templates/partials/search_results.html

Replaced the bare `{% for %}` loop with a Jinja conditional:

```html
{% if employees %}
<ul>
{% for employee in employees %}
    <li>
        {{ employee.name }} - {{ employee.department }}
    </li>
{% endfor %}
</ul>
{% else %}
<p>No employees found.</p>
{% endif %}
```

`{% if employees %}` evaluates to `True` when the list is non-empty, and `False` when it is empty — equivalent to checking `employees.length > 0`.

### 31.2 Test cases

| Query  | Expected result             |
|--------|-----------------------------|
| `zzzz` | No employees found.         |
| `IT`   | Alice, David                |

### Architectural note
The server decides which UI state to render — results list or empty-state message. No frontend JavaScript required. This is the core HTMX philosophy: centralized, server-driven rendering.

### What you learned
- Jinja conditional rendering (`{% if %} / {% else %} / {% endif %}`)
- Empty-state UX pattern
- Server-driven UI states
- Professional application feedback (loading states, empty states, error states)
- HTMX architecture: server owns all rendering decisions

---

## 32) Add Dynamic Search Result Count

### Goal
Display the number of matching employees alongside search results so users always know how many records were found.

### 32.1 Updated templates/partials/search_results.html

```html
{% if employees %}

<p>
    <strong>{{ employees|length }}</strong>
    employee{% if employees|length != 1 %}s{% endif %} found.
</p>

<ul>
{% for employee in employees %}
    <li>
        {{ employee.name }} - {{ employee.department }}
    </li>
{% endfor %}
</ul>

{% else %}

<p>No employees found.</p>

{% endif %}
```

Key Jinja concepts used:
- `employees|length` — Jinja filter equivalent to `len(employees)`, calculates list size.
- `{% if employees|length != 1 %}s{% endif %}` — handles singular/plural grammar ("1 employee found" vs "2 employees found").

### 32.2 Test cases

| Query  | Expected result          |
|--------|--------------------------|
| `IT`   | **2** employees found.   |
| `Emma` | **1** employee found.    |
| `zzzz` | No employees found.      |

### Architectural note
The backend now controls filtering, rendering, count calculation, and UX messaging in one place. The frontend receives ready-to-display HTML — no JavaScript counter logic required.

### What you learned
- Jinja filters (`|length`)
- Singular/plural conditional rendering
- Dynamic result counts
- Continuous UI feedback
- Centralized server-driven UX states

---

## 33) Add Real-Time Table Filtering with HTMX

### Goal
Wire the search input directly to the employee table so typing filters the table live — no separate search results section.

### 33.1 Updated /employees route (routes/main_routes.py)

Added query-parameter filtering, matching both `name` and `department`:

```python
@main.route("/employees")
def get_employees():
    query = request.args.get("query", "").lower()

    filtered_employees = []
    for employee in employees:
        name_match = query in employee["name"].lower()
        department_match = query in employee["department"].lower()
        if name_match or department_match:
            filtered_employees.append(employee)

    return render_template(
        "partials/employees_table.html",
        employees=filtered_employees
    )
```

### 33.2 Updated search input (templates/index.html)

Changed `hx-get` and `hx-target` to point at the employee table container:

```html
<input
    type="text"
    name="query"
    placeholder="Search employees..."
    hx-get="/employees"
    hx-trigger="keyup changed delay:500ms"
    hx-target="#employee-table-container"
    hx-indicator="#loading"
    hx-swap="innerHTML">
```

Removed the now-redundant `<div id="search-results"></div>`.

### 33.3 Updated employee table container (templates/index.html)

Added `id="employee-table-container"` so the search input can target it:

```html
<div
    id="employee-table-container"
    hx-get="/employees"
    hx-trigger="load, employee-added from:body"
    hx-target="this">
    Loading employees...
</div>
```

### 33.4 Behaviour

- Table auto-loads on page open.
- Typing in the search box sends `/employees?query=...` and replaces the table contents live.
- Adding an employee fires `employee-added` and the table refreshes automatically.
- Single unified component owns display, filtering, and updates.

### What you learned
- Component-driven filtering
- Unified reactive rendering
- Live table updates with server-side search
- Single source of UI truth
- Real dashboard-style HTMX architecture

---

## 34) Add Sorting to the Employee Table

### Goal
Make column headers clickable so the table reorders dynamically — server-side, no JavaScript.

### 34.1 Updated /employees route (routes/main_routes.py)

Added `sort` parameter, sorting logic, and passed both `sort` and `query` to the template:

```python
@main.route("/employees")
def get_employees():
    query = request.args.get("query", "").lower()
    sort = request.args.get("sort", "id")

    filtered_employees = []
    for employee in employees:
        name_match = query in employee["name"].lower()
        department_match = query in employee["department"].lower()
        if name_match or department_match:
            filtered_employees.append(employee)

    filtered_employees.sort(key=lambda employee: employee[sort])

    return render_template(
        "partials/employees_table.html",
        employees=filtered_employees,
        sort=sort,
        query=query
    )
```

`filtered_employees.sort(key=lambda employee: employee[sort])` dynamically sorts by `id`, `name`, or `department` based on the query parameter.

Passing `sort` and `query` back to the template preserves state across interactions.

### 34.2 Updated table headers (templates/partials/employees_table.html)

Each header is now a clickable HTMX link that preserves the current search query:

```html
<th>
    <a hx-get="/employees?query={{ query }}&sort=id"
       hx-target="#employee-table-container">ID</a>
</th>
<th>
    <a hx-get="/employees?query={{ query }}&sort=name"
       hx-target="#employee-table-container">Name</a>
</th>
<th>
    <a hx-get="/employees?query={{ query }}&sort=department"
       hx-target="#employee-table-container">Department</a>
</th>
```

### 34.3 Test cases

- Click **Name** → table sorts alphabetically by name.
- Click **Department** → table sorts by department.
- Click **ID** → table returns to insertion order.
- Type `IT` then click **Name** → filtered results sort by name, query preserved.

DevTools shows requests like `/employees?query=it&sort=name`.

### Architectural note
The server owns sorting state, filter state, and rendering. The frontend has no sort logic — only declarative HTMX attributes.

### What you learned
- Reactive sorting with query parameters
- Stateful HTMX requests (preserving query across interactions)
- Server-side ordering
- Dynamic table controls
- Enterprise dashboard architecture pattern

---

## 35) Add Pagination to the Employee Table

### Goal
Limit table rows per page and allow navigation between pages, preserving search and sort state.

### 35.1 Expanded mock data (data/mock.py)

Added 7 more employees (ids 6–12) so pagination is meaningful:

```python
{"id": 6, "name": "Frank", "department": "Security"},
{"id": 7, "name": "Grace", "department": "IT"},
{"id": 8, "name": "Helen", "department": "Finance"},
{"id": 9, "name": "Ian", "department": "HR"},
{"id": 10, "name": "Jack", "department": "Marketing"},
{"id": 11, "name": "Karen", "department": "IT"},
{"id": 12, "name": "Leo", "department": "Security"}
```

### 35.2 Updated /employees route (routes/main_routes.py)

Added `page` parameter, slicing logic, and `total_pages` calculation:

```python
page = int(request.args.get("page", 1))
per_page = 5

start = (page - 1) * per_page
end = start + per_page
paginated_employees = filtered_employees[start:end]
total_pages = (len(filtered_employees) + per_page - 1) // per_page
```

`(len + per_page - 1) // per_page` is integer ceiling division — ensures a partial last page is counted.

Template call updated to pass `page` and `total_pages`:

```python
return render_template(
    "partials/employees_table.html",
    employees=paginated_employees,
    sort=sort,
    query=query,
    page=page,
    total_pages=total_pages
)
```

### 35.3 Added pagination controls (templates/partials/employees_table.html)

Navigation buttons appear below the table and preserve current query and sort:

```html
<div style="margin-top:20px;">

{% if page > 1 %}
<button hx-get="/employees?query={{ query }}&sort={{ sort }}&page={{ page - 1 }}"
        hx-target="#employee-table-container">Previous</button>
{% endif %}

<span>Page {{ page }} of {{ total_pages }}</span>

{% if page < total_pages %}
<button hx-get="/employees?query={{ query }}&sort={{ sort }}&page={{ page + 1 }}"
        hx-target="#employee-table-container">Next</button>
{% endif %}

</div>
```

### 35.4 Test cases

- Default load → 5 rows, page 1 of 3, Next button visible.
- Click **Next** → page 2, Previous and Next both visible.
- Search `IT` → 4 results across pages, navigation adjusts.
- Sort by **Name** then page → sort preserved across pages.

DevTools shows requests like `/employees?query=it&sort=name&page=2`.

### Architectural note
The server slices, sorts, and filters before rendering. The frontend receives only the current page as ready HTML — no full dataset shipped to the browser.

### What you learned
- Server-side pagination
- Integer ceiling division for total pages
- State-preserving navigation (query + sort + page)
- Reactive page controls with HTMX
- Scalable table architecture

---

## 36) Add Flash Messages for Global User Feedback

### Goal
Show a success notification when an employee is added, rendered in a global reactive region — no page refresh.

### 36.1 Updated imports (routes/main_routes.py)

```python
from flask import Blueprint, render_template, request, flash, get_flashed_messages
```

### 36.2 Added secret key (app.py)

```python
app.secret_key = "super-secret-key"
```

Flask flash messaging uses the session, which requires a secret key.

### 36.3 Added /messages route (routes/main_routes.py)

```python
@main.route("/messages")
def messages():
    return render_template("partials/messages.html")
```

### 36.4 Created messages partial (templates/partials/messages.html)

```html
{% with messages = get_flashed_messages() %}
    {% if messages %}
        {% for message in messages %}
            <div class="message">{{ message }}</div>
        {% endfor %}
    {% endif %}
{% endwith %}
```

`get_flashed_messages()` retrieves and clears stored messages in one call — messages disappear after first render.

### 36.5 Added messages container to index.html

Placed at the top of `<body>`:

```html
<div
    id="messages"
    hx-get="/messages"
    hx-trigger="load, refresh-messages from:body"
    hx-target="this">
</div>
```

Listens for the custom `refresh-messages` event fired by the server response header.

### 36.6 Updated add_employee route

Added `flash()` call and extended `HX-Trigger` to fire two events:

```python
flash(f"Employee {name} added successfully.")

return response, 200, {
    "HX-Trigger": "employee-added, refresh-messages"
}
```

One POST now triggers both a table refresh and a notification refresh.

### 36.7 Added CSS (static/style.css)

```css
.message {
    background-color: #d4edda;
    color: #155724;
    padding: 12px;
    margin-bottom: 15px;
    border-radius: 5px;
}
```

### 36.8 Test

Add an employee → green success message appears at top, table updates — no page refresh.

### What you learned
- Flask `flash()` and `get_flashed_messages()`
- Session-backed temporary notifications
- Global reactive UI regions
- Multi-component synchronization via `HX-Trigger`
- Event-driven UX architecture

---

## 38) Prevent Duplicate Employees + Show Flash Message

### Goal
Reject duplicate employee names server-side and show a flash message — table unchanged on duplicate attempt.

### 38.1 Updated add_employee route (routes/main_routes.py)

Added duplicate check immediately after reading form data:

```python
existing_employee = next(
    (
        employee
        for employee in employees
        if employee["name"].lower() == name.lower()
    ),
    None
)

if existing_employee:
    flash(f"Employee '{name}' already exists.")
    return "", 200, {
        "HX-Trigger": "refresh-messages"
    }
```

If a duplicate is found:
- Employee is **not** added.
- Flash message is stored.
- Only `refresh-messages` fires — table stays unchanged.

If no duplicate, normal flow continues: employee added, table and messages both refresh.

### 38.2 Logic flow

```
POST /add-employee
  → duplicate found?
      YES → flash warning, fire refresh-messages only
      NO  → append employee, flash success, fire employee-added + refresh-messages
```

### 38.3 Test cases

| Action               | Expected result                          |
|----------------------|------------------------------------------|
| Add "Alice" again    | Flash: "Employee 'Alice' already exists." — table unchanged |
| Add "alice" (lower)  | Same — case-insensitive match            |
| Add "Zara" (new)     | Flash: "Employee Zara added successfully." — table updates |

### Architectural note
Validation lives entirely on the server. The frontend receives only HTML feedback — no client-side duplicate checking required.

### What you learned
- Server-side validation architecture
- Case-insensitive duplicate detection with `next()` + generator
- Conditional reactive responses (different `HX-Trigger` per outcome)
- Business rule enforcement in Flask routes
- Backend-driven feedback for invalid input

---

## 39) Clear the Form Automatically After Successful Submission

### Goal
Clear the add-employee form automatically after a successful submission, so the UI is immediately ready for the next entry.

### 39.1 Confirmed form id in templates/index.html

The form already has:

```html
<form
    id="employee-form"
    hx-post="/add-employee"
    hx-target="#form-result">
```

### 39.2 Added event listener script in templates/index.html

Inserted before `</body>`:

```html
<script>
document.body.addEventListener("employee-added", function () {
    document.getElementById("employee-form").reset();
});
</script>
```

This listens for the `employee-added` custom event (already emitted by the backend) and calls `.reset()` on the form.

### 39.3 Behavior

After successful add:
- employee is saved
- flash message appears
- table refreshes
- form fields clear automatically

No page refresh is required.

### Architectural note
This is minimal, intentional JavaScript. The backend remains the source of truth by emitting events; the frontend only reacts to those events.

### What you learned
- HTMX custom event handling in plain JavaScript
- Form reset automation with `.reset()`
- Backend-triggered client behavior
- Minimal-JS enhancement pattern in HTMX apps
- Event-driven UX flow

---

## 40) Add Auto-Dismissing Flash Messages

### Goal
Make flash messages disappear automatically after a short delay to reduce UI clutter.

### 40.1 Updated messages partial (templates/partials/messages.html)

Message container class updated from:

```html
<div class="message">
```

to:

```html
<div class="message auto-dismiss">
```

`auto-dismiss` is used by JavaScript to target removable notifications.

### 40.2 Updated script in templates/index.html

Added an HTMX lifecycle listener:

```html
document.body.addEventListener("htmx:afterSwap", function () {
    const messages = document.querySelectorAll(".auto-dismiss");
    messages.forEach(function (message) {
        setTimeout(function () {
            message.remove();
        }, 3000);
    });
});
```

How it works:
- HTMX swaps new message HTML into the page.
- `htmx:afterSwap` fires.
- Each `.auto-dismiss` message is removed after 3 seconds.

### 40.3 Test

Add an employee:
- message appears
- stays visible briefly
- disappears automatically (~3 seconds)

No page refresh required.

### What you learned
- HTMX lifecycle events (`htmx:afterSwap`)
- Timed DOM cleanup for notifications
- Auto-dismiss UX pattern
- Lightweight JS enhancements with HTMX

---

## 41) Add Polling with Automatic Table Refresh

### Goal
Keep the employee table synchronized by auto-refreshing at a fixed interval.

### 41.1 Updated employee table container (templates/index.html)

Changed trigger from:

```html
hx-trigger="load, employee-added from:body"
```

to:

```html
hx-trigger="load, every 5s, employee-added from:body"
```

### 41.2 Behavior

- Table loads on initial page render.
- Table refreshes every 5 seconds automatically.
- Table also refreshes immediately on `employee-added` event.

No manual action or page refresh is required.

### 41.3 Operational note

Polling improves synchronization but adds recurring server requests. Choose interval based on context (`5s`, `10s`, `30s`, etc.) to balance freshness and load.

### What you learned
- HTMX polling with `every 5s`
- Periodic trigger-based synchronization
- Live dashboard behavior without custom timer code
- Simple server-driven refresh architecture

---

## 42) Add Modal Windows for Employee Details

### Goal
Open employee details inside a server-rendered modal overlay using HTMX partial swaps.

### 42.1 Added modal routes (routes/main_routes.py)

New routes:

```python
@main.route("/employee-details/<int:id>")
def employee_details(id):
    ...
    return render_template("partials/employee_details_modal.html", employee=employee)


@main.route("/close-modal")
def close_modal():
    return ""
```

`/employee-details/<id>` renders modal HTML. `/close-modal` clears the modal container.

### 42.2 Added modal partial (templates/partials/employee_details_modal.html)

Created a modal overlay/card partial that shows:
- ID
- Name
- Department

Includes a **Close** button that targets `#modal` and swaps empty HTML via `/close-modal`.

### 42.3 Added View action in table rows (templates/partials/employee_row.html)

Added button:

```html
<button
    hx-get="/employee-details/{{ employee.id }}"
    hx-target="#modal"
    hx-swap="innerHTML">
    View
</button>
```

This opens the modal without page refresh.

### 42.4 Added modal mount point (templates/index.html)

Added container:

```html
<div id="modal"></div>
```

All modal content is dynamically injected into this region.

### 42.5 Added modal styles (static/style.css)

Added:
- `.modal-overlay`
- `.modal-card`
- `.modal-actions`

for centered overlay rendering and clean modal presentation.

### 42.6 Test

1. Load employee table.
2. Click **View** on any row.
3. Modal appears with employee details.
4. Click **Close**.
5. Modal disappears without refreshing the page.

### What you learned
- Modal rendering with HTMX partials
- Targeted overlay updates via `hx-target`
- Server-driven detail views
- Reusable modal mount pattern

---

## 43+) Next Steps Sequence (Planned)

Per your request, we are moving step-by-step and some steps may remain planned-only.

- **43)** Real Database Integration (SQLite + SQLAlchemy) — see full instructions below
- **44)** Form Validation System — planned (after DB model exists)

---

## 43) Real Database Integration (SQLite + SQLAlchemy)

> **Not yet implemented** — instructions below describe the full migration path when a database is available.

### Goal
Replace the in-memory `employees` list in `data/mock.py` with a real SQLite database managed by Flask-SQLAlchemy.

---

### 43.1 Install dependencies

```bash
source venv/bin/activate
pip install flask-sqlalchemy
pip freeze > requirements.txt
```

---

### 43.2 Create database configuration (db.py)

Create `db.py` in the project root:

```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
```

---

### 43.3 Define Employee model (models/employee.py)

Create folder and file `models/employee.py`:

```python
from db import db

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "department": self.department
        }
```

---

### 43.4 Update app.py

Wire the database to the Flask app:

```python
from flask import Flask
from db import db
from routes.main_routes import main

app = Flask(__name__)
app.secret_key = "super-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///employees.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(main)

if __name__ == "__main__":
    app.run(debug=True)
```

`db.create_all()` creates tables automatically on first startup.

---

### 43.5 Update routes/main_routes.py imports

Replace:

```python
from data.mock import employees
```

With:

```python
from db import db
from models.employee import Employee
```

---

### 43.6 Migrate route operations

Replace in-memory list operations with SQLAlchemy queries:

#### GET /employees (list with filter + sort + paginate)

```python
query_str = request.args.get("query", "").lower()
sort = request.args.get("sort", "id")
page = int(request.args.get("page", 1))
per_page = 5

sort_column = getattr(Employee, sort, Employee.id)
results = Employee.query.filter(
    db.or_(
        Employee.name.ilike(f"%{query_str}%"),
        Employee.department.ilike(f"%{query_str}%")
    )
).order_by(sort_column).paginate(page=page, per_page=per_page, error_out=False)

employees = [e.to_dict() for e in results.items]
total_pages = results.pages
```

#### POST /add-employee

```python
existing = Employee.query.filter(
    db.func.lower(Employee.name) == name.lower()
).first()

if not existing:
    db.session.add(Employee(name=name, department=department))
    db.session.commit()
```

#### PUT /update-employee/<id>

```python
employee = Employee.query.get_or_404(id)
employee.name = request.form.get("name")
employee.department = request.form.get("department")
db.session.commit()
```

#### DELETE /delete-employee/<id>

```python
employee = Employee.query.get_or_404(id)
db.session.delete(employee)
db.session.commit()
```

---

### 43.7 Seed initial data (optional)

After `db.create_all()` in `app.py`:

```python
with app.app_context():
    db.create_all()
    if Employee.query.count() == 0:
        seed = [
            Employee(name="Alice", department="IT"),
            Employee(name="Bob", department="HR"),
            Employee(name="Charlie", department="Finance"),
            Employee(name="David", department="IT"),
            Employee(name="Emma", department="Marketing"),
        ]
        db.session.bulk_save_objects(seed)
        db.session.commit()
```

---

### 43.8 Updated project structure after migration

```
htmx-flask-learning/
├── app.py
├── db.py
├── requirements.txt
├── data/
│   └── mock.py           ← no longer imported, kept for reference
├── models/
│   └── employee.py       ← SQLAlchemy Employee model
├── routes/
│   └── main_routes.py
├── templates/
│   ├── index.html
│   └── partials/
├── static/
│   └── style.css
└── instance/
    └── employees.db      ← auto-created by SQLite
```

---

### What you will learn
- Flask-SQLAlchemy setup and configuration
- ORM model definition and relationships
- Database-backed CRUD operations
- SQLAlchemy queries (filter, order_by, paginate, ilike)
- Session commit/rollback pattern
- Seeding initial data programmatically
- Migrating from in-memory mock data to persistent storage

---

## 44) Form Validation System

> **Not yet implemented** — instructions below describe the full server-side validation pattern to add once the DB step is ready (or directly on top of mock data).

### Goal
Add field-level validation to the Add Employee form: required fields, minimum length, allowed department values, and inline error feedback — all server-side, rendered as HTMX partials.

---

### 44.1 Create validation helper (utils/validators.py)

Create folder and file `utils/validators.py`:

```python
VALID_DEPARTMENTS = {"IT", "HR", "Finance", "Marketing", "Security"}

def validate_employee(name, department):
    errors = []

    if not name or len(name.strip()) < 2:
        errors.append("Name must be at least 2 characters.")

    if not department or department.strip() not in VALID_DEPARTMENTS:
        errors.append(
            f"Department must be one of: {', '.join(sorted(VALID_DEPARTMENTS))}."
        )

    return errors
```

Returns a list of error strings. Empty list means valid.

---

### 44.2 Create validation error partial (templates/partials/form_errors.html)

```html
{% if errors %}
<div class="form-errors">
    <ul>
    {% for error in errors %}
        <li>{{ error }}</li>
    {% endfor %}
    </ul>
</div>
{% endif %}
```

This partial is injected into `#form-result` when validation fails.

---

### 44.3 Update add_employee route (routes/main_routes.py)

Import validator:

```python
from utils.validators import validate_employee
```

Add validation before duplicate check:

```python
@main.route("/add-employee", methods=["POST"])
def add_employee():
    name = request.form.get("name", "").strip()
    department = request.form.get("department", "").strip()

    errors = validate_employee(name, department)
    if errors:
        return render_template("partials/form_errors.html", errors=errors), 200

    # existing duplicate check follows...
```

If validation fails:
- Returns rendered error partial into `#form-result`.
- No employee is added.
- No flash message fires.
- Table is unaffected.

---

### 44.4 Add error styles (static/style.css)

```css
.form-errors {
    background-color: #f8d7da;
    color: #721c24;
    padding: 12px;
    margin-bottom: 15px;
    border-radius: 5px;
}

.form-errors ul {
    margin: 0;
    padding-left: 18px;
}
```

---

### 44.5 Full validation + duplicate check flow

```
POST /add-employee
  → validate fields
      INVALID → render form_errors.html into #form-result, stop
  → check duplicate
      DUPLICATE → flash warning, fire refresh-messages, stop
  → add employee
      SUCCESS → flash success, fire employee-added + refresh-messages
```

---

### 44.6 Test cases

| Input                         | Expected result                              |
|-------------------------------|----------------------------------------------|
| Name: `A`, Dept: `IT`         | Error: name too short                        |
| Name: `Alice`, Dept: `Foo`    | Error: invalid department                    |
| Name: ``, Dept: ``            | Both errors rendered                         |
| Name: `Alice`, Dept: `IT`     | Duplicate warning (Alice already exists)     |
| Name: `Zara`, Dept: `Finance` | Success — employee added                     |

---

### What you will learn
- Server-side field validation pattern
- Reusable validator module
- Inline error rendering with HTMX partials
- Layered validation (field checks → business rules → persistence)
- Separation of validation logic from route logic

---

## 45) Authentication (Session-Based Login)

> **Not yet implemented** — instructions below describe the full session-based authentication pattern for this Flask + HTMX app.

### Goal
Protect the employee dashboard behind a login page. Unauthenticated users are redirected to `/login`. Authenticated users can log out. No third-party auth library required — pure Flask sessions.

---

### 45.1 Add a user store (data/mock.py)

Append a simple user dict alongside employees:

```python
users = {
    "admin": "password123"
}
```

In production this would be a DB table with hashed passwords (e.g. `werkzeug.security.generate_password_hash`).

---

### 45.2 Create login template (templates/login.html)

```html
<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
<div class="login-card">
    <h2>Login</h2>

    {% with messages = get_flashed_messages() %}
        {% if messages %}
            {% for message in messages %}
                <div class="message error">{{ message }}</div>
            {% endfor %}
        {% endif %}
    {% endwith %}

    <form method="POST" action="/login">
        <input type="text" name="username" placeholder="Username" required>
        <input type="password" name="password" placeholder="Password" required>
        <button type="submit">Login</button>
    </form>
</div>
</body>
</html>
```

Standard HTML form — no HTMX needed for login (full-page navigation is fine here).

---

### 45.3 Add auth routes (routes/main_routes.py)

Add imports:

```python
from flask import session, redirect, url_for
from data.mock import employees, users
from werkzeug.security import check_password_hash
```

Add login/logout routes:

```python
@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if username in users and users[username] == password:
            session["user"] = username
            return redirect(url_for("main.index"))

        flash("Invalid username or password.")
        return redirect(url_for("main.login"))

    return render_template("login.html")


@main.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("main.login"))
```

---

### 45.4 Create login_required decorator (utils/auth.py)

Create `utils/auth.py`:

```python
from functools import wraps
from flask import session, redirect, url_for

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("main.login"))
        return f(*args, **kwargs)
    return decorated
```

---

### 45.5 Protect the index route

In `routes/main_routes.py`, import and apply the decorator:

```python
from utils.auth import login_required

@main.route("/")
@login_required
def index():
    return render_template("index.html")
```

Apply `@login_required` to any route that should be protected.

---

### 45.6 Add logout button (templates/index.html)

Add to the top of the page alongside the heading:

```html
<div style="display:flex; justify-content:space-between; align-items:center;">
    <h1>Employee Dashboard</h1>
    <a href="/logout"><button>Logout</button></a>
</div>
```

---

### 45.7 Add login card styles (static/style.css)

```css
.login-card {
    max-width: 360px;
    margin: 80px auto;
    padding: 32px;
    border: 1px solid #dee2e6;
    border-radius: 8px;
    background: #fff;
}

.login-card h2 {
    margin-bottom: 20px;
}

.login-card input {
    display: block;
    width: 100%;
    margin-bottom: 12px;
}

.message.error {
    background-color: #f8d7da;
    color: #721c24;
}
```

---

### 45.8 Authentication flow

```
GET /
  → session has "user"?
      NO  → redirect to /login
      YES → render dashboard

POST /login
  → credentials valid?
      NO  → flash error, redirect to /login
      YES → session["user"] = username, redirect to /

GET /logout
  → session.pop("user")
  → redirect to /login
```

---

### 45.9 Test cases

| Action                        | Expected result                     |
|-------------------------------|-------------------------------------|
| Visit `/` unauthenticated     | Redirected to `/login`              |
| Login with wrong password     | Flash: "Invalid username or password." |
| Login with `admin/password123`| Redirected to dashboard             |
| Click Logout                  | Redirected to `/login`              |
| Visit `/` after logout        | Redirected to `/login`              |

---

### What you will learn
- Flask `session` for stateful auth
- Login/logout route patterns
- Custom `login_required` decorator with `functools.wraps`
- Protecting routes declaratively
- Redirect flow for unauthenticated access
- Separating auth logic into its own utility module

---

## 46) File Uploads

### Goal
Allow users to upload files from the dashboard. The file is sent via an HTMX form, validated server-side (type + size), saved to disk, and the result is rendered inline — no page refresh.

---

### 46.1 Configure upload folder (app.py)

```python
import os

app.config["UPLOAD_FOLDER"] = os.path.join(os.path.dirname(__file__), "uploads")
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024  # 2 MB limit
```

`MAX_CONTENT_LENGTH` causes Flask to automatically reject oversized uploads with a 413 error.

---

### 46.2 Create uploads/ directory

```bash
mkdir uploads
```

Files will be saved here server-side.

---

### 46.3 Add upload helpers and route (routes/main_routes.py)

Imports added:

```python
import os
from werkzeug.utils import secure_filename
from flask import current_app

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "pdf", "txt", "csv"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
```

Route:

```python
@main.route("/upload-file", methods=["POST"])
@login_required
def upload_file():
    file = request.files.get("file")

    if not file or file.filename == "":
        return render_template("partials/upload_result.html", error="No file selected.")

    if not allowed_file(file.filename):
        return render_template("partials/upload_result.html",
            error=f"File type not allowed. Allowed: {', '.join(sorted(ALLOWED_EXTENSIONS))}.")

    filename = secure_filename(file.filename)
    save_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    file.save(save_path)

    return render_template("partials/upload_result.html", filename=filename)
```

`secure_filename` sanitizes the filename to prevent path traversal attacks.

---

### 46.4 Create upload result partial (templates/partials/upload_result.html)

```html
{% if error %}
<div class="upload-result error">{{ error }}</div>
{% elif filename %}
<div class="upload-result success">
    <strong>Uploaded:</strong> {{ filename }}
</div>
{% endif %}
```

---

### 46.5 Add upload form to dashboard (templates/index.html)

```html
<h2>File Upload</h2>

<form
    hx-post="/upload-file"
    hx-target="#upload-result"
    hx-encoding="multipart/form-data">
    <input type="file" name="file" accept=".png,.jpg,.jpeg,.gif,.pdf,.txt,.csv">
    <button type="submit">Upload</button>
</form>

<div id="upload-result"></div>
```

`hx-encoding="multipart/form-data"` is required for file uploads with HTMX.

---

### 46.6 Add upload CSS (static/style.css)

```css
.upload-result {
    padding: 10px 14px;
    margin-top: 10px;
    border-radius: 5px;
}

.upload-result.success { background-color: #d4edda; color: #155724; }
.upload-result.error   { background-color: #f8d7da; color: #721c24; }
```

---

### 46.7 Test cases

| Action                          | Expected result                          |
|---------------------------------|------------------------------------------|
| Upload a `.txt` file            | Success: "Uploaded: filename.txt"        |
| Submit with no file selected    | Error: "No file selected."               |
| Upload a `.exe` file            | Error: "File type not allowed."          |
| Upload file > 2 MB              | Flask returns 413 Request Entity Too Large |

---

### What you learned
- `hx-encoding="multipart/form-data"` for HTMX file uploads
- `secure_filename` for path traversal prevention
- Server-side file type whitelisting
- `MAX_CONTENT_LENGTH` for size enforcement
- `current_app` for accessing config inside Blueprints
- Inline upload feedback with HTMX partials

---

---

## 47) Dockerize the App

> **Instructions only** — no implementation required.

### Goal
Package the Flask application into a Docker container so it runs identically in any environment.

---

### 47.1 Install gunicorn

```bash
source venv/bin/activate
pip install gunicorn
pip freeze > requirements.txt
```

Gunicorn is the production WSGI server used inside the container — Flask's built-in dev server is not suitable for production.

---

### 47.2 Create Dockerfile

Create `Dockerfile` in the project root:

```dockerfile
# Use official slim Python image
FROM python:3.12-slim

# Set working directory inside container
WORKDIR /app

# Copy dependency list first (layer caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create uploads directory
RUN mkdir -p uploads

# Expose the port gunicorn will listen on
EXPOSE 8000

# Run with gunicorn — 2 worker processes
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "app:app"]
```

Layer ordering matters: copying `requirements.txt` first means Docker reuses the pip install cache unless dependencies change.

---

### 47.3 Create .dockerignore

Create `.dockerignore` in the project root:

```
venv/
__pycache__/
*.pyc
*.pyo
.env
.git
uploads/
instance/
*.db
```

Prevents large or sensitive files from being copied into the image.

---

### 47.4 Create docker-compose.yml

Create `docker-compose.yml` for easier local development:

```yaml
version: "3.9"

services:
  web:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./uploads:/app/uploads
    environment:
      - FLASK_ENV=production
```

The `volumes` mount keeps uploaded files on the host, not lost when the container restarts.

---

### 47.5 Build and run

```bash
# Build the image
docker build -t htmx-flask-app .

# Run the container
docker run -p 8000:8000 htmx-flask-app

# Or with docker-compose
docker-compose up --build
```

Visit `http://localhost:8000` to verify.

---

### 47.6 Updated project structure

```
htmx-flask-learning/
├── app.py
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── requirements.txt
├── data/
├── routes/
├── templates/
├── static/
├── uploads/
└── venv/               ← excluded by .dockerignore
```

---

### What you will learn
- Docker image build with `FROM`, `COPY`, `RUN`, `CMD`
- Layer caching with dependency-first copy
- `.dockerignore` to exclude unnecessary files
- `docker-compose` for multi-container or local dev convenience
- Difference between Flask dev server and gunicorn in production
- Volume mounting for persistent file storage

---

## 48) Deploy to Azure

> **Instructions only** — no implementation required (Azure subscription needed).

### Goal
Deploy the Docker container image to Azure Container Apps — a serverless container platform that handles scaling, HTTPS, and infrastructure automatically.

---

### 48.1 Prerequisites

- Azure account with active subscription
- Azure CLI installed: `az --version`
- Docker installed and running
- App containerized per Step 47

---

### 48.2 Install Azure CLI (if needed)

```bash
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
az login
```

---

### 48.3 Create Azure resources

```bash
# Set variables
RESOURCE_GROUP=htmx-flask-rg
LOCATION=eastus
ACR_NAME=htmxflaskregistry
APP_ENV=htmx-flask-env
APP_NAME=htmx-flask-app

# Create resource group
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create Azure Container Registry
az acr create --resource-group $RESOURCE_GROUP \
              --name $ACR_NAME \
              --sku Basic \
              --admin-enabled true
```

---

### 48.4 Push image to Azure Container Registry

```bash
# Login to ACR
az acr login --name $ACR_NAME

# Tag and push image
docker tag htmx-flask-app $ACR_NAME.azurecr.io/htmx-flask-app:latest
docker push $ACR_NAME.azurecr.io/htmx-flask-app:latest
```

---

### 48.5 Create Container Apps environment and deploy

```bash
# Install Container Apps extension
az extension add --name containerapp

# Create environment
az containerapp env create \
  --name $APP_ENV \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION

# Deploy container
az containerapp create \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --environment $APP_ENV \
  --image $ACR_NAME.azurecr.io/htmx-flask-app:latest \
  --registry-server $ACR_NAME.azurecr.io \
  --target-port 8000 \
  --ingress external \
  --min-replicas 1 \
  --max-replicas 3
```

---

### 48.6 Verify deployment

```bash
az containerapp show \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --query "properties.configuration.ingress.fqdn" \
  --output tsv
```

Returns the public HTTPS URL for your deployed app.

---

### What you will learn
- Azure Container Registry (ACR) for private image hosting
- Azure Container Apps for serverless container hosting
- `az containerapp` CLI commands
- Image tagging and pushing workflow
- External ingress and HTTPS termination on Azure
- Min/max replica scaling configuration

---

## 49) CI/CD with GitHub Actions

> **Instructions only** — no implementation required.

### Goal
Automatically build, test, and deploy the app on every push to `main` using a GitHub Actions workflow.

---

### 49.1 Create workflow file

Create `.github/workflows/deploy.yml`:

```yaml
name: Build and Deploy

on:
  push:
    branches:
      - main

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run tests
        run: |
          python -m pytest tests/ --tb=short || echo "No tests found"

      - name: Log in to Azure Container Registry
        uses: azure/docker-login@v1
        with:
          login-server: ${{ secrets.ACR_LOGIN_SERVER }}
          username: ${{ secrets.ACR_USERNAME }}
          password: ${{ secrets.ACR_PASSWORD }}

      - name: Build and push Docker image
        run: |
          docker build -t ${{ secrets.ACR_LOGIN_SERVER }}/htmx-flask-app:${{ github.sha }} .
          docker push ${{ secrets.ACR_LOGIN_SERVER }}/htmx-flask-app:${{ github.sha }}

      - name: Deploy to Azure Container Apps
        uses: azure/CLI@v2
        with:
          azcliversion: latest
          inlineScript: |
            az containerapp update \
              --name htmx-flask-app \
              --resource-group htmx-flask-rg \
              --image ${{ secrets.ACR_LOGIN_SERVER }}/htmx-flask-app:${{ github.sha }}
```

---

### 49.2 Add GitHub Secrets

In your GitHub repo → **Settings → Secrets and variables → Actions**, add:

| Secret name        | Value                                   |
|--------------------|-----------------------------------------|
| `ACR_LOGIN_SERVER` | `htmxflaskregistry.azurecr.io`          |
| `ACR_USERNAME`     | ACR admin username (from Azure portal)  |
| `ACR_PASSWORD`     | ACR admin password (from Azure portal)  |

---

### 49.3 Workflow flow

```
git push → main
  → checkout code
  → install dependencies
  → run tests
  → build Docker image (tagged with git SHA)
  → push image to ACR
  → update Azure Container App to new image
```

Each deployment is tagged with the exact git commit SHA — making rollbacks trivial.

---

### What you will learn
- GitHub Actions workflow syntax (`on`, `jobs`, `steps`)
- Using `actions/checkout`, `actions/setup-python`
- Docker build + push inside a CI pipeline
- GitHub Secrets for secure credential storage
- Immutable image tags with `github.sha`
- Zero-downtime rolling updates with Azure Container Apps

---

## 50) Production WSGI Server (Gunicorn)

> **Instructions only** — gunicorn is already installed in Step 47. This step explains configuration for production tuning.

### Goal
Replace Flask's built-in dev server with Gunicorn, properly configured for concurrent traffic, timeouts, and logging.

---

### 50.1 Basic gunicorn command

```bash
gunicorn --bind 0.0.0.0:8000 --workers 2 app:app
```

- `--bind 0.0.0.0:8000` — listen on all interfaces, port 8000
- `--workers 2` — 2 parallel worker processes
- `app:app` — module `app.py`, Flask instance named `app`

---

### 50.2 Worker count formula

```
workers = (2 × CPU cores) + 1
```

For a 2-core machine: 5 workers. For a single-core container: 2–3 workers.

---

### 50.3 Create gunicorn.conf.py

Create `gunicorn.conf.py` in the project root:

```python
bind = "0.0.0.0:8000"
workers = 3
timeout = 60
keepalive = 5
accesslog = "-"       # log to stdout
errorlog = "-"        # log to stderr
loglevel = "info"
```

Run with:

```bash
gunicorn -c gunicorn.conf.py app:app
```

---

### 50.4 Update Dockerfile CMD

Replace the inline CMD with the config file:

```dockerfile
CMD ["gunicorn", "-c", "gunicorn.conf.py", "app:app"]
```

---

### 50.5 Comparison: dev server vs gunicorn

| Feature            | Flask dev server        | Gunicorn              |
|--------------------|-------------------------|-----------------------|
| Concurrent requests| Single-threaded         | Multiple workers      |
| Restart on code change | Yes (`debug=True`)  | No (use `--reload`)   |
| HTTPS              | No                      | Via reverse proxy     |
| Production safe    | No                      | Yes                   |

---

### What you will learn
- WSGI protocol and why Flask dev server is not production-ready
- Gunicorn worker model (pre-fork)
- Worker count tuning
- `gunicorn.conf.py` for clean configuration
- Logging to stdout/stderr for container log aggregation

---

## 51) Environment Configuration (.env and config classes)

> **Instructions only** — no implementation required.

### Goal
Move hardcoded values (secret key, upload path, debug flag) out of source code into environment variables, with a Flask config class pattern for different environments (development, production).

---

### 51.1 Install python-dotenv

```bash
pip install python-dotenv
pip freeze > requirements.txt
```

---

### 51.2 Create .env file

Create `.env` in the project root:

```
FLASK_SECRET_KEY=change-me-in-production
FLASK_DEBUG=false
UPLOAD_FOLDER=uploads
MAX_UPLOAD_MB=2
```

Add `.env` to `.gitignore` — never commit secrets.

---

### 51.3 Create config.py

Create `config.py`:

```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "fallback-dev-key")
    UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER", "uploads")
    MAX_CONTENT_LENGTH = int(os.environ.get("MAX_UPLOAD_MB", 2)) * 1024 * 1024

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
```

---

### 51.4 Update app.py

```python
from config import DevelopmentConfig, ProductionConfig
import os

app = Flask(__name__)

env = os.environ.get("FLASK_ENV", "development")
if env == "production":
    app.config.from_object(ProductionConfig)
else:
    app.config.from_object(DevelopmentConfig)
```

---

### 51.5 Add .env to .gitignore

```
.env
venv/
__pycache__/
uploads/
instance/
*.db
```

---

### 51.6 Environment variable flow

```
.env file (local dev)
  → python-dotenv loads into os.environ
  → config.py reads os.environ
  → app.py applies config class
  → routes use current_app.config["KEY"]

Production (Docker / Azure):
  → .env is not committed
  → environment variables set in container / Azure secrets
  → same config.py reads them transparently
```

---

### What you will learn
- `python-dotenv` for local `.env` loading
- Flask config class pattern (`from_object`)
- Environment-specific config (dev vs prod)
- `os.environ.get()` with safe defaults
- Secret management: never commit `.env`, use platform secrets in production
- `current_app.config` access pattern inside Blueprints
