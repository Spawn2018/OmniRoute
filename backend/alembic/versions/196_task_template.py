"""create task_template catalog with RLS FORCE

Revision ID: 196_task_template
Revises: 195_consignment
Create Date: 2026-09-10

HITL szablon zadania T5. Nie instancja task. Nie matching. Nie outbox.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "196_task_template"
down_revision: str | None = "195_consignment"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "task_template",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("template_code", sa.String(length=32), nullable=False),
        sa.Column("applies_when", sa.String(length=512), nullable=False),
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
            name="fk_task_template_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_task_template_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "template_code",
            name="uq_task_template_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_task_template_org_source_ref",
        ),
        sa.CheckConstraint(
            "template_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_task_template_code",
        ),
        sa.CheckConstraint(
            "char_length(applies_when) BETWEEN 1 AND 512",
            name="ck_task_template_when",
        ),
    )
    # Lista per tenant — RLS filtruje organization_id; unique kod nie zastępuje skanu.
    op.create_index(
        "ix_task_template_organization_id",
        "task_template",
        ["organization_id"],
    )
    op.execute("ALTER TABLE task_template ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE task_template FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY task_template_tenant_isolation ON task_template
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS task_template_tenant_isolation ON task_template")
    op.drop_index("ix_task_template_organization_id", table_name="task_template")
    op.drop_table("task_template")
