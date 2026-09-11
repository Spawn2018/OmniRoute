"""add optional asn.guide_code for CT4 block_409

Revision ID: 219_asn_guide_code
Revises: 218_routing_guide_enforcement
Create Date: 2026-09-11

HITL guide_code na ASN. Nie 409 na shipment.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "219_asn_guide_code"
down_revision: str | None = "218_routing_guide_enforcement"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "asn",
        sa.Column("guide_code", sa.String(length=32), nullable=True),
    )
    op.create_check_constraint(
        "ck_asn_guide_code",
        "asn",
        "guide_code IS NULL OR guide_code ~ '^[a-z][a-z0-9_]{1,31}$'",
    )


def downgrade() -> None:
    op.drop_constraint("ck_asn_guide_code", "asn", type_="check")
    op.drop_column("asn", "guide_code")
