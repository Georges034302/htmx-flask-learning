# Lesson 37: Dockerize the App

## Concept
Dockerize the App.


## 1. Dockerize the App

> **Instructions only** — no implementation required.

### Goal
Package the Flask application into a Docker container so it runs identically in any environment.

---

### 1.1 Install gunicorn

```bash
source venv/bin/activate
pip install gunicorn
pip freeze > requirements.txt
```

Gunicorn is the production WSGI server used inside the container — Flask's built-in dev server is not suitable for production.

---

### 1.2 Create Dockerfile

Create `Dockerfile` in the project root:

```dockerfile
# Use official slim Python image
FROM python:3.12-slim

# Set working directory inside container
WORKDIR /app

# Copy dependency list first (layer caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create uploads directory
RUN mkdir -p uploads

# Expose the port gunicorn will listen on
EXPOSE 8000

# Run with gunicorn — 2 worker processes
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "app:app"]
```

Layer ordering matters: copying `requirements.txt` first means Docker reuses the pip install cache unless dependencies change.

---

### 1.3 Create .dockerignore

Create `.dockerignore` in the project root:

```
venv/
__pycache__/
*.pyc
*.pyo
.env
.git
uploads/
instance/
*.db
```

Prevents large or sensitive files from being copied into the image.

---

### 1.4 Create docker-compose.yml

Create `docker-compose.yml` for easier local development:

```yaml
version: "3.9"

services:
  web:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./uploads:/app/uploads
    environment:
      - FLASK_ENV=production
```

The `volumes` mount keeps uploaded files on the host, not lost when the container restarts.

---

### 1.5 Build and run

```bash
# Build the image
docker build -t htmx-flask-app .

# Run the container
docker run -p 8000:8000 htmx-flask-app

# Or with docker-compose
docker-compose up --build
```

Visit `http://localhost:8000` to verify.

---

### 1.6 Updated project structure

```
htmx-flask-learning/
├── app.py
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── requirements.txt
├── data/
├── routes/
├── templates/
├── static/
├── uploads/
└── venv/               ← excluded by .dockerignore
```

---

