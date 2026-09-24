"""add optional valid_until on quotation leftover EXP1

Revision ID: 523_quotation_valid_until
Revises: 522_rate_line_fuel_index_id
Create Date: 2026-09-24

Opcjonalna data ważności HITL. Nie NBP. Nie Deadline Engine. Nie float.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "523_quotation_valid_until"
down_revision: str | None = "522_rate_line_fuel_index_id"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "quotation",
        sa.Column("valid_until", sa.Date(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("quotation", "valid_until")
