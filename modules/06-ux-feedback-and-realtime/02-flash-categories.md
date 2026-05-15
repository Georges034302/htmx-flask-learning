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
{% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
        {% for category, message in messages %}
            <div class="message {{ category }} auto-dismiss">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
{% endwith %}
```

`{{ category }}` is rendered as a CSS class, so `flash("...", "success")` produces `class="message success auto-dismiss"`.

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

### 1.3 Update CSS (static/style.css)

Replace the single hardcoded green `.message` rule with a neutral base and three category variants:

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

.message.warning {
    background-color: #fff3cd;
    color: #856404;
}

.message.error {
    background-color: #f8d7da;
    color: #721c24;
}
```

---

### 1.4 Test cases

| Action                        | Expected banner colour |
|-------------------------------|------------------------|
| Add a new employee            | Green (success)        |
| Add a duplicate employee      | Yellow (warning)       |
| Login with wrong password     | Red (error)            |

---

