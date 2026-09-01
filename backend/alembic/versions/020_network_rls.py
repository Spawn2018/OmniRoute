"""create network catalog with RLS

Revision ID: 020_network_rls
Revises: 019_dangerous_good_rls
Create Date: 2026-09-01
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "020_network_rls"
down_revision: str | None = "019_dangerous_good_rls"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "network",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("code", sa.String(length=32), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column(
            "aliases",
            postgresql.ARRAY(sa.Text()),
            nullable=False,
            server_default="{}",
        ),
        sa.Column("website", sa.String(length=256), nullable=True),
        sa.Column("region_scope", sa.String(length=64), nullable=True),
        sa.Column("is_global", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("source_ref", sa.String(length=256), nullable=False),
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
            name="fk_network_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "code", name="uq_network_org_code"),
        sa.CheckConstraint("code ~ '^[a-z][a-z0-9_]{1,31}$'", name="ck_network_code_snake"),
    )
    op.create_index("ix_network_organization_id", "network", ["organization_id"])
    op.create_index(
        "ix_network_aliases",
        "network",
        ["aliases"],
        postgresql_using="gin",
    )

    op.execute("ALTER TABLE network ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE network FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY network_tenant_isolation ON network
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS network_tenant_isolation ON network")
    op.drop_index("ix_network_aliases", table_name="network")
    op.drop_index("ix_network_organization_id", table_name="network")
    op.drop_table("network")
