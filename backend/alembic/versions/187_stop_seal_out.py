"""add optional seal_out on stop leftover T1 EXP1

Revision ID: 187_stop_seal_out
Revises: 186_stop_seal_in
Create Date: 2026-09-10

Opcjonalna plomba wyjazdu HITL. Nie awizacja. Nie PIN. Nie nowa tabela.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "187_stop_seal_out"
down_revision: str | None = "186_stop_seal_in"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "stop",
        sa.Column("seal_out", sa.String(length=32), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("stop", "seal_out")
