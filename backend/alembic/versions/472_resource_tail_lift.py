"""add optional tail_lift on resource leftover T2

Revision ID: 472_resource_tail_lift
Revises: 471_resource_reefer
Create Date: 2026-09-20

Opcjonalna flaga windy HITL. Nie matching ladunku.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "472_resource_tail_lift"
down_revision: str | None = "471_resource_reefer"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "resource",
        sa.Column("tail_lift", sa.Boolean(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("resource", "tail_lift")
