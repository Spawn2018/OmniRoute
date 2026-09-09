"""add optional remarks on container leftover T3

Revision ID: 160_container_remarks
Revises: 159_container_voyage
Create Date: 2026-09-09

Opcjonalna uwaga HITL. Bez wagi i bez PIN.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "160_container_remarks"
down_revision: str | None = "159_container_voyage"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "container",
        sa.Column("remarks", sa.String(length=256), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("container", "remarks")
