"""add optional mqc_window on quotation leftover EXP1

Revision ID: 526_quotation_mqc_window
Revises: 525_quotation_mqc_teu
Create Date: 2026-09-25

Opcjonalna etykieta okna HITL. Nie float. Nie MQC SQL. Nie Deadline Engine.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "526_quotation_mqc_window"
down_revision: str | None = "525_quotation_mqc_teu"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "quotation",
        sa.Column("mqc_window", sa.String(64), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("quotation", "mqc_window")
