CREATE SCHEMA IF NOT EXISTS identity;
CREATE TABLE identity.accounts (
 id uuid PRIMARY KEY, username text NOT NULL UNIQUE CHECK (length(username)>0),
 password_hash text NOT NULL CHECK (password_hash LIKE '$argon2id$v=19$%'),
 recovery_hash text NOT NULL CHECK (recovery_hash ~ '^[0-9a-f]{64}$'),
 state text NOT NULL CHECK (state IN ('active','inactive','locked')),
 revision bigint NOT NULL CHECK (revision>0), administrator boolean NOT NULL
);
CREATE UNIQUE INDEX one_first_administrator ON identity.accounts ((administrator)) WHERE administrator;
CREATE TABLE identity.bootstrap (
 singleton boolean PRIMARY KEY DEFAULT true CHECK(singleton),
 state text NOT NULL CHECK(state IN ('available','completed')),
 administrator_id uuid REFERENCES identity.accounts(id) ON DELETE RESTRICT,
 revision bigint NOT NULL CHECK(revision>0),
 CHECK ((state='available' AND administrator_id IS NULL) OR
        (state='completed' AND administrator_id IS NOT NULL))
);
INSERT INTO identity.bootstrap VALUES (true,'available',NULL,1);
CREATE TABLE identity.memberships (
 project_id uuid NOT NULL, account_id uuid NOT NULL REFERENCES identity.accounts(id),
 role text NOT NULL CHECK(role IN ('owner','editor','reviewer','viewer')),
 revision bigint NOT NULL CHECK(revision>0), PRIMARY KEY(project_id,account_id)
);
CREATE TABLE identity.oidc_links (
 id uuid PRIMARY KEY, account_id uuid NOT NULL REFERENCES identity.accounts(id),
 issuer text NOT NULL CHECK(issuer LIKE 'https://%'), subject text NOT NULL CHECK(length(subject)>0),
 state text NOT NULL CHECK(state IN ('linked','revoked')), revision bigint NOT NULL CHECK(revision>0),
 UNIQUE(issuer,subject), UNIQUE(id,account_id)
);
CREATE TABLE identity.sessions (
 id uuid PRIMARY KEY, account_id uuid NOT NULL REFERENCES identity.accounts(id),
 secret_hash text NOT NULL UNIQUE CHECK(secret_hash ~ '^[0-9a-f]{64}$'),
 csrf_hash text NOT NULL CHECK(csrf_hash ~ '^[0-9a-f]{64}$'),
 expires_at timestamptz NOT NULL, idle_expires_at timestamptz NOT NULL,
 state text NOT NULL CHECK(state IN ('active','revoked','expired','rotated')),
 revision bigint NOT NULL CHECK(revision>0), oidc_link_id uuid,
 CHECK(idle_expires_at<=expires_at),
 FOREIGN KEY(oidc_link_id,account_id) REFERENCES identity.oidc_links(id,account_id)
);
CREATE INDEX sessions_by_account ON identity.sessions(account_id);
CREATE TABLE identity.tokens (
 id uuid PRIMARY KEY, account_id uuid NOT NULL REFERENCES identity.accounts(id),
 secret_hash text NOT NULL UNIQUE CHECK(secret_hash ~ '^[0-9a-f]{64}$'),
 scopes text[] NOT NULL CHECK(cardinality(scopes)>0 AND array_position(scopes,NULL) IS NULL),
 expires_at timestamptz NOT NULL, project_id uuid,
 state text NOT NULL CHECK(state IN ('active','revoked','expired')),
 revision bigint NOT NULL CHECK(revision>0),
 FOREIGN KEY(project_id,account_id) REFERENCES identity.memberships(project_id,account_id)
);
CREATE INDEX tokens_by_account ON identity.tokens(account_id);
CREATE TABLE identity.requests (
 key_hash text NOT NULL CHECK(key_hash ~ '^[0-9a-f]{64}$'), operation text NOT NULL,
 principal_id uuid REFERENCES identity.accounts(id),
 payload_hash text NOT NULL CHECK(payload_hash ~ '^[0-9a-f]{64}$'), outcome_id uuid,
 UNIQUE NULLS NOT DISTINCT (key_hash,operation,principal_id)
);
CREATE TABLE identity.oidc_transactions (
 id uuid PRIMARY KEY, state_hash text NOT NULL UNIQUE CHECK(state_hash ~ '^[0-9a-f]{64}$'),
 nonce_hash text NOT NULL CHECK(nonce_hash ~ '^[0-9a-f]{64}$'),
 browser_hash text NOT NULL CHECK(browser_hash ~ '^[0-9a-f]{64}$'),
 account_id uuid REFERENCES identity.accounts(id), session_id uuid REFERENCES identity.sessions(id),
 expires_at timestamptz NOT NULL, state text NOT NULL CHECK(state IN ('pending','consumed','failed')),
 CHECK((account_id IS NULL)=(session_id IS NULL))
);
CREATE TABLE identity.ceremonies (
 id uuid PRIMARY KEY, account_id uuid NOT NULL REFERENCES identity.accounts(id),
 kit_hash text NOT NULL UNIQUE CHECK(kit_hash ~ '^[0-9a-f]{64}$')
);
-- BC-002 durable observations; these are private, not BC-014 ledger tables.
CREATE TABLE identity.observations (
 id uuid PRIMARY KEY, actor_id uuid, action text NOT NULL, target_id uuid,
 outcome text NOT NULL CHECK(outcome IN ('COMMITTED','DENIED')),
 policy_version text NOT NULL CHECK(length(policy_version)>0), correlation_id uuid NOT NULL,
 observed_at timestamptz NOT NULL, reason_code text,
 CHECK((outcome='COMMITTED' AND reason_code IS NULL) OR outcome='DENIED')
);
CREATE FUNCTION identity.protect_bootstrap() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
 IF TG_OP='DELETE' OR OLD.state='completed' OR NEW.revision<>OLD.revision+1 THEN
  RAISE EXCEPTION 'bootstrap is irreversible' USING ERRCODE='23514';
 END IF;
 RETURN NEW;
END $$;
CREATE TRIGGER protect_bootstrap BEFORE UPDATE OR DELETE ON identity.bootstrap
FOR EACH ROW EXECUTE FUNCTION identity.protect_bootstrap();
CREATE FUNCTION identity.protect_credential() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
 IF (to_jsonb(NEW)-'state'-'revision'-'idle_expires_at')<>
    (to_jsonb(OLD)-'state'-'revision'-'idle_expires_at') THEN
  RAISE EXCEPTION 'credential identity and expiry are immutable' USING ERRCODE='23514';
 END IF;
 IF NEW.state<>OLD.state AND (OLD.state<>'active' OR NEW.revision<>OLD.revision+1) THEN
  RAISE EXCEPTION 'credential terminal or stale transition' USING ERRCODE='23514';
 END IF;
 RETURN NEW;
END $$;
CREATE FUNCTION identity.protect_link() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
 IF OLD.state<>'linked' OR NEW.state<>'revoked' OR NEW.revision<>OLD.revision+1 OR
    (to_jsonb(NEW)-'state'-'revision')<>(to_jsonb(OLD)-'state'-'revision') THEN
  RAISE EXCEPTION 'link identity is immutable and revocation terminal' USING ERRCODE='23514';
 END IF;
 RETURN NEW;
END $$;
CREATE TRIGGER protect_link BEFORE UPDATE ON identity.oidc_links
FOR EACH ROW EXECUTE FUNCTION identity.protect_link();
CREATE TRIGGER protect_session BEFORE UPDATE ON identity.sessions
FOR EACH ROW EXECUTE FUNCTION identity.protect_credential();
CREATE TRIGGER protect_token BEFORE UPDATE ON identity.tokens
FOR EACH ROW EXECUTE FUNCTION identity.protect_credential();
CREATE FUNCTION identity.protect_callback() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
 IF OLD.state<>'pending' OR NEW.state NOT IN ('consumed','failed')
    OR (to_jsonb(NEW)-'state')<>(to_jsonb(OLD)-'state') THEN
  RAISE EXCEPTION 'callback is single-use' USING ERRCODE='23514';
 END IF;
 RETURN NEW;
END $$;
CREATE TRIGGER protect_callback BEFORE UPDATE ON identity.oidc_transactions
FOR EACH ROW EXECUTE FUNCTION identity.protect_callback();
CREATE FUNCTION identity.append_only() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
 RAISE EXCEPTION 'append-only observation' USING ERRCODE='23514';
END $$;
CREATE TRIGGER observations_append_only BEFORE UPDATE OR DELETE ON identity.observations
FOR EACH ROW EXECUTE FUNCTION identity.append_only();
CREATE TRIGGER ceremonies_append_only BEFORE UPDATE OR DELETE ON identity.ceremonies
FOR EACH ROW EXECUTE FUNCTION identity.append_only();
REVOKE ALL ON ALL TABLES IN SCHEMA identity FROM PUBLIC;
REVOKE ALL ON ALL FUNCTIONS IN SCHEMA identity FROM PUBLIC;
