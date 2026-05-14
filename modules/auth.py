from flask import Blueprint, render_template, request, redirect, session
from modules.db import get_connection
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

# ====================================
# LOGIN
# ====================================

@auth.route('/login', methods=['GET', 'POST'])
def login():

    erro = None

    if request.method == 'POST':

        email = request.form.get('email')
        senha = request.form.get('senha')

        conn = get_connection()

        usuario = conn.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        ).fetchone()

        conn.close()

        # 🔴 usuário não existe
        if not usuario:
            erro = "Usuário não encontrado"

        # 🔴 senha não existe no banco (proteção extra)
        elif not usuario["senha_hash"]:
            erro = "Erro no usuário (sem senha cadastrada)"

        # 🔴 senha inválida
        elif not check_password_hash(usuario["senha_hash"], senha):
            erro = "Senha incorreta"

        # 🟢 login OK
        else:
            session.clear()
            session['usuario'] = usuario['nome']
            return redirect('/dashboard')

    return render_template('login.html', erro=erro)


# ====================================
# CRIAR ADMIN (AUTO GARANTIDO)
# ====================================

@auth.route('/register')
def register_user():

    conn = get_connection()

    usuario = conn.execute(
        "SELECT * FROM users WHERE email = ?",
        ('admin@nivaldo.com',)
    ).fetchone()

    if not usuario:

        senha_hash = generate_password_hash('123456')

        conn.execute("""
            INSERT INTO users (nome, email, senha_hash)
            VALUES (?, ?, ?)
        """, (
            'Administrador',
            'admin@nivaldo.com',
            senha_hash
        ))

        conn.commit()

    conn.close()

    return """
    ✔ Usuário do sistema pronto!<br><br>
    Login: admin@nivaldo.com<br>
    Senha: 123456<br><br>
    Acesse /login agora
    """