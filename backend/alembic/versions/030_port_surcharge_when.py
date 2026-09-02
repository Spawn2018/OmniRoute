"""index port_surcharge matching on applies_when

Revision ID: 030_port_surcharge_when
Revises: 029_quotation_customer_rfq
Create Date: 2026-09-03

Ewaluacja warunku w SQL — równość po tokenie, nie nowa tabela i nie parser.
"""

from collections.abc import Sequence

from alembic import op

revision: str = "030_port_surcharge_when"
down_revision: str | None = "029_quotation_customer_rfq"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_index(
        "ix_port_surcharge_org_port_when",
        "port_surcharge",
        ["organization_id", "port_id", "applies_when"],
    )


def downgrade() -> None:
    op.drop_index("ix_port_surcharge_org_port_when", table_name="port_surcharge")
