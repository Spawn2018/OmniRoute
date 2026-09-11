"""optional shipment.asn_id link for CT1 HITL promote

Revision ID: 223_shipment_asn_id
Revises: 222_shipment_guide_labels
Create Date: 2026-09-11

HITL powiązanie awiza ze zleceniem. Nie auto przy POST asn.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "223_shipment_asn_id"
down_revision: str | None = "222_shipment_guide_labels"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "shipment",
        sa.Column("asn_id", PGUUID(as_uuid=True), nullable=True),
    )
    op.create_foreign_key(
        "fk_shipment_asn",
        "shipment",
        "asn",
        ["organization_id", "asn_id"],
        ["organization_id", "id"],
        ondelete="RESTRICT",
    )
    op.create_unique_constraint(
        "uq_shipment_org_asn",
        "shipment",
        ["organization_id", "asn_id"],
    )


def downgrade() -> None:
    op.drop_constraint("uq_shipment_org_asn", "shipment", type_="unique")
    op.drop_constraint("fk_shipment_asn", "shipment", type_="foreignkey")
    op.drop_column("shipment", "asn_id")
