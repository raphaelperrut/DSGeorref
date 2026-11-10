"""Persist BC-002 throttle state and its append-only decisions."""

from alembic import op

revision = "identity_login_throttle_v3"
down_revision = "identity_link_binding_v2"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""CREATE TABLE identity.throttle_buckets (
      operation text NOT NULL, bucket_digest text NOT NULL CHECK (bucket_digest ~ '^[0-9a-f]{64}$'),
      policy_version text NOT NULL, revision bigint NOT NULL CHECK (revision >= 1),
      failure_count bigint NOT NULL CHECK (failure_count >= 0),
      attempt_count bigint NOT NULL CHECK (attempt_count >= 0),
      window_started_at timestamptz NOT NULL, window_ends_at timestamptz NOT NULL,
      blocked_until timestamptz, state text NOT NULL CHECK (state IN ('open','limited','locked')),
      CHECK (window_ends_at > window_started_at),
      CHECK ((state = 'open') = (blocked_until IS NULL)),
      PRIMARY KEY (operation, bucket_digest)
    )""")
    op.execute("""CREATE TABLE identity.throttle_decisions (
      id uuid PRIMARY KEY, operation text NOT NULL, bucket_digest text NOT NULL,
      observed_at timestamptz NOT NULL, policy_version text NOT NULL, reason text NOT NULL,
      allowed boolean NOT NULL, before_state jsonb NOT NULL, after_state jsonb NOT NULL
    )""")
    op.execute("""CREATE TRIGGER throttle_decisions_append_only
      BEFORE UPDATE OR DELETE ON identity.throttle_decisions
      FOR EACH ROW EXECUTE FUNCTION identity.append_only()""")
    op.execute("REVOKE ALL ON identity.throttle_buckets, identity.throttle_decisions FROM PUBLIC")


def downgrade() -> None:
    op.execute(
        "LOCK TABLE identity.throttle_buckets, identity.throttle_decisions IN ACCESS EXCLUSIVE MODE"
    )
    op.execute("""DO $$ BEGIN
      IF EXISTS (SELECT FROM identity.throttle_buckets)
        OR EXISTS (SELECT FROM identity.throttle_decisions) THEN
        RAISE EXCEPTION 'populated throttle state requires preservation' USING ERRCODE='23514';
      END IF;
    END $$""")
    op.execute("DROP TABLE identity.throttle_decisions, identity.throttle_buckets")
