import sqlite3

from services.cliente_service import criar_cliente
from services.conta_service import criar_conta
from services.transacao_service import registrar_transacao
from analysis.analise_financeira import analisar_gastos, listar_contas
from database.init_db import init_db, seed_data

init_db()
seed_data()

# fluxo básico

cliente_id = criar_cliente("João", "12345678900")
conta_id = criar_conta(cliente_id)

registrar_transacao(conta_id, "entrada", 1000)
registrar_transacao(conta_id, "saida", 200)
registrar_transacao(conta_id, "saida", 500)

def listar_contas():
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM contas")
    contas = [row[0] for row in cursor.fetchall()]

    conn.close()
    return contas


contas = listar_contas()

for conta in contas:
    print(f"\nConta {conta}")

    resumo, alertas = analisar_gastos(conta)

    print("Resumo mensal:")
    print(resumo)

    print("Possíveis gastos suspeitos:")
    print(alertas)