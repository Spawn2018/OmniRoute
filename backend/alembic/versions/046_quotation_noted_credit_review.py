"""add noted_credit_review_id on quotation

Revision ID: 046_quote_noted_review
Revises: 045_operator_decision_quotation
Create Date: 2026-09-03

Wskazanie recenzji. Nie scoring. Nie nowa kwota.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "046_quote_noted_review"
down_revision: str | None = "045_operator_decision_quotation"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "quotation",
        sa.Column(
            "noted_credit_review_id",
            postgresql.UUID(as_uuid=True),
            nullable=True,
        ),
    )
    op.create_index(
        "ix_quotation_org_noted_credit_review",
        "quotation",
        ["organization_id", "noted_credit_review_id"],
    )


def downgrade() -> None:
    op.drop_index("ix_quotation_org_noted_credit_review", table_name="quotation")
    op.drop_column("quotation", "noted_credit_review_id")
