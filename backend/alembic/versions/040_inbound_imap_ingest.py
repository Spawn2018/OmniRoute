"""allow imap:// ingest on inbound_message

Revision ID: 040_inbound_imap_ingest
Revises: 039_outbox_event_rls
Create Date: 2026-09-03

Ingest skrzynki na tej samej tabeli. Nie live IMAP. Nie send.
"""

from collections.abc import Sequence

from alembic import op

revision: str = "040_inbound_imap_ingest"
down_revision: str | None = "039_outbox_event_rls"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.drop_constraint(
        "ck_inbound_message_source_fixture",
        "inbound_message",
        type_="check",
    )
    op.create_check_constraint(
        "ck_inbound_message_source_fixture",
        "inbound_message",
        "source_ref ~ '^(fixture|synth|graph|imap)://'",
    )


def downgrade() -> None:
    op.drop_constraint(
        "ck_inbound_message_source_fixture",
        "inbound_message",
        type_="check",
    )
    op.create_check_constraint(
        "ck_inbound_message_source_fixture",
        "inbound_message",
        "source_ref ~ '^(fixture|synth|graph)://'",
    )
