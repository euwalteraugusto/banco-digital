import os
import sqlite3

# Caminho do banco configurável por variável de ambiente (usado nos testes).
DB_PATH = os.environ.get("BANCO_DB", "banco.db")


def conectar():
    return sqlite3.connect(DB_PATH)
