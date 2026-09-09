"""add optional vessel_name on container leftover T3

Revision ID: 158_container_vessel
Revises: 157_container_seal3
Create Date: 2026-09-09

Opcjonalna nazwa statku HITL. Bez numeru rejsu i bez PIN.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "158_container_vessel"
down_revision: str | None = "157_container_seal3"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "container",
        sa.Column("vessel_name", sa.String(length=128), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("container", "vessel_name")
