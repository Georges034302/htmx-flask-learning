# Lesson 01: Add Flash Messages for Global User Feedback

## Concept
Add Flash Messages for Global User Feedback.


## 1. Add Flash Messages for Global User Feedback

### Goal
Show a success notification when an employee is added, rendered in a global reactive region — no page refresh.

### 1.1 Updated imports (routes/main_routes.py)

```python
from flask import Blueprint, render_template, request, flash, get_flashed_messages
```

### 1.2 Added secret key (app.py)

```python
app.secret_key = "super-secret-key"
```

Flask flash messaging uses the session, which requires a secret key.

### 1.3 Added /messages route (routes/main_routes.py)

```python
@main.route("/messages")
def messages():
    return render_template("partials/messages.html")
```

### 1.4 Created messages partial (templates/partials/messages.html)

```html
{% with messages = get_flashed_messages(with_categories=True) %}
    {% if messages %}
        {% for category, message in messages %}
            <div class="flash flash-{{ category }}">{{ message }}</div>
        {% endfor %}
    {% endif %}
{% endwith %}
```

`get_flashed_messages()` retrieves and clears stored messages in one call — messages disappear after first render.

### 1.5 Added messages container to index.html

Current placement is beside the Employee Table title inside `.table-header`:

```html
<div
    id="messages"
    hx-get="/messages"
    hx-trigger="load, refresh-messages from:body"
    hx-target="this">
</div>
```

Listens for the custom `refresh-messages` event fired by the server response header.

### 1.6 Updated add_employee route

Added `flash()` call and extended `HX-Trigger` to fire two events:

```python
flash(f"Employee {name} added successfully.")

return response, 200, {
    "HX-Trigger": "employee-added, refresh-messages"
}
```

One POST now triggers both a table refresh and a notification refresh.

### 1.7 CSS — static/css/main.css

`main.css` already provides all flash message styles. No custom CSS needed.

The relevant classes are:

| Class | Colour | Use |
|---|---|---|
| `.flash` | neutral | base style applied to every message |
| `.flash-success` | green | employee added, record saved |
| `.flash-error` | red | validation failure, not found |
| `.flash-warning` | amber | duplicate, constraint warning |
| `.flash-info` | blue | informational notices |

The template uses `flash-{{ category }}` so Flask category strings (`success`, `error`, `warning`, `info`) map directly to the CSS class.

### 1.8 Test

Add an employee → success message appears next to the table title, and table updates — no page refresh.

