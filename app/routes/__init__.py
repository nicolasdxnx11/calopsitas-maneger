"""
Rotas principais da aplicação
"""

from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from app.models.ave import Ave
from app.models.mutacao import Mutacao
from app.models.requisicao import Requisicao
from app.models.usuario import Usuario
from app.forms import LoginForm, RegistroForm, PerfilForm, AlterarSenhaForm
from app import db
from sqlalchemy import func
from datetime import datetime
from werkzeug.urls import url_parse
from werkzeug.security import generate_password_hash, check_password_hash

# Criar blueprint principal
main = Blueprint('main', __name__)

@main.route('/')
@main.route('/index')
@login_required
def index():
    return redirect(url_for('main.dashboard'))

@main.route('/dashboard')
@login_required
def dashboard():
    # Verificar se o usuário tem plantel, se não, criar um
    if not current_user.plantel:
        from app.models import Plantel
        plantel = Plantel(nome=f"Plantel de {current_user.nome}")
        current_user.plantel = plantel
        db.session.add(plantel)
        db.session.commit()
    
    # Estatísticas básicas filtradas pelo plantel do usuário
    plantel_id = current_user.plantel.id
    stats = {
        'total_aves': Ave.query.filter_by(plantel_id=plantel_id).count(),
        'aves_disponiveis': Ave.query.filter_by(plantel_id=plantel_id, status='disponivel').count(),
        'aves_reservadas': Ave.query.filter_by(plantel_id=plantel_id, status='reservado').count(),
        'aves_vendidas': Ave.query.filter_by(plantel_id=plantel_id, status='vendido').count(),
        'total_machos': Ave.query.filter_by(plantel_id=plantel_id, sexo='M').count(),
        'total_femeas': Ave.query.filter_by(plantel_id=plantel_id, sexo='F').count()
    }
    
    # Distribuição por mutação (filtrada pelo plantel)
    mutacoes = db.session.query(
        Mutacao.nome,
        func.count(Ave.id)
    ).join(Ave.mutacoes).filter(Ave.plantel_id == plantel_id).group_by(Mutacao.nome).all()
    
    stats['mutacoes_labels'] = [m[0] for m in mutacoes]
    stats['mutacoes_data'] = [m[1] for m in mutacoes]
    
    # Últimas requisições (filtradas pelo plantel)
    stats['ultimas_requisicoes'] = Requisicao.query.join(Ave).filter(
        Ave.plantel_id == plantel_id
    ).order_by(Requisicao.created_at.desc()).limit(5).all()
    
    return render_template('dashboard.html', title='Dashboard', stats=stats)

@main.route('/sobre')
def sobre():
    """Página sobre o sistema"""
    return render_template('sobre.html', title='Sobre')

@main.route('/api/health')
def health_check():
    """Endpoint para verificar se a API está funcionando"""
    return jsonify({
        'status': 'ok',
        'message': 'Calopsitas Manager API está funcionando!',
        'version': '1.0.0'
    })

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        if usuario and check_password_hash(usuario.senha_hash, form.senha.data):
            login_user(usuario, remember=form.lembrar.data)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.dashboard'))
        flash('Email ou senha inválidos.', 'danger')
    
    return render_template('auth/login.html', form=form)

@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistroForm()
    if form.validate_on_submit():
        usuario = Usuario(
            nome=form.nome.data,
            email=form.email.data,
            senha=form.senha.data
        )
        db.session.add(usuario)
        db.session.commit()
        flash('Conta criada com sucesso! Agora você pode fazer login.', 'success')
        return redirect(url_for('main.login'))
    
    return render_template('auth/register.html', form=form)

@main.route('/conta', methods=['GET', 'POST'])
@login_required
def conta():
    form = PerfilForm(current_user.email)
    if form.validate_on_submit():
        current_user.nome = form.nome.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Perfil atualizado com sucesso!', 'success')
        return redirect(url_for('main.conta'))
    elif request.method == 'GET':
        form.nome.data = current_user.nome
        form.email.data = current_user.email
    return render_template('conta/index.html', title='Minha Conta', form=form)

@main.route('/conta/alterar-senha', methods=['GET', 'POST'])
@login_required
def alterar_senha():
    form = AlterarSenhaForm()
    if form.validate_on_submit():
        if check_password_hash(current_user.senha, form.senha_atual.data):
            current_user.senha = generate_password_hash(form.nova_senha.data)
            db.session.commit()
            flash('Senha alterada com sucesso!', 'success')
            return redirect(url_for('main.conta'))
        flash('Senha atual incorreta.', 'danger')
    return render_template('conta/alterar_senha.html', title='Alterar Senha', form=form)

@main.route('/conta/plantel')
@login_required
def plantel():
    return render_template('conta/plantel.html', title='Meu Plantel')