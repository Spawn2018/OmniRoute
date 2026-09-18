"""add optional tare_kg on container leftover T3

Revision ID: 449_container_tare
Revises: 448_container_mixed_dd
Create Date: 2026-09-18

Opcjonalna tara HITL (kg Decimal). Nie VGM. Nie kalkulator. Nie PIN.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "449_container_tare"
down_revision: str | None = "448_container_mixed_dd"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "container",
        sa.Column("tare_kg", sa.Numeric(14, 4), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("container", "tare_kg")
