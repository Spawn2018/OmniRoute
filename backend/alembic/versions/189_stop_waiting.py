"""add optional waiting_free_minutes on stop leftover T1 EXP1

Revision ID: 189_stop_waiting
Revises: 188_stop_appointment_ref
Create Date: 2026-09-10

Opcjonalne minuty wolnego oczekiwania HITL. Nie odliczanie. Nie POD. Nie nowa tabela.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "189_stop_waiting"
down_revision: str | None = "188_stop_appointment_ref"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "stop",
        sa.Column("waiting_free_minutes", sa.Integer(), nullable=True),
    )
    op.create_check_constraint(
        "ck_stop_waiting_free",
        "stop",
        "waiting_free_minutes IS NULL OR waiting_free_minutes >= 0",
    )


def downgrade() -> None:
    op.drop_constraint("ck_stop_waiting_free", "stop", type_="check")
    op.drop_column("stop", "waiting_free_minutes")
