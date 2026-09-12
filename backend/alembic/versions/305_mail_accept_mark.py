"""create mail_accept_mark catalog with RLS FORCE

Revision ID: 304_mail_accept_mark
Revises: 303_funnel_mark
Create Date: 2026-09-12

EXP4.15 HITL znacznik Terms AI jako dane. Nie terms live. Nie CI blob.
"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "305_mail_accept_mark"
down_revision: str | None = "304_terms_ai_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"

def upgrade() -> None:
    op.create_table(
        "mail_accept_mark",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("mark_code", sa.String(length=32), nullable=False),
        sa.Column("accept_kind", sa.String(length=16), nullable=False),
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
        sa.Column("created_by", PGUUID(as_uuid=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organization.id"],
            name="fk_mail_accept_mark_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_mail_accept_mark_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_mail_accept_mark_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_mail_accept_mark_org_source_ref",
        ),
        sa.CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_mail_accept_mark_code",
        ),
        sa.CheckConstraint(
            "accept_kind IN ('mailto', 'confirm', 'reject', 'other')",
            name="ck_mail_accept_mark_accept_kind",
        ),
    )
    op.create_index(
        "ix_mail_accept_mark_organization_id",
        "mail_accept_mark",
        ["organization_id"],
    )
    op.execute("ALTER TABLE mail_accept_mark ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE mail_accept_mark FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY mail_accept_mark_tenant_isolation ON mail_accept_mark
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )

def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS mail_accept_mark_tenant_isolation ON mail_accept_mark",
    )
    op.drop_index(
        "ix_mail_accept_mark_organization_id",
        table_name="mail_accept_mark",
    )
    op.drop_table("mail_accept_mark")
