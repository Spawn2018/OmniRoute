"""expand carrier_inquiry statuses lane and answered quote leftover O3

Revision ID: 078_carrier_inquiry_batch
Revises: 077_channel_quote_transit
Create Date: 2026-09-08

Statusy Fali O. Lane POL/POD. Kwota tylko przy answered. Nie send.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "078_carrier_inquiry_batch"
down_revision: str | None = "077_channel_quote_transit"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_STATUSES = (
    "status IN ('draft','queued','sent','answered','declined')"
)
_ANSWERED = (
    "(status = 'answered' AND quoted_amount IS NOT NULL "
    "AND quoted_currency IS NOT NULL) OR "
    "(status <> 'answered' AND quoted_amount IS NULL "
    "AND quoted_currency IS NULL AND quoted_transit_days IS NULL)"
)


def upgrade() -> None:
    op.drop_constraint("ck_carrier_inquiry_status_draft", "carrier_inquiry", type_="check")
    op.add_column(
        "carrier_inquiry",
        sa.Column("origin_port_id", postgresql.UUID(as_uuid=True), nullable=True),
    )
    op.add_column(
        "carrier_inquiry",
        sa.Column("destination_port_id", postgresql.UUID(as_uuid=True), nullable=True),
    )
    op.add_column(
        "carrier_inquiry",
        sa.Column("quoted_amount", sa.Numeric(14, 4), nullable=True),
    )
    op.add_column(
        "carrier_inquiry",
        sa.Column("quoted_currency", sa.CHAR(length=3), nullable=True),
    )
    op.add_column(
        "carrier_inquiry",
        sa.Column("quoted_transit_days", sa.Integer(), nullable=True),
    )
    op.create_check_constraint("ck_carrier_inquiry_status", "carrier_inquiry", _STATUSES)
    op.create_check_constraint("ck_carrier_inquiry_answered_quote", "carrier_inquiry", _ANSWERED)
    op.create_check_constraint(
        "ck_carrier_inquiry_transit",
        "carrier_inquiry",
        "quoted_transit_days IS NULL OR quoted_transit_days >= 1",
    )
    op.create_foreign_key(
        "fk_carrier_inquiry_origin_port",
        "carrier_inquiry",
        "port",
        ["organization_id", "origin_port_id"],
        ["organization_id", "id"],
        ondelete="RESTRICT",
    )
    op.create_foreign_key(
        "fk_carrier_inquiry_destination_port",
        "carrier_inquiry",
        "port",
        ["organization_id", "destination_port_id"],
        ["organization_id", "id"],
        ondelete="RESTRICT",
    )


def downgrade() -> None:
    op.drop_constraint("fk_carrier_inquiry_destination_port", "carrier_inquiry", type_="foreignkey")
    op.drop_constraint("fk_carrier_inquiry_origin_port", "carrier_inquiry", type_="foreignkey")
    op.drop_constraint("ck_carrier_inquiry_transit", "carrier_inquiry", type_="check")
    op.drop_constraint("ck_carrier_inquiry_answered_quote", "carrier_inquiry", type_="check")
    op.drop_constraint("ck_carrier_inquiry_status", "carrier_inquiry", type_="check")
    op.drop_column("carrier_inquiry", "quoted_transit_days")
    op.drop_column("carrier_inquiry", "quoted_currency")
    op.drop_column("carrier_inquiry", "quoted_amount")
    op.drop_column("carrier_inquiry", "destination_port_id")
    op.drop_column("carrier_inquiry", "origin_port_id")
    op.create_check_constraint(
        "ck_carrier_inquiry_status_draft",
        "carrier_inquiry",
        "status = 'draft'",
    )
