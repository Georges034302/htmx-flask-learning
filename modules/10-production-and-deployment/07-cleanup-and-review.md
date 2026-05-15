# Lesson 07: Cleanup and Module Review

## Concept
Review the architecture produced by each lesson in this module, then clean up all Azure resources to avoid ongoing costs.


## 1. Module 10 Architecture Review

> Resource names in diagrams below use the pattern from `scripts/azure-vars.sh`. Globally unique names (ACR, Key Vault, MySQL server) include your `AZURE_SUFFIX` from `.env` — e.g. `htmxflaskacr14823`, `htmx-kv-14823`, `htmx-db-14823`.

### Per-lesson architecture

---

#### Lesson 01 — Environment Config and Key Vault

```
Local development
─────────────────
.env (git-ignored)
  APP_ADMIN_USER, APP_ADMIN_PASSWORD
  FLASK_SECRET_KEY, DATABASE_URL
        │
        ▼
Flask app  ←  os.environ  (python-dotenv loads .env)
mock.py    ←  os.environ  (no hardcoded credentials)

gunicorn.conf.py  (committed, non-sensitive)
        │
        └──► used by Dockerfile in Lesson 02

Azure (cloud only)
──────────────────
Resource Group: htmx-flask-rg
        │
        └──► Key Vault: htmx-kv-<SUFFIX>    (e.g. htmx-kv-14823)
               APP-ADMIN-USER
               APP-ADMIN-PASSWORD
               FLASK-SECRET-KEY
               DATABASE-URL        (added in Lesson 03)
               ── reused by Lessons 03, 04, 05, 06 ──
```

---

#### Lesson 02 — Docker (local)

```
docker-compose up --build
        │
        ├──► db  (mysql:8)
        │      Port 3306
        │      Volume: mysql_data (persistent)
        │      Init:   data/employee_db_setup.sql
        │
        └──► web  (Flask / Gunicorn)
               Port 8000
               Reads: DATABASE_URL=mysql+pymysql://app_user:...@db:3306/employees_db
               Volume: uploads
               depends_on: db (health check)

HTMX: served via CDN — no container needed
```

---

#### Lesson 03 — Azure Container Apps (manual)

```
ACR: htmxflaskacr<SUFFIX>    (e.g. htmxflaskacr14823)
  └── image: htmx-flask-app:<sha>
        │
        ▼
Container Apps Environment: htmx-flask-env
  └── Container App: htmx-flask-app
        │  Managed Identity: htmx-flask-identity
        │    ├── AcrPull  →  ACR (image pulls, no password)
        │    └── Key Vault Secrets User  →  Key Vault
        │          DATABASE-URL   →  env: DATABASE_URL
        │          FLASK-SECRET-KEY  →  env: FLASK_SECRET_KEY
        │
        ├── Ingress: HTTPS (auto TLS, public)
        ├── Scale: 0–3 replicas (scales to zero)
        └── Database: Azure DB for MySQL Flexible Server
                      htmx-db-<SUFFIX>.mysql.database.azure.com
```

---

#### Lesson 04 — Helm + AKS (manual)

```
AKS Cluster: htmx-flask-aks
  Addons: Key Vault Secrets Provider CSI, OIDC Issuer, Workload Identity
  Namespace: htmx-flask
        │
        ├── ServiceAccount: htmx-flask-sa
        │     Annotation: workload-identity client-id
        │           │
        │           ▼  (Workload Identity — no credentials in pod)
        │     Key Vault: htmx-kv-<SUFFIX>
        │           │
        │     SecretProviderClass: htmx-flask-kv-secrets
        │           │  (CSI driver syncs KV secrets on pod start)
        │           ▼
        │     Kubernetes Secret: htmx-flask-app-secrets
        │           DATABASE_URL, FLASK_SECRET_KEY
        │
        ├── Deployment: htmx-flask-app  (2 replicas)
        │     Reads secrets via secretKeyRef
        │     Volume mount: /mnt/secrets (required for CSI sync)
        │
        ├── Service: LoadBalancer  (port 80 → 8000)
        │
        └── Helm release: htmx-flask
              helm upgrade --install htmx-flask ./helm/htmx-flask-app
```

---

#### Lesson 05 — GitHub Actions CI/CD → Container Apps

```
git push → main
        │
        ▼
GitHub Actions workflow
  permissions: id-token: write   (OIDC token minted per run)
        │
        ├── azure/login@v2
        │     vars.AZURE_CLIENT_ID    (non-sensitive)
        │     vars.AZURE_TENANT_ID    (non-sensitive)
        │     vars.AZURE_SUBSCRIPTION_ID  (non-sensitive)
        │     ── no passwords stored in GitHub ──
        │
        ├── az acr login → docker build + push
        │     Image tagged: <ACR>/<app>:<git-sha>
        │
        └── azure/container-apps-deploy-action@v2
              Updates Lesson 03 Container App to new image SHA
                    │
                    ▼
              Container App restarts → fetches secrets from Key Vault
              via Managed Identity (unchanged from Lesson 03)
```

---

#### Lesson 06 — Azure DevOps CI/CD → AKS/Helm

```
git push → main
        │
        ▼
Azure DevOps Pipeline (.azure-pipelines/deploy.yml)
        │
        ├── Service Connection: htmx-flask-azure-sc
        │     Workload Identity Federation (no client secret)
        │
        ├── AzureCLI@2: az acr login → docker build + push
        │     Image tagged: <ACR>/<app>:<Build.SourceVersion>
        │
        └── HelmDeploy@0
              Kubernetes Service Connection: htmx-flask-aks-sc
              helm upgrade --install
              --set image.tag=<Build.SourceVersion>
                    │
                    ▼
              AKS pod restarts → Key Vault CSI driver syncs secrets
              via Workload Identity (unchanged from Lesson 04)
```

---

### Full module resource map

```
Azure Resource Group: htmx-flask-rg
├── Key Vault:                   htmx-kv-<SUFFIX>        (Lesson 01)
├── Container Registry:          htmxflaskacr<SUFFIX>    (Lesson 03)
├── MySQL Flexible Server:       htmx-db-<SUFFIX>        (Lesson 03)
├── Managed Identity:            htmx-flask-identity     (Lesson 03)
├── Container Apps Environment:  htmx-flask-env          (Lesson 03)
├── Container App:               htmx-flask-app          (Lesson 03)
├── AKS Cluster:                 htmx-flask-aks          (Lesson 04)
└── Managed Identity (WI):       htmx-flask-wi           (Lesson 04)

GitHub
└── Repository variables (non-sensitive): AZURE_CLIENT_ID, AZURE_TENANT_ID,
    AZURE_SUBSCRIPTION_ID, ACR_LOGIN_SERVER                (Lesson 05)

Azure DevOps
└── Service connections: htmx-flask-azure-sc, htmx-flask-aks-sc  (Lesson 06)
```

---

## 2. Cleanup

> Run these commands when you are finished with the module to avoid ongoing Azure charges.

### 2.1 Delete all Azure resources

The safest and fastest cleanup is deleting the entire resource group — this removes every resource created across all lessons.

```bash
az group delete \
  --name htmx-flask-rg \
  --yes \
  --no-wait
```

`--no-wait` returns immediately; deletion runs in the background (~5 minutes).

---

### 2.2 Delete the Azure AD app registration (OIDC)

The app registration for GitHub Actions OIDC lives outside the resource group and must be deleted separately:

```bash
APP_ID=$(az ad app list \
  --display-name htmx-flask-github-sp \
  --query "[0].appId" -o tsv)

az ad app delete --id $APP_ID
```

---

### 2.3 Delete local files

```bash
# Remove .env — already git-ignored but clean up the working directory
rm -f .env

# Remove gunicorn.conf.py if you do not need it locally
# (keep it if you plan to run gunicorn outside Docker)
```

---

### 2.4 Cleanup checklist

- [ ] `az group delete --name htmx-flask-rg` completed
- [ ] App registration `htmx-flask-github-sp` deleted
- [ ] `.env` removed from local working directory
- [ ] No Azure resources remain (verify: `az resource list --resource-group htmx-flask-rg`)
- [ ] Docker volumes cleaned: `docker-compose down -v`
- [ ] Local kubeconfig entry removed: `kubectl config delete-context htmx-flask-aks`

---
