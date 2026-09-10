"""add optional appointment_ref on stop leftover T1 EXP1

Revision ID: 188_stop_appointment_ref
Revises: 187_stop_seal_out
Create Date: 2026-09-10

Opcjonalny numer awizacji HITL. Nie okno doku. Nie waiting. Nie nowa tabela.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "188_stop_appointment_ref"
down_revision: str | None = "187_stop_seal_out"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "stop",
        sa.Column("appointment_ref", sa.String(length=32), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("stop", "appointment_ref")
