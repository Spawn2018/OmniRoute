"""widen shipment_leg.leg_kind to include air

Revision ID: 094_shipment_leg_air_kind
Revises: 093_container
Create Date: 2026-09-08

Odcinek lotniczy na tej samej tabeli. Nie list przewozowy.
"""

from collections.abc import Sequence

from alembic import op

revision: str = "094_shipment_leg_air_kind"
down_revision: str | None = "093_container"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.drop_constraint("ck_shipment_leg_kind", "shipment_leg", type_="check")
    op.create_check_constraint(
        "ck_shipment_leg_kind",
        "shipment_leg",
        "leg_kind IN ('road', 'rail', 'china_rail', 'ocean_lcl', 'air')",
    )


def downgrade() -> None:
    op.drop_constraint("ck_shipment_leg_kind", "shipment_leg", type_="check")
    op.create_check_constraint(
        "ck_shipment_leg_kind",
        "shipment_leg",
        "leg_kind IN ('road', 'rail', 'china_rail', 'ocean_lcl')",
    )
