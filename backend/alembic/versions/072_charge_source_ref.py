"""add charge.source_ref nullable leftover P0

Revision ID: 072_charge_source_ref
Revises: 071_dangerous_good_on_rfq
Create Date: 2026-09-08

Stare fixture zostają NULL. Nowy INSERT wymaga source_ref w serwisie.
Nie backfill. Nie druga tabela marży.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "072_charge_source_ref"
down_revision: str | None = "071_dangerous_good_on_rfq"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("charge", sa.Column("source_ref", sa.String(length=512), nullable=True))


def downgrade() -> None:
    op.drop_column("charge", "source_ref")
