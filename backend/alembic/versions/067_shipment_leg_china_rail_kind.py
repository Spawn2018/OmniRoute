"""widen shipment_leg.leg_kind to road|rail|china_rail

Revision ID: 067_shipment_leg_china_rail_kind
Revises: 066_shipment_leg_rail_kind
Create Date: 2026-09-03

Odcinek kolej z Chin na tej samej tabeli. Nie korytarz. Nie HTTP.
"""

from collections.abc import Sequence

from alembic import op

revision: str = "067_shipment_leg_china_rail_kind"
down_revision: str | None = "066_shipment_leg_rail_kind"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.drop_constraint("ck_shipment_leg_kind", "shipment_leg", type_="check")
    op.create_check_constraint(
        "ck_shipment_leg_kind",
        "shipment_leg",
        "leg_kind IN ('road', 'rail', 'china_rail')",
    )


def downgrade() -> None:
    op.drop_constraint("ck_shipment_leg_kind", "shipment_leg", type_="check")
    op.create_check_constraint(
        "ck_shipment_leg_kind",
        "shipment_leg",
        "leg_kind IN ('road', 'rail')",
    )
