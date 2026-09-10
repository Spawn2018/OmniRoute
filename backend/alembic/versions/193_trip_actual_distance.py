"""add optional actual_distance_km on trip leftover T2c

Revision ID: 193_trip_actual_distance
Revises: 192_trip_planned_distance
Create Date: 2026-09-10

Opcjonalna odległość wykonana HITL. Nie GPS. Nie nowa tabela.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "193_trip_actual_distance"
down_revision: str | None = "192_trip_planned_distance"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "trip",
        sa.Column("actual_distance_km", sa.Numeric(14, 4), nullable=True),
    )
    op.create_check_constraint(
        "ck_trip_actual_distance",
        "trip",
        "actual_distance_km IS NULL OR actual_distance_km >= 0",
    )


def downgrade() -> None:
    op.drop_constraint("ck_trip_actual_distance", "trip", type_="check")
    op.drop_column("trip", "actual_distance_km")
