"""create cash_flow with RLS FORCE

Revision ID: 060_cash_flow_rls
Revises: 059_fx_difference_rls
Create Date: 2026-09-03

Wiazanie wyceny z platnoscia. Nie kwota. Nie odejmowanie.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "060_cash_flow_rls"
down_revision: str | None = "059_fx_difference_rls"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "cash_flow",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("quotation_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("bank_payment_id", postgresql.UUID(as_uuid=True), nullable=False),
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
            name="fk_cash_flow_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "quotation_id"],
            ["quotation.organization_id", "quotation.id"],
            name="fk_cash_flow_quotation",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "bank_payment_id"],
            ["bank_payment.organization_id", "bank_payment.id"],
            name="fk_cash_flow_payment",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "quotation_id",
            "bank_payment_id",
            name="uq_cash_flow_pair",
        ),
    )
    op.create_index("ix_cash_flow_organization_id", "cash_flow", ["organization_id"])
    op.create_index(
        "ix_cash_flow_org_quotation",
        "cash_flow",
        ["organization_id", "quotation_id"],
    )
    op.execute("ALTER TABLE cash_flow ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE cash_flow FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY cash_flow_tenant_isolation
        ON cash_flow
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS cash_flow_tenant_isolation ON cash_flow")
    op.drop_index("ix_cash_flow_org_quotation", table_name="cash_flow")
    op.drop_index("ix_cash_flow_organization_id", table_name="cash_flow")
    op.drop_table("cash_flow")
