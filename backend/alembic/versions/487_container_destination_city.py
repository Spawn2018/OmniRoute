"""add optional destination_city on container

Revision ID: 487_container_destination_city
Revises: 486_container_pod_unlocode
Create Date: 2026-09-21

Opcjonalne miasto docelowe HITL. Nie geokoder. Nie mapa.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "487_container_destination_city"
down_revision: str | None = "486_container_pod_unlocode"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "container",
        sa.Column("destination_city", sa.String(64), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("container", "destination_city")
