"""add optional subcontractor_party_id on trip leftover T2c

Revision ID: 194_trip_subcontractor
Revises: 193_trip_actual_distance
Create Date: 2026-09-10

Opcjonalny FK podwykonawcy. Złożone FK per tenant. Nie /fleet.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "194_trip_subcontractor"
down_revision: str | None = "193_trip_actual_distance"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "trip",
        sa.Column("subcontractor_party_id", postgresql.UUID(as_uuid=True), nullable=True),
    )
    op.create_foreign_key(
        "fk_trip_subcontractor_party",
        "trip",
        "party",
        ["organization_id", "subcontractor_party_id"],
        ["organization_id", "id"],
        ondelete="RESTRICT",
    )


def downgrade() -> None:
    op.drop_constraint("fk_trip_subcontractor_party", "trip", type_="foreignkey")
    op.drop_column("trip", "subcontractor_party_id")
