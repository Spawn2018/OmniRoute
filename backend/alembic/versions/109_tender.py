"""create tender catalog with RLS FORCE

Revision ID: 109_tender
Revises: 108_tender_quote
Create Date: 2026-09-08

Nagłówek przetargu G2.0. Nie loty. Nie przyznanie automatyczne.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "109_tender"
down_revision: str | None = "108_tender_quote"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "tender",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("side", sa.String(length=8), nullable=False),
        sa.Column("kind", sa.String(length=16), nullable=False),
        sa.Column("status", sa.String(length=16), nullable=False),
        sa.Column("buyer_party_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("deadline_at", sa.Date(), nullable=False),
        sa.Column("incoterm", sa.String(length=3), nullable=False),
        sa.Column("trade_side", sa.String(length=8), nullable=False),
        sa.Column("named_place", sa.String(length=256), nullable=False),
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
            name="fk_tender_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "buyer_party_id"],
            ["party.organization_id", "party.id"],
            name="fk_tender_buyer_party",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_tender_org_id"),
        sa.CheckConstraint("side IN ('sell', 'buy')", name="ck_tender_side"),
        sa.CheckConstraint(
            "kind IN ('open', 'restricted', 'sealed', 'e_auction')",
            name="ck_tender_kind",
        ),
        sa.CheckConstraint(
            "status IN ('draft', 'open', 'awarded', 'lost', 'no_bid')",
            name="ck_tender_status",
        ),
    )
    op.create_index("ix_tender_organization_id", "tender", ["organization_id"])
    op.create_index("ix_tender_org_status", "tender", ["organization_id", "status"])
    op.execute("ALTER TABLE tender ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE tender FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY tender_tenant_isolation ON tender
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS tender_tenant_isolation ON tender")
    op.drop_index("ix_tender_org_status", table_name="tender")
    op.drop_index("ix_tender_organization_id", table_name="tender")
    op.drop_table("tender")
