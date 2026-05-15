# Lesson 02: Flash Message Categories (success, warning, error)

## Concept
Flash Message Categories (success, warning, error).


## 1. Flash Message Categories (success, warning, error)

### Goal
Extend the flash message system to support categories so each type of notification — success, warning, error — renders with a distinct colour, giving users clear visual feedback about the nature of each message.

### 1.1 Update messages partial (templates/partials/messages.html)

Change `get_flashed_messages()` to `get_flashed_messages(with_categories=true)`.

The return value changes from a list of strings to a list of `(category, message)` tuples.

```html
{% with messages = get_flashed_messages(with_categories=True) %}
    {% if messages %}
        {% for category, message in messages %}
            <div class="flash flash-{{ category }} auto-dismiss">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
{% endwith %}
```

`{{ category }}` is appended as a modifier class, so `flash("...", "success")` produces `class="flash flash-success auto-dismiss"`. All colour styles come from `static/css/main.css` — no custom CSS required.

---

### 1.2 Add categories to flash() calls (routes/main_routes.py)

Update every `flash()` call to include an explicit category:

```python
# Successful login redirected — no flash needed
# Login failure:
flash("Invalid username or password.", "error")

# Duplicate employee:
flash(f"Employee '{name}' already exists.", "warning")

# Successful add:
flash(f"Employee {name} added successfully.", "success")
```

Flask's built-in default category is `"message"` — using named categories lets CSS target each one independently.

---

### 1.3 CSS — static/css/main.css

`main.css` already defines all three category variants. No custom CSS is needed.

| Flask category | CSS class applied | Result |
|---|---|---|
| `"success"` | `.flash-success` | Green background, dark green text |
| `"warning"` | `.flash-warning` | Amber background, dark amber text |
| `"error"` | `.flash-error` | Red background, dark red text |
| `"info"` | `.flash-info` | Blue background, dark blue text |

Each variant uses CSS custom properties (`--success-bg`, `--error-bg`, etc.) so dark-theme support is automatic via `[data-theme="dark"]` in `main.css`.

---

### 1.4 Test cases

| Action                        | Expected banner colour |
|-------------------------------|------------------------|
| Add a new employee            | Green (success)        |
| Add a duplicate employee      | Yellow (warning)       |
| Login with wrong password     | Red (error)            |

---

