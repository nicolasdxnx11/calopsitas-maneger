# app/routes/auth.py  
"""Rotas de autenticação"""
from flask import Blueprint

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return "Login - Em desenvolvimento"

# =====================================