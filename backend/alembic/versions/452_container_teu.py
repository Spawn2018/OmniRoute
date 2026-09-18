"""add optional teu on container leftover T3

Revision ID: 452_container_teu
Revises: 451_container_payload
Create Date: 2026-09-18

Opcjonalne TEU HITL (Decimal). Nie kalkulator z typu ISO. Nie quantity.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "452_container_teu"
down_revision: str | None = "451_container_payload"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "container",
        sa.Column("teu", sa.Numeric(14, 4), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("container", "teu")
