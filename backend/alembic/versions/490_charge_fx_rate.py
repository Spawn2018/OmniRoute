"""add optional fx_rate override columns on charge

Revision ID: 490_charge_fx_rate
Revises: 489_shipment_tree_margin
Create Date: 2026-09-21

Opcjonalne tokeny kursu per opłata. Nie mnożenie NBP.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "490_charge_fx_rate"
down_revision: str | None = "489_shipment_tree_margin"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("charge", sa.Column("fx_rate_basis", sa.String(32), nullable=True))
    op.add_column("charge", sa.Column("fx_rate_offset_days", sa.String(8), nullable=True))
    op.add_column("charge", sa.Column("fx_rate_table", sa.String(16), nullable=True))
    op.create_check_constraint(
        "ck_charge_fx_rate_basis",
        "charge",
        "fx_rate_basis IS NULL OR fx_rate_basis IN "
        "('etd', 'loading_date', 'unloading_date', 'invoice_date')",
    )
    op.create_check_constraint(
        "ck_charge_fx_rate_offset_days",
        "charge",
        "fx_rate_offset_days IS NULL OR fx_rate_offset_days IN ('0', '-1')",
    )
    op.create_check_constraint(
        "ck_charge_fx_rate_table",
        "charge",
        "fx_rate_table IS NULL OR fx_rate_table IN ('nbp_a', 'nbp_b')",
    )


def downgrade() -> None:
    op.drop_constraint("ck_charge_fx_rate_table", "charge", type_="check")
    op.drop_constraint("ck_charge_fx_rate_offset_days", "charge", type_="check")
    op.drop_constraint("ck_charge_fx_rate_basis", "charge", type_="check")
    op.drop_column("charge", "fx_rate_table")
    op.drop_column("charge", "fx_rate_offset_days")
    op.drop_column("charge", "fx_rate_basis")
