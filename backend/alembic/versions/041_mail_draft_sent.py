"""allow mail_draft status sent and to_address

Revision ID: 041_mail_draft_sent
Revises: 040_inbound_imap_ingest
Create Date: 2026-09-03

Świadomy mailto po akceptacji. Nie Graph HTTP. Nie auto-send.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "041_mail_draft_sent"
down_revision: str | None = "040_inbound_imap_ingest"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.drop_constraint("ck_mail_draft_status", "mail_draft", type_="check")
    op.create_check_constraint(
        "ck_mail_draft_status",
        "mail_draft",
        "status IN ('draft', 'sent')",
    )
    op.add_column(
        "mail_draft",
        sa.Column("to_address", sa.String(length=320), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("mail_draft", "to_address")
    op.drop_constraint("ck_mail_draft_status", "mail_draft", type_="check")
    op.create_check_constraint(
        "ck_mail_draft_status",
        "mail_draft",
        "status = 'draft'",
    )
