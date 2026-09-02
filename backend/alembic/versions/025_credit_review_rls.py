"""create credit_review catalog with RLS

Revision ID: 025_credit_review_rls
Revises: 024_channel_quote_rls
Create Date: 2026-09-02
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "025_credit_review_rls"
down_revision: str | None = "024_channel_quote_rls"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "credit_review",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("decision", sa.String(length=8), nullable=False),
        sa.Column("review_date", sa.Date(), nullable=False),
        sa.Column("party_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("note", sa.String(length=512), nullable=True),
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
            name="fk_credit_review_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "party_id"],
            ["party.organization_id", "party.id"],
            name="fk_credit_review_party",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "party_id",
            "review_date",
            name="uq_credit_review_org_party_day",
        ),
        sa.CheckConstraint("decision IN ('ok','hold','refuse')", name="ck_credit_review_decision"),
    )
    op.create_index("ix_credit_review_organization_id", "credit_review", ["organization_id"])

    op.execute("ALTER TABLE credit_review ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE credit_review FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY credit_review_tenant_isolation ON credit_review
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS credit_review_tenant_isolation ON credit_review")
    op.drop_index("ix_credit_review_organization_id", table_name="credit_review")
    op.drop_table("credit_review")
