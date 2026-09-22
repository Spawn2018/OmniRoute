"""optional volume_m3 on groupage_tariff

Revision ID: 497_groupage_tariff_volume
Revises: 496_shipment_document_rod
Create Date: 2026-09-22

D5b objętość HITL. Nie paleta. Nie FSC. Nie kalkulator wagi.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "497_groupage_tariff_volume"
down_revision: str | None = "496_shipment_document_rod"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "groupage_tariff",
        sa.Column("volume_m3", sa.Numeric(14, 4), nullable=True),
    )
    op.create_check_constraint(
        "ck_groupage_tariff_volume_positive",
        "groupage_tariff",
        "volume_m3 IS NULL OR volume_m3 > 0",
    )


def downgrade() -> None:
    op.drop_constraint(
        "ck_groupage_tariff_volume_positive",
        "groupage_tariff",
        type_="check",
    )
    op.drop_column("groupage_tariff", "volume_m3")
