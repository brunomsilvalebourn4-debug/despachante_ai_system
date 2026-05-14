import os
import sqlite3
from config import Config

# =========================================
# CAMINHO DO BANCO
# =========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, Config.DB_NAME)

# =========================================
# CONEXÃO
# =========================================

def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row

    # 🔥 IMPORTANTE PARA RENDER / PRODUÇÃO
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")

    return conn


# =========================================
# CRIAR TABELAS
# =========================================

def criar_tabelas():

    conn = get_connection()
    cursor = conn.cursor()

    # =========================================
    # USERS
    # =========================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        email TEXT UNIQUE,
        senha_hash TEXT
    )
    """)

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

    # ALTERAÇÕES SEGURAS (SEM CRASH)
    colunas = [
        "endereco",
        "numero",
        "bairro",
        "cidade",
        "estado",
        "cep"
    ]

    for coluna in colunas:
        try:
            cursor.execute(f"ALTER TABLE clientes ADD COLUMN {coluna} TEXT")
        except sqlite3.OperationalError:
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
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()