"""add optional alliance_service on container leftover T3 EXP1

Revision ID: 484_container_alliance_service
Revises: 483_container_vessel_imo
Create Date: 2026-09-21

Opcjonalna etykieta aliansu HITL (tekst). Nie live alliance. Nie HTTP.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "484_container_alliance_service"
down_revision: str | None = "483_container_vessel_imo"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "container",
        sa.Column("alliance_service", sa.String(32), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("container", "alliance_service")
