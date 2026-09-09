"""add OS&D and CMR dates on cargo_claim leftover EXP0.8

Revision ID: 131_cargo_claim_cmr
Revises: 130_carbon_method
Create Date: 2026-09-09

HITL damage_code + notice/suit dates. Nie silnik dni. Nie kwota.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "131_cargo_claim_cmr"
down_revision: str | None = "130_carbon_method"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("cargo_claim", sa.Column("damage_code", sa.String(length=16), nullable=True))
    op.add_column(
        "cargo_claim",
        sa.Column("cmr_notice_window", sa.String(length=16), nullable=True),
    )
    op.add_column("cargo_claim", sa.Column("notice_due_at", sa.Date(), nullable=True))
    op.add_column("cargo_claim", sa.Column("suit_due_at", sa.Date(), nullable=True))
    op.execute(
        """
        UPDATE cargo_claim SET
            damage_code = CASE claim_kind
                WHEN 'shortage' THEN 'shortage'
                WHEN 'other' THEN 'loss'
                ELSE 'damage'
            END,
            cmr_notice_window = 'notice_7',
            notice_due_at = created_at::date,
            suit_due_at = created_at::date
        WHERE damage_code IS NULL
        """
    )
    op.alter_column("cargo_claim", "damage_code", nullable=False)
    op.alter_column("cargo_claim", "cmr_notice_window", nullable=False)
    op.alter_column("cargo_claim", "notice_due_at", nullable=False)
    op.alter_column("cargo_claim", "suit_due_at", nullable=False)
    op.create_check_constraint(
        "ck_cargo_claim_damage_code",
        "cargo_claim",
        "damage_code IN ('overage', 'shortage', 'damage', 'loss')",
    )
    op.create_check_constraint(
        "ck_cargo_claim_cmr_notice_window",
        "cargo_claim",
        "cmr_notice_window IN ('notice_7', 'notice_21')",
    )
    op.create_check_constraint(
        "ck_cargo_claim_cmr_order",
        "cargo_claim",
        "suit_due_at >= notice_due_at",
    )


def downgrade() -> None:
    op.drop_constraint("ck_cargo_claim_cmr_order", "cargo_claim", type_="check")
    op.drop_constraint("ck_cargo_claim_cmr_notice_window", "cargo_claim", type_="check")
    op.drop_constraint("ck_cargo_claim_damage_code", "cargo_claim", type_="check")
    op.drop_column("cargo_claim", "suit_due_at")
    op.drop_column("cargo_claim", "notice_due_at")
    op.drop_column("cargo_claim", "cmr_notice_window")
    op.drop_column("cargo_claim", "damage_code")
