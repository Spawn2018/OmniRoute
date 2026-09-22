"""create clone_carry_mark catalog with RLS FORCE

Revision ID: 503_clone_carry_mark
Revises: 502_pallet_synchro_mark
Create Date: 2026-09-23

Leftover 528 HITL stance U1 carry przy klonie. Nie auto-copy. Nie similar SQL.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "503_clone_carry_mark"
down_revision: str | None = "502_pallet_synchro_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "clone_carry_mark",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("mark_code", sa.String(length=32), nullable=False),
        sa.Column("carry_kind", sa.String(length=32), nullable=False),
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
            name="fk_clone_carry_mark_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_clone_carry_mark_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_clone_carry_mark_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_clone_carry_mark_org_source_ref",
        ),
        sa.CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_clone_carry_mark_code",
        ),
        sa.CheckConstraint(
            "carry_kind IN ('carry', 'held', 'skip', 'other')",
            name="ck_clone_carry_mark_kind",
        ),
    )
    op.create_index(
        "ix_clone_carry_mark_organization_id",
        "clone_carry_mark",
        ["organization_id"],
    )
    op.execute("ALTER TABLE clone_carry_mark ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE clone_carry_mark FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY clone_carry_mark_tenant_isolation ON clone_carry_mark
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS clone_carry_mark_tenant_isolation ON clone_carry_mark",
    )
    op.drop_index(
        "ix_clone_carry_mark_organization_id",
        table_name="clone_carry_mark",
    )
    op.drop_table("clone_carry_mark")
