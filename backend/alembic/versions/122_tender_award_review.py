"""create tender_award_review catalog with RLS FORCE

Revision ID: 122_tender_award_review
Revises: 121_tender_bid_stance
Create Date: 2026-09-09

HITL four-eyes: review_code + source_ref. Nie auto-award. Nie win/loss.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "122_tender_award_review"
down_revision: str | None = "121_tender_bid_stance"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "tender_award_review",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("tender_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("review_code", sa.String(length=16), nullable=False),
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
            name="fk_tender_award_review_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "tender_id"],
            ["tender.organization_id", "tender.id"],
            name="fk_tender_award_review_tender",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_tender_award_review_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "tender_id",
            name="uq_tender_award_review_org_tender",
        ),
        sa.CheckConstraint(
            "review_code IN ('countersign', 'challenge')",
            name="ck_tender_award_review_code",
        ),
    )
    op.create_index(
        "ix_tender_award_review_organization_id",
        "tender_award_review",
        ["organization_id"],
    )
    op.create_index(
        "ix_tender_award_review_org_code",
        "tender_award_review",
        ["organization_id", "review_code"],
    )
    op.execute("ALTER TABLE tender_award_review ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE tender_award_review FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY tender_award_review_tenant_isolation ON tender_award_review
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS tender_award_review_tenant_isolation ON tender_award_review"
    )
    op.drop_index("ix_tender_award_review_org_code", table_name="tender_award_review")
    op.drop_index(
        "ix_tender_award_review_organization_id", table_name="tender_award_review"
    )
    op.drop_table("tender_award_review")
