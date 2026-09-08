"""create shipment_stakeholder with RLS FORCE

Revision ID: 086_shipment_stakeholder
Revises: 085_incoterm_responsibility
Create Date: 2026-09-08

Strona zlecenia per tenant. Nie I3. Nie EXP1.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "086_shipment_stakeholder"
down_revision: str | None = "085_incoterm_responsibility"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "shipment_stakeholder",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("shipment_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("party_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("role", sa.String(length=16), nullable=False),
        sa.Column("source_ref", sa.String(length=256), nullable=False),
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
            name="fk_shipment_stakeholder_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "shipment_id"],
            ["shipment.organization_id", "shipment.id"],
            name="fk_shipment_stakeholder_shipment",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "party_id"],
            ["party.organization_id", "party.id"],
            name="fk_shipment_stakeholder_party",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["superseded_by"],
            ["shipment_stakeholder.id"],
            name="fk_shipment_stakeholder_superseded_by",
            ondelete="RESTRICT",
        ),
        sa.CheckConstraint(
            "role IN ('shipper','consignee','origin_agent','dest_agent',"
            "'ocean_carrier','omni_customs','client_customs')",
            name="ck_shipment_stakeholder_role",
        ),
    )
    op.create_index(
        "ix_shipment_stakeholder_organization_id",
        "shipment_stakeholder",
        ["organization_id"],
    )
    op.create_index(
        "ix_shipment_stakeholder_org_shipment",
        "shipment_stakeholder",
        ["organization_id", "shipment_id"],
    )
    op.execute("ALTER TABLE shipment_stakeholder ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE shipment_stakeholder FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY shipment_stakeholder_tenant_isolation
        ON shipment_stakeholder
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS shipment_stakeholder_tenant_isolation "
        "ON shipment_stakeholder"
    )
    op.drop_index(
        "ix_shipment_stakeholder_org_shipment",
        table_name="shipment_stakeholder",
    )
    op.drop_index(
        "ix_shipment_stakeholder_organization_id",
        table_name="shipment_stakeholder",
    )
    op.drop_table("shipment_stakeholder")
