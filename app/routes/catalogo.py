# app/routes/catalogo.py  
"""
Rotas para o catálogo de mutações
"""
from flask import Blueprint, render_template
from app.models import Mutacao

catalogo = Blueprint('catalogo', __name__)

@catalogo.route('/')
def index():
    """Mostra o catálogo de mutações"""
    mutacoes = Mutacao.query.all()
    return render_template('catalogo/index.html', title='Catálogo', mutacoes=mutacoes)

# =====================================