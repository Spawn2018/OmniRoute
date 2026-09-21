"""add optional vessel_imo on container leftover T3 EXP1

Revision ID: 483_container_vessel_imo
Revises: 482_container_grade
Create Date: 2026-09-21

Opcjonalny IMO HITL (tekst). Nie AIS. Nie cyfra kontrolna.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "483_container_vessel_imo"
down_revision: str | None = "482_container_grade"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "container",
        sa.Column("vessel_imo", sa.String(16), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("container", "vessel_imo")
