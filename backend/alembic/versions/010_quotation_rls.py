"""create quotation from current rate_line with RLS

Revision ID: 010_quotation_rls
Revises: 009_charge_rls
Create Date: 2026-09-01
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "010_quotation_rls"
down_revision: str | None = "009_charge_rls"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "quotation",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("charge_code", sa.String(length=32), nullable=False),
        sa.Column("rate_line_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("amount", sa.Numeric(14, 4), nullable=False),
        sa.Column("currency", sa.CHAR(length=3), nullable=False),
        sa.Column("source_ref", sa.String(length=512), nullable=False),
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
            name="fk_quotation_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["rate_line_id"],
            ["rate_line.id"],
            name="fk_quotation_rate_line_id",
            ondelete="RESTRICT",
        ),
    )
    op.create_index("ix_quotation_organization_id", "quotation", ["organization_id"])
    op.create_index(
        "ix_rate_line_current_charge_code",
        "rate_line",
        ["organization_id", "charge_code", "created_at"],
        postgresql_where=sa.text("superseded_by IS NULL"),
    )

    op.execute("ALTER TABLE quotation ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE quotation FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY quotation_tenant_isolation ON quotation
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS quotation_tenant_isolation ON quotation")
    op.drop_index("ix_rate_line_current_charge_code", table_name="rate_line")
    op.drop_index("ix_quotation_organization_id", table_name="quotation")
    op.drop_table("quotation")
