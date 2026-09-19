"""add optional temp_max on container leftover T3

Revision ID: 462_container_temp_max
Revises: 461_container_temp_min
Create Date: 2026-09-19

Opcjonalna temperatura max HITL Decimal. Nie float. Nie zasilanie.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "462_container_temp_max"
down_revision: str | None = "461_container_temp_min"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "container",
        sa.Column("temp_max", sa.Numeric(14, 4), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("container", "temp_max")
