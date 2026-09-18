"""add optional detention_free_days on container leftover V3

Revision ID: 447_container_detention
Revises: 446_container_demurrage
Create Date: 2026-09-18

Opcjonalne dni detention HITL. Dana w dniach. Nie odliczanie. Nie charge.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "447_container_detention"
down_revision: str | None = "446_container_demurrage"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "container",
        sa.Column("detention_free_days", sa.Integer(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("container", "detention_free_days")
