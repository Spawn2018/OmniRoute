"""add optional free_time_dest_h on container leftover T3

Revision ID: 173_container_free_time_dest
Revises: 172_container_free_time_origin
Create Date: 2026-09-10

Opcjonalne godziny wolnego czasu na destination. Dana HITL. Nie PIN.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "173_container_free_time_dest"
down_revision: str | None = "172_container_free_time_origin"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "container",
        sa.Column("free_time_dest_h", sa.Integer(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("container", "free_time_dest_h")
