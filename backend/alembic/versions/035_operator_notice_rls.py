"""create operator_notice inbox with RLS FORCE

Revision ID: 035_operator_notice_rls
Revises: 034_operator_decision_rls
Create Date: 2026-09-03

Inbox zapisany per tenant. Nie filtr pending z wycen.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "035_operator_notice_rls"
down_revision: str | None = "034_operator_decision_rls"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "operator_notice",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("kind", sa.String(length=16), nullable=False),
        sa.Column("body", sa.String(length=512), nullable=False),
        sa.Column("status", sa.String(length=8), nullable=False),
        sa.Column("read_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("source_ref", sa.String(length=512), nullable=False),
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
            name="fk_operator_notice_organization_id",
            ondelete="RESTRICT",
        ),
        sa.CheckConstraint("kind = 'manual'", name="ck_operator_notice_kind"),
        sa.CheckConstraint("status IN ('unread', 'read')", name="ck_operator_notice_status"),
        sa.CheckConstraint(
            "(status = 'unread' AND read_at IS NULL) OR "
            "(status = 'read' AND read_at IS NOT NULL)",
            name="ck_operator_notice_read_pair",
        ),
    )
    op.create_index(
        "ix_operator_notice_organization_id",
        "operator_notice",
        ["organization_id"],
    )
    op.create_index(
        "ix_operator_notice_org_created",
        "operator_notice",
        ["organization_id", "created_at"],
    )
    op.execute("ALTER TABLE operator_notice ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE operator_notice FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY operator_notice_tenant_isolation ON operator_notice
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS operator_notice_tenant_isolation ON operator_notice")
    op.drop_index("ix_operator_notice_org_created", table_name="operator_notice")
    op.drop_index("ix_operator_notice_organization_id", table_name="operator_notice")
    op.drop_table("operator_notice")
