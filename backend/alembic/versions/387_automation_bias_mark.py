"""create automation_bias_mark catalog with RLS FORCE

Revision ID: 387_automation_bias_mark
Revises: 386_risk_register_mark
Create Date: 2026-09-14

AI9.1 HITL katalog mitygacji automation bias. Nie CAPA. Nie auto-naprawa.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "387_automation_bias_mark"
down_revision: str | None = "386_risk_register_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "automation_bias_mark",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("mark_code", sa.String(length=32), nullable=False),
        sa.Column("bias_kind", sa.String(length=16), nullable=False),
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
            name="fk_automation_bias_mark_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "id",
            name="uq_automation_bias_mark_org_id",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_automation_bias_mark_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_automation_bias_mark_org_src",
        ),
        sa.CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_automation_bias_mark_code",
        ),
        sa.CheckConstraint(
            "bias_kind IN ('confirm', 'delay', 'review', 'other')",
            name="ck_automation_bias_mark_kind",
        ),
    )
    op.create_index(
        "ix_automation_bias_mark_organization_id",
        "automation_bias_mark",
        ["organization_id"],
    )
    op.execute("ALTER TABLE automation_bias_mark ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE automation_bias_mark FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY automation_bias_mark_tenant_isolation
        ON automation_bias_mark
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS automation_bias_mark_tenant_isolation ON automation_bias_mark",
    )
    op.drop_index(
        "ix_automation_bias_mark_organization_id",
        table_name="automation_bias_mark",
    )
    op.drop_table("automation_bias_mark")
