"""
Inicializador da aplicação Flask
Este arquivo configura e cria nossa aplicação
"""
from flask import render_template  # Adicionar esta linha
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import config
from flask_login import LoginManager

# Instâncias globais das extensões
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'main.login'  # Corrigir para main.login
login_manager.login_message = 'Por favor, faça login para acessar esta página.'
login_manager.remember_cookie_duration = 365 * 24 * 60 * 60  # 1 ano

def create_app(config_name='default'):
    """
    Factory function para criar a aplicação Flask
    
    Args:
        config_name (str): Nome da configuração ('development', 'production', 'default')
    
    Returns:
        Flask: Instância configurada da aplicação
    """
    
    # Criar instância do Flask
    app = Flask(__name__)
    
    # Carregar configurações
    app.config.from_object(config[config_name])
    
    # Inicializar extensões
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    # Criar pasta de uploads se não existir
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Registrar Blueprints (rotas organizadas)
    from app.routes import main
    from app.routes.auth import auth
    from app.routes.aves import aves
    from app.routes.cruzamentos import cruzamentos
    from app.routes.casais import casais
    from app.routes.catalogo import catalogo
    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(aves, url_prefix='/aves')
    app.register_blueprint(cruzamentos, url_prefix='/cruzamentos')
    app.register_blueprint(casais, url_prefix='/casais')
    app.register_blueprint(catalogo, url_prefix='/catalogo')
    
    # Context processor para disponibilizar variáveis em todos os templates
    @app.context_processor
    def inject_app_info():
        return {
            'app_name': 'Calopsitas Manager',
            'app_version': '1.0.0'
        }
    
    # Handler para arquivos não encontrados
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404
    
    # Handler para erros do servidor
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500
    
    # Importar Usuario e definir user_loader aqui para evitar importação circular
    from app.models.usuario import Usuario
    
    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))
    
    return app

# Importar modelos para que o SQLAlchemy os reconheça
from app import models