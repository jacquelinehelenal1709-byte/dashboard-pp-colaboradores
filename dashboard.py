import json
import os
from datetime import datetime
from flask import Blueprint, render_template, session
from decorators import login_required
import database as db

dashboard_bp = Blueprint('dashboard', __name__)

DADOS_JSON_PATH = os.environ.get(
    'DADOS_JSON_PATH',
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        '..', 'pp_colaboradores', 'saida', 'dados_dashboard.json'
    )
)

LOJAS_ORDEM = ['MATRIZ', 'PIRAQUARA_I', 'PIRAQUARA_II', 'MARIA_ANTONIETA']

LOJA_LABELS = {
    'MATRIZ': 'Matriz',
    'PIRAQUARA_I': 'Piraquara I',
    'PIRAQUARA_II': 'Piraquara II',
    'MARIA_ANTONIETA': 'Maria Antonieta',
}

PERFIL_LOJA = {
    'gestor_matriz': 'MATRIZ',
    'gestor_piraquara1': 'PIRAQUARA_I',
    'gestor_piraquara2': 'PIRAQUARA_II',
    'gestor_maria_antonieta': 'MARIA_ANTONIETA',
}


def _id_class(id_pct):
    if id_pct >= 1.0:
        return 'verde'
    elif id_pct >= 0.95:
        return 'amber'
    return 'vermelho'


def _situacao_class(situacao):
    s = situacao.upper()
    if s == 'ATINGIU':
        return 'badge-verde'
    elif s == 'PARCIAL':
        return 'badge-amber'
    return 'badge-vermelho'


def _situacao_display(situacao):
    return situacao.replace('NAO ', 'NÃO ')


def carregar_dados():
    path = os.path.abspath(DADOS_JSON_PATH)
    if not os.path.exists(path):
        return None, None
    try:
        with open(path, 'r', encoding='utf-8') as f:
            dados = json.load(f)
    except (json.JSONDecodeError, IOError):
        return None, None

    gerado_em = dados.get('gerado_em', '')
    try:
        dt = datetime.fromisoformat(gerado_em)
        gerado_em = dt.strftime('%d/%m/%Y %H:%M')
    except Exception:
        pass

    return dados, gerado_em


def enriquecer_dados(dados):
    for loja_data in dados.get('lojas', {}).values():
        for colab in loja_data.get('colaboradores', []):
            colab['_situacao_class'] = _situacao_class(colab.get('situacao', ''))
            colab['_situacao_display'] = _situacao_display(colab.get('situacao', ''))
            colab['_id_class'] = _id_class(colab.get('id_geral', 0))
            for ind in colab.get('indicadores', {}).values():
                ind['_id_class'] = _id_class(ind.get('id_pct', 0))


@dashboard_bp.route('/')
@dashboard_bp.route('/dashboard')
@login_required
def index():
    perfil = session.get('user_perfil')
    loja_usuario = session.get('user_loja')

    dados, gerado_em = carregar_dados()

    if not dados:
        return render_template('dashboard.html',
            dados_indisponiveis=True,
            gerado_em=None,
            perfil=perfil,
            nome=session.get('user_nome'),
            loja_usuario=loja_usuario,
            loja_labels=LOJA_LABELS,
        )

    enriquecer_dados(dados)

    is_admin_or_diretor = perfil in ('admin', 'diretor')

    if is_admin_or_diretor:
        lojas_visiveis = {k: dados['lojas'][k] for k in LOJAS_ORDEM if k in dados['lojas']}
    else:
        loja_key = PERFIL_LOJA.get(perfil)
        lojas_visiveis = {}
        if loja_key and loja_key in dados['lojas']:
            lojas_visiveis = {loja_key: dados['lojas'][loja_key]}

    consolidado = None
    if is_admin_or_diretor:
        resumos = [l.get('resumo', {}) for l in lojas_visiveis.values()]
        todos_colabs = []
        for loja_key, loja_data in lojas_visiveis.items():
            for colab in loja_data.get('colaboradores', []):
                todos_colabs.append({**colab, '_loja_label': LOJA_LABELS.get(loja_key, loja_key)})
        todos_colabs.sort(key=lambda x: x.get('id_geral', 0), reverse=True)

        consolidado = {
            'total_colaboradores': sum(r.get('total_colaboradores', 0) for r in resumos),
            'faturamento_realizado': sum(r.get('faturamento_realizado', 0) for r in resumos),
            'faturamento_previsto': sum(r.get('faturamento_previsto', 0) for r in resumos),
            'premio_total_ganho': sum(r.get('premio_total_ganho', 0) for r in resumos),
            'premio_total_possivel': sum(r.get('premio_total_possivel', 0) for r in resumos),
            'id_medio': (
                sum(r.get('id_medio', 0) for r in resumos) / len(resumos) if resumos else 0
            ),
            'colaboradores_ranking': todos_colabs,
        }

    periodo = dados.get('periodo', {})
    periodo_str = ''
    try:
        di = datetime.fromisoformat(periodo['inicio']).strftime('%d/%m')
        df = datetime.fromisoformat(periodo['fim']).strftime('%d/%m/%Y')
        periodo_str = f'{di} a {df}'
    except Exception:
        periodo_str = f"{periodo.get('inicio', '')} a {periodo.get('fim', '')}"

    return render_template('dashboard.html',
        dados_indisponiveis=False,
        gerado_em=gerado_em,
        perfil=perfil,
        nome=session.get('user_nome'),
        loja_usuario=loja_usuario,
        lojas=lojas_visiveis,
        lojas_ordem=[k for k in LOJAS_ORDEM if k in lojas_visiveis],
        loja_labels=LOJA_LABELS,
        consolidado=consolidado,
        is_admin_or_diretor=is_admin_or_diretor,
        periodo=periodo_str,
    )
