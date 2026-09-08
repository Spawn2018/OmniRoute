"""create trip catalog with RLS FORCE

Revision ID: 092_trip
Revises: 091_resource
Create Date: 2026-09-08

Przejazd per tenant. Nie km. Nie mapa.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "092_trip"
down_revision: str | None = "091_resource"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_unique_constraint("uq_resource_org_id", "resource", ["organization_id", "id"])
    op.create_table(
        "trip",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("trip_no", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=12), nullable=False),
        sa.Column("vehicle_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("trailer_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("driver_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("source_ref", sa.Text(), nullable=False),
        sa.Column("superseded_by", postgresql.UUID(as_uuid=True), nullable=True),
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
            name="fk_trip_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "vehicle_id"],
            ["resource.organization_id", "resource.id"],
            name="fk_trip_vehicle",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "trailer_id"],
            ["resource.organization_id", "resource.id"],
            name="fk_trip_trailer",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "driver_id"],
            ["resource.organization_id", "resource.id"],
            name="fk_trip_driver",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["superseded_by"],
            ["trip.id"],
            name="fk_trip_superseded_by",
            ondelete="RESTRICT",
        ),
        sa.CheckConstraint(
            "status IN ('draft', 'planned', 'in_transit', 'completed', 'cancelled')",
            name="ck_trip_status",
        ),
    )
    op.create_index("ix_trip_organization_id", "trip", ["organization_id"])
    op.create_index("ix_trip_org_status", "trip", ["organization_id", "status"])
    op.execute("ALTER TABLE trip ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE trip FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY trip_tenant_isolation
        ON trip
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS trip_tenant_isolation ON trip")
    op.drop_index("ix_trip_org_status", table_name="trip")
    op.drop_index("ix_trip_organization_id", table_name="trip")
    op.drop_table("trip")
    op.drop_constraint("uq_resource_org_id", "resource", type_="unique")
