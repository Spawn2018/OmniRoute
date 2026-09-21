"""add optional shipment_id on charge

Revision ID: 488_charge_shipment_id
Revises: 487_container_destination_city
Create Date: 2026-09-21

Opcjonalne wiązanie opłaty ze zleceniem tego tenanta. Nie widok marży drzewa.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "488_charge_shipment_id"
down_revision: str | None = "487_container_destination_city"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "charge",
        sa.Column("shipment_id", postgresql.UUID(as_uuid=True), nullable=True),
    )
    op.create_foreign_key(
        "fk_charge_shipment",
        "charge",
        "shipment",
        ["organization_id", "shipment_id"],
        ["organization_id", "id"],
        ondelete="RESTRICT",
    )


def downgrade() -> None:
    op.drop_constraint("fk_charge_shipment", "charge", type_="foreignkey")
    op.drop_column("charge", "shipment_id")
