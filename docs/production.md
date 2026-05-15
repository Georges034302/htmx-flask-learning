# Azure Production Deployment

Reference guide for Module 10. Covers concepts, deployment targets, security model, and architecture for taking the HTMX + Flask app from a local container to production on Azure.

---

## Concepts

### Secrets Management — Azure Key Vault

A Key Vault is a managed HSM-backed store for secrets, keys, and certificates. The core principle: **no secret ever lives in code, config files, environment variable literals, or CI/CD variables**.

```
┌─────────────────────────────────────────────────────────┐
│                    Azure Key Vault                       │
│                                                          │
│  APP-ADMIN-USER        ──► Flask app login check        │
│  APP-ADMIN-PASSWORD    ──► Flask app login check        │
│  FLASK-SECRET-KEY      ──► Flask session signing        │
│  DATABASE-URL          ──► SQLAlchemy connection string  │
└─────────────────────────────────────────────────────────┘
        ▲                           ▲
        │  RBAC: Secrets User       │  RBAC: Secrets User
   Managed Identity            Workload Identity
  (Container Apps)                 (AKS pod)
```

Secrets are fetched **at runtime** by the identity assigned to the workload — never at build time, never stored in the deployment manifest.

---

### Identity — Managed Identity vs Workload Identity

| Identity type | Used by | How it works |
|---|---|---|
| **User-assigned Managed Identity** | Container Apps (Lesson 03) | Azure assigns an identity to the Container App; no credentials anywhere |
| **Workload Identity (pod-level)** | AKS pods (Lesson 04) | Kubernetes ServiceAccount federated to Azure AD via OIDC issuer; no credentials in pod spec |

Both eliminate the need for any service principal secret in the application runtime.

---

### Authentication — OIDC / Workload Identity Federation

Used by CI/CD pipelines (not the app itself) to authenticate to Azure **without storing a password or certificate**.

```
┌──────────────────┐         short-lived JWT          ┌──────────────────┐
│  GitHub Actions  │ ──────────────────────────────►  │   Azure AD       │
│  (or ADO)        │                                   │                  │
│                  │ ◄──────────────────────────────── │  Validates JWT   │
└──────────────────┘       az session token            │  against trusted │
                                                       │  federated cred  │
                                                       └──────────────────┘
```

The token expires after the pipeline run. There is nothing to rotate, revoke, or accidentally commit.

---

### Container Registry — Azure Container Registry (ACR)

Stores Docker images privately within your Azure subscription. Image pulls by Container Apps and AKS pods use Managed Identity / Workload Identity (AcrPull role) — no registry password.

```
docker build → docker push → ACR
                               │
                    AcrPull (identity-based)
                    ┌──────────┴────────────┐
                    ▼                        ▼
           Container App              AKS pod
```

---

## Deployment Targets

### Target A — Azure Container Apps

Serverless container platform. No cluster to manage. Scales to zero when idle.

```
┌──────────────────────────────────────────────────────────────────┐
│                  Container Apps Environment                       │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │  Container App: htmx-flask-app                          │     │
│  │  ┌─────────────────────────────────────────────────┐   │     │
│  │  │  Flask + Gunicorn (port 8000)                   │   │     │
│  │  │  env: DATABASE_URL  ◄── secretref → Key Vault   │   │     │
│  │  │  env: FLASK_SECRET_KEY ◄── secretref → Key Vault│   │     │
│  │  └─────────────────────────────────────────────────┘   │     │
│  │  Identity: htmx-flask-identity (User-Assigned MI)      │     │
│  │    ├── AcrPull ──────────────────────────► ACR         │     │
│  │    └── Key Vault Secrets User ──────────► Key Vault    │     │
│  │  Ingress: HTTPS (auto TLS) — public                    │     │
│  │  Scale: 0 → 3 replicas                                 │     │
│  └─────────────────────────────────────────────────────────┘     │
└──────────────────────────────────────────────────────────────────┘
           │
           ▼
  Azure DB for MySQL Flexible Server
  htmx-db-<SUFFIX>.mysql.database.azure.com
  (TLS enforced, private access)
```

**Set up in:** Lesson 03 (manual), Lesson 05 (automated via GitHub Actions)

---

### Target B — Azure Kubernetes Service (AKS) with Helm

Managed Kubernetes cluster. Full control over workload configuration. Suitable for multi-service production systems.

```
┌──────────────────────────────────────────────────────────────────┐
│  AKS Cluster: htmx-flask-aks                                     │
│  Addons: Key Vault Secrets Provider CSI, OIDC Issuer,            │
│          Workload Identity                                        │
│                                                                   │
│  Namespace: htmx-flask                                           │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │                                                            │  │
│  │  ServiceAccount: htmx-flask-sa                            │  │
│  │    annotation: workload-identity/client-id                │  │
│  │         │                                                  │  │
│  │         │ OIDC federated credential                        │  │
│  │         ▼                                                  │  │
│  │    Azure AD ──► Key Vault Secrets User ──► Key Vault      │  │
│  │                                              │             │  │
│  │    SecretProviderClass: htmx-flask-kv-secrets│             │  │
│  │    (CSI driver syncs secrets on pod mount)   │             │  │
│  │         │                                    │             │  │
│  │         ▼                                    ▼             │  │
│  │    K8s Secret: htmx-flask-app-secrets                     │  │
│  │       DATABASE_URL, FLASK_SECRET_KEY                      │  │
│  │         │                                                  │  │
│  │         ▼                                                  │  │
│  │  Deployment: htmx-flask-app (2 replicas)                  │  │
│  │    Flask + Gunicorn (port 8000)                           │  │
│  │    env vars from secretKeyRef                             │  │
│  │         │                                                  │  │
│  │         ▼                                                  │  │
│  │  Service: LoadBalancer (port 80 → 8000)                   │  │
│  └────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────┘
```

**Set up in:** Lesson 04 (manual), Lesson 06 (automated via Azure DevOps)

---

## CI/CD Pipelines

### Pipeline A — GitHub Actions → Container Apps

```
Developer workstation
        │
        │  git push → main
        ▼
┌───────────────────────────────────────────────────────┐
│  GitHub Actions (.github/workflows/deploy.yml)        │
│                                                       │
│  1. Checkout code                                     │
│  2. Install deps + run pytest                         │
│  3. azure/login@v2                                    │
│       vars.AZURE_CLIENT_ID   (GitHub Variable)        │
│       vars.AZURE_TENANT_ID   (GitHub Variable)        │
│       vars.AZURE_SUBSCRIPTION_ID (GitHub Variable)    │
│       ── OIDC token, no stored password ──            │
│  4. az acr login --name ${{ vars.ACR_NAME }}          │
│  5. docker build + push                               │
│       Image: <ACR>/<app>:<git-sha>                    │
│  6. azure/container-apps-deploy-action@v2             │
│       Updates Container App to new image SHA          │
└───────────────────────────────────────────────────────┘
        │
        ▼
Container App restarts
  → fetches DATABASE_URL + FLASK_SECRET_KEY
    from Key Vault via Managed Identity (unchanged)
```

**Set up in:** Lesson 05

---

### Pipeline B — Azure DevOps → AKS / Helm

```
Developer workstation
        │
        │  git push → main
        ▼
┌───────────────────────────────────────────────────────┐
│  Azure DevOps Pipeline (.azure-pipelines/deploy.yml)  │
│                                                       │
│  Stage 1 — Build                                      │
│    AzureCLI@2 (Service Connection: WIF, no secret)    │
│       az acr login → docker build + push              │
│       Image: <ACR>/<app>:<Build.SourceVersion>        │
│                                                       │
│  Stage 2 — Test                                       │
│    UsePythonVersion@0 → pytest                        │
│                                                       │
│  Stage 3 — Deploy                                     │
│    HelmDeploy@0                                       │
│       Kubernetes Service Connection (OIDC)            │
│       helm upgrade --install                          │
│       --set image.tag=<Build.SourceVersion>           │
└───────────────────────────────────────────────────────┘
        │
        ▼
AKS pod restarts
  → CSI driver syncs DATABASE_URL + FLASK_SECRET_KEY
    from Key Vault via Workload Identity (unchanged)
```

**Set up in:** Lesson 06

---

## Full Resource Map

```
Azure Subscription
└── Resource Group: htmx-flask-rg
    │
    ├── Key Vault: htmx-kv-<SUFFIX>              (Lesson 01)
    │     Secrets: APP-ADMIN-USER, APP-ADMIN-PASSWORD,
    │              FLASK-SECRET-KEY, DATABASE-URL
    │
    ├── Container Registry: htmxflaskacr<SUFFIX> (Lesson 03)
    │     Images: htmx-flask-app:<git-sha>
    │
    ├── MySQL Flexible Server: htmx-db-<SUFFIX>  (Lesson 03)
    │     DB: employees_db
    │     Access: private (Container Apps VNet)
    │
    ├── Managed Identity: htmx-flask-identity    (Lesson 03)
    │     Roles: AcrPull, Key Vault Secrets User
    │     Used by: Container App
    │
    ├── Container Apps Environment: htmx-flask-env (Lesson 03)
    │     └── Container App: htmx-flask-app
    │           Secrets: keyvaultref → Key Vault
    │           Identity: htmx-flask-identity
    │
    ├── AKS Cluster: htmx-flask-aks              (Lesson 04)
    │     Addons: Key Vault CSI, OIDC, Workload Identity
    │     └── Namespace: htmx-flask
    │           ServiceAccount: htmx-flask-sa
    │           Helm release: htmx-flask
    │
    └── Managed Identity (WI): htmx-flask-wi     (Lesson 04)
          Roles: Key Vault Secrets User
          Federated: AKS OIDC → htmx-flask-sa

Azure AD
└── App Registration: htmx-flask-github-sp       (Lesson 05)
      Federated credential: GitHub Actions main branch
      Roles: Contributor (htmx-flask-rg), AcrPush

Azure DevOps
├── Service Connection: htmx-flask-azure-sc      (Lesson 06)
│     Type: Workload Identity Federation (automatic)
└── Service Connection: htmx-flask-aks-sc        (Lesson 06)
      Type: Kubernetes (AKS)

GitHub Repository
└── Variables (non-sensitive):                   (Lesson 05)
      AZURE_CLIENT_ID, AZURE_TENANT_ID,
      AZURE_SUBSCRIPTION_ID, ACR_LOGIN_SERVER, ACR_NAME
```

---

## Security Model Summary

| Layer | Credential | How eliminated |
|---|---|---|
| App secrets at runtime | DB password, Flask key | Azure Key Vault — fetched by identity, never in config |
| Container image pulls | ACR password | Managed Identity / Workload Identity (AcrPull role) |
| GitHub → Azure auth | SP secret | OIDC federated credential (short-lived token per run) |
| ADO → Azure auth | SP secret | Service Connection with Workload Identity Federation |
| ADO → AKS auth | kubeconfig | Kubernetes Service Connection (OIDC) |
| Secrets in pipeline YAML | Any | Nothing sensitive in YAML — all values from Key Vault at pod runtime |

**Zero long-lived credentials** anywhere in the delivery chain.

---

## Lesson Map

| Topic | Lesson |
|---|--------|
| `.env`, `gunicorn.conf.py`, `scripts/azure-vars.sh`, Key Vault provisioning | [Lesson 01](../modules/10-production-and-deployment/01-env-and-keyvault.md) |
| Dockerfile, Gunicorn, Docker Compose + MySQL | [Lesson 02](../modules/10-production-and-deployment/02-docker.md) |
| ACR, Azure DB for MySQL, Container Apps, Managed Identity | [Lesson 03](../modules/10-production-and-deployment/03-container-apps.md) |
| AKS, Helm 3, Key Vault CSI driver, Workload Identity | [Lesson 04](../modules/10-production-and-deployment/04-helm-aks.md) |
| GitHub Actions OIDC CI/CD → Container Apps | [Lesson 05](../modules/10-production-and-deployment/05-github-actions-cicd.md) |
| Azure DevOps Pipelines WIF CI/CD → AKS / Helm | [Lesson 06](../modules/10-production-and-deployment/06-azure-devops-cicd.md) |
| Architecture review + Azure cleanup | [Lesson 07](../modules/10-production-and-deployment/07-cleanup-and-review.md) |

---

Copyright (c) 2026 Dr. Georges Bou Ghantous. All rights reserved.
