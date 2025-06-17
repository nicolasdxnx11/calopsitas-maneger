"""
Modelo de Plantel
"""

from app import db
from . import BaseModel

class Plantel(BaseModel):
    __tablename__ = 'plantel'
    
    # Informações básicas
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    ativo = db.Column(db.Boolean, default=True)
    
    # Relacionamentos
    aves = db.relationship('Ave', back_populates='plantel', lazy='dynamic')
    
    def __repr__(self):
        return f'<Plantel {self.nome}>'
    
    def to_dict(self):
        """Converte o objeto para dicionário"""
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'ativo': self.ativo,
            'total_aves': self.aves.count()
        } 