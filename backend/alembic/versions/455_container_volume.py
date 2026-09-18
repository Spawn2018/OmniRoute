"""add optional volume_m3 on container leftover T3

Revision ID: 455_container_volume
Revises: 454_container_weight
Create Date: 2026-09-19

Opcjonalna objetosc HITL Decimal. Nie kalkulator CBM. Nie waga. Nie float.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "455_container_volume"
down_revision: str | None = "454_container_weight"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "container",
        sa.Column("volume_m3", sa.Numeric(14, 4), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("container", "volume_m3")
