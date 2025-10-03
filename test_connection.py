"""
Скрипт для перевірки підключення до бази даних Azure MySQL
Запуск: python test_connection.py
"""
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

def test_connection():
    """Тестує підключення до бази даних"""
    
    db_host = os.getenv('DB_HOST', 'localhost')
    db_user = os.getenv('DB_USER', 'root')
    db_password = os.getenv('DB_PASSWORD', 'password')
    db_name = os.getenv('DB_NAME', 'hospitalss')
    db_port = int(os.getenv('DB_PORT', '3306'))
    
    print("🔍 Перевірка налаштувань підключення:")
    print(f"   Host: {db_host}")
    print(f"   User: {db_user}")
    print(f"   Database: {db_name}")
    print(f"   Port: {db_port}")
    print()
    
    try:
        print("🔄 Спроба підключення до бази даних...")
        connection = pymysql.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name,
            port=db_port,
            connect_timeout=10,
            ssl_verify_cert=False,
            ssl_verify_identity=False
        )
        
        print("✅ Підключення успішне!")
        
        # Виконуємо тестовий запит
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"📊 Версія MySQL: {version[0]}")
            
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"📋 Кількість таблиць: {len(tables)}")
            if tables:
                print("   Таблиці:")
                for table in tables:
                    print(f"   - {table[0]}")
        
        connection.close()
        print("\n✅ Тест підключення завершено успішно!")
        return True
        
    except Exception as e:
        print(f"\n❌ Помилка підключення: {e}")
        print("\n💡 Перевірте:")
        print("   1. Чи правильні дані в .env файлі")
        print("   2. Чи дозволена ваша IP адреса в Azure MySQL Firewall")
        print("   3. Чи запущений MySQL сервер на Azure")
        return False

if __name__ == '__main__':
    test_connection()

