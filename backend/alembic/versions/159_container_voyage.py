"""add optional voyage_no on container leftover T3

Revision ID: 159_container_voyage
Revises: 158_container_vessel
Create Date: 2026-09-09

Opcjonalny numer rejsu HITL. Bez bookingu i bez PIN.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "159_container_voyage"
down_revision: str | None = "158_container_vessel"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "container",
        sa.Column("voyage_no", sa.String(length=32), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("container", "voyage_no")
