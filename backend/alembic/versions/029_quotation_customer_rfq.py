"""link quotation to customer_rfq without a second quote engine

Revision ID: 029_quotation_customer_rfq
Revises: 028_customer_rfq_rls
Create Date: 2026-09-03

Kwota nadal z rate_line. FK tenanta wymaga unique (organization_id, id) na RFQ.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "029_quotation_customer_rfq"
down_revision: str | None = "028_customer_rfq_rls"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_unique_constraint(
        "uq_customer_rfq_org_id",
        "customer_rfq",
        ["organization_id", "id"],
    )
    op.add_column(
        "quotation",
        sa.Column("customer_rfq_id", postgresql.UUID(as_uuid=True), nullable=True),
    )
    op.create_foreign_key(
        "fk_quotation_customer_rfq",
        "quotation",
        "customer_rfq",
        ["organization_id", "customer_rfq_id"],
        ["organization_id", "id"],
        ondelete="RESTRICT",
    )
    op.create_index(
        "ix_quotation_org_customer_rfq_id",
        "quotation",
        ["organization_id", "customer_rfq_id"],
    )


def downgrade() -> None:
    op.drop_index("ix_quotation_org_customer_rfq_id", table_name="quotation")
    op.drop_constraint("fk_quotation_customer_rfq", "quotation", type_="foreignkey")
    op.drop_column("quotation", "customer_rfq_id")
    op.drop_constraint("uq_customer_rfq_org_id", "customer_rfq", type_="unique")
