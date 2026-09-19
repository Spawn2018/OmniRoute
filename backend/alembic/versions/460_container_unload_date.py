"""add optional unload_date on container leftover T3

Revision ID: 460_container_unload_date
Revises: 459_container_delivery_date
Create Date: 2026-09-19

Opcjonalna data rozładunku HITL. Nie countdown. Nie cutoff. Nie float.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "460_container_unload_date"
down_revision: str | None = "459_container_delivery_date"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "container",
        sa.Column("unload_date", sa.Date(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("container", "unload_date")
