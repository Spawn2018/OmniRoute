"""add optional cargo_description on container leftover T3

Revision ID: 161_container_cargo
Revises: 160_container_remarks
Create Date: 2026-09-09

Opcjonalny opis ładunku HITL. Bez wagi i bez PIN.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "161_container_cargo"
down_revision: str | None = "160_container_remarks"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "container",
        sa.Column("cargo_description", sa.String(length=256), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("container", "cargo_description")
