"""add optional reefer on resource leftover T2

Revision ID: 471_resource_reefer
Revises: 470_resource_adr_certified
Create Date: 2026-09-19

Opcjonalna flaga chlodni HITL. Nie container.reefer. Nie temperatura.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "471_resource_reefer"
down_revision: str | None = "470_resource_adr_certified"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "resource",
        sa.Column("reefer", sa.Boolean(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("resource", "reefer")
