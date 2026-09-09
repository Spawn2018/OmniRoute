"""add optional seal_no_3 on container leftover T3

Revision ID: 157_container_seal3
Revises: 156_container_seal2
Create Date: 2026-09-09

Opcjonalna trzecia plomba HITL. Bez sekretu odbioru.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "157_container_seal3"
down_revision: str | None = "156_container_seal2"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "container",
        sa.Column("seal_no_3", sa.String(length=32), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("container", "seal_no_3")
