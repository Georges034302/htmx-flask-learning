# Lesson 38: Deploy to Azure

Included step: 48

## Concept
Deploy to Azure.


## 48) Deploy to Azure

> **Instructions only** — no implementation required (Azure subscription needed).

### Goal
Deploy the Docker container image to Azure Container Apps — a serverless container platform that handles scaling, HTTPS, and infrastructure automatically.

---

### 48.1 Prerequisites

- Azure account with active subscription
- Azure CLI installed: `az --version`
- Docker installed and running
- App containerized per Step 47

---

### 48.2 Install Azure CLI (if needed)

```bash
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
az login
```

---

### 48.3 Create Azure resources

```bash
# Set variables
RESOURCE_GROUP=htmx-flask-rg
LOCATION=eastus
ACR_NAME=htmxflaskregistry
APP_ENV=htmx-flask-env
APP_NAME=htmx-flask-app

# Create resource group
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create Azure Container Registry
az acr create --resource-group $RESOURCE_GROUP \
              --name $ACR_NAME \
              --sku Basic \
              --admin-enabled true
```

---

### 48.4 Push image to Azure Container Registry

```bash
# Login to ACR
az acr login --name $ACR_NAME

# Tag and push image
docker tag htmx-flask-app $ACR_NAME.azurecr.io/htmx-flask-app:latest
docker push $ACR_NAME.azurecr.io/htmx-flask-app:latest
```

---

### 48.5 Create Container Apps environment and deploy

```bash
# Install Container Apps extension
az extension add --name containerapp

# Create environment
az containerapp env create \
  --name $APP_ENV \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION

# Deploy container
az containerapp create \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --environment $APP_ENV \
  --image $ACR_NAME.azurecr.io/htmx-flask-app:latest \
  --registry-server $ACR_NAME.azurecr.io \
  --target-port 8000 \
  --ingress external \
  --min-replicas 1 \
  --max-replicas 3
```

---

### 48.6 Verify deployment

```bash
az containerapp show \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --query "properties.configuration.ingress.fqdn" \
  --output tsv
```

Returns the public HTTPS URL for your deployed app.

---

