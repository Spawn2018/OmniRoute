"""nullable ocean_bill.bill_no + unique when set for D6c pools

Revision ID: 494_ocean_bill_number_pool
Revises: 493_channel_quote_transport_mode
Create Date: 2026-09-22

D6c pule HBL/MBL z M-03. Nie konsolidacja. Nie PDF.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "494_ocean_bill_number_pool"
down_revision: str | None = "493_channel_quote_transport_mode"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.alter_column(
        "ocean_bill",
        "bill_no",
        existing_type=sa.String(length=32),
        nullable=True,
    )
    op.create_index(
        "uq_ocean_bill_org_bill_no",
        "ocean_bill",
        ["organization_id", "bill_no"],
        unique=True,
        postgresql_where=sa.text("bill_no IS NOT NULL"),
    )


def downgrade() -> None:
    op.drop_index("uq_ocean_bill_org_bill_no", table_name="ocean_bill")
    op.execute(
        "UPDATE ocean_bill SET bill_no = 'PENDING-' || SUBSTRING(id::text, 1, 8) "
        "WHERE bill_no IS NULL",
    )
    op.alter_column(
        "ocean_bill",
        "bill_no",
        existing_type=sa.String(length=32),
        nullable=False,
    )
