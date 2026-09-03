"""widen shipment_leg.leg_kind to include ocean_lcl

Revision ID: 068_shipment_leg_ocean_lcl_kind
Revises: 067_shipment_leg_china_rail_kind
Create Date: 2026-09-04

Odcinek drobnicy morskiej na tej samej tabeli. Nie CFS. Nie CBM.
"""

from collections.abc import Sequence

from alembic import op

revision: str = "068_shipment_leg_ocean_lcl_kind"
down_revision: str | None = "067_shipment_leg_china_rail_kind"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.drop_constraint("ck_shipment_leg_kind", "shipment_leg", type_="check")
    op.create_check_constraint(
        "ck_shipment_leg_kind",
        "shipment_leg",
        "leg_kind IN ('road', 'rail', 'china_rail', 'ocean_lcl')",
    )


def downgrade() -> None:
    op.drop_constraint("ck_shipment_leg_kind", "shipment_leg", type_="check")
    op.create_check_constraint(
        "ck_shipment_leg_kind",
        "shipment_leg",
        "leg_kind IN ('road', 'rail', 'china_rail')",
    )
