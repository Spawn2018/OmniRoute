"""add optional seal_in on stop leftover T1 EXP1

Revision ID: 186_stop_seal_in
Revises: 185_stop_pack
Create Date: 2026-09-10

Opcjonalna plomba wjazdu HITL. Nie druga plomba. Nie PIN. Nie nowa tabela.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "186_stop_seal_in"
down_revision: str | None = "185_stop_pack"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "stop",
        sa.Column("seal_in", sa.String(length=32), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("stop", "seal_in")
