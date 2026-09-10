"""add optional si_cutoff_at on container leftover T3

Revision ID: 174_container_si_cutoff
Revises: 173_container_free_time_dest
Create Date: 2026-09-10

Opcjonalny cutoff instrukcji SI. Dana HITL ze strefą. Nie live HTTP.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "174_container_si_cutoff"
down_revision: str | None = "173_container_free_time_dest"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "container",
        sa.Column("si_cutoff_at", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("container", "si_cutoff_at")
