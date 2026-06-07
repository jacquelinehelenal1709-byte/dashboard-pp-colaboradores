import sqlite3
import os
from datetime import datetime, timedelta

DB_PATH = os.environ.get(
    'DB_PATH',
    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'usuarios.db')
)


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with get_db() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                login TEXT NOT NULL UNIQUE,
                senha_hash TEXT NOT NULL,
                perfil TEXT NOT NULL,
                loja TEXT,
                ativo INTEGER NOT NULL DEFAULT 1,
                criado_em TEXT NOT NULL,
                ultimo_acesso TEXT
            );
            CREATE TABLE IF NOT EXISTS sessoes (
                token TEXT PRIMARY KEY,
                user_id INTEGER NOT NULL,
                expires_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES usuarios(id)
            );
            CREATE TABLE IF NOT EXISTS tentativas_login (
                ip TEXT PRIMARY KEY,
                tentativas INTEGER NOT NULL DEFAULT 0,
                bloqueado_ate TEXT,
                ultima_tentativa TEXT NOT NULL
            );
        """)


def get_usuario_by_login(login):
    with get_db() as conn:
        return conn.execute(
            "SELECT * FROM usuarios WHERE login = ? AND ativo = 1", (login,)
        ).fetchone()


def get_usuario_by_id(user_id):
    with get_db() as conn:
        return conn.execute("SELECT * FROM usuarios WHERE id = ?", (user_id,)).fetchone()


def get_todos_usuarios():
    with get_db() as conn:
        return conn.execute("SELECT * FROM usuarios ORDER BY perfil, nome").fetchall()


def criar_usuario(nome, login, senha_hash, perfil, loja=None):
    with get_db() as conn:
        conn.execute(
            "INSERT INTO usuarios (nome, login, senha_hash, perfil, loja, ativo, criado_em) VALUES (?, ?, ?, ?, ?, 1, ?)",
            (nome, login, senha_hash, perfil, loja, datetime.now().isoformat())
        )


def atualizar_usuario(user_id, nome, login, perfil, loja, ativo):
    with get_db() as conn:
        conn.execute(
            "UPDATE usuarios SET nome=?, login=?, perfil=?, loja=?, ativo=? WHERE id=?",
            (nome, login, perfil, loja, ativo, user_id)
        )


def atualizar_senha(user_id, senha_hash):
    with get_db() as conn:
        conn.execute("UPDATE usuarios SET senha_hash=? WHERE id=?", (senha_hash, user_id))


def atualizar_ultimo_acesso(user_id):
    with get_db() as conn:
        conn.execute(
            "UPDATE usuarios SET ultimo_acesso=? WHERE id=?",
            (datetime.now().isoformat(), user_id)
        )


# ── Sessions ──────────────────────────────────────────────────────────────────

def criar_sessao(token, user_id, hours=4):
    expires = (datetime.now() + timedelta(hours=hours)).isoformat()
    with get_db() as conn:
        conn.execute(
            "INSERT INTO sessoes (token, user_id, expires_at) VALUES (?, ?, ?)",
            (token, user_id, expires)
        )


def get_sessao(token):
    with get_db() as conn:
        return conn.execute(
            "SELECT * FROM sessoes WHERE token = ?", (token,)
        ).fetchone()


def deletar_sessao(token):
    with get_db() as conn:
        conn.execute("DELETE FROM sessoes WHERE token = ?", (token,))


def limpar_sessoes_expiradas():
    with get_db() as conn:
        conn.execute(
            "DELETE FROM sessoes WHERE expires_at < ?", (datetime.now().isoformat(),)
        )


# ── Rate limiting ──────────────────────────────────────────────────────────────

def verificar_bloqueio(ip):
    """Returns (bloqueado: bool, minutos_restantes: int)."""
    with get_db() as conn:
        row = conn.execute(
            "SELECT * FROM tentativas_login WHERE ip = ?", (ip,)
        ).fetchone()
        if not row or not row['bloqueado_ate']:
            return False, 0
        bloqueado_ate = datetime.fromisoformat(row['bloqueado_ate'])
        if datetime.now() > bloqueado_ate:
            conn.execute("DELETE FROM tentativas_login WHERE ip = ?", (ip,))
            return False, 0
        restante = int((bloqueado_ate - datetime.now()).total_seconds() / 60) + 1
        return True, restante


def registrar_tentativa_falha(ip):
    now = datetime.now().isoformat()
    with get_db() as conn:
        row = conn.execute(
            "SELECT * FROM tentativas_login WHERE ip = ?", (ip,)
        ).fetchone()
        if row:
            novas = row['tentativas'] + 1
            bloqueado_ate = (
                (datetime.now() + timedelta(minutes=15)).isoformat()
                if novas >= 5 else None
            )
            conn.execute(
                "UPDATE tentativas_login SET tentativas=?, bloqueado_ate=?, ultima_tentativa=? WHERE ip=?",
                (novas, bloqueado_ate, now, ip)
            )
        else:
            conn.execute(
                "INSERT INTO tentativas_login (ip, tentativas, bloqueado_ate, ultima_tentativa) VALUES (?, 1, NULL, ?)",
                (ip, now)
            )


def get_tentativas(ip):
    with get_db() as conn:
        return conn.execute(
            "SELECT * FROM tentativas_login WHERE ip = ?", (ip,)
        ).fetchone()


def limpar_tentativas(ip):
    with get_db() as conn:
        conn.execute("DELETE FROM tentativas_login WHERE ip = ?", (ip,))
