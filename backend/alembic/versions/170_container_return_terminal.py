"""add optional return_terminal on container leftover T3

Revision ID: 170_container_return_terminal
Revises: 169_container_pickup_terminal
Create Date: 2026-09-10

Opcjonalny terminal zwrotu HITL. Bez FK i bez PIN.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "170_container_return_terminal"
down_revision: str | None = "169_container_pickup_terminal"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "container",
        sa.Column("return_terminal", sa.String(length=32), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("container", "return_terminal")
