"""store customer_sop.blocks_auto for S10 before send

Revision ID: 033_customer_sop_blocks_auto
Revises: 032_quotation_document_number
Create Date: 2026-09-03

Flaga „nie wolno auto” na istniejącej SOP. customer_sop już ma RLS FORCE.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "033_customer_sop_blocks_auto"
down_revision: str | None = "032_quotation_document_number"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "customer_sop",
        sa.Column("blocks_auto", sa.Boolean(), nullable=False, server_default=sa.true()),
    )


def downgrade() -> None:
    op.drop_column("customer_sop", "blocks_auto")
