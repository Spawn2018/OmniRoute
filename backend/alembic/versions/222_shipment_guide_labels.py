"""optional plant_label/carrier_label on shipment for CT4 label match

Revision ID: 222_shipment_guide_labels
Revises: 221_routing_guide_match
Create Date: 2026-09-11

HITL etykiety jak ASN — matching lane/mode przy block_409.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "222_shipment_guide_labels"
down_revision: str | None = "221_routing_guide_match"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "shipment",
        sa.Column("plant_label", sa.String(length=128), nullable=True),
    )
    op.add_column(
        "shipment",
        sa.Column("carrier_label", sa.String(length=128), nullable=True),
    )
    op.create_check_constraint(
        "ck_shipment_plant_label",
        "shipment",
        "plant_label IS NULL OR char_length(btrim(plant_label)) BETWEEN 1 AND 128",
    )
    op.create_check_constraint(
        "ck_shipment_carrier_label",
        "shipment",
        "carrier_label IS NULL OR char_length(btrim(carrier_label)) BETWEEN 1 AND 128",
    )


def downgrade() -> None:
    op.drop_constraint("ck_shipment_carrier_label", "shipment", type_="check")
    op.drop_constraint("ck_shipment_plant_label", "shipment", type_="check")
    op.drop_column("shipment", "carrier_label")
    op.drop_column("shipment", "plant_label")
