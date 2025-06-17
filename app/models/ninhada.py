from app import db
from datetime import datetime
from app.models.associacoes import ninhada_filhote

class Ninhada(db.Model):
    __tablename__ = 'ninhadas'
    
    id = db.Column(db.Integer, primary_key=True)
    casal_id = db.Column(db.Integer, db.ForeignKey('casais.id'), nullable=False)
    data_postura = db.Column(db.Date, nullable=False)
    data_eclosao = db.Column(db.Date)
    observacoes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    casal = db.relationship('Casal', backref='ninhadas')
    # O relacionamento filhotes será definido após todos os modelos serem importados
    
    def __repr__(self):
        return f'<Ninhada {self.id}>' 