"""create sales_lane catalog with RLS FORCE

Revision ID: 365_sales_lane
Revises: 364_tracking_consent
Create Date: 2026-09-13

BR6.1 HITL katalog korytarza sprzedazy. Nie UN/LOCODE. Nie HubSpot.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "365_sales_lane"
down_revision: str | None = "364_tracking_consent"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "sales_lane",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("lane_code", sa.String(length=32), nullable=False),
        sa.Column("lane_kind", sa.String(length=16), nullable=False),
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
            name="fk_sales_lane_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_sales_lane_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "lane_code",
            name="uq_sales_lane_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_sales_lane_org_source_ref",
        ),
        sa.CheckConstraint(
            "lane_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_sales_lane_code",
        ),
        sa.CheckConstraint(
            "lane_kind IN ('repeat', 'spot', 'other')",
            name="ck_sales_lane_kind",
        ),
    )
    op.create_index(
        "ix_sales_lane_organization_id",
        "sales_lane",
        ["organization_id"],
    )
    op.execute("ALTER TABLE sales_lane ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE sales_lane FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY sales_lane_tenant_isolation ON sales_lane
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS sales_lane_tenant_isolation ON sales_lane",
    )
    op.drop_index(
        "ix_sales_lane_organization_id",
        table_name="sales_lane",
    )
    op.drop_table("sales_lane")
