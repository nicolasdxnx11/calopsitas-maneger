# app/routes/aves.py
"""Rotas para gerenciamento de aves"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.ave import Ave
from app.models.mutacao import Mutacao
from app import db
from app.models import Plantel
from app.forms import AveForm
from datetime import datetime

aves = Blueprint('aves', __name__)

@aves.route('/')
@login_required
def index():
    """Lista todas as aves"""
    aves = Ave.query.filter_by(plantel_id=current_user.plantel.id).all() if current_user.plantel else []
    return render_template('aves/index.html', title='Aves', aves=aves)

@aves.route('/nova', methods=['GET', 'POST'])
@login_required
def nova():
    """Cria uma nova ave"""
    form = AveForm()
    
    # Se o usuário não tem plantel, cria um
    if not current_user.plantel:
        plantel = Plantel(nome=f"Plantel de {current_user.nome}")
        current_user.plantel = plantel
        db.session.add(plantel)
        db.session.commit()
    
    if form.validate_on_submit():
        ave = Ave(
            nome=form.nome.data,
            sexo=form.sexo.data,
            data_nascimento=form.data_nascimento.data,
            status=form.status.data,
            plantel_id=current_user.plantel.id
        )
        
        # Adiciona as mutações selecionadas
        for mutacao_id in form.mutacoes.data:
            mutacao = Mutacao.query.get(mutacao_id)
            if mutacao:
                ave.mutacoes.append(mutacao)
        
        db.session.add(ave)
        db.session.commit()
        flash('Ave cadastrada com sucesso!', 'success')
        return redirect(url_for('aves.index'))
    
    return render_template('aves/form.html', form=form, title='Nova Ave')

@aves.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    """Edita uma ave existente"""
    ave = Ave.query.get_or_404(id)
    
    # Verifica se a ave pertence ao plantel do usuário
    if not current_user.plantel or ave.plantel_id != current_user.plantel.id:
        flash('Você não tem permissão para editar esta ave.', 'danger')
        return redirect(url_for('aves.index'))
    
    form = AveForm(obj=ave)
    
    if form.validate_on_submit():
        ave.nome = form.nome.data
        ave.sexo = form.sexo.data
        ave.data_nascimento = form.data_nascimento.data
        ave.status = form.status.data
        
        # Atualiza as mutações
        ave.mutacoes = []
        for mutacao_id in form.mutacoes.data:
            mutacao = Mutacao.query.get(mutacao_id)
            if mutacao:
                ave.mutacoes.append(mutacao)
        
        db.session.commit()
        flash('Ave atualizada com sucesso!', 'success')
        return redirect(url_for('aves.index'))
    
    return render_template('aves/form.html', form=form, title='Editar Ave')

@aves.route('/excluir/<int:id>')
@login_required
def excluir(id):
    """Exclui uma ave"""
    ave = Ave.query.get_or_404(id)
    
    # Verifica se a ave pertence ao plantel do usuário
    if not current_user.plantel or ave.plantel_id != current_user.plantel.id:
        flash('Você não tem permissão para excluir esta ave.', 'danger')
        return redirect(url_for('aves.index'))
    
    db.session.delete(ave)
    db.session.commit()
    flash('Ave excluída com sucesso!', 'success')
    return redirect(url_for('aves.index'))

# =====================================