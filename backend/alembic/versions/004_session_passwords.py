"""add password_hash and refresh_token with RLS

Revision ID: 004_session_passwords
Revises: 003_extraction_draft_rls
Create Date: 2026-08-31
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "004_session_passwords"
down_revision: str | None = "003_extraction_draft_rls"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("app_user", sa.Column("password_hash", sa.String(length=255), nullable=True))
    op.execute(
        """
        CREATE POLICY app_user_login_email ON app_user
        FOR SELECT
        USING (email = NULLIF(current_setting('app.login_email', true), ''))
        """
    )

    op.create_table(
        "refresh_token",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("token_hash", sa.String(length=64), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organization.id"],
            name="fk_refresh_token_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["app_user.id"],
            name="fk_refresh_token_user_id",
            ondelete="CASCADE",
        ),
        sa.UniqueConstraint("token_hash", name="uq_refresh_token_token_hash"),
    )
    op.create_index("ix_refresh_token_organization_id", "refresh_token", ["organization_id"])

    op.execute("ALTER TABLE refresh_token ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE refresh_token FORCE ROW LEVEL SECURITY")
    op.execute(
        """
        CREATE POLICY refresh_token_tenant_isolation ON refresh_token
        USING (organization_id = NULLIF(current_setting('app.current_org', true), '')::uuid)
        """
    )
    op.execute(
        """
        CREATE POLICY refresh_token_by_hash ON refresh_token
        FOR SELECT
        USING (token_hash = NULLIF(current_setting('app.refresh_hash', true), ''))
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS refresh_token_by_hash ON refresh_token")
    op.execute("DROP POLICY IF EXISTS refresh_token_tenant_isolation ON refresh_token")
    op.drop_index("ix_refresh_token_organization_id", table_name="refresh_token")
    op.drop_table("refresh_token")
    op.execute("DROP POLICY IF EXISTS app_user_login_email ON app_user")
    op.drop_column("app_user", "password_hash")
