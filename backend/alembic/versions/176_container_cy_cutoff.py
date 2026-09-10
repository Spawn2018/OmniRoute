"""add optional cy_cutoff_at on container leftover T3

Revision ID: 176_container_cy_cutoff
Revises: 175_container_ams_cutoff
Create Date: 2026-09-10

Opcjonalny cutoff CY. Dana HITL ze strefą. Nie live HTTP.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "176_container_cy_cutoff"
down_revision: str | None = "175_container_ams_cutoff"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "container",
        sa.Column("cy_cutoff_at", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("container", "cy_cutoff_at")
