"""create sales_invoice on shipment with RLS FORCE

Revision ID: 054_sales_invoice_rls
Revises: 053_edi_message_rls
Create Date: 2026-09-03

Faktura na zleceniu. Nie siec prawna. Nie kwota.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "054_sales_invoice_rls"
down_revision: str | None = "053_edi_message_rls"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "sales_invoice",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("shipment_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("invoice_kind", sa.String(length=16), nullable=False),
        sa.Column("invoice_ref", sa.String(length=64), nullable=False),
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
            name="fk_sales_invoice_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "shipment_id"],
            ["shipment.organization_id", "shipment.id"],
            name="fk_sales_invoice_shipment",
            ondelete="RESTRICT",
        ),
        sa.CheckConstraint(
            "invoice_kind IN ('issued', 'noted', 'other')",
            name="ck_sales_invoice_kind",
        ),
    )
    op.create_index(
        "ix_sales_invoice_organization_id",
        "sales_invoice",
        ["organization_id"],
    )
    op.create_index(
        "ix_sales_invoice_org_shipment",
        "sales_invoice",
        ["organization_id", "shipment_id"],
    )
    op.execute("ALTER TABLE sales_invoice ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE sales_invoice FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY sales_invoice_tenant_isolation ON sales_invoice
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS sales_invoice_tenant_isolation ON sales_invoice")
    op.drop_index("ix_sales_invoice_org_shipment", table_name="sales_invoice")
    op.drop_index("ix_sales_invoice_organization_id", table_name="sales_invoice")
    op.drop_table("sales_invoice")
