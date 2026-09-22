"""create pallet_ledger movement catalog with RLS FORCE

Revision ID: 501_pallet_ledger
Revises: 500_shipment_fx_anchor_dates
Create Date: 2026-09-22

D7c HITL ledger ruchu palet. delta_count ze znakiem. Nie mutuje salda. Nie giełda.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "501_pallet_ledger"
down_revision: str | None = "500_shipment_fx_anchor_dates"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "pallet_ledger",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("party_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("movement_code", sa.String(length=64), nullable=False),
        sa.Column("pallet_kind", sa.String(length=8), nullable=False),
        sa.Column("delta_count", sa.Integer(), nullable=False),
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
            name="fk_pallet_ledger_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "party_id"],
            ["party.organization_id", "party.id"],
            name="fk_pallet_ledger_party",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_pallet_ledger_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "movement_code",
            name="uq_pallet_ledger_org_code",
        ),
        sa.CheckConstraint(
            "pallet_kind IN ('chep','lpr','epal')",
            name="ck_pallet_ledger_kind",
        ),
        sa.CheckConstraint(
            "movement_code ~ '^[a-z][a-z0-9_]{0,63}$'",
            name="ck_pallet_ledger_code",
        ),
    )
    op.create_index(
        "ix_pallet_ledger_organization_id",
        "pallet_ledger",
        ["organization_id"],
    )
    op.create_index(
        "ix_pallet_ledger_org_party",
        "pallet_ledger",
        ["organization_id", "party_id"],
    )
    op.execute("ALTER TABLE pallet_ledger ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE pallet_ledger FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY pallet_ledger_tenant_isolation ON pallet_ledger
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS pallet_ledger_tenant_isolation ON pallet_ledger")
    op.drop_index("ix_pallet_ledger_org_party", table_name="pallet_ledger")
    op.drop_index("ix_pallet_ledger_organization_id", table_name="pallet_ledger")
    op.drop_table("pallet_ledger")
