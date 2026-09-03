"""create cost_to_serve with RLS FORCE

Revision ID: 061_cost_to_serve_rls
Revises: 060_cash_flow_rls
Create Date: 2026-09-03

Wiazanie SOP z wycena. Nie kwota. Nie suma.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "061_cost_to_serve_rls"
down_revision: str | None = "060_cash_flow_rls"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_unique_constraint(
        "uq_customer_sop_org_id",
        "customer_sop",
        ["organization_id", "id"],
    )
    op.create_table(
        "cost_to_serve",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("customer_sop_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("quotation_id", postgresql.UUID(as_uuid=True), nullable=False),
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
            name="fk_cost_to_serve_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "customer_sop_id"],
            ["customer_sop.organization_id", "customer_sop.id"],
            name="fk_cost_to_serve_sop",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "quotation_id"],
            ["quotation.organization_id", "quotation.id"],
            name="fk_cost_to_serve_quotation",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "customer_sop_id",
            "quotation_id",
            name="uq_cost_to_serve_pair",
        ),
    )
    op.create_index("ix_cost_to_serve_organization_id", "cost_to_serve", ["organization_id"])
    op.create_index(
        "ix_cost_to_serve_org_sop",
        "cost_to_serve",
        ["organization_id", "customer_sop_id"],
    )
    op.execute("ALTER TABLE cost_to_serve ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE cost_to_serve FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY cost_to_serve_tenant_isolation
        ON cost_to_serve
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS cost_to_serve_tenant_isolation ON cost_to_serve")
    op.drop_index("ix_cost_to_serve_org_sop", table_name="cost_to_serve")
    op.drop_index("ix_cost_to_serve_organization_id", table_name="cost_to_serve")
    op.drop_table("cost_to_serve")
    op.drop_constraint("uq_customer_sop_org_id", "customer_sop", type_="unique")
