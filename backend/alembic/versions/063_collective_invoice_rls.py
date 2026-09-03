"""create collective_invoice with RLS FORCE

Revision ID: 063_collective_invoice_rls
Revises: 062_bookkeeping_rls
Create Date: 2026-09-03

Dodatkowe zlecenie na fakturze. Nie kwota. Nie platnosc paczka.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "063_collective_invoice_rls"
down_revision: str | None = "062_bookkeeping_rls"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "collective_invoice",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("sales_invoice_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("shipment_id", postgresql.UUID(as_uuid=True), nullable=False),
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
            name="fk_collective_invoice_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "sales_invoice_id"],
            ["sales_invoice.organization_id", "sales_invoice.id"],
            name="fk_collective_invoice_invoice",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "shipment_id"],
            ["shipment.organization_id", "shipment.id"],
            name="fk_collective_invoice_shipment",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "sales_invoice_id",
            "shipment_id",
            name="uq_collective_invoice_pair",
        ),
    )
    op.create_index(
        "ix_collective_invoice_organization_id",
        "collective_invoice",
        ["organization_id"],
    )
    op.create_index(
        "ix_collective_invoice_org_invoice",
        "collective_invoice",
        ["organization_id", "sales_invoice_id"],
    )
    op.execute("ALTER TABLE collective_invoice ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE collective_invoice FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY collective_invoice_tenant_isolation
        ON collective_invoice
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS collective_invoice_tenant_isolation ON collective_invoice")
    op.drop_index("ix_collective_invoice_org_invoice", table_name="collective_invoice")
    op.drop_index("ix_collective_invoice_organization_id", table_name="collective_invoice")
    op.drop_table("collective_invoice")
