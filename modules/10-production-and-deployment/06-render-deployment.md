# Lesson 47: Deploy to Render

## Concept
Deploy to Render.

## 1. Deploy to Render

### Goal
Deploy the Flask + HTMX application to Render — a platform-as-a-service that requires no Docker or cloud CLI setup and provides a free tier suitable for hobby projects and demos.

> **Instructions only** — a Render account is required. Sign up at https://render.com.
>
> **Prerequisites:** Lesson 40 (Gunicorn) and Lesson 41 (environment config) must be complete. The app must start via Gunicorn and read its configuration from environment variables.

---

### 1.1 Why Render as an alternative to Azure

| Factor | Azure Container Apps (Lesson 38) | Render |
|---|---|---|
| Setup complexity | High (CLI, ACR, resource groups) | Low (GitHub connect + click deploy) |
| Free tier | Limited / trial only | Yes (free web service) |
| Docker required | Yes | No (Render detects Python automatically) |
| Custom domains | Yes | Yes (on paid plans) |
| Best for | Enterprise / team production | Demos, learning, solo projects |

Render auto-detects Python apps, installs dependencies from `requirements.txt`, and starts the app using the `Procfile`.

---

### 1.2 Prerequisites

Before deploying, confirm:

1. `requirements.txt` is up to date:
    ```bash
    source venv/bin/activate
    pip freeze > requirements.txt
    ```
    Verify `gunicorn` and `pymysql` (if using MySQL) are present.

2. The app starts locally with Gunicorn:
    ```bash
    gunicorn app:app
    ```
    No errors should appear.

3. The repository is pushed to GitHub (public or private).

---

### 1.3 Create a Procfile

Create `Procfile` in the project root (no file extension):

```
web: gunicorn app:app
```

- `web` — Render service type (web process that receives HTTP traffic).
- `gunicorn app:app` — module `app.py`, Flask instance `app`.

For production with the Gunicorn config file from Lesson 40:

```
web: gunicorn -c gunicorn.conf.py app:app
```

---

### 1.4 Create render.yaml (optional but recommended)

`render.yaml` lets you define the Render service in code, making deployments reproducible.

Create `render.yaml` in the project root:

```yaml
services:
  - type: web
    name: htmx-flask-app
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app
    envVars:
      - key: FLASK_ENV
        value: production
      - key: FLASK_SECRET_KEY
        generateValue: true        # Render generates a random value on first deploy
      - key: DATABASE_URL
        sync: false                # Set manually in Render dashboard (do not commit)
```

Key fields:
- `env: python` — Render uses its managed Python environment (no Dockerfile needed).
- `generateValue: true` — Render generates a secure random value automatically.
- `sync: false` — marks the variable as secret; must be set in the dashboard.

---

### 1.5 Push all files to GitHub

```bash
git add Procfile render.yaml requirements.txt
git commit -m "Add Render deployment files"
git push origin main
```

Verify `.gitignore` excludes these files:

```
venv/
.env
*.db
__pycache__/
```

---

### 1.6 Connect the repo to Render and deploy

1. Log in at https://render.com.
2. Click **New → Web Service**.
3. Connect your GitHub account and select the `htmx-flask-learning` repository.
4. Render detects `render.yaml` automatically if present, or you configure manually:
   - **Environment:** Python
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
5. Click **Create Web Service**.

Render will:
1. Clone the repository.
2. Run `pip install -r requirements.txt`.
3. Start `gunicorn app:app`.
4. Assign a public URL: `https://htmx-flask-app.onrender.com`.

---

### 1.7 Set environment variables in the Render dashboard

Navigate to your service → **Environment** tab.

Add these variables:

| Key | Value |
|---|---|
| `FLASK_ENV` | `production` |
| `FLASK_SECRET_KEY` | A long random string (use a password manager to generate) |
| `DATABASE_URL` | `mysql+pymysql://user:pass@host/dbname` (if using MySQL) |

> **Security rule:** Never put real credentials in `render.yaml` or commit them to Git. Always set secrets via the dashboard or use `generateValue: true` for keys Render can generate.

After adding variables, Render automatically redeploys.

---

### 1.8 Verify the live deployment

1. Open the Render-provided URL in your browser.
2. Confirm the employee dashboard loads.
3. Test HTMX interactions: search, add, delete.
4. Check Render **Logs** tab for any runtime errors.

**Common issues:**

| Issue | Cause | Fix |
|---|---|---|
| `ModuleNotFoundError` | Package missing from `requirements.txt` | Run `pip freeze > requirements.txt` and redeploy |
| `FLASK_SECRET_KEY not set` | Missing env var | Add `FLASK_SECRET_KEY` in Render dashboard |
| App loads but database errors | `DATABASE_URL` not set or wrong | Check `DATABASE_URL` in Render environment |
| `gunicorn: command not found` | Gunicorn not in `requirements.txt` | Add `gunicorn` and redeploy |
| 502 Bad Gateway | App crashed on startup | Check Render logs for Python traceback |

---

### 1.9 Automatic deploys

By default, Render deploys automatically on every push to `main`. To disable:
- Go to service → **Settings** → **Auto-Deploy** → set to manual.

To trigger a manual deploy:
- Render dashboard → **Manual Deploy** → **Deploy latest commit**.

---

### Summary

| Step | Action |
|---|---|
| Local prep | `Procfile`, `render.yaml`, `requirements.txt` |
| GitHub | Push all files, ensure `.env` is excluded |
| Render setup | New Web Service → connect repo → Python env |
| Secrets | Set `FLASK_SECRET_KEY` and `DATABASE_URL` in dashboard |
| Verify | Open live URL, test HTMX interactions, check logs |
