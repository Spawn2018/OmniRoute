"""create tender_ted_notice catalog with RLS FORCE

Revision ID: 123_tender_ted_notice
Revises: 122_tender_award_review
Create Date: 2026-09-09

HITL TED notice number + source_ref. Nie scrape. Nie live HTTP.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "123_tender_ted_notice"
down_revision: str | None = "122_tender_award_review"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "tender_ted_notice",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("tender_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("notice_number", sa.String(length=64), nullable=False),
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
            name="fk_tender_ted_notice_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "tender_id"],
            ["tender.organization_id", "tender.id"],
            name="fk_tender_ted_notice_tender",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_tender_ted_notice_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "tender_id",
            name="uq_tender_ted_notice_org_tender",
        ),
    )
    op.create_index(
        "ix_tender_ted_notice_organization_id",
        "tender_ted_notice",
        ["organization_id"],
    )
    op.create_index(
        "ix_tender_ted_notice_org_notice",
        "tender_ted_notice",
        ["organization_id", "notice_number"],
    )
    op.execute("ALTER TABLE tender_ted_notice ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE tender_ted_notice FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY tender_ted_notice_tenant_isolation ON tender_ted_notice
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS tender_ted_notice_tenant_isolation ON tender_ted_notice"
    )
    op.drop_index("ix_tender_ted_notice_org_notice", table_name="tender_ted_notice")
    op.drop_index(
        "ix_tender_ted_notice_organization_id", table_name="tender_ted_notice"
    )
    op.drop_table("tender_ted_notice")
