"""
Seed inicial: cria usuarios e dados de exemplo.
Executar uma vez: python seed.py
"""
import os
import json
import bcrypt
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

from database import init_db, get_db

USUARIOS_INICIAIS = [
    {'nome': 'Jacqueline Silva',     'login': 'jacqueline',       'perfil': 'admin',                  'loja': None},
    {'nome': 'Diretoria',            'login': 'diretor',          'perfil': 'diretor',                 'loja': None},
    {'nome': 'Gestor Matriz',        'login': 'gestor.matriz',    'perfil': 'gestor_matriz',           'loja': 'MATRIZ'},
    {'nome': 'Gestor Piraquara I',   'login': 'gestor.pira1',     'perfil': 'gestor_piraquara1',       'loja': 'PIRAQUARA_I'},
    {'nome': 'Gestor Piraquara II',  'login': 'gestor.pira2',     'perfil': 'gestor_piraquara2',       'loja': 'PIRAQUARA_II'},
    {'nome': 'Gestor M. Antonieta',  'login': 'gestor.maria',     'perfil': 'gestor_maria_antonieta',  'loja': 'MARIA_ANTONIETA'},
]

SENHA_INICIAL = 'Farmanello@2026'


def seed_usuarios():
    print('Criando usuários iniciais...')
    with get_db() as conn:
        for u in USUARIOS_INICIAIS:
            existing = conn.execute(
                'SELECT id FROM usuarios WHERE login = ?', (u['login'],)
            ).fetchone()
            if existing:
                print(f"  [skip] {u['login']} — já existe")
                continue
            h = bcrypt.hashpw(SENHA_INICIAL.encode(), bcrypt.gensalt(rounds=12)).decode()
            conn.execute(
                'INSERT INTO usuarios (nome, login, senha_hash, perfil, loja, ativo, criado_em) VALUES (?, ?, ?, ?, ?, 1, ?)',
                (u['nome'], u['login'], h, u['perfil'], u['loja'], datetime.now().isoformat())
            )
            print(f"  [ok]   {u['login']} ({u['perfil']})")


def _make_colab(nome, id_geral, situacao):
    escala = 1.0 if id_geral >= 1.0 else 0.0
    return {
        'nome': nome,
        'total_dias': 26, 'dias_trabalhados': 5, 'dias_restantes': 21,
        'base_calculo': 700.00,
        'id_geral': id_geral,
        'situacao': situacao,
        'premio_total': 700.00 if id_geral >= 1.0 else 0.00,
        'val_perdido': 0.00 if id_geral >= 1.0 else 700.00,
        'falta_mes': 50000.00,
        'val_nec_dia': 2380.95,
        'indicadores': {
            'venda_geral': {
                'meta': 55000.0, 'realizado': 10571.0, 'previsao': 55000.0,
                'id_pct': id_geral, 'escala': escala, 'peso': 0.50,
                'premio_base': 350.0, 'premio_ganho': 350.0 if id_geral >= 1.0 else 0.0,
                'sem_meta': False, 'is_quantidade': False
            },
            'vitaminas': {
                'meta': 115.0, 'realizado': 25.0, 'previsao': 130.0,
                'id_pct': 1.13, 'escala': 1.0, 'peso': 0.20,
                'premio_base': 140.0, 'premio_ganho': 140.0,
                'sem_meta': False, 'is_quantidade': True
            },
            'nao_medicamentos': {
                'meta': 11000.0, 'realizado': 2200.0, 'previsao': 11440.0,
                'id_pct': 1.04, 'escala': 1.0, 'peso': 0.30,
                'premio_base': 210.0, 'premio_ganho': 210.0,
                'sem_meta': False, 'is_quantidade': False
            },
        }
    }


def seed_dados_exemplo():
    dados_path = os.path.abspath(os.environ.get(
        'DADOS_JSON_PATH',
        os.path.join(os.path.dirname(__file__), '..', 'pp_colaboradores', 'saida', 'dados_dashboard.json')
    ))

    if os.path.exists(dados_path):
        print(f'  [skip] dados_dashboard.json já existe')
        return

    dados = {
        'gerado_em': datetime.now().isoformat(),
        'periodo': {'inicio': '2026-06-01', 'fim': '2026-06-05'},
        'lojas': {
            'MATRIZ': {
                'resumo': {
                    'total_colaboradores': 3, 'faturamento_realizado': 31500.0,
                    'faturamento_previsto': 165000.0, 'id_medio': 0.9700,
                    'premio_total_ganho': 1400.0, 'premio_total_possivel': 2100.0
                },
                'colaboradores': [
                    _make_colab('ELOY',    1.02, 'ATINGIU'),
                    _make_colab('MARIANA', 0.97, 'PARCIAL'),
                    _make_colab('CARLOS',  0.88, 'NAO ATINGIU'),
                ]
            },
            'PIRAQUARA_I': {
                'resumo': {
                    'total_colaboradores': 2, 'faturamento_realizado': 20000.0,
                    'faturamento_previsto': 104000.0, 'id_medio': 1.0800,
                    'premio_total_ganho': 1400.0, 'premio_total_possivel': 1400.0
                },
                'colaboradores': [
                    _make_colab('FERNANDA', 1.15, 'ATINGIU'),
                    _make_colab('ROBERTO',  1.05, 'ATINGIU'),
                ]
            },
            'PIRAQUARA_II': {
                'resumo': {
                    'total_colaboradores': 2, 'faturamento_realizado': 15400.0,
                    'faturamento_previsto': 80000.0, 'id_medio': 0.9200,
                    'premio_total_ganho': 0.0, 'premio_total_possivel': 1400.0
                },
                'colaboradores': [
                    _make_colab('PATRICIA', 0.94, 'PARCIAL'),
                    _make_colab('LUCAS',    0.90, 'NAO ATINGIU'),
                ]
            },
            'MARIA_ANTONIETA': {
                'resumo': {
                    'total_colaboradores': 2, 'faturamento_realizado': 24200.0,
                    'faturamento_previsto': 126000.0, 'id_medio': 1.0800,
                    'premio_total_ganho': 1400.0, 'premio_total_possivel': 1400.0
                },
                'colaboradores': [
                    _make_colab('AMANDA', 1.12, 'ATINGIU'),
                    _make_colab('THIAGO', 1.04, 'ATINGIU'),
                ]
            },
        }
    }

    os.makedirs(os.path.dirname(dados_path), exist_ok=True)
    with open(dados_path, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
    print(f'  [ok]   dados_dashboard.json criado em: {dados_path}')


if __name__ == '__main__':
    print('Inicializando banco de dados...')
    init_db()
    seed_usuarios()
    print('Criando dados de exemplo...')
    seed_dados_exemplo()
    print()
    print('Seed concluído!')
    print(f'Senha inicial de todos os usuários: {SENHA_INICIAL}')
    print('IMPORTANTE: altere as senhas em produção via /admin')
