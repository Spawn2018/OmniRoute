"""add needs_external_power flag on container leftover T3

Revision ID: 463_container_ext_power
Revises: 462_container_temp_max
Create Date: 2026-09-19

Flaga zasilania zewnętrznego HITL. Bez N3. Bez live.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "463_container_ext_power"
down_revision: str | None = "462_container_temp_max"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "container",
        sa.Column(
            "needs_external_power",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
    )


def downgrade() -> None:
    op.drop_column("container", "needs_external_power")
