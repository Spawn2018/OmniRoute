"""add optional mixed_dd_days on container leftover V3

Revision ID: 448_container_mixed_dd
Revises: 447_container_detention
Create Date: 2026-09-18

Opcjonalne dni mixed D&D HITL. Dana w dniach. Nie odliczanie. Nie charge.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "448_container_mixed_dd"
down_revision: str | None = "447_container_detention"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "container",
        sa.Column("mixed_dd_days", sa.Integer(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("container", "mixed_dd_days")
