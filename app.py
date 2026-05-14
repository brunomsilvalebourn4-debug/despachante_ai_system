import os
from flask import Flask, render_template

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

# 👉 DOCUMENTOS
from modules.documentos.routes import documentos_bp

# ====================================
# APP
# ====================================

app = Flask(__name__)

app.secret_key = 'nivaldo_secret'

# ====================================
# CRIAR TABELAS (COM CONTEXTO CORRETO)
# ====================================

with app.app_context():
    criar_tabelas()

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
    return render_template('login.html')


# ====================================
# DASHBOARD
# ====================================

@app.route('/dashboard')
def dashboard():
    conn = get_connection()

    total_clientes = conn.execute(
        "SELECT COUNT(*) FROM clientes"
    ).fetchone()[0]

    total_veiculos = conn.execute(
        "SELECT COUNT(*) FROM veiculos"
    ).fetchone()[0]

    total_processos = conn.execute(
        "SELECT COUNT(*) FROM processos"
    ).fetchone()[0]

    total_documentos = conn.execute(
        "SELECT COUNT(*) FROM documentos"
    ).fetchone()[0]

    conn.close()

    return render_template(
        'dashboard.html',
        total_clientes=total_clientes,
        total_veiculos=total_veiculos,
        total_processos=total_processos,
        total_documentos=total_documentos
    )


# ====================================
# RUN (PRONTO PARA PRODUÇÃO)
# ====================================

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)