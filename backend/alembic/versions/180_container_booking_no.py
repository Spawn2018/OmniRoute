"""add optional booking_no on container leftover T3

Revision ID: 180_container_booking_no
Revises: 179_container_last_survey
Create Date: 2026-09-10

Opcjonalny numer bookingu HITL. Nie live HTTP. Nie PIN.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "180_container_booking_no"
down_revision: str | None = "179_container_last_survey"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "container",
        sa.Column("booking_no", sa.String(64), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("container", "booking_no")
