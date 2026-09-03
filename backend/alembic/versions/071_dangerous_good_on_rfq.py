"""attach UN catalog ids to customer_rfq and quotation

Revision ID: 071_dangerous_good_on_rfq
Revises: 070_fraud_flag_rls
Create Date: 2026-09-04

Etykieta ładunku z katalogu M-52. Kwota wyceny nadal z rate_line.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "071_dangerous_good_on_rfq"
down_revision: str | None = "070_fraud_flag_rls"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_unique_constraint(
        "uq_dangerous_good_org_id",
        "dangerous_good",
        ["organization_id", "id"],
    )
    op.add_column(
        "customer_rfq",
        sa.Column("dangerous_good_id", postgresql.UUID(as_uuid=True), nullable=True),
    )
    op.create_foreign_key(
        "fk_customer_rfq_dangerous_good",
        "customer_rfq",
        "dangerous_good",
        ["organization_id", "dangerous_good_id"],
        ["organization_id", "id"],
        ondelete="RESTRICT",
    )
    op.create_index(
        "ix_customer_rfq_org_dangerous_good_id",
        "customer_rfq",
        ["organization_id", "dangerous_good_id"],
    )
    op.add_column(
        "quotation",
        sa.Column("dangerous_good_id", postgresql.UUID(as_uuid=True), nullable=True),
    )
    op.create_foreign_key(
        "fk_quotation_dangerous_good",
        "quotation",
        "dangerous_good",
        ["organization_id", "dangerous_good_id"],
        ["organization_id", "id"],
        ondelete="RESTRICT",
    )
    op.create_index(
        "ix_quotation_org_dangerous_good_id",
        "quotation",
        ["organization_id", "dangerous_good_id"],
    )


def downgrade() -> None:
    op.drop_index("ix_quotation_org_dangerous_good_id", table_name="quotation")
    op.drop_constraint("fk_quotation_dangerous_good", "quotation", type_="foreignkey")
    op.drop_column("quotation", "dangerous_good_id")
    op.drop_index("ix_customer_rfq_org_dangerous_good_id", table_name="customer_rfq")
    op.drop_constraint("fk_customer_rfq_dangerous_good", "customer_rfq", type_="foreignkey")
    op.drop_column("customer_rfq", "dangerous_good_id")
    op.drop_constraint("uq_dangerous_good_org_id", "dangerous_good", type_="unique")
