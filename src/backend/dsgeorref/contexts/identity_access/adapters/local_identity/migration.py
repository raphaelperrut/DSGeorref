"""Alembic entry for the exclusive controller; bounded locks and transactional DDL."""

from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, text


def migrate(dsn: str, direction: str) -> None:
    if direction not in {"upgrade", "downgrade"}:
        raise ValueError("unknown migration direction")
    engine = create_engine(dsn)
    try:
        with engine.begin() as connection:
            connection.execute(text("SET LOCAL lock_timeout = '5s'"))
            connection.execute(text("SET LOCAL statement_timeout = '30s'"))
            connection.execute(
                text("SELECT pg_advisory_xact_lock(hashtext('identity:migrations'))")
            )
            connection.execute(text("CREATE SCHEMA IF NOT EXISTS identity"))
            config = Config()
            config.set_main_option("script_location", str(Path(__file__).parent / "migrations"))
            config.attributes["connection"] = connection
            if direction == "upgrade":
                command.upgrade(config, "head")
            else:
                command.downgrade(config, "base")
    finally:
        engine.dispose()
