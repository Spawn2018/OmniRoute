"""add optional pol_unlocode on container

Revision ID: 485_container_pol_unlocode
Revises: 484_container_alliance_service
Create Date: 2026-09-21

Opcjonalny UN/LOCODE portu załadunku HITL. Nie FK portu. Nie mapa.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "485_container_pol_unlocode"
down_revision: str | None = "484_container_alliance_service"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "container",
        sa.Column("pol_unlocode", sa.String(5), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("container", "pol_unlocode")
