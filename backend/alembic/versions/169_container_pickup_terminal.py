"""add optional pickup_terminal on container leftover T3

Revision ID: 169_container_pickup_terminal
Revises: 168_container_reefer
Create Date: 2026-09-10

Opcjonalny terminal pobrania HITL. Bez FK i bez PIN.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "169_container_pickup_terminal"
down_revision: str | None = "168_container_reefer"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "container",
        sa.Column("pickup_terminal", sa.String(length=32), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("container", "pickup_terminal")
