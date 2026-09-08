"""add expected_buy snapshot on trip

Revision ID: 107_trip_expected_buy
Revises: 106_local_charge
Create Date: 2026-09-08

Snapshot kosztu kupna przy in_transit. Nie wariancja. Nie km.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "107_trip_expected_buy"
down_revision: str | None = "106_local_charge"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "trip",
        sa.Column("expected_buy_amount", sa.Numeric(14, 4), nullable=True),
    )
    op.add_column(
        "trip",
        sa.Column("expected_buy_currency", sa.CHAR(length=3), nullable=True),
    )
    op.create_check_constraint(
        "ck_trip_expected_buy_freeze",
        "trip",
        "("
        "(status IN ('in_transit', 'completed') "
        "AND expected_buy_amount IS NOT NULL AND expected_buy_amount > 0 "
        "AND expected_buy_currency ~ '^[A-Z]{3}$') "
        "OR "
        "(status IN ('draft', 'planned', 'cancelled') "
        "AND expected_buy_amount IS NULL AND expected_buy_currency IS NULL)"
        ")",
    )


def downgrade() -> None:
    op.drop_constraint("ck_trip_expected_buy_freeze", "trip", type_="check")
    op.drop_column("trip", "expected_buy_currency")
    op.drop_column("trip", "expected_buy_amount")
