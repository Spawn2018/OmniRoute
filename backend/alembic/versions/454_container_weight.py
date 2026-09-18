"""add optional weight_kg on container leftover T3

Revision ID: 454_container_weight
Revises: 453_container_quantity
Create Date: 2026-09-18

Opcjonalna waga HITL Decimal. Nie punkt. Nie VGM. Nie float.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "454_container_weight"
down_revision: str | None = "453_container_quantity"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "container",
        sa.Column("weight_kg", sa.Numeric(14, 4), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("container", "weight_kg")
