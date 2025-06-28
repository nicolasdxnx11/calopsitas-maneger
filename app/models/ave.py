"""
Modelo de Ave
"""

from app import db
from . import BaseModel, ave_mutacao
from datetime import date, datetime
from sqlalchemy import CheckConstraint

class Ave(BaseModel):
    __tablename__ = 'aves'
    
    # Informações básicas
    nome = db.Column(db.String(100), nullable=False)
    sexo = db.Column(db.String(1), nullable=False)  # M ou F
    data_nascimento = db.Column(db.Date, nullable=False)
    cor_base = db.Column(db.String(50))
    
    # Status e comercialização
    disponivel = db.Column(db.Boolean, default=True)
    preco = db.Column(db.Float)
    preco_negociavel = db.Column(db.Boolean, default=True)
    status = db.Column(db.String(20), default='ativo')  # ativo, vendido, falecido
    
    # Informações adicionais
    observacoes = db.Column(db.Text)
    historico_medico = db.Column(db.Text)
    
    # Fotos
    foto_principal = db.Column(db.String(200))
    fotos = db.relationship('FotoAve', backref='ave', lazy='dynamic')
    
    # Relacionamentos genealógicos
    pai_id = db.Column(db.Integer, db.ForeignKey('aves.id'))
    mae_id = db.Column(db.Integer, db.ForeignKey('aves.id'))
    pai = db.relationship('Ave', foreign_keys=[pai_id], backref='filhos_pai', remote_side='Ave.id')
    mae = db.relationship('Ave', foreign_keys=[mae_id], backref='filhos_mae', remote_side='Ave.id')
    
    # Relacionamento many-to-many com mutações (mutações visíveis/expressas)
    mutacoes = db.relationship('Mutacao', secondary=ave_mutacao, backref='aves')
    
    # Relacionamento many-to-many com mutações portadoras (não expressas)
    mutacoes_portadoras = db.relationship(
        'Mutacao',
        secondary='ave_mutacao_portadora',
        backref='aves_portadoras'
    )
    
    # Relacionamento com usuário (proprietário)
    proprietario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    proprietario = db.relationship('Usuario', backref='aves')

    # Relacionamento com plantel
    plantel_id = db.Column(db.Integer, db.ForeignKey('plantel.id'))
    plantel = db.relationship('Plantel', back_populates='aves')

    # Constraints
    __table_args__ = (
        CheckConstraint("sexo IN ('M', 'F')", name='check_sexo_valido'),
        CheckConstraint("status IN ('ativo', 'vendido', 'reservado', 'para_reproducao')", name='check_status_valido'),
        CheckConstraint("preco >= 0", name='check_preco_positivo'),
    )
    
    def __repr__(self):
        return f'<Ave {self.nome}>'
    
    @property
    def idade(self):
        """Retorna a idade da ave em meses"""
        hoje = datetime.now().date()
        idade_dias = (hoje - self.data_nascimento).days
        return idade_dias // 30  # Aproximação em meses
    
    def tem_mutacao(self, mutacao):
        """Verifica se a ave tem uma mutação específica (visível ou portadora)"""
        return mutacao in self.mutacoes or mutacao in self.mutacoes_portadoras
    
    def tem_mutacao_visivel(self, mutacao):
        """Verifica se a ave expressa uma mutação específica"""
        return mutacao in self.mutacoes
    
    def tem_mutacao_portadora(self, mutacao):
        """Verifica se a ave é portadora de uma mutação específica"""
        return mutacao in self.mutacoes_portadoras
    
    def get_genotipo_mutacao(self, mutacao):
        """
        Retorna o genótipo da ave para uma mutação específica
        Returns: 'homozigoto', 'heterozigoto', 'portador', 'normal', 'desconhecido'
        """
        if mutacao in self.mutacoes:
            # Se expressa a mutação
            if mutacao.is_ligada_sexo and self.sexo == 'F':
                # Fêmea com mutação ligada ao sexo é sempre homozigota
                return 'homozigoto'
            elif mutacao.is_dominante:
                # Para dominantes, pode ser homozigoto ou heterozigoto
                # Assumimos heterozigoto por padrão (mais comum)
                return 'heterozigoto'
            else:
                # Para recessivos, se expressa é homozigoto
                return 'homozigoto'
        elif mutacao in self.mutacoes_portadoras:
            return 'portador'
        else:
            return 'normal'
    
    def to_dict(self):
        """Converte o objeto para dicionário"""
        return {
            'id': self.id,
            'nome': self.nome,
            'sexo': self.sexo,
            'idade': self.idade,
            'cor_base': self.cor_base,
            'disponivel': self.disponivel,
            'preco': self.preco,
            'preco_negociavel': self.preco_negociavel,
            'status': self.status,
            'foto_principal': self.foto_principal,
            'mutacoes': [m.nome for m in self.mutacoes],
            'mutacoes_portadoras': [m.nome for m in self.mutacoes_portadoras]
        }

# Tabela auxiliar para mutações portadoras
ave_mutacao_portadora = db.Table('ave_mutacao_portadora',
    db.Column('ave_id', db.Integer, db.ForeignKey('aves.id'), primary_key=True),
    db.Column('mutacao_id', db.Integer, db.ForeignKey('mutacao.id'), primary_key=True)
)