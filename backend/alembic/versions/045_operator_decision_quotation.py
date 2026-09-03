"""allow operator_decision subject_kind quotation

Revision ID: 045_operator_decision_quotation
Revises: 044_quotation_negotiated_channel
Create Date: 2026-09-03

Accept oferty przez S11. Nie etykieta wyniku po angielsku. Nie accept extractu.
"""

from collections.abc import Sequence

from alembic import op

revision: str = "045_operator_decision_quotation"
down_revision: str | None = "044_quotation_negotiated_channel"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.drop_constraint(
        "ck_operator_decision_subject_kind",
        "operator_decision",
        type_="check",
    )
    op.create_check_constraint(
        "ck_operator_decision_subject_kind",
        "operator_decision",
        "subject_kind IN ('inbound_message', 'mail_draft', 'quotation')",
    )


def downgrade() -> None:
    op.drop_constraint(
        "ck_operator_decision_subject_kind",
        "operator_decision",
        type_="check",
    )
    op.create_check_constraint(
        "ck_operator_decision_subject_kind",
        "operator_decision",
        "subject_kind IN ('inbound_message', 'mail_draft')",
    )
