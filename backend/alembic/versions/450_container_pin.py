"""add optional pin_code on container leftover T3

Revision ID: 450_container_pin
Revises: 449_container_tare
Create Date: 2026-09-18

Opcjonalny PIN odbioru HITL (tekst). Nie live terminal. Nie ciphertext.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "450_container_pin"
down_revision: str | None = "449_container_tare"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "container",
        sa.Column("pin_code", sa.String(64), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("container", "pin_code")
