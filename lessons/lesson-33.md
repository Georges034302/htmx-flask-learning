# Lesson 33: Real Database Integration (SQLite + SQLAlchemy)

Included step: 43

Learning objective:
Master one focused concept from step 43 with precise, sequential execution.

Editor notes:
- Keep the exact sequence from source material.
- Validate behavior at each test checkpoint before continuing.

## Detailed walkthrough

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

### 43.7 Initialize and seed database with SQL script

Use the shared SQL setup file in `data/employee_db_setup.sql`.

Run:

```bash
sqlite3 employees.db < data/employee_db_setup.sql
```

What this script does:
- Creates the `employees` table
- Inserts the starter employee dataset
- Uses `DROP TABLE IF EXISTS employees` to allow reset/re-seed runs during learning

Optional ORM-based seed alternative:
- If you prefer seeding in Python instead of SQL, you can still use the previous `db.session.bulk_save_objects(...)` approach.
- Keep SQL script seeding as the default for this lesson to match repository data assets.

---

### 43.8 Updated project structure after migration

```
htmx-flask-learning/
├── app.py
├── db.py
├── requirements.txt
├── data/
│   ├── employee_db_setup.sql
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
- Seeding initial data with a reusable SQL script
- Migrating from in-memory mock data to persistent storage

---

