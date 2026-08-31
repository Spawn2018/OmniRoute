"""runtime role omniroute_app NOBYPASSRLS

Revision ID: 005_omniroute_app_rls
Revises: 004_session_passwords
Create Date: 2026-09-01
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "005_omniroute_app_rls"
down_revision: str | None = "004_session_passwords"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

# Hasło hello local/CI — prod: GitHub Encrypted Secrets, nie ten literał.
_CREATE_APP_ROLE = """
DO $$ BEGIN
  CREATE ROLE omniroute_app LOGIN PASSWORD 'omniroute'
    NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT NOBYPASSRLS;
EXCEPTION WHEN duplicate_object THEN
  ALTER ROLE omniroute_app WITH NOSUPERUSER NOCREATEDB
    NOCREATEROLE NOINHERIT NOBYPASSRLS LOGIN;
END $$;
"""


def upgrade() -> None:
    op.execute(_CREATE_APP_ROLE)
    bind = op.get_bind()
    db_name = bind.url.database
    if db_name:
        op.execute(sa.text(f'GRANT CONNECT ON DATABASE "{db_name}" TO omniroute_app'))
    op.execute("GRANT USAGE ON SCHEMA public TO omniroute_app")
    op.execute(
        "GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO omniroute_app"
    )
    op.execute("GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO omniroute_app")
    op.execute(
        "ALTER DEFAULT PRIVILEGES IN SCHEMA public "
        "GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO omniroute_app"
    )


def downgrade() -> None:
    op.execute(
        "ALTER DEFAULT PRIVILEGES IN SCHEMA public "
        "REVOKE SELECT, INSERT, UPDATE, DELETE ON TABLES FROM omniroute_app"
    )
    op.execute("REVOKE ALL ON ALL TABLES IN SCHEMA public FROM omniroute_app")
    op.execute("REVOKE ALL ON ALL SEQUENCES IN SCHEMA public FROM omniroute_app")
    op.execute("REVOKE USAGE ON SCHEMA public FROM omniroute_app")
    bind = op.get_bind()
    db_name = bind.url.database
    if db_name:
        op.execute(sa.text(f'REVOKE CONNECT ON DATABASE "{db_name}" FROM omniroute_app'))
    op.execute("DROP ROLE IF EXISTS omniroute_app")
