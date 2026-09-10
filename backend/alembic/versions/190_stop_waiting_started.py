"""add optional waiting_started_at on stop leftover T1 EXP1

Revision ID: 190_stop_waiting_started
Revises: 189_stop_waiting
Create Date: 2026-09-10

Opcjonalny start oczekiwania HITL. Nie odliczanie. Nie POD. Nie nowa tabela.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "190_stop_waiting_started"
down_revision: str | None = "189_stop_waiting"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "stop",
        sa.Column("waiting_started_at", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("stop", "waiting_started_at")
