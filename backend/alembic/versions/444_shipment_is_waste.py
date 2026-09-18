"""add is_waste flag on shipment leftover C6

Revision ID: 444_shipment_is_waste
Revises: 443_waste_mark
Create Date: 2026-09-18

HITL flaga odpadu na zleceniu. Nie MOS live. Nie waste_mark auto.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "444_shipment_is_waste"
down_revision: str | None = "443_waste_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "shipment",
        sa.Column(
            "is_waste",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
    )


def downgrade() -> None:
    op.drop_column("shipment", "is_waste")
