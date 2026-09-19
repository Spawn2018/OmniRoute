"""add optional gate_in_date on container leftover T3

Revision ID: 458_container_gate_in_date
Revises: 457_container_return_date
Create Date: 2026-09-19

Opcjonalna data wjazdu HITL. Nie countdown. Nie cutoff. Nie float.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "458_container_gate_in_date"
down_revision: str | None = "457_container_return_date"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "container",
        sa.Column("gate_in_date", sa.Date(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("container", "gate_in_date")
