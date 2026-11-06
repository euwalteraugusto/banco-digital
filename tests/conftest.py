import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from database import connection  # noqa: E402
from database.init_db import init_db  # noqa: E402


@pytest.fixture
def db(tmp_path, monkeypatch):
    """Banco SQLite temporário (isolado por teste) com o schema criado."""
    caminho = tmp_path / "teste.db"
    monkeypatch.setattr(connection, "DB_PATH", str(caminho))
    init_db()
    return caminho
