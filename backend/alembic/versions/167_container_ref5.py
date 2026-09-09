"""add optional ref_5 on container leftover T3

Revision ID: 167_container_ref5
Revises: 166_container_ref4
Create Date: 2026-09-09

Opcjonalna piąta referencja HITL. Bez wagi i bez PIN.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "167_container_ref5"
down_revision: str | None = "166_container_ref4"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "container",
        sa.Column("ref_5", sa.String(length=64), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("container", "ref_5")
