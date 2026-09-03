"""create fx_difference with RLS FORCE

Revision ID: 059_fx_difference_rls
Revises: 058_money_cost_rls
Create Date: 2026-09-03

Wiazanie wyceny z kursem tabeli A. Nie kwota. Nie przeliczenie.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "059_fx_difference_rls"
down_revision: str | None = "058_money_cost_rls"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "fx_difference",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("quotation_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("nbp_rate_id", postgresql.UUID(as_uuid=True), nullable=False),
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
            name="fk_fx_difference_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "quotation_id"],
            ["quotation.organization_id", "quotation.id"],
            name="fk_fx_difference_quotation",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "nbp_rate_id"],
            ["nbp_rate.organization_id", "nbp_rate.id"],
            name="fk_fx_difference_rate",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "quotation_id",
            "nbp_rate_id",
            name="uq_fx_difference_pair",
        ),
    )
    op.create_index("ix_fx_difference_organization_id", "fx_difference", ["organization_id"])
    op.create_index(
        "ix_fx_difference_org_quotation",
        "fx_difference",
        ["organization_id", "quotation_id"],
    )
    op.execute("ALTER TABLE fx_difference ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE fx_difference FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY fx_difference_tenant_isolation
        ON fx_difference
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS fx_difference_tenant_isolation ON fx_difference")
    op.drop_index("ix_fx_difference_org_quotation", table_name="fx_difference")
    op.drop_index("ix_fx_difference_organization_id", table_name="fx_difference")
    op.drop_table("fx_difference")
