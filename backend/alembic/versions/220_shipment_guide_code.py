"""add optional shipment.guide_code for CT4 block_409

Revision ID: 220_shipment_guide_code
Revises: 219_asn_guide_code
Create Date: 2026-09-11

HITL guide_code na shipment. Nie matching lane/mode.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "220_shipment_guide_code"
down_revision: str | None = "219_asn_guide_code"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "shipment",
        sa.Column("guide_code", sa.String(length=32), nullable=True),
    )
    op.create_check_constraint(
        "ck_shipment_guide_code",
        "shipment",
        "guide_code IS NULL OR guide_code ~ '^[a-z][a-z0-9_]{1,31}$'",
    )


def downgrade() -> None:
    op.drop_constraint("ck_shipment_guide_code", "shipment", type_="check")
    op.drop_column("shipment", "guide_code")
