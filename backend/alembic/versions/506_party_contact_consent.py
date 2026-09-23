"""add tracking_consent bool on party_contact leftover BR2.2

Revision ID: 506_party_contact_consent
Revises: 505_local_charge_carrier_service
Create Date: 2026-09-23

Flaga HITL zgody na śledzenie. Bez FK do katalogu. Bez live poll.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "506_party_contact_consent"
down_revision: str | None = "505_local_charge_carrier_service"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "party_contact",
        sa.Column(
            "tracking_consent",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
    )


def downgrade() -> None:
    op.drop_column("party_contact", "tracking_consent")
