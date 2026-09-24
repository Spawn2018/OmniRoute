"""add optional revision_no on quotation leftover EXP1

Revision ID: 524_quotation_revision_no
Revises: 523_quotation_valid_until
Create Date: 2026-09-25

Opcjonalny numer rewizji HITL. Nie NBP. Nie supersedes_id. Nie float.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "524_quotation_revision_no"
down_revision: str | None = "523_quotation_valid_until"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "quotation",
        sa.Column("revision_no", sa.Integer(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("quotation", "revision_no")
