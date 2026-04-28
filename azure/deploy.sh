#!/usr/bin/env bash
set -euo pipefail

RG_NAME=${1:-}
ENV=${2:-dev}

if [ -z "$RG_NAME" ]; then
  echo "Usage: ./azure/deploy.sh <resource-group> [env]"
  exit 2
fi

PARAMS="azure/iac/parameters/${ENV}.parameters.json"

az deployment group create \
  --resource-group "$RG_NAME" \
  --template-file azure/iac/main.bicep \
  --parameters "@${PARAMS}"

echo "Deployment complete."
