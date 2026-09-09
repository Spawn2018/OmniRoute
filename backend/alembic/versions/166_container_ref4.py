"""add optional ref_4 on container leftover T3

Revision ID: 166_container_ref4
Revises: 165_container_ref3
Create Date: 2026-09-09

Opcjonalna czwarta referencja HITL. Bez wagi i bez PIN.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "166_container_ref4"
down_revision: str | None = "165_container_ref3"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "container",
        sa.Column("ref_4", sa.String(length=64), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("container", "ref_4")
