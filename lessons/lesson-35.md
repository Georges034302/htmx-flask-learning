# Lesson 35: Authentication (Session-Based Login)

Included step: 45

## Concept
Authentication (Session-Based Login).

## Step flow

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

