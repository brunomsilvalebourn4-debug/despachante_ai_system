from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect

from modules.db import get_connection

veiculos = Blueprint(
    'veiculos',
    __name__
)

@veiculos.route('/veiculos', methods=['GET', 'POST'])
def pagina_veiculos():

    conn = get_connection()

    # ====================================
    # SALVAR VEÍCULO
    # ====================================

    if request.method == 'POST':

        cliente_id = request.form.get(
            'cliente_id'
        )

        placa = request.form.get(
            'placa'
        )

        renavam = request.form.get(
            'renavam'
        )

        marca_modelo = request.form.get(
            'marca_modelo'
        )

        ano_fabricacao = request.form.get(
            'ano_fabricacao'
        )

        ano_modelo = request.form.get(
            'ano_modelo'
        )

        tipo_servico = request.form.get(
            'tipo_servico'
        )

        status = request.form.get(
            'status'
        )

        data_entrada = request.form.get(
            'data_entrada'
        )

        numero_processo = request.form.get(
            'numero_processo'
        )

        observacoes = request.form.get(
            'observacoes'
        )

        vistoria = (
            'SIM'
            if request.form.get('vistoria')
            else 'NÃO'
        )

        recibo = (
            'SIM'
            if request.form.get('recibo')
            else 'NÃO'
        )

        cnh = (
            'SIM'
            if request.form.get('cnh')
            else 'NÃO'
        )

        comprovante = (
            'SIM'
            if request.form.get('comprovante')
            else 'NÃO'
        )

        honorarios = request.form.get(
            'honorarios'
        )

        taxa_detran = request.form.get(
            'taxa_detran'
        )

        conn.execute("""

            INSERT INTO veiculos (

                cliente_id,

                placa,
                renavam,
                marca_modelo,

                ano_fabricacao,
                ano_modelo,

                tipo_servico,
                status,

                data_entrada,
                numero_processo,

                observacoes,

                vistoria,
                recibo,
                cnh,
                comprovante,

                honorarios,
                taxa_detran

            )

            VALUES (

                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?, ?

            )

        """, (

            cliente_id,

            placa,
            renavam,
            marca_modelo,

            ano_fabricacao,
            ano_modelo,

            tipo_servico,
            status,

            data_entrada,
            numero_processo,

            observacoes,

            vistoria,
            recibo,
            cnh,
            comprovante,

            honorarios,
            taxa_detran

        ))

        conn.commit()

        return redirect('/veiculos')

    # ====================================
    # LISTAR CLIENTES
    # ====================================
    clientes = conn.execute("""

    SELECT

        id,
        nome,
        cpf,
        telefone,
        email,
        endereco,
        numero,
        bairro,
        cidade,
        estado,
        rg,
        data_nascimento,
        vencimento_cnh,
        org_exp,
        uf_exp,
        pgu_registro,
        nome_pai,
        nome_mae

    FROM clientes

    ORDER BY nome

""").fetchall()

    # ====================================
    # LISTAR VEÍCULOS
    # ====================================

    lista_veiculos = conn.execute("""

        SELECT

            veiculos.*,
            clientes.nome

        FROM veiculos

        LEFT JOIN clientes
        ON veiculos.cliente_id = clientes.id

        ORDER BY veiculos.id DESC

    """).fetchall()

    # ====================================
    # RENDER
    # ====================================

    return render_template(

        'veiculos.html',

        clientes=clientes,
        lista_veiculos=lista_veiculos

    )