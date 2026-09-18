"""add optional quantity on container leftover T3

Revision ID: 453_container_quantity
Revises: 452_container_teu
Create Date: 2026-09-18

Opcjonalna ilość HITL Integer. Nie kolumna punktu. Nie TEU. Nie float.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "453_container_quantity"
down_revision: str | None = "452_container_teu"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "container",
        sa.Column("quantity", sa.Integer(), nullable=True),
    )
    op.create_check_constraint(
        "ck_container_quantity",
        "container",
        "quantity IS NULL OR quantity >= 0",
    )


def downgrade() -> None:
    op.drop_constraint("ck_container_quantity", "container", type_="check")
    op.drop_column("container", "quantity")
