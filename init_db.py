"""
Скрипт для ініціалізації бази даних
Запуск: python init_db.py
"""
from app import app
from database import db

def init_database():
    """Створює всі таблиці в базі даних"""
    with app.app_context():
        try:
            print("🔄 Початок ініціалізації бази даних...")
            db.create_all()
            print("✅ База даних успішно ініціалізована!")
            print("📊 Всі таблиці створені.")
        except Exception as e:
            print(f"❌ Помилка при ініціалізації бази даних: {e}")
            raise

if __name__ == '__main__':
    init_database()

