"""allow operator_decision subject_kind margin_floor

Revision ID: 425_od_margin_floor
Revises: 424_handover_note
Create Date: 2026-09-17

N6 leftover S11: decyzja przy breach margin_floor. Nie auto charge. Nie mail.
"""

from collections.abc import Sequence

from alembic import op

revision: str = "425_od_margin_floor"
down_revision: str | None = "424_handover_note"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_NEW = (
    "subject_kind IN ("
    "'inbound_message', 'mail_draft', 'quotation', 'margin_floor')"
)
_OLD = "subject_kind IN ('inbound_message', 'mail_draft', 'quotation')"


def upgrade() -> None:
    op.drop_constraint(
        "ck_operator_decision_subject_kind",
        "operator_decision",
        type_="check",
    )
    op.create_check_constraint(
        "ck_operator_decision_subject_kind",
        "operator_decision",
        _NEW,
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
        _OLD,
    )
