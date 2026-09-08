"""add extraction_draft.draft_kind leftover O6

Revision ID: 082_extraction_draft_kind
Revises: 081_party_lane_scorecard
Create Date: 2026-09-08

rate_line | carrier_quote. Stare wiersze = rate_line. Nie F10.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "082_extraction_draft_kind"
down_revision: str | None = "081_party_lane_scorecard"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "extraction_draft",
        sa.Column(
            "draft_kind",
            sa.String(length=32),
            nullable=False,
            server_default="rate_line",
        ),
    )
    op.create_check_constraint(
        "ck_extraction_draft_kind",
        "extraction_draft",
        "draft_kind IN ('rate_line','carrier_quote')",
    )


def downgrade() -> None:
    op.drop_constraint("ck_extraction_draft_kind", "extraction_draft", type_="check")
    op.drop_column("extraction_draft", "draft_kind")
