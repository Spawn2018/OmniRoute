"""add limited_quantity on dangerous_good leftover EXP0.9

Revision ID: 516_dg_limited_quantity
Revises: 515_dg_marine_pollutant
Create Date: 2026-09-24

HITL limited quantity bool. LLM nie nadaje klasy. Nie live IMO.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "516_dg_limited_quantity"
down_revision: str | None = "515_dg_marine_pollutant"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "dangerous_good",
        sa.Column("limited_quantity", sa.Boolean(), nullable=True),
    )
    op.execute(
        """
        UPDATE dangerous_good SET limited_quantity = false
        WHERE limited_quantity IS NULL
        """
    )
    op.alter_column("dangerous_good", "limited_quantity", nullable=False)


def downgrade() -> None:
    op.drop_column("dangerous_good", "limited_quantity")
