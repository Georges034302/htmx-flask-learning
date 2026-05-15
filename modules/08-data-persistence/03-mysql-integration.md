# Lesson 03: MySQL Integration (Switching from SQLite)

## Concept
MySQL Integration (Switching from SQLite).

## 1. MySQL Integration (Switching from SQLite)

### Goal
Switch the Flask-SQLAlchemy database backend from SQLite (development) to MySQL (production) by changing only the connection URI and driver — no model or route code changes required.

> **Prerequisite:** Complete Module 08, Lesson 01 (SQLAlchemy integration) before this lesson. This lesson builds directly on the `db.py`, `models/employee.py`, and `config.py` files created there.

---

### 1.1 Why switch from SQLite to MySQL

| Factor | SQLite | MySQL |
|---|---|---|
| Concurrency | Single writer at a time | Multiple concurrent writers |
| Deployment | File on local disk | Network-accessible server |
| Production use | Not recommended | Standard choice |
| Setup effort | Zero (built into Python) | Requires a running server |

SQLite is correct for development. MySQL (or PostgreSQL) is the standard choice for any production deployment with real traffic.

Flask-SQLAlchemy abstracts the database entirely — the same model, session, and query code works with both. Only the connection URI changes.

---

### 1.2 Install the MySQL driver

SQLAlchemy requires a Python driver to talk to MySQL. The recommended option is **PyMySQL** (pure Python, no system dependencies):

```bash
source venv/bin/activate
pip install pymysql
pip freeze > requirements.txt
```

Alternative drivers:
- `mysqlclient` — C extension, faster but requires system `libmysqlclient-dev`.
- `mysql-connector-python` — official Oracle driver, heavier.

PyMySQL is the simplest choice for development and containerized deployments.

---

### 1.3 Understand the connection URI format

SQLAlchemy connection URI structure:

```
dialect+driver://username:password@host:port/database_name
```

Examples:

```
# SQLite (current — development only)
sqlite:///employees.db

# MySQL with PyMySQL driver
mysql+pymysql://user:password@localhost:3306/employees_db

# MySQL over a Unix socket (common in local installs)
mysql+pymysql://user:password@localhost/employees_db?unix_socket=/var/run/mysqld/mysqld.sock

# MySQL on a remote host (production)
mysql+pymysql://app_user:secure_pass@db.example.com:3306/prod_employees
```

---

### 1.4 Update config.py

Open `config.py` (created in Module 10, Lesson 05).

Update it to select the correct URI based on environment:

```python
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "dev-insecure-key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    # SQLite for local development — zero setup required
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///employees.db"
    )


class ProductionConfig(Config):
    DEBUG = False
    # MySQL for production — read all credentials from environment
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")

    @classmethod
    def validate(cls):
        if not cls.SQLALCHEMY_DATABASE_URI:
            raise RuntimeError(
                "DATABASE_URL environment variable is not set. "
                "Set it before starting the production server."
            )


config_map = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}
```

Key design decisions:
- `DATABASE_URL` is the single environment variable that controls the database.
- Development falls back to SQLite if `DATABASE_URL` is not set.
- Production raises a clear error if `DATABASE_URL` is missing — no silent SQLite fallback in prod.

---

### 1.5 Update .env for local MySQL testing

If you want to test MySQL locally, update `.env`:

```
FLASK_SECRET_KEY=change-me
FLASK_ENV=development
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/employees_db
```

For SQLite (default local setup), leave `DATABASE_URL` unset or comment it out:

```
FLASK_SECRET_KEY=change-me
FLASK_ENV=development
# DATABASE_URL=mysql+pymysql://...
```

---

### 1.6 Update app.py to use the config map

Open `app.py`. Update the config loading to use the environment-aware config:

```python
from flask import Flask
from db import db
from routes.main_routes import main
from config import config_map
import os

app = Flask(__name__)

env = os.environ.get("FLASK_ENV", "development")
app.config.from_object(config_map[env])

db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(main)

if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])
```

`config_map[env]` selects `DevelopmentConfig` or `ProductionConfig` based on the `FLASK_ENV` variable.

---

### 1.7 Create the MySQL database before running

If using MySQL locally, create the database first (SQLAlchemy does not create the database itself, only the tables within it):

```sql
-- Run in your MySQL client
CREATE DATABASE employees_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'app_user'@'localhost' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON employees_db.* TO 'app_user'@'localhost';
FLUSH PRIVILEGES;
```

Then start Flask. `db.create_all()` in `app.py` will create the `employee` table automatically.

---

### 1.8 Verify schema creation

```bash
python app.py
```

Flask startup output should show no errors.

Verify in MySQL:

```sql
USE employees_db;
SHOW TABLES;
-- Expected: employee

DESCRIBE employee;
-- Expected: id (int PK), name (varchar), department (varchar)
```

---

### 1.9 Common issues and fixes

| Issue | Cause | Fix |
|---|---|---|
| `ModuleNotFoundError: No module named 'pymysql'` | Driver not installed | `pip install pymysql` |
| `OperationalError: (1045) Access denied` | Wrong credentials in URI | Check `DATABASE_URL` in `.env` |
| `OperationalError: (1049) Unknown database` | Database not created | Run `CREATE DATABASE employees_db;` manually |
| `OperationalError: (2003) Can't connect` | MySQL server not running | `sudo systemctl start mysql` |
| `UnicodeDecodeError` on insert | Charset mismatch | Use `utf8mb4` when creating the database |

---

### Summary

No model, session, or query code changes are needed when switching from SQLite to MySQL. The only change is:

1. `pip install pymysql`.
2. Set `DATABASE_URL=mysql+pymysql://...` in `.env` or as a server environment variable.
3. Create the MySQL database manually once.
4. Start Flask — `db.create_all()` builds the tables.
