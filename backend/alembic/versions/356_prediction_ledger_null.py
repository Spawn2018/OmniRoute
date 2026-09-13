"""prediction_ledger: crps and mae nullable

Revision ID: 356_prediction_ledger_null
Revises: 355_version_window
Create Date: 2026-09-13

AI2 leftover. Nowy INSERT bez wpisanej metryki. Stare wiersze zostaja.
"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "356_prediction_ledger_null"
down_revision: str | None = "355_version_window"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.alter_column(
        "prediction_ledger",
        "crps",
        existing_type=sa.Numeric(14, 4),
        nullable=True,
    )
    op.alter_column(
        "prediction_ledger",
        "mae",
        existing_type=sa.Numeric(14, 4),
        nullable=True,
    )


def downgrade() -> None:
    op.alter_column(
        "prediction_ledger",
        "mae",
        existing_type=sa.Numeric(14, 4),
        nullable=False,
    )
    op.alter_column(
        "prediction_ledger",
        "crps",
        existing_type=sa.Numeric(14, 4),
        nullable=False,
    )
