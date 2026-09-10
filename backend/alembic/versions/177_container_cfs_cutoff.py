"""add optional cfs_cutoff_at on container leftover T3

Revision ID: 177_container_cfs_cutoff
Revises: 176_container_cy_cutoff
Create Date: 2026-09-10

Opcjonalny cutoff CFS. Dana HITL ze strefą. Nie live HTTP.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "177_container_cfs_cutoff"
down_revision: str | None = "176_container_cy_cutoff"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "container",
        sa.Column("cfs_cutoff_at", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("container", "cfs_cutoff_at")
