"""create jit_jis_mark catalog with RLS FORCE

Revision ID: 271_jit_jis_mark
Revises: 276_JIT/JIS_mark
Create Date: 2026-09-12

EXP3.1 HITL znacznik JIT/JIS jako dane. Nie live giełda. Nie silnik JIT.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "277_jit_jis_mark"
down_revision: str | None = "276_offboarding_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "jit_jis_mark",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("mark_code", sa.String(length=32), nullable=False),
        sa.Column("flow_kind", sa.String(length=16), nullable=False),
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
            name="fk_jit_jis_mark_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_jit_jis_mark_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_jit_jis_mark_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_jit_jis_mark_org_source_ref",
        ),
        sa.CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_jit_jis_mark_code",
        ),
        sa.CheckConstraint(
            "flow_kind IN ('jit', 'jis', 'kanban', 'other')",
            name="ck_jit_jis_mark_flow_kind",
        ),
    )
    op.create_index(
        "ix_jit_jis_mark_organization_id",
        "jit_jis_mark",
        ["organization_id"],
    )
    op.execute("ALTER TABLE jit_jis_mark ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE jit_jis_mark FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY jit_jis_mark_tenant_isolation ON jit_jis_mark
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS jit_jis_mark_tenant_isolation ON jit_jis_mark",
    )
    op.drop_index(
        "ix_jit_jis_mark_organization_id",
        table_name="jit_jis_mark",
    )
    op.drop_table("jit_jis_mark")
