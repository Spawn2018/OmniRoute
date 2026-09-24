"""add allotment_teu on rate_line leftover EXP1

Revision ID: 518_rate_line_allotment
Revises: 517_cargo_claim_evidence
Create Date: 2026-09-24

HITL opcjonalny Decimal TEU. Nie matching. Nie float. Nie druga marża.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "518_rate_line_allotment"
down_revision: str | None = "517_cargo_claim_evidence"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "rate_line",
        sa.Column("allotment_teu", sa.Numeric(14, 4), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("rate_line", "allotment_teu")
