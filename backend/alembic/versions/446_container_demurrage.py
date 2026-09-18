"""add optional demurrage_free_days on container leftover V3

Revision ID: 446_container_demurrage
Revises: 445_blank_sailing_mark
Create Date: 2026-09-18

Opcjonalne dni demurrage HITL. Dana w dniach. Nie odliczanie. Nie charge.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "446_container_demurrage"
down_revision: str | None = "445_blank_sailing_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "container",
        sa.Column("demurrage_free_days", sa.Integer(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("container", "demurrage_free_days")
