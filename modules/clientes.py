from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect

import sqlite3

from config import Config

# ====================================
# BLUEPRINT
# ====================================

clientes = Blueprint(
    'clientes',
    __name__
)

# ====================================
# CONEXÃO
# ====================================

def get_connection():

    conn = sqlite3.connect(
        Config.DB_NAME
    )

    conn.row_factory = sqlite3.Row

    return conn

# ====================================
# LISTAR + CADASTRAR
# ====================================

@clientes.route('/clientes', methods=['GET', 'POST'])
def pagina_clientes():

    conn = get_connection()

    # ====================================
    # SALVAR
    # ====================================

    if request.method == 'POST':

        nome = request.form.get('nome')

        telefone = request.form.get('telefone')

        cpf = request.form.get('cpf')

        rg = request.form.get('rg')

        org_exp = request.form.get('org_exp')

        uf_exp = request.form.get('uf_exp')

        pgu_registro = request.form.get('pgu_registro')

        nome_pai = request.form.get('nome_pai')

        nome_mae = request.form.get('nome_mae')

        data_nascimento = request.form.get(
            'data_nascimento'
        )

        vencimento_cnh = request.form.get(
            'vencimento_cnh'
        )

        email = request.form.get('email')

        cep = request.form.get('cep')

        endereco = request.form.get('endereco')

        numero = request.form.get('numero')

        bairro = request.form.get('bairro')

        cidade = request.form.get('cidade')

        estado = request.form.get('estado')

        conn.execute("""

            INSERT INTO clientes (

                nome,
                telefone,
                cpf,
                rg,
                org_exp,
                uf_exp,
                pgu_registro,
                nome_pai,
                nome_mae,
                data_nascimento,
                vencimento_cnh,
                email,
                cep,
                endereco,
                numero,
                bairro,
                cidade,
                estado

            )

            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

        """, (

            nome,
            telefone,
            cpf,
            rg,
            org_exp,
            uf_exp,
            pgu_registro,
            nome_pai,
            nome_mae,
            data_nascimento,
            vencimento_cnh,
            email,
            cep,
            endereco,
            numero,
            bairro,
            cidade,
            estado

        ))

        conn.commit()

    # ====================================
    # LISTA CLIENTES
    # ====================================

    lista_clientes = conn.execute("""

        SELECT *
        FROM clientes
        ORDER BY id DESC

    """).fetchall()

    conn.close()

    return render_template(
        'clientes.html',
        clientes_lista=lista_clientes
    )

# ====================================
# EDITAR CLIENTE
# ====================================

@clientes.route('/editar_cliente/<int:id>', methods=['GET', 'POST'])
def editar_cliente(id):

    conn = get_connection()

    cliente = conn.execute("""

        SELECT *
        FROM clientes
        WHERE id = ?

    """, (id,)).fetchone()

    # ====================================
    # SALVAR ALTERAÇÃO
    # ====================================

    if request.method == 'POST':

        nome = request.form.get('nome')

        telefone = request.form.get('telefone')

        cpf = request.form.get('cpf')

        rg = request.form.get('rg')

        org_exp = request.form.get('org_exp')

        uf_exp = request.form.get('uf_exp')

        pgu_registro = request.form.get('pgu_registro')

        nome_pai = request.form.get('nome_pai')

        nome_mae = request.form.get('nome_mae')

        data_nascimento = request.form.get(
            'data_nascimento'
        )

        vencimento_cnh = request.form.get(
            'vencimento_cnh'
        )

        email = request.form.get('email')

        cep = request.form.get('cep')

        endereco = request.form.get('endereco')

        numero = request.form.get('numero')

        bairro = request.form.get('bairro')

        cidade = request.form.get('cidade')

        estado = request.form.get('estado')

        conn.execute("""

            UPDATE clientes

            SET

                nome = ?,
                telefone = ?,
                cpf = ?,
                rg = ?,
                org_exp = ?,
                uf_exp = ?,
                pgu_registro = ?,
                nome_pai = ?,
                nome_mae = ?,
                data_nascimento = ?,
                vencimento_cnh = ?,
                email = ?,
                cep = ?,
                endereco = ?,
                numero = ?,
                bairro = ?,
                cidade = ?,
                estado = ?

            WHERE id = ?

        """, (

            nome,
            telefone,
            cpf,
            rg,
            org_exp,
            uf_exp,
            pgu_registro,
            nome_pai,
            nome_mae,
            data_nascimento,
            vencimento_cnh,
            email,
            cep,
            endereco,
            numero,
            bairro,
            cidade,
            estado,
            id

        ))

        conn.commit()

        conn.close()

        return redirect('/clientes')

    conn.close()

    return render_template(
        'editar_cliente.html',
        cliente=cliente
    )