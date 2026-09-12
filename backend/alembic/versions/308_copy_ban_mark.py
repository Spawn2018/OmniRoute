"""create copy_ban_mark catalog with RLS FORCE

Revision ID: 308_copy_ban_mark
Revises: 307_rag_sop_mark
Create Date: 2026-09-12

EXP4.19 HITL znacznik zakazu copy claimów jako dane. Nie copy marketingu. Nie kwota.
"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "308_copy_ban_mark"
down_revision: str | None = "307_rag_sop_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "copy_ban_mark",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("mark_code", sa.String(length=32), nullable=False),
        sa.Column("ban_kind", sa.String(length=16), nullable=False),
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
            name="fk_copy_ban_mark_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_copy_ban_mark_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_copy_ban_mark_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_copy_ban_mark_org_source_ref",
        ),
        sa.CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_copy_ban_mark_code",
        ),
        sa.CheckConstraint(
            "ban_kind IN ('eight_min', 'fifteen_k', 'five_hundred_k', 'other')",
            name="ck_copy_ban_mark_ban_kind",
        ),
    )
    op.create_index(
        "ix_copy_ban_mark_organization_id",
        "copy_ban_mark",
        ["organization_id"],
    )
    op.execute("ALTER TABLE copy_ban_mark ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE copy_ban_mark FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY copy_ban_mark_tenant_isolation ON copy_ban_mark
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS copy_ban_mark_tenant_isolation ON copy_ban_mark",
    )
    op.drop_index(
        "ix_copy_ban_mark_organization_id",
        table_name="copy_ban_mark",
    )
    op.drop_table("copy_ban_mark")
