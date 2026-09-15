"""add sales_lane origin/destination UN/LOCODE

Revision ID: 396_sales_lane_unlocode
Revises: 395_crm_pipeline_mark
Create Date: 2026-09-15

BR6.1 leftover HITL para miejsc na sales_lane. Nie FK port. Nie km.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "396_sales_lane_unlocode"
down_revision: str | None = "395_crm_pipeline_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_CODE = r"^[A-Z]{2}[A-Z0-9]{3}$"


def upgrade() -> None:
    op.add_column(
        "sales_lane",
        sa.Column("origin_unlocode", sa.String(length=5), nullable=True),
    )
    op.add_column(
        "sales_lane",
        sa.Column("destination_unlocode", sa.String(length=5), nullable=True),
    )
    op.execute(
        "UPDATE sales_lane SET origin_unlocode = 'PLGDN', "
        "destination_unlocode = 'DEHAM' "
        "WHERE origin_unlocode IS NULL OR destination_unlocode IS NULL"
    )
    op.alter_column("sales_lane", "origin_unlocode", nullable=False)
    op.alter_column("sales_lane", "destination_unlocode", nullable=False)
    op.create_check_constraint(
        "ck_sales_lane_origin_unlocode",
        "sales_lane",
        f"origin_unlocode ~ '{_CODE}'",
    )
    op.create_check_constraint(
        "ck_sales_lane_destination_unlocode",
        "sales_lane",
        f"destination_unlocode ~ '{_CODE}'",
    )
    op.create_check_constraint(
        "ck_sales_lane_unlocode_pair",
        "sales_lane",
        "origin_unlocode <> destination_unlocode",
    )


def downgrade() -> None:
    op.drop_constraint("ck_sales_lane_unlocode_pair", "sales_lane", type_="check")
    op.drop_constraint(
        "ck_sales_lane_destination_unlocode",
        "sales_lane",
        type_="check",
    )
    op.drop_constraint("ck_sales_lane_origin_unlocode", "sales_lane", type_="check")
    op.drop_column("sales_lane", "destination_unlocode")
    op.drop_column("sales_lane", "origin_unlocode")
