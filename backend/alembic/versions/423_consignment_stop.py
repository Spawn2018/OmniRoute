"""optional stop_id on consignment leftover N1

Revision ID: 423_consignment_stop
Revises: 422_shipment_package_consignment
Create Date: 2026-09-17

Opcjonalny punkt trasy na przesyłce. Złożone FK per tenant. Nie mapa.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "423_consignment_stop"
down_revision: str | None = "422_shipment_package_consignment"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "consignment",
        sa.Column("stop_id", postgresql.UUID(as_uuid=True), nullable=True),
    )
    op.create_foreign_key(
        "fk_consignment_stop",
        "consignment",
        "stop",
        ["organization_id", "shipment_id", "stop_id"],
        ["organization_id", "shipment_id", "id"],
        ondelete="RESTRICT",
    )


def downgrade() -> None:
    op.drop_constraint("fk_consignment_stop", "consignment", type_="foreignkey")
    op.drop_column("consignment", "stop_id")
