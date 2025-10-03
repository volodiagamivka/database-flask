"""
Скрипт для ініціалізації бази даних з SQL файлу
Використання: python init_from_sql.py
"""
import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

def init_database_from_sql():
    """Створює базу даних з SQL файлу"""
    
    # Отримуємо дані підключення
    db_host = os.getenv('DB_HOST', 'localhost')
    db_user = os.getenv('DB_USER', 'root')
    db_password = os.getenv('DB_PASSWORD', 'password')
    db_name = os.getenv('DB_NAME', 'hospitalss')
    db_port = int(os.getenv('DB_PORT', '3306'))
    
    print("🔄 Початок ініціалізації бази даних з SQL файлу...")
    print(f"📍 Підключення до: {db_host}:{db_port}")
    print(f"🗄️ База даних: {db_name}")
    print()
    
    try:
        # Підключення до MySQL сервера (без конкретної бази даних)
        connection = pymysql.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            port=db_port,
            charset='utf8mb4',
            ssl_verify_cert=False,
            ssl_verify_identity=False
        )
        
        with connection.cursor() as cursor:
            # Створюємо базу даних якщо не існує
            print("📊 Створення бази даних...")
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print(f"✅ База даних '{db_name}' готова")
            
            # Вибираємо базу даних
            cursor.execute(f"USE {db_name}")
            
            # Читаємо SQL файл
            sql_file_path = os.path.join(os.path.dirname(__file__), 'database_schema.sql')
            
            if not os.path.exists(sql_file_path):
                print(f"❌ SQL файл не знайдено: {sql_file_path}")
                return False
            
            print("📖 Читання SQL файлу...")
            with open(sql_file_path, 'r', encoding='utf-8') as file:
                sql_content = file.read()
            
            # Розділяємо SQL на окремі запити
            sql_queries = [query.strip() for query in sql_content.split(';') if query.strip()]
            
            print(f"🔧 Виконання {len(sql_queries)} SQL запитів...")
            
            for i, query in enumerate(sql_queries, 1):
                if query.upper().startswith('USE '):
                    continue  # Пропускаємо USE запити
                
                try:
                    cursor.execute(query)
                    if i % 10 == 0:  # Показуємо прогрес кожні 10 запитів
                        print(f"   Виконано {i}/{len(sql_queries)} запитів...")
                except Exception as e:
                    print(f"⚠️ Попередження при виконанні запиту {i}: {e}")
                    continue
            
            connection.commit()
            print(f"✅ Всі SQL запити виконано успішно!")
            
            # Перевіряємо створені таблиці
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"\n📋 Створено таблиць: {len(tables)}")
            for table in tables:
                print(f"   - {table[0]}")
            
            # Показуємо статистику даних
            print(f"\n📊 Статистика даних:")
            cursor.execute("SELECT COUNT(*) FROM hospitals")
            hospitals_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM patients")
            patients_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM doctors")
            doctors_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM medications")
            medications_count = cursor.fetchone()[0]
            
            print(f"   🏥 Лікарень: {hospitals_count}")
            print(f"   👥 Пацієнтів: {patients_count}")
            print(f"   👨‍⚕️ Лікарів: {doctors_count}")
            print(f"   💊 Медикаментів: {medications_count}")
        
        connection.close()
        print("\n🎉 База даних успішно ініціалізована з SQL файлу!")
        return True
        
    except Exception as e:
        print(f"\n❌ Помилка при ініціалізації бази даних: {e}")
        print("\n💡 Перевірте:")
        print("   1. Чи правильні дані в .env файлі")
        print("   2. Чи доступний MySQL сервер")
        print("   3. Чи існує файл database_schema.sql")
        return False

if __name__ == '__main__':
    init_database_from_sql()
