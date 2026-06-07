from functools import wraps
from flask import session, redirect, url_for, abort
from datetime import datetime
import database as db


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = session.get('session_token')
        user_id = session.get('user_id')
        if not token or not user_id:
            return redirect(url_for('auth.login'))
        sessao = db.get_sessao(token)
        if not sessao:
            session.clear()
            return redirect(url_for('auth.login'))
        if datetime.fromisoformat(sessao['expires_at']) < datetime.now():
            db.deletar_sessao(token)
            session.clear()
            return redirect(url_for('auth.login', msg='sessao_expirada'))
        return f(*args, **kwargs)
    return decorated


def perfil_required(*perfis):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            user_id = session.get('user_id')
            if not user_id:
                return redirect(url_for('auth.login'))
            usuario = db.get_usuario_by_id(user_id)
            if not usuario or usuario['perfil'] not in perfis:
                abort(403)
            return f(*args, **kwargs)
        return decorated
    return decorator
