import bcrypt
from flask import Blueprint, render_template, request, redirect, url_for, session
from decorators import login_required, perfil_required
import database as db

admin_bp = Blueprint('admin', __name__)

PERFIS = ['admin', 'diretor', 'gestor_matriz', 'gestor_piraquara1', 'gestor_piraquara2', 'gestor_maria_antonieta']
LOJAS = ['MATRIZ', 'PIRAQUARA_I', 'PIRAQUARA_II', 'MARIA_ANTONIETA']
LOJA_LABELS = {
    'MATRIZ': 'Matriz',
    'PIRAQUARA_I': 'Piraquara I',
    'PIRAQUARA_II': 'Piraquara II',
    'MARIA_ANTONIETA': 'Maria Antonieta',
}


@admin_bp.route('/admin')
@login_required
@perfil_required('admin')
def index():
    usuarios = db.get_todos_usuarios()
    return render_template('admin/index.html',
        usuarios=usuarios,
        nome=session.get('user_nome'),
        perfil=session.get('user_perfil'),
        loja_labels=LOJA_LABELS,
    )


@admin_bp.route('/admin/usuarios/novo', methods=['GET', 'POST'])
@login_required
@perfil_required('admin')
def novo_usuario():
    error = None
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        login_str = request.form.get('login', '').strip()
        senha = request.form.get('senha', '')
        confirmar = request.form.get('confirmar_senha', '')
        perfil = request.form.get('perfil', '')
        loja = request.form.get('loja', '') or None

        if not all([nome, login_str, senha, perfil]):
            error = 'Todos os campos obrigatórios devem ser preenchidos.'
        elif senha != confirmar:
            error = 'As senhas não coincidem.'
        elif len(senha) < 8:
            error = 'A senha deve ter no mínimo 8 caracteres.'
        else:
            senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt(rounds=12)).decode()
            try:
                db.criar_usuario(nome, login_str, senha_hash, perfil, loja)
                return redirect(url_for('admin.index'))
            except Exception as e:
                error = f"Login '{login_str}' já está em uso." if 'UNIQUE' in str(e) else 'Erro ao criar usuário.'

    return render_template('admin/usuario_form.html',
        modo='novo',
        error=error,
        nome=session.get('user_nome'),
        perfil=session.get('user_perfil'),
        perfis=PERFIS,
        lojas=LOJAS,
        loja_labels=LOJA_LABELS,
        usuario=None,
    )


@admin_bp.route('/admin/usuarios/<int:user_id>', methods=['GET', 'POST'])
@login_required
@perfil_required('admin')
def editar_usuario(user_id):
    usuario = db.get_usuario_by_id(user_id)
    if not usuario:
        return redirect(url_for('admin.index'))

    current_user_id = session.get('user_id')
    error = None

    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        login_str = request.form.get('login', '').strip()
        perfil_novo = request.form.get('perfil', '')
        loja = request.form.get('loja', '') or None
        ativo = 1 if request.form.get('ativo') else 0
        nova_senha = request.form.get('nova_senha', '')

        if user_id == current_user_id and not ativo:
            error = 'Você não pode desativar sua própria conta.'
        elif not all([nome, login_str, perfil_novo]):
            error = 'Nome, login e perfil são obrigatórios.'
        else:
            try:
                db.atualizar_usuario(user_id, nome, login_str, perfil_novo, loja, ativo)
                if nova_senha:
                    if len(nova_senha) < 8:
                        error = 'A nova senha deve ter no mínimo 8 caracteres.'
                    else:
                        h = bcrypt.hashpw(nova_senha.encode(), bcrypt.gensalt(rounds=12)).decode()
                        db.atualizar_senha(user_id, h)
                if not error:
                    return redirect(url_for('admin.index'))
            except Exception as e:
                error = f"Login '{login_str}' já está em uso." if 'UNIQUE' in str(e) else 'Erro ao atualizar usuário.'

    return render_template('admin/usuario_form.html',
        modo='editar',
        error=error,
        nome=session.get('user_nome'),
        perfil=session.get('user_perfil'),
        perfis=PERFIS,
        lojas=LOJAS,
        loja_labels=LOJA_LABELS,
        usuario=usuario,
        current_user_id=current_user_id,
    )
