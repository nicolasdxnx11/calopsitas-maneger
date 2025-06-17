"""
Modelos da aplicação - representam tabelas do banco
"""

from datetime import datetime
from app import db

# Modelo base com campos comuns
class BaseModel(db.Model):
    __abstract__ = True
    
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Tabela auxiliar para relacionamento many-to-many entre aves e mutações
ave_mutacao = db.Table('ave_mutacao',
    db.Column('ave_id', db.Integer, db.ForeignKey('aves.id'), primary_key=True),
    db.Column('mutacao_id', db.Integer, db.ForeignKey('mutacao.id'), primary_key=True)
)

# Importar todos os modelos
from .usuario import Usuario
from .mutacao import Mutacao  
from .ave import Ave
from .cruzamento import Cruzamento
from .plantel import Plantel
from .foto import FotoAve
from .requisicao import Requisicao
from app.models.casal import Casal, Ninhada
from .associacoes import ninhada_filhote
from flask_sqlalchemy import SQLAlchemy

# Definir relacionamento após todos os modelos serem importados
Ninhada.filhotes = db.relationship(
    Ave,
    secondary=ninhada_filhote,
    backref=db.backref('ninhadas', lazy='dynamic'),
    lazy='dynamic'
)

__all__ = [
    'Usuario',
    'Plantel',
    'Ave',
    'Mutacao',
    'Cruzamento',
    'FotoAve',
    'Requisicao',
    'Casal',
    'Ninhada',
    'ninhada_filhote'
]