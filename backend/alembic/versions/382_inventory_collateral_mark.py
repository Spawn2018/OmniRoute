"""create inventory_collateral_mark catalog with RLS FORCE

Revision ID: 382_inventory_collateral_mark
Revises: 381_inventory_finance_mark
Create Date: 2026-09-14

BR1.3 HITL katalog zabezpieczenia na towarze. Nie FK pozycji. Nie live zastaw.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "382_inventory_collateral_mark"
down_revision: str | None = "381_inventory_finance_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "inventory_collateral_mark",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("mark_code", sa.String(length=32), nullable=False),
        sa.Column("collateral_kind", sa.String(length=16), nullable=False),
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
            name="fk_inventory_collateral_mark_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "id",
            name="uq_inventory_collateral_mark_org_id",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_inventory_collateral_mark_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_inventory_collateral_mark_org_src",
        ),
        sa.CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_inventory_collateral_mark_code",
        ),
        sa.CheckConstraint(
            "collateral_kind IN ('pledge', 'lien', 'hold', 'other')",
            name="ck_inventory_collateral_mark_kind",
        ),
    )
    op.create_index(
        "ix_inventory_collateral_mark_organization_id",
        "inventory_collateral_mark",
        ["organization_id"],
    )
    op.execute("ALTER TABLE inventory_collateral_mark ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE inventory_collateral_mark FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY inventory_collateral_mark_tenant_isolation
        ON inventory_collateral_mark
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS inventory_collateral_mark_tenant_isolation "
        "ON inventory_collateral_mark",
    )
    op.drop_index(
        "ix_inventory_collateral_mark_organization_id",
        table_name="inventory_collateral_mark",
    )
    op.drop_table("inventory_collateral_mark")
