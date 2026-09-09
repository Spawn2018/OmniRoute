"""add optional hawb_no and mawb_no on air shipment_leg leftover U3b

Revision ID: 149_shipment_leg_air_waybill
Revises: 148_local_charge_iso
Create Date: 2026-09-09

Opcjonalny numer HAWB/MAWB jako dana. Bez puli M-03. Bez IATA HTTP.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "149_shipment_leg_air_waybill"
down_revision: str | None = "148_local_charge_iso"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "shipment_leg",
        sa.Column("hawb_no", sa.String(length=32), nullable=True),
    )
    op.add_column(
        "shipment_leg",
        sa.Column("mawb_no", sa.String(length=32), nullable=True),
    )
    op.create_check_constraint(
        "ck_shipment_leg_hawb_no",
        "shipment_leg",
        "hawb_no IS NULL OR hawb_no ~ '^[A-Za-z0-9-]{2,32}$'",
    )
    op.create_check_constraint(
        "ck_shipment_leg_mawb_no",
        "shipment_leg",
        "mawb_no IS NULL OR mawb_no ~ '^[A-Za-z0-9-]{2,32}$'",
    )
    op.create_check_constraint(
        "ck_shipment_leg_air_waybill",
        "shipment_leg",
        "(hawb_no IS NULL AND mawb_no IS NULL) OR leg_kind = 'air'",
    )
    op.create_unique_constraint(
        "uq_shipment_leg_org_hawb",
        "shipment_leg",
        ["organization_id", "hawb_no"],
    )
    op.create_unique_constraint(
        "uq_shipment_leg_org_mawb",
        "shipment_leg",
        ["organization_id", "mawb_no"],
    )


def downgrade() -> None:
    op.drop_constraint("uq_shipment_leg_org_mawb", "shipment_leg", type_="unique")
    op.drop_constraint("uq_shipment_leg_org_hawb", "shipment_leg", type_="unique")
    op.drop_constraint("ck_shipment_leg_air_waybill", "shipment_leg", type_="check")
    op.drop_constraint("ck_shipment_leg_mawb_no", "shipment_leg", type_="check")
    op.drop_constraint("ck_shipment_leg_hawb_no", "shipment_leg", type_="check")
    op.drop_column("shipment_leg", "mawb_no")
    op.drop_column("shipment_leg", "hawb_no")
