"""add optional delivery_date on container leftover T3

Revision ID: 459_container_delivery_date
Revises: 458_container_gate_in_date
Create Date: 2026-09-19

Opcjonalna data dostawy HITL. Nie countdown. Nie cutoff. Nie float.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "459_container_delivery_date"
down_revision: str | None = "458_container_gate_in_date"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "container",
        sa.Column("delivery_date", sa.Date(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("container", "delivery_date")
