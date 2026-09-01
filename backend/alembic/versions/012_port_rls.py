"""create port catalog with RLS

Revision ID: 012_port_rls
Revises: 011_organization_setting_rls
Create Date: 2026-09-01
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "012_port_rls"
down_revision: str | None = "011_organization_setting_rls"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "port",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("unlocode", sa.String(length=5), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("country_code", sa.String(length=2), nullable=False),
        sa.Column("lat", sa.Numeric(precision=8, scale=6), nullable=True),
        sa.Column("lng", sa.Numeric(precision=9, scale=6), nullable=True),
        sa.Column("is_seaport", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.Column(
            "function_flags",
            postgresql.ARRAY(sa.Text()),
            server_default="{}",
            nullable=False,
        ),
        sa.Column(
            "aliases",
            postgresql.ARRAY(sa.Text()),
            server_default="{}",
            nullable=False,
        ),
        sa.Column("is_official", sa.Boolean(), server_default=sa.text("true"), nullable=False),
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
            name="fk_port_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "unlocode", name="uq_port_org_unlocode"),
    )
    op.create_index("ix_port_organization_id", "port", ["organization_id"])
    op.create_index("ix_port_aliases", "port", ["aliases"], postgresql_using="gin")

    op.execute("ALTER TABLE port ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE port FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY port_tenant_isolation ON port
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS port_tenant_isolation ON port")
    op.drop_index("ix_port_aliases", table_name="port")
    op.drop_index("ix_port_organization_id", table_name="port")
    op.drop_table("port")
