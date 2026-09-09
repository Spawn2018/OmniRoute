"""add optional route_label on trip leftover T2

Revision ID: 153_trip_route_label
Revises: 152_stop_group
Create Date: 2026-09-09

Opcjonalna etykieta trasy HITL. Bez km.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "153_trip_route_label"
down_revision: str | None = "152_stop_group"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "trip",
        sa.Column("route_label", sa.String(length=128), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("trip", "route_label")
