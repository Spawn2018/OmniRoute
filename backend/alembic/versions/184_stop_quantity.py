"""add optional quantity on stop leftover T1 EXP1

Revision ID: 184_stop_quantity
Revises: 183_stop_weight
Create Date: 2026-09-10

Opcjonalna ilość HITL Integer. Nie opakowanie. Nie float. Nie nowa tabela.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "184_stop_quantity"
down_revision: str | None = "183_stop_weight"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "stop",
        sa.Column("quantity", sa.Integer(), nullable=True),
    )
    op.create_check_constraint(
        "ck_stop_quantity",
        "stop",
        "quantity IS NULL OR quantity >= 0",
    )


def downgrade() -> None:
    op.drop_constraint("ck_stop_quantity", "stop", type_="check")
    op.drop_column("stop", "quantity")
