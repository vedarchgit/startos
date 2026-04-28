import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-change-me-strongly-secret-key-12345')
    DEBUG      = os.getenv('FLASK_DEBUG', '1') == '1'
    
    # Use Supabase PostgreSQL for persistent database (production)
    POSTGRES_URL = os.getenv('POSTGRES_URL')
    if POSTGRES_URL:
        SQLALCHEMY_DATABASE_URI = POSTGRES_URL.replace('postgresql://', 'postgresql+psycopg2://')
    else:
        # Fallback to SQLite for local development
        SQLALCHEMY_DATABASE_URI = 'sqlite:///stratos.db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 3600,
    }
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    WTF_CSRF_ENABLED = True
    RATELIMIT_STORAGE_URI = "memory://"

class DevelopmentConfig(Config):
    DEBUG = True
    WTF_CSRF_ENABLED = False   # disable CSRF in dev so forms work without tokens

class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = True

config = {'development': DevelopmentConfig, 'production': ProductionConfig, 'default': DevelopmentConfig}
