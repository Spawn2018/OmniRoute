"""add optional bl_kind on container leftover T3

Revision ID: 171_container_bl_kind
Revises: 170_container_return_terminal
Create Date: 2026-09-10

Opcjonalny rodzaj listu HITL (original/seawaybill/telex/express). Nie PIN.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "171_container_bl_kind"
down_revision: str | None = "170_container_return_terminal"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "container",
        sa.Column("bl_kind", sa.String(length=16), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("container", "bl_kind")
