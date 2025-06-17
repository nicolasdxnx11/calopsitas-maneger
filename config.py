import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Configurações base da aplicação"""
    
    # Configurações básicas
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'chave-secreta-padrao'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configurações de upload
    UPLOAD_FOLDER = os.path.join(basedir, 'app/static/uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max-limit
    
    # Configurações de sessão
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)
    
    # Configurações de desenvolvimento
    DEBUG = True
    TESTING = False
    
    @staticmethod
    def init_app(app):
        # Criar pasta de uploads se não existir
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

class DevelopmentConfig(Config):
    """Configurações específicas para desenvolvimento"""
    DEBUG = True
    SQLALCHEMY_ECHO = True  # Mostra SQL no terminal
    
    @staticmethod
    def init_app(app):
        pass

class ProductionConfig(Config):
    """Configurações específicas para produção"""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')  # Deve ser definida no servidor
    
    # Em produção, usar PostgreSQL
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'calopsitas.db')

# Dicionário para facilitar seleção da configuração
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}