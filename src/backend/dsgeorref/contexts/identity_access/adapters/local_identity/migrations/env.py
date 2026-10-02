"""Injected connection and exclusive transaction owned by the migration caller."""

from alembic import context

connection = context.config.attributes["connection"]
context.configure(connection=connection, version_table_schema="identity")
with context.begin_transaction():
    context.run_migrations()
