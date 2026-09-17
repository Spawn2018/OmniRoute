"""create purchase_invoice catalog with RLS FORCE

Revision ID: 429_purchase_invoice
Revises: 428_self_billing_mark
Create Date: 2026-09-17

F10 HITL purchase_invoice ingest. Nie ranking. Nie allocation. Nie kwota.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "429_purchase_invoice"
down_revision: str | None = "428_self_billing_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "purchase_invoice",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("invoice_ref", sa.String(length=64), nullable=False),
        sa.Column("invoice_kind", sa.String(length=16), nullable=False),
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
            name="fk_purchase_invoice_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "id",
            name="uq_purchase_invoice_org_id",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "invoice_ref",
            name="uq_purchase_invoice_org_ref",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_purchase_invoice_org_source_ref",
        ),
        sa.CheckConstraint(
            "char_length(btrim(invoice_ref)) BETWEEN 1 AND 64",
            name="ck_purchase_invoice_ref",
        ),
        sa.CheckConstraint(
            "invoice_kind IN ('noted', 'other')",
            name="ck_purchase_invoice_kind",
        ),
    )
    op.create_index(
        "ix_purchase_invoice_organization_id",
        "purchase_invoice",
        ["organization_id"],
    )
    op.execute("ALTER TABLE purchase_invoice ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE purchase_invoice FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY purchase_invoice_tenant_isolation ON purchase_invoice
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS purchase_invoice_tenant_isolation ON purchase_invoice",
    )
    op.drop_index(
        "ix_purchase_invoice_organization_id",
        table_name="purchase_invoice",
    )
    op.drop_table("purchase_invoice")
