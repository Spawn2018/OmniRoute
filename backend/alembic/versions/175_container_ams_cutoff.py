"""add optional ams_cutoff_at on container leftover T3

Revision ID: 175_container_ams_cutoff
Revises: 174_container_si_cutoff
Create Date: 2026-09-10

Opcjonalny cutoff AMS. Dana HITL ze strefą. Nie live HTTP.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "175_container_ams_cutoff"
down_revision: str | None = "174_container_si_cutoff"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "container",
        sa.Column("ams_cutoff_at", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("container", "ams_cutoff_at")
