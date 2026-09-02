"""add inbound_message.party_id with same-tenant FK

Revision ID: 027_inbound_message_party
Revises: 026_inbound_message_rls
Create Date: 2026-09-02
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "027_inbound_message_party"
down_revision: str | None = "026_inbound_message_rls"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "inbound_message",
        sa.Column("party_id", postgresql.UUID(as_uuid=True), nullable=True),
    )
    op.create_foreign_key(
        "fk_inbound_message_party",
        "inbound_message",
        "party",
        ["organization_id", "party_id"],
        ["organization_id", "id"],
        ondelete="RESTRICT",
    )
    op.create_index("ix_inbound_message_party_id", "inbound_message", ["party_id"])


def downgrade() -> None:
    op.drop_index("ix_inbound_message_party_id", table_name="inbound_message")
    op.drop_constraint("fk_inbound_message_party", "inbound_message", type_="foreignkey")
    op.drop_column("inbound_message", "party_id")
