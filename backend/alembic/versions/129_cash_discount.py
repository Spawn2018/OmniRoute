"""create cash_discount catalog with RLS FORCE

Revision ID: 129_cash_discount
Revises: 128_party_document
Create Date: 2026-09-09

HITL cash discount kind on sales_invoice + source_ref. Nie kwota. Nie CAMT.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "129_cash_discount"
down_revision: str | None = "128_party_document"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "cash_discount",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("sales_invoice_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("discount_kind", sa.String(length=32), nullable=False),
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
            name="fk_cash_discount_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "sales_invoice_id"],
            ["sales_invoice.organization_id", "sales_invoice.id"],
            name="fk_cash_discount_sales_invoice",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_cash_discount_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "sales_invoice_id",
            "discount_kind",
            name="uq_cash_discount_org_invoice_kind",
        ),
        sa.CheckConstraint(
            "discount_kind ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_cash_discount_kind",
        ),
    )
    op.create_index("ix_cash_discount_organization_id", "cash_discount", ["organization_id"])
    op.execute("ALTER TABLE cash_discount ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE cash_discount FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY cash_discount_tenant_isolation ON cash_discount
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS cash_discount_tenant_isolation ON cash_discount")
    op.drop_index("ix_cash_discount_organization_id", table_name="cash_discount")
    op.drop_table("cash_discount")
