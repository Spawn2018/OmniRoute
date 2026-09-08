"""create tender_quote catalog with RLS FORCE

Revision ID: 108_tender_quote
Revises: 107_trip_expected_buy
Create Date: 2026-09-08

Ważność + limit orderów z oferty. Nie auto-award. Nie G2 tender.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "108_tender_quote"
down_revision: str | None = "107_trip_expected_buy"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "tender_quote",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("quotation_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("valid_until", sa.Date(), nullable=False),
        sa.Column("order_limit", sa.Integer(), nullable=False),
        sa.Column("source_ref", sa.String(length=256), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organization.id"],
            name="fk_tender_quote_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "quotation_id"],
            ["quotation.organization_id", "quotation.id"],
            name="fk_tender_quote_quotation",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_tender_quote_org_id"),
        sa.CheckConstraint("order_limit > 0", name="ck_tender_quote_order_limit"),
    )
    op.create_index(
        "ix_tender_quote_organization_id",
        "tender_quote",
        ["organization_id"],
    )
    op.create_index(
        "ix_tender_quote_org_quotation",
        "tender_quote",
        ["organization_id", "quotation_id"],
    )
    op.execute("ALTER TABLE tender_quote ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE tender_quote FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY tender_quote_tenant_isolation ON tender_quote
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS tender_quote_tenant_isolation ON tender_quote")
    op.drop_index("ix_tender_quote_org_quotation", table_name="tender_quote")
    op.drop_index("ix_tender_quote_organization_id", table_name="tender_quote")
    op.drop_table("tender_quote")
