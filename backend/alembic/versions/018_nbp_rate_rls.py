"""create nbp_rate catalog with RLS

Revision ID: 018_nbp_rate_rls
Revises: 017_commodity_code_rls
Create Date: 2026-09-01
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "018_nbp_rate_rls"
down_revision: str | None = "017_commodity_code_rls"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "nbp_rate",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("currency", sa.CHAR(length=3), nullable=False),
        sa.Column("rate_date", sa.Date(), nullable=False),
        sa.Column("mid", sa.Numeric(14, 4), nullable=False),
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
            name="fk_nbp_rate_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "currency",
            "rate_date",
            name="uq_nbp_rate_org_currency_date",
        ),
        sa.CheckConstraint(
            "currency ~ '^[A-Z]{3}$' AND currency <> 'PLN'",
            name="ck_nbp_rate_currency_iso",
        ),
        sa.CheckConstraint("mid > 0", name="ck_nbp_rate_mid_positive"),
    )
    op.create_index("ix_nbp_rate_organization_id", "nbp_rate", ["organization_id"])
    op.create_index(
        "ix_nbp_rate_org_currency_date",
        "nbp_rate",
        ["organization_id", "currency", "rate_date"],
    )

    op.execute("ALTER TABLE nbp_rate ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE nbp_rate FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY nbp_rate_tenant_isolation ON nbp_rate
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS nbp_rate_tenant_isolation ON nbp_rate")
    op.drop_index("ix_nbp_rate_org_currency_date", table_name="nbp_rate")
    op.drop_index("ix_nbp_rate_organization_id", table_name="nbp_rate")
    op.drop_table("nbp_rate")
