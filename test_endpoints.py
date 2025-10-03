"""
Скрипт для автоматичного тестування API endpoints
Використання: python test_endpoints.py [BASE_URL]
Приклад: python test_endpoints.py http://20.123.45.67:5000
"""

import requests
import json
import sys
from datetime import datetime

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    END = '\033[0m'

def print_success(message):
    print(f"{Colors.GREEN}✅ {message}{Colors.END}")

def print_error(message):
    print(f"{Colors.RED}❌ {message}{Colors.END}")

def print_info(message):
    print(f"{Colors.BLUE}ℹ️  {message}{Colors.END}")

def print_warning(message):
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.END}")

def test_endpoint(base_url, endpoint, method='GET', data=None, description=""):
    """Тестує окремий endpoint"""
    url = f"{base_url}{endpoint}"
    print_info(f"Тестування: {method} {endpoint}")
    if description:
        print(f"   Опис: {description}")
    
    try:
        if method == 'GET':
            response = requests.get(url, timeout=10)
        elif method == 'POST':
            response = requests.post(url, json=data, timeout=10)
        elif method == 'PUT':
            response = requests.put(url, json=data, timeout=10)
        elif method == 'DELETE':
            response = requests.delete(url, timeout=10)
        else:
            print_error(f"Невідомий метод: {method}")
            return None
        
        if response.status_code in [200, 201]:
            print_success(f"Статус: {response.status_code}")
            try:
                data = response.json()
                print(f"   Відповідь: {json.dumps(data, ensure_ascii=False, indent=2)[:200]}...")
            except:
                print(f"   Відповідь: {response.text[:200]}")
            return response
        else:
            print_warning(f"Статус: {response.status_code}")
            print(f"   Відповідь: {response.text[:200]}")
            return response
            
    except requests.exceptions.ConnectionError:
        print_error("Не вдалося підключитися до сервера")
        return None
    except requests.exceptions.Timeout:
        print_error("Тайм-аут з'єднання")
        return None
    except Exception as e:
        print_error(f"Помилка: {str(e)}")
        return None

def run_tests(base_url):
    """Запускає набір тестів для API"""
    print("\n" + "="*60)
    print(f"🚀 Тестування Hospital Management API")
    print(f"📍 URL: {base_url}")
    print(f"⏰ Час: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60 + "\n")
    
    tests_passed = 0
    tests_failed = 0
    
    # Тест 1: Swagger UI
    print("\n📋 Тест 1: Перевірка Swagger UI")
    response = test_endpoint(base_url, "/swagger/", description="Swagger документація")
    if response and response.status_code == 200:
        tests_passed += 1
    else:
        tests_failed += 1
    
    # Тест 2: Пацієнти - отримання списку
    print("\n📋 Тест 2: Отримання списку пацієнтів")
    response = test_endpoint(base_url, "/api/v1/patients", description="GET всіх пацієнтів")
    if response and response.status_code == 200:
        tests_passed += 1
    else:
        tests_failed += 1
    
    # Тест 3: Лікарі - отримання списку
    print("\n📋 Тест 3: Отримання списку лікарів")
    response = test_endpoint(base_url, "/api/v1/doctors", description="GET всіх лікарів")
    if response and response.status_code == 200:
        tests_passed += 1
    else:
        tests_failed += 1
    
    # Тест 4: Лікарні - отримання списку
    print("\n📋 Тест 4: Отримання списку лікарень")
    response = test_endpoint(base_url, "/api/v1/hospitals", description="GET всіх лікарень")
    if response and response.status_code == 200:
        tests_passed += 1
    else:
        tests_failed += 1
    
    # Тест 5: Медикаменти - отримання списку
    print("\n📋 Тест 5: Отримання списку медикаментів")
    response = test_endpoint(base_url, "/api/v1/medications", description="GET всіх медикаментів")
    if response and response.status_code == 200:
        tests_passed += 1
    else:
        tests_failed += 1
    
    # Тест 6: Відділення - отримання списку
    print("\n📋 Тест 6: Отримання списку відділень")
    response = test_endpoint(base_url, "/api/v1/departments", description="GET всіх відділень")
    if response and response.status_code == 200:
        tests_passed += 1
    else:
        tests_failed += 1
    
    # Результати
    print("\n" + "="*60)
    print("📊 РЕЗУЛЬТАТИ ТЕСТУВАННЯ")
    print("="*60)
    total_tests = tests_passed + tests_failed
    print(f"Всього тестів: {total_tests}")
    print_success(f"Успішно: {tests_passed}")
    if tests_failed > 0:
        print_error(f"Провалено: {tests_failed}")
    
    success_rate = (tests_passed / total_tests * 100) if total_tests > 0 else 0
    print(f"\n📈 Успішність: {success_rate:.1f}%")
    
    if success_rate == 100:
        print_success("\n🎉 Всі тести пройдено успішно!")
        print_info("Ваш API готовий до здачі!")
    elif success_rate >= 80:
        print_warning("\n⚠️  Більшість тестів пройдено, але є проблеми")
        print_info("Перевірте endpoints що не працюють")
    else:
        print_error("\n❌ Багато тестів провалено")
        print_info("Перевірте чи запущений сервер та база даних")
    
    print("="*60 + "\n")

def main():
    """Головна функція"""
    if len(sys.argv) > 1:
        base_url = sys.argv[1].rstrip('/')
    else:
        print_info("URL не вказано, використовую localhost:5000")
        print_info("Використання: python test_endpoints.py http://YOUR_VM_IP:5000")
        base_url = "http://localhost:5000"
    
    run_tests(base_url)
    
    print("\n💡 Порада:")
    print("   Для тестування на Azure VM використайте:")
    print("   python test_endpoints.py http://YOUR_VM_IP:5000")
    print("\n   Для детального тестування відкрийте Swagger UI:")
    print(f"   {base_url}/swagger/\n")

if __name__ == '__main__':
    main()

