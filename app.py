import streamlit as st
import pandas as pd
import sqlite3

from analysis.analise_financeira import analisar_gastos

# -------------------------
# CONFIG
# -------------------------
st.set_page_config(page_title="Banco Digital", layout="wide")

st.title("📊 Banco Digital - Dashboard Financeiro")

# -------------------------
# CONEXÃO
# -------------------------
conn = sqlite3.connect("banco.db")

contas = pd.read_sql_query("SELECT id FROM contas", conn)
conta_id = st.selectbox("Selecione a conta", contas["id"])

# -------------------------
# EXECUÇÃO
# -------------------------
if st.button("Gerar análise"):

    resumo, alertas = analisar_gastos(conta_id)

    df = pd.read_sql_query(
        "SELECT * FROM transacoes WHERE conta_id = ?",
        conn,
        params=(conta_id,)
    )

    df["data"] = pd.to_datetime(df["data"])
    df["mes"] = df["data"].dt.month

    # -------------------------
    # KPIs
    # -------------------------
    entradas = df[df["tipo"] == "entrada"]["valor"].sum()
    saidas = df[df["tipo"] == "saida"]["valor"].sum()
    saldo = entradas - saidas
    total_transacoes = len(df)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Entradas", f"R$ {entradas:.2f}")
    col2.metric("Saídas", f"R$ {saidas:.2f}")
    col3.metric("Saldo", f"R$ {saldo:.2f}")
    col4.metric("Transações", total_transacoes)

    st.divider()

    # -------------------------
    # GRÁFICO 1: FLUXO MENSAL
    # -------------------------
    fluxo = df.copy()
    fluxo["valor_ajustado"] = fluxo.apply(
        lambda x: x["valor"] if x["tipo"] == "entrada" else -x["valor"],
        axis=1
    )

    fluxo_mensal = fluxo.groupby("mes")["valor_ajustado"].sum()

    st.subheader("📈 Fluxo de Caixa Mensal")
    st.bar_chart(fluxo_mensal)

    # -------------------------
    # GRÁFICO 2: ENTRADAS vs SAÍDAS
    # -------------------------
    resumo_tipo = df.groupby("tipo")["valor"].sum()

    st.subheader("💰 Entradas vs Saídas")
    st.bar_chart(resumo_tipo)

    # -------------------------
    # ALERTAS
    # -------------------------
    st.subheader("⚠️ Gastos suspeitos")
    st.dataframe(alertas)

    # -------------------------
    # TABELA COMPLETA
    # -------------------------
    st.subheader("📄 Transações")
    st.dataframe(df.sort_values("data", ascending=False))

conn.close()