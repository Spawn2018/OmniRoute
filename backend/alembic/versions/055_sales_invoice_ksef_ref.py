"""add ksef session columns on sales_invoice

Revision ID: 055_sales_invoice_ksef_ref
Revises: 054_sales_invoice_rls
Create Date: 2026-09-03

Zapis numeru sesji. Nie live HTTP. Nie dokument ministerstwa.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "055_sales_invoice_ksef_ref"
down_revision: str | None = "054_sales_invoice_rls"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("sales_invoice", sa.Column("ksef_ref", sa.Text(), nullable=True))
    op.add_column(
        "sales_invoice",
        sa.Column("ksef_noted_at", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("sales_invoice", "ksef_noted_at")
    op.drop_column("sales_invoice", "ksef_ref")
