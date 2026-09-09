"""add reefer flag on container leftover T3

Revision ID: 168_container_reefer
Revises: 167_container_ref5
Create Date: 2026-09-09

Flaga chłodniczego HITL. Bez temperatury i bez PIN.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "168_container_reefer"
down_revision: str | None = "167_container_ref5"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "container",
        sa.Column("reefer", sa.Boolean(), nullable=False, server_default=sa.text("false")),
    )


def downgrade() -> None:
    op.drop_column("container", "reefer")
