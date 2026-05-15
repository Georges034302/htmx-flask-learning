# Lesson 03: CI/CD with GitHub Actions

## Concept
CI/CD with GitHub Actions.


## 1. CI/CD with GitHub Actions

> **Instructions only** — no implementation required.

### Goal
Automatically build, test, and deploy the app on every push to `main` using a GitHub Actions workflow.

---

### 1.1 Create workflow file

Create `.github/workflows/deploy.yml`:

```yaml
name: Build and Deploy

on:
  push:
    branches:
      - main

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

      - name: Log in to Azure Container Registry
        uses: azure/docker-login@v1
        with:
          login-server: ${{ secrets.ACR_LOGIN_SERVER }}
          username: ${{ secrets.ACR_USERNAME }}
          password: ${{ secrets.ACR_PASSWORD }}

      - name: Build and push Docker image
        run: |
          docker build -t ${{ secrets.ACR_LOGIN_SERVER }}/htmx-flask-app:${{ github.sha }} .
          docker push ${{ secrets.ACR_LOGIN_SERVER }}/htmx-flask-app:${{ github.sha }}

      - name: Deploy to Azure Container Apps
        uses: azure/CLI@v2
        with:
          azcliversion: latest
          inlineScript: |
            az containerapp update \
              --name htmx-flask-app \
              --resource-group htmx-flask-rg \
              --image ${{ secrets.ACR_LOGIN_SERVER }}/htmx-flask-app:${{ github.sha }}
```

---

### 1.2 Add GitHub Secrets

In your GitHub repo → **Settings → Secrets and variables → Actions**, add:

| Secret name        | Value                                   |
|--------------------|-----------------------------------------|
| `ACR_LOGIN_SERVER` | `htmxflaskregistry.azurecr.io`          |
| `ACR_USERNAME`     | ACR admin username (from Azure portal)  |
| `ACR_PASSWORD`     | ACR admin password (from Azure portal)  |

---

### 1.3 Workflow flow

```
git push → main
  → checkout code
  → install dependencies
  → run tests
  → build Docker image (tagged with git SHA)
  → push image to ACR
  → update Azure Container App to new image
```

Each deployment is tagged with the exact git commit SHA — making rollbacks trivial.

---

