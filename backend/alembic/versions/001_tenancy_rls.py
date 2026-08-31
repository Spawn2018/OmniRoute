"""create organization and app_user with RLS

Revision ID: 001_tenancy_rls
Revises:
Create Date: 2026-08-31
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "001_tenancy_rls"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "organization",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("slug", sa.String(length=63), nullable=False),
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
        sa.UniqueConstraint("slug", name="uq_organization_slug"),
    )

    op.create_table(
        "app_user",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("display_name", sa.String(length=255), nullable=False),
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
            name="fk_app_user_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "email", name="uq_app_user_org_email"),
    )
    op.create_index("ix_app_user_organization_id", "app_user", ["organization_id"])

    op.execute("ALTER TABLE organization ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE organization FORCE ROW LEVEL SECURITY")
    op.execute(
        """
        CREATE POLICY organization_tenant_isolation ON organization
        USING (id = NULLIF(current_setting('app.current_org', true), '')::uuid)
        """
    )

    op.execute("ALTER TABLE app_user ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE app_user FORCE ROW LEVEL SECURITY")
    op.execute(
        """
        CREATE POLICY app_user_tenant_isolation ON app_user
        USING (organization_id = NULLIF(current_setting('app.current_org', true), '')::uuid)
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS app_user_tenant_isolation ON app_user")
    op.execute("DROP POLICY IF EXISTS organization_tenant_isolation ON organization")
    op.drop_index("ix_app_user_organization_id", table_name="app_user")
    op.drop_table("app_user")
    op.drop_table("organization")
