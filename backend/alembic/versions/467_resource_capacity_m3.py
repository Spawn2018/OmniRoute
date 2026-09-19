"""add optional capacity_m3 on resource leftover T2

Revision ID: 467_resource_capacity_m3
Revises: 466_resource_capacity_ldm
Create Date: 2026-09-19

Opcjonalne m3 HITL (Decimal). Nie document_expiries. Nie kalkulator z LDM.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "467_resource_capacity_m3"
down_revision: str | None = "466_resource_capacity_ldm"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "resource",
        sa.Column("capacity_m3", sa.Numeric(14, 4), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("resource", "capacity_m3")
