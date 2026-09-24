"""add evidence HITL bools on cargo_claim leftover EXP0.8/EXP1

Revision ID: 517_cargo_claim_evidence
Revises: 516_dg_limited_quantity
Create Date: 2026-09-24

HITL evidence_gps / evidence_temp / evidence_photo. Nie live GPS. Nie Deadline Engine.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "517_cargo_claim_evidence"
down_revision: str | None = "516_dg_limited_quantity"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "cargo_claim",
        sa.Column("evidence_gps", sa.Boolean(), nullable=True),
    )
    op.add_column(
        "cargo_claim",
        sa.Column("evidence_temp", sa.Boolean(), nullable=True),
    )
    op.add_column(
        "cargo_claim",
        sa.Column("evidence_photo", sa.Boolean(), nullable=True),
    )
    op.execute(
        """
        UPDATE cargo_claim
        SET evidence_gps = false,
            evidence_temp = false,
            evidence_photo = false
        WHERE evidence_gps IS NULL
           OR evidence_temp IS NULL
           OR evidence_photo IS NULL
        """
    )
    op.alter_column("cargo_claim", "evidence_gps", nullable=False)
    op.alter_column("cargo_claim", "evidence_temp", nullable=False)
    op.alter_column("cargo_claim", "evidence_photo", nullable=False)


def downgrade() -> None:
    op.drop_column("cargo_claim", "evidence_photo")
    op.drop_column("cargo_claim", "evidence_temp")
    op.drop_column("cargo_claim", "evidence_gps")
