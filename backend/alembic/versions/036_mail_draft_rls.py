"""create mail_draft beside extract with RLS FORCE

Revision ID: 036_mail_draft_rls
Revises: 035_operator_notice_rls
Create Date: 2026-09-03

Szkic wychodzący obok extractu. Nie czat. Nie send.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "036_mail_draft_rls"
down_revision: str | None = "035_operator_notice_rls"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "mail_draft",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("subject_kind", sa.String(length=32), nullable=False),
        sa.Column("subject_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("body", sa.String(length=2048), nullable=False),
        sa.Column("status", sa.String(length=8), nullable=False),
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
            name="fk_mail_draft_organization_id",
            ondelete="RESTRICT",
        ),
        sa.CheckConstraint(
            "subject_kind = 'extraction_draft'",
            name="ck_mail_draft_subject_kind",
        ),
        sa.CheckConstraint("status = 'draft'", name="ck_mail_draft_status"),
    )
    op.create_index(
        "ix_mail_draft_organization_id",
        "mail_draft",
        ["organization_id"],
    )
    op.create_index(
        "ix_mail_draft_org_created",
        "mail_draft",
        ["organization_id", "created_at"],
    )
    op.execute("ALTER TABLE mail_draft ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE mail_draft FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY mail_draft_tenant_isolation ON mail_draft
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )
    op.drop_constraint(
        "ck_operator_decision_subject_kind",
        "operator_decision",
        type_="check",
    )
    op.create_check_constraint(
        "ck_operator_decision_subject_kind",
        "operator_decision",
        "subject_kind IN ('inbound_message', 'mail_draft')",
    )


def downgrade() -> None:
    op.drop_constraint(
        "ck_operator_decision_subject_kind",
        "operator_decision",
        type_="check",
    )
    op.create_check_constraint(
        "ck_operator_decision_subject_kind",
        "operator_decision",
        "subject_kind = 'inbound_message'",
    )
    op.execute("DROP POLICY IF EXISTS mail_draft_tenant_isolation ON mail_draft")
    op.drop_index("ix_mail_draft_org_created", table_name="mail_draft")
    op.drop_index("ix_mail_draft_organization_id", table_name="mail_draft")
    op.drop_table("mail_draft")
