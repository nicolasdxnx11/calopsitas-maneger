"""
Modelo de Requisição de Interesse
"""

from app import db
from . import BaseModel

class Requisicao(BaseModel):
    __tablename__ = 'requisicao'
    
    # Informações da requisição
    status = db.Column(db.String(20), default='pendente')  # pendente, aprovada, rejeitada
    observacoes = db.Column(db.Text)
    
    # Relacionamentos
    cliente_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    ave_id = db.Column(db.Integer, db.ForeignKey('aves.id'), nullable=False)
    ave = db.relationship('Ave', backref='requisicoes')
    
    def __repr__(self):
        return f'<Requisicao {self.id}>'
    
    def to_dict(self):
        """Converte o objeto para dicionário"""
        return {
            'id': self.id,
            'status': self.status,
            'observacoes': self.observacoes,
            'cliente': self.cliente.nome,
            'ave': self.ave.nome,
            'data_criacao': self.created_at.strftime('%d/%m/%Y %H:%M')
        } 