"""drop twin_mark kind list; add FK to dictionary

Revision ID: 350_twin_mark_kind_fk
Revises: 349_suggestion_ledger_kind_fk
Create Date: 2026-09-13

AI1.4 leftover. Slownik waliduje rodzaj. Nie lista CHECK.
"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "350_twin_mark_kind_fk"
down_revision: str | None = "349_suggestion_ledger_kind_fk"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute(
        """
        INSERT INTO twin_kind (
            id, organization_id, kind_code, source_ref, created_at, updated_at
        )
        SELECT gen_random_uuid(), d.organization_id, d.twin_kind,
               'fixture://twin-kind/backfill-' || d.twin_kind,
               now(), now()
        FROM (
            SELECT DISTINCT organization_id, twin_kind
            FROM twin_mark
        ) AS d
        WHERE NOT EXISTS (
            SELECT 1 FROM twin_kind s
            WHERE s.organization_id = d.organization_id
              AND s.kind_code = d.twin_kind
        )
        """
    )
    op.drop_constraint("ck_twin_mark_kind", "twin_mark", type_="check")
    op.alter_column(
        "twin_mark",
        "twin_kind",
        existing_type=sa.String(length=16),
        type_=sa.String(length=32),
        existing_nullable=False,
    )
    op.create_foreign_key(
        "fk_twin_mark_kind",
        "twin_mark",
        "twin_kind",
        ["organization_id", "twin_kind"],
        ["organization_id", "kind_code"],
        ondelete="RESTRICT",
    )


def downgrade() -> None:
    op.drop_constraint("fk_twin_mark_kind", "twin_mark", type_="foreignkey")
    op.alter_column(
        "twin_mark",
        "twin_kind",
        existing_type=sa.String(length=32),
        type_=sa.String(length=16),
        existing_nullable=False,
    )
    op.create_check_constraint(
        "ck_twin_mark_kind",
        "twin_mark",
        "length(twin_kind) BETWEEN 2 AND 16",
    )
