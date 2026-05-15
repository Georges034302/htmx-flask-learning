# Lesson 04: Production WSGI Server (Gunicorn)

## Concept
Production WSGI Server (Gunicorn).


## 1. Production WSGI Server (Gunicorn)

> **Instructions only** — gunicorn is already installed in Step 47. This step explains configuration for production tuning.

### Goal
Replace Flask's built-in dev server with Gunicorn, properly configured for concurrent traffic, timeouts, and logging.

---

### 1.1 Basic gunicorn command

```bash
gunicorn --bind 0.0.0.0:8000 --workers 2 app:app
```

- `--bind 0.0.0.0:8000` — listen on all interfaces, port 8000
- `--workers 2` — 2 parallel worker processes
- `app:app` — module `app.py`, Flask instance named `app`

---

### 1.2 Worker count formula

```
workers = (2 × CPU cores) + 1
```

For a 2-core machine: 5 workers. For a single-core container: 2–3 workers.

---

### 1.3 Create gunicorn.conf.py

Create `gunicorn.conf.py` in the project root:

```python
bind = "0.0.0.0:8000"
workers = 3
timeout = 60
keepalive = 5
accesslog = "-"       # log to stdout
errorlog = "-"        # log to stderr
loglevel = "info"
```

Run with:

```bash
gunicorn -c gunicorn.conf.py app:app
```

---

### 1.4 Update Dockerfile CMD

Replace the inline CMD with the config file:

```dockerfile
CMD ["gunicorn", "-c", "gunicorn.conf.py", "app:app"]
```

---

### 1.5 Comparison: dev server vs gunicorn

| Feature            | Flask dev server        | Gunicorn              |
|--------------------|-------------------------|-----------------------|
| Concurrent requests| Single-threaded         | Multiple workers      |
| Restart on code change | Yes (`debug=True`)  | No (use `--reload`)   |
| HTTPS              | No                      | Via reverse proxy     |
| Production safe    | No                      | Yes                   |

---

