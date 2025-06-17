from datetime import datetime
from app import db

class Casal(db.Model):
    __tablename__ = 'casais'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    macho_id = db.Column(db.Integer, db.ForeignKey('aves.id'), nullable=False)
    femea_id = db.Column(db.Integer, db.ForeignKey('aves.id'), nullable=False)
    data_formacao = db.Column(db.DateTime, default=datetime.utcnow)
    ativo = db.Column(db.Boolean, default=True)
    observacoes = db.Column(db.Text)
    
    # Relacionamentos
    macho = db.relationship('Ave', foreign_keys=[macho_id], backref='casais_como_macho')
    femea = db.relationship('Ave', foreign_keys=[femea_id], backref='casais_como_femea')
    ninhadas = db.relationship('Ninhada', backref='casal', lazy='dynamic')
    
    def calcular_probabilidades(self):
        """Calcula as probabilidades de mutações nos filhotes"""
        probabilidades = {}
        
        # Obter mutações do macho e da fêmea
        mutacoes_macho = self.macho.mutacoes
        mutacoes_femea = self.femea.mutacoes
        
        # Para cada mutação possível
        for mutacao in mutacoes_macho + mutacoes_femea:
            if mutacao.tipo_heranca == 'ligado ao sexo':
                # Cálculo para mutações ligadas ao sexo
                prob = self._calcular_probabilidade_ligada_sexo(mutacao)
            else:
                # Cálculo para mutações dominantes
                prob = self._calcular_probabilidade_dominante(mutacao)
            
            probabilidades[mutacao.nome] = prob
        
        return probabilidades
    
    def _calcular_probabilidade_ligada_sexo(self, mutacao):
        """Calcula probabilidade para mutações ligadas ao sexo"""
        # Verificar se macho tem a mutação
        macho_tem = any(m.id == mutacao.id for m in self.macho.mutacoes)
        # Verificar se fêmea tem a mutação
        femea_tem = any(m.id == mutacao.id for m in self.femea.mutacoes)
        
        if macho_tem and femea_tem:
            return {
                'machos': 100,  # Todos os machos terão
                'femeas': 100   # Todas as fêmeas terão
            }
        elif macho_tem:
            return {
                'machos': 50,   # 50% dos machos terão
                'femeas': 0     # Nenhuma fêmea terá
            }
        elif femea_tem:
            return {
                'machos': 50,   # 50% dos machos terão
                'femeas': 50    # 50% das fêmeas terão
            }
        else:
            return {
                'machos': 0,    # Nenhum macho terá
                'femeas': 0     # Nenhuma fêmea terá
            }
    
    def _calcular_probabilidade_dominante(self, mutacao):
        """Calcula probabilidade para mutações dominantes"""
        # Verificar se macho tem a mutação
        macho_tem = any(m.id == mutacao.id for m in self.macho.mutacoes)
        # Verificar se fêmea tem a mutação
        femea_tem = any(m.id == mutacao.id for m in self.femea.mutacoes)
        
        if macho_tem and femea_tem:
            return 100  # Todos os filhotes terão
        elif macho_tem or femea_tem:
            return 50   # 50% dos filhotes terão
        else:
            return 0    # Nenhum filhote terá

class Ninhada(db.Model):
    __tablename__ = 'ninhadas'
    
    id = db.Column(db.Integer, primary_key=True)
    casal_id = db.Column(db.Integer, db.ForeignKey('casais.id'), nullable=False)
    data_postura = db.Column(db.Date, nullable=False)
    quantidade_ovos = db.Column(db.Integer, default=0)
    quantidade_nascidos = db.Column(db.Integer, default=0)
    quantidade_sobreviventes = db.Column(db.Integer, default=0)
    observacoes = db.Column(db.Text)
    
    # Relacionamentos
    filhotes = db.relationship('Ave', backref='ninhada', lazy='dynamic') 