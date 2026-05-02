import sqlite3

DB_PATH = "banco.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Clientes
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        cpf TEXT NOT NULL UNIQUE
    )
    """)

    # Contas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER NOT NULL,
        saldo REAL DEFAULT 0,
        FOREIGN KEY (cliente_id) REFERENCES clientes(id)
    )
    """)

    # Transações (já antecipando evolução do projeto)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        conta_id INTEGER NOT NULL,
        tipo TEXT NOT NULL, -- deposito / saque
        valor REAL NOT NULL,
        data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (conta_id) REFERENCES contas(id)
    )
    """)

    conn.commit()
    conn.close()
    
def seed_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # evita duplicação
    cursor.execute("SELECT COUNT(*) FROM clientes")
    if cursor.fetchone()[0] > 0:
        print("Dados já existem. Seed ignorado.")
        conn.close()
        return

    # --- CLIENTES ---
    clientes = [
        ("João", "12345678900"),
        ("Maria", "98765432100"),
        ("Ana", "11122233344")
    ]

    cursor.executemany(
        "INSERT INTO clientes (nome, cpf) VALUES (?, ?)",
        clientes
    )

    # --- CONTAS ---
    cursor.execute("SELECT id FROM clientes")
    clientes_ids = cursor.fetchall()

    contas = [(cid[0],) for cid in clientes_ids]

    cursor.executemany(
        "INSERT INTO contas (cliente_id) VALUES (?)",
        contas
    )

    # --- TRANSAÇÕES (DADOS REALISTAS) ---
    transacoes = [
        # Conta 1 (João) - comportamento normal
        (1, "entrada", 2000, "2026-04-01"),
        (1, "saida", 150, "2026-04-02"),
        (1, "saida", 200, "2026-04-05"),
        (1, "saida", 300, "2026-04-10"),
        (1, "saida", 180, "2026-05-02"),
        (1, "saida", 220, "2026-05-05"),

        # Anomalia (João)
        (1, "saida", 3000, "2026-05-10"),

        # Conta 2 (Maria) - padrão diferente
        (2, "entrada", 5000, "2026-04-01"),
        (2, "saida", 1000, "2026-04-03"),
        (2, "saida", 1200, "2026-04-07"),
        (2, "saida", 900, "2026-05-01"),

        # Conta 3 (Ana) - baixo volume
        (3, "entrada", 1000, "2026-04-01"),
        (3, "saida", 50, "2026-04-02"),
        (3, "saida", 70, "2026-05-01"),
    ]

    cursor.executemany("""
        INSERT INTO transacoes (conta_id, tipo, valor, data)
        VALUES (?, ?, ?, ?)
    """, transacoes)

    conn.commit()
    conn.close()

    print("Seed completo inserido.")