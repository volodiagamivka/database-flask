from flask import Flask
from my_project.db_init import db


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://volgam:Gamivka1505@hospital.mysql.database.azure.com:3306/hospital'

    db.init_app(app)

    return app