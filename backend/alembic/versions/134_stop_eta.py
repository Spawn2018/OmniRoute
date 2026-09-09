"""add HITL eta clocks on stop leftover V2

Revision ID: 134_stop_eta
Revises: 133_prediction_ledger
Create Date: 2026-09-09

HITL eta_physical + eta_legal. Nie GPS. Nie pogoda. Nie silnik ETA.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "134_stop_eta"
down_revision: str | None = "133_prediction_ledger"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "stop",
        sa.Column("eta_physical", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        "stop",
        sa.Column("eta_legal", sa.DateTime(timezone=True), nullable=True),
    )
    op.execute(
        """
        UPDATE stop SET
            eta_physical = created_at,
            eta_legal = created_at
        WHERE eta_physical IS NULL
        """
    )
    op.alter_column("stop", "eta_physical", nullable=False)
    op.alter_column("stop", "eta_legal", nullable=False)


def downgrade() -> None:
    op.drop_column("stop", "eta_legal")
    op.drop_column("stop", "eta_physical")
