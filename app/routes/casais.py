from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Casal, Ave, Ninhada
from app.forms import CasalForm, NinhadaForm

casais = Blueprint('casais', __name__)

@casais.route('/casais')
@login_required
def index():
    """Lista todos os casais do usuário"""
    casais = Casal.query.join(Ave).filter(Ave.usuario_id == current_user.id).all()
    return render_template('casais/index.html', casais=casais)

@casais.route('/casais/novo', methods=['GET', 'POST'])
@login_required
def novo():
    """Cria um novo casal"""
    form = CasalForm()
    # Filtrar apenas aves do usuário atual
    form.macho_id.choices = [(a.id, a.nome) for a in Ave.query.filter_by(usuario_id=current_user.id, sexo='M').all()]
    form.femea_id.choices = [(a.id, a.nome) for a in Ave.query.filter_by(usuario_id=current_user.id, sexo='F').all()]
    
    if form.validate_on_submit():
        casal = Casal(
            nome=form.nome.data,
            macho_id=form.macho_id.data,
            femea_id=form.femea_id.data,
            observacoes=form.observacoes.data
        )
        db.session.add(casal)
        db.session.commit()
        flash('Casal criado com sucesso!', 'success')
        return redirect(url_for('casais.index'))
    
    return render_template('casais/form.html', form=form, title='Novo Casal')

@casais.route('/casais/<int:id>')
@login_required
def visualizar(id):
    """Visualiza detalhes do casal e probabilidades"""
    casal = Casal.query.get_or_404(id)
    # Verificar se o casal pertence ao usuário
    if casal.macho.usuario_id != current_user.id or casal.femea.usuario_id != current_user.id:
        flash('Acesso negado!', 'danger')
        return redirect(url_for('casais.index'))
    
    probabilidades = casal.calcular_probabilidades()
    return render_template('casais/visualizar.html', casal=casal, probabilidades=probabilidades)

@casais.route('/casais/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar(id):
    """Edita um casal existente"""
    casal = Casal.query.get_or_404(id)
    # Verificar se o casal pertence ao usuário
    if casal.macho.usuario_id != current_user.id or casal.femea.usuario_id != current_user.id:
        flash('Acesso negado!', 'danger')
        return redirect(url_for('casais.index'))
    
    form = CasalForm(obj=casal)
    # Filtrar apenas aves do usuário atual
    form.macho_id.choices = [(a.id, a.nome) for a in Ave.query.filter_by(usuario_id=current_user.id, sexo='M').all()]
    form.femea_id.choices = [(a.id, a.nome) for a in Ave.query.filter_by(usuario_id=current_user.id, sexo='F').all()]
    
    if form.validate_on_submit():
        casal.nome = form.nome.data
        casal.macho_id = form.macho_id.data
        casal.femea_id = form.femea_id.data
        casal.observacoes = form.observacoes.data
        db.session.commit()
        flash('Casal atualizado com sucesso!', 'success')
        return redirect(url_for('casais.index'))
    
    return render_template('casais/form.html', form=form, title='Editar Casal')

@casais.route('/casais/<int:id>/ninhada/nova', methods=['GET', 'POST'])
@login_required
def nova_ninhada(id):
    """Registra uma nova ninhada para o casal"""
    casal = Casal.query.get_or_404(id)
    # Verificar se o casal pertence ao usuário
    if casal.macho.usuario_id != current_user.id or casal.femea.usuario_id != current_user.id:
        flash('Acesso negado!', 'danger')
        return redirect(url_for('casais.index'))
    
    form = NinhadaForm()
    if form.validate_on_submit():
        ninhada = Ninhada(
            casal_id=casal.id,
            data_postura=form.data_postura.data,
            quantidade_ovos=form.quantidade_ovos.data,
            observacoes=form.observacoes.data
        )
        db.session.add(ninhada)
        db.session.commit()
        flash('Ninhada registrada com sucesso!', 'success')
        return redirect(url_for('casais.visualizar', id=casal.id))
    
    return render_template('casais/ninhada_form.html', form=form, casal=casal)

@casais.route('/casais/<int:id>/excluir', methods=['POST'])
@login_required
def excluir(id):
    """Exclui um casal"""
    casal = Casal.query.get_or_404(id)
    # Verificar se o casal pertence ao usuário
    if casal.macho.usuario_id != current_user.id or casal.femea.usuario_id != current_user.id:
        flash('Acesso negado!', 'danger')
        return redirect(url_for('casais.index'))
    
    db.session.delete(casal)
    db.session.commit()
    flash('Casal excluído com sucesso!', 'success')
    return redirect(url_for('casais.index')) 