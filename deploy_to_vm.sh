#!/bin/bash
# Скрипт для автоматичного деплою на Azure VM
# Використання: ./deploy_to_vm.sh YOUR_VM_IP path/to/your/key.pem

set -e  # Зупинити скрипт при помилці

# Кольори для виводу
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Перевірка аргументів
if [ $# -ne 2 ]; then
    echo -e "${RED}❌ Помилка: Не вистачає аргументів${NC}"
    echo "Використання: $0 VM_IP_ADDRESS PATH_TO_KEY"
    echo "Приклад: $0 20.123.45.67 ~/Downloads/hospital-vm-key.pem"
    exit 1
fi

VM_IP=$1
SSH_KEY=$2
VM_USER="azureuser"
PROJECT_DIR="hospital-management-system"

echo -e "${BLUE}🚀 Початок деплою на Azure VM${NC}"
echo -e "${BLUE}📍 VM IP: $VM_IP${NC}"
echo ""

# Перевірка доступності VM
echo -e "${BLUE}🔍 Перевірка доступності VM...${NC}"
if ssh -i "$SSH_KEY" -o ConnectTimeout=5 "$VM_USER@$VM_IP" "echo 'Connected'" > /dev/null 2>&1; then
    echo -e "${GREEN}✅ VM доступна${NC}"
else
    echo -e "${RED}❌ Не вдалося підключитися до VM${NC}"
    exit 1
fi

# Оновлення коду з GitHub
echo -e "${BLUE}📥 Оновлення коду з GitHub...${NC}"
ssh -i "$SSH_KEY" "$VM_USER@$VM_IP" << 'EOF'
    cd ~/hospital-management-system
    git pull origin main
EOF

# Встановлення/оновлення залежностей
echo -e "${BLUE}📦 Встановлення залежностей...${NC}"
ssh -i "$SSH_KEY" "$VM_USER@$VM_IP" << 'EOF'
    cd ~/hospital-management-system
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
EOF

# Перезапуск сервісу
echo -e "${BLUE}🔄 Перезапуск сервісу...${NC}"
ssh -i "$SSH_KEY" "$VM_USER@$VM_IP" << 'EOF'
    sudo systemctl restart hospital-app
    sleep 2
    sudo systemctl status hospital-app --no-pager
EOF

echo ""
echo -e "${GREEN}✅ Деплой завершено успішно!${NC}"
echo -e "${BLUE}🌐 Swagger UI: http://$VM_IP/swagger/${NC}"

