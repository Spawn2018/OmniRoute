"""add HITL shipment_ref on shipment leftover D9b

Revision ID: 144_shipment_ref
Revises: 143_rank_mark
Create Date: 2026-09-09

HITL twardy numer zlecenia. Bez kodu kreskowego. Bez wydruku. Bez 409 wyjazdu.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "144_shipment_ref"
down_revision: str | None = "143_rank_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "shipment",
        sa.Column("shipment_ref", sa.String(length=256), nullable=True),
    )
    op.create_unique_constraint(
        "uq_shipment_org_shipment_ref",
        "shipment",
        ["organization_id", "shipment_ref"],
    )


def downgrade() -> None:
    op.drop_constraint("uq_shipment_org_shipment_ref", "shipment", type_="unique")
    op.drop_column("shipment", "shipment_ref")
