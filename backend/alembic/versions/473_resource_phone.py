"""add optional phone on resource leftover T2

Revision ID: 473_resource_phone
Revises: 472_resource_tail_lift
Create Date: 2026-09-20

Opcjonalny telefon HITL. Nie party_contact. Nie SMS.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "473_resource_phone"
down_revision: str | None = "472_resource_tail_lift"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "resource",
        sa.Column("phone", sa.String(length=64), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("resource", "phone")
