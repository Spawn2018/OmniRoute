"""add optional packaging_code on container leftover T3

Revision ID: 162_container_pack
Revises: 161_container_cargo
Create Date: 2026-09-09

Opcjonalny kod opakowania HITL. Bez wagi i bez PIN.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "162_container_pack"
down_revision: str | None = "161_container_cargo"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "container",
        sa.Column("packaging_code", sa.String(length=32), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("container", "packaging_code")
