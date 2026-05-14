import os
from flask import Flask, render_template, redirect, session

# ====================================
# DATABASE
# ====================================

from modules.db import criar_tabelas, get_connection

# ====================================
# BLUEPRINTS
# ====================================

from modules.auth import auth
from modules.clientes import clientes
from modules.veiculos import veiculos
from modules.processos import processos
from modules.ai_assistant import ai_bp
from modules.documentos.routes import documentos_bp

# ====================================
# APP
# ====================================

app = Flask(__name__)

# 🔐 SECRET KEY SEGURA (Render + local)
app.secret_key = os.environ.get("SECRET_KEY", "dev_secret_fraco")

# 🍪 CONFIGURAÇÃO DE SESSÃO (IMPORTANTE NO RENDER)
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax"
)

# ====================================
# CRIAR TABELAS (STARTUP)
# ====================================

def inicializar_banco():
    try:
        criar_tabelas()
        print("✔ Banco inicializado com sucesso")
    except Exception as e:
        print("❌ Erro ao criar tabelas:", e)

with app.app_context():
    inicializar_banco()

# ====================================
# BLUEPRINTS
# ====================================

app.register_blueprint(auth)
app.register_blueprint(clientes)
app.register_blueprint(veiculos)
app.register_blueprint(processos)
app.register_blueprint(ai_bp)
app.register_blueprint(documentos_bp)

# ====================================
# HOME
# ====================================

@app.route('/')
def home():
    return redirect('/login')

# ====================================
# DASHBOARD (🔐 PROTEGIDO)
# ====================================

@app.route('/dashboard')
def dashboard():

    # 🔴 SE NÃO ESTIVER LOGADO, VOLTA PRO LOGIN
    if 'usuario' not in session:
        return redirect('/login')

    conn = get_connection()

    total_clientes = conn.execute("SELECT COUNT(*) FROM clientes").fetchone()[0]
    total_veiculos = conn.execute("SELECT COUNT(*) FROM veiculos").fetchone()[0]
    total_processos = conn.execute("SELECT COUNT(*) FROM processos").fetchone()[0]
    total_documentos = conn.execute("SELECT COUNT(*) FROM documentos").fetchone()[0]

    conn.close()

    return render_template(
        'dashboard.html',
        total_clientes=total_clientes,
        total_veiculos=total_veiculos,
        total_processos=total_processos,
        total_documentos=total_documentos
    )

# ====================================
# RUN
# ====================================

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)