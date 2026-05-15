# Lesson 04: Helm Deployment to AKS

## Concept
Deploy the Flask app to Azure Kubernetes Service (AKS) using Helm charts and the Azure Key Vault Secrets Store CSI driver — secrets are injected into pods from Key Vault via Workload Identity, never stored in Kubernetes manifests or GitHub.


## 1. Helm Deployment to AKS with Key Vault

> **Instructions only** — no implementation required (Azure subscription needed).

### Goal
Package the Flask app as a Helm chart and deploy it to AKS. `DATABASE_URL` and `FLASK_SECRET_KEY` are served from Azure Key Vault directly into the pod — they never appear in Kubernetes manifests, Helm values, or GitHub.

---

### 1.1 Prerequisites

- Azure CLI, `kubectl`, and Helm 3 installed
- App image pushed to ACR (Lesson 03)
- Key Vault populated with `APP-ADMIN-PASSWORD`, `FLASK-SECRET-KEY` (Lesson 01) and `DATABASE-URL` (Lesson 03)

---

### 1.2 Create AKS cluster with required addons

```bash
# Source shared config (created in Lesson 01)
source scripts/azure-vars.sh

az aks create \
  --resource-group $RESOURCE_GROUP \
  --name $CLUSTER_NAME \
  --node-count 2 \
  --node-vm-size Standard_B2s \
  --enable-addons azure-keyvault-secrets-provider \
  --enable-oidc-issuer \
  --enable-workload-identity \
  --attach-acr $ACR_NAME \
  --generate-ssh-keys

# Fetch kubeconfig
az aks get-credentials \
  --resource-group $RESOURCE_GROUP \
  --name $CLUSTER_NAME
```

`--enable-addons azure-keyvault-secrets-provider` installs the Secrets Store CSI driver.
`--enable-oidc-issuer` + `--enable-workload-identity` enable pod-level Azure identity without credentials.

---

### 1.3 Create Workload Identity for the pod

Workload Identity lets pods authenticate to Azure Key Vault using a Kubernetes service account — no credentials anywhere in the pod spec.

```bash
# KV_NAME, IDENTITY_NAME_WI, NAMESPACE, SERVICE_ACCOUNT all set by scripts/azure-vars.sh
# Use IDENTITY_NAME_WI for AKS (separate identity from Container Apps)
IDENTITY_NAME=$IDENTITY_NAME_WI

# Get the AKS OIDC issuer URL
OIDC_ISSUER=$(az aks show \
  --resource-group $RESOURCE_GROUP \
  --name $CLUSTER_NAME \
  --query "oidcIssuerProfile.issuerUrl" -o tsv)

# Create managed identity
az identity create \
  --name $IDENTITY_NAME \
  --resource-group $RESOURCE_GROUP

IDENTITY_CLIENT_ID=$(az identity show \
  --name $IDENTITY_NAME \
  --resource-group $RESOURCE_GROUP \
  --query clientId -o tsv)

IDENTITY_PRINCIPAL=$(az identity show \
  --name $IDENTITY_NAME \
  --resource-group $RESOURCE_GROUP \
  --query principalId -o tsv)

# Grant Key Vault Secrets User
KV_ID=$(az keyvault show --name $KV_NAME --query id -o tsv)
az role assignment create \
  --assignee $IDENTITY_PRINCIPAL \
  --role "Key Vault Secrets User" \
  --scope $KV_ID

# Create federated credential — trusts the Kubernetes service account in this namespace
az identity federated-credential create \
  --name htmx-flask-federated \
  --identity-name $IDENTITY_NAME \
  --resource-group $RESOURCE_GROUP \
  --issuer $OIDC_ISSUER \
  --subject "system:serviceaccount:${NAMESPACE}:${SERVICE_ACCOUNT}" \
  --audience api://AzureADTokenAudience
```

---

### 1.4 Helm chart structure

Create this directory layout in the repo root:

```
helm/
└── htmx-flask-app/
    ├── Chart.yaml
    ├── values.yaml
    └── templates/
        ├── namespace.yaml
        ├── serviceaccount.yaml
        ├── secretproviderclass.yaml
        ├── deployment.yaml
        └── service.yaml
```

---

### 1.5 Chart.yaml

```yaml
apiVersion: v2
name: htmx-flask-app
description: HTMX + Flask employee dashboard
type: application
version: 0.1.0
appVersion: "1.0.0"
```

---

### 1.6 values.yaml

> After running `source scripts/azure-vars.sh`, substitute the placeholders below:
> - `image.repository` → value of `echo "${ACR_LOGIN_SERVER}/htmx-flask-app"`
> - `keyVault.name` → value of `echo $KV_NAME`
> - `workloadIdentity.clientId` → value of `az identity show --name $IDENTITY_NAME_WI --query clientId -o tsv`

```yaml
image:
  repository: <ACR_LOGIN_SERVER>/htmx-flask-app   # echo $ACR_LOGIN_SERVER after sourcing vars
  tag: latest
  pullPolicy: IfNotPresent

replicaCount: 2

service:
  type: LoadBalancer
  port: 80
  targetPort: 8000

keyVault:
  name: ""          # echo $KV_NAME after sourcing scripts/azure-vars.sh
  tenantId: ""      # az account show --query tenantId -o tsv

workloadIdentity:
  clientId: ""      # az identity show --name $IDENTITY_NAME_WI --query clientId -o tsv
  serviceAccountName: htmx-flask-sa

namespace: htmx-flask
```

> `tenantId` and `clientId` are non-sensitive identifiers — they can safely live in `values.yaml` committed to the repo.

---

### 1.7 templates/namespace.yaml

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: {{ .Values.namespace }}
```

---

### 1.8 templates/serviceaccount.yaml

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: {{ .Values.workloadIdentity.serviceAccountName }}
  namespace: {{ .Values.namespace }}
  annotations:
    azure.workload.identity/client-id: {{ .Values.workloadIdentity.clientId }}
  labels:
    azure.workload.identity/use: "true"
```

---

### 1.9 templates/secretproviderclass.yaml

`SecretProviderClass` tells the CSI driver which Key Vault secrets to sync and how to expose them as a Kubernetes Secret.

```yaml
apiVersion: secrets-store.csi.x-k8s.io/v1
kind: SecretProviderClass
metadata:
  name: htmx-flask-kv-secrets
  namespace: {{ .Values.namespace }}
spec:
  provider: azure
  secretObjects:
    - secretName: htmx-flask-app-secrets
      type: Opaque
      data:
        - objectName: DATABASE-URL
          key: DATABASE_URL
        - objectName: FLASK-SECRET-KEY
          key: FLASK_SECRET_KEY
  parameters:
    usePodIdentity: "false"
    clientID: {{ .Values.workloadIdentity.clientId }}
    keyvaultName: {{ .Values.keyVault.name }}
    tenantId: {{ .Values.keyVault.tenantId }}
    objects: |
      array:
        - |
          objectName: DATABASE-URL
          objectType: secret
        - |
          objectName: FLASK-SECRET-KEY
          objectType: secret
```

---

### 1.10 templates/deployment.yaml

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: htmx-flask-app
  namespace: {{ .Values.namespace }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      app: htmx-flask-app
  template:
    metadata:
      labels:
        app: htmx-flask-app
        azure.workload.identity/use: "true"
    spec:
      serviceAccountName: {{ .Values.workloadIdentity.serviceAccountName }}
      containers:
        - name: htmx-flask-app
          image: {{ .Values.image.repository }}:{{ .Values.image.tag }}
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          ports:
            - containerPort: {{ .Values.service.targetPort }}
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: htmx-flask-app-secrets
                  key: DATABASE_URL
            - name: FLASK_SECRET_KEY
              valueFrom:
                secretKeyRef:
                  name: htmx-flask-app-secrets
                  key: FLASK_SECRET_KEY
            - name: FLASK_ENV
              value: production
          volumeMounts:
            - name: secrets-store
              mountPath: /mnt/secrets
              readOnly: true
      volumes:
        - name: secrets-store
          csi:
            driver: secrets-store.csi.k8s.io
            readOnly: true
            volumeAttributes:
              secretProviderClass: htmx-flask-kv-secrets
```

> The volume mount is required — the CSI driver only creates the Kubernetes Secret (`htmx-flask-app-secrets`) when at least one pod has the volume mounted and active.

---

### 1.11 templates/service.yaml

```yaml
apiVersion: v1
kind: Service
metadata:
  name: htmx-flask-app
  namespace: {{ .Values.namespace }}
spec:
  type: {{ .Values.service.type }}
  selector:
    app: htmx-flask-app
  ports:
    - protocol: TCP
      port: {{ .Values.service.port }}
      targetPort: {{ .Values.service.targetPort }}
```

---

### 1.12 Deploy with Helm

```bash
# Fill in values.yaml: keyVault.tenantId and workloadIdentity.clientId

# First install (or upgrade if already installed)
helm upgrade --install htmx-flask ./helm/htmx-flask-app \
  --namespace htmx-flask \
  --create-namespace \
  --set image.tag=$(git rev-parse --short HEAD)

# Watch rollout
kubectl rollout status deployment/htmx-flask-app -n htmx-flask

# Get external IP (LoadBalancer may take ~60s to assign)
kubectl get service htmx-flask-app -n htmx-flask
```

Update image after a new build:

```bash
helm upgrade htmx-flask ./helm/htmx-flask-app \
  --namespace htmx-flask \
  --set image.tag=<new-sha>
```

Roll back to previous Helm release:

```bash
helm rollback htmx-flask 1   # roll back to revision 1
helm history htmx-flask      # list all revisions
```

---

### Summary: how secrets flow

```
Azure Key Vault  (DATABASE-URL, FLASK-SECRET-KEY)
  ↓  CSI driver authenticates via Workload Identity (no credentials in pod)
SecretProviderClass  (maps Key Vault names → Kubernetes Secret keys)
  ↓  created automatically when pod starts, lives only in-cluster
Kubernetes Secret  htmx-flask-app-secrets
  ↓  secretKeyRef in pod spec
Pod env vars: DATABASE_URL, FLASK_SECRET_KEY
```

No secrets appear in Helm values, templates, manifests, or GitHub at any point.

---
