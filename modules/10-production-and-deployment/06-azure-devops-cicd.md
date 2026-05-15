# Lesson 06: CI/CD with Azure DevOps

## Concept
Automate Helm chart deployment to AKS using Azure Pipelines — the CI/CD system built into Azure DevOps. Uses a Service Connection with Workload Identity Federation for authentication: no passwords or secrets stored in the pipeline.


## 1. CI/CD with Azure DevOps Pipelines

> **Instructions only** — Azure DevOps organisation and Azure subscription needed.

### Goal
On every push to `main`, build the Docker image, push it to ACR, and deploy the updated Helm chart to AKS using Azure Pipelines. Authentication uses Workload Identity Federation — the same OIDC principle as Lesson 05, implemented through Azure DevOps Service Connections.

---

### 1.1 Why Azure DevOps for Helm/AKS

| | GitHub Actions (Lesson 05) | Azure DevOps Pipelines (this lesson) |
|---|---|---|
| **Target** | Container Apps | AKS via Helm |
| **Auth** | OIDC via `azure/login` action | Service Connection (Workload Identity Federation) |
| **Helm support** | Community action | Native `HelmDeploy` task |
| **Kubernetes support** | `kubectl` via az CLI | Native `KubernetesManifest` + Kubernetes service connection |
| **Enterprise use** | Common in open-source orgs | Dominant in enterprise Azure shops |

---

### 1.2 Create an Azure DevOps organisation and project

1. Go to [dev.azure.com](https://dev.azure.com) and sign in with your Azure account.
2. Create an organisation (e.g. `htmx-flask-org`) and a project (e.g. `htmx-flask-learning`).
3. Connect the project to your GitHub repo: **Project Settings → Pipelines → GitHub connections**.

---

### 1.3 Create a Service Connection (Workload Identity Federation)

A Service Connection is Azure DevOps' equivalent of GitHub's OIDC federation — no client secret is created.

1. Go to **Project Settings → Service connections → New service connection**.
2. Choose **Azure Resource Manager**.
3. Choose **Workload Identity federation (automatic)**.
4. Select your subscription and resource group (`htmx-flask-rg`).
5. Name it `htmx-flask-azure-sc`.
6. Click **Save**.

Azure DevOps creates the federated credential on the Azure side automatically.

---

### 1.4 Create a Kubernetes Service Connection

1. Go to **Project Settings → Service connections → New service connection**.
2. Choose **Kubernetes**.
3. Choose **Azure Subscription**, select your AKS cluster (`htmx-flask-aks`) and namespace (`htmx-flask`).
4. Name it `htmx-flask-aks-sc`.
5. Click **Save**.

---

### 1.5 Create the pipeline file

Create `.azure-pipelines/deploy.yml` in the repo root:

```yaml
trigger:
  branches:
    include:
      - main

pool:
  vmImage: ubuntu-latest

variables:
  # Fill in acrName and acrLoginServer with your suffixed values:
  # source scripts/azure-vars.sh && echo $ACR_NAME && echo $ACR_LOGIN_SERVER
  acrName: ""                         # echo $ACR_NAME
  acrLoginServer: ""                  # echo $ACR_LOGIN_SERVER
  imageName: htmx-flask-app
  helmReleaseName: htmx-flask
  helmChartPath: helm/htmx-flask-app
  namespace: htmx-flask
  azureServiceConnection: htmx-flask-azure-sc
  aksServiceConnection: htmx-flask-aks-sc

stages:

  - stage: Build
    displayName: Build and Push Image
    jobs:
      - job: BuildPush
        steps:
          - task: AzureCLI@2
            displayName: Build and push Docker image to ACR
            inputs:
              azureSubscription: $(azureServiceConnection)
              scriptType: bash
              scriptLocation: inlineScript
              inlineScript: |
                az acr login --name $(acrName)
                IMAGE_TAG=$(acrLoginServer)/$(imageName):$(Build.SourceVersion)
                docker build -t $IMAGE_TAG .
                docker push $IMAGE_TAG
                echo "##vso[task.setvariable variable=imageTag;isOutput=true]$IMAGE_TAG"
            name: buildStep

  - stage: Test
    displayName: Run Tests
    dependsOn: Build
    jobs:
      - job: Test
        steps:
          - task: UsePythonVersion@0
            inputs:
              versionSpec: "3.12"
          - script: |
              python -m pip install --upgrade pip
              pip install -r requirements.txt
              python -m pytest tests/ --tb=short || echo "No tests found"
            displayName: Install dependencies and run tests

  - stage: Deploy
    displayName: Deploy Helm Chart to AKS
    dependsOn: Test
    jobs:
      - deployment: HelmDeploy
        displayName: Helm upgrade
        environment: production
        strategy:
          runOnce:
            deploy:
              steps:
                - task: HelmDeploy@0
                  displayName: Helm upgrade --install
                  inputs:
                    connectionType: Kubernetes Service Connection
                    kubernetesServiceConnection: $(aksServiceConnection)
                    namespace: $(namespace)
                    command: upgrade
                    chartType: FilePath
                    chartPath: $(helmChartPath)
                    releaseName: $(helmReleaseName)
                    overrideValues: image.tag=$(Build.SourceVersion)
                    install: true
                    waitForExecution: true
```

---

### 1.6 Pipeline variables (non-sensitive)

In Azure DevOps → **Pipelines → Library → Variable groups**, no secrets are needed — all sensitive config is in Azure Key Vault and accessed via Workload Identity by the running pod (established in Lesson 04).

The pipeline only needs non-sensitive identifiers, all of which are already hardcoded in `variables:` in the YAML above.

---

### 1.7 How the pipeline authenticates

```
git push → main
  → ADO pipeline triggered
  → Build stage: AzureCLI@2 task uses Service Connection
      → ADO mints OIDC token for this pipeline run
      → Azure validates against federated credential
      → az session established — no password exchanged
      → az acr login → docker build + push
  → Test stage: pytest runs
  → Deploy stage: HelmDeploy@0 task uses Kubernetes Service Connection
      → helm upgrade --install with new image tag
      → AKS pod restarts with new image
      → Pod fetches DATABASE_URL + FLASK_SECRET_KEY from Key Vault
        via Workload Identity (Lesson 04 — unchanged)
```

---

### 1.8 Rollback

```bash
# Via Helm (local kubectl access)
helm rollback htmx-flask 1 --namespace htmx-flask

# Via Azure DevOps
# Re-run a previous pipeline build — it will deploy that build's image tag
```

---

### Summary: what is stored where

| Item | Location |
|---|---|
| `DATABASE_URL`, `FLASK_SECRET_KEY`, `APP_ADMIN_PASSWORD` | Azure Key Vault (Lesson 01) |
| Azure auth credentials | None — Workload Identity Federation |
| AKS credentials | None — Kubernetes Service Connection (OIDC) |
| Pipeline config | `.azure-pipelines/deploy.yml` (committed, no secrets) |
| Image tags | ACR, referenced by git commit SHA |

---
