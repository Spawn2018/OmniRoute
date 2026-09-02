"""attach HS/CN catalog ids to customer_rfq and quotation

Revision ID: 031_commodity_on_rfq
Revises: 030_port_surcharge_when
Create Date: 2026-09-03

Etykieta ładunku z katalogu M-09. Kwota wyceny nadal z rate_line.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "031_commodity_on_rfq"
down_revision: str | None = "030_port_surcharge_when"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_unique_constraint(
        "uq_commodity_code_org_id",
        "commodity_code",
        ["organization_id", "id"],
    )
    op.add_column(
        "customer_rfq",
        sa.Column("commodity_code_id", postgresql.UUID(as_uuid=True), nullable=True),
    )
    op.create_foreign_key(
        "fk_customer_rfq_commodity_code",
        "customer_rfq",
        "commodity_code",
        ["organization_id", "commodity_code_id"],
        ["organization_id", "id"],
        ondelete="RESTRICT",
    )
    op.create_index(
        "ix_customer_rfq_org_commodity_code_id",
        "customer_rfq",
        ["organization_id", "commodity_code_id"],
    )
    op.add_column(
        "quotation",
        sa.Column("commodity_code_id", postgresql.UUID(as_uuid=True), nullable=True),
    )
    op.create_foreign_key(
        "fk_quotation_commodity_code",
        "quotation",
        "commodity_code",
        ["organization_id", "commodity_code_id"],
        ["organization_id", "id"],
        ondelete="RESTRICT",
    )
    op.create_index(
        "ix_quotation_org_commodity_code_id",
        "quotation",
        ["organization_id", "commodity_code_id"],
    )


def downgrade() -> None:
    op.drop_index("ix_quotation_org_commodity_code_id", table_name="quotation")
    op.drop_constraint("fk_quotation_commodity_code", "quotation", type_="foreignkey")
    op.drop_column("quotation", "commodity_code_id")
    op.drop_index("ix_customer_rfq_org_commodity_code_id", table_name="customer_rfq")
    op.drop_constraint("fk_customer_rfq_commodity_code", "customer_rfq", type_="foreignkey")
    op.drop_column("customer_rfq", "commodity_code_id")
    op.drop_constraint("uq_commodity_code_org_id", "commodity_code", type_="unique")
