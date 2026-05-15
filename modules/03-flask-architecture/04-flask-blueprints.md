# Lesson 04: Introduce Flask Blueprints (Modular Route Organization)

## Concept
Introduce Flask Blueprints (Modular Route Organization).


## 1. Introduce Flask Blueprints (Modular Route Organization)

### Goal
Move all routes from `app.py` into a Blueprint module, leaving `app.py` as a clean entry point.

### 1.1 Create routes/main_routes.py

Created `routes/main_routes.py` with:

```python
from flask import Blueprint, render_template, request
import time
from data.mock import employees

main = Blueprint("main", __name__)
```

All routes moved here with decorators changed from `@app.route` to `@main.route`.

### 1.2 Simplify app.py

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
│   └── main.css
└── venv/
```

