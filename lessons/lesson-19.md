# Lesson 19: Introduce Flask Blueprints (Modular Route Organization)

Included step: 29

Learning objective:
Master one focused concept from step 29 with precise, sequential execution.

Editor notes:
- Keep the exact sequence from source material.
- Validate behavior at each test checkpoint before continuing.

## Detailed walkthrough

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

