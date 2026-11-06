import sqlite3

import pytest

from services.cliente_service import criar_cliente
from services.conta_service import criar_conta
from services.transacao_service import registrar_transacao


def _consulta(db, sql, params=()):
    conn = sqlite3.connect(db)
    try:
        return conn.execute(sql, params).fetchall()
    finally:
        conn.close()


# --- cliente -----------------------------------------------------------

def test_criar_cliente_persiste_e_retorna_id(db):
    cliente_id = criar_cliente("João", "12345678900")

    assert cliente_id == 1
    assert _consulta(db, "SELECT nome, cpf FROM clientes") == [("João", "12345678900")]


def test_criar_cliente_com_cpf_existente_retorna_mesmo_id_sem_duplicar(db):
    primeiro = criar_cliente("João", "12345678900")
    segundo = criar_cliente("Outro Nome", "12345678900")

    assert primeiro == segundo
    assert _consulta(db, "SELECT COUNT(*) FROM clientes") == [(1,)]


def test_clientes_com_cpfs_distintos_recebem_ids_distintos(db):
    assert criar_cliente("João", "111") != criar_cliente("Maria", "222")


# --- conta -------------------------------------------------------------

def test_criar_conta_inicia_com_saldo_zero(db):
    cliente_id = criar_cliente("Maria", "98765432100")

    conta_id = criar_conta(cliente_id)

    assert conta_id == 1
    assert _consulta(db, "SELECT cliente_id, saldo FROM contas WHERE id = ?", (conta_id,)) == [
        (cliente_id, 0.0)
    ]


def test_cliente_pode_ter_varias_contas(db):
    cliente_id = criar_cliente("Ana", "11122233344")

    assert criar_conta(cliente_id) != criar_conta(cliente_id)
    assert _consulta(db, "SELECT COUNT(*) FROM contas") == [(2,)]


# --- transação ---------------------------------------------------------

@pytest.fixture
def conta_id(db):
    return criar_conta(criar_cliente("João", "12345678900"))


def test_registrar_transacao_valida_e_persistida(db, conta_id):
    registrar_transacao(conta_id, "entrada", 1000)
    registrar_transacao(conta_id, "saida", 250.5)

    linhas = _consulta(db, "SELECT conta_id, tipo, valor FROM transacoes ORDER BY id")
    assert linhas == [(conta_id, "entrada", 1000.0), (conta_id, "saida", 250.5)]


def test_transacao_recebe_data_automatica(db, conta_id):
    registrar_transacao(conta_id, "entrada", 10)

    (data,), = _consulta(db, "SELECT data FROM transacoes")
    assert data is not None


@pytest.mark.parametrize("valor", [0, -1, -0.01])
def test_valor_nao_positivo_e_rejeitado(db, conta_id, valor):
    with pytest.raises(ValueError, match="positivo"):
        registrar_transacao(conta_id, "entrada", valor)

    assert _consulta(db, "SELECT COUNT(*) FROM transacoes") == [(0,)]


def test_tipo_invalido_e_rejeitado(db, conta_id):
    with pytest.raises(ValueError, match="Tipo inválido"):
        registrar_transacao(conta_id, "transferencia", 10)

    assert _consulta(db, "SELECT COUNT(*) FROM transacoes") == [(0,)]


def test_services_nao_tocam_o_banco_padrao(db, tmp_path, monkeypatch):
    """Garante que o isolamento funciona: nenhum banco.db é criado no cwd."""
    monkeypatch.chdir(tmp_path)

    criar_cliente("João", "999")

    assert not (tmp_path / "banco.db").exists()
