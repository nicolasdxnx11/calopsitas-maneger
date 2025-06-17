#!/usr/bin/env python3
"""
Script para fazer backup e migrar o banco de dados
"""

import os
import shutil
from datetime import datetime
from app import create_app, db
from flask_migrate import upgrade, migrate, init

def backup_database():
    """Faz backup do banco de dados atual"""
    if os.path.exists('calopsitas.db'):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = f'calopsitas_backup_{timestamp}.db'
        shutil.copy2('calopsitas.db', backup_file)
        print(f'✅ Backup criado: {backup_file}')
    else:
        print('⚠️ Nenhum banco de dados encontrado para backup')

def init_migrations():
    """Inicializa o sistema de migrações"""
    if not os.path.exists('migrations'):
        init()
        print('✅ Sistema de migrações inicializado')
    else:
        print('ℹ️ Sistema de migrações já existe')

def run_migrations():
    """Executa as migrações pendentes"""
    migrate()
    upgrade()
    print('✅ Migrações aplicadas com sucesso')

if __name__ == '__main__':
    # Criar aplicação
    app = create_app()
    
    with app.app_context():
        # Fazer backup
        backup_database()
        
        # Inicializar migrações se necessário
        init_migrations()
        
        # Executar migrações
        run_migrations() 