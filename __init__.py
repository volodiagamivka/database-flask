from flask import Flask
from flask_restx import Api
from my_project.db_init import db
import os
from dotenv import load_dotenv

# Завантажуємо змінні середовища з .env файлу
load_dotenv()


def create_app():
    app = Flask(__name__)

    # Отримуємо дані підключення з environment variables
    db_host = os.getenv('DB_HOST', 'localhost')
    db_user = os.getenv('DB_USER', 'root')
    db_password = os.getenv('DB_PASSWORD', 'password')
    db_name = os.getenv('DB_NAME', 'hospitalss')
    db_port = os.getenv('DB_PORT', '3306')
    
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}?ssl_verify_cert=false&ssl_verify_identity=false'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

    db.init_app(app)
    
    # Створюємо Flask-RESTX API
    api = Api(
        app, 
        version='1.0',
        title='Hospital Management API',
        description='API для управління лікарнею, пацієнтами, лікарями та медикаментами',
        doc='/swagger/',
        prefix='/api/v1'
    )
    
    # Імпортуємо всі моделі для правильного роботи relationships
    from my_project.auth.models import (
        Patient, Doctor, Hospital, Department, 
        Medication, PatientMedications, PatientStatus
    )
    
    # Імпортуємо та реєструємо namespaces
    from my_project.auth.route.patient_namespace import patient_ns
    api.add_namespace(patient_ns)

    return app