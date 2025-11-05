import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database Configuration - SQLite por defecto, PostgreSQL opcional
    USE_POSTGRESQL = os.environ.get('USE_POSTGRESQL', 'false').lower() == 'true'
    
    if USE_POSTGRESQL:
        # PostgreSQL Database Configuration
        DB_HOST = os.environ.get('DB_HOST') or 'localhost'
        DB_PORT = os.environ.get('DB_PORT') or '5432'
        DB_NAME = os.environ.get('DB_NAME') or 'bar_website'
        DB_USER = os.environ.get('DB_USER') or 'postgres'
        DB_PASSWORD = os.environ.get('DB_PASSWORD') or 'password'
        SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    else:
        # SQLite Database Configuration (por defecto)
        SQLALCHEMY_DATABASE_URI = 'sqlite:///bar_website.db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Email Configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    
    # Bar Information - BarManager Pro
    BAR_NAME = os.environ.get('BAR_NAME') or 'BarManager Pro'
    BAR_ADDRESS = os.environ.get('BAR_ADDRESS') or 'Av. Empresarial 456, Bogotá D.C.'
    BAR_PHONE = os.environ.get('BAR_PHONE') or '+57 301 456 7890'
    BAR_EMAIL = os.environ.get('BAR_EMAIL') or 'info@barmanagerpro.com'
    BAR_SLOGAN = os.environ.get('BAR_SLOGAN') or 'Sistema de Gestión Integral para Bares'

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}