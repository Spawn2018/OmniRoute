"""add optional driver2_id on trip leftover T2c

Revision ID: 151_trip_driver2
Revises: 150_shipment_parent
Create Date: 2026-09-09

Opcjonalny drugi kierowca. Bez km. Bez /fleet.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "151_trip_driver2"
down_revision: str | None = "150_shipment_parent"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "trip",
        sa.Column("driver2_id", postgresql.UUID(as_uuid=True), nullable=True),
    )
    op.create_foreign_key(
        "fk_trip_driver2",
        "trip",
        "resource",
        ["organization_id", "driver2_id"],
        ["organization_id", "id"],
        ondelete="RESTRICT",
    )
    # NULL <> UUID is UNKNOWN in CHECK — explicit IS NULL on both seats.
    op.create_check_constraint(
        "ck_trip_driver2_distinct",
        "trip",
        "driver2_id IS NULL OR driver_id IS NULL OR driver2_id <> driver_id",
    )


def downgrade() -> None:
    op.drop_constraint("ck_trip_driver2_distinct", "trip", type_="check")
    op.drop_constraint("fk_trip_driver2", "trip", type_="foreignkey")
    op.drop_column("trip", "driver2_id")
