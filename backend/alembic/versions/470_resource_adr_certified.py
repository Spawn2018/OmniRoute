"""add optional adr_certified on resource leftover T2

Revision ID: 470_resource_adr_certified
Revises: 469_resource_inventory_no
Create Date: 2026-09-19

Opcjonalna flaga ADR HITL. Nie reefer. Nie matching ladunku.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "470_resource_adr_certified"
down_revision: str | None = "469_resource_inventory_no"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "resource",
        sa.Column("adr_certified", sa.Boolean(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("resource", "adr_certified")
