"""optional FX anchor dates on shipment leftover T7

Revision ID: 500_shipment_fx_anchor_dates
Revises: 499_document_template_branding
Create Date: 2026-09-22

HITL kotwice kursu na zleceniu. Nie fx×FV. Nie mnożenie NBP.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "500_shipment_fx_anchor_dates"
down_revision: str | None = "499_document_template_branding"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("shipment", sa.Column("etd", sa.Date(), nullable=True))
    op.add_column("shipment", sa.Column("loading_date", sa.Date(), nullable=True))
    op.add_column("shipment", sa.Column("unloading_date", sa.Date(), nullable=True))
    op.add_column("shipment", sa.Column("invoice_date", sa.Date(), nullable=True))


def downgrade() -> None:
    op.drop_column("shipment", "invoice_date")
    op.drop_column("shipment", "unloading_date")
    op.drop_column("shipment", "loading_date")
    op.drop_column("shipment", "etd")
