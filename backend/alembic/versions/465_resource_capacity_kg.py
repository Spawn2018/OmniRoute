"""add optional capacity_kg on resource leftover T2

Revision ID: 465_resource_capacity_kg
Revises: 464_container_release
Create Date: 2026-09-19

Opcjonalna pojemnosc masowa HITL (kg Decimal). Nie LDM. Nie m3. Nie document_expiries.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "465_resource_capacity_kg"
down_revision: str | None = "464_container_release"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "resource",
        sa.Column("capacity_kg", sa.Numeric(14, 4), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("resource", "capacity_kg")
