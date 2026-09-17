"""allow operator_decision subject_kind product_ticket

Revision ID: 427_od_product_ticket
Revises: 426_product_ticket
Create Date: 2026-09-17

Plat-HD leftover S11: decyzja właściciela przy owner_ok. Nie auto-fix. Nie Mob.
"""

from collections.abc import Sequence

from alembic import op

revision: str = "427_od_product_ticket"
down_revision: str | None = "426_product_ticket"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_NEW = (
    "subject_kind IN ("
    "'inbound_message', 'mail_draft', 'quotation', 'margin_floor', 'product_ticket')"
)
_OLD = (
    "subject_kind IN ("
    "'inbound_message', 'mail_draft', 'quotation', 'margin_floor')"
)


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
