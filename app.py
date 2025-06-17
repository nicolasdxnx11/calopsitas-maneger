#!/usr/bin/env python3
"""
Arquivo principal para iniciar a aplicação Flask
"""

import os
from app import create_app, db
from app.models import Usuario, Ave, Mutacao, Cruzamento

# Criar aplicação usando configuração de desenvolvimento
app = create_app(os.getenv('FLASK_CONFIG') or 'default')

@app.shell_context_processor
def make_shell_context():
    """
    Disponibiliza objetos automaticamente no shell do Flask
    Útil para testes e debugging
    """
    return {
        'db': db,
        'Usuario': Usuario,
        'Ave': Ave,
        'Mutacao': Mutacao,
        'Cruzamento': Cruzamento
    }

@app.cli.command()
def init_db():
    """Comando para inicializar o banco de dados"""
    db.create_all()
    print('✅ Banco de dados inicializado!')

@app.cli.command()
def seed_db():
    """Comando para popular banco com dados iniciais"""
    # Aqui futuramente vamos adicionar mutações padrão
    print('🌱 Dados iniciais inseridos!')

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        # Executa comandos CLI, como init_db ou seed_db
        app.cli.main()
    else:
        # Executa o servidor normalmente
        app.run(debug=True, host='0.0.0.0', port=5003)