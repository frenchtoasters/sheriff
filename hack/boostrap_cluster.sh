#!/usr/bin/env bash

set -euo pipefail

# Config
NAMESPACE=${NAMESPACE:-sheriff}
RELEASE_NAME=${RELEASE_NAME:-nfs-server}
POSTGRES_PVC_NAME="postgres-pvc"

echo "🔧 Checking if namespace '$NAMESPACE' exists..."
if ! kubectl get namespace "$NAMESPACE" > /dev/null 2>&1; then
  echo "🚀 Namespace '$NAMESPACE' does not exist. Creating..."
  kubectl create namespace "$NAMESPACE"
else
  echo "✅ Namespace '$NAMESPACE' already exists."
fi

# Add Helm repo and update
helm repo add nfs-subdir-external-provisioner https://kubernetes-sigs.github.io/nfs-subdir-external-provisioner/
helm repo update

helm install nfs-client nfs-subdir-external-provisioner/nfs-subdir-external-provisioner \
  --namespace sheriff \
  --create-namespace \
  --set nfs.server=nfs-server.sheriff.svc.cluster.local \
  --set nfs.path=/nfsshare \
  --set storageClass.defaultClass=true

echo "✅ NFS Server Provisioner deployed successfully."

echo "📦 Creating Postgres PVC, Deployment, and Service from hack/postgres.yml..."
kubectl apply -n $NAMESPACE -f hack/pvc.yml
kubectl apply -n $NAMESPACE -f hack/postgres.yml
kubectl apply -n $NAMESPACE -f hack/deployment.yml

echo "✅ Postgres resources applied in namespace '$NAMESPACE'."

