# Lesson 01: Authentication (Session-Based Login)

## Concept
Authentication (Session-Based Login).


## 1. Authentication (Session-Based Login)


### Goal
Protect the employee dashboard behind a login page. Unauthenticated users are redirected to `/login`. Authenticated users can log out. No third-party auth library required — pure Flask sessions.

---

### 1.1 Add a user store (data/mock.py)

Append a simple user dict alongside employees:

```python
users = {
    "admin": "password123"
}
```

In production this would be a DB table with hashed passwords (e.g. `werkzeug.security.generate_password_hash`).

---

### 1.2 Create login template (templates/login.html)

```html
<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/main.css') }}">
</head>
<body>
<div class="panel panel-login">
    <h2>Login</h2>

    {% with messages = get_flashed_messages() %}
        {% if messages %}
            {% for message in messages %}
                <div class="flash flash-error">{{ message }}</div>
            {% endfor %}
        {% endif %}
    {% endwith %}

    <form method="POST" action="/login">
        <input type="text" name="username" placeholder="Username" required>
        <input type="password" name="password" placeholder="Password" required>
        <button type="submit" class="btn btn-primary">Login</button>
    </form>
</div>
</body>
</html>
```

Standard HTML form — no HTMX needed for login (full-page navigation is fine here).

---

### 1.3 Add auth routes (routes/main_routes.py)

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

### 1.4 Create login_required decorator (utils/auth.py)

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

### 1.5 Protect the index route

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

### 1.6 Add logout button (templates/index.html)

Add to the top of the page alongside the heading:

```html
<div class="page-header">
    <h1>Employee Dashboard</h1>
    <a href="/logout" class="btn btn-ghost">Logout</a>
</div>
```

---

### 1.7 CSS — static/css/main.css

The login page uses `.panel` for the card container and `.flash.flash-error` for authentication error messages — both already defined in `main.css`. No custom CSS is needed.

```html
<!-- Login card wrapper using existing panel classes -->
<div class="panel panel-login">
```

Buttons on the login form use `.btn .btn-primary` from `main.css`.

---

### 1.8 Authentication flow

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

### 1.9 Test cases

| Action                        | Expected result                     |
|-------------------------------|-------------------------------------|
| Visit `/` unauthenticated     | Redirected to `/login`              |
| Login with wrong password     | Flash: "Invalid username or password." |
| Login with `admin/password123`| Redirected to dashboard             |
| Click Logout                  | Redirected to `/login`              |
| Visit `/` after logout        | Redirected to `/login`              |

---

