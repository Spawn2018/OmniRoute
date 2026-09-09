"""widen extraction_draft.draft_kind to tender_rfp

Revision ID: 119_extraction_draft_tender_rfp
Revises: 118_tender_rfp_intake
Create Date: 2026-09-09

HITL RFP: kind na szkicu. Accept (API) zapisuje intake. Nie nowa tabela.
"""

from collections.abc import Sequence

from alembic import op

revision: str = "119_extraction_draft_tender_rfp"
down_revision: str | None = "118_tender_rfp_intake"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.drop_constraint("ck_extraction_draft_kind", "extraction_draft", type_="check")
    op.create_check_constraint(
        "ck_extraction_draft_kind",
        "extraction_draft",
        "draft_kind IN ('rate_line','carrier_quote','tender_rfp')",
    )


def downgrade() -> None:
    op.drop_constraint("ck_extraction_draft_kind", "extraction_draft", type_="check")
    op.create_check_constraint(
        "ck_extraction_draft_kind",
        "extraction_draft",
        "draft_kind IN ('rate_line','carrier_quote')",
    )
