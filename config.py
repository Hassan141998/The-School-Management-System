import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'default-dev-key-change-in-production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload configurations
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app', 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app.db')

class ProductionConfig(Config):
    DEBUG = False
    # Prioritize POSTGRES_URL (Vercel/Neon standard)
    uri = os.environ.get("POSTGRES_URL") or os.environ.get("DATABASE_URL")
    
    if uri and uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    
    if not uri:
        # Fallback for debugging, or raise clear error
        # using /tmp for read-write access in serverless if needed, but better to fail if no DB
        pass

    SQLALCHEMY_DATABASE_URI = uri

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
