"""create extraction_draft with RLS

Revision ID: 003_extraction_draft_rls
Revises: 002_table_view_rls
Create Date: 2026-08-31
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "003_extraction_draft_rls"
down_revision: str | None = "002_table_view_rls"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "extraction_draft",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="pending"),
        sa.Column("source_ref", sa.String(length=512), nullable=False),
        sa.Column("input_text", sa.Text(), nullable=False),
        sa.Column(
            "payload",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'{}'::jsonb"),
        ),
        sa.Column("reviewed_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("reviewed_at", sa.DateTime(timezone=True), nullable=True),
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
            name="fk_extraction_draft_organization_id",
            ondelete="RESTRICT",
        ),
        sa.CheckConstraint(
            "status IN ('pending', 'accepted', 'rejected')",
            name="ck_extraction_draft_status",
        ),
    )
    op.create_index(
        "ix_extraction_draft_organization_id",
        "extraction_draft",
        ["organization_id"],
    )
    op.create_index(
        "ix_extraction_draft_org_status",
        "extraction_draft",
        ["organization_id", "status"],
    )

    op.execute("ALTER TABLE extraction_draft ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE extraction_draft FORCE ROW LEVEL SECURITY")
    op.execute(
        """
        CREATE POLICY extraction_draft_tenant_isolation ON extraction_draft
        USING (organization_id = NULLIF(current_setting('app.current_org', true), '')::uuid)
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS extraction_draft_tenant_isolation ON extraction_draft")
    op.drop_index("ix_extraction_draft_org_status", table_name="extraction_draft")
    op.drop_index("ix_extraction_draft_organization_id", table_name="extraction_draft")
    op.drop_table("extraction_draft")
