"""create table_view with RLS

Revision ID: 002_table_view_rls
Revises: 001_tenancy_rls
Create Date: 2026-08-31
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "002_table_view_rls"
down_revision: str | None = "001_tenancy_rls"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "table_view",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("table_key", sa.String(length=128), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column(
            "config",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'{}'::jsonb"),
        ),
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
            name="fk_table_view_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["app_user.id"],
            name="fk_table_view_user_id",
            ondelete="CASCADE",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "user_id",
            "table_key",
            "name",
            name="uq_table_view_owner_key_name",
        ),
    )
    op.create_index("ix_table_view_organization_id", "table_view", ["organization_id"])
    op.create_index(
        "ix_table_view_owner_table",
        "table_view",
        ["organization_id", "user_id", "table_key"],
    )

    op.execute("ALTER TABLE table_view ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE table_view FORCE ROW LEVEL SECURITY")
    op.execute(
        """
        CREATE POLICY table_view_tenant_isolation ON table_view
        USING (organization_id = NULLIF(current_setting('app.current_org', true), '')::uuid)
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS table_view_tenant_isolation ON table_view")
    op.drop_index("ix_table_view_owner_table", table_name="table_view")
    op.drop_index("ix_table_view_organization_id", table_name="table_view")
    op.drop_table("table_view")
