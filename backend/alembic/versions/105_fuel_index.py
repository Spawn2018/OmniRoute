"""create fuel_index catalog with RLS FORCE

Revision ID: 105_fuel_index
Revises: 104_charge_template
Create Date: 2026-09-08

Indeks FSC/BAF/CAF jako dane obok nbp_rate. Nie mnożenie na charge.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "105_fuel_index"
down_revision: str | None = "104_charge_template"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "fuel_index",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("index_kind", sa.String(length=8), nullable=False),
        sa.Column("published_on", sa.Date(), nullable=False),
        sa.Column("index_value", sa.Numeric(14, 4), nullable=False),
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
            name="fk_fuel_index_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_fuel_index_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "index_kind",
            "published_on",
            name="uq_fuel_index_org_kind_day",
        ),
        sa.CheckConstraint("index_kind IN ('fsc', 'baf', 'caf')", name="ck_fuel_index_kind"),
        sa.CheckConstraint("index_value > 0", name="ck_fuel_index_value_positive"),
    )
    op.create_index(
        "ix_fuel_index_organization_id",
        "fuel_index",
        ["organization_id"],
    )
    op.create_index(
        "ix_fuel_index_org_kind",
        "fuel_index",
        ["organization_id", "index_kind"],
    )
    op.execute("ALTER TABLE fuel_index ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE fuel_index FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY fuel_index_tenant_isolation ON fuel_index
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS fuel_index_tenant_isolation ON fuel_index")
    op.drop_index("ix_fuel_index_org_kind", table_name="fuel_index")
    op.drop_index("ix_fuel_index_organization_id", table_name="fuel_index")
    op.drop_table("fuel_index")
