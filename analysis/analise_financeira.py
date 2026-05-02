import sqlite3

import pandas as pd
from database.connection import conectar

def analisar_gastos(conta_id):
    conn = sqlite3.connect("banco.db")

    df = pd.read_sql_query(
        "SELECT * FROM transacoes WHERE conta_id = ?",
        conn,
        params=(conta_id,)
    )

    conn.close()

    # 1. Converter data
    df["data"] = pd.to_datetime(df["data"])

    # 2. Criar mês
    df["mes"] = df["data"].dt.month

    # 3. Adicionar valor ajustado
    df = adicionar_valor_ajustado(df)

    resumo = df.groupby("mes")["valor_ajustado"].sum()

    suspeitos = detectar_gastos_suspeitos(df)

    return resumo, suspeitos

def adicionar_valor_ajustado(df):
    df["valor_ajustado"] = df.apply(
        lambda row: row["valor"] if row["tipo"] == "entrada" else -row["valor"],
        axis=1
    )
    return df

def calcular_resumo_mensal(df):
    resumo = df.groupby("mes")["valor_ajustado"].sum()
    return resumo

def calcular_fluxo_caixa(df):
    entradas = df[df["tipo"] == "entrada"].groupby("mes")["valor"].sum()
    saidas = df[df["tipo"] == "saida"].groupby("mes")["valor"].sum()

    resumo = pd.DataFrame({
        "entradas": entradas,
        "saidas": saidas
    }).fillna(0)

    resumo["saldo"] = resumo["entradas"] - resumo["saidas"]

    return resumo

def listar_contas():
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM contas")
    contas = [row[0] for row in cursor.fetchall()]

    conn.close()
    return contas

def detectar_gastos_suspeitos(df):
    media_saidas = df[df["tipo"] == "saida"]["valor"].mean()

    suspeitos = df[
        (df["tipo"] == "saida") &
        (df["valor"] > media_saidas * 3)
    ]

    return suspeitos