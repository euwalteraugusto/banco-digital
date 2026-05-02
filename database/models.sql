CREATE TABLE clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    cpf TEXT UNIQUE NOT NULL
);

CREATE TABLE contas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER,
    saldo REAL DEFAULT 0,
    FOREIGN KEY(cliente_id) REFERENCES clientes(id)
);

CREATE TABLE transacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conta_id INTEGER,
    valor REAL,
    tipo TEXT, -- entrada ou saida
    data TEXT,
    FOREIGN KEY(conta_id) REFERENCES contas(id)
);