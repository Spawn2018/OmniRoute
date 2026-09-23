"""add packing_group on dangerous_good leftover EXP0.9

Revision ID: 514_dangerous_good_packing_group
Revises: 513_local_charge_bind_mark
Create Date: 2026-09-23

HITL grupa pakowania I|II|III. LLM nie nadaje klasy. Nie live IMO.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "514_dangerous_good_packing_group"
down_revision: str | None = "513_local_charge_bind_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "dangerous_good",
        sa.Column("packing_group", sa.String(length=3), nullable=True),
    )
    op.execute(
        """
        UPDATE dangerous_good SET packing_group = 'II'
        WHERE packing_group IS NULL
        """
    )
    op.alter_column("dangerous_good", "packing_group", nullable=False)
    op.create_check_constraint(
        "ck_dangerous_good_packing_group",
        "dangerous_good",
        "packing_group IN ('I', 'II', 'III')",
    )


def downgrade() -> None:
    op.drop_constraint("ck_dangerous_good_packing_group", "dangerous_good", type_="check")
    op.drop_column("dangerous_good", "packing_group")
