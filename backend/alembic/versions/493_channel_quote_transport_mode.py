"""add transport_mode on channel_quote for air e-rates

Revision ID: 493_channel_quote_transport_mode
Revises: 492_charge_sell_in_pln
Create Date: 2026-09-22

U3 leftover e-rates. air wymaga lotniska w API/serwisie. Nie live IATA.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "493_channel_quote_transport_mode"
down_revision: str | None = "492_charge_sell_in_pln"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "channel_quote",
        sa.Column(
            "transport_mode",
            sa.String(length=16),
            nullable=False,
            server_default="other",
        ),
    )
    op.create_check_constraint(
        "ck_channel_quote_transport_mode",
        "channel_quote",
        "transport_mode IN ('air', 'other')",
    )
    op.drop_constraint("uq_channel_quote_org_lane_day", "channel_quote", type_="unique")
    op.create_unique_constraint(
        "uq_channel_quote_org_lane_day_mode",
        "channel_quote",
        [
            "organization_id",
            "party_id",
            "origin_port_id",
            "destination_port_id",
            "quote_date",
            "transport_mode",
        ],
    )
    op.alter_column("channel_quote", "transport_mode", server_default=None)


def downgrade() -> None:
    op.drop_constraint("uq_channel_quote_org_lane_day_mode", "channel_quote", type_="unique")
    op.create_unique_constraint(
        "uq_channel_quote_org_lane_day",
        "channel_quote",
        [
            "organization_id",
            "party_id",
            "origin_port_id",
            "destination_port_id",
            "quote_date",
        ],
    )
    op.drop_constraint("ck_channel_quote_transport_mode", "channel_quote", type_="check")
    op.drop_column("channel_quote", "transport_mode")
