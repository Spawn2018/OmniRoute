"""create bank_payment with RLS FORCE

Revision ID: 057_bank_payment_rls
Revises: 056_quote_invoice_settlement_rls
Create Date: 2026-09-03

Wiazanie faktury z rachunkiem. Nie kwota. Nie wyciag.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "057_bank_payment_rls"
down_revision: str | None = "056_quote_invoice_settlement_rls"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_unique_constraint(
        "uq_party_bank_account_org_id",
        "party_bank_account",
        ["organization_id", "id"],
    )
    op.create_table(
        "bank_payment",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("sales_invoice_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("party_bank_account_id", postgresql.UUID(as_uuid=True), nullable=False),
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
            name="fk_bank_payment_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "sales_invoice_id"],
            ["sales_invoice.organization_id", "sales_invoice.id"],
            name="fk_bank_payment_invoice",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "party_bank_account_id"],
            ["party_bank_account.organization_id", "party_bank_account.id"],
            name="fk_bank_payment_account",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "sales_invoice_id",
            "party_bank_account_id",
            name="uq_bank_payment_pair",
        ),
    )
    op.create_index(
        "ix_bank_payment_organization_id",
        "bank_payment",
        ["organization_id"],
    )
    op.create_index(
        "ix_bank_payment_org_invoice",
        "bank_payment",
        ["organization_id", "sales_invoice_id"],
    )
    op.execute("ALTER TABLE bank_payment ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE bank_payment FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY bank_payment_tenant_isolation
        ON bank_payment
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS bank_payment_tenant_isolation ON bank_payment")
    op.drop_index("ix_bank_payment_org_invoice", table_name="bank_payment")
    op.drop_index("ix_bank_payment_organization_id", table_name="bank_payment")
    op.drop_table("bank_payment")
    op.drop_constraint("uq_party_bank_account_org_id", "party_bank_account", type_="unique")
