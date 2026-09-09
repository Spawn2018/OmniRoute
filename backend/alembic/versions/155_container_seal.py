"""add optional seal_no_1 on container leftover T3

Revision ID: 155_container_seal
Revises: 154_stop_notes
Create Date: 2026-09-09

Opcjonalna pierwsza plomba HITL. Bez sekretu odbioru.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "155_container_seal"
down_revision: str | None = "154_stop_notes"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "container",
        sa.Column("seal_no_1", sa.String(length=32), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("container", "seal_no_1")
