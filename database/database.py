# conexão com o banco de dados

import sqlite3
import os

# caminho absoluto do banco (CORREÇÃO PRINCIPAL)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "gestao.db")

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def criar_tabelas():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS consertos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT NOT NULL,
        tecnico TEXT NOT NULL,
        cliente TEXT NOT NULL,
        servico_feito TEXT NOT NULL,
        observacoes TEXT,
        modelo TEXT,
        garantia TEXT,
        valor_cobrado REAL NOT NULL,
        lucro REAL
    );
    """)

    conn.commit()
    conn.close()
