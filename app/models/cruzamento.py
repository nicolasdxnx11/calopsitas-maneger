"""
Modelo de Cruzamento (básico por enquanto)
"""

from app import db
from . import BaseModel

class Cruzamento(BaseModel):
    __tablename__ = 'cruzamento'
    
    pai_id = db.Column(db.Integer, db.ForeignKey('aves.id'), nullable=False)
    mae_id = db.Column(db.Integer, db.ForeignKey('aves.id'), nullable=False)
    data_cruzamento = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='planejado')  # planejado, realizado, finalizado
    observacoes = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Cruzamento {self.id}>'