"""add optional packaging_code on stop leftover T1 EXP1

Revision ID: 185_stop_pack
Revises: 184_stop_quantity
Create Date: 2026-09-10

Opcjonalny kod opakowania HITL. Nie plomba. Nie FK słownika. Nie nowa tabela.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "185_stop_pack"
down_revision: str | None = "184_stop_quantity"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "stop",
        sa.Column("packaging_code", sa.String(length=32), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("stop", "packaging_code")
