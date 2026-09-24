"""add source_ref on charge_code leftover EXP1

Revision ID: 521_charge_code_source_ref
Revises: 520_rate_line_index_id
Create Date: 2026-09-24

HITL wymagany source_ref na katalogu kodów opłat. Backfill legacy.
Nie CHECK WAITING. Nie seed Omni.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "521_charge_code_source_ref"
down_revision: str | None = "520_rate_line_index_id"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "charge_code",
        sa.Column("source_ref", sa.Text(), nullable=True),
    )
    op.execute(
        "UPDATE charge_code SET source_ref = 'fixture://charge-code/legacy' "
        "WHERE source_ref IS NULL"
    )
    op.alter_column("charge_code", "source_ref", nullable=False)
    op.create_check_constraint(
        "ck_charge_code_source_ref_len",
        "charge_code",
        "char_length(source_ref) BETWEEN 1 AND 512",
    )


def downgrade() -> None:
    op.drop_constraint("ck_charge_code_source_ref_len", "charge_code", type_="check")
    op.drop_column("charge_code", "source_ref")
