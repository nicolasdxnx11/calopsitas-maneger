"""
Modelo para fotos das aves
"""

from app import db
from . import BaseModel
from sqlalchemy import CheckConstraint

class FotoAve(BaseModel):
    __tablename__ = 'foto_ave'
    
    # Informações da foto
    caminho = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.String(200))
    ordem = db.Column(db.Integer, default=0)  # Para ordenar as fotos
    
    # Relacionamento com a ave
    ave_id = db.Column(db.Integer, db.ForeignKey('aves.id'), nullable=False)
    
    # CheckConstraint para o campo simbolo
    __table_args__ = (
        CheckConstraint(
            "simbolo GLOB '[A-Za-z]'",
            name='check_simbolo_valido'
        ),
    )
    
    def __repr__(self):
        return f'<FotoAve {self.caminho}>' 