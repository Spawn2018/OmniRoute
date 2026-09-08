"""create local_charge catalog with RLS FORCE

Revision ID: 106_local_charge
Revises: 105_fuel_index
Create Date: 2026-09-08

Dopłata lokalna THC/ISPS jako dane + Decimal. Nie warning braków.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "106_local_charge"
down_revision: str | None = "105_fuel_index"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "local_charge",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("charge_kind", sa.String(length=16), nullable=False),
        sa.Column("amount", sa.Numeric(14, 4), nullable=False),
        sa.Column("currency", sa.CHAR(length=3), nullable=False),
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
            name="fk_local_charge_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_local_charge_org_id"),
        sa.CheckConstraint(
            "charge_kind IN ('thc', 'isps', 'seal', 'amendment')",
            name="ck_local_charge_kind",
        ),
        sa.CheckConstraint("amount > 0", name="ck_local_charge_amount_positive"),
        sa.CheckConstraint("currency ~ '^[A-Z]{3}$'", name="ck_local_charge_currency_iso"),
    )
    op.create_index(
        "ix_local_charge_organization_id",
        "local_charge",
        ["organization_id"],
    )
    op.create_index(
        "ix_local_charge_org_kind",
        "local_charge",
        ["organization_id", "charge_kind"],
    )
    op.execute("ALTER TABLE local_charge ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE local_charge FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY local_charge_tenant_isolation ON local_charge
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS local_charge_tenant_isolation ON local_charge")
    op.drop_index("ix_local_charge_org_kind", table_name="local_charge")
    op.drop_index("ix_local_charge_organization_id", table_name="local_charge")
    op.drop_table("local_charge")
