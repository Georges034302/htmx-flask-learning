# Lesson 26: Add Flash Messages for Global User Feedback

Included step: 36

Learning objective:
Master one focused concept from step 36 with precise, sequential execution.

Editor notes:
- Keep the exact sequence from source material.
- Validate behavior at each test checkpoint before continuing.

## Detailed walkthrough

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
    padding: 12px;
    margin-bottom: 15px;
    border-radius: 5px;
}

.message.success {
    background-color: #d4edda;
    color: #155724;
}
```

Note:
- Category-specific styles (`.message.warning`, `.message.error`) are added in Lesson 27.

### 36.8 Test

Add an employee → success message appears next to the table title, and table updates — no page refresh.

### What you learned
- Flask `flash()` and `get_flashed_messages()`
- Session-backed temporary notifications
- Global reactive UI regions
- Multi-component synchronization via `HX-Trigger`
- Event-driven UX architecture

---

