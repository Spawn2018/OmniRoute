"""index rate_card applies_when equality leftover P1b

Revision ID: 145_rate_card_match
Revises: 144_shipment_ref
Create Date: 2026-09-09

Równość applies_when w SQL. Nie parser WHEN/IF. Nie T-SQL.
"""

from collections.abc import Sequence

from alembic import op

revision: str = "145_rate_card_match"
down_revision: str | None = "144_shipment_ref"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # Lista po dokładnym applies_when — RLS filtruje organization_id.
    op.create_index(
        "ix_rate_card_org_when",
        "rate_card",
        ["organization_id", "applies_when"],
    )


def downgrade() -> None:
    op.drop_index("ix_rate_card_org_when", table_name="rate_card")
