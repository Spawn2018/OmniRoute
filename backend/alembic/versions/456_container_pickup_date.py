"""add optional pickup_date on container leftover T3

Revision ID: 456_container_pickup_date
Revises: 455_container_volume
Create Date: 2026-09-19

Opcjonalna data odbioru HITL. Nie countdown. Nie cutoff. Nie float.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "456_container_pickup_date"
down_revision: str | None = "455_container_volume"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "container",
        sa.Column("pickup_date", sa.Date(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("container", "pickup_date")
