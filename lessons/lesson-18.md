# Lesson 18: Refactor the Flask Application Structure

Included step: 28

## Concept
Refactor the Flask Application Structure.

## Step flow

## 28) Refactor the Flask Application Structure

### Goal
Move mock data out of `app.py` into a separate module — separating data from logic.

### 28.1 Create data/mock.py

Created `data/mock.py` with the employees list:

```python
employees = [
    {"id": 1, "name": "Alice", "department": "IT"},
    {"id": 2, "name": "Bob", "department": "HR"},
    {"id": 3, "name": "Charlie", "department": "Finance"},
    {"id": 4, "name": "David", "department": "IT"},
    {"id": 5, "name": "Emma", "department": "Marketing"}
]
```

### 28.2 Update app.py

Removed the inline `employees` list from `app.py`.

Added import at the top:

```python
from data.mock import employees
```

HTMX behavior, routes, and templates are unchanged.

### Project Structure

```
htmx-flask-learning/
├── app.py
├── requirements.txt
├── data/
│   └── mock.py
├── templates/
│   ├── index.html
│   └── partials/
├── static/
│   └── style.css
└── venv/
```

