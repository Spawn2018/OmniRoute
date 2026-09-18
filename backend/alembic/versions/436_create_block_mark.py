"""create create_block_mark catalog with RLS FORCE

Revision ID: 436_create_block_mark
Revises: 435_invoice_match_cand
Create Date: 2026-09-18

C8 HITL create_block_mark. Nie live 409. Nie blocks_create egzekucja.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "436_create_block_mark"
down_revision: str | None = "435_invoice_match_cand"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "create_block_mark",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("mark_code", sa.String(length=32), nullable=False),
        sa.Column("block_kind", sa.String(length=16), nullable=False),
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
            name="fk_create_block_mark_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "id",
            name="uq_create_block_mark_org_id",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_create_block_mark_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_create_block_mark_org_source_ref",
        ),
        sa.CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_create_block_mark_code",
        ),
        sa.CheckConstraint(
            "block_kind IN ('block', 'warn', 'allow', 'other')",
            name="ck_create_block_mark_block_kind",
        ),
    )
    op.create_index(
        "ix_create_block_mark_organization_id",
        "create_block_mark",
        ["organization_id"],
    )
    op.execute("ALTER TABLE create_block_mark ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE create_block_mark FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY create_block_mark_tenant_isolation
        ON create_block_mark
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS create_block_mark_tenant_isolation "
        "ON create_block_mark",
    )
    op.drop_index(
        "ix_create_block_mark_organization_id",
        table_name="create_block_mark",
    )
    op.drop_table("create_block_mark")
