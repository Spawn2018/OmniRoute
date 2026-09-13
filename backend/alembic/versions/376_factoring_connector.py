"""create factoring_connector catalog with RLS FORCE

Revision ID: 376_factoring_connector
Revises: 375_silk_corridor_mark
Create Date: 2026-09-14

BR5.0 HITL katalog partnera faktoringowego. Nie live SMEO HTTP. Nie sekrety.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "376_factoring_connector"
down_revision: str | None = "375_silk_corridor_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "factoring_connector",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("connector_code", sa.String(length=32), nullable=False),
        sa.Column("system_kind", sa.String(length=16), nullable=False),
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
        sa.Column("created_by", PGUUID(as_uuid=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organization.id"],
            name="fk_factoring_connector_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_factoring_connector_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "connector_code",
            name="uq_factoring_connector_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_factoring_connector_org_source_ref",
        ),
        sa.CheckConstraint(
            "connector_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_factoring_connector_code",
        ),
        sa.CheckConstraint(
            "system_kind IN ('smeo', 'other')",
            name="ck_factoring_connector_kind",
        ),
    )
    op.create_index(
        "ix_factoring_connector_organization_id",
        "factoring_connector",
        ["organization_id"],
    )
    op.execute("ALTER TABLE factoring_connector ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE factoring_connector FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY factoring_connector_tenant_isolation ON factoring_connector
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS factoring_connector_tenant_isolation ON factoring_connector"
    )
    op.drop_index("ix_factoring_connector_organization_id", table_name="factoring_connector")
    op.drop_table("factoring_connector")
