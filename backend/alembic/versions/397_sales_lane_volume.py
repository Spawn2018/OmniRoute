"""add sales_lane volume_label HITL text

Revision ID: 397_sales_lane_volume
Revises: 396_sales_lane_unlocode
Create Date: 2026-09-15

BR6.1 leftover HITL etykieta wolumenu na sales_lane. Nie float. Nie qty.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "397_sales_lane_volume"
down_revision: str | None = "396_sales_lane_unlocode"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "sales_lane",
        sa.Column("volume_label", sa.String(length=64), nullable=True),
    )
    op.execute(
        "UPDATE sales_lane SET volume_label = 'unset' WHERE volume_label IS NULL"
    )
    op.alter_column("sales_lane", "volume_label", nullable=False)
    op.create_check_constraint(
        "ck_sales_lane_volume_label",
        "sales_lane",
        "char_length(btrim(volume_label)) BETWEEN 1 AND 64",
    )


def downgrade() -> None:
    op.drop_constraint("ck_sales_lane_volume_label", "sales_lane", type_="check")
    op.drop_column("sales_lane", "volume_label")
