# Lesson 02: Dockerize the App

## Concept
Package the Flask application into a Docker image with Gunicorn as the production WSGI server, and wire a multi-container local development environment with MySQL using Docker Compose.


## 1. Dockerize the App

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

# Run with gunicorn using the config file created in Lesson 01
CMD ["gunicorn", "-c", "gunicorn.conf.py", "app:app"]
```

Layer ordering matters: copying `requirements.txt` first means Docker reuses the pip install cache unless dependencies change.

`gunicorn.conf.py` was created in Lesson 01. It sets `workers = 3`, `timeout = 60`, and logs to stdout/stderr so Docker captures them with `docker logs`.

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

Create `docker-compose.yml` in the project root. This is a **multi-container** setup: a MySQL 8 database container and the Flask web container, networked together automatically by Compose.

```yaml
version: "3.9"

services:

  db:
    image: mysql:8
    restart: unless-stopped
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: employees_db
      MYSQL_USER: app_user
      MYSQL_PASSWORD: app_password
    volumes:
      - mysql_data:/var/lib/mysql
      - ./data/employee_db_setup.sql:/docker-entrypoint-initdb.d/employee_db_setup.sql:ro
    ports:
      - "3306:3306"
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost", "-u", "root", "-prootpassword"]
      interval: 10s
      timeout: 5s
      retries: 5

  web:
    build: .
    restart: unless-stopped
    depends_on:
      db:
        condition: service_healthy
    environment:
      FLASK_ENV: production
      FLASK_SECRET_KEY: change-me-in-production
      DATABASE_URL: mysql+pymysql://app_user:app_password@db:3306/employees_db
    ports:
      - "8000:8000"
    volumes:
      - uploads:/app/uploads

volumes:
  mysql_data:   # persists MySQL data across container restarts
  uploads:      # persists uploaded files across container restarts
```

Key points:
- `db` uses `mysql:8` — no custom image needed.
- The init SQL (`data/employee_db_setup.sql`) is mounted read-only into `/docker-entrypoint-initdb.d/`. MySQL runs it automatically on first container start, creating and seeding the `employees_db` database.
- `web` only starts after `db` passes its health check (`depends_on: condition: service_healthy`), preventing connection errors on startup.
- `DATABASE_URL` uses `db` as the hostname — Compose puts both services on the same internal network and resolves service names as hostnames.
- `mysql_data` volume persists the database across `docker-compose down` / `up` cycles. Use `docker-compose down -v` to reset it.

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
├── gunicorn.conf.py    ← created in Lesson 01
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── requirements.txt
├── scripts/
│   └── azure-vars.sh   ← created in Lesson 01
├── data/
├── routes/
├── templates/
├── static/
├── uploads/
└── venv/               ← excluded by .dockerignore
```

---

