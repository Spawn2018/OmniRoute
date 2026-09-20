"""add optional driver_card_no on resource leftover T2

Revision ID: 474_resource_driver_card_no
Revises: 473_resource_phone
Create Date: 2026-09-20

Opcjonalny numer karty kierowcy HITL. Nie tacho live. Nie DDD.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "474_resource_driver_card_no"
down_revision: str | None = "473_resource_phone"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "resource",
        sa.Column("driver_card_no", sa.String(length=32), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("resource", "driver_card_no")
