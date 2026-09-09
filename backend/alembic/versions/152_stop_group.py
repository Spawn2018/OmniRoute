"""add optional stop_group_code on stop leftover T1

Revision ID: 152_stop_group
Revises: 151_trip_driver2
Create Date: 2026-09-09

Opcjonalny kod grupy punktów. Bez nowej tabeli. Bez unique.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "152_stop_group"
down_revision: str | None = "151_trip_driver2"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "stop",
        sa.Column("stop_group_code", sa.String(length=32), nullable=True),
    )
    # Unique would block two stops sharing a group token.
    op.create_check_constraint(
        "ck_stop_group_code",
        "stop",
        "stop_group_code IS NULL OR stop_group_code ~ '^[A-Za-z0-9_-]{2,32}$'",
    )


def downgrade() -> None:
    op.drop_constraint("ck_stop_group_code", "stop", type_="check")
    op.drop_column("stop", "stop_group_code")
