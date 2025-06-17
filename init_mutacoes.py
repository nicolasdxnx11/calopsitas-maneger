import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import Mutacao

def init_mutacoes():
    app = create_app()
    with app.app_context():
        # Lista completa de mutações
        mutacoes = [
            {
                'nome': 'Normal',
                'tipo_heranca': 'dominante',
                'descricao': 'Padrão selvagem, cor cinza com face amarela',
                'cor_resultante': 'Cinza com face amarela',
                'gene': 'Normal',
                'simbolo': 'N',
                'alelo_dominante': 'N',
                'alelo_recessivo': 'n'
            },
            {
                'nome': 'Arlequim',
                'tipo_heranca': 'ligado ao sexo',
                'descricao': 'Padrão de penas com manchas brancas',
                'cor_resultante': 'Cinza com manchas brancas',
                'gene': 'Arlequim',
                'simbolo': 'A',
                'alelo_dominante': 'A',
                'alelo_recessivo': 'a'
            },
            {
                'nome': 'Cara Branca',
                'tipo_heranca': 'ligado ao sexo',
                'descricao': 'Face branca sem bochechas amarelas',
                'cor_resultante': 'Cinza com face branca',
                'gene': 'Cara Branca',
                'simbolo': 'B',
                'alelo_dominante': 'B',
                'alelo_recessivo': 'b'
            },
            {
                'nome': 'Lutino',
                'tipo_heranca': 'ligado ao sexo',
                'descricao': 'Cor amarela com olhos vermelhos',
                'cor_resultante': 'Amarelo',
                'gene': 'Lutino',
                'simbolo': 'L',
                'alelo_dominante': 'L',
                'alelo_recessivo': 'l'
            },
            {
                'nome': 'Albino',
                'tipo_heranca': 'ligado ao sexo',
                'descricao': 'Cor branca com olhos vermelhos',
                'cor_resultante': 'Branco',
                'gene': 'Albino',
                'simbolo': 'A',
                'alelo_dominante': 'A',
                'alelo_recessivo': 'a'
            },
            {
                'nome': 'Canela',
                'tipo_heranca': 'ligado ao sexo',
                'descricao': 'Cor mais clara que o normal',
                'cor_resultante': 'Canela',
                'gene': 'Canela',
                'simbolo': 'C',
                'alelo_dominante': 'C',
                'alelo_recessivo': 'c'
            },
            {
                'nome': 'Opalino',
                'tipo_heranca': 'ligado ao sexo',
                'descricao': 'Padrão de penas com bordas mais claras',
                'cor_resultante': 'Opalino',
                'gene': 'Opalino',
                'simbolo': 'O',
                'alelo_dominante': 'O',
                'alelo_recessivo': 'o'
            },
            {
                'nome': 'Pérola',
                'tipo_heranca': 'ligado ao sexo',
                'descricao': 'Padrão de penas com manchas em forma de pérola',
                'cor_resultante': 'Pérola',
                'gene': 'Pérola',
                'simbolo': 'P',
                'alelo_dominante': 'P',
                'alelo_recessivo': 'p'
            },
            {
                'nome': 'Fulvo',
                'tipo_heranca': 'ligado ao sexo',
                'descricao': 'Cor marrom avermelhada',
                'cor_resultante': 'Fulvo',
                'gene': 'Fulvo',
                'simbolo': 'F',
                'alelo_dominante': 'F',
                'alelo_recessivo': 'f'
            },
            {
                'nome': 'Prata',
                'tipo_heranca': 'ligado ao sexo',
                'descricao': 'Cor prateada com face amarela',
                'cor_resultante': 'Prata',
                'gene': 'Prata',
                'simbolo': 'S',
                'alelo_dominante': 'S',
                'alelo_recessivo': 's'
            },
            {
                'nome': 'Oliva',
                'tipo_heranca': 'ligado ao sexo',
                'descricao': 'Cor oliva com face amarela',
                'cor_resultante': 'Oliva',
                'gene': 'Oliva',
                'simbolo': 'O',
                'alelo_dominante': 'O',
                'alelo_recessivo': 'o'
            },
            {
                'nome': 'Cara Branca Lutino',
                'tipo_heranca': 'ligado ao sexo',
                'descricao': 'Combinação de Cara Branca e Lutino',
                'cor_resultante': 'Branco com face branca',
                'gene': 'Cara Branca Lutino',
                'simbolo': 'BL',
                'alelo_dominante': 'BL',
                'alelo_recessivo': 'bl'
            },
            {
                'nome': 'Arlequim Lutino',
                'tipo_heranca': 'ligado ao sexo',
                'descricao': 'Combinação de Arlequim e Lutino',
                'cor_resultante': 'Amarelo com manchas brancas',
                'gene': 'Arlequim Lutino',
                'simbolo': 'AL',
                'alelo_dominante': 'AL',
                'alelo_recessivo': 'al'
            },
            {
                'nome': 'Canela Lutino',
                'tipo_heranca': 'ligado ao sexo',
                'descricao': 'Combinação de Canela e Lutino',
                'cor_resultante': 'Canela claro',
                'gene': 'Canela Lutino',
                'simbolo': 'CL',
                'alelo_dominante': 'CL',
                'alelo_recessivo': 'cl'
            },
            {
                'nome': 'Opalino Lutino',
                'tipo_heranca': 'ligado ao sexo',
                'descricao': 'Combinação de Opalino e Lutino',
                'cor_resultante': 'Amarelo com padrão opalino',
                'gene': 'Opalino Lutino',
                'simbolo': 'OL',
                'alelo_dominante': 'OL',
                'alelo_recessivo': 'ol'
            }
        ]

        # Adicionar mutações ao banco
        for mutacao_data in mutacoes:
            mutacao = Mutacao.query.filter_by(nome=mutacao_data['nome']).first()
            if not mutacao:
                mutacao = Mutacao(**mutacao_data)
                db.session.add(mutacao)
        
        db.session.commit()
        print("✅ Mutações inicializadas com sucesso!")

if __name__ == '__main__':
    init_mutacoes() 