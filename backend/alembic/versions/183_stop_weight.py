"""add optional weight_kg on stop leftover T1 EXP1

Revision ID: 183_stop_weight
Revises: 182_container_shipment_leg
Create Date: 2026-09-10

Opcjonalna waga HITL Decimal. Nie VGM. Nie float. Nie nowa tabela.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "183_stop_weight"
down_revision: str | None = "182_container_shipment_leg"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "stop",
        sa.Column("weight_kg", sa.Numeric(14, 4), nullable=True),
    )
    op.create_check_constraint(
        "ck_stop_weight_kg",
        "stop",
        "weight_kg IS NULL OR weight_kg >= 0",
    )


def downgrade() -> None:
    op.drop_constraint("ck_stop_weight_kg", "stop", type_="check")
    op.drop_column("stop", "weight_kg")
