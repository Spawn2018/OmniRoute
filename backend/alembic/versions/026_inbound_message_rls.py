"""create inbound_message catalog with RLS

Revision ID: 026_inbound_message_rls
Revises: 025_credit_review_rls
Create Date: 2026-09-02
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "026_inbound_message_rls"
down_revision: str | None = "025_credit_review_rls"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "inbound_message",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("source_ref", sa.String(length=512), nullable=False),
        sa.Column("from_address", sa.String(length=320), nullable=False),
        sa.Column("subject", sa.String(length=512), nullable=False),
        sa.Column("body_text", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=8), nullable=False),
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
            name="fk_inbound_message_organization_id",
            ondelete="RESTRICT",
        ),
        sa.CheckConstraint("status = 'draft'", name="ck_inbound_message_status_draft"),
        sa.CheckConstraint(
            "source_ref ~ '^(fixture|synth)://'",
            name="ck_inbound_message_source_fixture",
        ),
    )
    op.create_index("ix_inbound_message_organization_id", "inbound_message", ["organization_id"])
    op.create_index(
        "ix_inbound_message_org_created",
        "inbound_message",
        ["organization_id", "created_at"],
    )

    op.execute("ALTER TABLE inbound_message ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE inbound_message FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY inbound_message_tenant_isolation ON inbound_message
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS inbound_message_tenant_isolation ON inbound_message")
    op.drop_index("ix_inbound_message_org_created", table_name="inbound_message")
    op.drop_index("ix_inbound_message_organization_id", table_name="inbound_message")
    op.drop_table("inbound_message")
