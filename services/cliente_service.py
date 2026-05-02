import sqlite3

def criar_cliente(nome, cpf):
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()

    # 1. Verifica se já existe
    cursor.execute(
        "SELECT id FROM clientes WHERE cpf = ?",
        (cpf,)
    )
    resultado = cursor.fetchone()

    if resultado:
        conn.close()
        return resultado[0]  # retorna ID existente

    # 2. Se não existe, cria
    cursor.execute(
        "INSERT INTO clientes (nome, cpf) VALUES (?, ?)",
        (nome, cpf)
    )

    conn.commit()
    cliente_id = cursor.lastrowid

    conn.close()

    return cliente_id