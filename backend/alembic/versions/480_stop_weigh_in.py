"""add optional weigh_in_kg on stop leftover T1 EXP1

Revision ID: 480_stop_weigh_in
Revises: 479_stop_no_show_at
Create Date: 2026-09-20

Opcjonalna waga wjazdu HITL. Nie waga kontenera. Nie waga wyjazdu. Nie nowa tabela.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "480_stop_weigh_in"
down_revision: str | None = "479_stop_no_show_at"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "stop",
        sa.Column("weigh_in_kg", sa.Numeric(14, 4), nullable=True),
    )
    op.create_check_constraint(
        "ck_stop_weigh_in",
        "stop",
        "weigh_in_kg IS NULL OR weigh_in_kg >= 0",
    )


def downgrade() -> None:
    op.drop_constraint("ck_stop_weigh_in", "stop", type_="check")
    op.drop_column("stop", "weigh_in_kg")
