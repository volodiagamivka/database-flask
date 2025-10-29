#!/bin/bash

set -e

echo "=========================================="
echo "🧪 Локальне тестування Docker образу"
echo "=========================================="

echo ""
echo "1️⃣ Побудова Docker образу..."
docker build -t hospital-flask-app:test .

echo ""
echo "2️⃣ Запуск контейнера..."
docker-compose up -d

echo ""
echo "⏳ Очікування запуску додатку (30 секунд)..."
sleep 30

echo ""
echo "3️⃣ Перевірка здоров'я контейнера..."
docker-compose ps

echo ""
echo "4️⃣ Тестування API endpoints..."

echo "  • GET /api/v1/patients/"
curl -s http://localhost:5001/api/v1/patients/ | python3 -m json.tool || echo "✗ Помилка"

echo ""
echo "  • GET /api/v1/hospitals/"
curl -s http://localhost:5001/api/v1/hospitals/ | python3 -m json.tool || echo "✗ Помилка"

echo ""
echo "  • GET /api/v1/doctors/"
curl -s http://localhost:5001/api/v1/doctors/ | python3 -m json.tool || echo "✗ Помилка"

echo ""
echo "5️⃣ Перевірка логів..."
docker-compose logs --tail=20

echo ""
echo "=========================================="
echo "✅ Тестування завершено!"
echo ""
echo "Swagger UI: http://localhost:5001/swagger/"
echo ""
echo "Для зупинки контейнера: docker-compose down"
echo "=========================================="

