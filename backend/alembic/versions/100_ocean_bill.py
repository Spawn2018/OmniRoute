"""create ocean_bill on shipment with RLS FORCE

Revision ID: 100_ocean_bill
Revises: 099_groupage_tariff
Create Date: 2026-09-08

Znacznik HBL/MBL na zleceniu. Bez PDF. Nie booking HZ/S21.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "100_ocean_bill"
down_revision: str | None = "099_groupage_tariff"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "ocean_bill",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("shipment_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("bill_no", sa.String(length=32), nullable=False),
        sa.Column("bill_kind", sa.String(length=8), nullable=False),
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
            name="fk_ocean_bill_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "shipment_id"],
            ["shipment.organization_id", "shipment.id"],
            name="fk_ocean_bill_shipment",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_ocean_bill_org_id"),
        sa.CheckConstraint(
            "bill_kind IN ('hbl','mbl')",
            name="ck_ocean_bill_kind",
        ),
    )
    op.create_index(
        "ix_ocean_bill_organization_id",
        "ocean_bill",
        ["organization_id"],
    )
    op.create_index(
        "ix_ocean_bill_org_shipment",
        "ocean_bill",
        ["organization_id", "shipment_id"],
    )
    op.execute("ALTER TABLE ocean_bill ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE ocean_bill FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY ocean_bill_tenant_isolation ON ocean_bill
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS ocean_bill_tenant_isolation ON ocean_bill")
    op.drop_index("ix_ocean_bill_org_shipment", table_name="ocean_bill")
    op.drop_index("ix_ocean_bill_organization_id", table_name="ocean_bill")
    op.drop_table("ocean_bill")
