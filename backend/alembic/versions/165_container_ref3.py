"""add optional ref_3 on container leftover T3

Revision ID: 165_container_ref3
Revises: 164_container_ref2
Create Date: 2026-09-09

Opcjonalna trzecia referencja HITL. Bez wagi i bez PIN.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "165_container_ref3"
down_revision: str | None = "164_container_ref2"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "container",
        sa.Column("ref_3", sa.String(length=64), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("container", "ref_3")
