"""create bookkeeping with RLS FORCE

Revision ID: 062_bookkeeping_rls
Revises: 061_cost_to_serve_rls
Create Date: 2026-09-03

Wiazanie oplat z faktura. Nie kwota. Nie JPK.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "062_bookkeeping_rls"
down_revision: str | None = "061_cost_to_serve_rls"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_unique_constraint(
        "uq_charge_org_id",
        "charge",
        ["organization_id", "id"],
    )
    op.create_table(
        "bookkeeping",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("charge_id", postgresql.UUID(as_uuid=True), nullable=False),
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
            name="fk_bookkeeping_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "charge_id"],
            ["charge.organization_id", "charge.id"],
            name="fk_bookkeeping_charge",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "sales_invoice_id"],
            ["sales_invoice.organization_id", "sales_invoice.id"],
            name="fk_bookkeeping_invoice",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "charge_id",
            "sales_invoice_id",
            name="uq_bookkeeping_pair",
        ),
    )
    op.create_index("ix_bookkeeping_organization_id", "bookkeeping", ["organization_id"])
    op.create_index(
        "ix_bookkeeping_org_charge",
        "bookkeeping",
        ["organization_id", "charge_id"],
    )
    op.execute("ALTER TABLE bookkeeping ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE bookkeeping FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY bookkeeping_tenant_isolation
        ON bookkeeping
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS bookkeeping_tenant_isolation ON bookkeeping")
    op.drop_index("ix_bookkeeping_org_charge", table_name="bookkeeping")
    op.drop_index("ix_bookkeeping_organization_id", table_name="bookkeeping")
    op.drop_table("bookkeeping")
    op.drop_constraint("uq_charge_org_id", "charge", type_="unique")
