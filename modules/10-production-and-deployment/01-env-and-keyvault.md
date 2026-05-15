# Lesson 01: Environment Config and Key Vault

## Concept
Establish a secure configuration foundation: move hardcoded credentials out of source code into a local `.env` file, then mirror those secrets into Azure Key Vault for cloud deployments. This lesson is the prerequisite for all subsequent lessons in this module.


## 1. Environment Config and Key Vault

### Goal
Replace the hardcoded `admin / password123` in `mock.py` with credentials read from `.env` at runtime. Store the same secrets in Azure Key Vault so container and Kubernetes deployments never need plaintext credentials.

---

### 1.1 The problem with mock.py

`data/mock.py` currently contains:

```python
users = {
    "admin": "password123"   # hardcoded — never do this
}
```

This credential will also be reused as the application database user in later lessons. It must never be committed to source control.

---

### 1.2 Create .env (local development)

In the project root, create `.env`. **This file must never be committed to Git.**

```bash
# Prompt for admin password — never hardcode it
read -s -p "Enter admin password: " ADMIN_PASSWORD && echo
read -s -p "Confirm password: " ADMIN_PASSWORD_CONFIRM && echo

if [ "$ADMIN_PASSWORD" != "$ADMIN_PASSWORD_CONFIRM" ]; then
  echo "Passwords do not match. Aborting."
  exit 1
fi

cat > .env << EOF
# Application user — same credentials used for auth and DB app user
APP_ADMIN_USER=admin
APP_ADMIN_PASSWORD=${ADMIN_PASSWORD}

# Flask
FLASK_SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
FLASK_ENV=development
FLASK_DEBUG=1

# Database (local — updated to MySQL URL in later lessons)
DATABASE_URL=sqlite:///employees.db
EOF

echo ".env written."
unset ADMIN_PASSWORD ADMIN_PASSWORD_CONFIRM
```

> `read -s` suppresses terminal echo — the password is never visible or logged.

---

### 1.3 Add .env to .gitignore

```bash
grep -qxF '.env' .gitignore || echo '.env' >> .gitignore
```

Verify nothing sensitive is tracked:

```bash
git status --short | grep '\.env'   # should return nothing
```

---

### 1.4 Load .env in the Flask app

Install `python-dotenv`:

```bash
pip install python-dotenv
pip freeze > requirements.txt
```

At the top of `app.py` (or `config.py`), load the file before any `os.environ` reads:

```python
from dotenv import load_dotenv
import os

load_dotenv()   # reads .env into os.environ — no-op if file is absent

SECRET_KEY      = os.environ["FLASK_SECRET_KEY"]
ADMIN_USER      = os.environ["APP_ADMIN_USER"]
ADMIN_PASSWORD  = os.environ["APP_ADMIN_PASSWORD"]
DATABASE_URL    = os.environ.get("DATABASE_URL", "sqlite:///employees.db")
```

Using `os.environ["KEY"]` (not `.get`) for required values raises `KeyError` immediately on startup if the variable is missing — fail fast, not silently.

---

### 1.5 Update mock.py to read from environment

Replace the hardcoded `users` dict in `data/mock.py`:

```python
import os

employees = [
    {"id": 1,  "name": "Alice",   "department": "IT"},
    {"id": 2,  "name": "Bob",     "department": "HR"},
    {"id": 3,  "name": "Charlie", "department": "Finance"},
    {"id": 4,  "name": "David",   "department": "IT"},
    {"id": 5,  "name": "Emma",    "department": "Marketing"},
    {"id": 6,  "name": "Frank",   "department": "Security"},
    {"id": 7,  "name": "Grace",   "department": "IT"},
    {"id": 8,  "name": "Helen",   "department": "Finance"},
    {"id": 9,  "name": "Ian",     "department": "HR"},
    {"id": 10, "name": "Jack",    "department": "Marketing"},
    {"id": 11, "name": "Karen",   "department": "IT"},
    {"id": 12, "name": "Leo",     "department": "Security"},
]

# Credentials loaded from environment — never hardcoded
_user = os.environ.get("APP_ADMIN_USER", "")
_pass = os.environ.get("APP_ADMIN_PASSWORD", "")

users = {_user: _pass} if _user and _pass else {}
```

---

### 1.6 Gunicorn config

While setting up config files, also create `gunicorn.conf.py` in the project root — it will be used by the Dockerfile in Lesson 02:

```python
bind      = "0.0.0.0:8000"
workers   = 3          # formula: (2 × CPU cores) + 1; 3 suits a 1-core container
timeout   = 60
keepalive = 5
accesslog = "-"        # stdout
errorlog  = "-"        # stderr
loglevel  = "info"
```

> Never run Flask's built-in dev server in production. Gunicorn handles concurrent requests; Flask's dev server is single-threaded.

---

### 1.7 Suggested .env variables checklist

| Variable | Purpose | Required |
|---|---|---|
| `APP_ADMIN_USER` | Application auth username | Yes |
| `APP_ADMIN_PASSWORD` | Application auth + DB user password | Yes |
| `FLASK_SECRET_KEY` | Session signing key (32+ random bytes) | Yes |
| `FLASK_ENV` | `development` or `production` | Yes |
| `FLASK_DEBUG` | `1` (dev) or `0` (prod) | Yes |
| `DATABASE_URL` | SQLAlchemy connection string | Yes |
| `UPLOAD_FOLDER` | Path for file uploads | Module 09 |
| `MAX_CONTENT_LENGTH` | Max upload size in bytes | Module 09 |

---

### 1.8 Create scripts/azure-vars.sh

> **Instructions only** — Azure subscription needed. Skip if working locally only.

All cloud lessons (03–06) share the same Azure resource names. Some names must be **globally unique** across all Azure customers worldwide. Create a shared config script once here so every later lesson simply sources it.

**Step 1 — Generate and save a random suffix:**

```bash
# Run this ONCE. The suffix is saved to .env and reused by all later lessons.
AZURE_SUFFIX=$RANDOM
echo "AZURE_SUFFIX=${AZURE_SUFFIX}" >> .env
echo "Suffix: $AZURE_SUFFIX — saved to .env"

mkdir -p scripts
```

> `$RANDOM` produces 0–32767. For extra collision safety use `$(openssl rand -hex 4)` (8 hex chars) instead — both are fine for a learning project.

**Step 2 — Create `scripts/azure-vars.sh` and paste the content below into it:**

```bash
#!/usr/bin/env bash
# scripts/azure-vars.sh — Shared Azure config for Module 10
# Commit this file. It contains no secrets.
# Usage: source scripts/azure-vars.sh

# Load .env to get AZURE_SUFFIX (and other local config)
set -a; source .env; set +a

# ── Shared (non-unique) ──────────────────────────────────────────────────────
RESOURCE_GROUP=htmx-flask-rg
LOCATION=australiaeast

# ── Globally unique names (AZURE_SUFFIX from .env) ──────────────────────────
# ACR:       alphanumeric only, 5–50 chars, unique across all Azure tenants
ACR_NAME="htmxflaskacr${AZURE_SUFFIX}"
ACR_LOGIN_SERVER="${ACR_NAME}.azurecr.io"
# Key Vault: 3–24 chars, hyphens allowed, globally unique
KV_NAME="htmx-kv-${AZURE_SUFFIX}"
# MySQL:     globally unique
DB_SERVER="htmx-db-${AZURE_SUFFIX}"

# ── Unique within subscription ───────────────────────────────────────────────
APP_ENV=htmx-flask-env
APP_NAME=htmx-flask-app
IDENTITY_NAME=htmx-flask-identity    # Managed Identity — Container Apps (Lesson 03)
IDENTITY_NAME_WI=htmx-flask-wi       # Managed Identity — AKS Workload Identity (Lesson 04)
CLUSTER_NAME=htmx-flask-aks
NAMESPACE=htmx-flask
SERVICE_ACCOUNT=htmx-flask-sa

export RESOURCE_GROUP LOCATION \
       ACR_NAME ACR_LOGIN_SERVER KV_NAME DB_SERVER \
       APP_ENV APP_NAME IDENTITY_NAME IDENTITY_NAME_WI \
       CLUSTER_NAME NAMESPACE SERVICE_ACCOUNT
```

**Step 3 — Make it executable:**

```bash
chmod +x scripts/azure-vars.sh
```

---

### 1.9 Create Azure Resource Group

The resource group is the single container for **all** Azure resources used across Lessons 01–06: Key Vault, ACR, Container Apps, AKS, and MySQL. Create it once here.

```bash
source scripts/azure-vars.sh

az group create --name $RESOURCE_GROUP --location $LOCATION
```

---

### 1.10 Set up Azure Key Vault

This Key Vault is provisioned once here and reused by Lessons 03, 04, 05, and 06.

```bash
# source scripts/azure-vars.sh  # already loaded if running in the same session

# Create Key Vault with RBAC authorization
az keyvault create \
  --name $KV_NAME \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION \
  --enable-rbac-authorization true

# Read admin password from terminal — never paste into the command
read -s -p "Enter admin password to store in Key Vault: " KV_ADMIN_PASSWORD && echo

# Store secrets
az keyvault secret set \
  --vault-name $KV_NAME \
  --name "APP-ADMIN-USER" \
  --value "admin"

az keyvault secret set \
  --vault-name $KV_NAME \
  --name "APP-ADMIN-PASSWORD" \
  --value "$KV_ADMIN_PASSWORD"

az keyvault secret set \
  --vault-name $KV_NAME \
  --name "FLASK-SECRET-KEY" \
  --value "$(python3 -c 'import secrets; print(secrets.token_hex(32))')"

unset KV_ADMIN_PASSWORD
```

Secret names use hyphens (`APP-ADMIN-PASSWORD`) — Key Vault does not allow underscores in names. They are mapped back to the conventional env var names (`APP_ADMIN_PASSWORD`) by the Container App and Kubernetes SecretProviderClass in later lessons.

---

### 1.11 Grant yourself Key Vault Secrets Officer (to manage secrets)

```bash
MY_PRINCIPAL=$(az ad signed-in-user show --query id -o tsv)
KV_ID=$(az keyvault show --name $KV_NAME --query id -o tsv)

az role assignment create \
  --assignee $MY_PRINCIPAL \
  --role "Key Vault Secrets Officer" \
  --scope $KV_ID
```

---

### Summary

| Where | What is stored |
|---|---|
| `.env` (local, git-ignored) | App secrets + `AZURE_SUFFIX` |
| `scripts/azure-vars.sh` (committed) | Non-sensitive Azure resource names and locations |
| `gunicorn.conf.py` (committed) | Non-sensitive server config |
| Azure Key Vault | App secrets for cloud deployments (Lessons 03–06) |
| `mock.py` | No secrets — reads from environment |
| `app.py` | No secrets — reads from environment |

---
