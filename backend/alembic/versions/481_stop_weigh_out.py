"""add optional weigh_out_kg on stop leftover T1 EXP1

Revision ID: 481_stop_weigh_out
Revises: 480_stop_weigh_in
Create Date: 2026-09-21

Opcjonalna waga wyjazdu HITL. Nie waga kontenera. Nie nowa tabela.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "481_stop_weigh_out"
down_revision: str | None = "480_stop_weigh_in"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "stop",
        sa.Column("weigh_out_kg", sa.Numeric(14, 4), nullable=True),
    )
    op.create_check_constraint(
        "ck_stop_weigh_out",
        "stop",
        "weigh_out_kg IS NULL OR weigh_out_kg >= 0",
    )


def downgrade() -> None:
    op.drop_constraint("ck_stop_weigh_out", "stop", type_="check")
    op.drop_column("stop", "weigh_out_kg")
