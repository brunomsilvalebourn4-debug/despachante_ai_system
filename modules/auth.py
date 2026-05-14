from flask import Blueprint, render_template, request, redirect, session
from modules.db import get_connection
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

# LOGIN
@auth.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        senha = request.form['senha']

        conn = get_connection()

        usuario = conn.execute(

            "SELECT * FROM users WHERE email = ?",

            (email,)

        ).fetchone()

        conn.close()

        if usuario and check_password_hash(usuario['senha_hash'], senha):

            session['usuario'] = usuario['nome']

            return redirect('/dashboard')

        return render_template(
            'login.html',
            erro='Email ou senha inválidos'
        )

    return render_template('login.html')

# REGISTRO
@auth.route('/register')
def register_user():

    conn = get_connection()

    # VERIFICA SE JÁ EXISTE
    usuario = conn.execute(
        "SELECT * FROM users WHERE email = ?",
        ('admin@nivaldo.com',)
    ).fetchone()

    # CRIA ADMIN
    if not usuario:

        senha_hash = generate_password_hash('123456')

        conn.execute("""

            INSERT INTO users (
                nome,
                email,
                senha_hash
            )

            VALUES (?, ?, ?)

        """, (

            'Administrador',
            'admin@nivaldo.com',
            senha_hash

        ))

        conn.commit()

    conn.close()

    return '''
    Usuário criado com sucesso!<br><br>

    Login: admin@nivaldo.com<br>
    Senha: 123456
    '''