"""add bureau_attachment_ref on credit_review

Revision ID: 047_review_bureau_ref
Revises: 046_quote_noted_review
Create Date: 2026-09-03

Wskazanie raportu wywiadowni. Nie auto-limit. Nie nowa kwota.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "047_review_bureau_ref"
down_revision: str | None = "046_quote_noted_review"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "credit_review",
        sa.Column("bureau_attachment_ref", sa.Text(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("credit_review", "bureau_attachment_ref")
