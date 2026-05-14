from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect

from modules.db import get_connection

processos = Blueprint(
    'processos',
    __name__
)

@processos.route('/processos', methods=['GET', 'POST'])
def pagina_processos():

    conn = get_connection()

    # =========================================
    # SALVAR
    # =========================================

    if request.method == 'POST':

        cliente_id = request.form.get(
            'cliente_id'
        )

        veiculo_id = request.form.get(
            'veiculo_id'
        )

        tipo_servico = request.form.get(
            'tipo_servico'
        )

        valor_venda = request.form.get(
            'valor_venda'
        )

        nota_fiscal = request.form.get(
            'nota_fiscal'
        )

        status = request.form.get(
            'status'
        )

        motivo_pendencia = request.form.get(
            'motivo_pendencia'
        )

        conn.execute("""

            INSERT INTO processos (

                cliente_id,
                veiculo_id,

                tipo_servico,
                status,

                motivo_pendencia,

                valor_venda,
                nota_fiscal

            )

            VALUES (?, ?, ?, ?, ?, ?, ?)

        """, (

            cliente_id,
            veiculo_id,

            tipo_servico,
            status,

            motivo_pendencia,

            valor_venda,
            nota_fiscal

        ))

        conn.commit()

        return redirect('/processos')

    # =========================================
    # LISTAS
    # =========================================

    clientes = conn.execute("""

        SELECT *
        FROM clientes
        ORDER BY nome

    """).fetchall()

    veiculos = conn.execute("""

        SELECT *
        FROM veiculos
        ORDER BY placa

    """).fetchall()

    return render_template(

        'processos.html',

        clientes=clientes,
        veiculos=veiculos

    )