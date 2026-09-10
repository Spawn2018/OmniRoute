"""add optional shipment_leg_id on container leftover T3

Revision ID: 182_container_shipment_leg
Revises: 181_container_carrier_party
Create Date: 2026-09-10

Opcjonalny FK odcinka. Unique (org, id) na shipment_leg pod złożone FK. Nie live HTTP.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "182_container_shipment_leg"
down_revision: str | None = "181_container_carrier_party"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_unique_constraint(
        "uq_shipment_leg_org_id",
        "shipment_leg",
        ["organization_id", "id"],
    )
    op.add_column(
        "container",
        sa.Column("shipment_leg_id", postgresql.UUID(as_uuid=True), nullable=True),
    )
    op.create_foreign_key(
        "fk_container_shipment_leg",
        "container",
        "shipment_leg",
        ["organization_id", "shipment_leg_id"],
        ["organization_id", "id"],
        ondelete="RESTRICT",
    )


def downgrade() -> None:
    op.drop_constraint("fk_container_shipment_leg", "container", type_="foreignkey")
    op.drop_column("container", "shipment_leg_id")
    op.drop_constraint("uq_shipment_leg_org_id", "shipment_leg", type_="unique")
