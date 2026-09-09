"""add optional seal_no_2 on container leftover T3

Revision ID: 156_container_seal2
Revises: 155_container_seal
Create Date: 2026-09-09

Opcjonalna druga plomba HITL. Bez sekretu odbioru.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "156_container_seal2"
down_revision: str | None = "155_container_seal"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "container",
        sa.Column("seal_no_2", sa.String(length=32), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("container", "seal_no_2")
