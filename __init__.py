from flask import Flask
from flask_restx import Api
from my_project.db_init import db


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/hospital'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    
    # Додаємо тільки Swagger UI для документації
    api = Api(
        app, 
        version='1.0',
        title='Hospital Management API',
        description='API для управління лікарнею, пацієнтами, лікарями та медикаментами',
        doc='/swagger/',
        prefix='/api/v1'
    )

    return app