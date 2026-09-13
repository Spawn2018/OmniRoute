"""drop outcome_ledger kind list; add FK to outcome_kind

Revision ID: 352_outcome_ledger_kind_fk
Revises: 351_outcome_kind
Create Date: 2026-09-13

AI1.4 leftover. Slownik waliduje rodzaj. Nie lista CHECK.
"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "352_outcome_ledger_kind_fk"
down_revision: str | None = "351_outcome_kind"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute(
        """
        INSERT INTO outcome_kind (
            id, organization_id, kind_code, source_ref, created_at, updated_at
        )
        SELECT gen_random_uuid(), d.organization_id, d.outcome_kind,
               'fixture://outcome-kind/backfill-' || d.outcome_kind,
               now(), now()
        FROM (
            SELECT DISTINCT organization_id, outcome_kind
            FROM outcome_ledger
        ) AS d
        WHERE NOT EXISTS (
            SELECT 1 FROM outcome_kind s
            WHERE s.organization_id = d.organization_id
              AND s.kind_code = d.outcome_kind
        )
        """
    )
    op.drop_constraint("ck_outcome_ledger_kind", "outcome_ledger", type_="check")
    op.alter_column(
        "outcome_ledger",
        "outcome_kind",
        existing_type=sa.String(length=16),
        type_=sa.String(length=32),
        existing_nullable=False,
    )
    op.create_foreign_key(
        "fk_outcome_ledger_kind",
        "outcome_ledger",
        "outcome_kind",
        ["organization_id", "outcome_kind"],
        ["organization_id", "kind_code"],
        ondelete="RESTRICT",
    )


def downgrade() -> None:
    op.drop_constraint("fk_outcome_ledger_kind", "outcome_ledger", type_="foreignkey")
    op.alter_column(
        "outcome_ledger",
        "outcome_kind",
        existing_type=sa.String(length=32),
        type_=sa.String(length=16),
        existing_nullable=False,
    )
    op.create_check_constraint(
        "ck_outcome_ledger_kind",
        "outcome_ledger",
        "length(outcome_kind) BETWEEN 2 AND 16",
    )
