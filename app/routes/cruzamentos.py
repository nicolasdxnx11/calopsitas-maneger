# app/routes/cruzamentos.py
"""
Rotas para gerenciamento de cruzamentos
"""
from flask import Blueprint, render_template

cruzamentos = Blueprint('cruzamentos', __name__)

@cruzamentos.route('/')
def index():
    """Lista todos os cruzamentos"""
    return render_template('cruzamentos/index.html', title='Cruzamentos')