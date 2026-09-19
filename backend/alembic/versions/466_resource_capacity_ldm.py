"""add optional capacity_ldm on resource leftover T2

Revision ID: 466_resource_capacity_ldm
Revises: 465_resource_capacity_kg
Create Date: 2026-09-19

Opcjonalne LDM HITL (Decimal). Nie m3. Nie document_expiries.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "466_resource_capacity_ldm"
down_revision: str | None = "465_resource_capacity_kg"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "resource",
        sa.Column("capacity_ldm", sa.Numeric(14, 4), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("resource", "capacity_ldm")
