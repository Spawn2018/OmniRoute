"""add optional notes_for_driver on stop leftover T1

Revision ID: 154_stop_notes
Revises: 153_trip_route_label
Create Date: 2026-09-09

Opcjonalna notatka dla kierowcy HITL. Bez wagi.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "154_stop_notes"
down_revision: str | None = "153_trip_route_label"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "stop",
        sa.Column("notes_for_driver", sa.String(length=256), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("stop", "notes_for_driver")
