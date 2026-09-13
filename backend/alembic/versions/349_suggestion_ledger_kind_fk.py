"""drop suggestion_ledger kind list; add FK to suggestion_kind

Revision ID: 349_suggestion_ledger_kind_fk
Revises: 348_autonomy_level
Create Date: 2026-09-13

AI1.4 leftover. Slownik waliduje rodzaj. Nie lista CHECK.
"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "349_suggestion_ledger_kind_fk"
down_revision: str | None = "348_autonomy_level"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute(
        """
        INSERT INTO suggestion_kind (
            id, organization_id, kind_code, source_ref, created_at, updated_at
        )
        SELECT gen_random_uuid(), d.organization_id, d.suggestion_kind,
               'fixture://suggestion-kind/backfill-' || d.suggestion_kind,
               now(), now()
        FROM (
            SELECT DISTINCT organization_id, suggestion_kind
            FROM suggestion_ledger
        ) AS d
        WHERE NOT EXISTS (
            SELECT 1 FROM suggestion_kind s
            WHERE s.organization_id = d.organization_id
              AND s.kind_code = d.suggestion_kind
        )
        """
    )
    op.drop_constraint("ck_suggestion_ledger_kind", "suggestion_ledger", type_="check")
    op.alter_column(
        "suggestion_ledger",
        "suggestion_kind",
        existing_type=sa.String(length=16),
        type_=sa.String(length=32),
        existing_nullable=False,
    )
    op.create_foreign_key(
        "fk_suggestion_ledger_kind",
        "suggestion_ledger",
        "suggestion_kind",
        ["organization_id", "suggestion_kind"],
        ["organization_id", "kind_code"],
        ondelete="RESTRICT",
    )


def downgrade() -> None:
    op.drop_constraint("fk_suggestion_ledger_kind", "suggestion_ledger", type_="foreignkey")
    op.alter_column(
        "suggestion_ledger",
        "suggestion_kind",
        existing_type=sa.String(length=32),
        type_=sa.String(length=16),
        existing_nullable=False,
    )
    op.create_check_constraint(
        "ck_suggestion_ledger_kind",
        "suggestion_ledger",
        "length(suggestion_kind) BETWEEN 2 AND 16",
    )
