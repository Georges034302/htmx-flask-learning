# Lesson 03: Deploy to Azure Container Apps

## Concept
Deploy the Flask app to Azure Container Apps using Azure Key Vault for secrets and Azure Database for MySQL for persistence. No secrets are stored in code or environment variables — all sensitive config is managed by Key Vault and accessed via Managed Identity.


## 1. Deploy to Azure Container Apps

> **Instructions only** — no implementation required (Azure subscription needed).

### Goal
Deploy Flask to Azure Container Apps with:
- **Azure Container Registry (ACR)** — stores the Docker image
- **Azure Database for MySQL Flexible Server** — managed, persistent database
- **Azure Key Vault** — single source of truth for all secrets
- **Managed Identity** — Container App fetches secrets from Key Vault without storing credentials anywhere

---

### 1.1 Prerequisites

- Azure account with active subscription
- Azure CLI installed: `az --version`
- Docker installed and running
- App containerized (Lesson 02)
- `scripts/azure-vars.sh` and Key Vault provisioned (Lesson 01)

---

### 1.2 Install Azure CLI (if needed)

```bash
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
az login
```

---

### 1.3 Create core Azure resources

```bash
# Source shared config (created in Lesson 01)
source scripts/azure-vars.sh

# Resource group was created in Lesson 01 — skip if already exists
# az group create --name $RESOURCE_GROUP --location $LOCATION

# Azure Container Registry (no admin credentials — managed identity handles pulls)
az acr create \
  --resource-group $RESOURCE_GROUP \
  --name $ACR_NAME \
  --sku Basic

# Container Apps extension + environment
az extension add --name containerapp --upgrade
az containerapp env create \
  --name $APP_ENV \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION
```

---

### 1.4 Provision Azure Database for MySQL Flexible Server

```bash
# DB_SERVER is set by scripts/azure-vars.sh (globally unique, suffixed)
DB_ADMIN=dbadmin
DB_PASSWORD=$(openssl rand -base64 32)   # generate strong random password

az mysql flexible-server create \
  --resource-group $RESOURCE_GROUP \
  --name $DB_SERVER \
  --location $LOCATION \
  --admin-user $DB_ADMIN \
  --admin-password "$DB_PASSWORD" \
  --sku-name Standard_B1ms \
  --tier Burstable \
  --version 8.0 \
  --public-access None            # private — Container Apps VNet integration

# Create the application database
az mysql flexible-server db create \
  --resource-group $RESOURCE_GROUP \
  --server-name $DB_SERVER \
  --database-name employees_db

# Build the connection string
DB_HOST="${DB_SERVER}.mysql.database.azure.com"
DATABASE_URL="mysql+pymysql://${DB_ADMIN}:${DB_PASSWORD}@${DB_HOST}:3306/employees_db?ssl_ca=/etc/ssl/certs/ca-certificates.crt"
```

> Azure MySQL Flexible Server enforces TLS — the `ssl_ca` parameter is required.

---

### 1.5 Add DATABASE-URL to Key Vault

The Key Vault was provisioned in Lesson 01, which already stored `APP-ADMIN-USER`, `APP-ADMIN-PASSWORD`, and `FLASK-SECRET-KEY`. Now that the MySQL connection string is known, add it:

```bash
# source scripts/azure-vars.sh  # already loaded if running in the same session

# Store the connection string built in section 1.4
az keyvault secret set \
  --vault-name $KV_NAME \
  --name "DATABASE-URL" \
  --value "$DATABASE_URL"
```

> `DATABASE_URL` depends on the MySQL server created in section 1.4 — this is the only reason it was not stored in Lesson 01. All other secrets (`APP-ADMIN-PASSWORD`, `FLASK-SECRET-KEY`) are already in Key Vault.

---

### 1.6 Create Managed Identity and grant access

```bash
# IDENTITY_NAME is set by scripts/azure-vars.sh

# Create user-assigned managed identity
az identity create \
  --name $IDENTITY_NAME \
  --resource-group $RESOURCE_GROUP

IDENTITY_ID=$(az identity show \
  --name $IDENTITY_NAME \
  --resource-group $RESOURCE_GROUP \
  --query id -o tsv)

IDENTITY_PRINCIPAL=$(az identity show \
  --name $IDENTITY_NAME \
  --resource-group $RESOURCE_GROUP \
  --query principalId -o tsv)

KV_ID=$(az keyvault show --name $KV_NAME --query id -o tsv)
ACR_ID=$(az acr show --name $ACR_NAME --query id -o tsv)

# Key Vault Secrets User — read secrets at runtime
az role assignment create \
  --assignee $IDENTITY_PRINCIPAL \
  --role "Key Vault Secrets User" \
  --scope $KV_ID

# AcrPull — pull images from ACR (no ACR password needed)
az role assignment create \
  --assignee $IDENTITY_PRINCIPAL \
  --role "AcrPull" \
  --scope $ACR_ID
```

The identity has exactly two permissions: read secrets from Key Vault and pull images from ACR.

---

### 1.7 Push image to ACR

```bash
az acr login --name $ACR_NAME
docker build -t $ACR_NAME.azurecr.io/htmx-flask-app:latest .
docker push $ACR_NAME.azurecr.io/htmx-flask-app:latest
```

---

### 1.8 Deploy Container App with Key Vault secret references

```bash
KV_URI="https://${KV_NAME}.vault.azure.net/secrets"

az containerapp create \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --environment $APP_ENV \
  --image $ACR_NAME.azurecr.io/htmx-flask-app:latest \
  --registry-server $ACR_NAME.azurecr.io \
  --registry-identity $IDENTITY_ID \
  --user-assigned $IDENTITY_ID \
  --target-port 8000 \
  --ingress external \
  --min-replicas 0 \
  --max-replicas 3 \
  --secrets \
    "database-url=keyvaultref:${KV_URI}/DATABASE-URL,identityref:${IDENTITY_ID}" \
    "flask-secret-key=keyvaultref:${KV_URI}/FLASK-SECRET-KEY,identityref:${IDENTITY_ID}" \
  --env-vars \
    "DATABASE_URL=secretref:database-url" \
    "FLASK_SECRET_KEY=secretref:flask-secret-key" \
    "FLASK_ENV=production"
```

What happens here:
- `--secrets` declares Key Vault references — the Container App fetches values using the managed identity at runtime
- `--env-vars` maps those secrets into the container's environment via `secretref:` — the actual value is never stored in Container App config
- `--registry-identity` authenticates ACR image pulls using the same managed identity (no ACR password)
- `--min-replicas 0` scales to zero when idle (cost saving for dev/learning)

---

### 1.9 Verify deployment

```bash
az containerapp show \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --query "properties.configuration.ingress.fqdn" \
  --output tsv
```

Returns the public HTTPS URL. Azure Container Apps provides TLS termination automatically.

---

### Summary: where secrets live

| Secret | Stored in | Accessed by |
|---|---|---|
| `DATABASE_URL` | Key Vault | Container App via Managed Identity |
| `FLASK_SECRET_KEY` | Key Vault | Container App via Managed Identity |
| MySQL admin password | Key Vault (inside `DATABASE_URL`) | Never in code |
| ACR pull credentials | None — Managed Identity role | Container App at image pull |
| Azure deploy credentials | None — OIDC (see Lesson 05) | GitHub Actions at deploy time |

---

