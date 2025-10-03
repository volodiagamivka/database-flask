#!/bin/bash

echo "🔍 Monitoring Hospital API..."

# Check if service is running
if systemctl is-active --quiet hospital-app; then
    echo "✅ Service is running"
else
    echo "❌ Service is not running"
    exit 1
fi

# Check API endpoints
echo "🌐 Testing API endpoints..."

# Test patients
if curl -s -f http://localhost:5000/api/v1/patients/ > /dev/null; then
    echo "✅ Patients API working"
else
    echo "❌ Patients API failed"
fi

# Test hospitals
if curl -s -f http://localhost:5000/api/v1/hospitals/ > /dev/null; then
    echo "✅ Hospitals API working"
else
    echo "❌ Hospitals API failed"
fi

# Test Swagger UI
if curl -s -f http://localhost:5000/swagger/ > /dev/null; then
    echo "✅ Swagger UI working"
else
    echo "❌ Swagger UI failed"
fi

echo "🎉 Monitoring completed!"
