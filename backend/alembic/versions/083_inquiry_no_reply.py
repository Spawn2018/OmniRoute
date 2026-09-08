"""carrier_inquiry no_reply_after and notice kind leftover N5

Revision ID: 083_inquiry_no_reply
Revises: 082_extraction_draft_kind
Create Date: 2026-09-08

Data ciszy. Nie U4. Nie auto-send.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "083_inquiry_no_reply"
down_revision: str | None = "082_extraction_draft_kind"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "carrier_inquiry",
        sa.Column("no_reply_after", sa.Date(), nullable=True),
    )
    op.drop_constraint("ck_operator_notice_kind", "operator_notice", type_="check")
    op.create_check_constraint(
        "ck_operator_notice_kind",
        "operator_notice",
        "kind IN ('manual','no_reply')",
    )


def downgrade() -> None:
    op.drop_constraint("ck_operator_notice_kind", "operator_notice", type_="check")
    op.create_check_constraint(
        "ck_operator_notice_kind",
        "operator_notice",
        "kind = 'manual'",
    )
    op.drop_column("carrier_inquiry", "no_reply_after")
