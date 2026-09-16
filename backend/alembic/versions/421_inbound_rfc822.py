"""add optional rfc822 headers on inbound_message leftover O8

Revision ID: 421_inbound_rfc822
Revises: 420_trip_bill_mark
Create Date: 2026-09-16

HITL Message-ID / In-Reply-To. Nie Graph parse. Nie drugi czat.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "421_inbound_rfc822"
down_revision: str | None = "420_trip_bill_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "inbound_message",
        sa.Column("rfc822_message_id", sa.String(length=512), nullable=True),
    )
    op.add_column(
        "inbound_message",
        sa.Column("in_reply_to", sa.String(length=512), nullable=True),
    )
    op.create_index(
        "ix_inbound_message_org_rfc822",
        "inbound_message",
        ["organization_id", "rfc822_message_id"],
        unique=False,
        postgresql_where=sa.text("rfc822_message_id IS NOT NULL"),
    )


def downgrade() -> None:
    op.drop_index("ix_inbound_message_org_rfc822", table_name="inbound_message")
    op.drop_column("inbound_message", "in_reply_to")
    op.drop_column("inbound_message", "rfc822_message_id")
