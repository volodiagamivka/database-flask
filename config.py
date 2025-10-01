# Production Configuration
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Database configuration
    DB_HOST = os.environ.get('DB_HOST') or 'localhost'
    DB_USER = os.environ.get('DB_USER') or 'root'
    DB_PASSWORD = os.environ.get('DB_PASSWORD') or 'password'
    DB_NAME = os.environ.get('DB_NAME') or 'hospitalss'
    
    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return f'mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}/{self.DB_NAME}'

class DevelopmentConfig(Config):
    DEBUG = True
    FLASK_ENV = 'development'
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{os.environ.get("DB_USER", "root")}:{os.environ.get("DB_PASSWORD", "password")}@{os.environ.get("DB_HOST", "localhost")}/{os.environ.get("DB_NAME", "hospitalss")}'

class ProductionConfig(Config):
    DEBUG = False
    FLASK_ENV = 'production'
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{os.environ.get("DB_USER", "root")}:{os.environ.get("DB_PASSWORD", "password")}@{os.environ.get("DB_HOST", "localhost")}/{os.environ.get("DB_NAME", "hospitalss")}'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
