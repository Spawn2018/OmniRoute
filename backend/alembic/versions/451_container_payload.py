"""add optional payload_kg on container leftover T3

Revision ID: 451_container_payload
Revises: 450_container_pin
Create Date: 2026-09-18

Opcjonalna ładowność HITL (Decimal). Nie quantity. Nie kalkulator VGM.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "451_container_payload"
down_revision: str | None = "450_container_pin"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "container",
        sa.Column("payload_kg", sa.Numeric(14, 4), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("container", "payload_kg")
