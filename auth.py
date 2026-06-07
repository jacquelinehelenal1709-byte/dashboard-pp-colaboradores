import secrets
import bcrypt
from flask import Blueprint, render_template, request, redirect, url_for, session
import database as db

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('session_token'):
        return redirect(url_for('dashboard.index'))

    error = None
    msg_info = None

    if request.args.get('msg') == 'sessao_expirada':
        msg_info = 'Sua sessão expirou. Faça login novamente.'

    if request.method == 'POST':
        login_input = request.form.get('login', '').strip()
        senha_input = request.form.get('senha', '')
        ip = request.remote_addr

        bloqueado, minutos = db.verificar_bloqueio(ip)
        if bloqueado:
            error = f'Acesso bloqueado. Tente novamente em {minutos} minuto(s).'
            return render_template('login.html', error=error)

        usuario = db.get_usuario_by_login(login_input)

        if usuario and bcrypt.checkpw(senha_input.encode(), usuario['senha_hash'].encode()):
            db.limpar_tentativas(ip)
            token = secrets.token_hex(32)
            db.criar_sessao(token, usuario['id'])
            db.atualizar_ultimo_acesso(usuario['id'])
            db.limpar_sessoes_expiradas()

            session.permanent = True
            session['session_token'] = token
            session['user_id'] = usuario['id']
            session['user_nome'] = usuario['nome']
            session['user_perfil'] = usuario['perfil']
            session['user_loja'] = usuario['loja']

            return redirect(url_for('dashboard.index'))
        else:
            db.registrar_tentativa_falha(ip)
            row = db.get_tentativas(ip)
            tentativas = row['tentativas'] if row else 1
            if tentativas >= 5:
                error = 'Acesso bloqueado por 15 minutos.'
            else:
                restantes = 5 - tentativas
                error = f'Usuário ou senha inválidos. {restantes} tentativa(s) restante(s).'

    return render_template('login.html', error=error, msg_info=msg_info)


@auth_bp.route('/logout')
def logout():
    token = session.get('session_token')
    if token:
        db.deletar_sessao(token)
    session.clear()
    return redirect(url_for('auth.login'))
