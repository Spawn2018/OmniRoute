"""create shipment booking row with RLS FORCE

Revision ID: 049_shipment_rls
Revises: 048_party_sanctions_screen
Create Date: 2026-09-03

Zlecenie z wyceny. Nie tracking. Nie kwota.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "049_shipment_rls"
down_revision: str | None = "048_party_sanctions_screen"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_unique_constraint(
        "uq_quotation_org_id",
        "quotation",
        ["organization_id", "id"],
    )
    op.create_table(
        "shipment",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("quotation_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("party_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("source_ref", sa.String(length=256), nullable=False),
        sa.Column("status", sa.String(length=8), nullable=False),
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
            name="fk_shipment_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "quotation_id"],
            ["quotation.organization_id", "quotation.id"],
            name="fk_shipment_quotation",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "party_id"],
            ["party.organization_id", "party.id"],
            name="fk_shipment_party",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "quotation_id",
            name="uq_shipment_org_quotation",
        ),
        sa.CheckConstraint("status = 'draft'", name="ck_shipment_status_draft"),
    )
    op.create_index(
        "ix_shipment_organization_id",
        "shipment",
        ["organization_id"],
    )
    op.create_index(
        "ix_shipment_org_party",
        "shipment",
        ["organization_id", "party_id"],
    )
    op.create_index(
        "ix_shipment_org_created",
        "shipment",
        ["organization_id", "created_at"],
    )
    op.execute("ALTER TABLE shipment ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE shipment FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY shipment_tenant_isolation ON shipment
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS shipment_tenant_isolation ON shipment")
    op.drop_index("ix_shipment_org_created", table_name="shipment")
    op.drop_index("ix_shipment_org_party", table_name="shipment")
    op.drop_index("ix_shipment_organization_id", table_name="shipment")
    op.drop_table("shipment")
    op.drop_constraint("uq_quotation_org_id", "quotation", type_="unique")
