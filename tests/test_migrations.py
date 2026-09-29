from alembic import command
from alembic.autogenerate import compare_metadata
from alembic.config import Config
from alembic.migration import MigrationContext
from sqlalchemy import create_engine

from app.core.database import Base


def test_migrations_sobem_descem_e_batem_com_os_models(tmp_path, monkeypatch):
    """Garante que as migrations aplicam, revertem e geram o mesmo schema dos models."""
    url = f"sqlite:///{tmp_path / 'migrations.db'}"
    monkeypatch.setenv("DATABASE_URL", url)  # lido pelo alembic/env.py
    config = Config("alembic.ini")

    command.upgrade(config, "head")
    command.downgrade(config, "base")
    command.upgrade(config, "head")

    engine = create_engine(url)
    with engine.connect() as connection:
        diff = compare_metadata(MigrationContext.configure(connection), Base.metadata)
    engine.dispose()

    assert diff == [], f"Models e migrations estão diferentes; gere uma nova migration: {diff}"
