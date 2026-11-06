from database.connection import conectar

def criar_conta(cliente_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO contas (cliente_id) VALUES (?)",
        (cliente_id,)
    )

    conn.commit()

    conta_id = cursor.lastrowid  # <-- ESSENCIAL

    conn.close()

    return conta_id