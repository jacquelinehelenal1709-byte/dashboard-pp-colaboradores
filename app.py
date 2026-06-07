import os
from flask import Flask
from dotenv import load_dotenv

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get('SECRET_KEY', 'dev-insecure-key-CHANGE-IN-PRODUCTION')
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['SESSION_COOKIE_SECURE'] = os.environ.get('FLASK_ENV') == 'production'
    app.config['PERMANENT_SESSION_LIFETIME'] = 14400  # 4 horas

    # ── Template filters ──────────────────────────────────────────────────────

    @app.template_filter('brl')
    def brl_filter(value):
        if value is None:
            return '—'
        negative = value < 0
        parts = f'{abs(value):,.2f}'.split('.')
        integer_part = parts[0].replace(',', '.')
        result = f'R$ {integer_part},{parts[1]}'
        return f'- {result}' if negative else result

    @app.template_filter('brl_k')
    def brl_k_filter(value):
        """Compact: 48.2K or R$ 350"""
        if value is None:
            return '—'
        if abs(value) >= 1000:
            return f"R$ {value / 1000:.1f}K".replace('.', ',')
        return f'R$ {value:.0f}'

    @app.template_filter('brl_short')
    def brl_short_filter(value):
        """R$ 350,00 — for prize amounts"""
        if value is None:
            return '—'
        negative = value < 0
        formatted = f'{abs(value):.2f}'.replace('.', ',')
        result = f'R$ {formatted}'
        return f'- {result}' if negative else result

    @app.template_filter('pct')
    def pct_filter(value):
        if value is None:
            return '—'
        return f'{value * 100:.1f}%'

    @app.template_filter('qtd')
    def qtd_filter(value):
        if value is None:
            return '—'
        return str(int(round(value)))

    @app.template_filter('fmt_ind')
    def fmt_ind_filter(value, is_quantidade=False):
        if is_quantidade:
            return qtd_filter(value)
        return brl_k_filter(value)

    app.jinja_env.globals['min'] = min
    app.jinja_env.globals['max'] = max

    # ── Blueprints ────────────────────────────────────────────────────────────

    from auth import auth_bp
    from dashboard import dashboard_bp
    from admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(admin_bp)

    # ── Init DB ───────────────────────────────────────────────────────────────

    from database import init_db
    with app.app_context():
        init_db()

    return app


app = create_app()

if __name__ == '__main__':
    debug = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(debug=debug, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
