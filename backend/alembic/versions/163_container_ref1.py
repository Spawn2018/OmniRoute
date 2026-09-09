"""add optional ref_1 on container leftover T3

Revision ID: 163_container_ref1
Revises: 162_container_pack
Create Date: 2026-09-09

Opcjonalna referencja HITL. Bez wagi i bez PIN.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "163_container_ref1"
down_revision: str | None = "162_container_pack"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "container",
        sa.Column("ref_1", sa.String(length=64), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("container", "ref_1")
