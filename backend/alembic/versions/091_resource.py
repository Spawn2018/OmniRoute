"""create resource catalog with RLS FORCE

Revision ID: 091_resource
Revises: 090_stop
Create Date: 2026-09-08

Katalog floty per tenant. Nie trip. Nie HW.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "091_resource"
down_revision: str | None = "090_stop"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "resource",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("resource_kind", sa.String(length=8), nullable=False),
        sa.Column("display_name", sa.String(length=64), nullable=False),
        sa.Column("registration_no", sa.String(length=32), nullable=True),
        sa.Column("source_ref", sa.Text(), nullable=False),
        sa.Column("superseded_by", postgresql.UUID(as_uuid=True), nullable=True),
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
            name="fk_resource_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["superseded_by"],
            ["resource.id"],
            name="fk_resource_superseded_by",
            ondelete="RESTRICT",
        ),
        sa.CheckConstraint(
            "resource_kind IN ('vehicle', 'driver', 'trailer')",
            name="ck_resource_kind",
        ),
    )
    op.create_index("ix_resource_organization_id", "resource", ["organization_id"])
    op.create_index(
        "ix_resource_org_kind",
        "resource",
        ["organization_id", "resource_kind"],
    )
    op.execute("ALTER TABLE resource ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE resource FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY resource_tenant_isolation
        ON resource
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS resource_tenant_isolation ON resource")
    op.drop_index("ix_resource_org_kind", table_name="resource")
    op.drop_index("ix_resource_organization_id", table_name="resource")
    op.drop_table("resource")
