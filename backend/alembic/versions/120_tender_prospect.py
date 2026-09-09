"""create tender_prospect catalog with RLS FORCE

Revision ID: 120_tender_prospect
Revises: 119_extraction_draft_tender_rfp
Create Date: 2026-09-09

HITL prospecting: outreach_code + source_ref. Nie scrape. Nie bid/no-bid.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "120_tender_prospect"
down_revision: str | None = "119_extraction_draft_tender_rfp"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "tender_prospect",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("tender_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("party_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("outreach_code", sa.String(length=32), nullable=False),
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
            name="fk_tender_prospect_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "tender_id"],
            ["tender.organization_id", "tender.id"],
            name="fk_tender_prospect_tender",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "party_id"],
            ["party.organization_id", "party.id"],
            name="fk_tender_prospect_party",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_tender_prospect_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "tender_id",
            "party_id",
            name="uq_tender_prospect_org_tender_party",
        ),
        sa.CheckConstraint(
            "outreach_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_tender_prospect_outreach",
        ),
    )
    op.create_index(
        "ix_tender_prospect_organization_id",
        "tender_prospect",
        ["organization_id"],
    )
    op.create_index(
        "ix_tender_prospect_org_tender",
        "tender_prospect",
        ["organization_id", "tender_id"],
    )
    op.execute("ALTER TABLE tender_prospect ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE tender_prospect FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY tender_prospect_tenant_isolation ON tender_prospect
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS tender_prospect_tenant_isolation ON tender_prospect")
    op.drop_index("ix_tender_prospect_org_tender", table_name="tender_prospect")
    op.drop_index("ix_tender_prospect_organization_id", table_name="tender_prospect")
    op.drop_table("tender_prospect")
