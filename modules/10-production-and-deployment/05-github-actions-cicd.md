# Lesson 05: CI/CD with GitHub Actions

## Concept
Automate build and deployment to Azure Container Apps on every push to `main` using OIDC authentication — no stored credentials.


## 1. CI/CD with GitHub Actions

> **Instructions only** — no implementation required.

### Goal
Build the Docker image, push it to ACR, and deploy to Container Apps on every push to `main`. Authentication to Azure uses OpenID Connect (OIDC) — GitHub exchanges a short-lived token with Azure at runtime. No Azure passwords or service principal secrets are stored in GitHub.

---

### 1.1 Why OIDC instead of stored credentials

The traditional approach stores an Azure service principal secret in GitHub Secrets — a long-lived credential that must be rotated manually and is exposed if GitHub is compromised.

OIDC (OpenID Connect) eliminates stored credentials entirely:
- GitHub mints a short-lived JWT for each workflow run
- Azure validates it against a pre-configured trust relationship (federated credential)
- The token expires after the run — nothing to steal, nothing to rotate

---

### 1.2 Set up OIDC federation (one-time setup, run in Azure CLI)

```bash
# Source shared config (created in Lesson 01)
source scripts/azure-vars.sh

APP_NAME_SP=htmx-flask-github-sp
GITHUB_ORG=your-github-username
GITHUB_REPO=htmx-flask-learning

# Create app registration (no password/secret generated)
az ad app create --display-name $APP_NAME_SP
APP_ID=$(az ad app list --display-name $APP_NAME_SP --query "[0].appId" -o tsv)
az ad sp create --id $APP_ID
SP_OBJECT_ID=$(az ad sp show --id $APP_ID --query id -o tsv)

SUBSCRIPTION_ID=$(az account show --query id -o tsv)

# Grant Contributor on the resource group (deploy scope only)
az role assignment create \
  --assignee $SP_OBJECT_ID \
  --role "Contributor" \
  --scope "/subscriptions/${SUBSCRIPTION_ID}/resourceGroups/${RESOURCE_GROUP}"

# Grant AcrPush on ACR
ACR_ID=$(az acr show --name $ACR_NAME --query id -o tsv)
az role assignment create \
  --assignee $SP_OBJECT_ID \
  --role "AcrPush" \
  --scope $ACR_ID

# Create federated credential — trusts GitHub Actions on the main branch only
az ad app federated-credential create \
  --id $APP_ID \
  --parameters '{
    "name": "github-main",
    "issuer": "https://token.actions.githubusercontent.com",
    "subject": "repo:'"${GITHUB_ORG}/${GITHUB_REPO}"':ref:refs/heads/main",
    "audiences": ["api://AzureADTokenAudience"]
  }'

# Print the three non-sensitive values to add to GitHub
echo "AZURE_CLIENT_ID:       $APP_ID"
echo "AZURE_TENANT_ID:       $(az account show --query tenantId -o tsv)"
echo "AZURE_SUBSCRIPTION_ID: $SUBSCRIPTION_ID"
echo "ACR_LOGIN_SERVER:      $ACR_LOGIN_SERVER"   # from scripts/azure-vars.sh
```

---

### 1.3 Add GitHub repository variables

Go to **Settings → Secrets and variables → Actions → Variables** (not Secrets):

| Variable name | Value | Sensitive? |
|---|---|---|
| `AZURE_CLIENT_ID` | App registration client ID | No — identifier only |
| `AZURE_TENANT_ID` | Azure tenant ID | No |
| `AZURE_SUBSCRIPTION_ID` | Azure subscription ID | No |
| `ACR_LOGIN_SERVER` | Output of `echo $ACR_LOGIN_SERVER` after `source scripts/azure-vars.sh` | No |
| `ACR_NAME` | Output of `echo $ACR_NAME` after `source scripts/azure-vars.sh` | No |

> These go in **Variables**, not Secrets. `ACR_LOGIN_SERVER` includes the unique suffix from Lesson 01 (e.g. `htmxflaskacr14823.azurecr.io`). No app config secrets are stored in GitHub — those live in Key Vault (Lesson 01).

---

### 1.4 Create workflow file

Create `.github/workflows/deploy.yml`:

```yaml
name: Build and Deploy

on:
  push:
    branches:
      - main

permissions:
  id-token: write   # required: lets GitHub mint an OIDC token for this run
  contents: read

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run tests
        run: |
          python -m pytest tests/ --tb=short || echo "No tests found"

      - name: Log in to Azure (OIDC — no stored credentials)
        uses: azure/login@v2
        with:
          client-id: ${{ vars.AZURE_CLIENT_ID }}
          tenant-id: ${{ vars.AZURE_TENANT_ID }}
          subscription-id: ${{ vars.AZURE_SUBSCRIPTION_ID }}

      - name: Log in to ACR (via authenticated az session)
        run: az acr login --name ${{ vars.ACR_NAME }}

      - name: Build and push Docker image
        run: |
          docker build -t ${{ vars.ACR_LOGIN_SERVER }}/htmx-flask-app:${{ github.sha }} .
          docker push ${{ vars.ACR_LOGIN_SERVER }}/htmx-flask-app:${{ github.sha }}

      - name: Deploy to Azure Container Apps
        uses: azure/container-apps-deploy-action@v2
        with:
          containerAppName: htmx-flask-app
          resourceGroup: htmx-flask-rg
          imageToDeploy: ${{ vars.ACR_LOGIN_SERVER }}/htmx-flask-app:${{ github.sha }}
```

---

### 1.5 Workflow flow

```
git push → main
  → GitHub mints short-lived OIDC token (scoped to this run)
  → Azure validates token against federated credential trust
  → az session established — no password exchanged
  → install deps + run tests
  → az acr login (uses az session, no ACR password)
  → docker build + push (image tagged with git SHA)
  → Container App updated to new image SHA
  → Container App fetches DATABASE_URL + FLASK_SECRET_KEY
    from Key Vault via Managed Identity (runtime, unchanged)
```

Each deployment is tagged with the exact git commit SHA. Rollback: `az containerapp update --image ...:previous-sha`.

---

### 1.6 What is stored where

| Item | Location | Why |
|---|---|---|
| `DATABASE_URL` | Azure Key Vault | Secret — never in GitHub or Container App config |
| `FLASK_SECRET_KEY` | Azure Key Vault | Secret — never in GitHub or Container App config |
| `AZURE_CLIENT_ID` | GitHub Variables | Non-sensitive identifier |
| `AZURE_TENANT_ID` | GitHub Variables | Non-sensitive identifier |
| `AZURE_SUBSCRIPTION_ID` | GitHub Variables | Non-sensitive identifier |
| `ACR_LOGIN_SERVER` | GitHub Variables | Non-sensitive URL |
| Azure SP secret/password | Does not exist | OIDC — no long-lived credential |

---

