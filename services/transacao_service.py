import sqlite3

from database.connection import conectar
from datetime import datetime

def registrar_transacao(conta_id, tipo, valor):
    if valor <= 0:
        raise ValueError("Valor deve ser positivo")

    if tipo not in ["entrada", "saida"]:
        raise ValueError("Tipo inválido")

    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO transacoes (conta_id, tipo, valor)
        VALUES (?, ?, ?)
    """, (conta_id, tipo, valor))

    conn.commit()
    conn.close()