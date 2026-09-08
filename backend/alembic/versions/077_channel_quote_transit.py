"""add channel_quote.transit_days leftover O1

Revision ID: 077_channel_quote_transit
Revises: 076_entity_event
Create Date: 2026-09-08

Dni kalendarzowe na ofercie. Znaczki liczy SQL, nie kolumny.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "077_channel_quote_transit"
down_revision: str | None = "076_entity_event"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("channel_quote", sa.Column("transit_days", sa.Integer(), nullable=True))
    op.create_check_constraint(
        "ck_channel_quote_transit_days",
        "channel_quote",
        "transit_days IS NULL OR transit_days >= 1",
    )


def downgrade() -> None:
    op.drop_constraint("ck_channel_quote_transit_days", "channel_quote", type_="check")
    op.drop_column("channel_quote", "transit_days")
