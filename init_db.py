"""
Скрипт для ініціалізації бази даних
Запуск: python init_db.py [--sql]

Варіанти:
- python init_db.py          # Використовує SQLAlchemy (db.create_all())
- python init_db.py --sql     # Використовує SQL файл (database_schema.sql)
"""
import sys
from app import app
from my_project.db_init import db

def init_database_sqlalchemy():
    """Створює всі таблиці через SQLAlchemy"""
    with app.app_context():
        try:
            print("🔄 Початок ініціалізації бази даних через SQLAlchemy...")
            db.create_all()
            print("✅ База даних успішно ініціалізована через SQLAlchemy!")
            print("📊 Всі таблиці створені.")
        except Exception as e:
            print(f"❌ Помилка при ініціалізації бази даних: {e}")
            raise

def init_database_from_sql():
    """Створює базу даних з SQL файлу"""
    try:
        from init_from_sql import init_database_from_sql
        return init_database_from_sql()
    except ImportError:
        print("❌ Файл init_from_sql.py не знайдено")
        return False

def main():
    """Головна функція"""
    if len(sys.argv) > 1 and sys.argv[1] == '--sql':
        print("🗄️ Використовуємо SQL файл для ініціалізації...")
        success = init_database_from_sql()
        if not success:
            print("\n🔄 Спробуємо через SQLAlchemy...")
            init_database_sqlalchemy()
    else:
        print("🔧 Використовуємо SQLAlchemy для ініціалізації...")
        init_database_sqlalchemy()

if __name__ == '__main__':
    main()

