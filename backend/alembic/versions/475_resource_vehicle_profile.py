"""add optional vehicle_profile on resource leftover T2

Revision ID: 475_resource_vehicle_profile
Revises: 474_resource_driver_card_no
Create Date: 2026-09-20

Opcjonalny profil pojazdu HITL (etykieta). Nie HERE. Nie FK slownik.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "475_resource_vehicle_profile"
down_revision: str | None = "474_resource_driver_card_no"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "resource",
        sa.Column("vehicle_profile", sa.String(length=64), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("resource", "vehicle_profile")
