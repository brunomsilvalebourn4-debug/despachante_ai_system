import sqlite3
from config import Config

# =========================================
# CONEXÃO
# =========================================

def get_connection():
    conn = sqlite3.connect(Config.DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


# =========================================
# CRIAR TABELAS
# =========================================

def criar_tabelas():

    conn = get_connection()
    cursor = conn.cursor()

    # =========================================
    # CLIENTES
    # =========================================

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS clientes (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        nome TEXT,
        cpf TEXT,
        rg TEXT,
        telefone TEXT,
        email TEXT,

        data_nascimento TEXT,
        vencimento_cnh TEXT,
        org_exp TEXT,
        uf_exp TEXT,
        pgu_registro TEXT,
        nome_pai TEXT,
        nome_mae TEXT

    )

    """)

    # =========================================
    # ADICIONAR COLUNAS AUTOMATICAMENTE
    # =========================================

    colunas = [

    "data_nascimento",
    "vencimento_cnh",
    "org_exp",
    "uf_exp",
    "pgu_registro",
    "nome_pai",
    "nome_mae",

    "endereco",
    "numero",
    "bairro",
    "cidade",
    "estado",
    "cep"

]

    for coluna in colunas:

        try:

            cursor.execute(
                f"ALTER TABLE clientes ADD COLUMN {coluna} TEXT"
            )

        except:
            pass

    # =========================================
    # VEÍCULOS
    # =========================================

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS veiculos (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        cliente_id INTEGER,

        placa TEXT,
        renavam TEXT,

        marca_modelo TEXT,

        ano_fabricacao TEXT,
        ano_modelo TEXT,

        tipo_servico TEXT,
        status TEXT,

        data_entrada TEXT,
        numero_processo TEXT,

        observacoes TEXT,

        vistoria TEXT,
        recibo TEXT,
        cnh TEXT,
        comprovante TEXT,

        honorarios TEXT,
        taxa_detran TEXT

    )

    """)

    # =========================================
    # PROCESSOS
    # =========================================

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS processos (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        cliente_id INTEGER,
        veiculo_id INTEGER,

        tipo_servico TEXT,
        status TEXT DEFAULT 'PENDENTE',

        valor_venda TEXT,
        procuracao TEXT,
        nota_fiscal TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(cliente_id) REFERENCES clientes(id),
        FOREIGN KEY(veiculo_id) REFERENCES veiculos(id)

    )

    """)

    # =========================================
    # DOCUMENTOS
    # =========================================

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS documentos (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        processo_id INTEGER,

        nome_arquivo TEXT,
        caminho TEXT,
        tipo TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(processo_id) REFERENCES processos(id)

    )

    """)

    conn.commit()
    conn.close()