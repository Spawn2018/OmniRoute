"""add optional carrier_party_id on container leftover T3

Revision ID: 181_container_carrier_party
Revises: 180_container_booking_no
Create Date: 2026-09-10

Opcjonalny FK armatora. Złożone FK per tenant. Nie live HTTP.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "181_container_carrier_party"
down_revision: str | None = "180_container_booking_no"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "container",
        sa.Column("carrier_party_id", postgresql.UUID(as_uuid=True), nullable=True),
    )
    op.create_foreign_key(
        "fk_container_carrier_party",
        "container",
        "party",
        ["organization_id", "carrier_party_id"],
        ["organization_id", "id"],
        ondelete="RESTRICT",
    )


def downgrade() -> None:
    op.drop_constraint("fk_container_carrier_party", "container", type_="foreignkey")
    op.drop_column("container", "carrier_party_id")
