"""add marine_pollutant on dangerous_good leftover EXP0.9

Revision ID: 515_dg_marine_pollutant
Revises: 514_dangerous_good_packing_group
Create Date: 2026-09-23

HITL zanieczyszczenie morza bool. LLM nie nadaje klasy. Nie live IMO.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "515_dg_marine_pollutant"
down_revision: str | None = "514_dangerous_good_packing_group"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "dangerous_good",
        sa.Column("marine_pollutant", sa.Boolean(), nullable=True),
    )
    op.execute(
        """
        UPDATE dangerous_good SET marine_pollutant = false
        WHERE marine_pollutant IS NULL
        """
    )
    op.alter_column("dangerous_good", "marine_pollutant", nullable=False)


def downgrade() -> None:
    op.drop_column("dangerous_good", "marine_pollutant")
