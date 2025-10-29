#!/bin/bash

CONTAINER_APP_NAME="hospital-app"
RESOURCE_GROUP="hospital-rg"
LOG_FILE="scaling_log_$(date +%Y%m%d_%H%M%S).txt"

echo "=========================================="
echo "📊 Моніторинг автомасштабування"
echo "=========================================="
echo "Container App: $CONTAINER_APP_NAME"
echo "Resource Group: $RESOURCE_GROUP"
echo "Log File: $LOG_FILE"
echo "=========================================="
echo ""

echo "Час,Репліки,CPU,Memory,Requests" > $LOG_FILE

echo "Натисніть Ctrl+C для зупинки моніторингу"
echo ""

trap "echo ''; echo 'Моніторинг зупинено. Лог збережено в $LOG_FILE'; exit 0" INT

while true; do
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    
    REPLICAS=$(az containerapp replica list \
        --name $CONTAINER_APP_NAME \
        --resource-group $RESOURCE_GROUP \
        --query "length(@)" \
        --output tsv 2>/dev/null || echo "N/A")
    
    CPU=$(az monitor metrics list \
        --resource $(az containerapp show --name $CONTAINER_APP_NAME --resource-group $RESOURCE_GROUP --query id -o tsv 2>/dev/null) \
        --metric "UsageNanoCores" \
        --interval PT1M \
        --query "value[0].timeseries[0].data[-1].average" \
        --output tsv 2>/dev/null || echo "N/A")
    
    MEMORY=$(az monitor metrics list \
        --resource $(az containerapp show --name $CONTAINER_APP_NAME --resource-group $RESOURCE_GROUP --query id -o tsv 2>/dev/null) \
        --metric "WorkingSetBytes" \
        --interval PT1M \
        --query "value[0].timeseries[0].data[-1].average" \
        --output tsv 2>/dev/null || echo "N/A")
    
    REQUESTS=$(az monitor metrics list \
        --resource $(az containerapp show --name $CONTAINER_APP_NAME --resource-group $RESOURCE_GROUP --query id -o tsv 2>/dev/null) \
        --metric "Requests" \
        --interval PT1M \
        --query "value[0].timeseries[0].data[-1].total" \
        --output tsv 2>/dev/null || echo "N/A")
    
    if [ "$CPU" != "N/A" ] && [ "$CPU" != "" ]; then
        CPU_PERCENT=$(echo "scale=2; $CPU / 10000000" | bc)
    else
        CPU_PERCENT="N/A"
    fi
    
    if [ "$MEMORY" != "N/A" ] && [ "$MEMORY" != "" ]; then
        MEMORY_MB=$(echo "scale=2; $MEMORY / 1048576" | bc)
    else
        MEMORY_MB="N/A"
    fi
    
    echo "[$TIMESTAMP] Репліки: $REPLICAS | CPU: ${CPU_PERCENT}% | Memory: ${MEMORY_MB}MB | Requests: $REQUESTS"
    
    echo "$TIMESTAMP,$REPLICAS,$CPU_PERCENT,$MEMORY_MB,$REQUESTS" >> $LOG_FILE
    
    sleep 10
done

