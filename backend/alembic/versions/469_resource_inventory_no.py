"""add optional inventory_no on resource leftover T2

Revision ID: 469_resource_inventory_no
Revises: 468_resource_document
Create Date: 2026-09-19

Opcjonalny numer inwentarzowy HITL. Nie floating trailer. Nie myto.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "469_resource_inventory_no"
down_revision: str | None = "468_resource_document"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "resource",
        sa.Column("inventory_no", sa.String(length=32), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("resource", "inventory_no")
