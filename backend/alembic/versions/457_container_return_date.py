"""add optional return_date on container leftover T3

Revision ID: 457_container_return_date
Revises: 456_container_pickup_date
Create Date: 2026-09-19

Opcjonalna data zwrotu HITL. Nie countdown. Nie cutoff. Nie float.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "457_container_return_date"
down_revision: str | None = "456_container_pickup_date"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "container",
        sa.Column("return_date", sa.Date(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("container", "return_date")
