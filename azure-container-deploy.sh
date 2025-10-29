#!/bin/bash

set -e

echo "=========================================="
echo "🚀 Azure Container Deployment Script"
echo "=========================================="

RESOURCE_GROUP="hospital-rg"
LOCATION="eastus"
ACR_NAME="hospitalacrregistry"
CONTAINER_APP_ENV="hospital-env"
CONTAINER_APP_NAME="hospital-app"
IMAGE_NAME="hospital-flask-app"
IMAGE_TAG="latest"

echo ""
echo "📋 Конфігурація:"
echo "  Resource Group: $RESOURCE_GROUP"
echo "  Location: $LOCATION"
echo "  ACR Name: $ACR_NAME"
echo "  Container App: $CONTAINER_APP_NAME"
echo ""

read -p "Продовжити? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 1
fi

echo ""
echo "1️⃣ Створення Resource Group..."
az group create \
  --name $RESOURCE_GROUP \
  --location $LOCATION

echo ""
echo "2️⃣ Створення Azure Container Registry..."
az acr create \
  --resource-group $RESOURCE_GROUP \
  --name $ACR_NAME \
  --sku Basic \
  --admin-enabled true

echo ""
echo "3️⃣ Логін до ACR..."
az acr login --name $ACR_NAME

echo ""
echo "4️⃣ Побудова Docker образу..."
docker build -t $IMAGE_NAME:$IMAGE_TAG .

echo ""
echo "5️⃣ Тегування образу для ACR..."
ACR_LOGIN_SERVER=$(az acr show --name $ACR_NAME --query loginServer --output tsv)
docker tag $IMAGE_NAME:$IMAGE_TAG $ACR_LOGIN_SERVER/$IMAGE_NAME:$IMAGE_TAG

echo ""
echo "6️⃣ Завантаження образу в ACR..."
docker push $ACR_LOGIN_SERVER/$IMAGE_NAME:$IMAGE_TAG

echo ""
echo "7️⃣ Отримання креденшалів ACR..."
ACR_USERNAME=$(az acr credential show --name $ACR_NAME --query username --output tsv)
ACR_PASSWORD=$(az acr credential show --name $ACR_NAME --query passwords[0].value --output tsv)

echo ""
echo "8️⃣ Створення Container Apps Environment..."
az containerapp env create \
  --name $CONTAINER_APP_ENV \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION

echo ""
echo "9️⃣ Створення Container App з автомасштабуванням..."
az containerapp create \
  --name $CONTAINER_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --environment $CONTAINER_APP_ENV \
  --image $ACR_LOGIN_SERVER/$IMAGE_NAME:$IMAGE_TAG \
  --registry-server $ACR_LOGIN_SERVER \
  --registry-username $ACR_USERNAME \
  --registry-password $ACR_PASSWORD \
  --target-port 5000 \
  --ingress external \
  --min-replicas 1 \
  --max-replicas 10 \
  --cpu 0.5 \
  --memory 1.0Gi \
  --env-vars \
    DB_HOST=secretref:db-host \
    DB_USER=secretref:db-user \
    DB_PASSWORD=secretref:db-password \
    DB_NAME=secretref:db-name \
    DB_PORT=secretref:db-port \
    SECRET_KEY=secretref:secret-key

echo ""
echo "🔟 Налаштування автомасштабування..."
az containerapp update \
  --name $CONTAINER_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --scale-rule-name cpu-scale \
  --scale-rule-type cpu \
  --scale-rule-metadata type=Utilization value=70

az containerapp update \
  --name $CONTAINER_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --scale-rule-name memory-scale \
  --scale-rule-type memory \
  --scale-rule-metadata type=Utilization value=75

echo ""
echo "✅ Деплой завершено!"
echo ""
echo "📊 Отримання URL додатку..."
APP_URL=$(az containerapp show \
  --name $CONTAINER_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --query properties.configuration.ingress.fqdn \
  --output tsv)

echo ""
echo "=========================================="
echo "✨ Ваш додаток доступний за адресою:"
echo "   https://$APP_URL"
echo "   Swagger: https://$APP_URL/swagger/"
echo "=========================================="

