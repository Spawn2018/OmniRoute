"""create tender_bid_stance catalog with RLS FORCE

Revision ID: 121_tender_bid_stance
Revises: 120_tender_prospect
Create Date: 2026-09-09

HITL bid/no-bid: stance_code + source_ref. Nie win/loss. Nie auto-award.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "121_tender_bid_stance"
down_revision: str | None = "120_tender_prospect"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "tender_bid_stance",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("tender_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("stance_code", sa.String(length=16), nullable=False),
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
            name="fk_tender_bid_stance_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "tender_id"],
            ["tender.organization_id", "tender.id"],
            name="fk_tender_bid_stance_tender",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_tender_bid_stance_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "tender_id",
            name="uq_tender_bid_stance_org_tender",
        ),
        sa.CheckConstraint(
            "stance_code IN ('bid', 'no_bid')",
            name="ck_tender_bid_stance_code",
        ),
    )
    op.create_index(
        "ix_tender_bid_stance_organization_id",
        "tender_bid_stance",
        ["organization_id"],
    )
    op.create_index(
        "ix_tender_bid_stance_org_stance",
        "tender_bid_stance",
        ["organization_id", "stance_code"],
    )
    op.execute("ALTER TABLE tender_bid_stance ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE tender_bid_stance FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY tender_bid_stance_tenant_isolation ON tender_bid_stance
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS tender_bid_stance_tenant_isolation ON tender_bid_stance"
    )
    op.drop_index("ix_tender_bid_stance_org_stance", table_name="tender_bid_stance")
    op.drop_index("ix_tender_bid_stance_organization_id", table_name="tender_bid_stance")
    op.drop_table("tender_bid_stance")
