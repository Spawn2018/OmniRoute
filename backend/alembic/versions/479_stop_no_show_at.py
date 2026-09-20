"""add optional no_show_at on stop leftover T1 EXP1

Revision ID: 479_stop_no_show_at
Revises: 478_stop_appointment_status
Create Date: 2026-09-20

Opcjonalna chwila niestawiennictwa HITL. Nie szkic marży. Nie auto-status. Nie nowa tabela.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "479_stop_no_show_at"
down_revision: str | None = "478_stop_appointment_status"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "stop",
        sa.Column("no_show_at", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("stop", "no_show_at")
