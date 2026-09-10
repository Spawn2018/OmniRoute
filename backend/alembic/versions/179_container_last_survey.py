"""add optional last_survey_at on container leftover T3

Revision ID: 179_container_last_survey
Revises: 178_container_vgm
Create Date: 2026-09-10

Opcjonalny czas ostatniego przeglądu. Dana HITL ze strefą. Nie live HTTP.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "179_container_last_survey"
down_revision: str | None = "178_container_vgm"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "container",
        sa.Column("last_survey_at", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("container", "last_survey_at")
