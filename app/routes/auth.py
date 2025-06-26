# app/routes/auth.py  
"""Rotas de autenticação"""
from flask import Blueprint, render_template
from app.forms import LoginForm

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('auth/login.html', form=form)

# =====================================