"""optional consignment_id on shipment_package leftover D2b

Revision ID: 422_shipment_package_consignment
Revises: 421_inbound_rfc822
Create Date: 2026-09-17

Opcjonalny FK przesyłki na paczce. Złożone FK per tenant. Nie WMS.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "422_shipment_package_consignment"
down_revision: str | None = "421_inbound_rfc822"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "shipment_package",
        sa.Column("consignment_id", postgresql.UUID(as_uuid=True), nullable=True),
    )
    op.create_foreign_key(
        "fk_shipment_package_consignment",
        "shipment_package",
        "consignment",
        ["organization_id", "consignment_id"],
        ["organization_id", "id"],
        ondelete="RESTRICT",
    )


def downgrade() -> None:
    op.drop_constraint("fk_shipment_package_consignment", "shipment_package", type_="foreignkey")
    op.drop_column("shipment_package", "consignment_id")
