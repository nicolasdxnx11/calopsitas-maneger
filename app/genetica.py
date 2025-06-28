"""
Módulo de Genética para Calopsitas
Implementa cálculos científicos de probabilidades genéticas
"""

class CalculadoraGenetica:
    """Calculadora de probabilidades genéticas para calopsitas"""
    
    @staticmethod
    def calcular_probabilidades_cruzamento(macho, femea):
        """
        Calcula as probabilidades de mutações nos filhotes
        
        Args:
            macho: Objeto Ave (macho)
            femea: Objeto Ave (fêmea)
            
        Returns:
            dict: Dicionário com probabilidades por mutação
        """
        probabilidades = {}
        
        # Obter todas as mutações únicas do macho e da fêmea
        mutacoes_macho = set(macho.mutacoes + macho.mutacoes_portadoras)
        mutacoes_femea = set(femea.mutacoes + femea.mutacoes_portadoras)
        todas_mutacoes = mutacoes_macho.union(mutacoes_femea)
        
        for mutacao in todas_mutacoes:
            if mutacao.tipo_heranca == 'ligado ao sexo dominante':
                prob = CalculadoraGenetica._calcular_probabilidade_ligada_sexo_dominante(mutacao, macho, femea)
            elif mutacao.tipo_heranca == 'ligado ao sexo recessivo':
                prob = CalculadoraGenetica._calcular_probabilidade_ligada_sexo_recessiva(mutacao, macho, femea)
            elif mutacao.tipo_heranca == 'autossômico dominante':
                prob = CalculadoraGenetica._calcular_probabilidade_autossomica_dominante(mutacao, macho, femea)
            elif mutacao.tipo_heranca == 'autossômico recessivo':
                prob = CalculadoraGenetica._calcular_probabilidade_autossomica_recessiva(mutacao, macho, femea)
            else:
                # Mutação desconhecida, assumir recessiva
                prob = CalculadoraGenetica._calcular_probabilidade_autossomica_recessiva(mutacao, macho, femea)
            
            probabilidades[mutacao.nome] = {
                'tipo': mutacao.tipo_heranca,
                'probabilidade': prob,
                'descricao': mutacao.descricao,
                'cor_resultante': mutacao.cor_resultante,
                'gene': mutacao.gene,
                'simbolo': mutacao.simbolo
            }
        
        return probabilidades
    
    @staticmethod
    def _calcular_probabilidade_ligada_sexo_dominante(mutacao, macho, femea):
        """
        Calcula probabilidade para mutações ligadas ao sexo dominantes (ex: Pérola)
        
        Em calopsitas, machos são ZZ e fêmeas são ZW
        Para mutações dominantes ligadas ao sexo:
        - Macho com uma dose (ZpZ): transmite Zp para 50% das filhas, Z para 50% das filhas
        - Macho com duas doses (ZpZp): transmite Zp para todas as filhas
        - Fêmea com uma dose (ZpW): transmite Zp para 50% dos filhos machos
        """
        macho_tem = mutacao in macho.mutacoes or mutacao in macho.mutacoes_portadoras
        femea_tem = mutacao in femea.mutacoes or mutacao in femea.mutacoes_portadoras
        
        # Determinar genótipo do macho
        macho_genotipo = 'normal'
        if mutacao in macho.mutacoes:
            macho_genotipo = 'homozigoto' if macho.get_genotipo_mutacao(mutacao) == 'homozigoto' else 'heterozigoto'
        elif mutacao in macho.mutacoes_portadoras:
            macho_genotipo = 'portador'
        
        # Determinar genótipo da fêmea
        femea_genotipo = 'normal'
        if mutacao in femea.mutacoes:
            femea_genotipo = 'homozigoto'  # Fêmea sempre homozigota se expressa
        elif mutacao in femea.mutacoes_portadoras:
            femea_genotipo = 'portador'
        
        if macho_genotipo == 'homozigoto' and femea_genotipo == 'homozigoto':
            return {
                'machos': {'expressa': 100, 'portador': 0, 'normal': 0},
                'femeas': {'expressa': 100, 'portador': 0, 'normal': 0},
                'descricao': 'Ambos os pais são homozigotos dominantes'
            }
        elif macho_genotipo == 'homozigoto':
            # Macho homozigoto (ZpZp) - passa Zp para todas as filhas
            return {
                'machos': {'expressa': 0, 'portador': 0, 'normal': 100},
                'femeas': {'expressa': 100, 'portador': 0, 'normal': 0},
                'descricao': 'Macho homozigoto dominante - todas as fêmeas serão expressas'
            }
        elif macho_genotipo == 'heterozigoto' and femea_genotipo == 'homozigoto':
            # Macho heterozigoto (ZpZ) + fêmea homozigota (ZpW)
            return {
                'machos': {'expressa': 0, 'portador': 0, 'normal': 100},
                'femeas': {'expressa': 100, 'portador': 0, 'normal': 0},
                'descricao': 'Macho heterozigoto, fêmea homozigota - todas as fêmeas serão expressas'
            }
        elif macho_genotipo == 'heterozigoto' and femea_genotipo == 'portador':
            # Macho heterozigoto (ZpZ) + fêmea portadora (ZpW)
            return {
                'machos': {'expressa': 0, 'portador': 0, 'normal': 100},
                'femeas': {'expressa': 100, 'portador': 0, 'normal': 0},
                'descricao': 'Macho heterozigoto, fêmea portadora - todas as fêmeas serão expressas'
            }
        elif macho_genotipo == 'heterozigoto':
            # Macho heterozigoto (ZpZ) + fêmea normal (ZW)
            return {
                'machos': {'expressa': 0, 'portador': 0, 'normal': 100},
                'femeas': {'expressa': 50, 'portador': 0, 'normal': 50},
                'descricao': 'Macho heterozigoto dominante - 50% das fêmeas serão expressas'
            }
        elif femea_genotipo == 'homozigoto':
            # Macho normal (ZZ) + fêmea homozigota (ZpW)
            return {
                'machos': {'expressa': 0, 'portador': 0, 'normal': 100},
                'femeas': {'expressa': 0, 'portador': 0, 'normal': 100},
                'descricao': 'Fêmea homozigota dominante - nenhum filhote será expresso'
            }
        elif femea_genotipo == 'portador':
            # Macho normal (ZZ) + fêmea portadora (ZpW)
            return {
                'machos': {'expressa': 0, 'portador': 0, 'normal': 100},
                'femeas': {'expressa': 0, 'portador': 0, 'normal': 100},
                'descricao': 'Fêmea portadora dominante - nenhum filhote será expresso'
            }
        else:
            return {
                'machos': {'expressa': 0, 'portador': 0, 'normal': 100},
                'femeas': {'expressa': 0, 'portador': 0, 'normal': 100},
                'descricao': 'Nenhum dos pais possui a mutação'
            }
    
    @staticmethod
    def _calcular_probabilidade_ligada_sexo_recessiva(mutacao, macho, femea):
        """
        Calcula probabilidade para mutações ligadas ao sexo recessivas (ex: Lutino)
        
        Para mutações recessivas ligadas ao sexo:
        - Macho homozigoto recessivo (ZlZl): todos os filhos machos serão recessivos
        - Macho portador (Z+Zl): 50% dos filhos machos serão portadores
        - Fêmea recessiva (ZlW): 50% dos filhos machos serão recessivos
        """
        macho_tem = mutacao in macho.mutacoes or mutacao in macho.mutacoes_portadoras
        femea_tem = mutacao in femea.mutacoes or mutacao in femea.mutacoes_portadoras
        
        # Determinar genótipo do macho
        macho_genotipo = 'normal'
        if mutacao in macho.mutacoes:
            macho_genotipo = 'homozigoto'
        elif mutacao in macho.mutacoes_portadoras:
            macho_genotipo = 'portador'
        
        # Determinar genótipo da fêmea
        femea_genotipo = 'normal'
        if mutacao in femea.mutacoes:
            femea_genotipo = 'homozigoto'
        elif mutacao in femea.mutacoes_portadoras:
            femea_genotipo = 'portador'
        
        if macho_genotipo == 'homozigoto' and femea_genotipo == 'homozigoto':
            return {
                'machos': {'expressa': 100, 'portador': 0, 'normal': 0},
                'femeas': {'expressa': 100, 'portador': 0, 'normal': 0},
                'descricao': 'Ambos os pais são homozigotos recessivos'
            }
        elif macho_genotipo == 'homozigoto':
            # Macho homozigoto recessivo (ZlZl) - passa Zl para todos os filhos
            return {
                'machos': {'expressa': 100, 'portador': 0, 'normal': 0},
                'femeas': {'expressa': 0, 'portador': 0, 'normal': 100},
                'descricao': 'Macho homozigoto recessivo - todos os machos serão recessivos'
            }
        elif macho_genotipo == 'portador' and femea_genotipo == 'homozigoto':
            # Macho portador (Z+Zl) + fêmea homozigota (ZlW)
            return {
                'machos': {'expressa': 50, 'portador': 50, 'normal': 0},
                'femeas': {'expressa': 0, 'portador': 0, 'normal': 100},
                'descricao': 'Macho portador, fêmea homozigota recessiva - 50% dos machos serão recessivos'
            }
        elif macho_genotipo == 'portador' and femea_genotipo == 'portador':
            # Macho portador (Z+Zl) + fêmea portadora (ZlW)
            return {
                'machos': {'expressa': 25, 'portador': 50, 'normal': 25},
                'femeas': {'expressa': 0, 'portador': 0, 'normal': 100},
                'descricao': 'Ambos os pais são portadores - 25% dos machos serão recessivos'
            }
        elif macho_genotipo == 'portador':
            # Macho portador (Z+Zl) + fêmea normal (ZW)
            return {
                'machos': {'expressa': 0, 'portador': 50, 'normal': 50},
                'femeas': {'expressa': 0, 'portador': 0, 'normal': 100},
                'descricao': 'Macho portador recessivo - 50% dos machos serão portadores'
            }
        elif femea_genotipo == 'homozigoto':
            # Macho normal (ZZ) + fêmea homozigota (ZlW)
            return {
                'machos': {'expressa': 0, 'portador': 100, 'normal': 0},
                'femeas': {'expressa': 0, 'portador': 0, 'normal': 100},
                'descricao': 'Fêmea homozigota recessiva - todos os machos serão portadores'
            }
        elif femea_genotipo == 'portador':
            # Macho normal (ZZ) + fêmea portadora (ZlW)
            return {
                'machos': {'expressa': 0, 'portador': 50, 'normal': 50},
                'femeas': {'expressa': 0, 'portador': 0, 'normal': 100},
                'descricao': 'Fêmea portadora recessiva - 50% dos machos serão portadores'
            }
        else:
            return {
                'machos': {'expressa': 0, 'portador': 0, 'normal': 100},
                'femeas': {'expressa': 0, 'portador': 0, 'normal': 100},
                'descricao': 'Nenhum dos pais possui a mutação'
            }
    
    @staticmethod
    def _calcular_probabilidade_autossomica_dominante(mutacao, macho, femea):
        """
        Calcula probabilidade para mutações autossômicas dominantes
        """
        macho_tem = mutacao in macho.mutacoes or mutacao in macho.mutacoes_portadoras
        femea_tem = mutacao in femea.mutacoes or mutacao in femea.mutacoes_portadoras
        
        # Determinar genótipo
        macho_genotipo = 'normal'
        if mutacao in macho.mutacoes:
            macho_genotipo = 'homozigoto' if macho.get_genotipo_mutacao(mutacao) == 'homozigoto' else 'heterozigoto'
        elif mutacao in macho.mutacoes_portadoras:
            macho_genotipo = 'portador'
        
        femea_genotipo = 'normal'
        if mutacao in femea.mutacoes:
            femea_genotipo = 'homozigoto' if femea.get_genotipo_mutacao(mutacao) == 'homozigoto' else 'heterozigoto'
        elif mutacao in femea.mutacoes_portadoras:
            femea_genotipo = 'portador'
        
        if macho_genotipo == 'homozigoto' and femea_genotipo == 'homozigoto':
            return {
                'machos': {'expressa': 100, 'portador': 0, 'normal': 0},
                'femeas': {'expressa': 100, 'portador': 0, 'normal': 0},
                'descricao': 'Ambos os pais são homozigotos dominantes'
            }
        elif macho_genotipo == 'homozigoto' or femea_genotipo == 'homozigoto':
            return {
                'machos': {'expressa': 100, 'portador': 0, 'normal': 0},
                'femeas': {'expressa': 100, 'portador': 0, 'normal': 0},
                'descricao': 'Um dos pais é homozigoto dominante'
            }
        elif macho_genotipo == 'heterozigoto' and femea_genotipo == 'heterozigoto':
            return {
                'machos': {'expressa': 75, 'portador': 0, 'normal': 25},
                'femeas': {'expressa': 75, 'portador': 0, 'normal': 25},
                'descricao': 'Ambos os pais são heterozigotos dominantes'
            }
        elif macho_genotipo == 'heterozigoto' or femea_genotipo == 'heterozigoto':
            return {
                'machos': {'expressa': 50, 'portador': 0, 'normal': 50},
                'femeas': {'expressa': 50, 'portador': 0, 'normal': 50},
                'descricao': 'Um dos pais é heterozigoto dominante'
            }
        else:
            return {
                'machos': {'expressa': 0, 'portador': 0, 'normal': 100},
                'femeas': {'expressa': 0, 'portador': 0, 'normal': 100},
                'descricao': 'Nenhum dos pais possui a mutação dominante'
            }
    
    @staticmethod
    def _calcular_probabilidade_autossomica_recessiva(mutacao, macho, femea):
        """
        Calcula probabilidade para mutações autossômicas recessivas
        """
        macho_tem = mutacao in macho.mutacoes or mutacao in macho.mutacoes_portadoras
        femea_tem = mutacao in femea.mutacoes or mutacao in femea.mutacoes_portadoras
        
        # Determinar genótipo
        macho_genotipo = 'normal'
        if mutacao in macho.mutacoes:
            macho_genotipo = 'homozigoto'
        elif mutacao in macho.mutacoes_portadoras:
            macho_genotipo = 'portador'
        
        femea_genotipo = 'normal'
        if mutacao in femea.mutacoes:
            femea_genotipo = 'homozigoto'
        elif mutacao in femea.mutacoes_portadoras:
            femea_genotipo = 'portador'
        
        if macho_genotipo == 'homozigoto' and femea_genotipo == 'homozigoto':
            return {
                'machos': {'expressa': 100, 'portador': 0, 'normal': 0},
                'femeas': {'expressa': 100, 'portador': 0, 'normal': 0},
                'descricao': 'Ambos os pais são homozigotos recessivos'
            }
        elif macho_genotipo == 'homozigoto' or femea_genotipo == 'homozigoto':
            return {
                'machos': {'expressa': 0, 'portador': 100, 'normal': 0},
                'femeas': {'expressa': 0, 'portador': 100, 'normal': 0},
                'descricao': 'Um dos pais é homozigoto recessivo - todos os filhotes serão portadores'
            }
        elif macho_genotipo == 'portador' and femea_genotipo == 'portador':
            return {
                'machos': {'expressa': 25, 'portador': 50, 'normal': 25},
                'femeas': {'expressa': 25, 'portador': 50, 'normal': 25},
                'descricao': 'Ambos os pais são portadores'
            }
        elif macho_genotipo == 'portador' or femea_genotipo == 'portador':
            return {
                'machos': {'expressa': 0, 'portador': 50, 'normal': 50},
                'femeas': {'expressa': 0, 'portador': 50, 'normal': 50},
                'descricao': 'Um dos pais é portador'
            }
        else:
            return {
                'machos': {'expressa': 0, 'portador': 0, 'normal': 100},
                'femeas': {'expressa': 0, 'portador': 0, 'normal': 100},
                'descricao': 'Nenhum dos pais possui a mutação recessiva'
            }
    
    @staticmethod
    def gerar_relatorio_cruzamento(macho, femea, probabilidades):
        """
        Gera um relatório detalhado do cruzamento
        
        Args:
            macho: Objeto Ave (macho)
            femea: Objeto Ave (fêmea)
            probabilidades: Dicionário de probabilidades
            
        Returns:
            dict: Relatório estruturado
        """
        relatorio = {
            'pais': {
                'macho': {
                    'nome': macho.nome,
                    'mutacoes_visiveis': [m.nome for m in macho.mutacoes],
                    'mutacoes_portadoras': [m.nome for m in macho.mutacoes_portadoras],
                    'idade': macho.idade
                },
                'femea': {
                    'nome': femea.nome,
                    'mutacoes_visiveis': [m.nome for m in femea.mutacoes],
                    'mutacoes_portadoras': [m.nome for m in femea.mutacoes_portadoras],
                    'idade': femea.idade
                }
            },
            'probabilidades': probabilidades,
            'resumo': {
                'total_mutacoes': len(probabilidades),
                'mutacoes_ligadas_sexo_dominante': len([p for p in probabilidades.values() if p['tipo'] == 'ligado ao sexo dominante']),
                'mutacoes_ligadas_sexo_recessivo': len([p for p in probabilidades.values() if p['tipo'] == 'ligado ao sexo recessivo']),
                'mutacoes_autossomicas_dominante': len([p for p in probabilidades.values() if p['tipo'] == 'autossômico dominante']),
                'mutacoes_autossomicas_recessivo': len([p for p in probabilidades.values() if p['tipo'] == 'autossômico recessivo'])
            }
        }
        
        return relatorio 