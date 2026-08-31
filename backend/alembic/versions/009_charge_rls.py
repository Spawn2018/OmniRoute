"""create charge buy+sell with RLS

Revision ID: 009_charge_rls
Revises: 008_rate_line_rls
Create Date: 2026-09-01
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "009_charge_rls"
down_revision: str | None = "008_rate_line_rls"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "charge",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("charge_code", sa.String(length=32), nullable=False),
        sa.Column("buy_amount", sa.Numeric(14, 4), nullable=False),
        sa.Column("buy_currency", sa.CHAR(length=3), nullable=False),
        sa.Column("sell_amount", sa.Numeric(14, 4), nullable=False),
        sa.Column("sell_currency", sa.CHAR(length=3), nullable=False),
        sa.Column("rate_line_id", postgresql.UUID(as_uuid=True), nullable=True),
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
            name="fk_charge_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["rate_line_id"],
            ["rate_line.id"],
            name="fk_charge_rate_line_id",
            ondelete="RESTRICT",
        ),
        sa.CheckConstraint("buy_currency = sell_currency", name="charge_same_currency"),
    )
    op.create_index("ix_charge_organization_id", "charge", ["organization_id"])

    op.execute("ALTER TABLE charge ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE charge FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY charge_tenant_isolation ON charge
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS charge_tenant_isolation ON charge")
    op.drop_index("ix_charge_organization_id", table_name="charge")
    op.drop_table("charge")
