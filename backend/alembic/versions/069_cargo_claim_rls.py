"""create cargo_claim on shipment with RLS FORCE

Revision ID: 069_cargo_claim_rls
Revises: 068_shipment_leg_ocean_lcl_kind
Create Date: 2026-09-04

Reklamacja ładunku na zleceniu. Nie kwota. Nie scoring.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "069_cargo_claim_rls"
down_revision: str | None = "068_shipment_leg_ocean_lcl_kind"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "cargo_claim",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("shipment_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("claim_kind", sa.String(length=16), nullable=False),
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
            name="fk_cargo_claim_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "shipment_id"],
            ["shipment.organization_id", "shipment.id"],
            name="fk_cargo_claim_shipment",
            ondelete="RESTRICT",
        ),
        sa.CheckConstraint(
            "claim_kind IN ('damage', 'shortage', 'other')",
            name="ck_cargo_claim_kind",
        ),
    )
    op.create_index(
        "ix_cargo_claim_organization_id",
        "cargo_claim",
        ["organization_id"],
    )
    op.create_index(
        "ix_cargo_claim_org_shipment",
        "cargo_claim",
        ["organization_id", "shipment_id"],
    )
    op.execute("ALTER TABLE cargo_claim ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE cargo_claim FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY cargo_claim_tenant_isolation ON cargo_claim
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS cargo_claim_tenant_isolation ON cargo_claim")
    op.drop_index("ix_cargo_claim_org_shipment", table_name="cargo_claim")
    op.drop_index("ix_cargo_claim_organization_id", table_name="cargo_claim")
    op.drop_table("cargo_claim")
