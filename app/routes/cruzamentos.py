# app/routes/cruzamentos.py
"""
Rotas para gerenciamento de cruzamentos
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Casal, Ave, Ninhada, Plantel
from app.forms import CasalForm, NinhadaForm
from app.genetica import CalculadoraGenetica
from sqlalchemy import and_

cruzamentos = Blueprint('cruzamentos', __name__)

@cruzamentos.route('/')
@login_required
def index():
    """Lista todos os cruzamentos do usuário"""
    if not current_user.plantel:
        plantel = Plantel(nome=f"Plantel de {current_user.nome}")
        current_user.plantel = plantel
        db.session.add(plantel)
        db.session.commit()
    
    # Buscar casais do plantel do usuário
    casais = Casal.query \
        .join(Ave, Casal.macho_id == Ave.id) \
        .filter(Ave.plantel_id == current_user.plantel.id) \
        .all()
    
    return render_template('cruzamentos/index.html', title='Cruzamentos', casais=casais)

@cruzamentos.route('/simular', methods=['GET', 'POST'])
@login_required
def simular():
    """Simula um cruzamento entre duas aves"""
    if request.method == 'POST':
        macho_id = request.form.get('macho_id')
        femea_id = request.form.get('femea_id')
        
        if not macho_id or not femea_id:
            flash('Selecione um macho e uma fêmea para simular o cruzamento.', 'warning')
            return redirect(url_for('cruzamentos.simular'))
        
        macho = Ave.query.get(macho_id)
        femea = Ave.query.get(femea_id)
        
        if not macho or not femea:
            flash('Aves não encontradas.', 'danger')
            return redirect(url_for('cruzamentos.simular'))
        
        # Verificar se as aves pertencem ao plantel do usuário
        if macho.plantel_id != current_user.plantel.id or femea.plantel_id != current_user.plantel.id:
            flash('Você não tem permissão para simular cruzamentos com essas aves.', 'danger')
            return redirect(url_for('cruzamentos.simular'))
        
        # Calcular probabilidades usando o módulo de genética
        probabilidades = CalculadoraGenetica.calcular_probabilidades_cruzamento(macho, femea)
        relatorio = CalculadoraGenetica.gerar_relatorio_cruzamento(macho, femea, probabilidades)
        
        return render_template('cruzamentos/simulacao.html', 
                             macho=macho, femea=femea, 
                             probabilidades=probabilidades,
                             relatorio=relatorio)
    
    # GET: mostrar formulário de simulação
    if not current_user.plantel:
        plantel = Plantel(nome=f"Plantel de {current_user.nome}")
        current_user.plantel = plantel
        db.session.add(plantel)
        db.session.commit()
    
    machos = Ave.query.filter_by(plantel_id=current_user.plantel.id, sexo='M').all()
    femeas = Ave.query.filter_by(plantel_id=current_user.plantel.id, sexo='F').all()
    
    return render_template('cruzamentos/simular.html', 
                         title='Simular Cruzamento',
                         machos=machos, femeas=femeas)

@cruzamentos.route('/api/calcular-probabilidades', methods=['POST'])
@login_required
def api_calcular_probabilidades():
    """API para calcular probabilidades via AJAX"""
    macho_id = request.json.get('macho_id')
    femea_id = request.json.get('femea_id')
    
    macho = Ave.query.get(macho_id)
    femea = Ave.query.get(femea_id)
    
    if not macho or not femea:
        return jsonify({'error': 'Aves não encontradas'}), 404
    
    # Verificar permissões
    if macho.plantel_id != current_user.plantel.id or femea.plantel_id != current_user.plantel.id:
        return jsonify({'error': 'Acesso negado'}), 403
    
    probabilidades = CalculadoraGenetica.calcular_probabilidades_cruzamento(macho, femea)
    relatorio = CalculadoraGenetica.gerar_relatorio_cruzamento(macho, femea, probabilidades)
    
    return jsonify({
        'probabilidades': probabilidades,
        'relatorio': relatorio
    })

@cruzamentos.route('/historico')
@login_required
def historico():
    """Mostra histórico de cruzamentos realizados"""
    if not current_user.plantel:
        plantel = Plantel(nome=f"Plantel de {current_user.nome}")
        current_user.plantel = plantel
        db.session.add(plantel)
        db.session.commit()
    
    # Buscar casais com ninhadas
    casais_com_ninhadas = Casal.query \
        .join(Ave, Casal.macho_id == Ave.id) \
        .filter(Ave.plantel_id == current_user.plantel.id) \
        .filter(Casal.ninhadas.any()) \
        .all()
    
    return render_template('cruzamentos/historico.html', 
                         title='Histórico de Cruzamentos',
                         casais=casais_com_ninhadas)

@cruzamentos.route('/estatisticas')
@login_required
def estatisticas():
    """Mostra estatísticas de cruzamentos"""
    if not current_user.plantel:
        plantel = Plantel(nome=f"Plantel de {current_user.nome}")
        current_user.plantel = plantel
        db.session.add(plantel)
        db.session.commit()
    
    # Estatísticas básicas
    total_casais = Casal.query \
        .join(Ave, Casal.macho_id == Ave.id) \
        .filter(Ave.plantel_id == current_user.plantel.id) \
        .count()
    
    total_ninhadas = Ninhada.query \
        .join(Casal) \
        .join(Ave, Casal.macho_id == Ave.id) \
        .filter(Ave.plantel_id == current_user.plantel.id) \
        .count()
    
    total_filhotes = Ave.query \
        .filter_by(plantel_id=current_user.plantel.id) \
        .filter(Ave.ninhada_id.isnot(None)) \
        .count()
    
    stats = {
        'total_casais': total_casais,
        'total_ninhadas': total_ninhadas,
        'total_filhotes': total_filhotes,
        'media_filhotes_por_ninhada': total_filhotes / total_ninhadas if total_ninhadas > 0 else 0
    }
    
    return render_template('cruzamentos/estatisticas.html', 
                         title='Estatísticas de Cruzamentos',
                         stats=stats)