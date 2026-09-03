"""store quotation.document_number issued from settings prefix

Revision ID: 032_quotation_document_number
Revises: 031_commodity_on_rfq
Create Date: 2026-09-03

Numer na ofercie, nie licznik w organization_setting. quotation już ma RLS FORCE.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "032_quotation_document_number"
down_revision: str | None = "031_commodity_on_rfq"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "quotation",
        sa.Column("document_number", sa.String(length=32), nullable=True),
    )
    op.create_index(
        "uq_quotation_org_document_number",
        "quotation",
        ["organization_id", "document_number"],
        unique=True,
        postgresql_where=sa.text("document_number IS NOT NULL"),
    )


def downgrade() -> None:
    op.drop_index("uq_quotation_org_document_number", table_name="quotation")
    op.drop_column("quotation", "document_number")
