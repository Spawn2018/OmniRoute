"""add optional temp_min on container leftover T3

Revision ID: 461_container_temp_min
Revises: 460_container_unload_date
Create Date: 2026-09-19

Opcjonalna temperatura min HITL Decimal. Nie float. Nie druga kolumna max.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "461_container_temp_min"
down_revision: str | None = "460_container_unload_date"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "container",
        sa.Column("temp_min", sa.Numeric(14, 4), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("container", "temp_min")
