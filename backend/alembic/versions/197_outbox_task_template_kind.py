"""widen outbox_event kind for task_template_saved

Revision ID: 197_outbox_task_template_kind
Revises: 196_task_template
Create Date: 2026-09-10

Drugi kind outbox T5. Nie nowa tabela. Nie konsument.
"""

from collections.abc import Sequence

from alembic import op

revision: str = "197_outbox_task_template_kind"
down_revision: str | None = "196_task_template"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_NEW = (
    "event_kind IN ('inbound_message_saved','task_template_saved')"
)
_OLD = "event_kind = 'inbound_message_saved'"


def upgrade() -> None:
    op.drop_constraint("ck_outbox_event_kind", "outbox_event", type_="check")
    op.create_check_constraint("ck_outbox_event_kind", "outbox_event", _NEW)


def downgrade() -> None:
    op.drop_constraint("ck_outbox_event_kind", "outbox_event", type_="check")
    op.create_check_constraint("ck_outbox_event_kind", "outbox_event", _OLD)
