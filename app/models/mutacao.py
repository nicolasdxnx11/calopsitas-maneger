"""
Modelo de Mutação Genética
"""

from app import db
from . import BaseModel
from sqlalchemy import CheckConstraint

class Mutacao(BaseModel):
    __tablename__ = 'mutacao'
    
    # Informações básicas
    nome = db.Column(db.String(50), nullable=False, unique=True)
    tipo_heranca = db.Column(db.String(30), nullable=False)  # Tipos mais específicos
    descricao = db.Column(db.Text)
    cor_resultante = db.Column(db.String(100))
    
    # Informações genéticas
    gene = db.Column(db.String(50))  # Nome do gene
    simbolo = db.Column(db.String(10))  # Símbolo usado em genética
    alelo_dominante = db.Column(db.String(10))  # Ex: "A"
    alelo_recessivo = db.Column(db.String(10))  # Ex: "a"
    
    # Informações adicionais para cálculos precisos
    viabilidade_homozigoto = db.Column(db.Boolean, default=True)  # Se é viável em homozigose
    expressao_heterozigoto = db.Column(db.Boolean, default=True)  # Se expressa em heterozigose
    
    # Status
    ativo = db.Column(db.Boolean, default=True)
    
    # Constraints
    __table_args__ = (
        CheckConstraint(
            "tipo_heranca IN ('ligado ao sexo dominante', 'ligado ao sexo recessivo', 'autossômico dominante', 'autossômico recessivo')",
            name='check_tipo_heranca_valido'
        ),
        CheckConstraint(
            "simbolo GLOB '[A-Za-z]'",
            name='check_simbolo_valido'
        ),
        CheckConstraint(
            "alelo_dominante GLOB '[A-Z]'",
            name='check_alelo_dominante_valido'
        ),
        CheckConstraint(
            "alelo_recessivo GLOB '[a-z]'",
            name='check_alelo_recessivo_valido'
        ),
    )
    
    # Relacionamentos
    mutacoes_compativeis = db.relationship(
        'Mutacao',
        secondary='mutacao_compativel',
        primaryjoin='Mutacao.id==mutacao_compativel.c.mutacao_id',
        secondaryjoin='Mutacao.id==mutacao_compativel.c.compativel_id',
        backref=db.backref('compativel_com', lazy='dynamic')
    )
    
    def __repr__(self):
        return f'<Mutacao {self.nome}>'
    
    def to_dict(self):
        """Converte o objeto para dicionário"""
        return {
            'id': self.id,
            'nome': self.nome,
            'tipo_heranca': self.tipo_heranca,
            'descricao': self.descricao,
            'cor_resultante': self.cor_resultante,
            'gene': self.gene,
            'simbolo': self.simbolo,
            'alelo_dominante': self.alelo_dominante,
            'alelo_recessivo': self.alelo_recessivo,
            'viabilidade_homozigoto': self.viabilidade_homozigoto,
            'expressao_heterozigoto': self.expressao_heterozigoto
        }
    
    @property
    def is_ligada_sexo(self):
        """Verifica se é mutação ligada ao sexo"""
        return 'ligado ao sexo' in self.tipo_heranca
    
    @property
    def is_dominante(self):
        """Verifica se é mutação dominante"""
        return 'dominante' in self.tipo_heranca
    
    @property
    def is_recessiva(self):
        """Verifica se é mutação recessiva"""
        return 'recessivo' in self.tipo_heranca

# Tabela auxiliar para mutações compatíveis
mutacao_compativel = db.Table('mutacao_compativel',
    db.Column('mutacao_id', db.Integer, db.ForeignKey('mutacao.id'), primary_key=True),
    db.Column('compativel_id', db.Integer, db.ForeignKey('mutacao.id'), primary_key=True),
    CheckConstraint('mutacao_id < compativel_id', name='check_sem_ciclos')
)