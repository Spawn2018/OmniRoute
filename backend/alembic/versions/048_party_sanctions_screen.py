"""add sanctions screen columns on party

Revision ID: 048_party_sanctions_screen
Revises: 047_review_bureau_ref
Create Date: 2026-09-03

Zapis sprawdzenia listy. Nie auto-match. Nie live HTTP.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "048_party_sanctions_screen"
down_revision: str | None = "047_review_bureau_ref"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "party",
        sa.Column("sanctions_list_ref", sa.Text(), nullable=True),
    )
    op.add_column(
        "party",
        sa.Column("sanctions_checked_at", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("party", "sanctions_checked_at")
    op.drop_column("party", "sanctions_list_ref")
