"""create quote_invoice_settlement with RLS FORCE

Revision ID: 056_quote_invoice_settlement_rls
Revises: 055_sales_invoice_ksef_ref
Create Date: 2026-09-03

Wiazanie wyceny z faktura. Nie kwota. Nie druga marza.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "056_quote_invoice_settlement_rls"
down_revision: str | None = "055_sales_invoice_ksef_ref"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_unique_constraint(
        "uq_sales_invoice_org_id",
        "sales_invoice",
        ["organization_id", "id"],
    )
    op.create_table(
        "quote_invoice_settlement",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("quotation_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("sales_invoice_id", postgresql.UUID(as_uuid=True), nullable=False),
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
            name="fk_quote_invoice_settlement_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "quotation_id"],
            ["quotation.organization_id", "quotation.id"],
            name="fk_quote_invoice_settlement_quotation",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "sales_invoice_id"],
            ["sales_invoice.organization_id", "sales_invoice.id"],
            name="fk_quote_invoice_settlement_invoice",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "quotation_id",
            "sales_invoice_id",
            name="uq_quote_invoice_settlement_pair",
        ),
    )
    op.create_index(
        "ix_quote_invoice_settlement_organization_id",
        "quote_invoice_settlement",
        ["organization_id"],
    )
    op.create_index(
        "ix_quote_invoice_settlement_org_quotation",
        "quote_invoice_settlement",
        ["organization_id", "quotation_id"],
    )
    op.execute("ALTER TABLE quote_invoice_settlement ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE quote_invoice_settlement FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY quote_invoice_settlement_tenant_isolation
        ON quote_invoice_settlement
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS quote_invoice_settlement_tenant_isolation "
        "ON quote_invoice_settlement"
    )
    op.drop_index(
        "ix_quote_invoice_settlement_org_quotation",
        table_name="quote_invoice_settlement",
    )
    op.drop_index(
        "ix_quote_invoice_settlement_organization_id",
        table_name="quote_invoice_settlement",
    )
    op.drop_table("quote_invoice_settlement")
    op.drop_constraint("uq_sales_invoice_org_id", "sales_invoice", type_="unique")
