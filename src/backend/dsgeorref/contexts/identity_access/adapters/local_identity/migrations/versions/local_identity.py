"""Initial additive BC-002 identity schema. No adjacent runtime reader exists yet."""

from pathlib import Path

from alembic import op

revision = "local_identity_v1"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    source = Path(__file__).resolve().parents[1] / "schema.sql"
    op.execute(source.read_text(encoding="utf-8"))


def downgrade() -> None:
    # Never silently erase an initialized installation or reopen its bootstrap.
    op.execute("""DO $$ BEGIN
      IF EXISTS(SELECT 1 FROM identity.accounts) THEN
        RAISE EXCEPTION 'nonempty identity requires coordinated restore';
      END IF;
    END $$""")
    for table in (
        "observations",
        "ceremonies",
        "oidc_transactions",
        "requests",
        "tokens",
        "sessions",
        "oidc_links",
        "memberships",
        "bootstrap",
        "accounts",
    ):
        op.execute(f"DROP TABLE identity.{table}")
    for function in (
        "append_only",
        "protect_callback",
        "protect_credential",
        "protect_bootstrap",
        "protect_link",
    ):
        op.execute(f"DROP FUNCTION identity.{function}()")
