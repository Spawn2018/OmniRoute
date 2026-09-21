"""add optional grade on container leftover T3 EXP1

Revision ID: 482_container_grade
Revises: 481_stop_weigh_out
Create Date: 2026-09-21

Opcjonalny stopien HITL (tekst). Nie lista branzy. Nie VGM.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "482_container_grade"
down_revision: str | None = "481_stop_weigh_out"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "container",
        sa.Column("grade", sa.String(32), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("container", "grade")
