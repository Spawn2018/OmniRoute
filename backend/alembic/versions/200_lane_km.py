"""create lane_km catalog with RLS FORCE

Revision ID: 200_lane_km
Revises: 199_circle_sim
Create Date: 2026-09-10

HITL km ładowny/pusty/dolot jako dane. Nie Haversine. Nie trip.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "200_lane_km"
down_revision: str | None = "199_circle_sim"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "lane_km",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("km_code", sa.String(length=32), nullable=False),
        sa.Column("loaded_km", sa.Numeric(14, 4), nullable=False),
        sa.Column("empty_km", sa.Numeric(14, 4), nullable=False),
        sa.Column("approach_km", sa.Numeric(14, 4), nullable=False),
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
            name="fk_lane_km_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_lane_km_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "km_code",
            name="uq_lane_km_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_lane_km_org_source_ref",
        ),
        sa.CheckConstraint(
            "km_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_lane_km_code",
        ),
        sa.CheckConstraint(
            "loaded_km >= 0",
            name="ck_lane_km_loaded",
        ),
        sa.CheckConstraint(
            "empty_km >= 0",
            name="ck_lane_km_empty",
        ),
        sa.CheckConstraint(
            "approach_km >= 0",
            name="ck_lane_km_approach",
        ),
    )
    # Lista per tenant: unique prefix albo ten indeks — nie sekwencyjne skanowanie.
    op.create_index(
        "ix_lane_km_organization_id",
        "lane_km",
        ["organization_id"],
    )
    op.execute("ALTER TABLE lane_km ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE lane_km FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY lane_km_tenant_isolation ON lane_km
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS lane_km_tenant_isolation ON lane_km")
    op.drop_index("ix_lane_km_organization_id", table_name="lane_km")
    op.drop_table("lane_km")
