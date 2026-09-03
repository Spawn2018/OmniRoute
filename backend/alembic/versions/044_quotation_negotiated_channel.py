"""add negotiated_channel_quote_id on quotation

Revision ID: 044_quotation_negotiated_channel
Revises: 043_carrier_inquiry_rls
Create Date: 2026-09-03

Wskazanie oferty kanału. Nie nowa kwota. Nie zamiast margin().
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "044_quotation_negotiated_channel"
down_revision: str | None = "043_carrier_inquiry_rls"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "quotation",
        sa.Column(
            "negotiated_channel_quote_id",
            postgresql.UUID(as_uuid=True),
            nullable=True,
        ),
    )
    op.create_index(
        "ix_quotation_org_negotiated_channel",
        "quotation",
        ["organization_id", "negotiated_channel_quote_id"],
    )


def downgrade() -> None:
    op.drop_index("ix_quotation_org_negotiated_channel", table_name="quotation")
    op.drop_column("quotation", "negotiated_channel_quote_id")
