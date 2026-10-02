"""Additive binding of an explicit OIDC linking transaction to its session owner.

v1 readers/writers remain compatible; no tables, states or backfill are added.
The exclusive migration controller bounds lock/duration. Existing invalid rows
fail constraint validation atomically; no cutover occurs on failure. Alembic's
transactional revision is the resume checkpoint. Completion requires the validated
composite FK. There is no data rewrite or irreversible phase; downgrade retains
all accounts, credentials, bootstrap and audit, so no BackupSet is needed for
this revision. The initial v1 populated-downgrade/restore guard still applies.
"""

from alembic import op

revision = "identity_link_binding_v2"
down_revision = "local_identity_v1"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""ALTER TABLE identity.sessions
      ADD CONSTRAINT sessions_id_account_key UNIQUE (id, account_id)""")
    op.execute("""ALTER TABLE identity.oidc_transactions
      ADD CONSTRAINT oidc_transaction_session_owner_fk
      FOREIGN KEY (session_id, account_id) REFERENCES identity.sessions(id, account_id)""")


def downgrade() -> None:
    op.execute("""ALTER TABLE identity.oidc_transactions
      DROP CONSTRAINT oidc_transaction_session_owner_fk""")
    op.execute("ALTER TABLE identity.sessions DROP CONSTRAINT sessions_id_account_key")
