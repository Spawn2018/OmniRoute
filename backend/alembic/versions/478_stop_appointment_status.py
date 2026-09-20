"""add optional appointment_status on stop leftover T1 EXP1

Revision ID: 478_stop_appointment_status
Revises: 477_stop_group_bind
Create Date: 2026-09-20

Opcjonalny status awizacji HITL na punkcie. Nie dok. Nie no_show_at. Nie nowa tabela.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "478_stop_appointment_status"
down_revision: str | None = "477_stop_group_bind"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "stop",
        sa.Column("appointment_status", sa.String(length=16), nullable=True),
    )
    op.create_check_constraint(
        "ck_stop_appointment_status",
        "stop",
        "appointment_status IS NULL OR appointment_status IN "
        "('noted', 'advised', 'confirmed', 'cancelled')",
    )


def downgrade() -> None:
    op.drop_constraint("ck_stop_appointment_status", "stop", type_="check")
    op.drop_column("stop", "appointment_status")
