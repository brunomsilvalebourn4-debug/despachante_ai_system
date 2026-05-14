import sqlite3
import re
import random

from config import Config

memoria = {}

saudacoes = [

    "Olá 😊 Como posso ajudar você hoje?",
    "Oi 😊 Bem-vindo ao Nivaldo Despachante.",
    "Olá 😊 Em que posso ajudar?",
    "Tudo bem? 😊 Como posso ajudar no seu processo?"

]

respostas_consulta = [

    "Consultei aqui 😊",
    "Verifiquei no sistema 😊",
    "Localizei seu processo 😊",
    "Acabei de consultar 😊"

]

def chamar_ia(pergunta, telefone='admin'):

    pergunta_lower = pergunta.lower()

    conn = sqlite3.connect(
        Config.DB_NAME
    )

    conn.row_factory = sqlite3.Row

    if telefone not in memoria:

        memoria[telefone] = {

            'placa': None

        }

    contexto = memoria[telefone]

    palavras_saudacao = [

        'oi',
        'olá',
        'ola',
        'bom dia',
        'boa tarde',
        'boa noite'

    ]

    if any(p in pergunta_lower for p in palavras_saudacao):

        return random.choice(
            saudacoes
        )

    regex_placa = r'[A-Z]{3}[0-9][A-Z0-9][0-9]{2}'

    placas = re.findall(

        regex_placa,

        pergunta.upper()

    )

    processo = None

    # CONSULTA PLACA
    if placas:

        placa = placas[0]

        processo = conn.execute("""

            SELECT

                processos.status,
                processos.tipo_servico,
                processos.motivo_pendencia,

                clientes.nome,

                veiculos.placa

            FROM processos

            LEFT JOIN clientes
            ON processos.cliente_id = clientes.id

            LEFT JOIN veiculos
            ON processos.veiculo_id = veiculos.id

            WHERE veiculos.placa = ?

        """, (placa,)).fetchone()

        if processo:

            contexto['placa'] = placa

            return f"""

{random.choice(respostas_consulta)}

Cliente:
{processo['nome']}

Placa:
{processo['placa']}

Serviço:
{processo['tipo_servico']}

Status:
{processo['status']}

Motivo:
{processo['motivo_pendencia']}
"""

    # USA CONTEXTO
    if contexto['placa']:

        processo = conn.execute("""

            SELECT

                processos.status,
                processos.tipo_servico,
                processos.motivo_pendencia,

                clientes.nome,

                veiculos.placa

            FROM processos

            LEFT JOIN clientes
            ON processos.cliente_id = clientes.id

            LEFT JOIN veiculos
            ON processos.veiculo_id = veiculos.id

            WHERE veiculos.placa = ?

        """, (contexto['placa'],)).fetchone()

    palavras_status = [

        'status',
        'pendente',
        'pronto',
        'demora',
        'andamento',
        'situação',
        'situacao',
        'como está',
        'como esta',
        'já saiu',
        'ja saiu',
        'atualização'

    ]

    if processo and any(p in pergunta_lower for p in palavras_status):

        return f"""

{random.choice(respostas_consulta)}

O processo da placa
{processo['placa']}

está atualmente:

👉 {processo['status']}

Motivo:
{processo['motivo_pendencia']}

Serviço:
{processo['tipo_servico']}
"""

    return """

Entendi 😊

Pode me explicar melhor sua dúvida?
"""