"""
Modelo de Usuário
"""

from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from . import BaseModel

class Usuario(BaseModel):
    __tablename__ = 'usuario'
    
    # Informações básicas
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    
    # Tipo de usuário e permissões
    tipo = db.Column(db.String(20), default='cliente')  # admin, proprietario, cliente
    ativo = db.Column(db.Boolean, default=True)
    
    # Relacionamento com plantel (para proprietários)
    plantel_id = db.Column(db.Integer, db.ForeignKey('plantel.id'))
    plantel = db.relationship('Plantel', backref='proprietarios', foreign_keys=[plantel_id])
    
    # Requisições de interesse (para clientes)
    requisicoes = db.relationship('Requisicao', backref='cliente', lazy='dynamic')
    
    def __repr__(self):
        return f'<Usuario {self.nome}>'
    
    @property
    def senha(self):
        raise AttributeError('senha não é um atributo legível')
    
    @senha.setter
    def senha(self, senha):
        self.senha_hash = generate_password_hash(senha)
    
    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)
    
    def is_admin(self):
        return self.tipo == 'admin'
    
    def is_proprietario(self):
        return self.tipo == 'proprietario'
    
    def is_cliente(self):
        return self.tipo == 'cliente'
    
    def to_dict(self):
        """Converte o objeto para dicionário"""
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'tipo': self.tipo,
            'ativo': self.ativo
        }

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return self.ativo

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)