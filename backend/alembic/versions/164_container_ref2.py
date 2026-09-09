"""add optional ref_2 on container leftover T3

Revision ID: 164_container_ref2
Revises: 163_container_ref1
Create Date: 2026-09-09

Opcjonalna druga referencja HITL. Bez wagi i bez PIN.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "164_container_ref2"
down_revision: str | None = "163_container_ref1"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "container",
        sa.Column("ref_2", sa.String(length=64), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("container", "ref_2")
