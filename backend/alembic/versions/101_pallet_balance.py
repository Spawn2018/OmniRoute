"""create pallet_balance on party with RLS FORCE

Revision ID: 101_pallet_balance
Revises: 100_ocean_bill
Create Date: 2026-09-08

Saldo Chep/LPR na kontrahencie. Integer sztuk. Nie giełda. Nie depozyt.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "101_pallet_balance"
down_revision: str | None = "100_ocean_bill"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "pallet_balance",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("party_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("pallet_kind", sa.String(length=8), nullable=False),
        sa.Column("unit_count", sa.Integer(), nullable=False),
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
            name="fk_pallet_balance_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "party_id"],
            ["party.organization_id", "party.id"],
            name="fk_pallet_balance_party",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_pallet_balance_org_id"),
        sa.CheckConstraint(
            "pallet_kind IN ('chep','lpr')",
            name="ck_pallet_balance_kind",
        ),
        sa.CheckConstraint("unit_count >= 0", name="ck_pallet_balance_count"),
    )
    op.create_index(
        "ix_pallet_balance_organization_id",
        "pallet_balance",
        ["organization_id"],
    )
    op.create_index(
        "ix_pallet_balance_org_party",
        "pallet_balance",
        ["organization_id", "party_id"],
    )
    op.execute("ALTER TABLE pallet_balance ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE pallet_balance FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY pallet_balance_tenant_isolation ON pallet_balance
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS pallet_balance_tenant_isolation ON pallet_balance")
    op.drop_index("ix_pallet_balance_org_party", table_name="pallet_balance")
    op.drop_index("ix_pallet_balance_organization_id", table_name="pallet_balance")
    op.drop_table("pallet_balance")
