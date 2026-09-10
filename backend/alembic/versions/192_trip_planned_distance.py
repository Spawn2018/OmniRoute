"""add optional planned_distance_km on trip leftover T2c

Revision ID: 192_trip_planned_distance
Revises: 191_stop_pod_quality
Create Date: 2026-09-10

Opcjonalna odległość planowana HITL. Nie actual. Nie GPS. Nie nowa tabela.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "192_trip_planned_distance"
down_revision: str | None = "191_stop_pod_quality"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "trip",
        sa.Column("planned_distance_km", sa.Numeric(14, 4), nullable=True),
    )
    op.create_check_constraint(
        "ck_trip_planned_distance",
        "trip",
        "planned_distance_km IS NULL OR planned_distance_km >= 0",
    )


def downgrade() -> None:
    op.drop_constraint("ck_trip_planned_distance", "trip", type_="check")
    op.drop_column("trip", "planned_distance_km")
