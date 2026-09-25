"""add optional mqc_teu on quotation leftover EXP1

Revision ID: 525_quotation_mqc_teu
Revises: 524_quotation_revision_no
Create Date: 2026-09-25

Opcjonalny Decimal TEU HITL. Nie float. Nie MQC SQL. Nie mqc_window.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "525_quotation_mqc_teu"
down_revision: str | None = "524_quotation_revision_no"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "quotation",
        sa.Column("mqc_teu", sa.Numeric(14, 4), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("quotation", "mqc_teu")
