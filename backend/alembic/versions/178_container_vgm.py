"""add optional VGM bundle on container leftover T3

Revision ID: 178_container_vgm
Revises: 177_container_cfs_cutoff
Create Date: 2026-09-10

Opcjonalny VGM HITL: kg Decimal, metoda SOLAS, cutoff ze strefą. Nie live HTTP.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "178_container_vgm"
down_revision: str | None = "177_container_cfs_cutoff"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "container",
        sa.Column("vgm_kg", sa.Numeric(14, 4), nullable=True),
    )
    op.add_column(
        "container",
        sa.Column("vgm_method", sa.String(16), nullable=True),
    )
    op.add_column(
        "container",
        sa.Column("vgm_cutoff_at", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("container", "vgm_cutoff_at")
    op.drop_column("container", "vgm_method")
    op.drop_column("container", "vgm_kg")
