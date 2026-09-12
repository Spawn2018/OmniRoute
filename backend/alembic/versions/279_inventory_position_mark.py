"""create inventory_position_mark catalog with RLS FORCE

Revision ID: 271_inventory_position_mark
Revises: 276_Inventory position_mark
Create Date: 2026-09-12

EXP3.3 HITL znacznik Inventory position jako dane. Nie live giełda. Nie bilans SQL.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "279_inventory_position_mark"
down_revision: str | None = "278_vda_odette_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "inventory_position_mark",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("mark_code", sa.String(length=32), nullable=False),
        sa.Column("stock_kind", sa.String(length=16), nullable=False),
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
            name="fk_inventory_position_mark_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_inventory_position_mark_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_inventory_position_mark_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_inventory_position_mark_org_source_ref",
        ),
        sa.CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_inventory_position_mark_code",
        ),
        sa.CheckConstraint(
            "stock_kind IN ('position', 'plant', 'sku', 'other')",
            name="ck_inventory_position_mark_stock_kind",
        ),
    )
    op.create_index(
        "ix_inventory_position_mark_organization_id",
        "inventory_position_mark",
        ["organization_id"],
    )
    op.execute("ALTER TABLE inventory_position_mark ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE inventory_position_mark FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY inventory_position_mark_tenant_isolation ON inventory_position_mark
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS inventory_position_mark_tenant_isolation ON inventory_position_mark",
    )
    op.drop_index(
        "ix_inventory_position_mark_organization_id",
        table_name="inventory_position_mark",
    )
    op.drop_table("inventory_position_mark")
